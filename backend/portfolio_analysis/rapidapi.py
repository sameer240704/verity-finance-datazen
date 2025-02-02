import json
import os
from gemini_model import GeminiModel
import requests
from tavily import TavilyClient
from dotenv import load_dotenv
import re

load_dotenv()

class TavilyAPI:
    def __init__(self):
        self.client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    def search(self, query):
        """
        Searches using the Tavily API.

        Args:
            query: The search query.

        Returns:
            The search results.
        """
        search_response = self.client.search(query=query, max_results=1)
        return search_response

# Function to fetch financial data from the API
def fetch_financial_data(symbol):
    url = "https://real-time-finance-data.p.rapidapi.com/company-income-statement"
    headers = {
        "x-rapidapi-key": os.environ["RAPIDAPI_API_KEY"],
        "x-rapidapi-host": "real-time-finance-data.p.rapidapi.com"
    }

    # First attempt
    querystring = {"symbol": symbol, "period": "QUARTERLY", "language": "en"}
    response = requests.get(url, headers=headers, params=querystring)

    # Handle 403 error (Forbidden)
    if response.status_code == 403:
        print(f"Attempting workaround for symbol: {symbol}")
        querystring["symbol"] = f"{symbol}:NASDAQ"  # Try appending :NASDAQ
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            print(f"Workaround successful for {symbol}:NASDAQ")
            return response.json()
        else:
            print(f"Workaround failed for {symbol}:NASDAQ. Status code: {response.status_code}")
            return None

    # Check if the request was successful
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
        return None

# Function to read data from JSON files
def read_json_file(file_path):
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")
    with open(abs_path, 'r') as file:
        return json.load(file)
    
def read_txt_file(file_path):
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found: {abs_path}")
    with open(abs_path, 'r') as file:
        return file.read()

# Function to generate a structured report for the entire portfolio
def generate_portfolio_report(stocks, bonds, tavily_api):
    portfolio_report = {
        "stocks": {},
        "bonds": bonds,
        "articles": {}
    }

    # Fetch financial data and articles for each stock
    for stock in stocks:
        if 'tickerSymbol' in stock:
            symbol = stock['tickerSymbol']
            json_response = fetch_financial_data(symbol)
            if json_response and json_response.get("status") == "OK":
                portfolio_report["stocks"][symbol] = {
                    "company_info": json_response['data'],
                    "stock_data": stock
                }

            article = tavily_api.search(stock['stockName'])
            portfolio_report["articles"][stock['stockName']] = article.get("results", [])
        else:
            print(f"Warning: 'tickerSymbol' key not found in stock: {stock}")

    # Fetch articles for each bond
    for bond in bonds:
        if 'bondType' in bond:
            article = tavily_api.search(bond['bondType'])
            portfolio_report["articles"][bond['bondType']] = article.get("results", [])
        else:
            print(f"Warning: 'bondType' key not found in bond: {bond}")

    # Save the structured report in the current directory
    report_dir = os.path.dirname(__file__)
    with open(os.path.join(report_dir, 'portfolio_report.json'), 'w') as json_file:
        json.dump(portfolio_report, json_file, indent=4)

    return portfolio_report

# Function to generate textual report using Gemini
def generate_textual_report(portfolio_data, gemini_model):
    # Construct the prompt for Gemini
    prompt = "Generate a comprehensive portfolio report and market analysis based on the following data:\n\n"

    # Add stock information to the prompt
    prompt += "Stocks:\n"
    for symbol, data in portfolio_data["stocks"].items():
        prompt += f"  {symbol}:\n"
        prompt += f"    Company Info: {json.dumps(data['company_info'])}\n"
        prompt += f"    Stock Data: {json.dumps(data['stock_data'])}\n"
        if symbol in portfolio_data["articles"]:
            prompt += f"    Recent Article: {json.dumps(portfolio_data['articles'][symbol])}\n"

    # Add bond information to the prompt
    prompt += "\nBonds:\n"
    for bond in portfolio_data["bonds"]:
        prompt += f"  {bond['bondType']}: {json.dumps(bond)}\n"
        if bond['bondType'] in portfolio_data["articles"]:
            prompt += f"    Recent Article: {json.dumps(portfolio_data['articles'][bond['bondType']])}\n"

    # Get response from Gemini
    response = gemini_model.get_response(prompt)

    # Save the textual report in the current directory
    report_dir = os.path.dirname(__file__)
    with open(os.path.join(report_dir, 'portfolio_report.txt'), 'w') as txt_file:
        txt_file.write(response)


# ====== Data to return to user =======

def extract_text_report_data(text):
    summary_match = re.search(r'I\. Executive Summary\s*(.*?)\s*II\.', text, re.DOTALL)
    recommendations_match = re.search(r'Recommendations\s*(.*?)\s*Conclusion', text, re.DOTALL)
    conclusion_match = re.search(r'Conclusion\s*(.*)', text, re.DOTALL)
    
    summary = summary_match.group(1).strip() if summary_match else "Summary not found"
    recommendations = recommendations_match.group(1).strip() if recommendations_match else "Recommendations not found"
    conclusion = conclusion_match.group(1).strip() if conclusion_match else "Conclusion not found"

    return {
        "summary": summary,
        "recommendations": recommendations,
        "conclusion": conclusion
    }

def generate_json_report_data(json_data):
    """
    Extracts the stocks and bonds sections from the JSON data.

    Args:
        json_data (dict): The loaded JSON data.

    Returns:
        dict: A dictionary containing only the stocks and bonds data.
    """
    return {
      "stocks": json_data.get("stocks", {}),
      "bonds": json_data.get("bonds", [])
    }

# Main function
def main():
    # Read stocks and bonds data (correct file paths)
    stocks = read_json_file('../data/stocks.json')
    bonds = read_json_file('../data/bonds.json')

    # Initialize Tavily API
    tavily_api = TavilyAPI()

    # Generate portfolio report with financial data and articles
    portfolio_report_data = generate_portfolio_report(stocks, bonds, tavily_api)

    # Initialize Gemini Model
    gemini_model = GeminiModel()

    # Generate textual report using Gemini
    generate_textual_report(portfolio_report_data, gemini_model)

    text_report = read_txt_file('./portfolio_report.txt')
    json_report = read_json_file('./portfolio_report.json')
    text_data = extract_text_report_data(text_report)
    portfolio_report_data = generate_json_report_data(json_report)

    final_data = {
        "text_data": text_data,
        "json_data": portfolio_report_data
    }

    print(json.dumps(final_data, indent=4))