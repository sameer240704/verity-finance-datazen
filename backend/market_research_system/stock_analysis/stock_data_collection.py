from utils.tavily_api import TavilyAPI
# from utils.faiss_index import FAISSIndex
from utils.yfinance_api import YFinanceAPI
from utils.rapidapi_api import RapidAPI
from models.gemini_model import GeminiModel
# from utils.faiss_index import FAISSIndex
from models.gemini_model import GeminiModel
import json
import ast
import json
from typing import Dict
from utils.data_processing import clean_response_string 
import pandas as pd

class StockDataCollectionAgent:
    def __init__(self, gemini_model, stock_name, brief_aim, data_validation_agent):
        self.gemini_model = gemini_model
        self.stock_name = stock_name
        self.brief_aim = brief_aim
        self.tavily_api = TavilyAPI()
        # self.faiss_index = FAISSIndex()
        self.yfinance_api = YFinanceAPI()
        self.rapidapi_api = RapidAPI()
        self.data_validation_agent = data_validation_agent
        self.prompt_template = """
        You are a Stock Data Collection Agent.
        Your goal is to gather news, articles, reports, historical stock chart data, and key financial data related to '{stock_name}'.
        Aim: {brief_aim}

        Tasks:
        1. Use the Tavily Search API to find recent information about '{stock_name}'.
           - Search query: "News and reports on {stock_name}"
        2. Retrieve the historical stock chart data for '{stock_name}' using YFinance.
        3. Extract key financial data (revenue, earnings, etc.) and company information for '{stock_name}' using YFinance or RapidAPI. You can use function calling if necessary.

        Provide your response as a detailed paragraph or a bulleted list. DO NOT FORMAT THE RESPONSE AS JSON.
        """

    def run(self):
        prompt = self.prompt_template.format(stock_name=self.stock_name, brief_aim=self.brief_aim)

        tavily_query = f"News and reports on {self.stock_name}"
        tavily_results = self.tavily_api.search(tavily_query)

        stock_chart_data = self.yfinance_api.get_stock_chart(self.stock_name)
        if stock_chart_data is None:
            print(f"Warning: Could not retrieve stock chart data for {self.stock_name}")
            stock_chart_data = ""  # or some default value

        company_details = self.yfinance_api.get_company_info(self.stock_name)
        if company_details is None or (isinstance(company_details, pd.DataFrame) and company_details.empty):
            company_details = self.rapidapi_api.get_company_info(self.stock_name)
            if company_details is None or (isinstance(company_details, pd.DataFrame) and company_details.empty):
                print(f"Warning: Could not retrieve company details for {self.stock_name}")
                company_details = {}  # or some default value

        financial_data = self.yfinance_api.get_financial_data(self.stock_name)
        if financial_data is None or (isinstance(financial_data, pd.DataFrame) and financial_data.empty):
            financial_data = self.rapidapi_api.get_financial_data(self.stock_name)
            if financial_data is None or (isinstance(financial_data, pd.DataFrame) and financial_data.empty):
                print(f"Warning: Could not retrieve financial data for {self.stock_name}")
                financial_data = {}  # or some default value
                
        # Combine and process data using Gemini
        combined_data = {
            "prompt": prompt,
            "tavily_results": tavily_results,
            "stock_chart_data": stock_chart_data,
            "company_details": company_details,
            "financial_data": financial_data
        }
        combined_data_str = str(combined_data)

        gemini_response = self.gemini_model.get_response(combined_data_str)
        print("Raw Gemini Response (Stock):", gemini_response)

        return gemini_response