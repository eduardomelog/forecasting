import yfinance as yf
from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

# Set up Streamlit app
st.title("Stock Price Prediction with Prophet")
st.write("This app allows you to predict stock prices using Prophet. You can choose the start date for historical data and the number of prediction days.")

# User inputs
start_date = st.date_input("Select start date for historical data (min: 01-01-2022)", value=datetime(2022, 1, 1), min_value=datetime(2022, 1, 1), max_value=datetime.now().date())
prediction_days = st.slider("Select number of prediction days", min_value=1, max_value=30, value=10)

# Define the stock symbol for Apple in a list
stocks = ['AAPL']

# Fetch data from Yahoo Finance
stock_data = {}
for stock in stocks:
    stock_data[stock] = yf.download(stock, start=start_date)

# Prepare the data for Prophet
prepared_data = {}
for stock, data in stock_data.items():
    df = data[['Close']].reset_index()
    df.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    prepared_data[stock] = df

# Train a forecasting model for AAPL
models = {}
predictions = {}
for stock, df in prepared_data.items():
    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    model.fit(df)
    future = model.make_future_dataframe(periods=prediction_days)
    forecast = model.predict(future)
    models[stock] = model
    predictions[stock] = forecast

# Display the last 3 months of data
for stock, data in stock_data.items():
    last_three_months = data[data.index >= (data.index.max() - pd.DateOffset(months=3))]
    
    st.write(f"## Last 3 months of data for {stock}")
    st.line_chart(last_three_months['Close'])

# Display predictions with customizable prediction days
for stock, forecast in predictions.items():
    last_period = forecast.iloc[-(30+prediction_days):]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(np.array(last_period['ds'][:-prediction_days]), last_period['yhat'][:-prediction_days], label='Historical Data', color='dodgerblue', linewidth=2)
    ax.plot(np.array(last_period['ds'][-prediction_days:]), last_period['yhat'][-prediction_days:], linestyle='--', label='Prediction', color='darkorange', linewidth=2)
    ax.fill_between(np.array(last_period['ds']), last_period['yhat_lower'], last_period['yhat_upper'], color='orange', alpha=0.2)
    
    today_minus_one = datetime.now().date() - timedelta(days=1)
    ax.axvline(x=pd.to_datetime(today_minus_one), color='red', linestyle='--', label=f'{today_minus_one}')
    
    ax.set_title(f"Prediction for {stock} - Last 30 days and {prediction_days} future days", fontsize=16)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Close Price", fontsize=12)
    ax.legend(fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True)
    
    st.write(f"## Prediction for {stock}")
    st.pyplot(fig)
