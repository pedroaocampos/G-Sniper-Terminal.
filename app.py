# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V6.6 - ELITE STRIKE (OPTIMIZADO & FIABLE)
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

# 2. ESTÉTICA PREMIUM (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    .branding-header { text-align: center; padding: 15px; border-bottom: 2px solid #d4af37; margin-bottom: 25px; }
    .quant-card { background-color: #161b22; border: 1px solid #d4af37; padding: 15px; border-radius: 12px; margin-bottom: 10px; text-align: center; }
    .risk-box { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .academy-card { background: linear-gradient(145deg, #1e242c, #161b22); border-left: 5px solid #d4af37; padding: 25px; border-radius: 10px; margin-bottom: 20px; }
    .badge-buy { background-color: #27ae60; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES CORE
def calc_zscore(df, period=20):
    return (df['Close'] - df['Close'].rolling(window=period).mean()) / df['Close'].rolling(window=period).std()

def calc_adr_weekly(df):
    return (df['High'] - df['Low']).rolling(window=5).mean()

def calc_vpin(df, window=20):
    vpt = (df['Volume'] * (df['Close'].pct_change())).rolling(window=window).std()
    return (vpt / vpt.rolling(window=100).max()) * 100

@st.cache_data(ttl=600)
def get_data_safe(ticker):
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        return df if not df.empty else None
    except: return None

# 4. ARSENAL DE ÉLITE (12 ACTIVOS SELECCIONADOS)
ASSETS = {
    "EURUSD=X": "💱 EUR/USD", "GBPUSD=X": "💱 GBP/USD", "USDJPY=X": "💱 USD/JPY", 
    "AUDUSD=X": "💱 AUD/USD", "BTC-USD": "🪙 BITCOIN", "ETH-USD": "🪙 ETHEREUM", 
    "SOL-USD": "🪙 SOLANA", "ES=F": "📊 S&P 500", "NQ=F": "📊 NASDAQ 100", 
    "GC=F": "🛢️ ORO", "CL=F": "🛢️ PETRÓLEO", "SI=F": "🛢️ PLATA"
}

ORACULOS = {"UUP": "DXY PROXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 5. ESTRUCTURA
st.markdown("<div class='branding-header'><h1>🦅 G-SNIPER QUANT TERMINAL</h1><p style='color:#d4af37;'>ELITE STRIKE V6.6</p></div>", unsafe_allow_html=True)
tab_term, tab_acad = st.tabs(["🦅 TERMINAL", "📚 ACADEMIA ELITE"])

with tab_term:
    st.sidebar.markdown("### 💰 MONEY MANAGER")
    balance = st.sidebar.number_input("CAPITAL ($):", value=1000.0)
    risk_pct = st.sidebar.slider("RIESGO (%):", 0.1, 5.0, 1.0)
    st.sidebar.markdown("---")
    selected_ticker = st.sidebar.selectbox("ACTIVO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
    btn_scan = st.sidebar.button("⚡ ESCÁNER DE ÉLITE (12)")

    # Monitor Macro
    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data_safe(t)
        if df_o is not None:
            v = df_o['Close'].iloc[-1]
            m_cols[i].metric(n, f"{v:.2f}", f"{v - df_o['Close'].iloc[-2]:.2f}")

    st.markdown("---")

    if btn_scan:
        st.markdown("### ⚡ RESULTADOS DEL ESCUADRÓN DE ÉLITE")
        tickers = list(ASSETS.keys())
        with st.spinner("Sincronizando mercados..."):
            data_bulk = yf.download(tickers, period="1y", interval="1d", progress=False, auto_adjust=True)
        
        cols_cards = st.columns(3)
        for idx, t in enumerate(tickers):
            try:
                df_s = pd.DataFrame({'Close': data_bulk['Close'][t], 'High': data_bulk['High'][t], 'Low': data_bulk['Low'][t], 'Volume': data_bulk['Volume'][t]}).dropna()
                if len(df_s) > 30:
                    z = (df_s['Close'].iloc[-1] - df_s['Close'].rolling(20).mean().iloc[-1]) / df_s['Close'].rolling(20).std().iloc[-1]
                    with cols_cards[idx % 3]:
                        st.markdown(f"<div class='quant-card'><b>{ASSETS[t]}</b><br><span style='font-size:20px;'>{df_s['Close'].iloc[-1]:.4f}</span><br>Z-Score: {z:.2f}</div>", unsafe_allow_html=True)
            except: continue
        st.success("Escaneo completado.")

    else:
        df_f = get_data_safe(selected_ticker)
        if df_f is not None:
            c_l, c_r = st.columns([2.2, 1])
            with c_l:
                df_f['EMA20'] = df_f['Close'].ewm(span=20, adjust=False).mean()
                fig = go.Figure(data=[go.Candlestick(x=df_f.index, open=df_f['Open'], high=df_f['High'], low=df_f['Low'], close=df_f['Close'])])
                fig.add_trace(go.Scatter(x=df_f.index, y=df_f['EMA20'], mode='lines', line=dict(color='#d4af37', width=1.5), name="EMA 20"))
                fig.update_layout(template='plotly_dark', height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, width='stretch')
            with c_r:
                st.markdown("### 🧠 ANALÍTICA")
                z_act = (df_f['Close'].iloc[-1] - df_f['Close'].rolling(20).mean().iloc[-1]) / df_f['Close'].rolling(20).std().iloc[-1]
                adr_w = (df_f['High'] - df_f['Low']).rolling(5).mean().iloc[-1]
                
                st.metric("Z-SCORE", f"{z_act:.2f}")
                st.metric("ADR SEMANAL", f"{adr_w:.4f}")
                
                risk_u = balance * (risk_pct / 100)
                sl = adr_w * 0.75
                lot = risk_u / (sl * 100000) if "=" in selected_ticker else risk_u / sl
                
                st.markdown(f"<div class='risk-box'>Riesgo: ${risk_u:.2f}<br><b>Lotes/Unidades: {lot:.2f}</b></div>", unsafe_allow_html=True)

with tab_acad:
    st.markdown("## 📚 ACADEMIA G-SNIPER")
    st.markdown("""<div class="academy-card"><h4 style="color:#d4af37;">🦅 EL SINCROMECANISMO</h4><p>Nuestra terminal detecta la elasticidad del precio respecto a la EMA 20. El Z-Score cuantifica qué tan 'estirado' está el mercado para predecir la reversión.</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="academy-card"><h4 style="color:#d4af37;">📏 GESTIÓN DE RIESGO</h4><p>La calculadora de lotaje utiliza el ADR (Average Daily Range) para asegurarte de que tu Stop Loss sea técnico y no emocional.</p></div>""", unsafe_allow_html=True)
