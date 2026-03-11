"""results/ahp.py — AHP weight computation and TOPSIS scoring."""

import numpy as np
import pandas as pd

from results.constants import (
    ALTERNATIVES,
    ALT_SUBSCORES,
    CRIT_RAW_MAP,
)


def ahp_weights(matrix: pd.DataFrame) -> np.ndarray:
    """Compute priority vector from a pairwise comparison matrix."""
    arr = matrix.values.astype(float)
    col_sums = arr.sum(axis=0)
    norm = arr / col_sums
    return norm.mean(axis=1)


def compute_criteria_weights(
    matrices: dict[str, pd.DataFrame],
) -> tuple[dict[str, float], dict[str, float], dict[str, list[tuple[str, float]]]]:
    """
    Returns:
        main_weights   : {raw_criterion_name: global_weight}
        sub_weights    : {short_sub_name: global_weight}
        subs_by_parent : {display_crit_label: [(sub_name, local_weight), ...]}
    """
    main_w = ahp_weights(matrices["main"])
    crit_names = list(matrices["main"].index)
    main_weights = dict(zip(crit_names, main_w))

    sub_weights: dict[str, float] = {}
    subs_by_parent: dict[str, list[tuple[str, float]]] = {
        label: [] for _, label in CRIT_RAW_MAP.values()
    }

    for raw_crit, (mat_key, crit_label) in CRIT_RAW_MAP.items():
        parent_w = main_weights.get(raw_crit, 0.0)
        local_w = ahp_weights(matrices[mat_key])
        sub_names = list(matrices[mat_key].index)
        for name, lw in zip(sub_names, local_w):
            short = _shorten_subcrit(name)
            sub_weights[short] = lw * parent_w
            subs_by_parent[crit_label].append((name, lw))

    return main_weights, sub_weights, subs_by_parent


def compute_topsis(sub_weights: dict[str, float]) -> dict[str, float]:
    """
    Weighted-sum score per alternative using AHP sub-weights
    and fixed ALT_SUBSCORES reference values.
    Returns {alternative: score}.
    """
    scores = np.zeros(len(ALTERNATIVES))
    total_w = 0.0
    for sub, w in sub_weights.items():
        if sub in ALT_SUBSCORES:
            scores += w * np.array(ALT_SUBSCORES[sub])
            total_w += w
    if total_w > 0:
        scores /= total_w
    return dict(zip(ALTERNATIVES, scores))


def _shorten_subcrit(name: str) -> str:
    mapping = {"Ability to save money": "Ability to save"}
    return mapping.get(name, name)
