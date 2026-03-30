# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V5.0 - ACADEMY & HOTMART EDITION
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

# 2. ESTÉTICA PREMIUM (CSS) - INCLUYE DISEÑO DE ACADEMIA
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    
    /* Tarjetas de Diseño Quant */
    .quant-card {
        background-color: #161b22;
        border: 1px solid #d4af37;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        text-align: center;
    }
    
    /* Tarjetas de Academia (Flash Cards) */
    .academy-card {
        background: linear-gradient(145deg, #1e242c, #161b22);
        border-left: 5px solid #d4af37;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    .academy-title { color: #d4af37; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    .academy-text { color: #bdc3c7; line-height: 1.6; font-size: 16px; }
    .pro-tip { background-color: rgba(212, 175, 55, 0.1); padding: 10px; border-radius: 5px; border: 1px dashed #d4af37; margin-top: 10px; }

    /* Badges */
    .badge-buy { background-color: #27ae60; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; }

    /* Botones Sidebar */
    .stButton>button { 
        border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; 
        background-color: transparent; font-weight: bold;
    }
    .stButton>button:hover { background-color: #d4af37 !important; color: #0b0d11 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES QUANT (Z-SCORE, VPIN, ADR)
def calc_zscore(df, period=20):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    return (df['Close'] - sma) / std

def calc_adr_weekly(df):
    return (df['High'] - df['Low']).rolling(window=5).mean()

def calc_vpin_proxy(df, window=20):
    vpt = (df['Volume'] * (df['Close'].pct_change())).rolling(window=window).std()
    return (vpt / vpt.rolling(window=100).max()) * 100

@st.cache_data(ttl=300)
def get_data(ticker, p="1y"):
    try:
        df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
        if not df.empty and isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        return df
    except: return None

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

ORACULOS = {"DX-Y.NYB": "DXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 5. ESTRUCTURA DE PESTAÑAS (ACADEMIA INTEGRADA)
st.title("🦅 G-SNIPER QUANT TERMINAL")
tab_terminal, tab_academia = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA G-SNIPER"])

# --- PESTAÑA 1: TERMINAL OPERATIVA ---
with tab_terminal:
    st.caption(f"SINCROMECANISMO: {datetime.now(pytz.timezone('America/New_York')).strftime('%d-%b-%Y %H:%M:%S')} NYT")
    st.markdown("---")
    
    # SideBar (Solo visible en terminal para no ensuciar la academia)
    st.sidebar.markdown("### 🎯 PANEL DE CONTROL")
    selected_ticker = st.sidebar.selectbox("SELECCIONAR MERCADO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
    scan_global = st.sidebar.button("⚡ ESCANEAR ARSENAL GLOBAL")

    # Oráculos
    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data(t, "5d")
        if df_o is not None and not df_o.empty:
            val = float(df_o['Close'].iloc[-1])
            prev = float(df_o['Close'].iloc[-2]) if len(df_o)>1 else val
            m_cols[i].metric(n, f"{val:.2f}", f"{val-prev:.2f}")

    st.markdown("---")

    col_graf, col_ia = st.columns([2, 1])
    df_foco = get_data(selected_ticker, "1y")

    if df_foco is not None and not df_foco.empty:
        with col_graf:
            st.markdown(f"### 🔭 GRÁFICO PROFESIONAL: {ASSETS[selected_ticker]}")
            fig = go.Figure(data=[go.Candlestick(x=df_foco.index, open=df_foco['Open'], high=df_foco['High'], low=df_foco['Low'], close=df_foco['Close'], increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
            fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

        with col_ia:
            st.markdown("### 🧠 ANALÍTICA QUANT")
            df_foco['Z'] = calc_zscore(df_foco)
            df_foco['Target'] = (df_foco['Close'].shift(-1) > df_foco['Close']).astype(int)
            train = df_foco[['Z', 'Target']].dropna()
            model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
            prob = float(model.predict_proba(df_foco[['Z']].iloc[[-1]])[0][1] * 100)
            
            st.markdown(f"<div class='quant-card'><h1 style='color: white !important; margin-bottom:0;'>{prob:.1f}%</h1><p style='color:#d4af37;'>PROBABILIDAD IA</p></div>", unsafe_allow_html=True)
            
            z_actual = df_foco['Z'].iloc[-1]
            adr_w = calc_adr_weekly(df_foco).iloc[-1]
            vpin = calc_vpin_proxy(df_foco).iloc[-1]
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Z-SCORE", f"{z_actual:.2f}")
                st.metric("VPIN", f"{vpin:.1f}%")
            with c2:
                st.metric("ADR SEM.", f"{adr_w:.4f}")
                if abs(z_actual) > 2: st.warning("REVERSIÓN")
                else: st.success("NORMAL")

            st.markdown("---")
            if prob > 60: st.markdown("<div style='text-align:center'><span class='badge-buy'>🔥 EJECUTAR COMPRA</span></div>", unsafe_allow_html=True)
            elif prob < 40: st.markdown("<div style='text-align:center'><span class='badge-sell'>🔴 EJECUTAR VENTA</span></div>", unsafe_allow_html=True)
            else: st.markdown("<div style='text-align:center'><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></div>", unsafe_allow_html=True)

    if scan_global:
        st.markdown("---")
        st.markdown("### ⚡ MATRIZ GLOBAL (32 ACTIVOS)")
        cols = st.columns(3)
        idx = 0
        with st.spinner("Procesando arsenal..."):
            for t, name in ASSETS.items():
                df = get_data(t, "1y")
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

# --- PESTAÑA 2: ACADEMIA G-SNIPER ---
with tab_academia:
    st.markdown("### 📚 MANUAL DE OPERACIONES TÁCTICAS")
    st.write("Bienvenido a la Bóveda de Conocimiento. Aquí entenderás la ciencia detrás de la Terminal.")
    
    # FLASH CARDS
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🦅 EL ORÁCULO IA (Random Forest)</div>
            <div class="academy-text">
                Nuestra Inteligencia Artificial no adivina; <b>clasifica probabilidades</b>. Utiliza un algoritmo de "Bosque Aleatorio" que analiza miles de micro-decisiones basadas en la volatilidad y la desviación histórica.
                <br><b>Lectura:</b> Por encima de 60% es una señal de alta convicción institucional.
            </div>
            <div class="pro-tip">💡 <b>TIP DEL COMANDANTE:</b> Nunca operes señales con IA menor al 55%, son zonas de ruido.</div>
        </div>
        
        <div class="academy-card">
            <div class="academy-title">📉 Z-SCORE (Desviación Estadística)</div>
            <div class="academy-text">
                Mide cuántas "Desviaciones Estándar" se ha alejado el precio de su promedio real. Es el GPS de la reversión. 
                <br><b>Lectura:</b> Un Z-Score superior a +2.0 indica que el precio está carísimo (Venta). Inferior a -2.0 indica que está regalado (Compra).
            </div>
            <div class="pro-tip">💡 <b>TIP DEL COMANDANTE:</b> Cuando la IA y el Z-Score coinciden en un extremo, la probabilidad de éxito supera el 85%.</div>
        </div>
        
        <div class="academy-card">
            <div class="academy-title">🔥 VPIN (Volumen de Presión)</div>
            <div class="academy-text">
                Identifica la "Toxicidad del Flujo". Nos dice si el volumen que ves en el gráfico es de traders minoristas atrapados o de <b>Grandes Instituciones</b> barriendo el mercado.
                <br><b>Lectura:</b> Un VPIN alto (>70%) confirma que el movimiento tiene gasolina real para continuar.
            </div>
        </div>
        
        <div class="academy-card">
            <div class="academy-title">📏 ADR SEMANAL (Rango Diario Promedio)</div>
            <div class="academy-text">
                Es la regla que mide cuánto se mueve un activo en una semana normal. Te sirve para poner tus <b>Take Profit</b> de forma realista.
                <br><b>Lectura:</b> Si el ADR es de 100 pips y el precio ya movió 90, ya no hay espacio para entrar. La operación terminó.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("⚠️ Esta terminal es una herramienta de asistencia probabilística. La gestión de riesgo es responsabilidad del operador.")
