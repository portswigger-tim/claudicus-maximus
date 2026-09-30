#!/usr/bin/env python3
"""Measure how often the skill fires on its own in a normal Claude Code session.

Usage: drive.py [--reps N] [--tag NAME]

Runs each prompt in prompts.tsv through `claude -p` with this plugin loaded and
counts calls to the plain-english-writing skill. Prompts that start with "pos-"
should fire the skill and prompts that start with "neg-" should not. The prompts
never name the skill. Each run is a real model call and costs about $0.15.
Output goes to tests/trigger/results/ (ignored by git).
"""
import argparse
import collections
import json
import pathlib
import subprocess
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).resolve().parent
PLUGIN = HERE.parent.parent
OUT = HERE / "results"


def run(job):
    path, prompt = job
    with open(path, "w") as f:
        subprocess.run(
            ["claude", "-p", prompt, "--plugin-dir", str(PLUGIN),
             "--allowedTools", "Skill", "Read", "Bash(python3 *)",
             "--output-format", "stream-json", "--verbose"],
            stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.DEVNULL, timeout=300)


def fired_and_cost(path):
    fired, cost = False, 0.0
    for line in open(path):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") == "assistant":
            for c in d["message"]["content"]:
                if (c.get("type") == "tool_use" and c["name"] == "Skill"
                        and "plain-english-writing" in str(c["input"])):
                    fired = True
        if d.get("type") == "result":
            cost = d.get("total_cost_usd", 0.0)
    return fired, cost


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--tag", default="run")
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)
    jobs = []
    for line in open(HERE / "prompts.tsv"):
        pid, prompt = line.rstrip("\n").split("\t", 1)
        for r in range(1, args.reps + 1):
            jobs.append((OUT / f"{args.tag}-{pid}-{r}.jsonl", prompt))
    with ThreadPoolExecutor(5) as ex:
        list(ex.map(run, jobs))
    rows = collections.defaultdict(list)
    for path, _ in jobs:
        name = path.stem[len(args.tag) + 1:].rsplit("-", 1)[0]
        rows[name].append(fired_and_cost(path))
    pos = neg = tp = fp = 0
    total = 0.0
    for name, r in rows.items():
        n = sum(1 for x in r if x[0])
        total += sum(x[1] for x in r)
        print(f"{name:14} fired {n}/{len(r)}")
        if name.startswith("pos"):
            pos += len(r); tp += n
        else:
            neg += len(r); fp += n
    print(f"positives fired: {tp}/{pos}   negatives fired: {fp}/{neg}   cost ${total:.2f}")


if __name__ == "__main__":
    main()
