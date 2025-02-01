import json
import os
import yfinance as yf

STOCKS_FILE = './data/stocks.json'
BONDS_FILE = './data/bonds.json'


def load_stocks_data():
    """Loads stock data from the JSON file or creates it if not present."""
    if not os.path.exists(STOCKS_FILE):
        os.makedirs(os.path.dirname(STOCKS_FILE), exist_ok=True)
        save_stocks_data([])

    with open(STOCKS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_stocks_data(data):
    """Saves stock data to the JSON file."""
    with open(STOCKS_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def fetch_stock_data(ticker):
    """Fetches real-time stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y")
        dividends = history["Dividends"].sum()
        current_price = stock.history(period="1d")["Close"].iloc[-1]

        return {
            "currentPrice": round(current_price, 2),
            "dividendYield": round((dividends / current_price) * 100, 2) if current_price else 0,
        }
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return {
            "currentPrice": None,
            "dividendYield": None,
        }

def calculate_stock_value(stock):
    """Calculates the value of a stock holding."""
    if stock.get("currentPrice") is not None and stock.get("numberOfShares") is not None:
      return stock["currentPrice"] * stock["numberOfShares"]
    return 0



# ------ Bonds ------- #

def load_bonds_data():
    """Loads bond data from the JSON file or returns an empty list."""
    if os.path.exists(BONDS_FILE):
        with open(BONDS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_bonds_data(data):
    """Saves bond data to the JSON file."""
    with open(BONDS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_bond_value(bond):
  """Calculates the value of a bond holding."""
  if bond.get("principal") is not None:
      return bond["principal"]
  return 0

def calculate_total_portfolio_value(stocks, bonds):
    """Calculates the total value of the portfolio."""
    stock_value = sum(calculate_stock_value(stock) for stock in stocks)
    bond_value = sum(calculate_bond_value(bond) for bond in bonds)
    return stock_value + bond_value


def update_portfolio_weightages():
    """Updates the weightageInPortfolio for all stocks and bonds."""
    stocks = load_stocks_data()
    bonds = load_bonds_data()
    total_portfolio_value = calculate_total_portfolio_value(stocks, bonds)


    if total_portfolio_value == 0:
        for stock in stocks:
            stock["weightageInPortfolio"] = 0
        for bond in bonds:
            bond["weightageInPortfolio"] = 0
    else:
    # Update stock weightages
        for stock in stocks:
          stock_value = calculate_stock_value(stock)
          stock["weightageInPortfolio"] = round((stock_value / total_portfolio_value) * 100, 2) if stock_value else 0


        # Update bond weightages
        for bond in bonds:
            bond_value = calculate_bond_value(bond)
            bond["weightageInPortfolio"] = round((bond_value / total_portfolio_value) * 100, 2) if bond_value else 0



    save_stocks_data(stocks)
    save_bonds_data(bonds)