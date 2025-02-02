import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd

def fetch_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']  # Prophet requires columns 'ds' and 'y'
    df['ds'] = df['ds'].dt.tz_localize(None)
    return df

# Function to train Prophet model and make predictions
def predict_future_prices(df, years):
    # Initialize and fit the Prophet model
    model = Prophet()
    model.fit(df)
    
    # Create a future DataFrame for predictions
    future = model.make_future_dataframe(periods=years * 365)  # Convert years to days
    
    # Make predictions
    forecast = model.predict(future)
    
    return model, forecast

# Function to plot predictions
def plot_predictions(model, forecast, symbol):
    fig = model.plot(forecast)
    plt.title(f"{symbol} Stock Price Prediction")
    plt.xlabel("Date")
    plt.ylabel("Stock Price (USD)")
    plt.show()

# Main function
def main():
    # User inputs
    symbol = input("Enter the stock symbol (e.g., AAPL): ").upper()
    years = int(input("Enter the number of years to predict: "))
    
    # Fetch historical data
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    start_date = (pd.Timestamp.now() - pd.DateOffset(years=10)).strftime('%Y-%m-%d')  # Last 10 years of data
    df = fetch_stock_data(symbol, start_date, end_date)
    
    # Train Prophet model and make predictions
    model, forecast = predict_future_prices(df, years)
    
    # Display the latest price
    latest_price = df['y'].iloc[-1]
    print(f"Latest {symbol} stock price: ${latest_price:.2f}")
    
    # Display future predictions
    future_prices = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(years * 365)
    print(f"Predicted {symbol} stock prices for the next {years} year(s):")
    print(future_prices)
    
    # Plot predictions
    plot_predictions(model, forecast, symbol)

# Run the program
if __name__ == "__main__":
    main()