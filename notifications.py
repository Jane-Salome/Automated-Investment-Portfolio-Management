import random
import time
import copy
import streamlit as st

previous_state = {}

def fetch_portfolio(user_id):
    return {
        'user_id': user_id,
        'portfolio_value': round(random.uniform(90000, 110000), 2),
        'asset_allocation': {
            'stocks': round(random.uniform(55, 65), 2),
            'bonds': round(random.uniform(25, 35), 2),
            'cash': round(random.uniform(5, 10), 2)
        },
        'risk_level': random.choice(['low', 'medium', 'high'])
    }

def detect_changes(new_data, old_data):
    changes = []
    if not old_data:
        return ['Initial data loaded']

    if new_data['portfolio_value'] != old_data['portfolio_value']:
        changes.append(f"Portfolio value changed from ₹{old_data['portfolio_value']} to ₹{new_data['portfolio_value']}.")

    for asset in new_data['asset_allocation']:
        new_val = new_data['asset_allocation'][asset]
        old_val = old_data['asset_allocation'][asset]
        if new_val != old_val:
            changes.append(f"{asset.capitalize()} allocation changed from {old_val}% to {new_val}%.")

    if new_data['risk_level'] != old_data['risk_level']:
        changes.append(f"Risk level changed from {old_data['risk_level']} to {new_data['risk_level']}.")

    return changes

def run_notification_ui():
    st.header("🔔 Portfolio Notifications (Simulated)")
    user_id = 101
    current_data = fetch_portfolio(user_id)
    old_data = previous_state.get(user_id)
    changes = detect_changes(current_data, old_data)

    if changes:
        for msg in changes:
            st.warning(msg)
        previous_state[user_id] = copy.deepcopy(current_data)
    else:
        st.success("✅ No changes detected.")
