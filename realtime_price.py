import streamlit as st
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime
import time
import matplotlib.pyplot as plt

def run_realtime_price_monitor():
    st.header("📊 Real-Time Price Monitor (Live Preview)")

    ticker_symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL, TCS.NS)", value="AAPL")
    interval_sec = st.slider("Update Interval (seconds)", 1, 10, 5)

    window_size = 30
    timestamps = []
    prices = []

    model = LinearRegression()
    chart = st.empty()
    start_button = st.button("Start Live Monitoring")

    if start_button:
        while True:
            data = yf.download(tickers=ticker_symbol, period="1d", interval="1m")
            if not data.empty and 'Close' in data.columns:
                current_price = data['Close'].iloc[-1]
                current_time = datetime.datetime.now().strftime("%H:%M:%S")

                timestamps.append(current_time)
                prices.append(current_price)

                if len(prices) > window_size:
                    timestamps = timestamps[-window_size:]
                    prices = prices[-window_size:]

                if len(prices) >= 5:
                    X = np.arange(len(prices)).reshape(-1, 1)
                    y = np.array(prices)
                    model.fit(X, y)
                    next_price = model.predict(np.array([[len(prices)]]))[0]
                    predicted_prices = list(prices) + [next_price]
                    predicted_timestamps = timestamps + ['next']
                else:
                    predicted_prices = prices
                    predicted_timestamps = timestamps

                fig, ax = plt.subplots()
                ax.plot(timestamps, prices, label="Actual Price")
                ax.plot(predicted_timestamps, predicted_prices, linestyle='--', label="Predicted")
                ax.set_title(f"Live Price: {ticker_symbol}")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price")
                ax.legend()
                plt.xticks(rotation=45)
                chart.pyplot(fig)

                time.sleep(interval_sec)
            else:
                st.warning("No data received!")
