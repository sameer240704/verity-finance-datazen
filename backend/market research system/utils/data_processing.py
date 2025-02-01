# Add any data processing utility functions here, e.g.,:
import re
import ast

def clean_response_string(response):
    """
    Cleans the response string to make it compatible with ast.literal_eval().

    Args:
        response: The raw response string from Gemini or the dictionary.

    Returns:
        A cleaned string that can be parsed by ast.literal_eval().
    """
    if isinstance(response, dict):
        return response

    if isinstance(response, str):
        # Remove any leading/trailing whitespace
        response_str = response.strip()

        # Replace single quotes with double quotes (JSON standard)
        response_str = response_str.replace("'", '"')

        # Remove any trailing commas before closing braces/brackets
        response_str = re.sub(r',\s*}', '}', response_str)
        response_str = re.sub(r',\s*]', ']', response_str)

        return response_str
    
    return response

def calculate_ratios(financial_data):
    """
    Calculates financial ratios from financial data.
    """
    # Implement your ratio calculation logic here
    pass