"""
Mortgage calculation engine.

This module contains the core business logic for calculating mortgage
payments, interest, and payment schedules.
"""

import math
from typing import List

from .config import MONTHS_PER_YEAR, PERCENTAGE_DIVISOR
from .models import (
    MortgageInputs,
    MortgageResults,
    PaymentSchedule,
    PaymentScheduleEntry,
)


class MortgageCalculator:
    """
    Calculator for mortgage-related computations.
    
    This class provides methods to calculate monthly payments, total interest,
    and generate payment schedules for a given mortgage.
    """
    
    @staticmethod
    def calculate_mortgage(inputs: MortgageInputs) -> MortgageResults:
        """
        Calculate mortgage payment details.
        
        Args:
            inputs: MortgageInputs object containing loan parameters
            
        Returns:
            MortgageResults object containing calculated values
            
        Raises:
            ValueError: If loan amount is zero or negative
            ZeroDivisionError: If calculation results in division by zero
        """
        loan_amount = inputs.home_value - inputs.deposit
        
        if loan_amount <= 0:
            raise ValueError(
                "Loan amount must be positive. "
                "Ensure home value is greater than deposit."
            )
        
        # Convert annual interest rate to monthly decimal rate
        monthly_interest_rate = (
            inputs.interest_rate / PERCENTAGE_DIVISOR
        ) / MONTHS_PER_YEAR
        
        number_of_payments = inputs.loan_term_years * MONTHS_PER_YEAR
        
        # Calculate monthly payment using standard mortgage formula
        # M = P * [r(1+r)^n] / [(1+r)^n - 1]
        # where M = monthly payment, P = principal, r = monthly rate, n = number of payments
        try:
            if monthly_interest_rate == 0:
                # Special case: 0% interest rate
                monthly_payment = loan_amount / number_of_payments
            else:
                power_term = (1 + monthly_interest_rate) ** number_of_payments
                monthly_payment = (
                    loan_amount
                    * (monthly_interest_rate * power_term)
                    / (power_term - 1)
                )
        except ZeroDivisionError as e:
            raise ZeroDivisionError(
                "Error in payment calculation. Check input values."
            ) from e
        
        total_payments = monthly_payment * number_of_payments
        total_interest = total_payments - loan_amount
        
        return MortgageResults(
            loan_amount=loan_amount,
            monthly_payment=monthly_payment,
            total_payments=total_payments,
            total_interest=total_interest,
            monthly_interest_rate=monthly_interest_rate,
            number_of_payments=number_of_payments,
        )
    
    @staticmethod
    def generate_payment_schedule(
        inputs: MortgageInputs,
        results: MortgageResults,
    ) -> PaymentSchedule:
        """
        Generate a detailed payment schedule for the mortgage.
        
        Args:
            inputs: MortgageInputs object containing loan parameters
            results: MortgageResults object from calculate_mortgage
            
        Returns:
            PaymentSchedule object containing all payment entries
        """
        entries: List[PaymentScheduleEntry] = []
        remaining_balance = results.loan_amount
        
        for month in range(1, results.number_of_payments + 1):
            # Calculate interest for current month
            interest_payment = remaining_balance * results.monthly_interest_rate
            
            # Calculate principal payment (remainder after interest)
            principal_payment = results.monthly_payment - interest_payment
            
            # Update remaining balance
            remaining_balance -= principal_payment
            
            # Prevent negative balance due to floating point precision
            if remaining_balance < 0.01:
                remaining_balance = 0
            
            # Calculate which year of the loan this payment is in
            year = math.ceil(month / MONTHS_PER_YEAR)
            
            entries.append(
                PaymentScheduleEntry(
                    month=month,
                    payment=results.monthly_payment,
                    principal=principal_payment,
                    interest=interest_payment,
                    remaining_balance=remaining_balance,
                    year=year,
                )
            )
        
        return PaymentSchedule(entries=entries)
    
    @classmethod
    def calculate_all(cls, inputs: MortgageInputs) -> tuple[MortgageResults, PaymentSchedule]:
        """
        Convenience method to calculate both results and schedule.
        
        Args:
            inputs: MortgageInputs object containing loan parameters
            
        Returns:
            Tuple of (MortgageResults, PaymentSchedule)
        """
        results = cls.calculate_mortgage(inputs)
        schedule = cls.generate_payment_schedule(inputs, results)
        return results, schedule
