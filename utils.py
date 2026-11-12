from numpy.fft import rfft
import streamlit as st
import pandas as pd
import numpy as np

# ---------- Compute Metrics ----------

def get_periods_per_year(data: pd.Series, rf_yearly = 0.044):
    """
    Infer annualisation periods from the DatetimeIndex.
    Supports daily, weekly, monthly and hourly data.
    """

    if not isinstance(data.index, pd.DatetimeIndex):
        raise TypeError("Data must have a DatetimeIndex")

    interval = data.index.to_series().diff().median()

    if interval <= pd.Timedelta(hours=1):
        periods = 252 * 6.5  # Approx. US equity trading hours

    elif interval <= pd.Timedelta(days=1):
        periods = 252

    elif interval <= pd.Timedelta(days=7):
        periods = 52

    elif interval <= pd.Timedelta(days=31):
        periods = 12

    elif interval <= pd.Timedelta(days=92):
        periods = 4

    elif interval <= pd.Timedelta(days=366):
        periods = 1

    rf = (1 + rf_yearly)**(1/periods) - 1

    if periods:
        return periods,rf

    else:
        raise ValueError("Unable to infer sampling frequency")

class Metrics():

    def compute_returns(df: pd.DataFrame):
        returns = df.pct_change().dropna()
        return returns

    def compute_annualised_volatility(returns: pd.Series):
        periods,_ = get_periods_per_year(data=returns)
        vol = returns.std()*np.sqrt(periods)
        vol *= 100
        return vol.item()

    def compute_annualised_return(wealth: pd.Series):
        elapsed_years = ((wealth.index[-1] - wealth.index[0]).total_seconds() / (365.25 * 24 * 60 * 60))
        cagr = (wealth.iloc[-1] / wealth.iloc[0]) ** (1 / elapsed_years) - 1
        return float(cagr * 100)

    def compute_annualised_sharpe(returns: pd.Series):
        periods,rf = get_periods_per_year(returns)
        excess = returns - rf
        vol = returns.std()
        sharpe = (excess.mean() / vol) * np.sqrt(periods)
        return sharpe.item()

    def compute_annualised_sortino(returns: pd.Series):
        periods,rf = get_periods_per_year(returns)
        excess = returns - rf
        downside = excess.clip(upper=0)
        downside_vol = np.sqrt(np.mean(downside**2))
        sortino = (excess.mean() / downside_vol) * np.sqrt(periods)
        return sortino.item()

    def compute_drawdowns(wealth: pd.Series):
        previous_peaks = wealth.cummax()
        drawdowns = (wealth - previous_peaks)/previous_peaks
        return drawdowns

    def compute_max_drawdown(wealth: pd.Series):
        previous_peaks = wealth.cummax()
        max_drawdown = ((wealth - previous_peaks) / previous_peaks).min().item() * 100
        return max_drawdown

# ---------- Hide Sidebar Navigation Helper Function ----------

def hide_sidebar_navigation():
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

# ---------- Toggle Between Time Periods ----------

def time_period_selector(key_prefix="default"):

    periods = {
        "1D": "1d",
        "5D": "5d",
        "1M": "1mo",
        "3M": "3mo",
        "6M": "6mo",
        "YTD": "ytd",
        "1Y": "1y",
        "5Y": "5y"
    }

    selected_period = st.segmented_control(
        "Time Period",
        options=list(periods.keys()),
        default="1M",
        selection_mode="single",
        label_visibility="collapsed",
        key=f"{key_prefix}_period"
    )

    if selected_period in ("1D","5D"):
        interval = "1m"
    

    elif selected_period in ("1M","3M","6M"):
        interval = '1h'

    else:
        interval = "1d"

    return interval, periods[selected_period] if selected_period else "1mo"

# ---------- Toggle Between Price Types (OHLCV) ----------

def data_type_selector(key_prefix="default"):

    types = {
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Close": "Close",
        "Volume": "Volume",
    }

    selected_data_type = st.segmented_control(
        "Select Data Type",
        options=list(types.keys()),
        default="Close",
        selection_mode="single",
        label_visibility="collapsed",
        key=f"{key_prefix}_data_type"
    )

    return selected_data_type if selected_data_type else "Close"

# ---------- Toggle Between Tickers ----------

def ticker_selector(names, tickers, label="Select Company", key_prefix="default"):

    options = {
        f"{name} ({ticker})": ticker
        for name, ticker in zip(names, tickers)
    }

    selected_ticker = st.selectbox(
        label,
        options=list(options.keys()),
        key=f"{key_prefix}_ticker"
    )

    return options[selected_ticker] if selected_ticker else options[names[0]]