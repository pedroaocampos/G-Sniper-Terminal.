# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V7.2 - MASTER CLASS EDITION
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import time
import random

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

# 2. ESTÉTICA PREMIUM (CSS) - NEGRO PURO Y ORO
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    .branding-header { text-align: center; padding: 20px; border-bottom: 2px solid #d4af37; margin-bottom: 25px; }
    .quant-card { background-color: #0b0d11; border: 1px solid #d4af37; padding: 20px; border-radius: 12px; margin-bottom: 15px; text-align: center; }
    .risk-box { background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-top: 10px; }
    
    /* ACADEMIA ELITE - DISEÑO EXPANDIDO */
    .academy-card { background: linear-gradient(145deg, #161b22, #0b0d11); border-left: 5px solid #d4af37; padding: 35px; border-radius: 12px; margin-bottom: 35px; border-right: 1px solid #333; }
    .academy-title { color: #d4af37; font-size: 28px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid rgba(212,175,55,0.4); padding-bottom: 10px; }
    .academy-subtitle { color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; }
    .academy-text { color: #bdc3c7; line-height: 1.9; font-size: 17px; text-align: justify; }
    .pro-tip { background-color: rgba(212, 175, 55, 0.15); padding: 20px; border-radius: 8px; border: 1px dashed #d4af37; margin-top: 20px; color: #ffffff; font-weight: bold; font-style: italic; }
    .formula { background-color: #000000; padding: 15px; border-radius: 6px; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 20px 0; border: 1px solid #444; font-size: 18px; }

    /* Badges */
    .badge-buy { background-color: #27ae60; color: white; padding: 6px 18px; border-radius: 8px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 6px 18px; border-radius: 8px; font-weight: bold; }
    .badge-wait { background-color: #f1c40f; color: #000000 !important; padding: 6px 18px; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. FUNCIONES CORE
@st.cache_data(ttl=600)
def get_data_safe(ticker):
    try:
        time.sleep(random.uniform(0.3, 0.6))
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

# 4. ARSENAL (32 ACTIVOS)
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
st.markdown("""<div class='branding-header'><h1>🦅 G-SNIPER QUANT TERMINAL</h1><p style='color:#d4af37; letter-spacing: 5px; font-weight:bold;'>MASTER CLASS EDITION V7.2</p></div>""", unsafe_allow_html=True)

tab_term, tab_acad = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA ELITE"])

with tab_term:
    st.sidebar.markdown("### 💰 MONEY MANAGER")
    balance = st.sidebar.number_input("CAPITAL TOTAL ($):", value=1000.0)
    risk_p = st.sidebar.slider("RIESGO POR OPERACIÓN (%):", 0.1, 5.0, 1.0)
    st.sidebar.markdown("---")
    selected = st.sidebar.selectbox("ACTIVO SELECCIONADO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])

    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data_safe(t)
        if df_o is not None:
            v = df_o['Close'].iloc[-1]
            m_cols[i].metric(n, f"{v:.2f}", f"{v - df_o['Close'].iloc[-2]:.2f}")
    
    st.markdown("---")
    
    df_f = get_data_safe(selected)
    if df_f is not None:
        c_l, c_r = st.columns([2.2, 1])
        with c_l:
            df_f['EMA20'] = df_f['Close'].ewm(span=20, adjust=False).mean()
            fig = go.Figure(data=[go.Candlestick(x=df_f.index, open=df_f['Open'], high=df_f['High'], low=df_f['Low'], close=df_f['Close'], 
                            increasing_line_color='#27ae60', decreasing_line_color='#e74c3c', name="Velas")])
            fig.add_trace(go.Scatter(x=df_f.index, y=df_f['EMA20'], mode='lines', line=dict(color='#d4af37', width=1.8), name="EMA 20"))
            
            fig.update_layout(template='plotly_dark', height=580, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False,
                              paper_bgcolor='black', plot_bgcolor='black', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
            st.plotly_chart(fig, use_container_width=True)
        
        with c_r:
            st.markdown("### 🧠 ANALÍTICA QUANT")
            z_act = calc_zscore(df_f).iloc[-1]
            adr_w = (df_f['High'] - df_f['Low']).rolling(5).mean().iloc[-1]
            vpin_val = calc_vpin(df_f).iloc[-1]
            
            # IA
            df_f['Z'] = calc_zscore(df_f); df_f['T'] = (df_f['Close'].shift(-1) > df_f['Close']).astype(int)
            train = df_f[['Z', 'T']].dropna()
            model = RandomForestClassifier(n_estimators=30).fit(train[['Z']], train['T'])
            p_ia = model.predict_proba(df_f[['Z']].iloc[[-1]])[0][1] * 100

            st.markdown(f"<div class='quant-card'><h1 style='color:white; margin:0;'>{p_ia:.1f}%</h1><p style='color:#d4af37;'>PROBABILIDAD IA</p></div>", unsafe_allow_html=True)

            cx, cy = st.columns(2)
            cx.metric("Z-SCORE", f"{z_act:.2f}")
            cx.metric("FLUJO VPIN", f"{vpin_val:.1f}%") # LIMPIO DE "YAYA"
            fmt = ".4f" if "=" in selected else ".2f"
            cy.metric("ADR SEMANAL", f"{adr_w:{fmt}}")
            cy.metric("ESTADO", "REVERSIÓN" if abs(z_act) > 2.2 else "ESTABLE")
            
            risk_u = balance * (risk_p / 100); sl = adr_w * 0.75
            lot = risk_u / (sl * 100000) if "=" in selected else risk_u / sl
            st.markdown(f"<div class='risk-box'>Riesgo Máximo: <b>${risk_u:.2f}</b><br>SL Sugerido: <b>{sl:.4f}</b><br><span style='font-size:18px; color:#d4af37;'>LOTES: {lot:.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            if p_ia > 62: st.markdown("<center><span class='badge-buy'>🔥 ACUMULACIÓN: COMPRA</span></center>", unsafe_allow_html=True)
            elif p_ia < 38: st.markdown("<center><span class='badge-sell'>🔴 DISTRIBUCIÓN: VENTA</span></center>", unsafe_allow_html=True)
            else: st.markdown("<center><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></center>", unsafe_allow_html=True)

# --- TAB: ACADEMIA MASTER CLASS ---
with tab_acad:
    st.markdown("## 📚 ACADEMIA G-SNIPER: INTELIGENCIA QUANT")
    
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🦅 EL SINCROMECANISMO (EMA 20)</div>
            <p class="academy-text">
                En el trading institucional, el precio siempre orbita alrededor de un <b>punto de equilibrio</b>. G-SNIPER utiliza la Media Móvil Exponencial de 20 periodos (EMA 20) como este eje central. 
                <br><br>
                Cuando el precio se aleja excesivamente de esta línea, se genera una tensión estadística que tarde o temprano provoca un regreso al promedio (Mean Reversion). La línea dorada en tu gráfico no es un indicador más, es el imán del mercado.
            </p>
        </div>

        <div class="academy-card">
            <div class="academy-title">🔥 FLUJO VPIN (Volume Probability of Informed Trading)</div>
            <p class="academy-text">
                El <b>VPIN</b> es una métrica de alta frecuencia que identifica la <b>toxicidad del flujo de órdenes</b>. Nos permite distinguir si un movimiento de precio está respaldado por dinero institucional "informado" o si es simple ruido minorista.
            </p>
            <div class="academy-subtitle">Cómo interpretarlo:</div>
            <p class="academy-text">
                • <b>VPIN > 70%:</b> Alta toxicidad. Las instituciones están empujando el precio con intención real. Confirmación de tendencia.<br>
                • <b>VPIN < 30%:</b> Bajo interés institucional. El mercado está en una fase de "lavado" o manipulación sin volumen real.
            </p>
        </div>

        <div class="academy-card">
            <div class="academy-title">📏 Z-SCORE: LA REGLA DE LA DESVIACIÓN</div>
            <p class="academy-text">
                El Z-Score cuantifica cuántas <b>Desviaciones Estándar</b> se ha desplazado el precio respecto a su EMA 20. Es la herramienta definitiva para saber si un activo está objetivamente "caro" o "barato".
            </p>
            <div class="formula">Z = (Precio Actual - EMA 20) / Desviación Estándar</div>
            <p class="academy-text">
                Un Z-Score por encima de +2.2 indica que el activo ha subido demasiado rápido y es probable una <b>distribución</b>. Un valor por debajo de -2.2 indica una <b>acumulación</b> inminente.
            </p>
        </div>

        <div class="academy-card">
            <div class="academy-title">📊 PILARES MACRO: DXY, YIELDS Y VIX</div>
            <p class="academy-text">
                Ningún activo se mueve solo. La terminal monitorea las tres fuerzas que dictan el sentimiento global:
            </p>
            <div class="academy-subtitle">1. DXY (Índice del Dólar)</div>
            <p class="academy-text">Es el refugio del capital. Si el DXY sube, el capital huye de las criptos y las acciones. Si baja, el riesgo está "ON" (compras activas).</p>
            <div class="academy-subtitle">2. 10Y Yields (Bonos de Tesoro)</div>
            <p class="academy-text">Representan el costo del dinero. Un aumento en los rendimientos de los bonos castiga a las empresas tecnológicas y de crecimiento.</p>
            <div class="academy-subtitle">3. VIX (Índice de Miedo)</div>
            <p class="academy-text">Mide la volatilidad implícita. Si el VIX explota por encima de 25, hay pánico. Un Sniper profesional compra cuando el pánico está en su punto máximo y vende cuando hay complacencia.</p>
        </div>

        <div class="academy-card">
            <div class="academy-title">📏 ADR SEMANAL Y MONEY MANAGER</div>
            <p class="academy-text">
                El <b>Average Daily Range (ADR)</b> mide la volatilidad histórica reciente para proyectar cuánto "recorrido" le queda al precio en una sesión. 
            </p>
            <div class="pro-tip">💡 GESTIÓN PROFESIONAL: G-SNIPER utiliza el ADR para sugerirte un Stop Loss que el ruido del mercado no pueda tocar. Si tu SL no está basado en la volatilidad real, eres la liquidez de los bancos.</div>
        </div>
    """, unsafe_allow_html=True)
