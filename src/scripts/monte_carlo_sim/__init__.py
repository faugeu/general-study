"""
Finance simulation package.
Expose the main public functions/classes.
"""

from .config import IncomeParams, ExpenseParams, AssetParams, SimParams
from .utils import monthly_converter
from .processes.income import generate_income_path_deaton, generate_income_path_gibrat
from .processes.expenses import generate_expense_path
from .processes.returns import generate_independent_real_returns
from .simulation.wealth_path import simulate_one_path
from .simulation.monte_carlo import run_monte_carlo

__all__ = [
    "IncomeParams",
    "ExpenseParams",
    "AssetParams",
    "SimParams",
    "monthly_converter",
    "generate_income_path_deaton",
    "generate_income_path_gibrat",
    "generate_expense_path",
    "generate_independent_real_returns",
    "simulate_one_path",
    "run_monte_carlo",
]
