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

# Título de la aplicación
st.title('Visualización de Pronóstico de Acciones')

# Gráficas
st.subheader('Gráfica de Valores Reales y Pronósticos')

fig, ax = plt.subplots(figsize=(12, 8))

# Graficar los valores reales y pronósticos para cada acción
for col in forecast_columns:
    ax.plot(df['ds'], df[col.replace('_forecast', '_real')], label=col.replace('_forecast', '_real'), linewidth=2)
    ax.plot(df['ds'], df[col], linestyle='--', label=col, linewidth=2)

# Personalizar la gráfica
ax.set_xlabel('Fecha', fontsize=14)
ax.set_ylabel('Precio Ajustado', fontsize=14)
ax.set_title('Pronóstico vs Real', fontsize=18, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig)

