import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('stock_forecast.csv')

# Convert the 'ds' column to datetime type
df['ds'] = pd.to_datetime(df['ds'])

# Set forecast values to null if the date is before 2024-08-10
mask = df['ds'] < pd.to_datetime('2024-08-10')
forecast_columns = [col for col in df.columns if 'forecast' in col]
df.loc[mask, forecast_columns] = np.nan

# Filter data to show only those before 2024-08-10 in the first graph
df_before_date = df[df['ds'] < pd.to_datetime('2024-08-10')]

# App title
st.title('Stock Forecast Visualization')

# Add a hyperlink to the GitHub repository
st.markdown("[GitHub Repository](https://github.com/eduardomelog/forecast)")

# Selectbox to choose a stock
ticker = st.selectbox('Select a stock:', options=['MSFT', 'AAPL', 'AMZN', 'GOOGL', 'META'])

fig, ax = plt.subplots(figsize=(12, 8))

# Plot the real and forecasted values for the selected stock before 2024-08-10
ax.plot(df_before_date['ds'], df_before_date[f'{ticker}_real'], label=f'{ticker} Real', linewidth=2, color='blue')
ax.plot(df_before_date['ds'], df_before_date[f'{ticker}_forecast'], linestyle='--', label=f'{ticker} Forecast', linewidth=2, color='orange')

# Customize the graph
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('Adjusted Price', fontsize=14)
ax.set_title(f'Real stock values for {ticker}', fontsize=18, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig)

# Filter data for the last two months
two_months_ago = df['ds'].max() - pd.DateOffset(months=2)
df_last_two_months = df[df['ds'] >= two_months_ago]

fig, ax = plt.subplots(figsize=(12, 8))

# Plot the real and forecasted values for the selected stock in the last two months
ax.plot(df_last_two_months['ds'], df_last_two_months[f'{ticker}_real'], label=f'{ticker} Real', linewidth=2, color='blue')
ax.plot(df_last_two_months['ds'], df_last_two_months[f'{ticker}_forecast'], linestyle='--', label=f'{ticker} Forecast', linewidth=2, color='orange')

# Customize the graph
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('Adjusted Price', fontsize=14)
ax.set_title(f'Forecast vs Real for {ticker} (Last 2 Months)', fontsize=18, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig)
