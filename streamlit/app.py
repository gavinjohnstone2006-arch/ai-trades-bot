import os, subprocess, sys, time
import streamlit as st

st.set_page_config(page_title="AI Trades Bot", layout="centered")
st.title("AI Trades Bot — Web Controller")

with st.form("runform"):
    symbols = st.text_input("Symbols (comma-separated)", "AAPL,TSLA,NVDA")
    strategy = st.selectbox("Strategy", ["gap_and_go","orb_breakout","vwap_reversion"])
    asset = st.selectbox("Asset Class", ["stock","crypto"])
    mode = st.selectbox("Mode", ["paper","live"])
    broker = st.selectbox("Broker (optional)", ["","alpaca","binance","bybit","kraken"])
    risk = st.number_input("Risk per trade (fraction)", value=0.003, step=0.001, format="%.4f")
    interval = st.selectbox("Interval", ["1m","5m","15m"])
    partials = st.text_input("Partials (e.g., 50@1R,50@2R)", "50@1R,50@2R")
    trail = st.number_input("Trailing stop fraction", value=0.0, step=0.001, format="%.4f")
    notify = st.checkbox("Send Discord/Telegram Alerts", value=False)
    run_once = st.form_submit_button("Run Once")
    start_loop = st.form_submit_button("Start Loop (60s)")

def build_cmd():
    cmd = [
        sys.executable, "main.py",
        "--mode", mode,
        "--symbols", symbols,
        "--strategy", strategy,
        "--asset_class", asset,
        "--risk", str(risk),
        "--interval", interval,
        "--partials", partials,
        "--trail_pct", str(trail),
    ]
    if broker: cmd += ["--broker", broker]
    if notify: cmd += ["--notify"]
    return cmd

placeholder = st.empty()

def run_once_cmd():
    cmd = build_cmd()
    placeholder.code(" ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    st.text_area("Output", (res.stdout or "") + "\n" + (res.stderr or ""), height=250)

if run_once:
    run_once_cmd()

if start_loop:
    st.warning("Loop running. Keep this page open. Close/stop the app to end.")
    while True:
        run_once_cmd()
        time.sleep(60)
