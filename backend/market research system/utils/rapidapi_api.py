import os
import requests

class RapidAPI:
    def __init__(self):
        self.api_key = os.environ.get("RAPIDAPI_API_KEY")
        self.base_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    def get_company_info(self, stock_symbol):
        """
        Retrieves company information using RapidAPI's Yahoo Finance endpoint.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            A dictionary containing company information, or an empty dictionary if an error occurs.
        """
        url = f"{self.base_url}get-profile"
        querystring = {"symbol": stock_symbol, "region": "US"}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting company info for {stock_symbol} from RapidAPI: {e}")
            return {}

    def get_financial_data(self, stock_symbol):
        """
        Retrieves financial data using RapidAPI's Yahoo Finance endpoint.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            A dictionary containing financial data, or an empty dictionary if an error occurs.
        """
        url = f"{self.base_url}get-financials"
        querystring = {"symbol": stock_symbol, "region": "US"}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting financial data for {stock_symbol} from RapidAPI: {e}")
            return {}