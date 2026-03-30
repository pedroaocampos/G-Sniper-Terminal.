# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V6.8 - EDICIÓN ANTI-BLOCK (ACADEMIA FULL)
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
    .branding-header { text-align: center; padding: 20px; border-bottom: 2px solid #d4af37; margin-bottom: 25px; }
    .quant-card { background-color: #161b22; border: 1px solid #d4af37; padding: 15px; border-radius: 12px; margin-bottom: 10px; text-align: center; }
    .risk-box { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-top: 10px; }
    
    /* ACADEMIA STYLE */
    .academy-card { background: linear-gradient(145deg, #1e242c, #161b22); border-left: 5px solid #d4af37; padding: 30px; border-radius: 10px; margin-bottom: 25px; }
    .academy-title { color: #d4af37; font-size: 24px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid rgba(212,175,55,0.2); }
    .formula { background-color: #000000; padding: 12px; border-radius: 6px; color: #00ff00; font-family: monospace; text-align: center; margin: 15px 0; }

    /* Badges */
    .badge-buy { background-color: #27ae60; color: white; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    
    .stButton>button { border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; font-weight: bold; height: 50px; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES QUANT CON PROTECCIÓN ANTI-BLOQUEO
@st.cache_data(ttl=600)
def get_data_safe(ticker, p="1y"):
    """Descarga datos con reintento para evitar Rate Limits."""
    for i in range(2):
        try:
            time.sleep(random.uniform(0.5, 1.2)) # Evasión de bot
            df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
                return df
        except: time.sleep(2)
    return None

def calc_zscore(df, period=20):
    return (df['Close'] - df['Close'].rolling(window=period).mean()) / df['Close'].rolling(window=period).std()

def calc_vpin(df, window=20):
    vpt = (df['Volume'] * (df['Close'].pct_change())).rolling(window=window).std()
    return (vpt / vpt.rolling(window=100).max()) * 100

# 4. ARSENAL (12 ACTIVOS DE ÉLITE)
ASSETS = {
    "EURUSD=X": "💱 EUR/USD", "GBPUSD=X": "💱 GBP/USD", "USDJPY=X": "💱 USD/JPY", 
    "BTC-USD": "🪙 BITCOIN", "ETH-USD": "🪙 ETHEREUM", "SOL-USD": "🪙 SOLANA",
    "ES=F": "📊 S&P 500", "NQ=F": "📊 NASDAQ 100", "YM=F": "📊 DOW JONES",
    "GC=F": "🛢️ ORO", "CL=F": "🛢️ PETRÓLEO", "SI=F": "🛢️ PLATA"
}
ORACULOS = {"UUP": "DXY PROXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 5. ESTRUCTURA DE PANTALLA
st.markdown("""<div class='branding-header'><h1>🦅 G-SNIPER QUANT TERMINAL</h1><p style='color:#d4af37; letter-spacing: 5px; font-weight:bold;'>EDICIÓN ELITE V6.8</p></div>""", unsafe_allow_html=True)

t_term, t_acad = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA ELITE"])

with t_term:
    # --- PANEL LATERAL ---
    st.sidebar.markdown("### 💰 MONEY MANAGER")
    balance = st.sidebar.number_input("CAPITAL ($):", value=1000.0)
    risk_p = st.sidebar.slider("RIESGO POR OPERACIÓN (%):", 0.1, 5.0, 1.0)
    st.sidebar.markdown("---")
    selected = st.sidebar.selectbox("ACTIVO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
    btn_scan = st.sidebar.button("⚡ ESCÁNER GLOBAL")

    # Monitor Macro (Blindado)
    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data_safe(t, "5d")
        if df_o is not None:
            v = df_o['Close'].iloc[-1]
            m_cols[i].metric(n, f"{v:.2f}", f"{v - df_o['Close'].iloc[-2]:.2f}")
        else:
            m_cols[i].caption(f"{n}\n(Sincronizando...)")

    st.markdown("---")

    if btn_scan:
        st.markdown("### ⚡ RESULTADOS DE LA MATRIZ (12 ACTIVOS)")
        tickers = list(ASSETS.keys())
        with st.spinner("Ejecutando algoritmos neuronales..."):
            data_bulk = yf.download(tickers, period="1y", interval="1d", progress=False, auto_adjust=True)
        
        c_cards = st.columns(3)
        for idx, t in enumerate(tickers):
            try:
                df_s = pd.DataFrame({'Close': data_bulk['Close'][t]}).dropna()
                z = (df_s['Close'].iloc[-1] - df_s['Close'].rolling(20).mean().iloc[-1]) / df_s['Close'].rolling(20).std().iloc[-1]
                with c_cards[idx % 3]:
                    st.markdown(f"<div class='quant-card'><b>{ASSETS[t]}</b><br><span style='font-size:20px;'>{df_s['Close'].iloc[-1]:.4f}</span><br>Z-Score: {z:.2f}</div>", unsafe_allow_html=True)
            except: continue
    else:
        df_f = get_data_safe(selected)
        if df_f is not None:
            c_l, c_r = st.columns([2.2, 1])
            with c_l:
                df_f['EMA20'] = df_f['Close'].ewm(span=20, adjust=False).mean()
                fig = go.Figure(data=[go.Candlestick(x=df_f.index, open=df_f['Open'], high=df_f['High'], low=df_f['Low'], close=df_f['Close'], name="Precio")])
                fig.add_trace(go.Scatter(x=df_f.index, y=df_f['EMA20'], mode='lines', line=dict(color='#d4af37', width=1.5), name="Sincromecanismo (EMA 20)"))
                fig.update_layout(template='plotly_dark', height=500, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, width='stretch')
            
            with c_r:
                st.markdown("### 🧠 ANALÍTICA QUANT")
                z_act = (df_f['Close'].iloc[-1] - df_f['Close'].rolling(20).mean().iloc[-1]) / df_f['Close'].rolling(20).std().iloc[-1]
                adr_w = (df_f['High'] - df_f['Low']).rolling(5).mean().iloc[-1]
                vpin_val = calc_vpin(df_f).iloc[-1]
                
                st.metric("Z-SCORE (DS)", f"{z_act:.2f}")
                st.metric("FLUJO VPIN", f"{vpin_val:.1f}%")
                fmt = ".4f" if "=" in selected else ".2f"
                st.metric("ADR SEMANAL", f"{adr_w:{fmt}}")
                
                risk_u = balance * (risk_p / 100)
                sl = adr_w * 0.75
                lot = risk_u / (sl * 100000) if "=" in selected else risk_u / sl
                
                st.markdown(f"<div class='risk-box'>Riesgo: <b>${risk_u:.2f}</b> | SL: <b>{sl:.4f}</b><br><span style='font-size:18px; color:#d4af37;'>LOTES: {lot:.2f}</span></div>", unsafe_allow_html=True)
                
                st.markdown("---")
                if z_act < -2.2: st.markdown("<center><span class='badge-buy'>🔥 ACUMULACIÓN: COMPRA</span></center>", unsafe_allow_html=True)
                elif z_act > 2.2: st.markdown("<center><span class='badge-sell'>🔴 DISTRIBUCIÓN: VENTA</span></center>", unsafe_allow_html=True)
                else: st.markdown("<center><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></center>", unsafe_allow_html=True)

# --- TAB: ACADEMIA ---
with tab_acad:
    st.markdown("## 📚 ACADEMIA G-SNIPER ELITE")
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🦅 EL SINCROMECANISMO (EMA 20)</div>
            <p class="academy-text">Basado en backtesting riguroso, nuestra terminal utiliza la <b>EMA 20</b> como centro de gravedad. Cuando el precio se aleja excesivamente de esta línea (desequilibrio), la probabilidad de una regresión al promedio aumenta drásticamente.</p>
        </div>
        
        <div class="academy-card">
            <div class="academy-title">📊 LOS REYES MACRO (DXY, YIELDS, VIX)</div>
            <p class="academy-text">
                • <b>DXY (Dólar):</b> Si el dólar sube, la liquidez huye de los activos de riesgo.<br>
                • <b>10Y Yields:</b> El costo del dinero. Si sube, las tecnológicas caen.<br>
                • <b>VIX:</b> El termómetro del pánico. Si supera 25, buscamos rebotes institucionales.
            </p>
        </div>

        <div class="academy-card">
            <div class="academy-title">🔥 VPIN (FLUJO DE VOLUMEN)</div>
            <p class="academy-text">Identifica la <b>toxicidad del flujo</b>. Un VPIN superior al 70% confirma que las instituciones están inyectando órdenes reales y no es una manipulación minorista.</p>
        </div>

        <div class="academy-card">
            <div class="academy-title">📐 Z-SCORE Y ADR SEMANAL</div>
            <div class="formula">Z = (Precio - Media) / Desviación</div>
            <p class="academy-text">El <b>Z-Score</b> es tu GPS: Z > 2.2 significa mercado caro; Z < -2.2 significa mercado barato. El <b>ADR Semanal</b> mide la zancada del activo para poner Stop Loss técnicos.</p>
        </div>
    """, unsafe_allow_html=True)
