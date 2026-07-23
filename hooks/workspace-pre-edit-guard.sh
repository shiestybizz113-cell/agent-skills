#!/bin/bash
set -euo pipefail

command -v jq >/dev/null 2>&1 || exit 0

if [ -t 0 ]; then
  INPUT="{}"
else
  INPUT=$(cat)
fi

FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null || true)
[ -n "$FILE_PATH" ] || exit 0

BASE_NAME=$(basename "$FILE_PATH")

is_lock_file() {
  case "$BASE_NAME" in
    package-lock.json|yarn.lock|pnpm-lock.yaml|bun.lockb|Cargo.lock|poetry.lock|Pipfile.lock)
      return 0
      ;;
  esac
  return 1
}

is_sensitive_path() {
  case "$FILE_PATH" in
    */.git/*|.git/*|*/.runtime/*|.runtime/*)
      return 0
      ;;
  esac

  case "$BASE_NAME" in
    .env|.env.local|.env.production|.env.development|.env.test|.envrc)
      return 0
      ;;
    .env.*)
      case "$BASE_NAME" in
        .env.example|.env.sample|.env.template)
          return 1
          ;;
        *)
          return 0
          ;;
      esac
      ;;
    *.pem|*.key|*.p12|*.pfx|id_rsa|id_ed25519|credentials.json|secrets.json|secrets.yaml|secrets.yml)
      return 0
      ;;
  esac

  return 1
}

if is_sensitive_path; then
  printf 'Blocked edit to sensitive path: %s\n' "$FILE_PATH" >&2
  printf 'Use an example or template file instead, or make the request explicit if this secret-bearing path truly must change.\n' >&2
  exit 2
fi

if is_lock_file; then
  printf 'Blocked direct edit to lock file: %s\n' "$FILE_PATH" >&2
  printf 'Regenerate lock files through the package manager instead of manual editing.\n' >&2
  exit 2
fi

exit 0
