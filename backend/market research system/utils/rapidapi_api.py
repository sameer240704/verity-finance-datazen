import os
import requests
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
        
    def get_current_price(self, stock_symbol):
        """
        Retrieves the current price of a stock using RapidAPI's Yahoo Finance endpoint.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            The current price of the stock, or None if an error occurs.
        """
        url = f"{self.base_url}get-price"
        querystring = {"symbol": stock_symbol, "region": "US"}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            # Extract the current price from the response (you may need to adjust the path)
            current_price = data.get("price", {}).get("regularMarketPrice", {}).get("raw")
            return current_price
        except requests.exceptions.RequestException as e:
            print(f"Error getting current price for {stock_symbol} from RapidAPI: {e}")
            return None

    def get_performance(self, stock_symbol, period="30d"):
        """
        Retrieves the performance (percentage change) of a stock over a given period using RapidAPI.

        Args:
            stock_symbol: The stock symbol.
            period: The time period (not directly supported by RapidAPI, so we'll use a workaround).

        Returns:
            The performance of the stock over the last 30 days, or None if an error occurs.
        """
        url = f"{self.base_url}get-historical-data"
        querystring = {"symbol": stock_symbol, "region": "US"}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            # Extract historical prices (you may need to adjust the path)
            prices = data.get("prices")
            if prices and len(prices) >= 30:
                # Get the closing price 30 days ago and the most recent closing price
                end_price = prices[0].get("close")
                start_price = prices[29].get("close")  # Assuming 30 trading days

                if start_price and end_price:
                    performance = ((end_price - start_price) / start_price) * 100
                    return f"{performance:.2f}%"
                else:
                    return None
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error getting performance data for {stock_symbol} from RapidAPI: {e}")
            return None