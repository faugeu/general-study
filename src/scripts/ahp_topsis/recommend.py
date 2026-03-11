"""AHP + TOPSIS recommendation pipeline."""

import pandas as pd

from .constants import (
    CRITERIA,
    SUBCRITERIA,
    CRITERION_TYPES,
    get_decision_df,
)
from .ahp import compute_crisp_consistency
from .weights import compute_global_subcriteria_weights
from .topsis import topsis, explain_top_alternative


def recommend_ahp_topsis(
    criteria_comparisons,
    subcriteria_comparisons,
):
    decision_df = get_decision_df()

    criteria_result = compute_crisp_consistency(
        CRITERIA,
        criteria_comparisons,
        node_name="Main criteria",
    )
    criteria_weights = criteria_result["weights_dict"]

    sub_results = {}
    local_sub_weights = {}
    consistency_rows = []

    consistency_rows.append(
        {
            "Node": "Main criteria",
            "CR": criteria_result["CR"],
            "Status": criteria_result["status"],
        }
    )

    for criterion in CRITERIA:
        res = compute_crisp_consistency(
            SUBCRITERIA[criterion],
            subcriteria_comparisons[criterion],
            node_name=criterion,
        )
        sub_results[criterion] = res
        local_sub_weights[criterion] = res["weights_dict"]

        consistency_rows.append(
            {
                "Node": criterion,
                "CR": res["CR"],
                "Status": res["status"],
            }
        )

    global_weights = compute_global_subcriteria_weights(
        criteria_weights, local_sub_weights
    )

    global_weights_df = (
        pd.DataFrame(
            {
                "Sub-criterion": list(global_weights.keys()),
                "Global weight": list(global_weights.values()),
            }
        )
        .sort_values("Global weight", ascending=False)
        .reset_index(drop=True)
    )

    topsis_result = topsis(
        decision_df=decision_df,
        weights_dict=global_weights,
        criterion_types=CRITERION_TYPES,
    )

    final_ranking = topsis_result["ranking_df"]
    top_alternative = final_ranking.iloc[0]["Alternative"]

    top_preview, top_full = explain_top_alternative(
        top_alternative=top_alternative,
        weighted_df=topsis_result["weighted_df"],
        global_weights=global_weights,
        top_n=4,
    )

    explanation_text = (
        f"The top recommended alternative is '{top_alternative}' because it "
        f"is closest to the ideal solution after weighting all sub-criteria "
        f"using AHP preferences."
    )

    return {
        "criteria_result": criteria_result,
        "subcriteria_results": sub_results,
        "global_weights": global_weights,
        "global_weights_df": global_weights_df,
        "consistency_report": pd.DataFrame(consistency_rows),
        "topsis_result": topsis_result,
        "final_ranking": final_ranking,
        "top_alternative": top_alternative,
        "top_contributions_preview": top_preview,
        "top_contributions_full": top_full,
        "explanation_text": explanation_text,
    }


def quick_recommend(user_payload):
    return recommend_ahp_topsis(
        criteria_comparisons=user_payload["criteria_comparisons"],
        subcriteria_comparisons=user_payload["subcriteria_comparisons"],
    )


def create_input_template():
    return {
        "criteria_comparisons": {
            ("Financial security", "Personal characteristics"): None,
            ("Financial security", "Profitability"): None,
            ("Financial security", "Readiness"): None,
            ("Personal characteristics", "Profitability"): None,
            ("Personal characteristics", "Readiness"): None,
            ("Profitability", "Readiness"): None,
        },
        "subcriteria_comparisons": {
            "Financial security": {
                ("Availability", "Information"): None,
                ("Availability", "Simplicity"): None,
                ("Availability", "Stability"): None,
                ("Information", "Simplicity"): None,
                ("Information", "Stability"): None,
                ("Simplicity", "Stability"): None,
            },
            "Personal characteristics": {
                ("Ability to save money", "Financial priorities"): None,
                ("Ability to save money", "Level of income"): None,
                ("Financial priorities", "Level of income"): None,
            },
            "Profitability": {
                ("Liquidity", "Return"): None,
                ("Liquidity", "Volatility"): None,
                ("Return", "Volatility"): None,
            },
            "Readiness": {
                ("Experience", "Financial education"): None,
                ("Experience", "Risk attitude"): None,
                ("Financial education", "Risk attitude"): None,
            },
        },
    }


def print_final_summary(result):
    """Print final recommendation summary (CLI-safe, no display())."""
    top = result["top_alternative"]
    score = result["final_ranking"].iloc[0]["Closeness"]

    print("Final Recommendation")
    print("--------------------")
    print(f"Top alternative: {top}")
    print(f"TOPSIS closeness score: {score:.6f}")
    print("\nTop 5 influential sub-criteria:")
    print(result["top_contributions_preview"].to_string(index=False))
