#!/usr/bin/env python
"""Read metrics and latency logs and plot quality-latency curves.

Input:
  out/metrics.json
  out/latency.json (optional): [{"setting":"baseline","latency_ms":...}, ...]
Output:
  out/quality_latency.png
"""
import json, os
import matplotlib.pyplot as plt

def main():
    metrics = json.load(open("out/metrics.json"))
    latency_path = "out/latency.json"
    series = [{"setting":"current", "hit@10":metrics.get("hit@10",0), "ndcg@10":metrics.get("ndcg@10",0), "latency_ms": None}]
    if os.path.exists(latency_path):
        with open(latency_path) as f:
            latency = json.load(f)
        # align by index if multiple settings exist
        for i, row in enumerate(latency):
            s = { "setting": row.get("setting", f"run-{i}"),
                  "hit@10": metrics.get("hit@10", 0),
                  "ndcg@10": metrics.get("ndcg@10", 0),
                  "latency_ms": row.get("latency_ms", None) }
            series.append(s)

    xs = [s.get("latency_ms", 0) or 0 for s in series]
    ys = [s["hit@10"] for s in series]

    # Plot 1: latency vs hit@10
    plt.figure()
    plt.scatter(xs, ys)
    for s, x, y in zip(series, xs, ys):
        plt.text(x, y, s["setting"])
    plt.xlabel("Latency (ms)")
    plt.ylabel("Hit@10")
    plt.title("Quality vs Latency (Hit@10)")
    plt.savefig("out/quality_latency.png", bbox_inches="tight")

if __name__ == "__main__":
    main()
