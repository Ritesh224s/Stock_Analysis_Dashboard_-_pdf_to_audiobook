import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ================== FUNCTIONS ==================

def calculate_indicators(data):
    out = data.copy()

    # Ensure Close is always Series (not DataFrame with multiple tickers)
    if isinstance(out['Close'], pd.DataFrame):
        close = out['Close'].iloc[:, 0]  # take first ticker if multi
    else:
        close = out['Close']

    # SMA 20
    out["SMA_20"] = close.rolling(window=20).mean()

    # Bollinger Bands
    rolling_std = close.rolling(window=20).std()
    out["Upper_BB"] = out["SMA_20"] + (rolling_std * 2)
    out["Lower_BB"] = out["SMA_20"] - (rolling_std * 2)

    return out


def plot_stock(data, indicators):
    plt.figure(figsize=(12, 6))

    # Handle Close column (Series or DataFrame)
    if isinstance(data['Close'], pd.DataFrame):
        close = data['Close'].iloc[:, 0]
    else:
        close = data['Close']

    plt.plot(data.index, close, label="Close Price", color="blue")

    if "SMA_20" in indicators:
        plt.plot(data.index, data["SMA_20"], label="SMA 20", color="orange")
    if "Upper_BB" in indicators:
        plt.plot(data.index, data["Upper_BB"], label="Upper BB", color="green")
    if "Lower_BB" in indicators:
        plt.plot(data.index, data["Lower_BB"], label="Lower BB", color="red")

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)


def plot_volume(data):
    plt.figure(figsize=(12, 4))

    # Ensure Volume is Series
    if isinstance(data['Volume'], pd.DataFrame):
        volume = data['Volume'].iloc[:, 0]
    else:
        volume = data['Volume']

    plt.bar(data.index, volume, color="blue", alpha=0.4)
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.grid(True)
    st.pyplot(plt)


# ================== STREAMLIT APP ==================

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("StockPulse – Capture the pulse of the market")

st.header("📈 Interactive Stock Dashboard")

st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, INFY)", "AAPL")
start_date = st.sidebar.text_input("Start Date", "2022-01-01")
end_date = st.sidebar.text_input("End Date", "2025-09-04")

indicators = st.sidebar.multiselect(
    "Select Indicators to Display",
    ["SMA_20", "Upper_BB", "Lower_BB"],
    default=["SMA_20"]
)

try:
    # Download stock data
    data = yf.download(ticker, start=start_date, end=end_date)

    if not data.empty:
        data = calculate_indicators(data)

        st.subheader("Stock Price with Indicators")
        plot_stock(data, indicators)

        st.subheader("Trading Volume")
        plot_volume(data)
    else:
        st.error("No data found for the given ticker and date range.")

except Exception as e:
    st.error(f"Error fetching stock data: {e}")
