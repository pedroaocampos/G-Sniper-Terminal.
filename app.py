# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V7.0 - MINDSET & QUANT EDITION (32 ASSETS)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import time
import random

# 1. CONFIGURACIÓN
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

# 2. CSS PREMIUM
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    .branding-header { text-align: center; padding: 20px; border-bottom: 2px solid #d4af37; margin-bottom: 25px; }
    .quant-card { background-color: #161b22; border: 1px solid #d4af37; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; }
    .risk-box { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .academy-card { background: linear-gradient(145deg, #1e242c, #161b22); border-left: 5px solid #d4af37; padding: 30px; border-radius: 10px; margin-bottom: 25px; }
    .badge-buy { background-color: #27ae60; color: white; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    .badge-lock { background-color: #555; color: #999; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES QUANT
@st.cache_data(ttl=300)
def get_data_safe(ticker):
    try:
        time.sleep(random.uniform(0.3, 0.7))
        df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            return df
    except: return None
    return None

def calc_zscore(df, period=20):
    return (df['Close'] - df['Close'].rolling(window=period).mean()) / df['Close'].rolling(window=period).std()

def calc_vpin(df, window=20):
    vpt = (df['Volume'] * (df['Close'].pct_change())).rolling(window=window).std()
    return (vpt / vpt.rolling(window=100).max()) * 100

# 4. ARSENAL COMPLETO (32 ACTIVOS)
ASSETS = {
    "EURUSD=X": "💱 EUR/USD", "GBPUSD=X": "💱 GBP/USD", "USDJPY=X": "💱 USD/JPY", "USDCHF=X": "💱 USD/CHF",
    "AUDUSD=X": "💱 AUD/USD", "USDCAD=X": "💱 USD/CAD", "NZDUSD=X": "💱 NZD/USD", "EURGBP=X": "💱 EUR/GBP",
    "BTC-USD": "🪙 BITCOIN", "ETH-USD": "🪙 ETHEREUM", "SOL-USD": "🪙 SOLANA", "XRP-USD": "🪙 RIPPLE",
    "ADA-USD": "🪙 CARDANO", "BNB-USD": "🪙 BINANCE", "LINK-USD": "🪙 CHAINLINK", "DOT-USD": "🪙 POLKADOT",
    "ES=F": "📊 S&P 500", "NQ=F": "📊 NASDAQ 100", "YM=F": "📊 DOW JONES", "RTY=F": "📊 RUSSELL 2000",
    "^GDAXI": "📊 DAX 40", "^FTSE": "📊 FTSE 100", "^N225": "📊 NIKKEI 225", "GC=F": "🛢️ ORO",
    "SI=F": "🛢️ PLATA", "CL=F": "🛢️ PETRÓLEO", "NG=F": "🛢️ GAS NATURAL", "HG=F": "🛢️ COBRE",
    "AAPL": "🍎 APPLE", "TSLA": "⚡ TESLA", "NVDA": "🤖 NVIDIA", "AMZN": "📦 AMAZON"
}
ORACULOS = {"UUP": "DXY PROXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 5. HEADER
st.markdown("""<div class='branding-header'><h1>🦅 G-SNIPER QUANT TERMINAL</h1><p style='color:#d4af37; letter-spacing: 5px; font-weight:bold;'>MINDSET & QUANT V7.0</p></div>""", unsafe_allow_html=True)

tab_term, tab_acad = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA ELITE"])

with tab_term:
    # --- SIDEBAR: PSICOLOGÍA Y GESTIÓN ---
    st.sidebar.markdown("### 🧠 CHECKLIST DEL SNIPER")
    q1 = st.sidebar.checkbox("¿He dormido bien y estoy enfocado?")
    q2 = st.sidebar.checkbox("¿Acepto que hoy puedo perder dinero?")
    q3 = st.sidebar.checkbox("¿Mi riesgo está bajo control?")
    q4 = st.sidebar.checkbox("¿He revisado noticias macro?")
    q5 = st.sidebar.checkbox("¿Estoy operando sin revancha?")
    q6 = st.sidebar.checkbox("¿El activo está en zona EMA 20?")
    q7 = st.sidebar.checkbox("¿Respetaré mi Take Profit?")
    
    psico_ready = all([q1, q2, q3, q4, q5, q6, q7])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💰 GESTIÓN DE CAPITAL")
    balance = st.sidebar.number_input("CAPITAL ($):", value=1000.0)
    risk_p = st.sidebar.slider("RIESGO (%):", 0.1, 5.0, 1.0)
    st.sidebar.markdown("---")
    selected = st.sidebar.selectbox("ACTIVO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])

    # Monitor Macro
    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data_safe(t)
        if df_o is not None:
            v = df_o['Close'].iloc[-1]
            m_cols[i].metric(n, f"{v:.2f}", f"{v - df_o['Close'].iloc[-2]:.2f}")
        else: m_cols[i].caption(f"{n}\n(Sync...)")

    st.markdown("---")
    
    df_f = get_data_safe(selected)
    if df_f is not None:
        c_l, c_r = st.columns([2.2, 1])
        with c_l:
            df_f['EMA20'] = df_f['Close'].ewm(span=20, adjust=False).mean()
            fig = go.Figure(data=[go.Candlestick(x=df_f.index, open=df_f['Open'], high=df_f['High'], low=df_f['Low'], close=df_f['Close'], name="Precio")])
            fig.add_trace(go.Scatter(x=df_f.index, y=df_f['EMA20'], mode='lines', line=dict(color='#d4af37', width=1.5), name="EMA 20"))
            fig.update_layout(template='plotly_dark', height=500, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with c_r:
            st.markdown("### 🧠 ANALÍTICA QUANT")
            z_act = calc_zscore(df_f).iloc[-1]
            adr_w = (df_f['High'] - df_f['Low']).rolling(5).mean().iloc[-1]
            vpin_val = calc_vpin(df_f).iloc[-1]
            
            st.metric("Z-SCORE (DS)", f"{z_act:.2f}")
            st.metric("FLUJO VPIN", f"{vpin_val:.1f}%")
            fmt = ".4f" if "=" in selected else ".2f"
            st.metric("ADR SEMANAL", f"{adr_w:{fmt}}")
            
            risk_u = balance * (risk_p / 100); sl = adr_w * 0.75
            lot = risk_u / (sl * 100000) if "=" in selected else risk_u / sl
            st.markdown(f"<div class='risk-box'>Riesgo: <b>${risk_u:.2f}</b> | SL: <b>{sl:.4f}</b><br><span style='font-size:18px; color:#d4af37;'>LOTES: {lot:.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            if not psico_ready:
                st.markdown("<center><span class='badge-lock'>🛡️ ANALÍTICA BLOQUEADA: REVISAR CHECKLIST</span></center>", unsafe_allow_html=True)
            else:
                if z_act < -2.2: st.markdown("<center><span class='badge-buy'>🔥 ACUMULACIÓN: COMPRA</span></center>", unsafe_allow_html=True)
                elif z_act > 2.2: st.markdown("<center><span class='badge-sell'>🔴 DISTRIBUCIÓN: VENTA</span></center>", unsafe_allow_html=True)
                else: st.markdown("<center><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></center>", unsafe_allow_html=True)

with tab_acad:
    st.markdown("## 📚 ACADEMIA G-SNIPER ELITE")
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🧠 PSICOLOGÍA DEL SNIPER</div>
            <p>El 90% del trading es mental. El <b>Checklist Táctico</b> de la barra lateral no es opcional. Un Sniper no dispara porque tiene una bala; dispara porque todas las condiciones (mentales y técnicas) están alineadas.</p>
        </div>
        <div class="academy-card">
            <div class="academy-title">🦅 EL SINCROMECANISMO (EMA 20)</div>
            <p>Referencia institucional de equilibrio. La distancia entre el precio y la EMA 20 (medida por el Z-Score) es nuestra principal ventaja estadística.</p>
        </div>
    """, unsafe_allow_html=True)
