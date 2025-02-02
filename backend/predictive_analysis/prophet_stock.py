import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
import base64

def fetch_stock_data(symbol, start_date, end_date):
    """
    Fetches historical stock data from Yahoo Finance.
    
    Attempts to get more granular data (daily) if available, otherwise falls back to weekly.
    """
    stock = yf.Ticker(symbol)

    # Try to get daily data first
    df = stock.history(start=start_date, end=end_date, interval="1d")
    
    if df.empty:
        print(f"No daily data found for {symbol}, trying weekly interval...")
        # If daily data is not available, try weekly data
        df = stock.history(start=start_date, end=end_date, interval="1wk")

        if df.empty:
            print(f"No weekly data found for {symbol}, trying monthly interval...")
            # If weekly data is not available, try monthly data
            df = stock.history(start=start_date, end=end_date, interval="1mo")

    if df.empty:
        print(f"No data found for {symbol} between {start_date} and {end_date}.")
        return None

    df.reset_index(inplace=True)
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']  # Prophet requires columns 'ds' and 'y'
    df['ds'] = df['ds'].dt.tz_localize(None)  # Remove timezone information
    return df

def predict_future_prices(df, years, seasonality_mode='additive', changepoint_prior_scale=0.05, holidays_prior_scale=10, seasonality_prior_scale=10, growth='linear'):
    """
    Trains a Prophet model and makes predictions.

    Args:
        df (pd.DataFrame): DataFrame with 'ds' (datestamp) and 'y' (value) columns.
        years (int): Number of years to predict into the future.
        seasonality_mode (str): 'additive' or 'multiplicative'.
        changepoint_prior_scale (float): Adjust the flexibility of the trend.
        holidays_prior_scale (float): Adjust the strength of holidays effects.
        seasonality_prior_scale (float): Adjust the strength of seasonality effects.
        growth (str): 'linear' or 'logistic' - type of growth curve.
    
    Returns:
        Prophet: Trained Prophet model.
        pd.DataFrame: Forecast DataFrame.
    """

    # For logistic growth, we need to specify a carrying capacity
    if growth == 'logistic':
        # Example: Set carrying capacity to a value higher than the maximum historical price
        # You might need to adjust this based on your understanding of the stock
        df['cap'] = df['y'].max() * 2 

    model = Prophet(
        growth=growth,
        seasonality_mode=seasonality_mode,
        changepoint_prior_scale=changepoint_prior_scale,
        holidays_prior_scale=holidays_prior_scale,
        seasonality_prior_scale=seasonality_prior_scale,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    # Add specific holidays (example for US)
    model.add_country_holidays(country_name='US')

    model.fit(df)
    future = model.make_future_dataframe(periods=years * 365)

    # Add carrying capacity to future dataframe for logistic growth
    if growth == 'logistic':
        future['cap'] = df['cap'].iloc[0]  # Use the same cap as in the historical data

    forecast = model.predict(future)
    return model, forecast

def plot_predictions(model, forecast, symbol, output_dir, historical_color='#0072B2', forecast_color='#D55E00', uncertainty_color='#009E73'):
    """
    Plots the Prophet model's predictions with enhanced aesthetics.

    Args:
        model (Prophet): Trained Prophet model.
        forecast (pd.DataFrame): Forecast DataFrame.
        symbol (str): Stock symbol.
        output_dir(str): The directory to save the images
        historical_color (str): Color for historical data.
        forecast_color (str): Color for forecasted data.
        uncertainty_color (str): Color for uncertainty intervals.
    """
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)

    # Plot historical data
    ax.plot(model.history['ds'], model.history['y'], color=historical_color, label='Historical', linewidth=2)

    # Plot forecasted data
    ax.plot(forecast['ds'], forecast['yhat'], color=forecast_color, label='Forecast', linewidth=2)

    # Fill uncertainty intervals
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color=uncertainty_color, alpha=0.3, label='Uncertainty Interval')

    # Customize plot
    ax.set_title(f"{symbol} Stock Price Prediction", fontsize=16)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Stock Price (USD)", fontsize=14)
    ax.grid(True, which='major', c='gray', ls='-', lw=1, alpha=0.2)
    ax.legend(fontsize=12)

    # Improve tick labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    image_path = os.path.join(output_dir, f"{symbol}_prediction.png")
    plt.savefig(image_path)
    plt.close(fig)
    return image_path

def main(years):
    """
    Fetches stock data, trains Prophet models, makes predictions, and generates plots for multiple stocks.
    """
    try:
        abs_path = os.path.join(os.path.dirname(__file__), "../data/stocks.json")
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"File not found: {abs_path}")
        with open(abs_path, 'r') as file:
            stocks_data = json.load(file)
    except FileNotFoundError:
        print("Error: stocks.json file not found.")
        return []

    # Fetch as much historical data as possible
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    start_date = '1950-01-01' # YFinance can handle this far back
    
    image_data_list = []
    
    output_dir = os.path.dirname(__file__)

    for stock in stocks_data:
        symbol = stock["tickerSymbol"]
        print(f"Processing {symbol}...")

        try:
            df = fetch_stock_data(symbol, start_date, end_date)
            if df is None:
                print(f"Skipping {symbol} due to insufficient data.")
                continue

            # --- Model Tuning Parameters ---
            # Experiment with these to potentially improve accuracy
            seasonality_mode = 'multiplicative'  # Try 'additive' too
            changepoint_prior_scale = 0.15 # Increased flexibility for trend changes, was 0.1
            holidays_prior_scale = 15  # Increased impact of holidays, was 10      
            seasonality_prior_scale = 15 # Increased impact of seasonality, was 10
            growth = 'linear'  # Try 'logistic' if you expect saturation

            model, forecast = predict_future_prices(
                df, years, 
                seasonality_mode=seasonality_mode,
                changepoint_prior_scale=changepoint_prior_scale,
                holidays_prior_scale=holidays_prior_scale,
                seasonality_prior_scale=seasonality_prior_scale,
                growth=growth
            )

            # --- Enhanced Plotting ---
            image_path = plot_predictions(model, forecast, symbol, output_dir)
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            image_data_list.append(image_data)
            print(f"Prediction plot saved for {symbol}")

            # Display the latest price
            latest_price = df['y'].iloc[-1]
            print(f"Latest {symbol} stock price: ${latest_price:.2f}")
        
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
    return image_data_list