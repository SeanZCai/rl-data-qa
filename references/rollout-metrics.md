# Normalized rollout metrics

The helper is a read-only, Python 3.10+ standard-library calculator. Run it against an explicit JSONL export of observed rollout verdicts; do not relabel missing evaluations as failures or fabricate traces to make this format complete.

```json
{"task_id":"task-a","model":"model-a@revision","condition":"baseline","seed":0,"sample_id":"0","status":"pass"}
{"task_id":"task-a","model":"model-a@revision","condition":"baseline","seed":0,"sample_id":"1","status":"environment_failure"}
```

Required: nonempty strings `task_id`, `model`, `condition`, `sample_id`; integer `seed`; `status` exactly `pass`, `fail`, or `environment_failure`. Extra fields are ignored. A `(task_id, model, condition, seed, sample_id)` identifies one attempt and must be unique. Repeated keys, nonstandard JSON constants, malformed records, and empty inputs fail with exit code 2. Valid inputs return JSON to stdout and exit 0, including valid but insufficient evidence; inspect `warnings`.

```bash
python3 scripts/summarize_rollouts.py scores.jsonl --k 1 5 16 --min-samples 16
```

Each task/model/condition/seed cell reports attempts, clean samples `n`, successes `c`, environment failures/rate, observed success per attempted episode, and pass@k **conditional on a clean environment**. Environment failures remain in the attempt denominator and are never classified as model failures. This conditional estimate can be biased as an end-to-end capability estimate when environment failures depend on task or model behavior; report both views and investigate causes.

The estimator assumes exchangeable independent draws under fixed generation conditions. Compare matched cells with an explicit sampling plan. `n < k` yields `null` and a warning, never zero or an extrapolated value. Low sample counts also warn. A cell with only environment failures has `n=0`, no pass@k estimate, and an observed per-attempt success rate of zero.

The script detects absent combinations among observed task IDs and observed model/condition/seed configurations. This rectangular expectation is a diagnostic, not proof that your study intended a full grid. It cannot detect tasks or configurations never mentioned anywhere in the input. Reconcile against the external task and run manifest before making coverage claims.

It does not compute confidence intervals, bootstrap comparisons, quality labels, training-band acceptance, rubric semantics, contamination, human agreement, or a release decision. It does not check that a score agrees with the actual trace or verify provenance. Use the appropriate protocol references and raw artifacts for those checks.
