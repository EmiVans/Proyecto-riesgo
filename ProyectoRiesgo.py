import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import kurtosis, skew, shapiro ,norm

st.title("Evaluación del Riesgo Financiero de NVIDIA")

# Descarga los datos de los ultimos 10 años
@st.cache_data
def obtener_datos(stock):
    df = yf.download(stock, start="2010-01-01")["Close"]
    return df

# Calcula los rendimientos diarios
@st.cache_data
def calcular_rendimientos(df):
    return df.pct_change().dropna()


with st.spinner("Descargando datos..."):
    NVIDIA_precios = obtener_datos('NVDA')
    NVIDIA_rendimientos = calcular_rendimientos(NVIDIA_precios)


st.subheader(f"Métricas de Rendimiento: Nvidia")

rendimiento_medio = NVIDIA_rendimientos.mean()
Kurtosis = kurtosis(NVIDIA_rendimientos)
skew = skew(NVIDIA_rendimientos)
    
col1, col2, col3 = st.columns(3)

# Asegúrate de que las variables sean numéricas y luego formatea correctamente
col1.metric("Rendimiento Medio Diario", f"{rendimiento_medio:.4%}")
col2.metric("Kurtosis", f"{Kurtosis:.4f}")  # Asegúrate de que Kurtosis tenga 4 decimales
col3.metric("Skew", f"{skew:.2f}")  # Asegúrate de que Skew tenga 2 decimales

# Gráfico de rendimientos diarios
st.subheader(f"Gráfico de Rendimientos: NVIDIA")
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(NVIDIA_rendimientos.index, NVIDIA_rendimientos, label="NVIDIA")
ax.axhline(y=0, color='r', linestyle='--', alpha=0.7)
ax.legend()
ax.set_title(f"Rendimientos de NVIDIA")
ax.set_xlabel("Fecha")
ax.set_ylabel("Rendimiento Diario")
st.pyplot(fig)
    
# Histograma de rendimientos
st.subheader("Distribución de Rendimientos")
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(NVIDIA_rendimientos, bins=30, alpha=0.7, color='blue', edgecolor='black')
ax.axvline(rendimiento_medio, color='red', linestyle='dashed', linewidth=2, label=f"Promedio: {rendimiento_medio:.4%}")
ax.legend()
ax.set_title("Histograma de Rendimientos")
ax.set_xlabel("Rendimiento Diario")
ax.set_ylabel("Frecuencia")
st.pyplot(fig)

    