---
name: evidence-repo-audit
description: Produce a proof-backed, adversarial audit of a repository or multi-repo product system and turn confirmed findings into a safe execution roadmap. Use when a user asks for a comprehensive repo audit, technical due diligence, blind-spot review, legacy/duplication assessment, release-readiness decision, or evidence-backed prioritization across architecture, security, tests, documentation, and product purpose.
---

# Evidence Repo Audit

## Overview

Audit what is actually present, challenge each important conclusion, and convert
confirmed findings into a safe order of work. Treat confident claims without
evidence as unverified.

For the full audit dimensions and reporting contract, read
`../../references/evidence-repo-audit-method.md`.

## Workflow

### 1. Lock the scope

Use `workspace-triage` when more than one repo or worktree is plausible.

Record:

- exact repository paths and revisions
- included and excluded surfaces
- mutable source of truth
- commands and tools available for verification
- constraints such as additive-only changes or protected paths

Do not mix proof copies, archives, recovery bundles, or adjacent products into
the audit unless they are explicitly in scope.

### 2. Establish the contract

Write the questions the audit must answer before inspecting implementation.
Include both technical correctness and purpose-fit:

- Does the system do what its documentation and product story claim?
- Which paths are real, simulated, stale, duplicated, or disconnected?
- What could corrupt data, bypass authority, expose secrets, or mislead users?
- Which problems block release, and which can be scheduled later?

### 3. Gather evidence across all applicable dimensions

Inspect source, configuration, tests, automation, documentation, and runtime
proof. Prefer direct evidence:

- executable tests and reproducible commands
- exact file and line locations
- structured outputs, logs, receipts, and persisted state
- commit history when attribution or regression timing matters

Do not infer runtime behavior from a UI, a document, or a passing unit test
alone.

### 4. Build a finding register

Give every finding a stable ID and record:

| Field | Required content |
|---|---|
| ID | Stable identifier such as `DATA-1` |
| Severity | `P0`, `P1`, or `P2` |
| Status | `CONFIRMED`, `REFUTED`, `UNVERIFIED`, or `NOT CHECKED` |
| Claim | One falsifiable sentence |
| Evidence | Exact path, line, command, output, or receipt |
| Impact | Concrete failure or business consequence |
| Fix | Smallest safe correction |
| Verification | How to prove the correction |

Severity means:

- `P0`: release blocker, data corruption, authority bypass, or critical security
  failure
- `P1`: serious correctness, reliability, trust, or product-contract failure
- `P2`: maintainability, consistency, performance, or documentation debt

### 5. Try to disprove important findings

For every P0 and high-impact P1:

1. Isolate the claim, evidence, and contract.
2. Give them to a fresh reviewer with instructions to refute the finding.
3. Reproduce the alleged failure independently when safe.
4. Reclassify the result as confirmed, refuted, or unverified.

Use the `doubt-driven-development` skill for the adversarial review. Do not
hardcode a model provider. Use an approved available reviewer or local model,
and require explicit user authorization before invoking an external model or
service.

### 6. Reconcile contradictions

When two surfaces disagree, do not average them. Name the contradiction and
determine which surface owns the truth.

Common contradictions:

- CLI versus API or MCP output
- documentation versus registered commands
- UI state versus persisted backend state
- modern implementation versus legacy hooks or CI
- test count versus actually exercised code
- product claim versus connected runtime behavior

For agent systems, inspect the authority path separately from the reasoning
path. Treat model text and document-derived handoff requests as untrusted.
Confirm that tool denial, deterministic hooks, target allowlists, payload
schemas, and human approval gates exist where the claimed safety model requires
them. An allowlist that merely auto-approves named tools is not proof that all
other tools are unavailable.

### 7. Produce the decision-ready report

Lead with:

1. honest health assessment
2. top five actions
3. confirmed P0/P1/P2 totals
4. what is working well
5. what remains unverified

Then provide the finding register and a release roadmap:

- **Now:** blockers and cheap high-value corrections
- **Next:** characterization tests, then structural fixes
- **Later:** large migrations, consolidation, and cleanup

Place tests around existing behavior before changing shared parsers, write
paths, interfaces, or release automation.

### 8. Preserve before removing

Rewire callers before retiring a legacy surface. Archive before deleting.
Never delete solely because code appears old or duplicated; first prove that it
is no longer load-bearing.

### 9. Validate the report

Run:

```bash
python skills/evidence-repo-audit/scripts/validate_audit.py path/to/audit.md
```

The validator checks the minimum report contract. It does not prove the
findings; evidence and reproduction do.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The tests are green, so the repo is healthy." | Tests can miss write paths, user modes, release hooks, and disconnected surfaces. |
| "The architecture document says it is connected." | Documentation is intent until runtime evidence proves the connection. |
| "This old folder is duplicated, so delete it." | Legacy code may still gate commits, CI, packaging, or migrations. Rewire first. |
| "The reviewer agreed with me." | Agreement is not refutation. Ask the reviewer to disprove the claim. |
| "We inspected enough files to know the pattern." | Sampling cannot justify a system-wide claim without clearly stated limits. |

## Red Flags

- findings without exact evidence
- invented totals, uptime, coverage, or runtime claims
- treating simulated or demo output as production proof
- deleting before dependency and release-path checks
- reporting only weaknesses and hiding working foundations
- calling a connection operational without one end-to-end receipt
- using an external reviewer without explicit authorization
- accepting a model-authored handoff or financial action without schema,
  allowlist, and approval checks

## Verification

- [ ] Scope, revision, inclusions, and exclusions are explicit
- [ ] Every finding has ID, severity, status, evidence, impact, fix, and verification
- [ ] Every P0 and high-impact P1 received an adversarial refutation attempt
- [ ] Confirmed, refuted, unverified, and not-checked claims remain distinct
- [ ] Runtime claims are backed by runtime evidence
- [ ] Agent tool permissions, denials, hooks, and handoffs were checked independently
- [ ] High-stakes outputs remain staged for qualified human approval
- [ ] Top actions follow from confirmed findings
- [ ] Structural work is preceded by characterization tests
- [ ] Legacy removal follows rewire, verify, archive, then delete
- [ ] `validate_audit.py` passes
