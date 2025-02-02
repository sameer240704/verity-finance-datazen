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

    def search(self, query, max_results=5):  # Increase max_results if needed
        """
        Searches using the Tavily API.

        Args:
            query: The search query.
            max_results: The maximum number of results to return.

        Returns:
            The search results.
        """
        search_response = self.client.search(query=query, max_results=max_results)
        return search_response
    
# Function to get recommended stocks from the internet using Tavily
def get_recommended_stocks_from_internet(tavily_api, num_stocks=2):
    """
    Fetches recommended stocks from the internet using Tavily.

    Args:
        tavily_api (TavilyAPI): The Tavily API client.
        num_stocks (int): The number of recommended stocks to fetch.

    Returns:
        list: A list of recommended stocks with their associated articles.
    """
    recommended_stocks = []
    search_results = tavily_api.search("What are the best stocks to buy now?", max_results=5)
    articles = search_results.get("results", [])

    # Extract stock recommendations from articles (basic extraction)
    # You can make this more sophisticated based on article content
    extracted_stocks = set()  # Use a set to avoid duplicate stock mentions
    for article in articles:
        # Basic keyword-based extraction (very basic example)
        content = article['content'].upper() # Convert to uppercase for case-insensitive matching
        if "BUY" in content or "STRONG BUY" in content or "OUTPERFORM" in content:
            # Extract potential stock symbols (this is a very rudimentary example)
            # You'll need a more robust method to accurately extract symbols
            for word in content.split():
                if word.isupper() and 2 <= len(word) <= 5 and word not in extracted_stocks:
                    extracted_stocks.add(word)

    for stock_symbol in extracted_stocks:
      if len(recommended_stocks) >= num_stocks:
          break  # Stop when we have enough recommendations
      recommended_stocks.append({
          "stock": {"tickerSymbol": stock_symbol},  # Store only the ticker symbol
          "articles": articles  # You can refine which articles are associated
      })

    return recommended_stocks

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
        "articles": {},
        "recommended_stocks": []
    }

    # Fetch financial data and articles for each stock in portfolio
    for stock in stocks:
        if 'tickerSymbol' in stock:
            symbol = stock['tickerSymbol']
            json_response = fetch_financial_data(symbol)
            if json_response and json_response.get("status") == "OK":
                portfolio_report["stocks"][symbol] = {
                    "company_info": json_response['data'],
                    "stock_data": stock
                }

            article = tavily_api.search(f"news about {stock['stockName']} stock", max_results=5)
            portfolio_report["articles"][stock['stockName']] = article.get("results", [])
        else:
            print(f"Warning: 'tickerSymbol' key not found in stock: {stock}")

    # Fetch articles for each bond
    for bond in bonds:
        if 'bondType' in bond:
            article = tavily_api.search(f"news about {bond['bondType']} bond", max_results=5)
            portfolio_report["articles"][bond['bondType']] = article.get("results", [])
        else:
            print(f"Warning: 'bondType' key not found in bond: {bond}")

    # Get recommended stocks from the internet
    recommended_stocks = get_recommended_stocks_from_internet(tavily_api)
    portfolio_report["recommended_stocks"] = recommended_stocks

    # Save the structured report in the current directory
    report_dir = os.path.dirname(__file__)
    with open(os.path.join(report_dir, 'portfolio_report.json'), 'w') as json_file:
        json.dump(portfolio_report, json_file, indent=4)

    return portfolio_report
# Function to generate textual report using Gemini
def generate_textual_report(portfolio_data, gemini_model):
    # Construct the prompt for Gemini
    prompt = "Generate a comprehensive portfolio report and market analysis based on the following data, The analysis must have 3 headings, that is, 'Portfolio Summary', 'Recommended Stocks', and 'Conclusion':\n\n"

    # Add Portfolio Summary heading
    prompt += "*Portfolio Summary*\n\n"

    # Add stock information to the prompt
    prompt += "Stocks:\n"
    for symbol, data in portfolio_data["stocks"].items():
        prompt += f"  {symbol}:\n"
        prompt += f"    Company Info: {json.dumps(data['company_info'])}\n"
        prompt += f"    Stock Data: {json.dumps(data['stock_data'])}\n"
        if symbol in portfolio_data["articles"]:
            prompt += f"    Recent Articles:\n"
            for article in portfolio_data['articles'][symbol]:
                prompt += f"      - {article['url']}\n"

    # Add bond information to the prompt
    prompt += "\nBonds:\n"
    for bond in portfolio_data["bonds"]:
        prompt += f"  {bond['bondType']}: {json.dumps(bond)}\n"
        if bond['bondType'] in portfolio_data["articles"]:
            prompt += f"    Recent Articles:\n"
            for article in portfolio_data['articles'][bond['bondType']]:
                prompt += f"      - {article['url']}\n"

    # Add Recommended Stocks section
    prompt += "\n*Recommended Stocks*\n\n"
    for recommended_stock in portfolio_data["recommended_stocks"]:
        prompt += f"  Stock: {recommended_stock['stock']['tickerSymbol']}\n" # Only include ticker symbol
        prompt += f"  Articles:\n"
        for article in recommended_stock['articles']:
            prompt += f"    - {article['url']}\n"

    # Add Conclusion heading
    prompt += "\n*Conclusion*\n\n"
    # Get response from Gemini
    response = gemini_model.get_response(prompt)

    # Save the textual report in the current directory
    report_dir = os.path.dirname(__file__)
    with open(os.path.join(report_dir, 'portfolio_report.txt'), 'w') as txt_file:
        txt_file.write(response)


# ====== Data to return to user =======

def extract_text_report_data(text):
    """
    Extracts Portfolio Summary, Recommended Stocks, and Conclusion from the text report,
    handling both ** and ### markers before the section titles.

    Args:
        text (str): The content of the text report.

    Returns:
        dict: A dictionary containing the extracted sections.
    """
    summary_match = re.search(r'(?:\*\*|###)\s*Portfolio Summary\s*(.*?)(?:\*\*|###)\s*Recommended Stocks', text, re.DOTALL)
    recommendations_match = re.search(r'(?:\*\*|###)\s*Recommended Stocks\s*(.*?)(?:\*\*|###)\s*Conclusion', text, re.DOTALL)
    conclusion_match = re.search(r'(?:\*\*|###)\s*Conclusion\s*(.*)', text, re.DOTALL)

    summary = summary_match.group(1).strip() if summary_match else "Portfolio Summary not available right now. Please contact the development cell."
    recommendations = recommendations_match.group(1).strip() if recommendations_match else "Recommendations not available right now. Please contact the development cell."
    conclusion = conclusion_match.group(1).strip() if conclusion_match else "Conclusion not available right now. Please contact the development cell."

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

    return final_data