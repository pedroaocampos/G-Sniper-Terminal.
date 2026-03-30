# ==============================================================================
# 🦅 G-SNIPER TERMINAL QUANT | TRONO DE LA BESTIA V88.6
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import pytz
from datetime import datetime

# 🛡️ 1. CONFIGURACIÓN DE LA TERMINAL (ESTÉTICA DE ÉLITE)
st.set_page_config(page_title="G-SNIPER | OMNI-REVELATION", layout="wide", initial_sidebar_state="collapsed")

# CSS para Modo Oscuro y formato de tabla institucional
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .dataframe { font-family: 'Courier New', monospace; font-size: 14px; text-align: center; }
    h1, h2, h3 { color: #d4af37; font-family: 'Courier New', monospace; } /* Dorado Institucional */
    </style>
""", unsafe_allow_html=True)

# ⚔️ 2. DICCIONARIO DE ACTIVOS
ASSETS = {
    "ES=F": "S&P500", "NQ=F": "NAS100", "GC=F": "GOLD", "CL=F": "OIL", 
    "EURUSD=X": "EURUSD", "GBPUSD=X": "GBPUSD", "GBPJPY=X": "GBPJPY",
    "BTC-USD": "BITCOIN", "ETH-USD": "ETHEREUM"
} 

ORACULOS = {"DX-Y.NYB": "DXY 👑", "^TNX": "10Y YIELD 🔟", "^VIX": "VIX 📉"}

# 🧠 3. FUNCIONES CUANTITATIVAS BASE
def get_data(ticker, p="2y"):
    df = yf.download(ticker, period=p, interval="1d", progress=False, auto_adjust=True)
    if not df.empty and isinstance(df.columns, pd.MultiIndex): 
        df.columns = df.columns.get_level_values(0)
    return df if not df.empty else None

def calc_mfi(df, n=14):
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    mf = tp * df['Volume']
    pos_mf = pd.Series(np.where(tp > tp.shift(1), mf, 0), index=df.index)
    neg_mf = pd.Series(np.where(tp < tp.shift(1), mf, 0), index=df.index)
    mfr = pos_mf.rolling(n).sum() / neg_mf.rolling(n).sum().replace(0, np.nan)
    return 100 - (100 / (1 + mfr.fillna(1)))

def calc_atr(df, n=14):
    tr = pd.concat([df['High'] - df['Low'], abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))], axis=1).max(axis=1)
    return tr.rolling(n).mean()

# 🚀 4. INTERFAZ DE STREAMLIT
st.title("🦅 TRONO DE LA BESTIA V88.6 | DOSSIER ALTO TICKET")
st.caption(f"SINCRO NYT: {datetime.now(pytz.timezone('America/New_York')).strftime('%d-%b-%Y %H:%M:%S')}")
st.markdown("---")

if st.button("⚡ EJECUTAR ESCÁNER CUÁNTICO UNIVERSAL"):
    with st.spinner('Calibrando Oráculos y Redes Neuronales...'):
        
        # Oráculos Macro
        macro_col1, macro_col2, macro_col3 = st.columns(3)
        macro_data = {}
        for t, n in ORACULOS.items():
            df_o = yf.download(t, period="5d", progress=False, auto_adjust=True)
            val = float(df_o['Close'].iloc[-1]) if not df_o.empty else 0.0
            macro_data[n] = val
            
        macro_col1.metric("DXY (ÍNDICE DÓLAR)", f"{macro_data.get('DXY 👑', 0):.3f}")
        macro_col2.metric("VIX (MIEDO)", f"{macro_data.get('VIX 📉', 0):.2f}")
        macro_col3.metric("10Y YIELDS", f"{macro_data.get('10Y YIELD 🔟', 0):.3f}%")
        
        st.markdown("### I. INTELIGENCIA CUÁNTICA (ML & RISK)")
        
        results_ml = []
        results_tac = []
        
        # Motor de Análisis
        for t, name in ASSETS.items():
            df = get_data(t)
            if df is None or len(df) < 100: continue
            
            # Lógica IA & Monte Carlo
            df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['Z'] = (df['Close'] - df['EMA20']) / df['Close'].rolling(20).std().replace(0, 0.001)
            df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
            train = df[['Z', 'Target']].dropna()
            
            model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42).fit(train[['Z']], train['Target'])
            prob = float(model.predict_proba(df[['Z']].iloc[[-1]])[0][1] * 100)
            
            sims = [np.prod([1.02 if np.random.rand() < (prob/100) else 0.985 for _ in range(30)]) < 1.0 for _ in range(1000)]
            ruin = float(np.mean(sims) * 100)
            kelly_val = (2.0 * (prob / 100.0) - (1.0 - (prob / 100.0))) / 2.0
            kelly = float(max(0, kelly_val) * 100.0)
            
            # Táctica
            mfi = float(calc_mfi(df).iloc[-1])
            atr = float(calc_atr(df).iloc[-1])
            p = float(df['Close'].iloc[-1])
            acc = "🟢 BUY" if p > df['EMA20'].iloc[-1] else "🔴 SELL"
            sync = "✅" if (acc == "🟢 BUY" and mfi > 50) or (acc == "🔴 SELL" and mfi < 50) else "🟡"
            
            sentencia = "🔥 EXECUTE" if (prob > 58 or prob < 42) and ruin < 15 else "🛡️ ACECHO"
            
            results_ml.append({"ACTIVO": name, "IA PROB": f"{prob:.1f}%", "RUIN %": f"{ruin:.1f}%", "KELLY %": f"{kelly:.1f}%", "SENTENCIA": sentencia})
            results_tac.append({"ACTIVO": name, "DIRECCIÓN": acc, "PULSE (MFI)": f"{mfi:.0f}", "SYNC": sync, "ENTRADA": f"{p:.4f}", "ESTRATEGIA": "APEX-IA"})
            
        # Despliegue de Tablas
        df_ml = pd.DataFrame(results_ml)
        df_tac = pd.DataFrame(results_tac)
        
        st.dataframe(df_ml, use_container_width=True)
        st.markdown("### II. DOSSIER TÁCTICO DE EJECUCIÓN")
        st.dataframe(df_tac, use_container_width=True)
        
        st.success("✅ ANÁLISIS COMPLETADO. DOCTRINA ALPHA-CENTURION APLICADA.")
        st.caption("PROPIEDAD DE G-SNIPER UNIT - ACCESO EXCLUSIVO BAJO LICENCIA")