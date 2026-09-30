## Stage 3. Packaging for lab delivery

A lab researcher making a buy decision needs to answer six core questions from your materials within a few days. Structure the delivery package to make each one answerable without digging. When the Mode Declaration says benchmark, use [Question 1B](#question-1b-does-this-discriminate) instead of [Question 1](#question-1-is-this-trainable) and [Question 4B](#question-4b-is-the-rubric-tight-enough) instead of [Question 4](#question-4-does-training-on-it-help); the B questions are mode-specific substitutions, not additions.

### Question 1. Is this trainable?

Provide the pass@k curves and hillclimbness analysis from your own testing (stage 2), not just the vendor's reported numbers. Show which tasks fall in the core productive training band (pass@1 in [0.25, 0.75]), which fall only in the optional widened curriculum range [0.1, 0.9] with the two tails reported separately, and which are too easy or too hard. Report the mean score distribution across tasks and declare the k and n used for every pass@k estimate.

### Question 1B. Does this discriminate?

Applies when the Mode Declaration says benchmark or both. Cite [M11](requirements.md#m11-benchmark-only-discrimination-index) (discrimination index), [M5](requirements.md#m5-both-cross-model-evaluation-with-unbiased-passk) (cross-model pass@k spread), the per-task variance distribution, and the [M4](requirements.md#m4-both-multi-surface-contamination-report-and-agent-invisible-canaries) contamination report. A benchmark that distinguishes capability tiers has top-frontier-model standard deviation above 0.10 on the majority of tasks, with saturation (mean above 0.90) and floor (mean below 0.10) tasks combined under 30%. A benchmark whose tasks appear in pretraining N-gram analysis above the [M4](requirements.md#m4-both-multi-surface-contamination-report-and-agent-invisible-canaries) threshold is measuring memorization, not capability, and cannot answer Q1B affirmatively regardless of discrimination index.

### Question 2. Is this real?

Provide the provenance chain for each task. If tasks come from real-world workflows, explain the pipeline from raw data to training example. If they're contrived, explain why the contrivance maps to real work and who built it (years of experience, domain). Include the provenance scoring from intake review.

Include the economic grounding statement and the value-tier distribution from intake. Faithful provenance is necessary and not enough. A cleanly sourced task that captures commodity work still trains a commodity capability. Show that the task set is weighted toward the high-value tier of the domain rather than its busywork.

### Question 3. Is the grading correct?

Include the grader source code, the rubric definitions, and at least one end-to-end worked example showing a model trace being graded against the rubric with explanations for each criterion's pass/fail result. Include your reward hacking probe results from stage 2. If you found and fixed grader gaps, describe what you changed and why.

### Question 4. Does training on it help?

Show before/after performance: base model vs. post-trained model on held-out tasks from the same domain. Report pass@1 and mean score improvement. If you used SDFT, include the log-probability shift distribution as supporting evidence. If you used RL, show the reward curve over training steps.

### Question 4B. Is the rubric tight enough?

Applies when the Mode Declaration says benchmark or both. Cite [M13](requirements.md#m13-benchmark-only-pass-condition-tightness-audit) (pass-condition tightness audit) and [M12](requirements.md#m12-benchmark-only-anti-pattern-penalty-audit) (anti-pattern penalty audit). A rubric whose pass conditions reward concept presence rather than capability demonstration produces benchmarks that rank verbose models above competent ones. Tightness ratio above 0.30 (more than 30% of sampled criteria satisfiable by minimum-effort output) and anti-pattern separation ratio below 0.80 are both rejection criteria, independent of any other quality signal.

### Question 5. Does it break anything?

Include the catastrophic forgetting check results from stage 2. Show general-capability eval scores before and after training. If it's a multi-domain dataset, show the sequential training results with per-domain retention.

### Question 6. Is the environment architecture sound?

Provide the environment specification. Sandbox configuration, snapshot and replay capability, tool fidelity, cloudbox or simulation tier if applicable, and any known divergence from the production system the environment represents. Include agent trace artifacts in a format that allows a reviewer to re-run a rollout to the same result. A dataset whose environment cannot be reproduced is not evaluable downstream regardless of how strong the tasks and rubrics look on paper. This question becomes primary for data covering SDLC, DevOps, production-cloud workflows, and any other domain where the environment is load-bearing for the task.

Include the environment failure rate from stage 2 and the concurrency it was measured at, together with the harness load-test results. An environment whose failure rate exceeds five percent, or whose reliability was never measured under the concurrency the buyer will train at, is not evaluable downstream however faithful the tools and tasks look.

### Delivery format

Package the dataset and QC results as:

- **Dataset files** in JSON-lines format with schema documentation
- **QC report** (active-testing results, formatted per the six core questions above with the mode-appropriate Q1/Q1B and Q4/Q4B substitutions)
- **Grader source code**, runnable, with a README
- **Model traces:** at least 3 per task, in raw format with tool calls preserved
- **Run configurations:** per-rollout, not per-dataset
- **Cross-model results:** tabular, with confidence intervals
- `MODE_DECLARATION.json` and (for dual-mode datasets) `PARTITION_MANIFEST.json` at the repository root

Do not include: marketing materials, narrative descriptions of what the data could be used for, benchmarks without underlying data, or summary statistics without distributions.

After completing all three stages, classify the dataset:
