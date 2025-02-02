import os
import requests

class RapidAPI:
    def __init__(self):
        self.api_key = os.environ.get("RAPIDAPI_API_KEY")
        self.base_url = "https://real-time-finance-data.p.rapidapi.com/"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
        }

    def get_company_info(self, stock_symbol):
        """
        Retrieves company information using RapidAPI's Yahoo Finance endpoint.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            A dictionary containing company information, or an empty dictionary if an error occurs.
        """
        url = f"{self.base_url}company-profile"
        querystring = {"symbol": stock_symbol, "language": "en"}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting company info for {stock_symbol} from RapidAPI: {e}")
            return {}  # Return empty dictionary in case of an error

    def get_financial_data(self, stock_symbol):
        """
        Retrieves financial data using RapidAPI's Yahoo Finance endpoint.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            A dictionary containing financial data, or an empty dictionary if an error occurs.
        """
        url = f"{self.base_url}stock-statistics"
        querystring = {"symbol": stock_symbol, "language": "en"}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting financial data for {stock_symbol} from RapidAPI: {e}")
            return {}  # Return empty dictionary in case of an error
    
    def get_balance_sheet(self, symbol):
        """Fetches the company balance sheet data."""
        url = f"{self.base_url}company-balance-sheet"
        return self._fetch_data(url, symbol)

    def get_income_statement(self, symbol):
        """Fetches the company income statement data."""
        url = f"{self.base_url}company-income-statement"
        return self._fetch_data(url, symbol)

    def get_cash_flow(self, symbol):
        """Fetches the company cash flow data."""
        url = f"{self.base_url}company-cash-flow"
        return self._fetch_data(url, symbol)

    def get_stock_news(self, symbol):
        """Fetches the latest news for a given stock."""
        url = f"{self.base_url}stock-news"
        querystring = {"symbol": symbol, "language": "en"}
        response = requests.get(url, headers=self.headers, params=querystring)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch news for {symbol}. Status code: {response.status_code}")
            return None
        
    def get_current_price(self, stock_symbol):
        """
        Retrieves the current price of a stock using RapidAPI's Yahoo Finance endpoint.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            The current price of the stock, or None if an error occurs.
        """
        url = f"{self.base_url}quote"
        querystring = {"symbol": stock_symbol, "language": "en"}
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
        url = f"{self.base_url}historical-chart"
        querystring = {"symbol": stock_symbol,"period":"1M","interval":"1d","range":"30d", "language": "en"}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            data = response.json()
            # Extract historical prices (you may need to adjust the path)
            prices = data.get("data")
            if prices and len(prices) >= 2:
                # Get the closing price 30 days ago and the most recent closing price
                end_price = prices[0].get("close")
                start_price = prices[-1].get("close")  # Assuming 30 trading days

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

    def _fetch_data(self, url, symbol):
        """
        Helper function to fetch data from RapidAPI with a workaround for 403 errors.
        """
        querystring = {"symbol": symbol, "period": "QUARTERLY", "language": "en"}
        response = requests.get(url, headers=self.headers, params=querystring)

        # Handle 403 error (Forbidden)
        if response.status_code == 403:
            print(f"Attempting workaround for symbol: {symbol}")
            querystring["symbol"] = f"{symbol}:NASDAQ"  # Try appending :NASDAQ
            response = requests.get(url, headers=self.headers, params=querystring)

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