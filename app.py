# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V3.0 - BLACK EDITION (10/10)
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import pytz
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA & ESTILO DE LUJO
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    
    /* Tarjetas Dinámicas */
    .quant-card {
        background-color: #161b22;
        border: 1px solid #d4af37;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: transform 0.3s;
    }
    .quant-card:hover { transform: scale(1.02); border-color: #ffffff; }
    
    /* Botones Premium */
    .stButton>button { 
        border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; 
        background-color: transparent; font-weight: bold; height: 50px;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { background-color: #d4af37; color: #0b0d11; box-shadow: 0px 0px 15px #d4af37; }
    
    /* Badges de Señal */
    .badge-buy { background-color: #27ae60; color: white; padding: 4px 10px; border-radius: 5px; font-weight: bold; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 4px 10px; border-radius: 5px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. ARSENAL DE ACTIVOS
ASSETS = {
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "USDJPY=X": "USD/JPY",
    "BTC-USD": "BITCOIN", "ETH-USD": "ETHEREUM", "SOL-USD": "SOLANA", 
    "ES=F": "S&P 500", "NQ=F": "NASDAQ 100", "GC=F": "ORO", "CL=F": "PETRÓLEO"
} 

@st.cache_data(ttl=300)
def get_data(ticker, p="1y"):
    try:
        df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
        if not df.empty and isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        return df
    except: return None

# 3. INTERFAZ SUPERIOR
st.title("🦅 G-SNIPER QUANT TERMINAL")
col_header_1, col_header_2 = st.columns([2, 1])
with col_header_1:
    st.caption(f"SINCROMECANISMO: {datetime.now(pytz.timezone('America/New_York')).strftime('%d-%b-%Y %H:%M:%S')} NYT")
with col_header_2:
    st.success("SISTEMA OPERATIVO - LICENCIA PREMIUM")

st.markdown("---")

# 4. PANEL LATERAL & ESCÁNER
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2583/2583118.png", width=100) # Icono de águila/lujo
st.sidebar.markdown("### 🎯 MENÚ TÁCTICO")
selected_ticker = st.sidebar.selectbox("ACTIVO EN FOCO:", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
scan_global = st.sidebar.button("⚡ ESCANEAR MERCADO TOTAL")

# 5. SECCIÓN: FOCO TÁCTICO (ANÁLISIS PROFUNDO)
col_a, col_b = st.columns([2, 1])
df_foco = get_data(selected_ticker, "6mo")

if df_foco is not None and not df_foco.empty:
    with col_a:
        st.markdown(f"### 🔭 GRÁFICO DE ALTA PRECISIÓN: {ASSETS[selected_ticker]}")
        fig = go.Figure(data=[go.Candlestick(x=df_foco.index,
                        open=df_foco['Open'], high=df_foco['High'],
                        low=df_foco['Low'], close=df_foco['Close'],
                        increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
        fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=450,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("### 🧠 SENTENCIA DE IA")
        # Lógica IA
        df_foco['EMA20'] = df_foco['Close'].ewm(span=20, adjust=False).mean()
        df_foco['Z'] = (df_foco['Close'] - df_foco['EMA20']) / df_foco['Close'].rolling(20).std().replace(0, 0.001)
        df_foco['Target'] = (df_foco['Close'].shift(-1) > df_foco['Close']).astype(int)
        train = df_foco[['Z', 'Target']].dropna()
        model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
        prob = float(model.predict_proba(df_foco[['Z']].iloc[[-1]])[0][1] * 100)
        
        # UI de la IA
        st.markdown(f"<div class='quant-card'><h1 style='text-align: center; color: white !important;'>{prob:.1f}%</h1><p style='text-align: center;'>CONFIANZA DE ACIERTO</p></div>", unsafe_allow_html=True)
        st.progress(int(prob))
        
        if prob > 60: st.markdown("<span class='badge-buy'>🔥 SEÑAL: EJECUTAR COMPRA FUERTE</span>", unsafe_allow_html=True)
        elif prob < 40: st.markdown("<span class='badge-sell'>🔴 SEÑAL: EJECUTAR VENTA FUERTE</span>", unsafe_allow_html=True)
        else: st.markdown("<span style='color: #f1c40f;'>🛡️ ESTADO: ACECHO (SIN ENTRADA)</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 📰 NOTICIAS DE IMPACTO")
        ticker_obj = yf.Ticker(selected_ticker)
        news = ticker_obj.news[:3]
        for n in news:
            st.markdown(f"**[{n['title']}]({n['link']})**")
            st.caption(f"Fuente: {n['publisher']}")

# 6. SECCIÓN: ESCÁNER GLOBAL (TARJETAS DINÁMICAS)
if scan_global:
    st.markdown("---")
    st.markdown("### ⚡ MATRIZ DE ESCANEO UNIVERSAL")
    cols = st.columns(3)
    idx = 0
    with st.spinner("Procesando arsenal global..."):
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
                    color_borde = "#27ae60" if p_ia > 60 else "#e74c3c" if p_ia < 40 else "#d4af37"
                    st.markdown(f"""
                        <div class="quant-card" style="border-left: 5px solid {color_borde};">
                            <h4>{name}</h4>
                            <p>Precio: <b>{df['Close'].iloc[-1]:.4f}</b></p>
                            <p>IA: <b>{p_ia:.1f}%</b></p>
                        </div>
                    """, unsafe_allow_html=True)
                idx += 1
