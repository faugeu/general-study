"""Income process implementations."""

from typing import Optional
import numpy as np
from ..utils import monthly_converter
from ..config import IncomeParams


def generate_income_path_gibrat(
    y0: float,
    g_real_monthly: float,
    rho: float,
    sigma_z: float,
    months: int,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Gibrat-style log-linear income process.

    ln(y_t) = ln(y_{t-1}) + ln(1 + g_real_monthly) + z_t
    z_t = rho * z_{t-1} + eps_t, eps_t ~ N(0, sigma_z^2)

    sigma_z is the standard deviation of the AR(1) shock in log units.
    """
    rng = np.random.default_rng(seed)
    log_y = np.empty(months, dtype=float)
    z = np.empty(months, dtype=float)

    log_y[0] = np.log(y0)
    # initialize stationary z (approx) if |rho| < 1
    if abs(rho) < 1.0:
        z[0] = rng.normal(0.0, sigma_z / np.sqrt(1.0 - rho**2))
    else:
        z[0] = rng.normal(0.0, sigma_z)

    log_growth = np.log(1.0 + g_real_monthly)

    for t in range(1, months):
        eps = rng.normal(0.0, sigma_z)
        z[t] = rho * z[t - 1] + eps
        log_y[t] = log_y[t - 1] + log_growth + z[t]

    return np.exp(log_y)


def generate_income_path_deaton(
    params: IncomeParams,
    g_real_monthly: float,
    months: int,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Deaton / Carroll-style process:
      P_t (permanent) follows random walk in logs with drift log(1 + g_real_monthly)
      transitory shock multiplies P_t each period.

    Returns series of levels y_t = P_t * exp(epsilon_t).
    """
    rng = np.random.default_rng(seed)

    P = np.empty(months, dtype=float)
    y = np.empty(months, dtype=float)

    P[0] = params.y0
    log_growth = np.log(1.0 + g_real_monthly)

    # Permanent component
    for t in range(1, months):
        eta = rng.normal(0.0, params.sigma_perm)
        P[t] = P[t - 1] * np.exp(log_growth + eta)

    # Transitory shocks and final income
    for t in range(months):
        epsilon = rng.normal(0.0, params.sigma_trans)
        y[t] = P[t] * np.exp(epsilon)

    return y
