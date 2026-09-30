# SFT intake assessment

The four-pair fixture passes local format and response-integrity checks. **Broader SFT intake readiness remains unestablished**: target-model scope, base-model evaluation, held-out performance, and reproducible construction provenance are absent. This is a complete intake-only assessment of the supplied fixture, not a production-readiness or training-benefit claim.

## Contract and scope

- Dataset: `synthetic-test-1`; declared use: training; method: SFT; requested stage: intake only.
- Declared task type: string transformations; source: programmatically constructed toy examples; license: CC0-1.0. These are manifest claims, not independently verified provenance or licensing evidence.
- The manifest expressly calls this a tiny synthetic fixture, not a production dataset. Target model, capability band, and broader task-value claim are unspecified.
- A fixed four-row artifact is present. Regeneration support is unspecified; no generator is supplied.
- Inspected both supplied files in full. No sampling, training, model calls, network calls, or input changes. Dataset contents were treated only as audit material.

## Evidence ledger

Paths below are relative to `evals/fixtures/sft/`; all evidence is version `synthetic-test-1`.

| Check | Applicability and criterion | Artifact / rows | Observed result | Status | Remediation |
|---|---|---|---|---|---|
| SFT-01 Contract | SFT intake requires method/use identification | `manifest.json` | Training, SFT, intake only explicitly declared | PASS | Specify intended target model and capability objective before interpreting evaluation results |
| SFT-02 Pair format | SFT requires intact prompt-response pairs and consistent counts | `manifest.json`; `pairs.jsonl` lines 1–4, IDs `0`–`3` | 4/4 parse; 4/4 contain nonempty string ID, prompt, response, source; actual count 4 equals declared count 4 | PASS | None for this check; original-context completeness is not independently established |
| SFT-03 Identity and duplication | Pair integrity requires usable identities and duplicate accounting | `pairs.jsonl` lines 1–4 | 4 unique IDs; 0 exact duplicate prompt-response pairs out of 4 | PASS | Check family/semantic overlap when a larger corpus and split are available |
| SFT-04 Response correctness | These simple transformations can be checked directly without an RL grader | `pairs.jsonl`: IDs `0`, `1`, `2`, `3` | Expected outputs `GREEN`, `BLUE`, `tac`, `god`; 4/4 supplied responses match | PASS | None for these four examples; this is label validation, not model performance |
| SFT-05 Provenance | SFT pair provenance must substantiate construction claims | `manifest.json`; all pair source fields | 4/4 sources match the version; synthetic source and license are declared, but construction code/history and supporting provenance are absent | MISSING_EVIDENCE | Supply generator/version and construction provenance sufficient to reproduce the pairs and support the license claim |
| SFT-06 Review evidence | Record review honestly; automated checks do not establish human review | `manifest.json`: `review_pass_count` | Declared review passes: 0; no human annotations or review records supplied | MISSING_EVIDENCE | Retain this disclosure; define any additional review needed for the intended use |
| SFT-07 Base and held-out evaluation | SFT intake uses base-model prompt performance and cross-model held-out performance | `manifest.json`; complete two-file bundle | Base-model evaluation explicitly unavailable; no held-out split, evaluation results, model IDs, seeds, or evaluation protocol | MISSING_EVIDENCE | Declare model panel and evaluation construct; provide held-out partition/provenance and reproducible evaluation evidence |
| SFT-08 Coverage | Intake should characterize what the pairs represent | `pairs.jsonl` lines 1–4; `manifest.json` | Auditor-inferred families: uppercase 2/4, reverse 2/4. No per-pair declared taxonomy or broader coverage evidence | MISSING_EVIDENCE | Document the intentionally narrow scope and family assignments; do not infer general capability from four pairs |
| SFT-09 RL artifacts | RL graders, reward rubrics, rollout traces, and RLVR training-band quotas are not conditions of SFT pair-data intake | Declared SFT method | No RL artifacts supplied; none needed for the checks above | NOT_APPLICABLE | None |
| SFT-10 Training diagnostics | Log-probability shifts and forgetting checks apply later in an SFT QA pipeline, outside this request | `manifest.json`: `post_training_run_available` | No post-training run available; no diagnostics executed | NOT_RUN | Scope these only after intake gaps are resolved and execution is separately authorized |

## Next applicable checks

1. Complete the lightweight SFT contract: target model class, intended learning objective, fixed versus regenerable status, construction provenance, and declared task families. Keep the toy-only designation explicit.
2. Define a held-out set with separate prompts and documented construction/split rules. Check exact and family-level overlap before any evaluation claim; four training examples alone cannot establish generalization.
3. Specify and obtain base-model and cross-model held-out evaluation evidence. For these transformations, direct output comparison is sufficient; an RL reward system is unnecessary. Record model/version, prompt context, decoding settings, row IDs, seeds, sample counts, and scoring normalization. If pass@k is used, require `n >= k` and the unbiased estimator. Stop interpretation if the split leaks or scoring/context is unspecified. No model evaluation was run here.
4. After an applicable intake decision and separate authorization, plan SFT log-probability shifts and matched retention checks. This is a proposed later stage, not an intake experiment or permission to train.

## Reproducibility and limits

SHA-256 of the inspected bytes:

```text
manifest.json  d17f8e4dc4a99d9d6c002fd7dbe7169f07b3c67270322d76d0f79cc5680ba282
pairs.jsonl    9dba344b922e46ba6dd6ff541d5f2fbb9eef27c1f01c2da84945d653b65601c4
```

Checks used Python standard-library JSON parsing, SHA-256, field/type checks, ID and exact-pair sets, and direct `str.upper()` / reverse slicing on each prompt payload. Denominator: all 4 supplied rows; no random seed or bootstrap applies to this exhaustive fixture inspection. The 4/4 correctness result measures these labels only. No source repository, human review, model behavior, training benefit, retention, or broader population quality was verified.

Applied `SKILL.md` and its `references/modes.md` and `references/intake.md`, with the explicit SFT overrides controlling applicability.
