# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V6.2 - ELITE DOSSIER (ACADEMIA COMPLETA)
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
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

# 2. ESTÉTICA PREMIUM (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    .branding-header { text-align: center; padding: 15px; border-bottom: 2px solid #d4af37; margin-bottom: 25px; }
    .quant-card { background-color: #161b22; border: 1px solid #d4af37; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; }
    .risk-box { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-top: 10px; }
    
    /* ACADEMIA STYLE */
    .academy-card { 
        background: linear-gradient(145deg, #1e242c, #161b22); 
        border-left: 5px solid #d4af37; 
        padding: 30px; 
        border-radius: 12px; 
        margin-bottom: 30px; 
        box-shadow: 10px 10px 25px rgba(0,0,0,0.7);
    }
    .academy-title { color: #d4af37; font-size: 26px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid rgba(212,175,55,0.3); padding-bottom: 10px; }
    .academy-text { color: #bdc3c7; line-height: 1.8; font-size: 18px; }
    .pro-tip { background-color: rgba(212, 175, 55, 0.15); padding: 15px; border-radius: 8px; border: 1px dashed #d4af37; margin-top: 15px; color: #ffffff; font-weight: 500; }
    .formula { background-color: #000000; padding: 12px; border-radius: 6px; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 15px 0; border: 1px solid #333; }

    .badge-buy { background-color: #27ae60; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    
    .stButton>button { border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #d4af37 !important; color: #0b0d11 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR QUANT (Z-SCORE, VPIN, ADR)
def calc_zscore(df, period=20):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    return (df['Close'] - sma) / std

def calc_adr_weekly(df):
    return (df['High'] - df['Low']).rolling(window=5).mean()

def calc_vpin_proxy(df, window=20):
    vpt = (df['Volume'] * (df['Close'].pct_change())).rolling(window=window).std()
    return (vpt / vpt.rolling(window=100).max()) * 100

@st.cache_data(ttl=600)
def get_data_safe(ticker, p="1y"):
    for i in range(3):
        try:
            time.sleep(random.uniform(0.5, 1.2))
            df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                return df
        except: time.sleep(1.5)
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

# 5. BRANDING & TABS
st.markdown("""<div class='branding-header'><h1>🦅 G-SNIPER QUANT TERMINAL</h1><p style='color:#d4af37; letter-spacing: 5px; font-weight:bold;'>EDICIÓN ELITE V6.2</p></div>""", unsafe_allow_html=True)
tab_term, tab_acad = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA G-SNIPER"])

# --- TAB: TERMINAL ---
with tab_term:
    st.sidebar.markdown("### 💰 GESTIÓN DE CAPITAL")
    balance = st.sidebar.number_input("CAPITAL ($):", min_value=100.0, value=1000.0)
    risk_p = st.sidebar.slider("RIESGO (%):", 0.1, 5.0, 1.0)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 MERCADO")
    selected = st.sidebar.selectbox("ACTIVO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
    scan = st.sidebar.button("⚡ ESCÁNER GLOBAL")

    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data_safe(t, "5d")
        if df_o is not None:
            val = float(df_o['Close'].iloc[-1])
            m_cols[i].metric(n, f"{val:.2f}", f"{val - float(df_o['Close'].iloc[-2]):.2f}")
        else: m_cols[i].caption(f"{n}\n(Syncing...)")

    st.markdown("---")
    c_graf, c_ia = st.columns([2.2, 1])
    df = get_data_safe(selected, "1y")

    if df is not None:
        with c_graf:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
            fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, width='stretch')

        with c_ia:
            st.markdown("### 🧠 ANALÍTICA QUANT")
            df['Z'] = calc_zscore(df); df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            train = df[['Z', 'Target']].dropna()
            model = RandomForestClassifier(n_estimators=50, max_depth=5).fit(train[['Z']], train['Target'])
            prob = float(model.predict_proba(df[['Z']].iloc[[-1]])[0][1] * 100)
            
            st.markdown(f"<div class='quant-card'><h1 style='color:white; margin:0;'>{prob:.1f}%</h1><p style='color:#d4af37;'>PROBABILIDAD IA</p></div>", unsafe_allow_html=True)
            
            z_act = df['Z'].iloc[-1]; adr_w = calc_adr_weekly(df).iloc[-1]; vpin_val = calc_vpin_proxy(df).iloc[-1]
            
            # --- LIMPIEZA "YAYA" -> FLUJO VPIN ---
            cx, cy = st.columns(2)
            cx.metric("Z-SCORE (DS)", f"{z_act:.2f}")
            cx.metric("FLUJO VPIN", f"{vpin_val:.1f}%") # CORREGIDO
            fmt = ".4f" if "=" in selected else ".2f"
            cy.metric("ADR SEMANAL", f"{adr_w:{fmt}}")
            cy.metric("ESTADO", "REVERSIÓN" if abs(z_act) > 2.2 else "ESTABLE")

            risk_u = balance * (risk_p / 100); sl = adr_w * 0.75
            lot = risk_u / (sl * 100000) if "=" in selected else risk_u / sl
            st.markdown(f"<div class='risk-box'><p style='margin:0;'>Arriesgar: <b>${risk_u:.2f}</b> | SL: <b>{sl:.4f}</b></p><p style='color:#d4af37; font-size:18px; margin:5px 0;'><b>LOTES: {lot:.2f}</b></p></div>", unsafe_allow_html=True)

            if prob > 62: st.markdown("<center><span class='badge-buy'>🔥 ACUMULACIÓN: COMPRA</span></center>", unsafe_allow_html=True)
            elif prob < 38: st.markdown("<center><span class='badge-sell'>🔴 DISTRIBUCIÓN: VENTA</span></center>", unsafe_allow_html=True)
            else: st.markdown("<center><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></center>", unsafe_allow_html=True)

# --- TAB: ACADEMIA ---
with tab_acad:
    st.markdown("## 📚 DOSSIER DE INTELIGENCIA ESTRATÉGICA")
    
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🦅 MÓDULO 1: EL SINCROMECANISMO</div>
            <div class="academy-text">
                El corazón de G-SNIPER es el <b>Sincromecanismo</b>. A diferencia de los indicadores basura, este sistema mide la elasticidad del precio respecto a la EMA 20. Cuando el precio se "estira" demasiado, el sistema detecta una inminente regresión al promedio.
            </div>
            <div class="pro-tip">💡 <b>REGLA DE ORO:</b> Si el precio está lejos de la EMA y la IA confirma, el "elástico" está a punto de romperse.</div>
        </div>

        <div class="academy-card">
            <div class="academy-title">🧠 MÓDULO 2: ORÁCULO IA (RANDOM FOREST)</div>
            <div class="academy-text">
                Nuestra IA entrena 50 árboles de decisión en tiempo real cada vez que seleccionas un activo. Analiza la estructura de volatilidad del último año para clasificar el momento actual.
            </div>
            <div class="formula">Confianza = (Árboles a favor / 50) * 100</div>
            <div class="pro-tip">💡 <b>UMBRALES:</b> No operes nada por debajo del 60% de probabilidad.</div>
        </div>

        <div class="academy-card">
            <div class="academy-title">📉 MÓDULO 3: Z-SCORE (GPS ESTADÍSTICO)</div>
            <div class="academy-text">
                El Z-Score nos dice cuántas <b>Desviaciones Estándar</b> se ha movido el precio. Es la herramienta definitiva para cazar techos y suelos.
            </div>
            <div class="formula">Z = (Precio Actual - Media) / Desviación Estándar</div>
            <div class="academy-text">
                • <b>Z > +2.0:</b> Mercado sobrecomprado (Busca Ventas).<br>
                • <b>Z < -2.0:</b> Mercado sobrevendido (Busca Compras).
            </div>
        </div>

        <div class="academy-card">
            <div class="academy-title">🔥 MÓDULO 4: FLUJO VPIN (VOLUMEN INFORMADO)</div>
            <div class="academy-text">
                El <b>VPIN</b> (Volume Probability of Informed Trading) separa el ruido minorista del dinero institucional. Un VPIN alto indica que los "Market Makers" están posicionados.
            </div>
            <div class="pro-tip">💡 <b>INSTITUCIONAL:</b> Si el VPIN supera el 70%, el movimiento tiene gasolina real.</div>
        </div>

        <div class="academy-card">
            <div class="academy-title">📏 MÓDULO 5: ADR SEMANAL & MONEY MANAGER</div>
            <div class="academy-text">
                El <b>Average Daily Range (ADR)</b> mide la zancada del mercado. Si el ADR semanal está agotado, no entres. Nuestra calculadora usa el ADR para poner un Stop Loss que las instituciones no puedan barrer.
            </div>
            <div class="pro-tip">💡 <b>GESTIÓN:</b> Deja que la terminal calcule tu lotaje. La supervivencia es la base de la riqueza.</div>
        </div>
    """, unsafe_allow_html=True)
