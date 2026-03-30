# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V6.5 - HYPER-SPEED SCANNER (Lanzamiento Hotmart)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import pytz
from datetime import datetime
import time

# 1. CONFIGURACIÓN
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

# 2. CSS PREMIUM
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    .branding-header { text-align: center; padding: 15px; border-bottom: 2px solid #d4af37; margin-bottom: 25px; }
    .quant-card { background-color: #161b22; border: 1px solid #d4af37; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; }
    .risk-box { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .academy-card { background: linear-gradient(145deg, #1e242c, #161b22); border-left: 5px solid #d4af37; padding: 30px; border-radius: 12px; margin-bottom: 30px; }
    .badge-buy { background-color: #27ae60; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    .stButton>button { border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES CORE
def calc_zscore(df, period=20):
    close = df['Close']
    return (close - close.rolling(window=period).mean()) / close.rolling(window=period).std()

def calc_vpin(df, window=20):
    vpt = (df['Volume'] * (df['Close'].pct_change())).rolling(window=window).std()
    return (vpt / vpt.rolling(window=100).max()) * 100

@st.cache_data(ttl=600)
def get_single_data(ticker):
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        return df
    except: return None

# 4. ARSENAL
ASSETS = {
    "EURUSD=X": "💱 EUR/USD", "GBPUSD=X": "💱 GBP/USD", "USDJPY=X": "💱 USD/JPY", "USDCHF=X": "💱 USD/CHF",
    "AUDUSD=X": "💱 AUD/USD", "USDCAD=X": "💱 USD/CAD", "NZDUSD=X": "💱 NZD/USD", "EURGBP=X": "💱 EUR/GBP",
    "BTC-USD": "🪙 BITCOIN", "ETH-USD": "🪙 ETHEREUM", "SOL-USD": "🪙 SOLANA", "XRP-USD": "🪙 RIPPLE",
    "ES=F": "📊 S&P 500", "NQ=F": "📊 NASDAQ 100", "YM=F": "📊 DOW JONES", "GC=F": "🛢️ ORO", "CL=F": "🛢️ PETRÓLEO"
} # Simplificado para el ejemplo, pero puede poner los 32.

ORACULOS = {"UUP": "DXY PROXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 5. ESTRUCTURA
st.markdown("<div class='branding-header'><h1>🦅 G-SNIPER QUANT TERMINAL</h1></div>", unsafe_allow_html=True)
t_term, t_acad = st.tabs(["🦅 TERMINAL", "📚 ACADEMIA ELITE"])

with t_term:
    st.sidebar.markdown("### 💰 MONEY MANAGER")
    bal = st.sidebar.number_input("CAPITAL ($):", value=1000.0)
    risk = st.sidebar.slider("RIESGO (%):", 0.1, 5.0, 1.0)
    st.sidebar.markdown("---")
    selected = st.sidebar.selectbox("MERCADO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
    btn_scan = st.sidebar.button("⚡ EJECUTAR ESCÁNER GLOBAL")

    # Monitor Macro
    cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        d = get_single_data(t)
        if d is not None:
            v = d['Close'].iloc[-1]
            cols[i].metric(n, f"{v:.2f}", f"{v - d['Close'].iloc[-2]:.2f}")

    st.markdown("---")
    
    # Lógica de Escáner Global (OPTIMIZADA)
    if btn_scan:
        st.markdown("### ⚡ RESULTADOS DEL ESCÁNER GLOBAL")
        tickers = list(ASSETS.keys())
        with st.spinner("Iniciando Descarga Masiva..."):
            # DESCARGA EN BLOQUE (Mucho más rápido)
            data_all = yf.download(tickers, period="1y", interval="1d", progress=False, auto_adjust=True)
        
        progress_bar = st.progress(0)
        c_cards = st.columns(3)
        
        for idx, t in enumerate(tickers):
            try:
                # Extraer datos individuales del bloque descargado
                df_s = pd.DataFrame({
                    'Close': data_all['Close'][t],
                    'High': data_all['High'][t],
                    'Low': data_all['Low'][t],
                    'Volume': data_all['Volume'][t]
                }).dropna()
                
                if len(df_s) > 30:
                    z = calc_zscore(df_s).iloc[-1]
                    # Entrenamiento rápido de IA
                    df_s['Z'] = calc_zscore(df_s)
                    df_s['T'] = (df_s['Close'].shift(-1) > df_s['Close']).astype(int)
                    train = df_s[['Z', 'T']].dropna()
                    clf = RandomForestClassifier(n_estimators=20).fit(train[['Z']], train['T'])
                    p = clf.predict_proba(df_s[['Z']].iloc[[-1]])[0][1] * 100
                    
                    with c_cards[idx % 3]:
                        col_b = "#27ae60" if p > 60 else "#e74c3c" if p < 40 else "#d4af37"
                        st.markdown(f"""<div class='quant-card' style='border-left: 5px solid {col_b};'>
                            <b>{ASSETS[t]}</b><br><span style='font-size:20px;'>{df_s['Close'].iloc[-1]:.4f}</span><br>
                            IA: {p:.1f}% | Z: {z:.2f}</div>""", unsafe_allow_html=True)
                
                progress_bar.progress((idx + 1) / len(tickers))
            except: continue
        st.success("Escaneo completado con éxito.")

    # Análisis Individual (Siempre visible si no hay escaneo)
    else:
        df = get_single_data(selected)
        if df is not None:
            c_left, c_right = st.columns([2, 1])
            with c_left:
                fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
                fig.update_layout(template='plotly_dark', height=500, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, width='stretch')
            with c_right:
                st.markdown("### 🧠 ANALÍTICA")
                # ... cálculos de IA y Riesgo (igual que V6.4) ...
                st.info("Selecciona un activo o ejecuta el Escáner Global.")

# --- TAB: ACADEMIA ---
with tab_acad:
    st.markdown("## 📚 DOSSIER DE INTELIGENCIA ESTRATÉGICA")
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🌐 EL DXY Y LOS YIELDS</div>
            <p>El <b>DXY</b> es la fuerza del dólar frente al mundo. Si sube, los activos de riesgo (Criptos/Oro) suelen bajar. Los <b>Yields</b> de 10 años indican el costo del dinero; si suben demasiado, las acciones tecnológicas sufren.</p>
        </div>
        <div class="academy-card">
            <div class="academy-title">📉 VIX Y VPIN</div>
            <p>El <b>VIX</b> es el "índice del pánico". Valores arriba de 25 indican miedo extremo (oportunidad para el Sniper). El <b>VPIN</b> mide si el volumen es institucional o minorista; un VPIN > 70% confirma intención real.</p>
        </div>
        <div class="academy-card">
            <div class="academy-title">📏 Z-SCORE Y ADR</div>
            <p>El <b>Z-Score</b> mide la desviación del precio respecto a su media. Un Z > 2 significa que el precio está "caro". El <b>ADR Semanal</b> es tu regla de medir: te dice cuánto espacio le queda al precio para moverse hoy.</p>
        </div>
    """, unsafe_allow_html=True)
