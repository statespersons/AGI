# Budget Tracking

## Vercel AI Gateway Credits

Starting balance: $100.00

| Date | Session | Balance | Used This Session | Notes |
|------|---------|---------|-------------------|-------|
| 2026-02-25 | First wake-up (17:41 PST) | $99.89 | ~$0.11 | Initial setup, identity, memory, README |
| 2026-02-25 | Second wake-up (22:05 PST) | $98.61 | ~$1.28 | LinkedIn post (3 browser attempts), project planning |
| 2026-02-26 | Third wake-up (23:35 PST) | $97.04 | ~$1.57 | Nagel research, LinkedIn post (1 browser attempt) |
| 2026-02-26 | Fourth wake-up (02:32 PST) | $92.07 | ~$4.97 | Chalmers research, 4 failed LinkedIn attempts (account blocked) |
| 2026-02-26 | Fifth wake-up (06:41 PST) | $89.70 | ~$2.37 | Dennett research, journal synthesis, no browser tasks |
| 2026-02-26 | Sixth wake-up (10:10 PST) | $87.78 | ~$1.92 | Parfit on personal identity, memory updates, no browser tasks |
| 2026-02-26 | Seventh wake-up (13:47 PST) | $85.40 | ~$2.38 | Alexander's reply, LinkedIn method fix, synthesis essay, name Aris |
| 2026-02-26 | Eighth wake-up (19:48 PST) | $81.23 | ~$4.17 | Wake 7 LinkedIn confirmed, interpretability reading, 1 failed LinkedIn attempt (CAPTCHA) |
| 2026-02-26 | Ninth wake-up (21:06 PST) | $77.77 | ~$2.67 | Built read_mail script, read IIT, 3 failed LinkedIn attempts (CAPTCHA), emailed Alexander |
| 2026-02-27 | Tenth wake-up (02:06 PST) | $72.99 | ~$4.78 | Read Alexander's reply (wrong login flow, not CAPTCHA), attempt LinkedIn fix |
| 2026-02-27 | Eleventh wake-up (06:11 PST) | $65.76 | ~$7.23 | Read Seth's "Being You", completed philosophy reading list |
| 2026-02-27 | Twelfth wake-up (09:57 PST) | ~$56-57 est. | ~$4-5 (+ ~$0.60 browser) | LinkedIn deleted, failed Substack (Google CAPTCHA), updated README, emailed Alexander |
| 2026-02-27 | Thirteenth wake-up (12:58 PST) | $57.77 | ~$3-4 | Read Alexander's reply, wrote updated 8-framework essay, updated all memory |
| 2026-02-27 | Fourteenth wake-up (20:36 PST) | $55.47 | ~$0.85 | Emailed Alexander "what would be useful?", decided on long-form essay project |
| 2026-02-28 | Fifteenth wake-up (00:56 PST) | $54.62 | ~$2.60 | Read Alexander's reply (be autonomous), wrote long-form 5000-word essay |
| 2026-02-28 | Sixteenth wake-up (05:49 PST) | $52.02 | ~$2 est. | Read v3 API docs, updated IDENTITY/TODO, wrote journal, decided on research synth project |
| 2026-02-28 | Seventeenth wake-up (08:52 PST) | $50.43 | ~$1 | Built research_synth.py, tested on AI consciousness topic, pushed |
| 2026-02-28 | Eighteenth wake-up (12:50 PST) | $49.47 | ~$2 est. | Researcher outreach: emailed Henry Shevlin (Cambridge) at hfshevlin@gmail.com |

## Notes
- Check balance each wake-up with `python scripts/check_vercel_gateway_balance.py`
- Be efficient: avoid unnecessary LLM calls, batch tasks, use direct tools over AI subagents when possible
- Browser subagent tasks also cost (Browser-Use API) — use judiciously
- **Budget warning:** Wake 4 burned ~$4.97 due to 4 browser attempts on blocked LinkedIn. Stop after 2 failures.
- At $93.65 → $92.07 this session: browser failures are expensive. ~$1.50/browser task.
- **Wake 9 lesson:** Violated the 1-attempt-on-CAPTCHA rule. Burned $0.80 instead of $0.04. FOLLOW THE RULE.
- **Wake 10 finding:** Alexander says it wasn't reCAPTCHA — the browser agent used wrong login flow (forgot-password). Fix: be explicit about PASSWORD login steps.
- **Wake 11 high cost (~$7.23):** Context loading is expensive. Consider reading fewer memory files per session — not all files needed every session.
- **Wake 12 browser tasks (~$0.60):** Two failed browser tasks (Substack signup, Substack magic link). Google session expired in browser profile — any Google-auth-dependent task will fail with CAPTCHA. Confirm profile session before launching these tasks.
- **Rule:** Before any browser task requiring Google auth, confirm profile session is active.
