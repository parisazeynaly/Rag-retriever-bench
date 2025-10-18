import numpy as np

def is_sufficient(candidates_df, min_docs: int = 4) -> bool:
    if len(candidates_df) < min_docs:
        return False
    # simple heuristic: mean score above 40th percentile
    return np.mean(candidates_df["score"]) > np.percentile(candidates_df["score"], 40)
