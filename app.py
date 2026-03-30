# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V3.4 - EDICIÓN LINK-MASTER (CORRECCIÓN DE BUCLE)
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

# 2. ESTÉTICA BLACK EDITION (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    
    /* Tarjetas de Escáner */
    .quant-card {
        background-color: #161b22;
        border: 1px solid #d4af37;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    .quant-card:hover { border-color: #ffffff; transform: translateY(-3px); }

    /* Botones Premium */
    .stButton>button { 
        border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; 
        background-color: transparent; font-weight: bold; text-transform: uppercase;
    }
    .stButton>button:hover { background-color: #d4af37 !important; color: #0b0d11 !important; }
    
    /* Badges de Estado */
    .badge-buy { background-color: #27ae60; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    
    /* Estilo de Noticias (Flash News) */
    .news-container {
        border-left: 3px solid #d4af37;
        padding-left: 15px;
        margin-bottom: 20px;
        background: rgba(212, 175, 55, 0.05);
        padding: 10px;
        border-radius: 0 10px 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ARSENAL COMPLETO (32 ACTIVOS)
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

ORACULOS = {"DX-Y.NYB": "DXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

@st.cache_data(ttl=300)
def get_data(ticker, p="1y"):
    try:
        df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
        if not df.empty and isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        return df
    except: return None

# 4. CABECERA
st.title("🦅 G-SNIPER QUANT TERMINAL")
c_h1, c_h2 = st.columns([2, 1])
with c_h1:
    st.caption(f"SINCROMECANISMO: {datetime.now(pytz.timezone('America/New_York')).strftime('%d-%b-%Y %H:%M:%S')} NYT")
with c_h2:
    st.markdown("<div style='text-align: right;'><span class='badge-buy'>SISTEMA OPERATIVO 🟢</span></div>", unsafe_allow_html=True)

st.markdown("---")

# 5. SIDEBAR
st.sidebar.markdown("### 🎯 PANEL DE CONTROL")
selected_ticker = st.sidebar.selectbox("SELECCIONAR MERCADO (32):", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
scan_global = st.sidebar.button("⚡ ESCANEAR ARSENAL GLOBAL")

# 6. MONITORES MACRO
m_cols = st.columns(3)
for i, (t, n) in enumerate(ORACULOS.items()):
    df_o = get_data(t, "5d")
    if df_o is not None and not df_o.empty:
        val = float(df_o['Close'].iloc[-1])
        prev = float(df_o['Close'].iloc[-2]) if len(df_o)>1 else val
        m_cols[i].metric(n, f"{val:.2f}", f"{val-prev:.2f}")

st.markdown("---")

# 7. FOCO TÁCTICO
col_graf, col_ia = st.columns([2, 1])
df_foco = get_data(selected_ticker, "6mo")

if df_foco is not None and not df_foco.empty:
    with col_graf:
        st.markdown(f"### 🔭 GRÁFICO PROFESIONAL: {ASSETS[selected_ticker]}")
        fig = go.Figure(data=[go.Candlestick(x=df_foco.index, open=df_foco['Open'], high=df_foco['High'], low=df_foco['Low'], close=df_foco['Close'], increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
        fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_ia:
        st.markdown("### 🧠 ANALÍTICA IA")
        df_foco['EMA20'] = df_foco['Close'].ewm(span=20, adjust=False).mean()
        df_foco['Z'] = (df_foco['Close'] - df_foco['EMA20']) / df_foco['Close'].rolling(20).std().replace(0, 0.001)
        df_foco['Target'] = (df_foco['Close'].shift(-1) > df_foco['Close']).astype(int)
        train = df_foco[['Z', 'Target']].dropna()
        model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
        prob = float(model.predict_proba(df_foco[['Z']].iloc[[-1]])[0][1] * 100)
        
        st.markdown(f"<div class='quant-card'><h1 style='color: white !important; text-align:center;'>{prob:.1f}%</h1><p style='text-align:center; color:#d4af37;'>CONFIANZA PREDICTIVA</p></div>", unsafe_allow_html=True)
        
        if prob > 60: st.markdown("<div style='text-align:center'><span class='badge-buy'>🔥 EJECUTAR COMPRA</span></div>", unsafe_allow_html=True)
        elif prob < 40: st.markdown("<div style='text-align:center'><span class='badge-sell'>🔴 EJECUTAR VENTA</span></div>", unsafe_allow_html=True)
        else: st.markdown("<div style='text-align:center'><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 📰 FLASH NEWS (EXTERNAL)")
        
        # MÓDULO DE NOTICIAS CORREGIDO
        try:
            ticker_obj = yf.Ticker(selected_ticker)
            news_items = ticker_obj.news[:3]
            if news_items:
                for item in news_items:
                    title = item.get('title', 'Noticia importante')
                    link = item.get('link', '')
                    
                    # VALIDACIÓN DE ENLACE: Si el enlace no empieza con http, lo ignoramos o corregimos
                    if link.startswith('http'):
                        st.markdown(f"""
                        <div class="news-container">
                            <a href="{link}" target="_blank" style="text-decoration:none; color:#bdc3c7; font-size:14px;">
                                <b>{title}</b><br>
                                <span style="color:#d4af37; font-size:11px;">VER REPORTE EXTERNO ↗</span>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No se detectan noticias externas para este activo.")
        except:
            st.caption("Radar de noticias temporalmente inaccesible.")

# 8. ESCÁNER GLOBAL
if scan_global:
    st.markdown("---")
    st.markdown("### ⚡ MATRIZ GLOBAL (32 ACTIVOS)")
    st.info("Analizando el arsenal completo...")
    cols = st.columns(3)
    idx = 0
    with st.spinner("Entrenando modelos neuronales..."):
        for t, name in ASSETS.items():
            df = get_data(t, "1y")
            if df is not None and len(df) > 50:
                df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
                df['Z'] = (df['Close'] - df['EMA20']) / df['Close'].rolling(20).std().replace(0, 0.001)
                df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
                train = df[['Z', 'Target']].dropna()
                model = RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
                p_ia = float(model.predict_proba(df[['Z']].iloc[[-1]])[0][1] * 100)
                
                with cols[idx % 3]:
                    c_b = "#27ae60" if p_ia > 60 else "#e74c3c" if p_ia < 40 else "#d4af37"
                    b_cl = "badge-buy" if p_ia > 60 else "badge-sell" if p_ia < 40 else "badge-wait"
                    st.markdown(f"""
                    <div class='quant-card' style='border-left: 5px solid {c_b};'>
                        <h4 style='margin-bottom:0;'>{name}</h4>
                        <p style='color:white; font-size:18px; margin:5px 0;'><b>{df['Close'].iloc[-1]:.4f}</b></p>
                        <span class='{b_cl}'>IA: {p_ia:.1f}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                idx += 1
