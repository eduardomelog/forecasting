import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar el DataFrame desde el archivo CSV
df = pd.read_csv('stock_forecast.csv')

# Convertir la columna 'ds' a tipo datetime
df['ds'] = pd.to_datetime(df['ds'])

# Título de la aplicación
st.title('Pronóstico de Acciones')

# Input de fecha de inicio y fin
start_date = st.date_input('Fecha de inicio', min_value=pd.to_datetime('2022-01-01'), max_value=pd.to_datetime('2024-08-09'))
end_date = st.date_input('Fecha de fin', min_value=start_date, max_value=pd.to_datetime('2024-08-09'))

# Input de número de días de pronóstico
forecast_days = st.slider('Número de días para el pronóstico', min_value=1, max_value=30, value=10)

# Filtrar el DataFrame por las fechas seleccionadas
filtered_df = df[(df['ds'] >= pd.to_datetime(start_date)) & (df['ds'] <= pd.to_datetime(end_date))]

# Filtrar el DataFrame por el número de días de pronóstico
forecast_filtered_df = filtered_df.tail(forecast_days)

# Gráficas
st.subheader('Gráfica de Valores Reales y Pronósticos')

# Configurar el estilo de las gráficas
plt.style.use('seaborn-darkgrid')
