"""
Data models for Mortgage Calculator.

This module defines the data structures used throughout the application
using dataclasses for type safety and immutability.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MortgageInputs:
    """
    Immutable data class representing mortgage input parameters.
    
    Attributes:
        home_value: The total value of the home
        deposit: The initial deposit amount
        interest_rate: Annual interest rate as a percentage
        loan_term_years: The loan term in years
    """
    home_value: float
    deposit: float
    interest_rate: float
    loan_term_years: int
    
    def __post_init__(self) -> None:
        """Validate inputs after initialization."""
        if self.home_value < 0:
            raise ValueError("Home value must be non-negative")
        if self.deposit < 0:
            raise ValueError("Deposit must be non-negative")
        if self.deposit > self.home_value:
            raise ValueError("Deposit cannot exceed home value")
        if self.interest_rate < 0:
            raise ValueError("Interest rate must be non-negative")
        if self.loan_term_years < 1:
            raise ValueError("Loan term must be at least 1 year")


@dataclass(frozen=True)
class MortgageResults:
    """
    Immutable data class representing calculated mortgage results.
    
    Attributes:
        loan_amount: The principal loan amount
        monthly_payment: The monthly payment amount
        total_payments: Total amount paid over the loan term
        total_interest: Total interest paid over the loan term
        monthly_interest_rate: Monthly interest rate (as decimal)
        number_of_payments: Total number of monthly payments
    """
    loan_amount: float
    monthly_payment: float
    total_payments: float
    total_interest: float
    monthly_interest_rate: float
    number_of_payments: int


@dataclass(frozen=True)
class PaymentScheduleEntry:
    """
    Immutable data class representing a single payment in the schedule.
    
    Attributes:
        month: Payment month number (1-indexed)
        payment: Total payment amount for the month
        principal: Principal portion of the payment
        interest: Interest portion of the payment
        remaining_balance: Remaining loan balance after payment
        year: Year of the loan (1-indexed)
    """
    month: int
    payment: float
    principal: float
    interest: float
    remaining_balance: float
    year: int


@dataclass
class PaymentSchedule:
    """
    Data class representing the complete payment schedule.
    
    Attributes:
        entries: List of payment schedule entries
    """
    entries: List[PaymentScheduleEntry]
    
    def to_dict_list(self) -> List[dict]:
        """
        Convert payment schedule to a list of dictionaries.
        
        Returns:
            List of dictionaries suitable for DataFrame creation
        """
        return [
            {
                "Month": entry.month,
                "Payment": entry.payment,
                "Principal": entry.principal,
                "Interest": entry.interest,
                "Remaining Balance": entry.remaining_balance,
                "Year": entry.year,
            }
            for entry in self.entries
        ]
