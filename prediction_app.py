import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go

def run_prediction():
    st.header("📈 Stock Price Prediction")

    data = pd.read_csv("Combined_Stock_Data.csv", parse_dates=['Date'])
    data.set_index('Date', inplace=True)

    target_column = st.selectbox("Select the target column for prediction", options=['High', 'Open', 'Close', 'Low'])

    X = data[['High', 'Open', 'Close']]
    y = data[target_column]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    val_predictions = model.predict(X_val)

    mse = mean_squared_error(y_val, val_predictions)
    st.write(f"Validation Mean Squared Error: {mse:.4f}")

    future_days = st.sidebar.slider("Select Future Prediction Days (1-30)", min_value=1, max_value=30, value=7)
    last_known_date = data.index[-1]
    future_dates = [last_known_date + timedelta(days=i) for i in range(1, future_days + 1)]
    future_predictions = model.predict(X.tail(future_days))

    fig = go.Figure()

    years_back = 5
    start_date = last_known_date - timedelta(days=365 * years_back)
    historical_data = data[target_column].loc[start_date:]

    fig.add_trace(go.Scatter(x=historical_data.index, y=historical_data, mode='lines', name='Historical Data', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=future_dates, y=future_predictions, mode='lines+markers', name='Future Prediction', line=dict(color='red', dash='dash')))

    fig.update_layout(title=f"{target_column} Stock Price Prediction (Next {future_days} Days)", xaxis_title="Date", yaxis_title="Price", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
