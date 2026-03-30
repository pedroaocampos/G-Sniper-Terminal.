# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V5.2 - EDICIÓN STEALTH & ROBUST (ANTI-LIMIT)
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

# 1. CONFIGURACIÓN DE PÁGINA (ESTÁNDAR 2026)
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

# 2. ESTÉTICA PREMIUM (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    .quant-card { background-color: #161b22; border: 1px solid #d4af37; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; }
    .academy-card { background: linear-gradient(145deg, #1e242c, #161b22); border-left: 5px solid #d4af37; padding: 25px; border-radius: 10px; margin-bottom: 20px; }
    .badge-buy { background-color: #27ae60; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .stButton>button { border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; background-color: transparent; font-weight: bold; }
    .stButton>button:hover { background-color: #d4af37 !important; color: #0b0d11 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES QUANT MEJORADAS (CON MANEJO DE ERRORES)
def calc_zscore(df, period=20):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    return (df['Close'] - sma) / std

def calc_adr_weekly(df):
    return (df['High'] - df['Low']).rolling(window=5).mean()

def calc_vpin_proxy(df, window=20):
    vpt = (df['Volume'] * (df['Close'].pct_change())).rolling(window=window).std()
    return (vpt / vpt.rolling(window=100).max()) * 100

@st.cache_data(ttl=600) # Aumentamos cache a 10 min para evitar bloqueos
def get_data_safe(ticker, p="1y"):
    try:
        time.sleep(0.2) # Pequeña pausa stealth para no saturar la API
        df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
        if not df.empty and isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        return df if not df.empty else None
    except Exception as e:
        return None

# 4. ARSENAL (32 ACTIVOS)
ASSETS = {
    "EURUSD=X": "💱 EUR/USD", "GBPUSD=X": "💱 GBP/USD", "USDJPY=X": "💱 USD/JPY", "USDCHF=X": "💱 USD/CHF",
    "AUDUSD=X": "💱 AUD/USD", "USDCAD=X": "💱 USD/CAD", "NZDUSD=X": "💱 NZD/USD", "EURGBP=X": "💱 EUR/GBP",
    "EURJPY=X": "💱 EUR/JPY", "GBPJPY=X": "💱 GBP/JPY", "AUDJPY=X": "💱 AUD/JPY", "EURCHF=X": "💱 EUR/CHF",
    "BTC-USD": "🪙 BITCOIN", "ETH-USD": "🪙 ETHEREUM", "SOL-USD": "🪙 SOLANA", "XRP-USD": "🪙 RIPPLE",
    "ADA-USD": "🪙 CARDANO", "DOGE-USD": "🪙 DOGECOIN", "BNB-USD": "🪙 BINANCE COIN", "LINK-USD": "🪙 CHAINLINK",
    "ES=F": "📊 S&P 500", "NQ=F": "📊 NASDAQ 100", "YM=F": "📊 DOW JONES", "RTY=F": "📊 RUSSELL 2000",
    "^GDAXI": "📊 DAX 40", "^FTSE": "📊 FTSE 100", "^N225": "📊 NIKKEI 225",
    "GC=F": "🛢️ ORO", "SI=F": "🛢️ PLATA", "CL=F": "🛢️ PETRÓLEO", "NG=F": "🛢️ GAS NATURAL", "HG=F": "🛢️ COBRE"
}

ORACULOS = {"UUP": "DXY PROXY (USD) 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 5. ESTRUCTURA
st.title("🦅 G-SNIPER QUANT TERMINAL")
tab_terminal, tab_academia = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA G-SNIPER"])

with tab_terminal:
    st.sidebar.markdown("### 🎯 PANEL DE CONTROL")
    selected_ticker = st.sidebar.selectbox("SELECCIONAR MERCADO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
    scan_global = st.sidebar.button("⚡ ESCANEAR ARSENAL GLOBAL")

    # Oráculos con manejo de error por Rate Limit
    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data_safe(t, "5d")
        if df_o is not None and not df_o.empty:
            val = float(df_o['Close'].iloc[-1])
            prev = float(df_o['Close'].iloc[-2]) if len(df_o)>1 else val
            m_cols[i].metric(n, f"{val:.2f}", f"{val-prev:.2f}")
        else:
            m_cols[i].error(f"{n} Offline")

    st.markdown("---")
    col_graf, col_ia = st.columns([2, 1])
    df_foco = get_data_safe(selected_ticker, "1y")

    if df_foco is not None and not df_foco.empty:
        with col_graf:
            st.markdown(f"### 🔭 MONITOR TÁCTICO: {ASSETS[selected_ticker]}")
            fig = go.Figure(data=[go.Candlestick(x=df_foco.index, open=df_foco['Open'], high=df_foco['High'], low=df_foco['Low'], close=df_foco['Close'], increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
            fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, width='stretch') # ACTUALIZACIÓN SINTAXIS 2026

        with col_ia:
            st.markdown("### 🧠 ANALÍTICA INSTITUCIONAL")
            df_foco['Z'] = calc_zscore(df_foco)
            df_foco['Target'] = (df_foco['Close'].shift(-1) > df_foco['Close']).astype(int)
            train = df_foco[['Z', 'Target']].dropna()
            
            if len(train) > 10:
                model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
                prob = float(model.predict_proba(df_foco[['Z']].iloc[[-1]])[0][1] * 100)
                st.markdown(f"<div class='quant-card'><h1 style='color: white !important; margin-bottom:0;'>{prob:.1f}%</h1><p style='color:#d4af37;'>PROBABILIDAD IA</p></div>", unsafe_allow_html=True)
                
                z_actual = df_foco['Z'].iloc[-1]
                adr_w = calc_adr_weekly(df_foco).iloc[-1]
                vpin = calc_vpin_proxy(df_foco).iloc[-1]
                
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Z-SCORE (DS)", f"{z_actual:.2f}")
                    st.metric("FLUJO VPIN", f"{vpin:.1f}%")
                with c2:
                    fmt = ".4f" if "USD" in selected_ticker or "=" in selected_ticker else ".2f"
                    st.metric("ADR SEMANAL", f"{adr_w:{fmt}}")
                    if abs(z_actual) > 2.2: st.warning("REVERSIÓN")
                    else: st.success("ESTABLE")

                st.markdown("---")
                if prob > 62: st.markdown("<div style='text-align:center'><span class='badge-buy'>🔥 ACUMULACIÓN: EJECUTAR COMPRA</span></div>", unsafe_allow_html=True)
                elif prob < 38: st.markdown("<div style='text-align:center'><span class='badge-sell'>🔴 DISTRIBUCIÓN: EJECUTAR VENTA</span></div>", unsafe_allow_html=True)
                else: st.markdown("<div style='text-align:center'><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></div>", unsafe_allow_html=True)

    if scan_global:
        st.markdown("---")
        st.markdown("### ⚡ MATRIZ GLOBAL (32 ACTIVOS)")
        cols = st.columns(3)
        idx = 0
        with st.spinner("Procesando arsenal con protocolo Stealth..."):
            for t, name in ASSETS.items():
                df = get_data_safe(t, "1y")
                if df is not None and len(df) > 50:
                    df['Z'] = calc_zscore(df)
                    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
                    train = df[['Z', 'Target']].dropna()
                    model = RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
                    p_ia = float(model.predict_proba(df[['Z']].iloc[[-1]])[0][1] * 100)
                    with cols[idx % 3]:
                        c_b = "#27ae60" if p_ia > 60 else "#e74c3c" if p_ia < 40 else "#d4af37"
                        b_cl = "badge-buy" if p_ia > 60 else "badge-sell" if p_ia < 40 else "badge-wait"
                        st.markdown(f"<div class='quant-card' style='border-left: 5px solid {c_b};'><h4>{name}</h4><p style='color:white; font-size:18px;'><b>{df['Close'].iloc[-1]:.4f}</b></p><span class='{b_cl}'>IA: {p_ia:.1f}%</span></div>", unsafe_allow_html=True)
                    idx += 1

with tab_academia:
    st.markdown("### 📚 MANUAL DE OPERACIONES TÁCTICAS")
    st.markdown("""<div class="academy-card"><h4 style="color:#d4af37;">📊 ACUMULACIÓN VS DISTRIBUCIÓN</h4><p>En el trading institucional, no hablamos de simple compra o venta. <b>Acumulación:</b> Las ballenas compran sin mover el precio. <b>Distribución:</b> Las instituciones sueltan sus posiciones al público.</p></div>""", unsafe_allow_html=True)
