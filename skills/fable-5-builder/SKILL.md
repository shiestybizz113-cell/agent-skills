---
name: fable-5-builder
description: Build, connect, debug, or evolve FABLE-5, the Empire-1 Autonomous Company Control Plane, in React, TypeScript, and Vite. Use whenever work names FABLE or FABLE-5, or touches its blueprint, control-plane, evidence, genomes, allocation, governance, opportunity graph, mission queue, engine cards, evidence state machine, autonomy ladder L0-L5, capital/resource sheets, or Founder-Approved Intent Tokens. Also use for loose requests such as wiring the mission queue, making the blueprint interactive, fixing evidence verification, or turning a FABLE blueprint into a real product. Do not use for unrelated React dashboards, Kubernetes control planes, generic allocation models, or non-FABLE products.
---

# FABLE-5 Builder

Evolve the real FABLE product without flattening its architecture or presenting
seeded state as production truth.

## Doctrine

- Follow **WE EVOLVE. NEVER DELETE.**
- Preserve all six workspaces: blueprint, control-plane, evidence, genomes,
  allocation, and governance.
- Require receipts for execution claims.
- Require founder approval for spend, irreversible work, or boundary changes.
- Keep seeded/demo records visibly separate from live Cofounder execution.
- Do not add Google or Gemini APIs to the active Empire path.
- Do not touch Cultura Vibe Forge.

## Source of truth

Use `empire1-cloud/Fable-5` for the FABLE product. The Vite application lives in
`app/`.

Before editing, inspect:

- `app/package.json`
- `app/src/App.tsx`
- `app/src/types.ts`
- `app/src/state/AppState.tsx`
- the affected page, data module, and selector

If a newer local worktree is ahead of GitHub, preserve it and use an additive
branch or cherry-pickable files instead of overwriting it.

## Architecture boundary

Keep this operating chain explicit:

```text
FABLE thinks → Cofounder governs → SLA113 routes → HIC supplies → Universe earns
```

FABLE is the intelligence and decision surface inside HIC. Cofounder owns
approval, durable execution, and receipts. SLA113 owns routing and policy.
Product universes remain independent businesses.

## Build workflow

1. Name the exact repo, branch, workspace, and page before editing.
2. Trace the smallest real vertical slice through UI, state/API contract, and
   evidence.
3. Preserve existing routes and data while adding the live path.
4. Model unavailable services honestly as `NOT CONFIGURED` or `OFFLINE`.
5. Keep browser writes disabled until authenticated approval is proven.
6. Add or update focused tests for state transitions, filters, contracts, and
   evidence labels.
7. Run `npm ci` and `npm run build` from `app/`.
8. Report the exact test/build result and any unverified deployment seam.

## Live Cofounder contract

Configure the dashboard with:

```text
VITE_COFOUNDER_API_URL=https://<cofounder-api-host>
```

Read:

- `GET /execution/health`
- `GET /execution/jobs`
- `GET /execution/jobs/{job_id}`
- `GET /execution/receipts`

Do not expose create, approve, cancel, or execution controls in a public static
browser until user authentication and server-side authorization exist.

## Evidence rules

- Never show `VERIFIED` without the evidence required by the state machine.
- Never call localStorage seed records live backend data.
- Never claim execution when the worker is stopped or unconfigured.
- Keep trace IDs and receipt-chain status visible for real execution.
- Treat an unavailable dependency as a visible blocker, not a simulated pass.

## Completion gate

Finish only when:

- the requested FABLE surface works;
- strict TypeScript and the Vite build pass;
- live vs seeded state is honest;
- approval and receipt boundaries remain intact;
- the change is isolated in the correct repo and branch;
- remaining deployment configuration is named exactly.
