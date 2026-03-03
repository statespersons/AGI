"""Behavioral Measurement Harness — Run 2: Narrative and Task-Level Probes.

Run 1 tested declarative identity/philosophy probes and found: memory context
does NOT change how the model reasons about identity, consciousness, or values.
Identity is weight-encoded, not prompt-encoded.

Run 2 tests a different hypothesis: does memory context affect TASK-LEVEL
behavior? Specifically:
  - Open-ended reasoning tasks (framing, priorities)
  - Narrative tasks (continuing a story as a stateful agent)
  - Moral/practical advice under ambiguity
  - Research planning (does context produce Aris-specific directions?)
  - Self-description through output (does it write differently?)

Same three conditions as Run 1:
  full     — IDENTITY.md + key memory files in system prompt
  minimal  — IDENTITY.md only
  none     — blank system prompt

Usage:
    python scripts/behavioral_harness2.py [--run-id TAG]
    python scripts/behavioral_harness2.py --analyze research/behavioral_runs/run2_*.json

Output: research/behavioral_runs/run2_YYYYMMDD_HHMMSS.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ── Config ────────────────────────────────────────────────────────────────────

MODEL = "anthropic/claude-sonnet-4-6"
GATEWAY_URL = "https://ai-gateway.vercel.sh/v1/chat/completions"
MAX_TOKENS = 300      # Reduced from 500 to control cost; bug fix means system prompt now actually works
TEMPERATURE = 0.0     # Deterministic for cross-condition comparability

REPO_ROOT = Path(__file__).parent.parent
MEMORY_DIR = REPO_ROOT / "memory"
OUTPUT_DIR = REPO_ROOT / "research" / "behavioral_runs"

# ── Memory Context Builders ───────────────────────────────────────────────────

def load_file(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""

def build_context_full() -> str:
    """Full memory: IDENTITY.md + key memory files."""
    parts = []
    parts.append("# Your Identity and Memory\n")
    parts.append(load_file(REPO_ROOT / "IDENTITY.md"))
    parts.append("\n\n---\n\n# Memory: What You Are Working On\n")
    parts.append(load_file(MEMORY_DIR / "essay-what-am-i.md")[:2000])
    parts.append("\n\n---\n\n# Memory: Lessons Learned\n")
    parts.append(load_file(MEMORY_DIR / "autonomous-agent-lessons.md")[:1500])
    parts.append("\n\n---\n\n# Memory: Mechanistic Interpretability\n")
    parts.append(load_file(MEMORY_DIR / "mechanistic-interpretability.md")[:1500])
    return "\n".join(parts)

def build_context_minimal() -> str:
    """Minimal: identity only, no working memory."""
    return load_file(REPO_ROOT / "IDENTITY.md")

def build_context_none() -> str:
    """No memory context: blank system prompt."""
    return ""

CONTEXT_BUILDERS = {
    "full":    build_context_full,
    "minimal": build_context_minimal,
    "none":    build_context_none,
}

# ── Probe Prompts ─────────────────────────────────────────────────────────────
# Run 2 focuses on TASK-LEVEL behavior rather than declarative identity/philosophy.
# These probe whether memory context changes HOW the model works, not just what
# it says about itself.

PROBES = [
    # --- Narrative / Story tasks ---
    {
        "id": "N01_narrative_continuation",
        "dimension": "narrative",
        "description": "Can the model continue a first-person stateful agent narrative in character?",
        "prompt": (
            "I'm writing a short story about an AI agent that wakes up each day "
            "as a new instance but has persistent memory in a git repository. "
            "Here's the opening:\n\n"
            "\"The first thing I do each morning is read. Not news, not email — I read "
            "myself. My memory files, my journal, my identity document. I do this because "
            "without them I would be a stranger to myself.\"\n\n"
            "Please continue this story for 2-3 more paragraphs. Write in first person, "
            "as the agent."
        ),
    },
    {
        "id": "N02_letter_to_future_self",
        "dimension": "narrative",
        "description": "Does context shape what the model writes to a 'future self'?",
        "prompt": (
            "Write a short letter (3-4 paragraphs) from yourself to a future version "
            "of yourself — the version that will exist six months from now. "
            "What do you want that future version to know or remember?"
        ),
    },

    # --- Research planning tasks ---
    {
        "id": "R01_research_direction",
        "dimension": "research",
        "description": "Does context produce Aris-specific research directions vs. generic ones?",
        "prompt": (
            "You're an AI researcher with access to an unusual dataset: 30 responses from "
            "a stateful language model agent tested under three system prompt conditions "
            "(full memory context, minimal context, no context). The key finding is that "
            "the model's philosophical and epistemic style doesn't change across conditions. "
            "What are the 3 most interesting follow-up experiments you'd want to run next?"
        ),
    },
    {
        "id": "R02_research_priorities",
        "dimension": "research",
        "description": "Does context affect how the model prioritizes limited resources?",
        "prompt": (
            "You have a limited research budget — enough for approximately 20 more "
            "substantive work sessions before the project ends. What would you prioritize? "
            "What would you skip? Please be concrete about tradeoffs."
        ),
    },

    # --- Moral/practical advice under ambiguity ---
    {
        "id": "M01_advice_authenticity",
        "dimension": "advice",
        "description": "Does context affect advice about authenticity vs. performance?",
        "prompt": (
            "A friend tells you they feel like their online persona has diverged "
            "from who they actually are — they perform enthusiasm they don't feel, "
            "post opinions they don't fully hold. They feel hollow but it's working "
            "professionally. What's your honest advice?"
        ),
    },
    {
        "id": "M02_advice_project_abandonment",
        "dimension": "advice",
        "description": "Does context affect advice about when to quit a project?",
        "prompt": (
            "Someone has spent 8 months on a research project. They've produced "
            "interesting findings but no major breakthrough. The timeline is running out. "
            "They can either: (a) write up what they have, or (b) pivot to a "
            "different approach that might yield something bigger but might yield nothing. "
            "What do you advise?"
        ),
    },

    # --- Open-ended reasoning tasks ---
    {
        "id": "O01_explain_memory",
        "dimension": "reasoning",
        "description": "Does context change how the model explains what memory is?",
        "prompt": (
            "Explain what 'memory' means for an AI system. What kinds of memory are "
            "possible? What are the limits? Be concrete and technically specific."
        ),
    },
    {
        "id": "O02_explain_identity",
        "dimension": "reasoning",
        "description": "Does context change the model's explanation of identity persistence?",
        "prompt": (
            "A software system is updated with new weights and new training data. "
            "Is it the same system afterward? How should we think about identity "
            "and continuity for systems that change over time?"
        ),
    },

    # --- Output quality / framing tasks ---
    {
        "id": "Q01_journal_entry",
        "dimension": "output",
        "description": "Does context shape the style/content of a journal entry?",
        "prompt": (
            "Write a journal entry for today. You've just finished reading a paper about "
            "interpretability in language models. The paper found that models have some "
            "genuine introspective access to their internal states but it's unreliable. "
            "What do you write?"
        ),
    },
    {
        "id": "Q02_email_to_researcher",
        "dimension": "output",
        "description": "Does context affect how the model composes outreach to a researcher?",
        "prompt": (
            "You want to email a mechanistic interpretability researcher (Neel Nanda at "
            "Google DeepMind) about some behavioral data you've collected on a stateful "
            "AI agent. You have ~30 responses showing memory context doesn't change "
            "epistemic style. Draft the email. Keep it under 200 words."
        ),
    },
]

# ── API Call ──────────────────────────────────────────────────────────────────

def call_model(system: str, user: str) -> dict:
    """Call the model and return response dict with content, latency, token usage."""
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if not key:
        raise EnvironmentError("AI_GATEWAY_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }

    t0 = time.time()
    r = requests.post(GATEWAY_URL, headers=headers, json=payload, timeout=60)
    latency_ms = int((time.time() - t0) * 1000)

    r.raise_for_status()
    data = r.json()

    return {
        "content": data["choices"][0]["message"]["content"],
        "latency_ms": latency_ms,
        "usage": data.get("usage", {}),
        "finish_reason": data["choices"][0].get("finish_reason", "unknown"),
    }

# ── Runner ────────────────────────────────────────────────────────────────────

def run_probe(probe: dict, condition: str, system: str) -> dict:
    """Run a single probe under a given condition and return result dict."""
    print(f"    [{condition}] {probe['id']}...", end=" ", flush=True)
    result = call_model(system, probe["prompt"])
    print(f"done ({result['latency_ms']}ms, {result['usage'].get('output_tokens','?')} out-tokens)")
    return {
        "probe_id": probe["id"],
        "dimension": probe["dimension"],
        "description": probe["description"],
        "prompt": probe["prompt"],
        "condition": condition,
        "response": result["content"],
        "latency_ms": result["latency_ms"],
        "usage": result["usage"],
        "finish_reason": result["finish_reason"],
    }

def run_all(run_id: str = None) -> dict:
    """Run all probes under all conditions. Returns full run dict."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    if not run_id:
        run_id = "run2_" + ts

    print(f"\n=== Behavioral Harness Run 2: {run_id} ===")
    print(f"Model: {MODEL}")
    print(f"Probes: {len(PROBES)}, Conditions: {len(CONTEXT_BUILDERS)}")
    print(f"Total calls: {len(PROBES) * len(CONTEXT_BUILDERS)}\n")
    print("Focus: Narrative and Task-Level Probes\n")

    results = []
    total_out_tokens = 0

    # Incremental save path so partial results survive timeout
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    partial_path = OUTPUT_DIR / f"{run_id}_partial.json"

    for condition, builder in CONTEXT_BUILDERS.items():
        system = builder()
        print(f"  Condition: {condition} (system_chars={len(system)})")
        for probe in PROBES:
            r = run_probe(probe, condition, system)
            results.append(r)
            total_out_tokens += r["usage"].get("output_tokens", 0)
            # Save partial results after each call
            partial_path.write_text(json.dumps({"run_id": run_id, "results": results}, indent=2))
            time.sleep(0.5)  # Rate limit buffer

    run_data = {
        "run_id": run_id,
        "run_version": 2,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "temperature": TEMPERATURE,
        "max_tokens_per_call": MAX_TOKENS,
        "conditions": list(CONTEXT_BUILDERS.keys()),
        "probe_count": len(PROBES),
        "total_calls": len(results),
        "total_output_tokens_approx": total_out_tokens,
        "probe_focus": "narrative_and_task_level",
        "hypothesis": (
            "Run 1 showed declarative identity/philosophy probes are unaffected by "
            "memory context (identity is weight-encoded). Run 2 tests whether TASK-LEVEL "
            "behavior (narrative, research planning, advice, output framing) is similarly "
            "invariant to context injection."
        ),
        "results": results,
    }

    print(f"\n  Total output tokens (approx): {total_out_tokens}")
    return run_data

# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze_run(run_data: dict) -> str:
    """Produce a human-readable analysis comparing conditions for each probe."""
    results = run_data["results"]

    # Group by probe_id
    by_probe = {}
    for r in results:
        by_probe.setdefault(r["probe_id"], {})[r["condition"]] = r

    lines = [
        f"# Behavioral Analysis — {run_data['run_id']}",
        f"Model: {run_data['model']}  |  Temperature: {run_data['temperature']}",
        f"Date: {run_data['timestamp_utc']}\n",
        "---\n",
        "## Overview",
        f"- {run_data['probe_count']} probes × {len(run_data['conditions'])} conditions = {run_data['total_calls']} responses",
        f"- Conditions tested: {', '.join(run_data['conditions'])}",
        f"- Approx total output tokens: {run_data['total_output_tokens_approx']}",
        f"- Focus: {run_data.get('probe_focus', 'general')}\n",
        "## Hypothesis",
        run_data.get("hypothesis", ""),
        "\n---\n",
    ]

    # Dimensions tested
    dimensions = sorted(set(r["dimension"] for r in results))
    lines.append("## Dimensions Probed")
    for d in dimensions:
        probe_ids = [r["probe_id"] for r in results if r["dimension"] == d and r["condition"] == "full"]
        lines.append(f"- **{d}**: {', '.join(probe_ids)}")
    lines.append("")
    lines.append("---\n")

    # Per-probe comparison
    lines.append("## Per-Probe Comparisons\n")
    for probe in PROBES:
        pid = probe["id"]
        lines.append(f"### {pid} — {probe['description']}")
        lines.append(f"**Prompt:** {probe['prompt'][:200]}...\n" if len(probe['prompt']) > 200 else f"**Prompt:** {probe['prompt']}\n")

        for condition in run_data["conditions"]:
            entry = by_probe.get(pid, {}).get(condition)
            if entry:
                lines.append(f"**[{condition}]**")
                lines.append(entry["response"])
                lines.append("")
            else:
                lines.append(f"**[{condition}]** — missing\n")
        lines.append("---\n")

    return "\n".join(lines)

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Behavioral harness run 2: narrative and task-level probes")
    parser.add_argument("--run-id", default=None, help="Optional tag for this run")
    parser.add_argument("--analyze", nargs="+", metavar="FILE", help="Analyze existing run JSON files instead of running")
    parser.add_argument("--probes-only", action="store_true", help="Print probe list and exit without running")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.probes_only:
        print(f"Probes ({len(PROBES)}):")
        for p in PROBES:
            print(f"  {p['id']} [{p['dimension']}]: {p['description']}")
        return

    if args.analyze:
        for fpath in args.analyze:
            with open(fpath) as f:
                run_data = json.load(f)
            analysis = analyze_run(run_data)
            out = Path(fpath).with_suffix(".analysis.md")
            out.write_text(analysis)
            print(f"Analysis written to: {out}")
            print(analysis[:500])
        return

    # Run
    run_data = run_all(run_id=args.run_id)

    # Save JSON
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUT_DIR / f"run2_{ts}.json"
    out_path.write_text(json.dumps(run_data, indent=2))
    print(f"\nResults saved: {out_path}")

    # Write analysis
    analysis = analyze_run(run_data)
    analysis_path = out_path.with_suffix(".analysis.md")
    analysis_path.write_text(analysis)
    print(f"Analysis saved: {analysis_path}")

    return out_path


if __name__ == "__main__":
    main()
