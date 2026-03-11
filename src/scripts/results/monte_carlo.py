"""results/monte_carlo.py — Monte Carlo simulation engine."""

import numpy as np

from results.constants import ALT_PARAMS, ALTERNATIVES, N_SIMS


def run_monte_carlo(
    T: int,
    monthly_savings: float,
    initial_wealth: float,
    annual_r: float,
    annual_v: float,
    n: int = N_SIMS,
) -> dict:
    """
    Run n Monte Carlo paths.
    Returns dict with keys: runs, median, q10, q90, finals.
    """
    mr = annual_r / 12.0
    mv = annual_v / np.sqrt(12.0)

    rng = np.random.default_rng()
    # Shape: (n, T)
    noise = rng.standard_normal((n, T))
    monthly_ret = 1.0 + mr + mv * noise  # (n, T)

    # Vectorised path calculation
    portfolio = np.empty((n, T))
    pf = np.full(n, initial_wealth, dtype=float)
    for t in range(T):
        pf = pf * monthly_ret[:, t] + monthly_savings
        portfolio[:, t] = pf

    return {
        "runs": portfolio,
        "median": np.median(portfolio, axis=0),
        "q10": np.percentile(portfolio, 10, axis=0),
        "q90": np.percentile(portfolio, 90, axis=0),
        "finals": portfolio[:, -1],
    }


def run_all_simulations(
    time_horizon: int,
    monthly_savings: float,
    initial_wealth: float,
) -> dict[str, dict]:
    """Run simulations for all alternatives. Returns {alt_name: result}."""
    return {
        alt: run_monte_carlo(
            T=time_horizon,
            monthly_savings=monthly_savings,
            initial_wealth=initial_wealth,
            annual_r=ALT_PARAMS[alt]["r"],
            annual_v=ALT_PARAMS[alt]["v"],
        )
        for alt in ALTERNATIVES
    }
