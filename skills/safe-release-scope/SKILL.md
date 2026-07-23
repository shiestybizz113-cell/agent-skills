---
name: safe-release-scope
description: Build a safe repo-by-repo staging and release plan in a shared workspace. Use before commit, push, or PR work when multiple repos are dirty or when secrets, runtime files, or unrelated changes may be present.
disable-model-invocation: true
---

# Safe Release Scope

Use this skill when preparing code for commit, push, or PR review in a workspace
with multiple repos and mixed-risk files.

## Goals

- Separate changes by repo.
- Block secrets, runtime state, archives, and accidental broad staging.
- Produce exact staging commands instead of `git add -A`.
- Keep one branch and one purpose per release unit whenever possible.

## Workflow

### 1. Inventory dirty repos

Start with repo discovery and status:

```bash
find "$CLAUDE_PROJECT_DIR" -maxdepth 3 -name .git -type d | sort
git -C "<repo>" status -sb
git -C "<repo>" diff --stat
git -C "<repo>" diff --name-only
```

### 2. Classify each changed file

Split files into:

- in-scope code or docs
- related generated artifacts
- unrelated churn
- blocked sensitive files

### 3. Block sensitive or misleading files

Never stage these unless the user explicitly asks and the file is meant to be
versioned:

- `.env`, `.env.local`, `.env.*` except safe examples
- private keys, certs, token dumps
- `.runtime/`
- archives, backups, recovery bundles
- databases and local state files
- `node_modules/`, `.venv/`, build cache
- lock files touched by hand rather than by a package manager flow

### 4. Produce a staging plan

Output exact commands like:

```bash
git -C "<repo>" add path/to/file1 path/to/file2
git -C "<repo>" commit -m "..."
```

If there are unrelated changes, keep them out of the staging set and say so.

### 5. Verify release readiness

Before recommending push, confirm:

- branch name
- changed file list
- no blocked files staged
- smallest relevant tests or checks run
- push destination if requested

## Hard Rules

- Never recommend `git add -A` in a shared workspace.
- Never recommend committing secrets or runtime state.
- Never merge repos into one release description if they serve different purposes.
- If the worktree is dirty in unrelated ways, call that out instead of hiding it.
- If the user asks for push planning only, stop after the plan and verification.

## Output Template

```text
Release unit: <repo path>
In scope:
- file1
- file2

Keep out:
- file3 — unrelated
- file4 — secret/runtime artifact

Suggested commands:
- git -C "<repo>" add file1 file2
- git -C "<repo>" commit -m "clear scoped message"

Checks:
- branch: <name>
- validation: <command/result or not run>
- push ready: yes/no
```
