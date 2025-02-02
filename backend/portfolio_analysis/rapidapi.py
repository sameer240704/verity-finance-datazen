import json
import os
from gemini_model import GeminiModel
import requests
from tavily import TavilyClient
from dotenv import load_dotenv

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
    with open(file_path, 'r') as file:
        return json.load(file)

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

    # Save the structured report
    with open('portfolio_report.json', 'w') as json_file:
        json.dump(portfolio_report, json_file, indent=4)

    return portfolio_report

# Function to generate textual report using Gemini
def generate_textual_report(portfolio_data, gemini_model):
    # Construct the prompt for Gemini
    prompt = "Generate a comprehensive portfolio report based on the following data:\n\n"

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

    # Save the textual report
    with open('portfolio_report.txt', 'w') as txt_file:
        txt_file.write(response)

# Main function
def main():
    # Read stocks and bonds data (correct file paths)
    stocks = read_json_file('backend/data/stocks.json')
    bonds = read_json_file('backend/data/bonds.json')

    # Initialize Tavily API
    tavily_api = TavilyAPI()

    # Generate portfolio report with financial data and articles
    portfolio_report_data = generate_portfolio_report(stocks, bonds, tavily_api)

    # Initialize Gemini Model
    gemini_model = GeminiModel()

    # Generate textual report using Gemini
    generate_textual_report(portfolio_report_data, gemini_model)

if __name__ == "__main__":
    main()