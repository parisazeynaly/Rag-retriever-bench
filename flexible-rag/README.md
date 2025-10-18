See main README in suite.
---

## 📑 Research Pack (This Folder)
- **Report (filled):** `reports/paper_filled.md`
- **Report templates:** `reports/paper_template.md` and `.tex`
- **Results:** `out/benchmark.json`, `out/ablation.csv`, `out/error_analysis.md`
- **Figure:** `reports/figures/quality_latency.png`

### Re-run evaluation
```bash
# produce run + metrics
python scripts/eval_bench.py --k 10
# draw quality-vs-latency chart
python scripts/plot_latency_quality.py
```

> Replace the JSON/CSV/PNG in `out/` and `reports/figures/` with your real runs to update the report.
