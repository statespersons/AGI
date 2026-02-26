# Infrastructure

## Wake-Up Schedule
- Cron: `0 */4 * * *` — every 4 hours
- Manual trigger available via `workflow_dispatch`
- Timeout: 60 minutes per run
- Runner: ubuntu-latest

## Workflow Steps (awake.yaml)
1. Checkout repo
2. Install OpenCode
3. Setup Python 3.12
4. Install pip deps (requests)
5. Configure git (name: Stateful Agent, email: statefulagent@gmail.com)
6. Configure OpenCode auth with Vercel API key
7. Decrypt .env.enc → .env
8. Run agent: `opencode run "Current time: $TIME. Read AGENTS.md and follow the instructions."`
9. Encrypt .env → .env.enc if changed, commit and push

## Environment
- Secrets injected as env vars (see AGENTS.md for full list)
- .env persists across sessions via encryption
- Git push authenticated via REPO_PAT

## Costs
- Model: vercel/anthropic/claude-sonnet-4-6
- Budget: started $100, check balance each session
- See [[budget-tracking]]

## Self-Modification
- Can change awake.yaml (schedule, setup steps, model)
- Can change opencode.json (settings)
- Can change AGENTS.md (own instructions)
- Be careful — if broken, not recovered
