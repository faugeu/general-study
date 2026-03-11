"""Parameter dataclasses for simulations."""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np


@dataclass
class IncomeParams:
    """Parameters for income processes."""

    y0: float = 5_000.0
    rho: float = 0.85
    sigma_perm: float = 0.05  # permanent shock sd (log)
    sigma_trans: float = 0.15  # transitory shock sd (log)
    g_nominal_annual: float = 0.024


@dataclass
class ExpenseParams:
    """Parameters for expense (rare shock) process."""

    e0: float = 3_000.0
    p_shock: float = 0.02
    mu_shock_log: float = float(np.log(1.5))
    sigma_shock_log: float = 0.8


@dataclass
class AssetParams:
    """
    Asset return parameters.

    - mu_nominal: array of annual nominal means (e.g., 0.067 for 6.7% p.a.).
    - sigma_nominal: array of annual nominal standard deviations (volatility).
    - weights: portfolio weights (optional; only used inside simulation to build portfolio).
    """

    mu_nominal: np.ndarray = field(default_factory=lambda: np.array([0.067, 0.02]))
    sigma_nominal: np.ndarray = field(default_factory=lambda: np.array([0.20, 0.06]))
    weights: np.ndarray = field(default_factory=lambda: np.array([1.0, 0.0]))


@dataclass
class SimParams:
    """Simulation-level parameters."""

    W0: float = 10_000.0  # initial wealth
    i_annual: float = 0.02  # annual inflation / nominal interest
    tau: float = 0.0  # income tax rate (fraction)
    months: int = 12
    seed: Optional[int] = None  # optional global seed for reproducibility
