import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
import json
import argparse

def fetch_stock_data(symbol, start_date, end_date):
    """Fetches historical stock data from Yahoo Finance."""
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    df = df[['Date', 'Close']]
    df.columns = ['ds', 'y']  # Prophet requires columns 'ds' and 'y'
    df['ds'] = df['ds'].dt.tz_localize(None)
    return df

def predict_future_prices(df, years, seasonality_mode='additive', changepoint_prior_scale=0.05, holidays_prior_scale=10, seasonality_prior_scale=10):
    """
    Trains a Prophet model and makes predictions.

    Args:
        df (pd.DataFrame): DataFrame with 'ds' (datestamp) and 'y' (value) columns.
        years (int): Number of years to predict into the future.
        seasonality_mode (str): 'additive' or 'multiplicative'.
        changepoint_prior_scale (float): Adjust the flexibility of the trend.
        holidays_prior_scale (float): Adjust the strength of holidays effects.
        seasonality_prior_scale (float): Adjust the strength of seasonality effects.
    
    Returns:
        Prophet: Trained Prophet model.
        pd.DataFrame: Forecast DataFrame.
    """
    model = Prophet(
        seasonality_mode=seasonality_mode,
        changepoint_prior_scale=changepoint_prior_scale,
        holidays_prior_scale=holidays_prior_scale,
        seasonality_prior_scale=seasonality_prior_scale,
        daily_seasonality=True, 
        weekly_seasonality=True,
        yearly_seasonality=True
    )
    
    # Add specific holidays (example for US)
    # You can customize this for different countries/regions
    model.add_country_holidays(country_name='US')

    model.fit(df)
    future = model.make_future_dataframe(periods=years * 365)
    forecast = model.predict(future)
    return model, forecast

def plot_predictions(model, forecast, symbol, historical_color='#0072B2', forecast_color='#D55E00', uncertainty_color='#009E73'):
    """
    Plots the Prophet model's predictions with enhanced aesthetics.

    Args:
        model (Prophet): Trained Prophet model.
        forecast (pd.DataFrame): Forecast DataFrame.
        symbol (str): Stock symbol.
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

    plt.savefig(f"{symbol}_prediction.png")
    plt.close(fig)

def main():
    """
    Fetches stock data, trains Prophet models, makes predictions, and generates plots for multiple stocks.
    """
    parser = argparse.ArgumentParser(description="Predict stock prices using Prophet.")
    parser.add_argument("years", type=int, help="Number of years to predict")
    args = parser.parse_args()
    years_to_predict = args.years

    try:
        with open("..\data\stocks.json", "r") as f:
            stocks_data = json.load(f)
    except FileNotFoundError:
        print("Error: stocks.json file not found.")
        return

    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    start_date = (pd.Timestamp.now() - pd.DateOffset(years=10)).strftime('%Y-%m-%d')

    for stock in stocks_data:
        symbol = stock["tickerSymbol"]
        print(f"Processing {symbol}...")

        try:
            df = fetch_stock_data(symbol, start_date, end_date)

            # --- Model Tuning Parameters (Experiment with these!) ---
            seasonality_mode = 'multiplicative'  # Try 'additive' as well
            changepoint_prior_scale = 0.1  # Increase for more flexible trend
            holidays_prior_scale = 10      # Increase to make holidays have a stronger effect
            seasonality_prior_scale = 10   # Increase to make seasonality have a stronger effect

            model, forecast = predict_future_prices(
                df, years_to_predict, 
                seasonality_mode=seasonality_mode,
                changepoint_prior_scale=changepoint_prior_scale,
                holidays_prior_scale=holidays_prior_scale,
                seasonality_prior_scale=seasonality_prior_scale
            )

            # --- Enhanced Plotting ---
            plot_predictions(model, forecast, symbol)
            print(f"Prediction plot saved for {symbol}")

            # Display the latest price
            latest_price = df['y'].iloc[-1]
            print(f"Latest {symbol} stock price: ${latest_price:.2f}")
        
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

if __name__ == "__main__":
    main()