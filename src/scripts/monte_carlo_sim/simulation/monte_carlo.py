"""Monte Carlo driver that uses simulate_one_path repeatedly."""

from typing import Dict
import numpy as np

from ..config import IncomeParams, ExpenseParams, AssetParams, SimParams
from .wealth_path import simulate_one_path


def run_monte_carlo(
    n_paths: int,
    income_params: IncomeParams,
    expense_params: ExpenseParams,
    asset_params: AssetParams,
    sim_params: SimParams,
    use_income_model: str = "deaton",
) -> Dict[str, np.ndarray]:
    """
    Run n_paths independent Monte Carlo simulations.

    Returns dict with arrays shaped (n_paths, months):
      - W_all, s_all, y_all
    """
    months = sim_params.months
    W_all = np.zeros((n_paths, months), dtype=float)
    s_all = np.zeros((n_paths, months), dtype=float)
    y_all = np.zeros((n_paths, months), dtype=float)

    # Use a SeedSequence to spawn independent seeds if a global seed is provided.
    if sim_params.seed is not None:
        ss = np.random.SeedSequence(sim_params.seed)
    else:
        ss = np.random.SeedSequence()

    child_seeds = ss.spawn(n_paths)

    for i, child in enumerate(child_seeds):
        child_seed_int = int(np.random.default_rng(child).integers(1 << 31))
        out = simulate_one_path(
            income_params=income_params,
            expense_params=expense_params,
            asset_params=asset_params,
            sim_params=sim_params,
            use_income_model=use_income_model,
            seed=child_seed_int,
        )
        W_all[i, :] = out["W"]
        s_all[i, :] = out["s"]
        y_all[i, :] = out["y"]

    return {"W_all": W_all, "s_all": s_all, "y_all": y_all}
