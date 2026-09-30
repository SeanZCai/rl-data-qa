import importlib.util
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'summarize_rollouts.py'
spec = importlib.util.spec_from_file_location('metrics', SCRIPT)
metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metrics)


def row(sample='0', status='pass', **extra):
    return {'task_id': 'a', 'model': 'm', 'condition': 'base', 'seed': 0,
            'sample_id': sample, 'status': status, **extra}


def summarize(rows, **kwargs):
    return metrics.summarize(enumerate(rows, 1), **kwargs)


class MetricsTests(unittest.TestCase):
    def test_estimator_against_all_subsets(self):
        for n in range(1, 9):
            for c in range(n + 1):
                for k in range(1, n + 1):
                    draws = list(itertools.combinations(range(n), k))
                    expected = sum(any(i < c for i in draw) for draw in draws) / len(draws)
                    self.assertAlmostEqual(metrics.pass_at_k(n, c, k), expected, places=14)

    def test_pass_one_is_empirical_fraction(self):
        self.assertAlmostEqual(metrics.pass_at_k(16, 4, 1), 0.25)

    def test_not_plugin_estimator_or_consistency(self):
        actual = metrics.pass_at_k(4, 2, 2)
        self.assertAlmostEqual(actual, 5 / 6)
        self.assertNotAlmostEqual(actual, 1 - (1 - 2 / 4) ** 2)
        self.assertNotAlmostEqual(actual, (2 / 4) ** 2)

    def test_invalid_counts(self):
        for args in [(3, 4, 1), (3, -1, 1), (0, 0, 1), (3, 1, 4), (3, 1, 0), (True, 1, 1)]:
            with self.assertRaises(ValueError):
                metrics.pass_at_k(*args)

    def test_environment_failure_denominators(self):
        result = summarize([row('0'), row('1', 'fail'), row('2', 'environment_failure')], ks=[1, 3])
        group = result['groups'][0]
        self.assertEqual((group['attempts'], group['n'], group['c']), (3, 2, 1))
        self.assertEqual(group['conditional_pass_at_k'], {'1': 0.5, '3': None})
        self.assertAlmostEqual(group['environment_failure_rate'], 1 / 3)
        self.assertAlmostEqual(group['success_per_attempt'], 1 / 3)
        self.assertEqual(result['release_readiness'], 'not_assessed')

    def test_all_environment_failures_do_not_become_model_failures(self):
        group = summarize([row(status='environment_failure')])['groups'][0]
        self.assertEqual(group['n'], 0)
        self.assertEqual(group['conditional_pass_at_k'], {'1': None, '5': None})
        self.assertEqual(group['environment_failure_rate'], 1)

    def test_cells_stay_separate_and_missing_grid_is_reported(self):
        result = summarize([row('0'), row('0', task_id='b'), row('0', model='m2'),
                            row('0', condition='treatment'), row('0', seed=1)])
        self.assertEqual(len(result['groups']), 5)
        self.assertEqual(len(result['missing_observed_cells']), 3)
        self.assertEqual(result['attempts'], 5)

    def test_duplicate_attempt_rejected(self):
        with self.assertRaises(metrics.InvalidRecords):
            summarize([row(), row(status='fail')])

    def test_invalid_schema_rejected(self):
        for value in [[], None, 1, 'pass', row(seed=True), row(seed=1.0),
                      row(status='error'), row(status=[]), row(sample_id=1),
                      row(task_id=' '), row(model=None)]:
            with self.subTest(value=value), self.assertRaises(metrics.InvalidRecords):
                summarize([value])

    def test_empty_and_invalid_options_rejected(self):
        for rows, kwargs in [([], {}), ([row()], {'ks': [0]}),
                             ([row()], {'ks': []}), ([row()], {'min_samples': 0})]:
            with self.assertRaises(ValueError):
                summarize(rows, **kwargs)

    def run_cli(self, content, *args):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'scores.jsonl'
            source.write_text(content)
            before = source.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), *args],
                                    capture_output=True, text=True)
            self.assertEqual(source.read_bytes(), before)
            return result

    def test_cli_valid_input_and_warning_are_json(self):
        result = self.run_cli(json.dumps(row()) + '\n', '--k', '1', '5')
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload['groups'][0]['conditional_pass_at_k'], {'1': 1.0, '5': None})
        self.assertEqual(payload['uncertainty'], 'not_computed')
        self.assertTrue(payload['warnings'])
        self.assertEqual(result.stderr, '')

    def test_cli_rejects_malformed_duplicate_keys_and_nonfinite_json(self):
        for content in ['{bad}\n', '{"task_id":"a","task_id":"b"}\n',
                        json.dumps(row())[:-1] + ',"extra":NaN}\n', ' \n']:
            result = self.run_cli(content)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, '')
            self.assertIn('error:', result.stderr)

    def test_strings_are_data_and_never_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / 'never-create'
            malicious = f'$(touch {sentinel})'
            result = self.run_cli(json.dumps(row(task_id=malicious)))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)['groups'][0]['task_id'], malicious)
            self.assertFalse(sentinel.exists())

    def test_rare_success_numerical_stability(self):
        self.assertTrue(math.isclose(metrics.pass_at_k(10**12, 1, 1), 1e-12, rel_tol=1e-12))


if __name__ == '__main__':
    unittest.main()
