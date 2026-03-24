from ahp_topsis import compute_crisp_consistency
from .constants import MATRICES


def build_ahp_matrices(survey_results: dict) -> dict:
    """
    Convert raw survey results into full AHP consistency objects.

    Returns
    -------
    dict
        matrix_key -> result dict from compute_crisp_consistency()
    """
    results = {}

    for matrix in MATRICES:
        key = matrix["key"]
        criteria = matrix["criteria"]

        comparisons = survey_results[key]

        result = compute_crisp_consistency(
            items=criteria,
            comparisons=comparisons,
            node_name=key,
        )

        results[key] = result

    return results
