df = pd.read_csv('stock_forecast.csv')

# Convertir la columna 'ds' a tipo datetime
df['ds'] = pd.to_datetime(df['ds'])

# Título de la aplicación
st.title('Pronóstico de Acciones')
