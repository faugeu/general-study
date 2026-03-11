# results/ahp.py
from typing import Dict, Tuple, Any

import pandas as pd

# --- These imports assume your ahp_topsis package exposes same modules shown earlier ---
from ahp_topsis.weights import compute_global_subcriteria_weights
from ahp_topsis.topsis import topsis
from ahp_topsis.constants import CRITERIA, CRITERION_TYPES, get_decision_df


def compute_criteria_weights(
    prebuilt_matrices: dict,
) -> Tuple[Dict[str, float], Dict[str, float], Dict[str, list]]:
    """
    Convert the prebuilt/precomputed AHP matrices into the three objects the UI expects.

    Args
        prebuilt_matrices: dict written to st.session_state["ahp_matrices"] by the survey flow.
            Expected keys:
                - "main" -> {"weights_dict": {...}, "CR": ..., "status": ...}
                - one key per main criterion in lowercase (e.g. "financial security") -> {"weights_dict": {...}, ...}

    Returns
        main_weights: dict mapping main criterion -> weight (used to render top-level cards)
        global_sub_weights: dict mapping sub-criterion name -> global weight (suitable to pass straight to TOPSIS)
        subs_by_parent: dict mapping main criterion -> list of its sub-criteria names (used by the UI)
    """
    # main criteria
    if "main" not in prebuilt_matrices:
        raise KeyError(
            "prebuilt_matrices must include a 'main' key with top-level results"
        )

    criteria_result = prebuilt_matrices["main"]
    main_weights = criteria_result.get("weights_dict", {})

    # collect local sub-weights and build subs_by_parent
    local_sub_weights = {}
    subs_by_parent = {}

    for criterion in CRITERIA:
        key = criterion.lower()
        if key not in prebuilt_matrices:
            raise KeyError(
                f"Missing AHP matrix for criterion '{criterion}' (expected key '{key}')"
            )

        res = prebuilt_matrices[key]
        weights_dict = res.get("weights_dict", {})
        local_sub_weights[criterion] = weights_dict
        subs_by_parent[criterion] = weights_dict

    # compute flattened global sub-criteria weights (AHP: main_weights * local weights)
    global_sub_weights = compute_global_subcriteria_weights(
        main_weights, local_sub_weights
    )

    return main_weights, global_sub_weights, subs_by_parent


def compute_topsis(global_sub_weights: Dict[str, float]) -> Dict[str, Any]:
    """
    Run TOPSIS using the provided global sub-criteria weights and return a dict suitable for the UI.

    Args
        global_sub_weights: dict mapping sub-criterion name -> weight (must match the decision matrix column names)

    Returns
        A dict with keys:
            - 'ranking_df' : DataFrame with ranking results (alternatives sorted by closeness)
            - 'score_matrix': DataFrame with sub-criteria as rows and alternatives as columns (good for heatmaps)
            - 'weighted_df': DataFrame alternatives x sub-criteria after weighting (as returned by topsis function)
            - 'topsis_result': the raw return from the topsis(...) function for advanced uses
    """
    decision_df = get_decision_df()

    topsis_result = topsis(
        decision_df=decision_df,
        weights_dict=global_sub_weights,
        criterion_types=CRITERION_TYPES,
    )

    # expected fields from your topsis implementation
    ranking_df = topsis_result.get("ranking_df")
    weighted_df = topsis_result.get("weighted_df")

    # create score_matrix shaped sub-criteria x alternatives for heatmap rendering:
    # - weighted_df is expected to be alternatives x subcriteria (rows = alternatives)
    # - transpose it so rows=subcriteria, cols=alternatives
    if weighted_df is None:
        raise ValueError(
            "topsis_result missing 'weighted_df' — ensure topsis returns weighted_df"
        )

    score_matrix = weighted_df.transpose().copy()
    # optional: make indices and columns human-friendly (if they're not already)
    score_matrix.index.name = "Sub-criterion"
    score_matrix.columns.name = "Alternative"

    return {
        "ranking_df": ranking_df,
        "score_matrix": score_matrix,
        "weighted_df": weighted_df,
        "topsis_result": topsis_result,
    }
