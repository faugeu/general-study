"""results/monte_carlo.py — Monte Carlo simulation engine."""

import numpy as np

from results.constants import ALT_PARAMS, ALTERNATIVES, N_SIMS

from monte_carlo_sim.config import IncomeParams, ExpenseParams, AssetParams, SimParams
from monte_carlo_sim.simulation.monte_carlo import run_monte_carlo


def run_all_simulations(
    time_horizon: int,
    initial_wealth: float,
    monthly_income: float,
    monthly_spending: float,
) -> dict[str, dict]:

    income = IncomeParams(
        y0=monthly_income,
        rho=0.75,
        sigma_perm=0.07,
        sigma_trans=0.06,
        g_nominal_annual=0.05,
    )

    expense = ExpenseParams(
        e0=monthly_spending,
        p_shock=0.05,
        mu_shock_log=np.log(1.5),
        sigma_shock_log=0.8,
    )

    sim = SimParams(
        W0=initial_wealth,
        i_annual=0.02,
        tau=0.0,
        months=time_horizon,
        seed=12345,
    )

    asset_configs = {
        "Bank Deposits": AssetParams(
            mu_nominal=np.array([0.0395]),
            sigma_nominal=np.array([0.0057]),
            weights=np.array([1.0]),
        ),
        "Stocks": AssetParams(
            mu_nominal=np.array([0.0612]),
            sigma_nominal=np.array([0.1542]),
            weights=np.array([1.0]),
        ),
        "Mutual Funds": AssetParams(
            mu_nominal=np.array([0.0552]),
            sigma_nominal=np.array([0.0949]),
            weights=np.array([1.0]),
        ),
        "Real Estate & Commodities": AssetParams(
            mu_nominal=np.array([0.0482]),
            sigma_nominal=np.array([0.1568]),
            weights=np.array([1.0]),
        ),
    }

    results = {}

    for name, asset_params in asset_configs.items():

        sim_result = run_monte_carlo(
            n_paths=1000,
            income_params=income,
            expense_params=expense,
            asset_params=asset_params,
            sim_params=sim,
            use_income_model="deaton",
        )

        W_all = sim_result["W_all"]

        results[name] = {
            "runs": W_all,
            "median": np.median(W_all, axis=0),
            "q10": np.percentile(W_all, 10, axis=0),
            "q90": np.percentile(W_all, 90, axis=0),
            "finals": W_all[:, -1],
        }

    return results
