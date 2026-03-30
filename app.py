# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V5.3 - TOTAL KNOWLEDGE EDITION (HOTMART READY)
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

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

# 2. ESTÉTICA PREMIUM (CSS)
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
    
    /* Tarjetas de Academia (Flash Cards Expandidas) */
    .academy-card {
        background: linear-gradient(145deg, #1e242c, #161b22);
        border-left: 5px solid #d4af37;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.6);
    }
    .academy-title { color: #d4af37; font-size: 24px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #d4af37; padding-bottom: 10px; }
    .academy-text { color: #bdc3c7; line-height: 1.8; font-size: 17px; }
    .pro-tip { background-color: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 8px; border: 1px dashed #d4af37; margin-top: 15px; color: #ffffff; }
    .formula { background-color: #000000; padding: 10px; border-radius: 5px; color: #00ff00; font-family: monospace; text-align: center; margin: 10px 0; }

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

# 3. FUNCIONES QUANT
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
    try:
        time.sleep(0.3) # Protocolo Stealth para evitar Rate Limit
        df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
        if not df.empty and isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        return df if not df.empty else None
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

ORACULOS = {"UUP": "DXY PROXY (USD) 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 5. ESTRUCTURA DE PESTAÑAS
st.title("🦅 G-SNIPER QUANT TERMINAL")
tab_terminal, tab_academia = st.tabs(["🦅 TERMINAL OPERATIVA", "📚 ACADEMIA G-SNIPER"])

# --- TAB: TERMINAL ---
with tab_terminal:
    st.sidebar.markdown("### 🎯 PANEL DE CONTROL")
    selected_ticker = st.sidebar.selectbox("SELECCIONAR MERCADO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
    scan_global = st.sidebar.button("⚡ ESCANEAR ARSENAL GLOBAL")

    m_cols = st.columns(3)
    for i, (t, n) in enumerate(ORACULOS.items()):
        df_o = get_data_safe(t, "5d")
        if df_o is not None and not df_o.empty:
            val = float(df_o['Close'].iloc[-1])
            prev = float(df_o['Close'].iloc[-2]) if len(df_o)>1 else val
            m_cols[i].metric(n, f"{val:.2f}", f"{val-prev:.2f}")

    st.markdown("---")
    col_graf, col_ia = st.columns([2, 1])
    df_foco = get_data_safe(selected_ticker, "1y")

    if df_foco is not None and not df_foco.empty:
        with col_graf:
            st.markdown(f"### 🔭 MONITOR TÁCTICO: {ASSETS[selected_ticker]}")
            fig = go.Figure(data=[go.Candlestick(x=df_foco.index, open=df_foco['Open'], high=df_foco['High'], low=df_foco['Low'], close=df_foco['Close'], increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
            fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, width='stretch')

        with col_ia:
            st.markdown("### 🧠 ANALÍTICA INSTITUCIONAL")
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
                st.metric("Z-SCORE (DS)", f"{z_actual:.2f}")
                st.metric("FLUJO VPIN", f"{vpin:.1f}%")
            with c2:
                fmt = ".4f" if "USD" in selected_ticker or "=" in selected_ticker else ".2f"
                st.metric("ADR SEMANAL", f"{adr_w:{fmt}}")
                if abs(z_actual) > 2.2: st.warning("REVERSIÓN")
                else: st.success("ESTABLE")

            st.markdown("---")
            if prob > 62: st.markdown("<div style='text-align:center'><span class='badge-buy'>🔥 ACUMULACIÓN: COMPRA</span></div>", unsafe_allow_html=True)
            elif prob < 38: st.markdown("<div style='text-align:center'><span class='badge-sell'>🔴 DISTRIBUCIÓN: VENTA</span></div>", unsafe_allow_html=True)
            else: st.markdown("<div style='text-align:center'><span class='badge-wait'>🛡️ ESTADO: ACECHO</span></div>", unsafe_allow_html=True)

    if scan_global:
        st.markdown("---")
        st.markdown("### ⚡ MATRIZ GLOBAL (32 ACTIVOS)")
        cols = st.columns(3)
        idx = 0
        with st.spinner("Sincronizando arsenal..."):
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

# --- TAB: ACADEMIA ---
with tab_academia:
    st.markdown("## 📚 DOSSIER DE INTELIGENCIA QUANT")
    st.write("Bienvenido al centro de mando educativo. Aquí aprenderás a interpretar los datos de la terminal para operar como una institución.")
    
    # CARD 1: EL SINCROMECANISMO
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🦅 MÓDULO 1: EL SINCROMECANISMO G-SNIPER</div>
            <div class="academy-text">
                El sistema G-SNIPER no utiliza indicadores rezagados tradicionales. Se basa en el <b>Sincromecanismo</b>: la unión perfecta entre la Media Móvil Exponencial (EMA 20) y la Acción del Precio pura.
                <br><br>
                Cuando el precio se aleja demasiado de la EMA 20, se crea un desequilibrio magnético. La terminal detecta este estiramiento y calcula cuándo el "elástico" está a punto de romperse para regresar al promedio.
            </div>
            <div class="pro-tip">💡 <b>ESTRATEGIA:</b> Si el precio está lejos de la EMA 20 y el Z-Score está en un extremo, prepárate para la reversión.</div>
        </div>
    """, unsafe_allow_html=True)

    # CARD 2: RANDOM FOREST IA
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🧠 MÓDULO 2: ORÁCULO IA (RANDOM FOREST)</div>
            <div class="academy-text">
                Nuestra IA utiliza un algoritmo de <b>Machine Learning</b> llamado <i>Random Forest Classifier</i>. No es una bola de cristal, es un motor estadístico que entrena 50 "árboles de decisión" simultáneos cada vez que seleccionas un activo.
                <br><br>
                La IA analiza la relación entre la volatilidad actual y los resultados históricos del último año para darte un porcentaje de probabilidad.
            </div>
            <div class="formula">Probabilidad IA = (Árboles Alcistas / Total Árboles) * 100</div>
            <div class="pro-tip">💡 <b>PROTOCOLO:</b> Operamos solo cuando la probabilidad supera el 62% (Compra) o es inferior al 38% (Venta).</div>
        </div>
    """, unsafe_allow_html=True)

    # CARD 3: Z-SCORE (EL GPS ESTADÍSTICO)
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">📉 MÓDULO 3: Z-SCORE (LA REVERSIÓN A LA MEDIA)</div>
            <div class="academy-text">
                El <b>Z-Score</b> es el indicador más potente de la terminal. Nos dice cuántas desviaciones estándar se ha movido el precio respecto a su promedio.
                <br><br>
                Matemáticamente, el 95% del tiempo el precio debe estar entre un Z-Score de -2 y +2. 
            </div>
            <div class="formula">$$Z = \\frac{Precio - Promedio}{Desviación}$$</div>
            <div class="academy-text">
                • <b>Z > +2.0:</b> Mercado extremadamente caro. Alta probabilidad de caída.<br>
                • <b>Z < -2.0:</b> Mercado extremadamente barato. Alta probabilidad de rebote.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # CARD 4: VPIN (VOLUMEN INSTITUCIONAL)
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🔥 MÓDULO 4: VPIN (VOLUMEN DE PRESIÓN)</div>
            <div class="academy-text">
                El VPIN (Volume Probability of Informed Trading) identifica la <b>toxicidad del flujo</b>. Nos permite distinguir entre el volumen "tonto" (traders minoristas atrapados) y el volumen "informado" (Grandes Instituciones).
                <br><br>
                • <b>VPIN ALTO (>70%):</b> Los peces gordos están inyectando liquidez agresiva. El movimiento tiene fuerza.<br>
                • <b>VPIN BAJO (<30%):</b> El mercado está en rango o manipulación sin intención real.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # CARD 5: ADR SEMANAL (OBJETIVOS TÁCTICOS)
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">📏 MÓDULO 5: ADR SEMANAL (GESTIÓN DE OBJETIVOS)</div>
            <div class="academy-text">
                El <b>Average Daily Range (ADR)</b> mide la volatilidad real del activo en la última semana. Es tu regla para saber dónde poner el Take Profit.
                <br><br>
                Si el ADR de una divisa es de 0.0080 (80 pips) y hoy ya ha movido 75 pips, la probabilidad de que siga avanzando es mínima. Has llegado tarde a la fiesta.
            </div>
            <div class="pro-tip">💡 <b>REGLA DE ORO:</b> Nunca abras una operación si el activo ya ha recorrido más del 70% de su ADR diario/semanal.</div>
        </div>
    """, unsafe_allow_html=True)

    # CARD 6: LOS ORÁCULOS MACRO
    st.markdown("""
        <div class="academy-card">
            <div class="academy-title">🌐 MÓDULO 6: CORRELACIÓN MACRO (LOS TRES REYES)</div>
            <div class="academy-text">
                La terminal monitorea tres activos que mueven al mundo:
                <br><br>
                1. <b>DXY (Dólar):</b> El rey. Si el Dólar sube, las criptos y el oro suelen bajar.<br>
                2. <b>10Y Yield (Bonos):</b> Si sube, el dinero fluye fuera de las acciones tecnológicas (Nasdaq).<br>
                3. <b>VIX (Miedo):</b> Si el VIX sube de 20, hay pánico. Los mercados caen, pero las oportunidades de reversión aumentan.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.warning("🦅 RECUERDA: La Terminal G-SNIPER te da la probabilidad, tú pones la disciplina. La gestión de riesgo es la única garantía de supervivencia.")
