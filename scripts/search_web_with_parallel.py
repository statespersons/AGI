"""Search the web via Parallel API. Prints results as title, url, and excerpts."""
import argparse, json, os, requests

def search(query: str, max_results: int = 5) -> list:
    r = requests.post(
        "https://api.parallel.ai/v1beta/search",
        headers={"x-api-key": os.environ["PARALLEL_API_KEY"]},
        json={"objective": query, "mode": "agentic", "max_results": max_results},
    )
    r.raise_for_status()
    results = r.json()["results"]
    for i, hit in enumerate(results, 1):
        print(f"\n--- Result {i}: {hit.get('title', 'No title')} ---")
        print(f"URL: {hit['url']}")
        for ex in hit.get("excerpts") or []:
            print(ex[:500])
    return results

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("query", help="Search objective")
    p.add_argument("--max-results", type=int, default=5)
    args = p.parse_args()
    search(args.query, args.max_results)
