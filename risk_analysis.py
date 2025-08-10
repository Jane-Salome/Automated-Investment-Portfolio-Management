import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def run_risk_analysis():
    st.header("🛡️ Risk Analysis")

    ticker = "AAPL"
    start_date = "2024-01-01"
    end_date = "2025-05-30"
    portfolio_value = 100000
    max_loss_per_trade = 0.02
    allocation_per_stock = 0.1

    data = yf.download(ticker, start=start_date, end=end_date)
    data.dropna(inplace=True)
    data['Daily Return'] = data['Close'].pct_change()

    VaR_95 = np.percentile(data['Daily Return'].dropna(), 5)
    max_position_size = portfolio_value * allocation_per_stock
    stop_loss_price = float(data['Close'].iloc[-1] * (1 - max_loss_per_trade))
    initial_capital = portfolio_value
    cumulative_returns = (1 + data['Daily Return']).cumprod()
    portfolio_values = initial_capital * cumulative_returns

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=portfolio_values, mode="lines", name="Portfolio Value"))
    fig.add_trace(go.Scatter(x=data.index, y=[stop_loss_price]*len(data), mode="lines", name="Stop-Loss Price", line=dict(dash="dash", color="red")))
    fig.update_layout(title=f"Risk Management Backtest for {ticker}", xaxis_title="Date", yaxis_title="Portfolio Value")
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"95% VaR for {ticker}: {VaR_95:.2%}")
    st.info(f"Stop-Loss Price: ${stop_loss_price:.2f}")
