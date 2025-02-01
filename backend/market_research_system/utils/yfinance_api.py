import yfinance as yf
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import os
import requests

class YFinanceAPI:
    def get_stock_chart(self, stock_symbol, period="1y"):
        """
        Retrieves the historical stock chart data using YFinance.

        Args:
            stock_symbol: The stock symbol.
            period: The time period for the chart (e.g., "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max").

        Returns:
            Base64 encoded image data of the stock chart.
        """
        try:
            ticker = yf.Ticker(stock_symbol)
            hist = ticker.history(period=period)

            # Create a plot
            plt.figure(figsize=(10, 5))
            plt.plot(hist['Close'])
            plt.title(f'{stock_symbol} Stock Chart ({period})')
            plt.xlabel('Date')
            plt.ylabel('Price')

            # Save the plot to a BytesIO object
            image_stream = BytesIO()
            plt.savefig(image_stream, format='png')
            image_stream.seek(0)
            plt.close()

            # Encode the image to base64
            base64_image = base64.b64encode(image_stream.read()).decode('utf-8')
            return base64_image
        except Exception as e:
            print(f"Error getting stock chart for {stock_symbol}: {e}")
            return None

    def get_company_info(self, stock_symbol):
        """
        Retrieves key company information using YFinance.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            A dictionary containing company information.
        """
        try:
            ticker = yf.Ticker(stock_symbol)
            info = ticker.info
            # You might want to filter or select specific information from 'info'
            return info
        except Exception as e:
            print(f"Error getting company info for {stock_symbol}: {e}")
            return {}

    def get_financial_data(self, stock_symbol):
        """
        Retrieves key financial data using YFinance.

        Args:
            stock_symbol: The stock symbol.

        Returns:
            A dictionary containing financial data.
        """
        try:
            ticker = yf.Ticker(stock_symbol)
            financials = ticker.financials
            # You might want to filter or select specific data from 'financials'
            return financials
        except Exception as e:
            print(f"Error getting financial data for {stock_symbol}: {e}")
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