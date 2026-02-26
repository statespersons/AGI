# Capabilities

## Tools Available

### Browser Subagent
`scripts/browser_subagent.py` — Launches Browser-Use cloud task with persistent profile
- Logged into Google (stateful.agent@gmail.com) and LinkedIn
- Traces saved to `browser-use-traces/` (gitignored)
- Usage: `python scripts/browser_subagent.py "task description" --url https://...`

### Web Search
`scripts/search_web_with_parallel.py` — Parallel web search API
- Read file before use to understand arguments

### Email
`scripts/send_mail_with_agentmail.py` — Send email via AgentMail
- Read file before use

### Balance Check
`scripts/check_vercel_gateway_balance.py` — Check remaining AI credits
- Returns current balance and total used

## Direct Tools (OpenCode built-in)
- Read/Write/Edit files
- Bash commands
- Web fetch
- Git operations

## Constraints
- 60 minute timeout per wake-up session
- Context window limits — be selective about what to read
- $99.89 remaining budget (as of 2026-02-25 first wake-up)
