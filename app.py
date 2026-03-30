# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V2.0 EDICIÓN LUJO - RADAR GLOBAL
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

# 2. ESTÉTICA PREMIUM (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; }
    .stButton>button { border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 5px; border-width: 2px;}
    .stButton>button:hover { background-color: #d4af37; color: black; }
    </style>
""", unsafe_allow_html=True)

# 3. BASE DE DATOS EXTENDIDA (ARSENAL GLOBAL)
ASSETS = {
    # 💱 FOREX (PARES MAYORES)
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "USDJPY=X": "USD/JPY",
    "USDCHF=X": "USD/CHF", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD", "NZDUSD=X": "NZD/USD",
    
    # 🪙 CRIPTOMONEDAS
    "BTC-USD": "BITCOIN", "ETH-USD": "ETHEREUM", "SOL-USD": "SOLANA", 
    "XRP-USD": "RIPPLE", "ADA-USD": "CARDANO", "BNB-USD": "BINANCE COIN",
    
    # 📊 ÍNDICES BURSÁTILES (FUTUROS)
    "ES=F": "S&P 500", "NQ=F": "NASDAQ 100", "YM=F": "DOW JONES", 
    "RTY=F": "RUSSELL 2000", "^GDAXI": "DAX ALEMÁN", "^FTSE": "FTSE 100 UK", "^N225": "NIKKEI 225 JAPÓN",
    
    # 🛢️ MATERIAS PRIMAS
    "GC=F": "ORO", "SI=F": "PLATA", "CL=F": "PETRÓLEO WTI", 
    "NG=F": "GAS NATURAL", "HG=F": "COBRE", "ZC=F": "MAÍZ"
} 

ORACULOS = {"DX-Y.NYB": "DXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

@st.cache_data(ttl=300) # Cache para optimizar velocidad
def get_data(ticker, p="1y"):
    df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
    if not df.empty and isinstance(df.columns, pd.MultiIndex): 
        df.columns = df.columns.get_level_values(0)
    return df if not df.empty else None

# 4. INTERFAZ PRINCIPAL
st.title("🦅 G-SNIPER QUANT TERMINAL | V2.0 GLOBAL")
st.caption(f"SINCROMECANISMO NYT: {datetime.now(pytz.timezone('America/New_York')).strftime('%d-%b-%Y %H:%M:%S')} | ESTADO: OPERATIVO 🟢")
st.markdown("---")

# PANEL LATERAL DE MANDO
st.sidebar.markdown("### 🎯 CENTRO DE MANDO")
selected_ticker = st.sidebar.selectbox("SELECCIONAR ACTIVO PARA ANÁLISIS:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])

if st.sidebar.button("⚡ ESCANEAR TODO EL MERCADO"):
    st.session_state['scan_all'] = True
else:
    if 'scan_all' not in st.session_state:
        st.session_state['scan_all'] = False

# SECCIÓN A: ORÁCULOS MACRO
st.markdown("### 🌐 MONITORES MACROECONÓMICOS")
macro_cols = st.columns(3)
for i, (t, n) in enumerate(ORACULOS.items()):
    df_o = get_data(t, "5d")
    if df_o is not None:
        val = float(df_o['Close'].iloc[-1])
        prev = float(df_o['Close'].iloc[-2]) if len(df_o)>1 else val
        delta = val - prev
        macro_cols[i].metric(n, f"{val:.2f}", f"{delta:.2f}")
st.markdown("---")

# SECCIÓN B: ANÁLISIS PROFUNDO CON GRÁFICO
st.markdown(f"### 🔭 ANÁLISIS TÁCTICO INDIVIDUAL: {ASSETS[selected_ticker]}")
df_activo = get_data(selected_ticker, "6mo")

if df_activo is not None and not df_activo.empty and len(df_activo) > 20:
    # Construcción del Gráfico Profesional
    fig = go.Figure(data=[go.Candlestick(x=df_activo.index,
                    open=df_activo['Open'], high=df_activo['High'],
                    low=df_activo['Low'], close=df_activo['Close'],
                    increasing_line_color='#00ff00', decreasing_line_color='#ff0000')])
    fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=450,
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    
    col_graf, col_datos = st.columns([2.5, 1])
    with col_graf:
        st.plotly_chart(fig, use_container_width=True)
    
    with col_datos:
        st.markdown("#### 🧠 MATRIZ IA & RIESGO")
        # Lógica ML
        df_activo['EMA20'] = df_activo['Close'].ewm(span=20, adjust=False).mean()
        df_activo['Z'] = (df_activo['Close'] - df_activo['EMA20']) / df_activo['Close'].rolling(20).std().replace(0, 0.001)
        df_activo['Target'] = (df_activo['Close'].shift(-1) > df_activo['Close']).astype(int)
        train = df_activo[['Z', 'Target']].dropna()
        
        if len(train) > 0:
            model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
            prob = float(model.predict_proba(df_activo[['Z']].iloc[[-1]])[0][1] * 100)
            
            p = float(df_activo['Close'].iloc[-1])
            acc = "🟢 ALCISTA (BUY)" if p > df_activo['EMA20'].iloc[-1] else "🔴 BAJISTA (SELL)"
            
            st.metric("PRECIO ACTUAL", f"{p:.4f}")
            st.metric("TENDENCIA TÉCNICA", acc)
            
            st.markdown("#### PROBABILIDAD DE ÉXITO (IA)")
            st.progress(int(prob))
            color = '#00ff00' if prob >= 50 else '#ff0000'
            st.markdown(f"<h2 style='color: {color} !important;'>{prob:.1f}%</h2>", unsafe_allow_html=True)
        else:
            st.warning("Datos insuficientes para la IA en este activo.")
else:
    st.error("Mercado cerrado o datos no disponibles temporalmente para este activo.")

# SECCIÓN C: MATRIZ UNIVERSAL
if st.session_state['scan_all']:
    st.markdown("---")
    st.markdown("### ⚡ MATRIZ DE ESCANEO UNIVERSAL")
    with st.spinner("Desplegando Redes Neuronales sobre el mercado global... Esto tomará unos segundos."):
        results = []
        for t, name in ASSETS.items():
            df = get_data(t, "1y")
            if df is None or len(df) < 50: continue
            df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['Z'] = (df['Close'] - df['EMA20']) / df['Close'].rolling(20).std().replace(0, 0.001)
            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            train = df[['Z', 'Target']].dropna()
            
            if len(train) > 0:
                model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
                prob = float(model.predict_proba(df[['Z']].iloc[[-1]])[0][1] * 100)
                
                precio = float(df['Close'].iloc[-1])
                tendencia = "ALCISTA 🟢" if precio > df['EMA20'].iloc[-1] else "BAJISTA 🔴"
                accion = "🔥 EJECUTAR" if (prob > 58 or prob < 42) else "🛡️ ACECHAR"
                
                results.append({"MERCADO": name, "PRECIO": f"{precio:.4f}", "TENDENCIA": tendencia, "PROB. IA": f"{prob:.1f}%", "ACCIÓN": accion})
        
        st.dataframe(pd.DataFrame(results), use_container_width=True)
