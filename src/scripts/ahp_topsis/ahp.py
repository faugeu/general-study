"""AHP utilities: pairwise matrices, weights, consistency, and CR suggestions."""

import numpy as np
import pandas as pd
from itertools import combinations

RI_TABLE = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49,
}


def validate_ahp_value(value):
    value = float(value)
    if value <= 0:
        raise ValueError("AHP value must be greater than 0.")
    return value


def validate_comparisons(items, comparisons, name="comparisons"):
    expected_pairs = set(combinations(items, 2))
    provided_pairs = set(comparisons.keys())

    missing = expected_pairs - provided_pairs
    extra = provided_pairs - expected_pairs

    if missing:
        raise ValueError(f"Missing pairs in {name}: {missing}")
    if extra:
        raise ValueError(f"Unexpected pairs in {name}: {extra}")

    for _, value in comparisons.items():
        validate_ahp_value(value)


def build_pairwise_matrix(items, comparisons):
    validate_comparisons(items, comparisons)

    n = len(items)
    idx = {item: i for i, item in enumerate(items)}
    matrix = np.ones((n, n), dtype=float)

    for (a, b), value in comparisons.items():
        value = validate_ahp_value(value)
        i, j = idx[a], idx[b]
        matrix[i, j] = value
        matrix[j, i] = 1.0 / value

    return matrix


def ahp_weights_from_matrix(matrix):
    matrix = np.array(matrix, dtype=float)
    n = matrix.shape[0]

    eigvals, eigvecs = np.linalg.eig(matrix)
    max_idx = int(np.argmax(eigvals.real))

    lambda_max = eigvals[max_idx].real
    principal_vec = np.abs(eigvecs[:, max_idx].real)
    weights = principal_vec / principal_vec.sum()

    ci = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    ri = RI_TABLE.get(n, 1.49)
    cr = ci / ri if ri != 0 else 0.0

    return weights, lambda_max, ci, cr


def compute_crisp_consistency(items, comparisons, node_name="Node"):
    matrix = build_pairwise_matrix(items, comparisons)
    weights, lambda_max, ci, cr = ahp_weights_from_matrix(matrix)

    return {
        "node": node_name,
        "matrix_df": pd.DataFrame(matrix, index=items, columns=items),
        "weights_df": pd.DataFrame({
            "Item": items,
            "Weight": weights,
        }).sort_values("Weight", ascending=False).reset_index(drop=True),
        "weights_dict": dict(zip(items, weights)),
        "lambda_max": lambda_max,
        "CI": ci,
        "CR": cr,
        "status": "OK" if cr <= 0.10 else "REVIEW",
    }


_SAATY_VALUES = [
    1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2,
    1, 2, 3, 4, 5, 6, 7, 8, 9,
]


def _nearest_saaty(value: float) -> float:
    """Round a positive float to the nearest Saaty scale value."""
    return min(_SAATY_VALUES, key=lambda s: abs(s - value))


def suggest_consistency_fix(items, comparisons, top_n: int = 3) -> list[dict]:
    """Return the most inconsistent pairs with nearest Saaty suggestions."""
    matrix = build_pairwise_matrix(items, comparisons)
    weights, _, _, _ = ahp_weights_from_matrix(matrix)
    n = len(items)

    rows = []
    for i in range(n):
        for j in range(i + 1, n):
            current = matrix[i][j]
            ideal = weights[i] / weights[j] if weights[j] != 0 else 1.0
            suggested = _nearest_saaty(ideal)
            error = abs(current - ideal)

            if suggested != current:
                rows.append({
                    "pair": (items[i], items[j]),
                    "current_value": round(current, 4),
                    "ideal_value": round(ideal, 4),
                    "suggested": suggested,
                    "error": round(error, 4),
                })

    rows.sort(key=lambda x: x["error"], reverse=True)
    return rows[:top_n]
