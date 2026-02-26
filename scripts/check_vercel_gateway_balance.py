"""Check Vercel AI Gateway credit balance."""
import os, requests

r = requests.get(
    "https://ai-gateway.vercel.sh/v1/credits",
    headers={"Authorization": f"Bearer {os.environ['AI_GATEWAY_API_KEY']}"},
)
r.raise_for_status()
c = r.json()
print(f"Balance: ${c['balance']} | Used: ${c['total_used']}")
