"""
Configuration module for Mortgage Calculator.

This module contains all configuration constants and default values
used throughout the application.
"""

from typing import Final

# Application Settings
APP_TITLE: Final[str] = "Mortgage Repayments Calculator"

# Default Input Values
DEFAULT_HOME_VALUE: Final[int] = 500000
DEFAULT_DEPOSIT: Final[int] = 100000
DEFAULT_INTEREST_RATE: Final[float] = 5.5
DEFAULT_LOAN_TERM_YEARS: Final[int] = 30

# Validation Constraints
MIN_HOME_VALUE: Final[int] = 0
MIN_DEPOSIT: Final[int] = 0
MIN_INTEREST_RATE: Final[float] = 0.0
MIN_LOAN_TERM: Final[int] = 1
MAX_LOAN_TERM: Final[int] = 50

# Calculation Constants
MONTHS_PER_YEAR: Final[int] = 12
PERCENTAGE_DIVISOR: Final[int] = 100

# Display Settings
CURRENCY_SYMBOL: Final[str] = "$"
DECIMAL_PLACES_MONTHLY: Final[int] = 2
DECIMAL_PLACES_TOTAL: Final[int] = 0
