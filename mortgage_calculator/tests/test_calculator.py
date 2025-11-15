"""
Unit tests for Mortgage Calculator.

This module contains comprehensive tests for all calculator functions
and data models.
"""

import pytest
import math
from mortgage_calculator.models import (
    MortgageInputs,
    MortgageResults,
    PaymentScheduleEntry,
    PaymentSchedule,
)
from mortgage_calculator.calculations import MortgageCalculator
from mortgage_calculator.utils import (
    format_currency,
    validate_inputs,
    calculate_loan_to_value_ratio,
)


class TestMortgageInputs:
    """Tests for MortgageInputs data class."""
    
    def test_valid_inputs(self):
        """Test creation with valid inputs."""
        inputs = MortgageInputs(
            home_value=500000,
            deposit=100000,
            interest_rate=5.5,
            loan_term_years=30,
        )
        assert inputs.home_value == 500000
        assert inputs.deposit == 100000
        assert inputs.interest_rate == 5.5
        assert inputs.loan_term_years == 30
    
    def test_negative_home_value(self):
        """Test that negative home value raises ValueError."""
        with pytest.raises(ValueError, match="Home value must be non-negative"):
            MortgageInputs(
                home_value=-100000,
                deposit=50000,
                interest_rate=5.0,
                loan_term_years=30,
            )
    
    def test_negative_deposit(self):
        """Test that negative deposit raises ValueError."""
        with pytest.raises(ValueError, match="Deposit must be non-negative"):
            MortgageInputs(
                home_value=500000,
                deposit=-10000,
                interest_rate=5.0,
                loan_term_years=30,
            )
    
    def test_deposit_exceeds_home_value(self):
        """Test that deposit > home value raises ValueError."""
        with pytest.raises(ValueError, match="Deposit cannot exceed home value"):
            MortgageInputs(
                home_value=500000,
                deposit=600000,
                interest_rate=5.0,
                loan_term_years=30,
            )
    
    def test_negative_interest_rate(self):
        """Test that negative interest rate raises ValueError."""
        with pytest.raises(ValueError, match="Interest rate must be non-negative"):
            MortgageInputs(
                home_value=500000,
                deposit=100000,
                interest_rate=-1.0,
                loan_term_years=30,
            )
    
    def test_invalid_loan_term(self):
        """Test that loan term < 1 raises ValueError."""
        with pytest.raises(ValueError, match="Loan term must be at least 1 year"):
            MortgageInputs(
                home_value=500000,
                deposit=100000,
                interest_rate=5.0,
                loan_term_years=0,
            )


class TestMortgageCalculator:
    """Tests for MortgageCalculator class."""
    
    def test_basic_calculation(self):
        """Test basic mortgage calculation."""
        inputs = MortgageInputs(
            home_value=500000,
            deposit=100000,
            interest_rate=5.5,
            loan_term_years=30,
        )
        
        calculator = MortgageCalculator()
        results = calculator.calculate_mortgage(inputs)
        
        # Verify loan amount
        assert results.loan_amount == 400000
        
        # Verify monthly payment is positive
        assert results.monthly_payment > 0
        
        # Verify total payments > loan amount
        assert results.total_payments > results.loan_amount
        
        # Verify total interest is positive
        assert results.total_interest > 0
        
        # Verify number of payments
        assert results.number_of_payments == 360  # 30 years * 12 months
    
    def test_zero_interest_rate(self):
        """Test calculation with 0% interest rate."""
        inputs = MortgageInputs(
            home_value=300000,
            deposit=50000,
            interest_rate=0.0,
            loan_term_years=25,
        )
        
        calculator = MortgageCalculator()
        results = calculator.calculate_mortgage(inputs)
        
        # With 0% interest, monthly payment should be loan_amount / number_of_payments
        expected_monthly = 250000 / (25 * 12)
        assert math.isclose(results.monthly_payment, expected_monthly, rel_tol=1e-9)
        
        # Total interest should be 0
        assert math.isclose(results.total_interest, 0, abs_tol=0.01)
    
    def test_invalid_loan_amount(self):
        """Test that deposit >= home value raises ValueError."""
        inputs = MortgageInputs(
            home_value=200000,
            deposit=200000,
            interest_rate=5.0,
            loan_term_years=30,
        )
        
        calculator = MortgageCalculator()
        with pytest.raises(ValueError, match="Loan amount must be positive"):
            calculator.calculate_mortgage(inputs)
    
    def test_payment_schedule_length(self):
        """Test that payment schedule has correct number of entries."""
        inputs = MortgageInputs(
            home_value=400000,
            deposit=80000,
            interest_rate=4.0,
            loan_term_years=20,
        )
        
        calculator = MortgageCalculator()
        results = calculator.calculate_mortgage(inputs)
        schedule = calculator.generate_payment_schedule(inputs, results)
        
        # Should have 240 entries (20 years * 12 months)
        assert len(schedule.entries) == 240
    
    def test_payment_schedule_final_balance(self):
        """Test that final payment brings balance to zero."""
        inputs = MortgageInputs(
            home_value=300000,
            deposit=60000,
            interest_rate=3.5,
            loan_term_years=15,
        )
        
        calculator = MortgageCalculator()
        results = calculator.calculate_mortgage(inputs)
        schedule = calculator.generate_payment_schedule(inputs, results)
        
        # Final balance should be approximately zero
        final_entry = schedule.entries[-1]
        assert final_entry.remaining_balance < 1.0  # Less than $1
    
    def test_payment_schedule_decreasing_balance(self):
        """Test that remaining balance decreases with each payment."""
        inputs = MortgageInputs(
            home_value=500000,
            deposit=100000,
            interest_rate=5.0,
            loan_term_years=30,
        )
        
        calculator = MortgageCalculator()
        results = calculator.calculate_mortgage(inputs)
        schedule = calculator.generate_payment_schedule(inputs, results)
        
        # Check that balance decreases
        for i in range(len(schedule.entries) - 1):
            current_balance = schedule.entries[i].remaining_balance
            next_balance = schedule.entries[i + 1].remaining_balance
            assert current_balance >= next_balance


class TestUtilityFunctions:
    """Tests for utility functions."""
    
    def test_format_currency_default(self):
        """Test default currency formatting."""
        result = format_currency(1234.56)
        assert result == "$1,235"  # Default 0 decimal places
    
    def test_format_currency_two_decimals(self):
        """Test currency formatting with 2 decimal places."""
        result = format_currency(1234.56, decimal_places=2)
        assert result == "$1,234.56"
    
    def test_validate_inputs_valid(self):
        """Test validation with valid inputs."""
        error = validate_inputs(500000, 100000, 5.5, 30)
        assert error is None
    
    def test_validate_inputs_zero_home_value(self):
        """Test validation with zero home value."""
        error = validate_inputs(0, 50000, 5.0, 30)
        assert error is not None
        assert "Home value must be greater than zero" in error
    
    def test_validate_inputs_negative_deposit(self):
        """Test validation with negative deposit."""
        error = validate_inputs(500000, -10000, 5.0, 30)
        assert error is not None
        assert "Deposit cannot be negative" in error
    
    def test_validate_inputs_deposit_equals_home_value(self):
        """Test validation when deposit equals home value."""
        error = validate_inputs(300000, 300000, 5.0, 30)
        assert error is not None
        assert "Deposit must be less than home value" in error
    
    def test_calculate_ltv_ratio(self):
        """Test LTV ratio calculation."""
        ltv = calculate_loan_to_value_ratio(500000, 100000)
        assert math.isclose(ltv, 80.0, rel_tol=1e-9)
    
    def test_calculate_ltv_ratio_zero_home_value(self):
        """Test LTV ratio with zero home value."""
        ltv = calculate_loan_to_value_ratio(0, 0)
        assert ltv == 0.0


class TestPaymentSchedule:
    """Tests for PaymentSchedule data class."""
    
    def test_to_dict_list(self):
        """Test conversion to dictionary list."""
        entries = [
            PaymentScheduleEntry(
                month=1,
                payment=2000.0,
                principal=500.0,
                interest=1500.0,
                remaining_balance=199500.0,
                year=1,
            )
        ]
        schedule = PaymentSchedule(entries=entries)
        dict_list = schedule.to_dict_list()
        
        assert len(dict_list) == 1
        assert dict_list[0]["Month"] == 1
        assert dict_list[0]["Payment"] == 2000.0
        assert dict_list[0]["Principal"] == 500.0
        assert dict_list[0]["Interest"] == 1500.0
        assert dict_list[0]["Remaining Balance"] == 199500.0
        assert dict_list[0]["Year"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
