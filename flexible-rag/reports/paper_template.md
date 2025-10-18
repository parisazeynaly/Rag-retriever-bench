---
title: "Flexible RAG: Hybrid Retrieval, Routing, and Re-Ranking"
authors: ["<Your Name>"]
affiliation: "<Your University or Lab>"
date: "<YYYY-MM>"
abstract: |
  We present a lean Retrieval-Augmented Generation (RAG) system emphasizing retriever quality.
  Our contributions are: (i) a hybrid retrieval baseline (dense+sparse), (ii) a lightweight
  re-ranking stage, and (iii) an optional semantic routing/HyDE. We report improvements in Hit@k
  and nDCG at modest latency costs, with ablations per component.
keywords: ["RAG", "Information Retrieval", "Re-ranking", "Hybrid Search", "Semantic Routing"]
---

# 1. Introduction
Motivation, problem statement, and contributions.

# 2. Related Work
Briefly discuss dense retrieval, BM25, re-ranking (cross-encoder, ColBERT), and routing.

# 3. Method
## 3.1 Indexing & Chunking
Describe chunk size/overlap, embedding model.
## 3.2 Hybrid Retrieval
Combine dense similarity and BM25; formula and design.
## 3.3 Re-ranking
Choice of model(s), latency trade-offs.
## 3.4 Optional: HyDE / Routing
Where and when they help.

# 4. Experiments
## 4.1 Datasets
Public benchmark(s) + your in-domain data.
## 4.2 Metrics
Hit@k, nDCG@k, latency; report hardware.
## 4.3 Ablation
Baseline → +rerank → +HyDE/Router; tables/plots.

# 5. Results & Analysis
Quantitative results and case studies; error analysis.

# 6. Limitations and Threats to Validity
Data drift, domain shift, reproducibility considerations.

# 7. Conclusion & Future Work

# References
Cite key papers/tools used.
