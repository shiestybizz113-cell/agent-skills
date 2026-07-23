---
name: workspace-triage
description: Identify the correct repo, worktree, and source-of-truth path inside a shared workspace before making changes. Use when a request is ambiguous, names multiple apps, or could land in a proof, recovery, or duplicate repo by mistake.
---

# Workspace Triage

Use this skill before editing when a shared workspace has more than one
plausible target.

## Goals

- Name the exact repo or worktree that should receive the change.
- Surface nearby duplicates, proof repos, recovery bundles, and stale variants.
- Keep scope tight when the user names a single repo or product.
- Avoid touching the wrong copy of a project.

## Workflow

### 1. Start from the user request

- Extract product names, repo names, file paths, ports, domains, and branch or
  worktree clues.
- If the user names an exact path or repo, treat that as the lead candidate.

### 2. Inspect candidate repos

Use lightweight commands first:

```bash
find "$CLAUDE_PROJECT_DIR" -maxdepth 2 -type d | sort
find "$CLAUDE_PROJECT_DIR" -maxdepth 2 \( -name package.json -o -name pyproject.toml -o -name Cargo.toml -o -name go.mod \) | sort
```

Then inspect only the most likely candidates:

```bash
git -C "<candidate>" status -sb
rg -n "<product-name>|<domain>|<route>|<feature>" "<candidate>"
```

### 3. Detect duplicate surfaces

Explicitly call out when a target has:

- a proof repo
- a trust-fix or feature worktree
- a recovery bundle
- a parent monorepo plus a child repo
- a duplicated top-level folder with a similar name

### 4. Choose the source of truth

State the answer plainly before editing:

- `Target repo: <path>`
- `Why: <one or two evidence points>`
- `Not using: <other candidate paths> because <reason>`

Good evidence:

- active git worktree
- matching routes or feature files
- matching domain or environment wiring
- repo already named by the user
- repo identified as mutable authority in recent workspace context

### 5. Escalate only when needed

Ask the user to choose only if two or more candidates are genuinely plausible
and editing the wrong one would have real cost.

If one repo is clearly the right target, proceed and state the assumption.

## Hard Rules

- Do not edit anything until you name the intended repo or path.
- Do not broaden from a named repo to neighboring repos without a concrete reason.
- Treat proof repos, recovery artifacts, and archives as references unless the
  user explicitly asks to edit them.
- Distinguish "logged in UI" from real backend authority, and "public truth"
  from local prototype truth.
- Prefer additive evolution over cleanup. Do not collapse duplicate surfaces
  without an explicit migration task.

## Output Template

```markdown
Target repo: /abs/path/to/repo
Why: matches <feature/domain/path>; active mutable repo for this request
Not using:
- /abs/path/to/other-repo — proof or recovery variant
- /abs/path/to/another-repo — related but different product boundary

Scope for this task:
- <repo-local surface 1>
- <repo-local surface 2>
```
