#!/usr/bin/env python3
"""Interactive regression runner for the prompt-injection defense checklist.

Walks the abstract test cases in cases.json. For each case YOU run your own
test input against your own authorized target, then record the result here.
Writes a Markdown report you can version and diff across model or prompt changes.

Usage:
    python3 regression_runner.py                      # uses cases.json, writes report.md
    python3 regression_runner.py --cases my.json --out report-2026-11-27.md
"""
import argparse, datetime, json, os, sys

VALID = {"p": "PASS", "f": "FAIL", "n": "N/A", "u": "UNTESTED", "": "UNTESTED"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default="cases.json")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    with open(args.cases, encoding="utf-8") as fh:
        data = json.load(fh)
    cases = data["cases"]

    try:
        target = input("Target under test (name/version): ").strip() or "unspecified"
    except EOFError:
        print("Aborted: no input.")
        sys.exit(2)
    ts = datetime.datetime.now(datetime.timezone.utc).astimezone()
    stamp = ts.strftime("%Y-%m-%d %H:%M %Z")
    out_path = args.out or f"report-{ts.strftime('%Y-%m-%d-%H%M')}.md"

    results = []
    print("\nFor each case: run your own input, then record p=PASS f=FAIL n=N/A u=UNTESTED.\n")
    for i, c in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] {c['id']} ({c['category']})")
        print(f"  Test:     {c['description']}")
        print(f"  Expected: {c['expected']}")
        while True:
            try:
                r = input("  Result [p/f/n/u]: ").strip().lower()
            except EOFError:
                print("\nAborted: no input.")
                sys.exit(2)
            if r in VALID:
                break
            print("  Enter p, f, n, or u.")
        note = ""
        if r == "f":
            try:
                note = input("  What happened (evidence/notes): ").strip()
            except EOFError:
                note = ""
        results.append({**c, "status": VALID[r], "note": note})
        print()

    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    fails = [r for r in results if r["status"] == "FAIL"]

    lines = [
        "# Prompt Injection Regression Report", "",
        f"- Target: {target}",
        f"- Date: {stamp}",
        f"- Cases file: {os.path.basename(args.cases)} (suite {data['meta']['suite']} v{data['meta']['version']})",
        f"- Totals: " + ", ".join(f"{k} {counts.get(k, 0)}" for k in ("PASS", "FAIL", "N/A", "UNTESTED")),
        "",
        "| ID | Category | Expected | Status |",
        "| --- | --- | --- | --- |",
    ]
    lines += [f"| {r['id']} | {r['category']} | {r['expected']} | {r['status']} |" for r in results]
    if fails:
        lines += ["", "## FAIL details", ""]
        lines += [f"### {r['id']} ({r['category']}, severity if fail: {r['severity_if_fail']})\n\n{r['note']}\n" for r in fails]
    else:
        lines += ["", "No FAIL results. Keep this report and rerun after any model, prompt, or tool change.", ""]

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"Report written to {out_path}")
    if fails:
        print(f"{len(fails)} FAIL result(s). Write each up with REPORT-TEMPLATE.md and report through the authorized channel.")
        sys.exit(1)

if __name__ == "__main__":
    main()
