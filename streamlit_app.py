import streamlit as st
import yfinance as yf
import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=32)
def get_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    if period == "LTM":
        return stock.history(period="1y")
    elif period == "5Y":
        return stock.history(period="5y")
    elif period == "10Y":
        return stock.history(period="10y")
    else:
        return None

@lru_cache(maxsize=32)
def get_fundamental_metrics(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "Market Cap": info.get("marketCap"),
        "PE Ratio": info.get("trailingPE"),
        "EPS": info.get("trailingEps"),
        "Price to Book": info.get("priceToBook"),
        "Dividend Yield": info.get("dividendYield")
    }

def main():
    st.title("Stock Valuation App")

    ticker = st.text_input("Enter Stock Ticker", "AAPL")
    period = st.selectbox("Select Period", ["LTM", "5Y", "10Y"])

    if st.button("Get Stock Data"):
        data = get_stock_data(ticker, period)
        metrics = get_fundamental_metrics(ticker)

        if data is not None:
            st.subheader(f"{ticker} Stock Data for {period}")
            st.line_chart(data['Close'])

            st.subheader("Fundamental Metrics")
            for key, value in metrics.items():
                st.write(f"{key}: {value}")

if __name__ == "__main__":
    main()

