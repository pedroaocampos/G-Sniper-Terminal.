# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V6.3 - INSTITUTIONAL DIPLOMACY (CON EMA 20 VISUAL)
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
    }
    .academy-title { color: #d4af37; font-size: 26px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid rgba(212,175,55,0.3); padding-bottom: 10px; }
    .academy-text { color: #bdc3c7; line-height: 1.8; font-size: 18px; }
    .pro-tip { background-color: rgba(212, 175, 55, 0.15); padding: 15px; border-radius: 8px; border: 1px dashed #d4af37; margin-top: 15px; color: #ffffff; }
    .formula { background-color: #000000; padding: 12px; border-radius: 6px; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 15px 0; border: 1px solid #333; }

    .badge-buy { background-color: #27ae60; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 4px 12px; border-radius: 6px; font-weight: bold; }
    
    .stButton>button { border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #d4af37 !important; color: #0b0d11 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. MOTOR QUANT
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
            time.sleep(random.uniform(0.4, 0.8))
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

# 5. HEADER BRANDING
st.markdown("""<div class='branding-header'><h1>🦅 G-SNIPER QUANT TERMINAL</h1><p style='color:#d4af37; letter-spacing: 5px; font-weight:bold;'>EDICIÓN ELITE V6.3</p></div>""", unsafe_allow_html=True)
tab_term, tab_acad = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA G-SNIPER"])

# --- TAB: TERMINAL ---
with tab_term:
    st.sidebar.markdown("### 💰 GESTIÓN DE CAPITAL")
    balance = st.sidebar.number_input("CAPITAL ($):", min_value=100.0, value=1000.0)
    risk_p = st.sidebar.slider("RIESGO (%):", 0.1, 5.0, 1.0)
    st.sidebar.markdown("---")
    selected = st.sidebar.selectbox("MERCADO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
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
        # Cálculo de la EMA 20 para el gráfico
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
        
        with c_graf:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                            increasing_line_color='#27ae60', decreasing_line_color='#e74c3c', name="Precio")])
            
            # --- SUMAMOS LA LÍNEA DORADA (EMA 20) ---
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], mode='lines', line=dict(color='#d4af37', width=1.5), name="Sincromecanismo (EMA 20)"))
            
            fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=500, 
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False,
                              legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
            st.plotly_chart(fig, width='stretch')

        with c_ia:
            st.markdown("### 🧠 ANALÍTICA QUANT")
            df['Z'] = calc_zscore(df); df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            train = df[['Z', 'Target']].dropna()
            model = RandomForestClassifier(n_estimators=50, max_depth=5).fit(train[['Z']], train['Target'])
            prob = float(model.predict_proba(df[['Z']].iloc[[-1]])[0][1] * 100)
            
            st.markdown(f"<div class='quant-card'><h1 style='color:white; margin:0;'>{prob:.1f}%</h1><p style='color:#d4af37;'>PROBABILIDAD IA</p></div>", unsafe_allow_html=True)
            
            z_act = df['Z'].iloc[-1]; adr_w = calc_adr_weekly(df).iloc[-1]; vpin_val = calc_vpin_proxy(df).iloc[-1]
            
            cx, cy = st.columns(2)
            cx.metric("Z-SCORE (DS)", f"{z_act:.2f}")
            cx.metric("FLUJO VPIN", f"{vpin_val:.1f}%")
            fmt = ".4f" if "=" in selected else ".2f"
            cy.metric("ADR SEMANAL", f"{adr_w:{fmt}}")
            cy.metric("ESTADO", "REVERSIÓN" if abs(z_act) > 2.2 else "ESTABLE")

            risk_u = balance * (risk_p / 100); sl = adr_w * 0.75
            lot = risk_u / (sl * 100000) if "=" in selected else risk_u / sl
            st.markdown(f"<div class='risk-box'><p style='margin:0;'>Riesgo: <b>${risk_u:.2f}</b> | SL: <b>{sl:.4f}</b></p><p style='color:#d4af37; font-size:18px; margin:5px 0;'><b>LOTES: {lot:.2f}</b></p></div>", unsafe_allow_html=True)

            if prob > 62: st.markdown("<center><span class='badge-buy'>🔥 ACUMULACIÓN: COMPRA</span></center>", unsafe_allow_html=True)
            elif prob < 38: st.markdown("<center><span class='badge-sell'>🔴 DISTRIBUCIÓN: VENTA</span></center>", unsafe_allow_html=True)
            else: st.markdown("<center><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></center>", unsafe_allow_html=True)

    if scan:
        st.markdown("---")
        st.markdown("### ⚡ MATRIZ GLOBAL (32 ACTIVOS)")
        cols = st.columns(3)
        idx = 0
        with st.spinner("Sincronizando arsenal..."):
            for t, name in ASSETS.items():
                df_s = get_data_safe(t, "1y")
                if df_s is not None and len(df_s) > 50:
                    df_s['Z'] = calc_zscore(df_s); df_s['Target'] = (df_s['Close'].shift(-1) > df_s['Close']).astype(int)
                    train_s = df_s[['Z', 'Target']].dropna()
                    model_s = RandomForestClassifier(n_estimators=30, max_depth=5).fit(train_s[['Z']], train_s['Target'])
                    p_ia = float(model_s.predict_proba(df_s[['Z']].iloc[[-1]])[0][1] * 100)
                    with cols[idx % 3]:
                        c_b = "#27ae60" if p_ia > 60 else "#e74c3c" if p_ia < 40 else "#d4af37"
                        b_cl = "badge-buy" if p_ia > 60 else "badge-sell" if p_ia < 40 else "badge-wait"
                        st.markdown(f"<div class='quant-card' style='border-left: 5px solid {c_b};'><h4>{name}</h4><p style='color:white; font-size:18px;'><b>{df_s['Close'].iloc[-1]:.4f}</b></p><span class='{b_cl}'>IA: {p_ia:.1f}%</span></div>", unsafe_allow_html=True)
                    idx += 1

# --- TAB: ACADEMIA ---
with tab_acad:
    st.markdown("## 📚 DOSSIER DE INTELIGENCIA ESTRATÉGICA")
    
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🦅 MÓDULO 1: EL SINCROMECANISMO G-SNIPER</div>
            <div class="academy-text">
                A diferencia de los indicadores convencionales que suelen presentar retraso (lagging), G-SNIPER se basa en un <b>Sincromecanismo</b> validado por backtesting riguroso. Este sistema mide la elasticidad del precio respecto a su promedio exponencial móvil (EMA 20).
                <br><br>
                El precio, por naturaleza estadística, siempre busca regresar a su centro de gravedad. Cuando el precio se "estira" excesivamente (detectado por nuestra analítica), la terminal identifica una inminente regresión al promedio.
            </div>
            <div class="pro-tip">💡 <b>OBSERVACIÓN TÁCTICA:</b> La línea dorada en el gráfico representa tu centro de gravedad. La distancia entre las velas y esta línea es la base de nuestra probabilidad.</div>
        </div>

        <div class="academy-card">
            <div class="academy-title">🧠 MÓDULO 2: ORÁCULO IA (RANDOM FOREST)</div>
            <div class="academy-text">
                Nuestra IA utiliza un motor de Machine Learning que entrena 50 árboles de decisión en tiempo real. Este enfoque nos diferencia al no basarnos en una sola condición, sino en una clasificación probabilística de la estructura actual del mercado.
            </div>
            <div class="formula">Probabilidad = (Consenso de Árboles / 50) * 100</div>
        </div>

        <div class="academy-card">
            <div class="academy-title">📉 MÓDULO 3: Z-SCORE (GPS ESTADÍSTICO)</div>
            <div class="academy-text">
                El Z-Score es nuestra métrica de desviación. Basado en un análisis de varianza, nos indica cuántas desviaciones estándar se ha desplazado el activo respecto a su EMA 20.
            </div>
            <div class="formula">$$Z = \\frac{Precio - EMA_{20}}{Desviación \ Estándar}$$</div>
            <div class="academy-text">
                • <b>Z > +2.2:</b> Distribución Institucional Inminente.<br>
                • <b>Z < -2.2:</b> Acumulación Institucional Inminente.
            </div>
        </div>
    """, unsafe_allow_html=True)
