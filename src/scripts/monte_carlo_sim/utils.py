"""Small helpers used across the package."""

from typing import Optional


def monthly_converter(rate_annual: float) -> float:
    """
    Convert an annual rate to the equivalent monthly rate assuming monthly compounding:
        (1 + r_annual)^(1/12) - 1
    """
    return (1.0 + rate_annual) ** (1.0 / 12.0) - 1.0
