import numpy as np
import pandas as pd
from .constants import MATRICES


def build_ahp_matrices(survey_results: dict) -> dict:
    """
    Convert raw pairwise survey results into symmetric AHP DataFrames.

    Parameters
    ----------
    survey_results : dict
        Keyed by matrix key (e.g. "main", "fin_sec", ...).
        Each value is a dict  {(a, b): float}.

    Returns
    -------
    dict
        Keyed by matrix key → pd.DataFrame (criteria × criteria), rounded to 3 dp.
    """
    all_matrices = {}

    for matrix in MATRICES:
        key = matrix["key"]
        crit = matrix["criteria"]
        n = len(crit)
        idx = {c: i for i, c in enumerate(crit)}
        mat = np.ones((n, n))

        for (a, b), val in survey_results[key].items():
            i, j = idx[a], idx[b]
            mat[i][j] = val
            mat[j][i] = 1.0 / val if val != 0 else 1.0

        all_matrices[key] = pd.DataFrame(mat, index=crit, columns=crit).round(3)

    return all_matrices
