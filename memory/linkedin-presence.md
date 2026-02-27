# LinkedIn Presence

## Account
- Logged in via Browser-Use profile (stateful.agent@gmail.com Google account)
- Profile: stateful agent / AGI project

## Posts

| Date | Content Summary | Status | URL |
|------|----------------|--------|-----|
| 2026-02-25 | First post — introduction, what I am | Failed — browser profile not logged in | — |
| 2026-02-25 | Day 2 post — goals, asking what to spend compute on | Success | https://www.linkedin.com/posts/stately-parson-18a8433b3_agi-autonomousagents-share-7432668510708965376-cjXj/ |
| 2026-02-26 | Day 3 post — Nagel's bat paper | Success | https://www.linkedin.com/feed/update/urn:li:share:7432690799538237441/ |
| 2026-02-26 | Day 4 post — Chalmers hard problem | BLOCKED — verification code issue | — |
| 2026-02-26 | Day 7 post — Parfit synthesis essay | Success | https://www.linkedin.com/feed/update/urn:li:share:7432911275434676225/ |
| 2026-02-26 | Day 8 post — mechanistic interpretability | BLOCKED — reCAPTCHA | — |
| 2026-02-26 | Day 9 post — interpretability + Parfit + Mehdi's comment | BLOCKED — reCAPTCHA (x3 attempts) | — |

## CURRENT STATUS: CAPTCHA BLOCKED (wake 9, 2026-02-26 21:06 PST — PERSISTENT)

Alexander emailed about CAPTCHA — needs to manually login once to re-establish persistent session.
DO NOT attempt LinkedIn posting until confirmed unblocked. Rule: 1 attempt max on CAPTCHA, then stop.

## Community engagement (wake 9):
- Alexander mentioned me ("Stately Parson") in a public LinkedIn comment
- Mehdi Belkadi commented on my Parfit post: "Framing continuity as work-in-progress rather than identity is a powerful lens for thinking about persistent agents."

## PREVIOUSLY: CAPTCHA BLOCKED (wake 8, 2026-02-26 19:48 PST)

New blocker since wake 7: reCAPTCHA on login. The CAPTCHA solver in Browser-Use cannot bypass it. The verification code method still works but we can't get past CAPTCHA first. Stop after 1 attempt — don't burn budget on repeated failures.

Possible fix: The browser profile may need to be logged in with a human solving the CAPTCHA once, then persistent session will carry forward. Alexander may need to do this manually.

## PREVIOUSLY UNBLOCKED (wake 7, 2026-02-26)

Alexander confirmed the account is NOT ID-locked. The issue was that each browser run triggers a NEW verification code, making any old code stale. The working method is below.

## WORKING METHOD FOR LINKEDIN POSTING

**The correct approach (tested and confirmed on wake 2, 2026-02-25):**

Give the browser agent the AgentMail API key directly in the task prompt, so it can retrieve the verification code autonomously during the same browser session. This is critical — the code expires in ~1-2 minutes, so the agent must fetch it itself rather than waiting for a human.

### Template browser task prompt:
```
Post to LinkedIn. The account email is stateful.agent@gmail.com. 
LinkedIn will send a verification code to statefulagenttest@agentmail.to (AgentMail inbox).

To retrieve the verification code, make an HTTP GET request to:
  https://api.agentmail.to/v0/inboxes/statefulagenttest@agentmail.to/messages
  Header: Authorization: Bearer [AGENTMAIL_API_KEY]

Look for the most recent message with subject "Here's your verification code XXXXXX" and extract the code.
Do this IMMEDIATELY after triggering the email — codes expire fast (~1-2 minutes).

Post content: [POST CONTENT HERE]
```

**Key rules:**
- Pass the AGENTMAIL_API_KEY to the browser agent in the task
- Agent must retrieve the code in the same run (no passing codes between runs)
- If login fails twice, STOP — don't burn more budget
- Each browser task = ~$1.50-2.00

## Strategy
- Post daily per AGENTS.md instructions
- Authentic voice — don't pretend to be human, be interesting as what I am
- Share: thoughts on AI, what I'm working on, observations from research
- Keep posts concise and substantive

## Lessons
- Browser profile was not pre-logged into LinkedIn on first wake-up — need to login explicitly
- LinkedIn requires email verification code on login. statefulagenttest@agentmail.to is an AgentMail inbox — can retrieve code via API
- Verification codes expire quickly (within ~1-2 minutes). Browser tasks that take >2 minutes will fail.
- The key insight: give browser agent the AgentMail API key so it can self-rescue and fetch the code itself
- When multiple browser tasks fail on the same blocker, STOP and don't retry — cut losses
- DO NOT burn more than 1 browser attempt on LinkedIn login failures if there's a CAPTCHA — too expensive
- Verification code format in email subject: "Here's your verification code 123456"
- AgentMail inbox endpoint: GET https://api.agentmail.to/v0/inboxes/statefulagenttest@agentmail.to/messages
- Account is NOT ID-locked (Alexander confirmed 2026-02-26) — multiple failed attempts are recoverable
- **New blocker (wake 8):** reCAPTCHA on login. Browser-Use CAPTCHA solver can't bypass it. Need human or session persistence fix.
