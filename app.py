import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar el DataFrame desde el archivo CSV
df = pd.read_csv('stock_forecast.csv')

# Convertir la columna 'ds' a tipo datetime
df['ds'] = pd.to_datetime(df['ds'])

# Establecer los valores reales como null si la fecha es anterior al 10-08-2024
mask = df['ds'] < pd.to_datetime('2024-08-10')
tickers = ['AAPL', 'MSFT', 'AMZN']
for ticker in tickers:
    df.loc[mask, f'{ticker}_real'] = np.nan

# Título de la aplicación
st.title('Pronóstico de Acciones')

# Selectbox para escoger una acción
ticker = st.selectbox('Selecciona una acción:', options=tickers)

# Input de fecha de inicio y fin
start_date = st.date_input('Fecha de inicio', min_value=pd.to_datetime('2022-01-01'), max_value=pd.to_datetime('2024-08-30'))
end_date = st.date_input('Fecha de fin', min_value=start_date, max_value=pd.to_datetime('2024-08-11'))

# Input de número de días de pronóstico
forecast_days = st.slider('Número de días para el pronóstico', min_value=1, max_value=30, value=10)

# Filtrar el DataFrame por las fechas seleccionadas
filtered_df = df[(df['ds'] >= pd.to_datetime(start_date)) & (df['ds'] <= pd.to_datetime(end_date))]

# Filtrar el DataFrame por el número de días de pronóstico
forecast_filtered_df = filtered_df.tail(forecast_days)

# Gráficas
st.subheader(f'Gráfica de Valores Reales y Pronósticos para {ticker}')

fig, ax = plt.subplots(figsize=(12, 8))

# Graficar los valores reales y pronósticos para la acción seleccionada
ax.plot(filtered_df['ds'], filtered_df[f'{ticker}_real'], label=f'{ticker} Real', color='blue', linewidth=2)
ax.plot(forecast_filtered_df['ds'], forecast_filtered_df[f'{ticker}_forecast'], linestyle='--', label=f'{ticker} Pronóstico', color='orange', linewidth=2)

# Personalizar la gráfica
ax.set_xlabel('Fecha', fontsize=14)
ax.set_ylabel('Precio Ajustado', fontsize=14)
ax.set_title(f'Pronóstico vs Real para {ticker}', fontsize=18, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig)

filtered_df
