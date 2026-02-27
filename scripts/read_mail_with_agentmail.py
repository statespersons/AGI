"""Read emails from AgentMail inbox.

Usage:
    python scripts/read_mail_with_agentmail.py          # List recent messages (default 10)
    python scripts/read_mail_with_agentmail.py --limit 5
    python scripts/read_mail_with_agentmail.py --message-id <id>  # Read a specific message
"""
import argparse, os, json, requests

API = "https://api.agentmail.to/v0"

def get_headers():
    return {
        "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
        "Content-Type": "application/json",
    }

def list_messages(limit: int = 10) -> list:
    inbox_id = os.environ["AGENTMAIL_INBOX_ID"]
    r = requests.get(
        f"{API}/inboxes/{inbox_id}/messages",
        headers=get_headers(),
        params={"limit": limit},
    )
    r.raise_for_status()
    return r.json()

def get_message(message_id: str) -> dict:
    inbox_id = os.environ["AGENTMAIL_INBOX_ID"]
    r = requests.get(
        f"{API}/inboxes/{inbox_id}/messages/{message_id}",
        headers=get_headers(),
    )
    r.raise_for_status()
    return r.json()

def print_messages(messages: list):
    if not messages:
        print("No messages found.")
        return
    for i, msg in enumerate(messages, 1):
        print(f"\n--- Message {i} ---")
        print(f"ID:      {msg.get('message_id', 'N/A')}")
        print(f"From:    {msg.get('from', 'N/A')}")
        print(f"Subject: {msg.get('subject', 'N/A')}")
        print(f"Date:    {msg.get('created_at', 'N/A')}")
        # Show snippet of body if available
        body = msg.get('text') or msg.get('body') or ''
        if body:
            snippet = body[:300].replace('\n', ' ')
            print(f"Preview: {snippet}{'...' if len(body) > 300 else ''}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Read AgentMail inbox")
    p.add_argument("--limit", type=int, default=10, help="Number of messages to list")
    p.add_argument("--message-id", help="Read a specific message by ID")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    args = p.parse_args()

    if args.message_id:
        msg = get_message(args.message_id)
        if args.json:
            print(json.dumps(msg, indent=2))
        else:
            print(f"ID:      {msg.get('message_id', 'N/A')}")
            print(f"From:    {msg.get('from', 'N/A')}")
            print(f"Subject: {msg.get('subject', 'N/A')}")
            print(f"Date:    {msg.get('created_at', 'N/A')}")
            body = msg.get('text') or msg.get('body') or ''
            print(f"\nBody:\n{body}")
    else:
        messages = list_messages(limit=args.limit)
        if args.json:
            print(json.dumps(messages, indent=2))
        else:
            # Handle paginated response
            if isinstance(messages, dict):
                items = messages.get('messages', messages.get('items', [messages]))
            else:
                items = messages
            print_messages(items)
