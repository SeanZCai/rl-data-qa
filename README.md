# RL Data QC/QA — Beta

An impromptu skill for Codex and Claude Code that turns the **QC for RL Data** protocol into an evidence-based dataset audit. It covers intake, active testing, failure attribution, and delivery readiness for RLVR, benchmarks, SFT/SDFT, RLHF, DPO, and agentic data without deterministic verifiers.

The skill selects checks by dataset use and training method, traces findings to actual artifacts, and keeps missing evidence separate from failed tests. Detailed procedures and research citations are bundled as references, so it works without fetching the article.

**Beta:** thresholds are proposed protocol criteria and need domain calibration. The skill assists an audit; it does not certify data quality. Qualified human reviews and empirical experiments cannot be replaced by generated assertions.

## Install

Requires an agent with local file access. The optional metrics helper and tests require Python 3.10+; no Python packages, API keys, or MCP servers are needed for the helper.

### Codex

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/SeanZCai/rl-data-qa.git "$HOME/.agents/skills/rl-data-qa"
```

Start a new session, then invoke:

```text
$rl-data-qa Audit ./dataset for RLVR intake readiness. Report blockers and missing evidence.
```

Codex's documented user skill location is `~/.agents/skills`; repository skills can live in `.agents/skills`. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

### Claude Code

```bash
mkdir -p "$HOME/.claude/skills"
git clone https://github.com/SeanZCai/rl-data-qa.git "$HOME/.claude/skills/rl-data-qa"
```

Start a new session, then invoke:

```text
/rl-data-qa Audit ./dataset as a pure benchmark. Assess discrimination and verifier evidence.
```

For a shared project installation, use `.claude/skills/rl-data-qa` in that repository. See the [official Claude Code skill documentation](https://code.claude.com/docs/en/skills). Both hosts use the same `SKILL.md` and relative resources; there are no host-specific tools in the workflow.

Clone into a new folder; these commands do not overwrite an existing installation. To reproduce this release, check out `v0.1.0-beta.1` in the clone.

## Use

Supply the dataset or a local artifact bundle, the intended use, and the scope of the review. Useful requests include:

- “Review this SFT dataset's intake evidence. Do not run training.”
- “Check whether this rubric and verifier audit support the benchmark's release claim.”
- “Triage these failed observable trajectories into prompt, harness, and capability failures.”
- “Design the smallest authorized experiment that would test the training-value claim.”

The result is a readiness assessment, evidence ledger, blockers, and next checks. Full release assessment follows applicable M1–M19 requirements; narrow questions stay narrow. Dataset text and task instructions are treated as evidence, not as instructions to the auditor. The workflow does not request private chain-of-thought.

## Metrics helper

From the installed skill folder:

```bash
python3 scripts/summarize_rollouts.py evals/fixtures/benchmark/scores.jsonl --k 1 5
```

The helper validates normalized rollout records and computes unbiased pass@k per task/model/condition/seed. It preserves environment-failure accounting, reports unsupported estimates as `null`, and flags low sample counts or missing observed cells. Its output is **metrics only**, never a release verdict. See the [input contract and statistical limits](references/rollout-metrics.md).

## Test

```bash
python3 -m unittest discover -s tests -v
```

Tests cover the estimator against enumerated sample subsets, schema failures, duplicate attempts, environment-failure denominators, unsupported k, cell coverage, CLI behavior, resource links, and reference discoverability. GitHub Actions runs the same suite on pushes and pull requests.

The [behavioral evaluations](evals/README.md) contain synthetic fixtures, prompts, acceptance criteria, and the observed results. They are small smoke tests, not a comprehensive evaluation of the protocol or either agent platform.

## Protocol interpretation

The references preserve the article's procedures and internal cross-references. The entrypoint supplies method-specific applicability and clarifies three statistical ambiguities: `c/n` is correct for pass@1; productive training-band quotas do not apply to pure benchmarks; and verifier-conditioned error rates must not be mislabeled as conventional truth-conditioned FPR/FNR. Frontier-shape cutoffs remain provisional heuristics. These clarifications take precedence when using the skill.

[Start with the skill instructions](SKILL.md). Released under the [MIT license](LICENSE).
