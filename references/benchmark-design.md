## Benchmark-aligned RL and evaluation design

This section defines release requirements for any dataset marketed as benchmark-aligned RL, agentic evaluation, or long-horizon professional work. Frequency in model cards is evidence of buyer attention, not evidence that training on benchmark replicas causes general capability transfer. Alignment claims therefore require an explicit transfer contract, clean information-flow boundaries, and results reported under reproducible evaluation surfaces.

### 1. Benchmark-aligned RL without leakage

Train on construct-matched sibling tasks that exercise the same skill cluster, not on released benchmark items, solutions, distinctive templates, benchmark-specific assets, grader internals, or answer-bearing tool schemas. The benchmark evaluation split remains private and outside the training and reward-development loop. A vendor may claim benchmark alignment only when improvement transfers to private family holdouts and at least one independently implemented evaluation surface.

- **Define the target construct and observable task events that measure it.** A matching topic, output format, or vocabulary is not a transfer claim.
- **Pre-register the expected direction of transfer**, the held-out benchmarks or realistic work simulations, the expert-rating check, and ablations that remove tools, sources, state, or intermediate calculations.
- **Classify every artifact as agent-visible, tool-mediated, verifier-only, or publication-only.** Reference answers, canaries, hidden tests, grader targets, and evaluation seeds remain unreachable from the agent container and the task-authoring model.

### 2. `BENCHMARK_ALIGNMENT.json` and sibling task splits

Any benchmark-aligned RL claim ships `BENCHMARK_ALIGNMENT.json` at the bundle root. Required fields are: schema_version; dataset_version; target_benchmark_families and exact versions; target_skill_clusters; alignment_claims; prohibited_training_material; construct_to_observable_event_map; sibling_generator manifests; split_manifest; information_flow_manifest; leakage_controls; transfer_evaluations; ablations; expert_validation; foreign_harness_results; and refresh_policy. Every claim points to raw result artifacts rather than narrative-only evidence.

- **Each sibling generator records** its code commit and hash, parameter schema, valid ranges, constraint checks, source and asset licenses, seed policy, generated-instance hashes, and reviewer sign-off. The generator must vary task substance, not merely names or numbers.
- **Use family-level splits:** training_siblings, tuning_siblings, private_family_holdout, and benchmark_evaluation. Separate families across template, source, asset, interface, and seed boundaries; do not randomly split near-duplicate instances across train and evaluation.
- **Run exact, semantic, structural, template, asset, and tool-schema overlap checks across every split.** Record all adjudicated matches and prove that private seeds, assets, canaries, and grader targets are not reachable from the training or agent-visible surfaces.

### 3. Full harness and resource envelope

A score is a property of a model, task set, harness, and resource envelope together. Publish a machine-readable run manifest that pins the model name and checkpoint or API revision; system, developer, and user prompts or hashes; harness commit; container image digest; environment snapshot; scorer and judge revisions; tool registry and schemas; network and permission policy; retry and recovery policy; context and compaction policy; maximum turns; wall-clock timeout; concurrency; hardware and software stack; and all sampling parameters.

- **Report per-rollout input, output, cache, and tool-result tokens;** per-agent and all-agent totals; critical-path and aggregate wall clock; tool calls; cost; failures; retries; and state-snapshot volume.
- **Treat missing resource fields as unknown, not zero.** Results with materially different prompts, tools, agent counts, reasoning budgets, context policies, or judge versions are different evaluation surfaces and are not silently pooled.
- **Smoke-test the published image and entry point** under the declared network, permissions, concurrency, and timeout limits. Reconcile manifest totals to raw traces before release.

### 4. Multi-agent, reasoning-effort, and tool-surface curves

Single headline points hide scaffold confounding. For representative tasks, estimate response curves across agent count, reasoning-effort or compute budget, and tool surface while holding the remaining envelope fixed. At minimum include a single-agent baseline, the marketed multi-agent condition, a low and high reasoning-effort condition, and tool ablations that remove or replace each load-bearing tool family.

- **For multi-agent curves,** report topology, agent roles, communication channel, shared-state policy, delegation limit, per-agent budget, all-agent budget, critical-path latency, aggregate compute, cost, and coordination failures at each point.
- **For reasoning-effort curves,** report the provider setting or explicit compute budget and measure both quality and efficiency. Do not equate hidden reasoning tokens with task horizon or require their disclosure.
- **For tool-surface curves,** vary tool availability, fidelity, schema verbosity, permissions, and failure injection. A result that collapses when a distinctive schema or answer-bearing retrieval tool is removed is a surface dependency, not demonstrated general capability.
- **Plot score with paired uncertainty** against all-agent tokens, cost, and critical-path wall clock. Publish the full curve and Pareto frontier rather than selecting only the best-scoring scaffold.

### 5. Dynamic, stateful, and editable-artifact tasks

Tasks advertised as dynamic, stateful, computer-use, ERP, or editable-artifact work must exercise those properties in the scored harness. A read-only workflow that produces a plan is labeled planning, not execution. Dynamic families vary source data, timestamps, permissions, partial failures, and conflicting state under private seeds while preserving a verifiable objective.

- **Ship pre-state, observable intermediate state, post-state, intended deltas, forbidden side effects, and immutable audit logs.** Score exact state changes, idempotency, concurrency behavior, rollback, and recovery from stale data, tool failure, interruption, and partial completion.
- **Use mutating tools when the capability claim is action-taking.** Verify permission boundaries and safe escalation or abstention; a textual promise to act does not satisfy a state-changing criterion.
- **For documents, spreadsheets, slides, code, images, or other editable artifacts,** ship the native file and validate both semantic correctness and artifact integrity. Include reopen/edit checks, formulas or executable behavior where applicable, layout or render checks, provenance, and diffable final artifacts rather than grading prose descriptions alone.

### 6. Judge bias, length bias, and observable evidence

Pin every LLM judge by provider, model, revision, full prompt, temperature, schema, retry policy, cache key, and position-swap policy. Calibrate against qualified humans on a stratified sample and report criterion-level agreement, repeated-judge stability, false positives, false negatives, abstentions, and infrastructure failures. The judge cites observable transcript, tool, state, rubric, and final-output evidence; private chain-of-thought is neither requested nor treated as ground truth.

- **Run length-matched counterfactuals**, concise-versus-verbose rewrites with meaning held constant, answer-order swaps, style and format perturbations, and decoy-detail tests. Report score change by criterion and model.
- **Rubric criteria reward required evidence and task completion**, not concept count, citation count, or output length. When length legitimately improves completeness, show that the gain survives criterion-level evidence verification and required-artifact ablation.
- **Keep deterministic checks, LLM judgments, cascade adjustments, and final contributions in a per-criterion reward ledger** so length and judge effects can be audited independently.

### 7. Saturation monitoring and refresh

Every benchmark and sibling family declares a saturation review cadence and pre-registered refresh triggers. Signals include sustained ceiling clustering, compressed cross-model spread, low item variance, weak rank stability, loss of predictive validity on external held-outs, shortcut discovery, contamination evidence, or a new model generation that moves a material share of tasks out of the intended band. No universal calendar or score threshold fits every domain.

- **Refresh from the underlying objective and generator**, not by selecting only items that the current frontier model fails. Filter-for-failure creates anti-correlated, short-lived sets and confounds capability progress with construction policy.
- **Version generators, assets, rubrics, judges, harnesses, and model cohorts separately.** Preserve frozen anchor items and bridging studies so longitudinal comparisons remain interpretable while private replacement families restore discrimination.
- **After every refresh, rerun contamination, verifier soundness, judge calibration, surface curves, cross-model pass@k, paired uncertainty, and expert-validity checks** before publishing a new headline score.

### 8. Evaluation card and separated composite indices

Ship `EVAL_CARD.md` and a machine-readable `EVAL_CARD.json`. The card states the intended construct and use; mode; task-family and split design; provenance and licenses; population and exclusions; harness and resource envelope; tool and state surfaces; models, sample sizes, seeds, and uncertainty; verifier and judge evidence; contamination controls; expert review; known limitations and misuse risks; saturation status; refresh policy; and exact links to raw artifacts. Report results by exact evaluation condition before any roll-up.

- **Keep capability, safety and alignment, efficiency and cost, and reliability and recovery as separate scorecards.** Do not merge them into one unlabeled quality number or let strength on one axis cancel failure on another.
- **Every composite is explicitly labeled composite** and publishes its components, units, normalization, weights, aggregation formula, uncertainty, missing-data rule, and sensitivity to alternative weights. Missing results remain missing, never zero.
- **Do not double-count a component and a composite containing that component** in frequency tables, portfolio coverage, or overall rankings. Preserve exact benchmark versions and incompatible scoring methods as separate rows even when a canonical-family view is also provided.
