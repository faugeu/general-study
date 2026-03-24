"""TOPSIS: normalize, weight, ideal points, closeness, ranking."""

import numpy as np
import pandas as pd


def topsis(decision_df, weights_dict, criterion_types):
    criteria = list(decision_df.index)
    alternatives = list(decision_df.columns)

    X = decision_df.values.astype(float)

    denom = np.sqrt((X**2).sum(axis=1, keepdims=True))
    normalized = X / denom

    weights = np.array([weights_dict[c] for c in criteria], dtype=float).reshape(-1, 1)
    weighted = normalized * weights

    ideal_best = []
    ideal_worst = []

    for i, c in enumerate(criteria):
        row = weighted[i, :]
        if criterion_types[c] == "benefit":
            ideal_best.append(row.max())
            ideal_worst.append(row.min())
        else:
            ideal_best.append(row.min())
            ideal_worst.append(row.max())

    ideal_best = np.array(ideal_best).reshape(-1, 1)
    ideal_worst = np.array(ideal_worst).reshape(-1, 1)

    d_plus = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=0))
    d_minus = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=0))

    closeness = d_minus / (d_plus + d_minus)

    ranking_df = (
        pd.DataFrame(
            {
                "Alternative": alternatives,
                "Closeness": closeness,
            }
        )
        .sort_values("Closeness", ascending=False)
        .reset_index(drop=True)
    )

    ranking_df["Rank"] = range(1, len(ranking_df) + 1)

    normalized_df = pd.DataFrame(normalized, index=criteria, columns=alternatives)
    weighted_df = pd.DataFrame(weighted, index=criteria, columns=alternatives)

    ideal_df = pd.DataFrame(
        {
            "Criterion": criteria,
            "Type": [criterion_types[c] for c in criteria],
            "Ideal Best": ideal_best.flatten(),
            "Ideal Worst": ideal_worst.flatten(),
        }
    )

    return {
        "normalized_df": normalized_df,
        "weighted_df": weighted_df,
        "ideal_df": ideal_df,
        "ranking_df": ranking_df,
    }


def explain_top_alternative(top_alternative, weighted_df, global_weights, top_n=4):
    contributions = []

    for criterion in weighted_df.index:
        contribution = weighted_df.loc[criterion, top_alternative]
        contributions.append(
            {
                "Sub-criterion": criterion,
                "Global weight": global_weights[criterion],
                "Weighted value": contribution,
            }
        )

    contrib_df = (
        pd.DataFrame(contributions)
        .sort_values("Weighted value", ascending=False)
        .reset_index(drop=True)
    )

    return contrib_df.head(min(top_n, len(contrib_df))), contrib_df
