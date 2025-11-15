"""
Main application entry point for Mortgage Calculator.

This module serves as the entry point for the Streamlit application,
orchestrating the UI components and business logic.
"""

import streamlit as st
import logging
from typing import Optional

from mortgage_calculator.calculations import MortgageCalculator
from mortgage_calculator.models import MortgageInputs
from mortgage_calculator.ui_components import MortgageUI
from mortgage_calculator.utils import validate_inputs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main application function.
    
    This function orchestrates the entire application flow:
    1. Renders the UI
    2. Collects user inputs
    3. Validates inputs
    4. Performs calculations
    5. Displays results
    """
    # Set page configuration
    st.set_page_config(
        page_title="Mortgage Calculator",
        page_icon="🏠",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    # Initialize UI
    ui = MortgageUI()
    
    # Render title
    ui.render_title()
    
    try:
        # Collect user inputs
        inputs = ui.render_input_section()
        
        # Validate inputs
        validation_error = validate_inputs(
            inputs.home_value,
            inputs.deposit,
            inputs.interest_rate,
            inputs.loan_term_years,
        )
        
        if validation_error:
            ui.show_error(validation_error)
            logger.warning(f"Validation error: {validation_error}")
            return
        
        # Perform calculations
        logger.info(f"Calculating mortgage for inputs: {inputs}")
        calculator = MortgageCalculator()
        results, schedule = calculator.calculate_all(inputs)
        
        # Display results
        ui.render_summary_metrics(results)
        ui.render_additional_info(inputs, results)
        ui.render_payment_schedule(schedule)
        
        logger.info("Calculations completed successfully")
        
    except ValueError as e:
        error_message = f"Invalid input: {str(e)}"
        ui.show_error(error_message)
        logger.error(error_message, exc_info=True)
        
    except ZeroDivisionError as e:
        error_message = "Calculation error: Division by zero occurred"
        ui.show_error(error_message)
        logger.error(error_message, exc_info=True)
        
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        ui.show_error(error_message)
        logger.error(error_message, exc_info=True)
        
        # In production, you might want to send this to a monitoring service
        if st.checkbox("Show detailed error information (debug mode)"):
            st.exception(e)


if __name__ == "__main__":
    main()
