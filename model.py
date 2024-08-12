import yfinance as yf
from prophet import Prophet
import pandas as pd

# List of tickers
tickers = ['MSFT', 'AAPL', 'AMZN', 'GOOGL', 'META']

# Download the data from Yahoo Finance
data = yf.download(tickers, start='2022-01-01')['Adj Close']

# Function to create and train the Prophet model and make the forecast
def forecast_stock(data, ticker):
    # Prepare the data for Prophet
    df = data[[ticker]].reset_index()
    df.columns = ['ds', f'{ticker}_real']

    # Create the model and fit it
    model = Prophet()
    model.fit(df.rename(columns={f'{ticker}_real': 'y'}))

    # Create a DataFrame for the next 30 days
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Return the DataFrame with the date, real values, and forecast
    forecast = forecast[['ds', 'yhat']].rename(columns={'yhat': f'{ticker}_forecast'})
    df_combined = pd.merge(df, forecast, on='ds', how='outer')
    
    return df_combined

# Create the forecast DataFrames for each ticker
forecast_combined = None

for ticker in tickers:
    forecast_ticker = forecast_stock(data, ticker)
    if forecast_combined is None:
        forecast_combined = forecast_ticker
    else:
        forecast_combined = pd.merge(forecast_combined, forecast_ticker, on='ds', how='outer')

# Display the first rows of the combined DataFrame
display(forecast_combined.head(10))
display(forecast_combined.tail(50))

# Save the DataFrame to a CSV file
forecast_combined.to_csv('stock_forecast.csv', index=False)
