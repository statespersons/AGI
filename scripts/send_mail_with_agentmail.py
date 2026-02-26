"""Send an email via AgentMail."""
import argparse, os, requests

API = "https://api.agentmail.to/v0"
HEADERS = {
    "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
    "Content-Type": "application/json",
}

def send(to: str, subject: str, body: str) -> dict:
    inbox_id = os.environ["AGENTMAIL_INBOX_ID"]
    r = requests.post(
        f"{API}/inboxes/{inbox_id}/messages/send",
        headers=HEADERS,
        json={"to": to, "subject": subject, "text": body},
    )
    r.raise_for_status()
    result = r.json()
    print(f"Sent message {result['message_id']} in thread {result['thread_id']}")
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("to", help="Recipient email address")
    p.add_argument("subject", help="Email subject")
    p.add_argument("body", help="Email body text")
    args = p.parse_args()
    send(args.to, args.subject, args.body)
