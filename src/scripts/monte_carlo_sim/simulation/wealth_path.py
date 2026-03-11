"""Wealth dynamics / single-path simulation (independent-asset returns)."""

from typing import Dict, Optional
import numpy as np

from ..config import SimParams, IncomeParams, ExpenseParams, AssetParams
from ..utils import monthly_converter
from ..processes.income import generate_income_path_deaton, generate_income_path_gibrat
from ..processes.expenses import generate_expense_path
from ..processes.returns import generate_independent_real_returns


def simulate_one_path(
    income_params: IncomeParams,
    expense_params: ExpenseParams,
    asset_params: AssetParams,
    sim_params: SimParams,
    use_income_model: str = "deaton",
    seed: Optional[int] = None,
) -> Dict[str, np.ndarray]:
    """
    Simulate a single Monte Carlo path of income, expenses, and wealth using
    independent asset returns.

    Returns
    -------
    dict of arrays (months,) with keys:
        y : income
        e : expenses
        s : savings (income_net - expense)
        W : wealth
        r_portfolio : realized portfolio return per month
        r_assets : realized returns per asset (months x n_assets)
    """

    rng = np.random.default_rng(seed)

    # Spawn internal seeds for independent streams
    seed_income = int(rng.integers(1 << 30))
    seed_exp = int(rng.integers(1 << 30))
    seed_assets = int(rng.integers(1 << 30))

    months = sim_params.months

    # Convert rates
    g_nominal_monthly = monthly_converter(income_params.g_nominal_annual)
    i_monthly = monthly_converter(sim_params.i_annual)

    # Real growth for income (approx Fisher-style)
    g_real_monthly = (1.0 + g_nominal_monthly) / (1.0 + i_monthly) - 1.0

    # -------------------------
    # Income series
    # -------------------------
    if use_income_model == "deaton":
        y = generate_income_path_deaton(
            income_params,
            g_real_monthly,
            months,
            seed=seed_income,
        )

    elif use_income_model == "gibrat":
        y = generate_income_path_gibrat(
            y0=income_params.y0,
            g_real_monthly=g_real_monthly,
            rho=income_params.rho,
            sigma_z=income_params.sigma_perm,
            months=months,
            seed=seed_income,
        )

    else:
        raise ValueError("Unknown income model: choose 'deaton' or 'gibrat'")

    # -------------------------
    # Expenses
    # -------------------------
    e = generate_expense_path(
        expense_params,
        months,
        seed=seed_exp,
    )

    # -------------------------
    # Asset returns (independent)
    # -------------------------
    r_assets = generate_independent_real_returns(
        asset_params,
        months,
        monthly_inflation=i_monthly,
        seed=seed_assets,
    )

    # -------------------------
    # Portfolio return
    # -------------------------
    weights = np.asarray(asset_params.weights, dtype=float)

    if weights.ndim != 1 or weights.size != r_assets.shape[1]:
        raise ValueError(
            "weights length must match number of assets in asset_params.mu_nominal"
        )

    r_portfolio = (r_assets * weights).sum(axis=1)

    # -------------------------
    # Savings and wealth evolution
    # -------------------------
    s = np.empty(months, dtype=float)
    W = np.empty(months, dtype=float)

    W[0] = sim_params.W0

    for t in range(months):
        y_net = max(0.0, y[t] * (1.0 - sim_params.tau))
        s[t] = y_net - e[t]

        if t == 0:
            W[t] = (sim_params.W0 + s[t]) * (1.0 + r_portfolio[t])
        else:
            W[t] = (W[t - 1] + s[t]) * (1.0 + r_portfolio[t])

    return {
        "y": y,
        "e": e,
        "s": s,
        "W": W,
        "r_portfolio": r_portfolio,
        "r_assets": r_assets,
    }
