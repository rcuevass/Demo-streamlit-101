"""
Streamlit UI components for Mortgage Calculator.

This module contains all Streamlit-specific UI code, separated from
business logic for better testability and maintainability.
"""

import streamlit as st
import pandas as pd
from typing import Tuple

from .config import (
    APP_TITLE,
    DEFAULT_HOME_VALUE,
    DEFAULT_DEPOSIT,
    DEFAULT_INTEREST_RATE,
    DEFAULT_LOAN_TERM_YEARS,
    MIN_HOME_VALUE,
    MIN_DEPOSIT,
    MIN_INTEREST_RATE,
    MIN_LOAN_TERM,
)
from .models import MortgageInputs, MortgageResults, PaymentSchedule
from .utils import (
    format_monthly_payment,
    format_total_amount,
    create_schedule_dataframe,
    aggregate_by_year,
    calculate_loan_to_value_ratio,
)


class MortgageUI:
    """
    Streamlit UI components for mortgage calculator.
    
    This class encapsulates all Streamlit UI rendering logic,
    keeping it separate from business logic.
    """
    
    @staticmethod
    def render_title() -> None:
        """Render the application title."""
        st.title(APP_TITLE)
    
    @staticmethod
    def render_input_section() -> MortgageInputs:
        """
        Render the input section and collect user inputs.
        
        Returns:
            MortgageInputs object with user-provided values
        """
        st.write("### Input Data")
        col1, col2 = st.columns(2)
        
        with col1:
            home_value = st.number_input(
                "Home Value",
                min_value=MIN_HOME_VALUE,
                value=DEFAULT_HOME_VALUE,
                step=10000,
                help="Total value of the property",
            )
            
            deposit = st.number_input(
                "Deposit",
                min_value=MIN_DEPOSIT,
                value=DEFAULT_DEPOSIT,
                step=5000,
                help="Initial down payment amount",
            )
        
        with col2:
            interest_rate = st.number_input(
                "Interest Rate (in %)",
                min_value=MIN_INTEREST_RATE,
                value=DEFAULT_INTEREST_RATE,
                step=0.1,
                format="%.2f",
                help="Annual interest rate as a percentage",
            )
            
            loan_term = st.number_input(
                "Loan Term (in years)",
                min_value=MIN_LOAN_TERM,
                value=DEFAULT_LOAN_TERM_YEARS,
                step=1,
                help="Duration of the loan in years",
            )
        
        return MortgageInputs(
            home_value=float(home_value),
            deposit=float(deposit),
            interest_rate=float(interest_rate),
            loan_term_years=int(loan_term),
        )
    
    @staticmethod
    def render_summary_metrics(results: MortgageResults) -> None:
        """
        Render the summary metrics section.
        
        Args:
            results: MortgageResults object with calculated values
        """
        st.write("### Repayment Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Monthly Repayment",
                value=format_monthly_payment(results.monthly_payment),
            )
        
        with col2:
            st.metric(
                label="Total Repayments",
                value=format_total_amount(results.total_payments),
            )
        
        with col3:
            st.metric(
                label="Total Interest",
                value=format_total_amount(results.total_interest),
            )
    
    @staticmethod
    def render_additional_info(inputs: MortgageInputs, results: MortgageResults) -> None:
        """
        Render additional loan information.
        
        Args:
            inputs: MortgageInputs object
            results: MortgageResults object
        """
        with st.expander("📊 Additional Loan Information"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Loan Amount",
                    value=format_total_amount(results.loan_amount),
                )
                
                ltv_ratio = calculate_loan_to_value_ratio(
                    inputs.home_value,
                    inputs.deposit,
                )
                st.metric(
                    label="Loan-to-Value Ratio",
                    value=f"{ltv_ratio:.1f}%",
                )
            
            with col2:
                st.metric(
                    label="Number of Payments",
                    value=f"{results.number_of_payments}",
                )
                
                effective_rate = results.monthly_interest_rate * 100
                st.metric(
                    label="Monthly Interest Rate",
                    value=f"{effective_rate:.4f}%",
                )
    
    @staticmethod
    def render_payment_schedule(schedule: PaymentSchedule) -> None:
        """
        Render the payment schedule section with chart and table.
        
        Args:
            schedule: PaymentSchedule object
        """
        st.write("### Payment Schedule")
        
        # Create DataFrame from schedule
        df = create_schedule_dataframe(schedule)
        
        # Display line chart of remaining balance by year
        payments_df = aggregate_by_year(df)
        st.line_chart(
            payments_df,
            use_container_width=True,
        )
        
        # Display detailed schedule table in an expander
        with st.expander("📋 View Detailed Payment Schedule"):
            # Format currency columns for display
            display_df = df.copy()
            display_df["Payment"] = display_df["Payment"].apply(
                lambda x: format_monthly_payment(x)
            )
            display_df["Principal"] = display_df["Principal"].apply(
                lambda x: format_monthly_payment(x)
            )
            display_df["Interest"] = display_df["Interest"].apply(
                lambda x: format_monthly_payment(x)
            )
            display_df["Remaining Balance"] = display_df["Remaining Balance"].apply(
                lambda x: format_total_amount(x)
            )
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )
    
    @staticmethod
    def show_error(message: str) -> None:
        """
        Display an error message.
        
        Args:
            message: Error message to display
        """
        st.error(f"❌ {message}")
    
    @staticmethod
    def show_warning(message: str) -> None:
        """
        Display a warning message.
        
        Args:
            message: Warning message to display
        """
        st.warning(f"⚠️ {message}")
