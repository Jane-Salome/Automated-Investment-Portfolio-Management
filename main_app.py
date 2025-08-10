import streamlit as st
from prediction_app import run_prediction
from risk_analysis import run_risk_analysis
from notifications import run_notification_ui
from realtime_price import run_realtime_price_monitor

st.set_page_config(page_title="📊 Stock Market App", layout="wide")

st.sidebar.title("📁 Navigation")
page = st.sidebar.radio("Go to", ["📈 Prediction", "🛡️ Risk Analysis", "🔔 Notifications", "📊 Real-Time Monitor"])

if page == "📈 Prediction":
    run_prediction()
elif page == "🛡️ Risk Analysis":
    run_risk_analysis()
elif page == "🔔 Notifications":
    run_notification_ui()
elif page == "📊 Real-Time Monitor":
    run_realtime_price_monitor()
