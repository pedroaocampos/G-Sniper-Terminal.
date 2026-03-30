# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | V3.2 - ARSENAL ELITE (32 ACTIVOS & ALTA VISIBILIDAD)
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

# CSS PERSONALIZADO - DISEÑO DE ALTO TICKET & ALTA LEGIBILIDAD
st.markdown("""
    <style>
    /* Fondo y Colores Base */
    .stApp { background-color: #0b0d11; }
    h1, h2, h3, h4 { color: #d4af37 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stMarkdown, p, span, label { color: #bdc3c7 !important; }
    
    /* Tarjetas Dinámicas del Escáner */
    .quant-card {
        background-color: #161b22;
        border: 1px solid #d4af37;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
    }
    .quant-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0px 5px 15px rgba(212, 175, 55, 0.2);
        border-color: #ffffff;
    }
    
    /* Botones Premium */
    .stButton>button { 
        border-color: #d4af37; color: #d4af37; width: 100%; border-radius: 8px; 
        background-color: transparent; font-weight: bold; height: 50px;
        text-transform: uppercase; letter-spacing: 2px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #d4af37 !important; color: #0b0d11 !important; }
    
    /* Badges de Estado */
    .badge-buy { background-color: #27ae60; color: white; padding: 5px 12px; border-radius: 6px; font-weight: bold; display: inline-block; }
    .badge-sell { background-color: #e74c3c; color: white; padding: 5px 12px; border-radius: 6px; font-weight: bold; display: inline-block; }
    
    /* --- CORRECCIÓN DE CONTRASTE: ESPACIO AMARILLO --- */
    /* Letras Negras sobre Amarillo Dorado para máximo contraste visual */
    .badge-wait { 
        background-color: #f1c40f; 
        color: #000000 !important; 
        padding: 5px 12px; 
        border-radius: 6px; 
        font-weight: bold; 
        display: inline-block;
        border: 1px solid #d4af37;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #0e1117; border-right: 1px solid #d4af37; }
    </style>
""", unsafe_allow_html=True)

# 2. ARSENAL DE ACTIVOS (ESPECTRO GLOBAL COMPLETO - 32 TOTAL)
# Organizados con iconos para mejor legibilidad institucional
ASSETS = {
    # 💱 FOREX MAJORS & CROSSES (12)
    "EURUSD=X": "💱 EUR/USD", "GBPUSD=X": "💱 GBP/USD", "USDJPY=X": "💱 USD/JPY", "USDCHF=X": "💱 USD/CHF",
    "AUDUSD=X": "💱 AUD/USD", "USDCAD=X": "💱 USD/CAD", "NZDUSD=X": "💱 NZD/USD", "EURGBP=X": "💱 EUR/GBP",
    "EURJPY=X": "💱 EUR/JPY", "GBPJPY=X": "💱 GBP/JPY", "AUDJPY=X": "💱 AUD/JPY", "EURCHF=X": "💱 EUR/CHF",
    
    # 🪙 CRIPTOMONEDAS TOP (8)
    "BTC-USD": "🪙 BITCOIN", "ETH-USD": "🪙 ET HEREUM", "SOL-USD": "🪙 SOLANA", "XRP-USD": "🪙 RIPPLE",
    "ADA-USD": "🪙 CARDANO", "DOGE-USD": "🪙 DOGECOIN", "BNB-USD": "🪙 BINANCE COIN", "LINK-USD": "🪙 CHAINLINK",
    
    # 📊 ÍNDICES BURSÁTILES MUNDIALES (CFDs/FUTUROS) (7)
    "ES=F": "📊 S&P 500 (US)", "NQ=F": "📊 NASDAQ 100 (US)", "YM=F": "📊 DOW JONES (US)", "RTY=F": "📊 RUSSELL 2000 (US)",
    "^GDAXI": "📊 DAX 40 (DE)", "^FTSE": "📊 FTSE 100 (UK)", "^N225": "📊 NIKKEI 225 (JP)",
    
    # 🛢️ COMMODITIES / MATERIAS PRIMAS (5)
    "GC=F": "🛢️ ORO", "SI=F": "🛢️ PLATA", "CL=F": "🛢️ PETRÓLEO WTI", "NG=F": "🛢️ GAS NATURAL", "HG=F": "🛢️ COBRE"
} 

ORACULOS = {"DX-Y.NYB": "DXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

@st.cache_data(ttl=300)
def get_data(ticker, p="1y"):
    try:
        df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
        if not df.empty and isinstance(df.columns, pd.MultiIndex): 
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception:
        return None

# 3. CABECERA INSTITUCIONAL
st.title("🦅 G-SNIPER QUANT TERMINAL")
c_h1, c_h2 = st.columns([2, 1])
with c_h1:
    st.caption(f"SINCROMECANISMO: {datetime.now(pytz.timezone('America/New_York')).strftime('%d-%b-%Y %H:%M:%S')} NYT")
with c_h2:
    st.markdown("<div style='text-align: right;'><span class='badge-buy'>SISTEMA OPERATIVO 🟢</span></div>", unsafe_allow_html=True)

st.markdown("---")

# 4. PANEL LATERAL
st.sidebar.markdown("### 🎯 CENTRO DE MANDO")
# Usamos format_func para organizar por categorías visuales
selected_ticker = st.sidebar.selectbox("ACTIVO EN FOCO (32 TOTAL):", list(ASSETS.keys()), format_func=lambda x: ASSETS[x])
st.sidebar.markdown("---")
scan_global = st.sidebar.button("⚡ EJECUTAR ESCÁNER GLOBAL")

# 5. MONITORES MACRO (ORÁCULOS)
st.markdown("#### 🌐 MONITORES ESTRATÉGICOS")
m_cols = st.columns(3)
for i, (t, n) in enumerate(ORACULOS.items()):
    df_o = get_data(t, "5d")
    if df_o is not None and not df_o.empty:
        val = float(df_o['Close'].iloc[-1])
        prev = float(df_o['Close'].iloc[-2]) if len(df_o)>1 else val
        delta = val - prev
        m_cols[i].metric(n, f"{val:.2f}", f"{delta:.2f}")

st.markdown("---")

# 6. ANÁLISIS DE ACTIVO SELECCIONADO
col_graf, col_ia = st.columns([2, 1])
df_foco = get_data(selected_ticker, "6mo")

if df_foco is not None and not df_foco.empty:
    with col_graf:
        st.markdown(f"### 🔭 GRÁFICO TÁCTICO: {ASSETS[selected_ticker]}")
        fig = go.Figure(data=[go.Candlestick(x=df_foco.index,
                        open=df_foco['Open'], high=df_foco['High'],
                        low=df_foco['Low'], close=df_foco['Close'],
                        increasing_line_color='#27ae60', decreasing_line_color='#e74c3c')])
        fig.update_layout(template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0), height=450,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_ia:
        st.markdown("### 🧠 SENTENCIA IA")
        # Algoritmo de Probabilidad
        df_foco['EMA20'] = df_foco['Close'].ewm(span=20, adjust=False).mean()
        df_foco['Z'] = (df_foco['Close'] - df_foco['EMA20']) / df_foco['Close'].rolling(20).std().replace(0, 0.001)
        df_foco['Target'] = (df_foco['Close'].shift(-1) > df_foco['Close']).astype(int)
        train = df_foco[['Z', 'Target']].dropna()
        
        if len(train) > 10:
            model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
            prob = float(model.predict_proba(df_foco[['Z']].iloc[[-1]])[0][1] * 100)
            
            st.markdown(f"""<div class='quant-card'>
                <h1 style='color: white !important; margin-bottom: 0;'>{prob:.1f}%</h1>
                <p style='color: #d4af37;'>CONFIANZA PREDICTIVA</p>
            </div>""", unsafe_allow_html=True)
            st.progress(int(prob))
            
            # --- CORRECCIÓN DE VISIBILIDAD DE LA SENTENCIA ---
            if prob > 60: st.markdown("<div style='text-align:center'><span class='badge-buy'>🔥 SEÑAL: EJECUTAR COMPRA</span></div>", unsafe_allow_html=True)
            elif prob < 40: st.markdown("<div style='text-align:center'><span class='badge-sell'>🔴 SEÑAL: EJECUTAR VENTA</span></div>", unsafe_allow_html=True)
            else: 
                # Ahora usa letras NEGRAS para máximo contraste sobre el amarillo
                st.markdown("<div style='text-align:center'><span class='badge-wait'>🛡️ ESTADO: ACECHO (SIN ENTRADA)</span></div>", unsafe_allow_html=True)
        
        # Módulo de Noticias Seguro (Anti-KeyError)
        st.markdown("---")
        st.markdown("#### 📰 RADAR DE NOTICIAS")
        try:
            t_obj = yf.Ticker(selected_ticker)
            # Aumentamos a 3 noticias para mas valor
            news = t_obj.news[:3]
            if news:
                for n in news:
                    t_str = n.get('title', 'Noticia en curso...')
                    l_str = n.get('link', '#')
                    # Abrir noticias en pestaña nueva por defecto
                    st.markdown(f"**[{t_str}]({l_str})**", unsafe_allow_html=True)
            else: st.info("Sin noticias de impacto en este momento.")
        except: st.caption("Radar de noticias offline temporalmente.")

# 7. ESCÁNER GLOBAL (TARJETAS DINÁMICAS - SOPORTA 32 ACTIVOS)
if scan_global:
    st.markdown("---")
    st.markdown("### ⚡ MATRIZ DE ESCANEO UNIVERSAL (32 ACTIVOS)")
    
    # Aviso de tiempo de carga para 32 activos
    st.info("⚡ Iniciando análisis de Redes Neuronales sobre el arsenal completo (32 mercados). La primera carga de datos puede tomar unos segundos.")
    
    cols = st.columns(3)
    idx = 0
    # Spinner mas agresivo para la espera
    with st.spinner("Sincronizando arsenal y entrenando IA..."):
        # Iteramos sobre el nuevo arsenal gigante
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
                    color_b = "#27ae60" if p_ia > 60 else "#e74c3c" if p_ia < 40 else "#d4af37"
                    
                    # Usamos badges estilizados dentro de las tarjetas
                    badge_class = "badge-buy" if p_ia > 60 else "badge-sell" if p_ia < 40 else "badge-wait"
                    badge_text = "BUY F." if p_ia > 60 else "SELL F." if p_ia < 40 else "WAIT"
                    
                    # UI Premium para las tarjetas
                    st.markdown(f"""
                        <div class="quant-card" style="border-left: 6px solid {color_b};">
                            <h4 style='margin-bottom: 5px;'>{name}</h4>
                            <p style='font-size: 18px; color: white;'>Precio: <b>{df['Close'].iloc[-1]:.4f}</b></p>
                            <span class="{badge_class}">IA: {p_ia:.1f}%</span>
                        </div>
                    """, unsafe_allow_html=True)
                idx += 1
        
        st.success(f"Escáner finalizado sobre {idx} activos activos del arsenal global.")
