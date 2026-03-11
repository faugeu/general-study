"""Expense / shock models."""

from typing import Optional
import numpy as np
from ..config import ExpenseParams


def generate_expense_path(
    params: ExpenseParams,
    months: int,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate expense series with rare lognormal shocks.

    E_t = e0 + I_t * (e0 * (exp(Z) - 1)), where I_t ~ Bernoulli(p_shock), Z ~ N(mu_z, sigma_z).
    """
    rng = np.random.default_rng(seed)
    expenses = np.full(months, params.e0, dtype=float)

    for t in range(months):
        if rng.random() < params.p_shock:
            Z = rng.normal(params.mu_shock_log, params.sigma_shock_log)
            shock = params.e0 * (np.exp(Z) - 1.0)
            expenses[t] = params.e0 + shock
        else:
            expenses[t] = params.e0

    return expenses
