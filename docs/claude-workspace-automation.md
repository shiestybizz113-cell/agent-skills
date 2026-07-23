# Claude Workspace Automation

This repo can also supply a lightweight safety layer for shared local
workspaces, especially when one parent directory contains many repos and
worktrees.

## What It Adds

- `skills/workspace-triage/SKILL.md`
  - Helps agents choose the correct repo or worktree before editing.
- `skills/safe-release-scope/SKILL.md`
  - Forces repo-by-repo staging and push planning instead of broad workspace commits.
- `hooks/workspace-pre-edit-guard.sh`
  - Blocks direct edits to `.env` files, secret-bearing files, `.git`, `.runtime`,
    and hand-edited lockfiles.
- `hooks/workspace-post-edit-validate.py`
  - After edits, finds the nearest repo and runs a lightweight repo-local check.

## Recommended Setup

Add hook entries to the target workspace's `.claude/settings.json` or
`.claude/settings.local.json`.

If you cloned `agent-skills` locally and want to run the hooks directly from
this repo, use absolute paths:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /absolute/path/to/agent-skills/hooks/workspace-pre-edit-guard.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /absolute/path/to/agent-skills/hooks/workspace-post-edit-validate.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

If you prefer project-local copies, copy the two hook files into that project's
`.claude/hooks/` directory and point the commands there instead.

## When To Use The Skills

- Use `workspace-triage` when a workspace contains multiple plausible repos,
  proof copies, archives, or recovery bundles.
- Use `safe-release-scope` before `commit`, `push`, or PR work in any dirty
  multi-repo workspace.

## Validation Notes

- `workspace-pre-edit-guard.sh` expects `jq`.
- `workspace-post-edit-validate.py` prefers `npm`, `python3`, and optionally
  `pytest` when present.
- The post-edit validator intentionally reports failures without blocking the
  edit itself. It is a fast verification nudge, not a merge gate.
