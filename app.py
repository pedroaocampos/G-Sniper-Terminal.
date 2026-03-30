# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V2.1 - EDICIÓN LEGIBILIDAD PRO
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import pytz
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

# 2. ESTÉTICA PREMIUM MEJORADA (CSS) - CORRECCIÓN DE CONTRASTE
st.markdown("""
    <style>
    /* Fondo General */
    .stApp { background-color: #0b0d11; }
    
    /* Títulos en Dorado Institucional */
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    
    /* Texto General en Gris Plata (Evita el deslumbramiento del blanco) */
    .stMarkdown, p, span, label { color: #bdc3c7 !important; font-family: 'Arial', sans-serif; }
    
    /* Métricas: Etiquetas en Dorado, Valores en Blanco suave */
    [data-testid="stMetricLabel"] { color: #d4af37 !important; font-size: 16px !important; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-weight: bold !important; }
    
    /* Botones Estilizados */
    .stButton>button { border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; border-width: 2px; background-color: transparent; font-weight: bold; }
    .stButton>button:hover { background-color: #d4af37; color: #0b0d11; }
    
    /* Sidebar (Menú Lateral) */
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #d4af37; }
    </style>
""", unsafe_allow_html=True)

# 3. BASE DE DATOS EXTENDIDA (ARSENAL GLOBAL)
ASSETS = {
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "USDJPY=X": "USD/JPY",
    "USDCHF=X": "USD/CHF", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD",
    "BTC-USD": "BITCOIN", "ETH-USD": "ETHEREUM", "SOL-USD": "SOLANA", 
    "ES=F": "S&P 500", "NQ=F": "NASDAQ 100", "GC=F": "ORO", "SI=F": "PLATA", "CL=F": "PETRÓLEO"
} 
ORACULOS = {"DX-Y.NYB": "DXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

@st.cache_data(ttl=300)
def get_data(ticker, p="1y"):
    try:
        df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
        if not df.empty and isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return None

# 4. INTERFAZ PRINCIPAL
st.title("🦅 G-SNIPER QUANT TERMINAL")
st.caption(f"SINCROMECANISMO NYT: {datetime.now(pytz.timezone('America/New_York')).strftime('%d-%b-%Y %H:%M:%S')} | MODO: ALTA VISIBILIDAD 🟢")
st.markdown("---")

# PANEL LATERAL
st.sidebar.markdown("### 🎯 CENTRO DE MANDO")
selected_ticker = st.sidebar.selectbox("SELECCIONAR ACTIVO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
scan_btn = st.sidebar.button("⚡ ESCANEAR MERCADO GLOBAL")

# SECCIÓN A: ORÁCULOS MACRO
st.markdown("#### 🌐 MONITORES ESTRATÉGICOS")
macro_cols = st.columns(3)
for i, (t, n) in enumerate(ORACULOS.items()):
    df_o = get_data(t, "5d")
    if df_o is not None and not df_o.empty:
        val = float(df_o['Close'].iloc[-1])
        prev = float(df_o['Close'].iloc[-2]) if len(df_o)>1 else val
        delta = val - prev
        macro_cols[i].metric(n, f"{val:.2f}", f"{delta:.2f}")

st.markdown("---")

# SECCIÓN B: ANÁLISIS PROFUNDO
st.markdown(f"#### 🔭 FOCO TÁCTICO: {ASSETS[selected_ticker]}")
df_activo = get_data(selected_ticker, "6mo")

if df_activo is not None and not df_activo.empty:
    fig = go.Figure(data=[go.Candlestick(x=df_activo.index,
                    open=df_activo['Open'], high=df_activo['High'],
                    low=df_activo['Low'], close=df_activo['Close'],
                    increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
    fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=400,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("##### 🧠 MATRIZ DE RIESGO IA")
        df_activo['EMA20'] = df_activo['Close'].ewm(span=20, adjust=False).mean()
        df_activo['Z'] = (df_activo['Close'] - df_activo['EMA20']) / df_activo['Close'].rolling(20).std().replace(0, 0.001)
        df_activo['Target'] = (df_activo['Close'].shift(-1) > df_activo['Close']).astype(int)
        train = df_activo[['Z', 'Target']].dropna()
        
        if len(train) > 10:
            model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
            prob = float(model.predict_proba(df_activo[['Z']].iloc[[-1]])[0][1] * 100)
            precio = float(df_activo['Close'].iloc[-1])
            
            st.metric("PRECIO ACTUAL", f"{precio:.4f}")
            st.markdown(f"**CONFIANZA IA:** `{prob:.1f}%`")
            st.progress(int(prob))
            
            sentencia = "🔥 EJECUTAR COMPRA" if prob > 60 else "🔴 EJECUTAR VENTA" if prob < 40 else "🛡️ EN ESPERA"
            st.info(sentencia)

# SECCIÓN C: ESCÁNER GLOBAL
if scan_btn:
    st.markdown("---")
    st.markdown("#### ⚡ ESCÁNER DE ALTO NIVEL")
    results = []
    with st.spinner("Procesando..."):
        for t, name in ASSETS.items():
            df = get_data(t, "1y")
            if df is not None and len(df) > 50:
                df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
                df['Z'] = (df['Close'] - df['EMA20']) / df['Close'].rolling(20).std().replace(0, 0.001)
                df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
                train = df[['Z', 'Target']].dropna()
                model = RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
                prob = float(model.predict_proba(df[['Z']].iloc[[-1]])[0][1] * 100)
                results.append({"MERCADO": name, "PRECIO": f"{df['Close'].iloc[-1]:.4f}", "IA PROB": f"{prob:.1f}%"})
        st.table(pd.DataFrame(results))
