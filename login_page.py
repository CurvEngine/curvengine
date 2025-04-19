import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from monte_engine_core import MonteEngine
import auth

st.set_page_config(page_title="Monte Carlo Simulator", layout="centered")
st.title("🏀 Monte Carlo Betting Simulator")

if "auth_state" not in st.session_state:
    st.session_state.auth_state = None

if not st.session_state.auth_state:
    st.subheader("🔐 Login to use CURV")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            res = auth.login_user(email, password)
            if "session" in res and res.session is not None:
                st.session_state.auth_state = res.session
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Login failed.")
    with col2:
        if st.button("Sign Up"):
            res = auth.signup_user(email, password)
            if "user" in res and res.user is not None:
                st.success("✅ Account created! Please log in.")
            else:
                st.error("❌ Signup failed. Email may be taken.")
    st.stop()

# If logged in, show simulator
events = []
n_events = st.number_input("How many events?", min_value=1, max_value=10, value=2, step=1)

for i in range(n_events):
    st.subheader(f"Event {i+1}")
    label = st.text_input(f"Label for Event {i+1}", value=f"Team {i+1}", key=f"label_{i}")
    probability = st.slider(f"Win Probability for {label}", 0.0, 1.0, 0.65, 0.01, key=f"prob_{i}")
    odds = st.number_input(f"Odds for {label}", value=-110, step=1, key=f"odds_{i}")
    stake = st.number_input(f"Stake for {label} ($)", value=100, step=10, key=f"stake_{i}")
    events.append({"label": label, "probability": probability, "odds": odds, "stake": stake})

if st.button("Run Simulation"):
    engine = MonteEngine(simulations=10000)
    results = engine.simulate_card(events)

    st.subheader("📊 Simulation Results")
    st.write(f"**Mean Profit:** ${results['mean_profit']:.2f}")
    st.write(f"**Chance of Profit:** {results['prob_profit']*100:.2f}%")
    st.write(f"**98% Confidence Interval:** ${results['confidence_interval'][0]:.2f} to ${results['confidence_interval'][1]:.2f}")

    st.subheader("📉 Profit Distribution")
    fig, ax = plt.subplots()
    ax.hist(results['all_simulations'], bins=50, color='skyblue', edgecolor='black')
    ax.set_title("Profit Distribution Across 10,000 Simulations")
    ax.set_xlabel("Profit ($)")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("📈 Cumulative Probability Curve")
    sorted_profits = np.sort(results['all_simulations'])
    cumulative = np.arange(1, len(sorted_profits)+1) / len(sorted_profits)
    fig2, ax2 = plt.subplots()
    ax2.plot(sorted_profits, cumulative, color='green')
    ax2.set_title("Cumulative Probability of Profit")
    ax2.set_xlabel("Profit ($)")
    ax2.set_ylabel("Probability ≤ x")
    ax2.grid(True)
    st.pyplot(fig2)

st.markdown("---")
st.markdown(f"Logged in as: `{email}`")
if st.button("Logout"):
    auth.sign_out()
    st.session_state.auth_state = None
    st.success("You’ve been logged out.")
