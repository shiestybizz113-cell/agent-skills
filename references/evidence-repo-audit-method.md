# Evidence Repo Audit Method

This reference adapts the strongest reusable ideas from the public
[Ontos v4.7.0 comprehensive repo audit](https://github.com/ohjonathan/Project-Ontos/blob/bd04620376ed6a8d0024e990e04a86da402b9398/docs/reviews/2026-07-02-fable-repo-audit.md).
It is a behavioral and reporting standard, not a copy of the audit and not a
model runtime.

## Audit dimensions

Use every dimension that applies and mark the others `NOT CHECKED`.

1. Architecture and boundary ownership
2. Data integrity and round-trip safety
3. Write paths, locking, rollback, and idempotency
4. Security, authority, secrets, and trust boundaries
5. Legacy code, duplication, dead paths, and release coupling
6. Unit, integration, end-to-end, and failure-path testing
7. CLI, API, MCP, UI, and machine-contract consistency
8. Documentation, agent context, and contributor clarity
9. Configuration, environment dependence, and hardcoded values
10. Performance, concurrency, scaling, and resource limits
11. Packaging, CI, deployment, rollback, and release readiness
12. Observability, evidence, receipts, and incident diagnosis
13. Product purpose-fit and claimed-versus-delivered behavior
14. Cross-repository drift and duplicated sources of truth
15. Change attribution, regression timing, and ownership

## Evidence states

- `CONFIRMED`: directly reproduced or supported by exact primary evidence
- `REFUTED`: a targeted attempt disproved the claim
- `UNVERIFIED`: plausible but not proven with available access
- `NOT CHECKED`: intentionally outside the completed inspection

Never silently convert an unverified claim into a finding.

## Finding contract

Every finding must contain:

```text
ID:
Severity: P0 | P1 | P2
Status: CONFIRMED | REFUTED | UNVERIFIED | NOT CHECKED
Claim:
Evidence:
Impact:
Fix:
Verification:
```

Keep the claim falsifiable. Prefer “command X rewrites valid YAML into an
unparseable file” over “serialization is bad.”

## Refutation contract

For every P0 and high-impact P1, give a fresh reviewer only:

- the isolated claim
- the evidence
- the expected contract
- instructions to find a counterexample or disprove the claim

Do not give the reviewer the original author’s reasoning. Reconcile the
reviewer’s response against the primary artifact; never treat a second model as
authority.

Use provider-neutral language. External reviewers require explicit user
authorization. Local or already-approved reviewers are preferred when privacy
or system canon is involved.

## Report order

1. Executive summary and honest health assessment
2. Top five actions
3. Confirmed finding totals by severity
4. What is working well
5. Scope and exclusions
6. Finding register
7. Refuted and unverified claims
8. Execution roadmap
9. Verification record

## Roadmap order

- **Now:** release blockers, data loss, authority bypass, and cheap high-value
  corrections
- **Next:** characterization tests followed by parser, interface, write-path,
  and consistency fixes
- **Later:** coordinated migrations, large refactors, repo slimming, and
  archival work

Rewire before retirement. Verify before archive. Archive before deletion.

## Supporting public patterns

The following public Anthropic repositories reinforce specific parts of this
method without becoming runtime dependencies:

- [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks):
  evaluation cases should separate input, produced output, expected answer or
  rubric, and score. Prefer deterministic grading when the contract is exact;
  use human or model grading only when judgment is unavoidable.
- [Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins):
  keep domain instructions, explicit commands, and external connectors as
  separate surfaces. Audit each surface and the handoffs between them instead
  of treating a plugin description as proof that a connector works.
- [Anthropic CLI](https://github.com/anthropics/anthropic-cli):
  treat authentication, session state, structured output, and API execution as
  explicit runtime boundaries. Do not claim a CLI-backed verification ran
  unless the binary, authentication, invocation, and returned result were
  checked.
- [Buffa](https://github.com/anthropics/buffa):
  prefer conformance suites over happy-path claims, publish benchmark
  methodology with raw measurements, state unsupported features and known
  limitations, and name the stability surface separately from internal code.
- [Claude Agent SDK for Python](https://github.com/anthropics/claude-agent-sdk-python):
  inspect working-directory scope, tool auto-approval, explicit tool denial,
  deterministic hooks, session state, and typed errors separately. A tool
  allowlist may control automatic approval without removing other tools.
- [Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial):
  separate instructions from evidence, require a clear output contract, use
  examples for ambiguous formats, and include hallucination checks when a claim
  cannot be verified directly.
- [Claude for Financial Services](https://github.com/anthropics/financial-services):
  schema-validate worker output before orchestration, resolve cross-file
  references, detect drift between source skills and bundled copies, treat
  model-authored handoffs as untrusted, allowlist destinations, and stage
  financial work for qualified human sign-off rather than execution.
- [Conductor](https://github.com/conductor-oss/conductor):
  audit durable orchestration through persisted steps, configurable retries and
  timeouts, crash recovery, idempotent workers, and replay from a failed task.
  Keep deterministic workflow state separate from side-effecting business
  logic, and validate any workflow definition generated dynamically by an LLM
  before execution.

These sources are reference patterns only. The audit workflow remains
provider-neutral and can run without Anthropic services.
