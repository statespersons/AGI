"""Run a Browser Use cloud task, poll until done, print output, save trace."""
import argparse, json, os, time, requests

API = "https://api.browser-use.com/api/v2"
HEADERS = {"X-Browser-Use-API-Key": os.environ["BROWSER_USE_API_KEY"]}

def run(task: str, url: str | None = None) -> dict:
    body = {
        "task": task,
        "sessionSettings": {
            "profileId": os.environ["BROWSER_USE_PROFILE_ID"],
            "proxyCountryCode": "us",
        },
    }
    if url:
        body["startUrl"] = url

    task_id = requests.post(f"{API}/tasks", json=body, headers=HEADERS).json()["id"]
    print(f"Task {task_id} created, polling...")

    while True:
        time.sleep(5)
        s = requests.get(f"{API}/tasks/{task_id}/status", headers=HEADERS).json()
        if s["status"] in ("finished", "stopped"):
            break

    detail = requests.get(f"{API}/tasks/{task_id}", headers=HEADERS).json()

    os.makedirs("browser-use-traces", exist_ok=True)
    with open(f"browser-use-traces/{task_id}.json", "w") as f:
        json.dump(detail, f, indent=2)

    print(f"Status: {detail['status']} | Success: {detail.get('isSuccess')}")
    print(f"Output: {detail.get('output', 'None')}")
    return detail

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("task", help="Task instruction for the browser agent")
    p.add_argument("--url", help="Starting URL", default=None)
    args = p.parse_args()
    run(args.task, args.url)
