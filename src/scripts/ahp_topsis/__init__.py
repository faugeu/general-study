"""
AHP-TOPSIS pipeline: AHP for criteria weights + TOPSIS for investment alternatives ranking.
"""

from .constants import (
    ALTERNATIVES,
    CRITERIA,
    SUBCRITERIA,
    DECISION_MATRIX,
    CRITERION_TYPES,
    get_decision_df,
)
from .ahp import compute_crisp_consistency, suggest_consistency_fix
from .recommend import (
    recommend_ahp_topsis,
    quick_recommend,
    create_input_template,
    print_final_summary,
)

__all__ = [
    "ALTERNATIVES",
    "CRITERIA",
    "SUBCRITERIA",
    "DECISION_MATRIX",
    "CRITERION_TYPES",
    "get_decision_df",
    "compute_crisp_consistency",
    "suggest_consistency_fix",
    "recommend_ahp_topsis",
    "quick_recommend",
    "create_input_template",
    "print_final_summary",
]
