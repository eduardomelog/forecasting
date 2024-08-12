import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('stock_forecast.csv')

# Convertir la columna 'ds' a tipo datetime
df['ds'] = pd.to_datetime(df['ds'])

# Establecer los valores de pronóstico como null si la fecha es anterior al 10-08-2024
mask = df['ds'] < pd.to_datetime('2024-08-10')
forecast_columns = [col for col in df.columns if 'forecast' in col]
df.loc[mask, forecast_columns] = np.nan

# Filtrar datos para mostrar solo aquellos antes del 10-08-2024 en el primer gráfico
df_before_date = df[df['ds'] < pd.to_datetime('2024-08-10')]

# Título de la aplicación
st.title('Visualización de Pronóstico de Acciones')

# Selectbox para escoger una acción
ticker = st.selectbox('Selecciona una acción:', options=['AAPL', 'MSFT', 'AMZN'])

# Gráfica completa antes del 10-08-2024
st.subheader(f'Gráfica de Valores Reales y Pronósticos para {ticker} (Antes del 10-08-2024)')

fig, ax = plt.subplots(figsize=(12, 8))

# Graficar los valores reales y pronósticos para la acción seleccionada antes del 10-08-2024
ax.plot(df_before_date['ds'], df_before_date[f'{ticker}_real'], label=f'{ticker} Real', linewidth=2, color='blue')
ax.plot(df_before_date['ds'], df_before_date[f'{ticker}_forecast'], linestyle='--', label=f'{ticker} Pronóstico', linewidth=2, color='orange')

# Personalizar la gráfica
ax.set_xlabel('Fecha', fontsize=14)
ax.set_ylabel('Precio Ajustado', fontsize=14)
ax.set_title(f'Pronóstico vs Real para {ticker} (Antes del 10-08-2024)', fontsize=18, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig)

# Gráfica de los últimos dos meses
st.subheader(f'Gráfica de Valores Reales y Pronósticos para {ticker} (Últimos 2 Meses)')

# Filtrar los datos para los últimos dos meses
two_months_ago = df['ds'].max() - pd.DateOffset(months=2)
df_last_two_months = df[df['ds'] >= two_months_ago]

fig, ax = plt.subplots(figsize=(12, 8))

# Graficar los valores reales y pronósticos para la acción seleccionada en los últimos dos meses
ax.plot(df_last_two_months['ds'], df_last_two_months[f'{ticker}_real'], label=f'{ticker} Real', linewidth=2, color='blue')
ax.plot(df_last_two_months['ds'], df_last_two_months[f'{ticker}_forecast'], linestyle='--', label=f'{ticker} Pronóstico', linewidth=2, color='orange')

# Personalizar la gráfica
ax.set_xlabel('Fecha', fontsize=14)
ax.set_ylabel('Precio Ajustado', fontsize=14)
ax.set_title(f'Pronóstico vs Real para {ticker} (Últimos 2 Meses)', fontsize=18, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig)
