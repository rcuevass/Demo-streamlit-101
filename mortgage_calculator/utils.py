"""
Utility functions for Mortgage Calculator.

This module contains helper functions for formatting, validation,
and data conversion.
"""

import pandas as pd
from typing import Optional

from .config import (
    CURRENCY_SYMBOL,
    DECIMAL_PLACES_MONTHLY,
    DECIMAL_PLACES_TOTAL,
)
from .models import PaymentSchedule


def format_currency(
    amount: float,
    decimal_places: int = DECIMAL_PLACES_TOTAL,
    symbol: str = CURRENCY_SYMBOL,
) -> str:
    """
    Format a number as currency.
    
    Args:
        amount: The amount to format
        decimal_places: Number of decimal places to display
        symbol: Currency symbol to use
        
    Returns:
        Formatted currency string
        
    Example:
        >>> format_currency(1234.56, 2)
        '$1,234.56'
    """
    return f"{symbol}{amount:,.{decimal_places}f}"


def format_monthly_payment(amount: float) -> str:
    """
    Format a monthly payment amount.
    
    Args:
        amount: The payment amount
        
    Returns:
        Formatted currency string with 2 decimal places
    """
    return format_currency(amount, DECIMAL_PLACES_MONTHLY)


def format_total_amount(amount: float) -> str:
    """
    Format a total amount (no decimal places).
    
    Args:
        amount: The total amount
        
    Returns:
        Formatted currency string with no decimal places
    """
    return format_currency(amount, DECIMAL_PLACES_TOTAL)


def create_schedule_dataframe(schedule: PaymentSchedule) -> pd.DataFrame:
    """
    Convert PaymentSchedule to pandas DataFrame.
    
    Args:
        schedule: PaymentSchedule object
        
    Returns:
        DataFrame with payment schedule data
    """
    return pd.DataFrame(schedule.to_dict_list())


def aggregate_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate payment schedule by year, showing minimum remaining balance.
    
    Args:
        df: DataFrame with payment schedule
        
    Returns:
        DataFrame grouped by year with minimum remaining balance
    """
    if df.empty:
        return pd.DataFrame(columns=["Year", "Remaining Balance"])
    
    return df[["Year", "Remaining Balance"]].groupby("Year").min()


def validate_inputs(
    home_value: float,
    deposit: float,
    interest_rate: float,
    loan_term: int,
) -> Optional[str]:
    """
    Validate mortgage input values.
    
    Args:
        home_value: The home value
        deposit: The deposit amount
        interest_rate: Annual interest rate percentage
        loan_term: Loan term in years
        
    Returns:
        Error message if validation fails, None otherwise
    """
    if home_value <= 0:
        return "Home value must be greater than zero."
    
    if deposit < 0:
        return "Deposit cannot be negative."
    
    if deposit >= home_value:
        return "Deposit must be less than home value."
    
    if interest_rate < 0:
        return "Interest rate cannot be negative."
    
    if loan_term < 1:
        return "Loan term must be at least 1 year."
    
    if loan_term > 50:
        return "Loan term cannot exceed 50 years."
    
    return None


def calculate_loan_to_value_ratio(home_value: float, deposit: float) -> float:
    """
    Calculate the loan-to-value (LTV) ratio.
    
    Args:
        home_value: The home value
        deposit: The deposit amount
        
    Returns:
        LTV ratio as a percentage
    """
    if home_value <= 0:
        return 0.0
    
    loan_amount = home_value - deposit
    return (loan_amount / home_value) * 100
