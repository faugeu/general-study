"""Asset return generators (independent assets)."""

from typing import Optional
import numpy as np
from ..utils import monthly_converter
from ..config import AssetParams


def generate_independent_real_returns(
    asset_params: AssetParams,
    months: int,
    monthly_inflation: float,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Generate monthly *real* returns for each asset independently.

    Nominal model (monthly compounding, GBM-style lognormal increments):
        R_nominal_t = exp( (mu_m - 0.5*sigma_m^2) + sigma_m * z_t ) - 1
    where:
        mu_m    = monthly nominal mean from annual mu_nominal
        sigma_m = monthly volatility from annual sigma_nominal
        z_t ~ N(0,1)

    Real returns (Fisher-like adjustment):
        r_real = (1 + R_nominal) / (1 + i_m) - 1

    Returns: array shape (months, n_assets)
    """
    rng = np.random.default_rng(seed)
    mu_annual = np.asarray(asset_params.mu_nominal, dtype=float)
    sigma_annual = np.asarray(asset_params.sigma_nominal, dtype=float)

    n = mu_annual.size
    # convert to monthly equivalents (compounding)
    mu_monthly = (1.0 + mu_annual) ** (1.0 / 12.0) - 1.0
    # approximate conversion of annual vol -> monthly vol (assuming iid monthly increments)
    sigma_monthly = sigma_annual / np.sqrt(12.0)

    out = np.zeros((months, n), dtype=float)
    i_m = monthly_inflation

    for t in range(months):
        z = rng.standard_normal(size=n)
        # lognormal nominal return
        log_r = (np.log(1.0 + mu_monthly) - 0.5 * sigma_monthly**2) + sigma_monthly * z
        R_nominal = np.exp(log_r) - 1.0
        # convert to real
        r_real = (1.0 + R_nominal) / (1.0 + i_m) - 1.0
        out[t, :] = r_real

    return out
