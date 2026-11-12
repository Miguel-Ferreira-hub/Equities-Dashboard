import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from utils import hide_sidebar_navigation,time_period_selector,data_type_selector,ticker_selector
from utils import Metrics

# ---------- Computation ----------
healthcare_tickers = [
    "UNH",       # UnitedHealth Group
    "CVS",       # CVS Health
    "CI",        # The Cigna Group
    "HUM",       # Humana
    "HCA",       # HCA Healthcare
    "MCK",       # McKesson
    "COR",       # Cencora
    "CAH",       # Cardinal Health
    "MDT",       # Medtronic
    "ABT",       # Abbott Laboratories
    "ISRG",      # Intuitive Surgical
    "SYK",       # Stryker
    "BSX",       # Boston Scientific
    "EW",        # Edwards Lifesciences
    "BDX",       # Becton Dickinson
    "GEHC",      # GE HealthCare
    "DHR",       # Danaher
    "TMO",       # Thermo Fisher Scientific
    "IDXX",      # IDEXX Laboratories
    "UHS"        # Universal Health Services
]

healthcare_names = [
    "UnitedHealth Group",
    "CVS Health",
    "The Cigna Group",
    "Humana",
    "HCA Healthcare",
    "McKesson",
    "Cencora",
    "Cardinal Health",
    "Medtronic",
    "Abbott Laboratories",
    "Intuitive Surgical",
    "Stryker",
    "Boston Scientific",
    "Edwards Lifesciences",
    "Becton Dickinson",
    "GE HealthCare",
    "Danaher",
    "Thermo Fisher Scientific",
    "IDEXX Laboratories",
    "Universal Health Services"
]

# ---------- Page Config ----------
st.set_page_config(
    page_title="Healthcare Dashboard",
    page_icon="🏦",
    layout="wide")

# ---------- Sidebar ----------
hide_sidebar_navigation()

with st.sidebar:

    if st.button(
    "🌐\n\nDashboard Selection",
    key="Dashboard Selection",
    use_container_width=True
    ):
        st.switch_page("app.py")

    if st.button(
    "🛡️\n\nDefence",
    key="Defence",
    use_container_width=True
    ):
        st.switch_page("pages/defence.py")

    if st.button(
        "🏦\n\nBanking",
        # key="Banking",
        use_container_width=True
    ):
        st.switch_page("pages/banking.py")

    if st.button(
        "💻\n\nTechnology",
        key="Technology",
        use_container_width=True
    ):
        st.switch_page("pages/technology.py")

    if st.button(
        "🤖\n\nSemiconductors & AI",
        key="Semiconductors & AI",
        use_container_width=True
    ):
        st.switch_page("pages/semiconductors.py")

    if st.button(
        "🏥\n\nHealthcare",
        key="Healthcare",
        use_container_width=True
    ):
        st.switch_page("pages/healthcare.py")

    if st.button(
        "🛒\n\nConsumer Staples",
        key="Consumer Staples",
        use_container_width=True
    ):
        st.switch_page("pages/consumer.py")

    if st.button(
        "💊\n\nPharmaceuticals",
        key="Pharmaceuticals",
        use_container_width=True
    ):
        st.switch_page("pages/pharmaceuticals.py")

    if st.button(
        "🛢️\n\nEnergy, Oil & Gas",
        key="Energy, Oil & Gas",
        use_container_width=True
    ):
        st.switch_page("pages/energy.py")

st.subheader("Healthcare Dashboard",text_alignment="center")

with st.container(border=True):

    # Retrieve selected Yahoo Finance period
    interval,period = time_period_selector(key_prefix="healthcare")

    selected_type = data_type_selector(key_prefix="healthcare")

    selected_ticker = ticker_selector(
        healthcare_names,
        healthcare_tickers,
        "Select Ticker",
        key_prefix="healthcare"
    )

    data = yf.download(
        selected_ticker,
        period=period,
        interval=interval,
        auto_adjust=True
    )

    # Metrics
    returns = Metrics.compute_returns(data[f"{selected_type}"])
    cagr = Metrics.compute_annualised_return(wealth=data[f"{selected_type}"])
    vol = Metrics.compute_annualised_volatility(returns=returns)
    sharpe = Metrics.compute_annualised_sharpe(returns=returns)
    sortino = Metrics.compute_annualised_sortino(returns=returns)
    drawdowns = Metrics.compute_drawdowns(wealth=data[f"{selected_type}"])
    max_drawdown = Metrics.compute_max_drawdown(wealth=data[f"{selected_type}"])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data[f"{selected_type}"].index, 
            y=data[f"{selected_type}"].values.ravel(),
            name=(f"{selected_ticker} {selected_type} Price" if selected_type != "Volume" else f"{selected_ticker} Volume"), 
            mode="lines",
            line=dict(color="#4ade80", width=2.2),
            fill="tozeroy", 
            fillcolor="rgba(74,222,128,0.08)"
        )
    )

    if selected_type != "Volume":

        fig.add_annotation(
            x=0.02,
            y=0.98,
            xref="paper",
            yref="paper",
            text=(
                "<b>PERFORMANCE SUMMARY</b><br>"
                f"Annualised Return: {cagr:.1f}%<br>"
                f"Annualised Volatility: {vol:.1f}%<br>"
                f"Max Drawdown: {max_drawdown:.1f}%<br>"
                f"Sharpe: {sharpe:.2f}<br>"
                f"Sortino: {sortino:.2f}<br>"
            ),
            showarrow=False,
            align="left",
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(30, 30, 30, 0.85)",
            bordercolor="rgba(150, 150, 150, 0.5)",
            borderwidth=1,
            borderpad=10,
            font=dict(
                size=11,
                color="white"
            )
        )

    fig.update_yaxes(tickprefix="$")

    fig.update_layout(
        title=(f"{selected_ticker} {selected_type} Price" if selected_type != "Volume" else f"{selected_ticker} Volume"),
        xaxis_title="Date",
        yaxis_title=f"{selected_type} Price ($)",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={"scrollZoom":False}
    )

if selected_type != "Volume":

    with st.container(border=True):

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=drawdowns.index,
                y=drawdowns.values.ravel()*100,
                fill="tozeroy",
                mode="lines",
                name="Drawdown",
                fillcolor="rgba(248,113,113,0.20)",
                line=dict(color="#f87171", width=1.4)
            ),
        )

        fig.update_yaxes(ticksuffix="%")

        fig.update_layout(
            title=f"{selected_ticker} {selected_type} Drawdowns",
            xaxis_title="Date",
            yaxis_title=f"Drawdown (%)",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={"scrollZoom":False}
        )

col1, col2, = st.columns(2)

if selected_type != "Volume":

    with col1:

        with st.container(border=True):

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=returns.index, 
                    y=returns.values.ravel() * 100,
                    name=f"{selected_ticker} {selected_type} Returns", 
                    mode="lines",
                    line=dict(color="#4ade80", width=2.2),
                    fill="tozeroy", 
                    fillcolor="rgba(74,222,128,0.08)"
                )
            )

            fig.update_yaxes(ticksuffix="%")

            fig.update_layout(
                title=f"{selected_ticker} {selected_type} Returns",
                xaxis_title="Date",
                yaxis_title="Returns (%)",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={"scrollZoom":False}
            )

    with col2:

        with st.container(border=True):

                fig = go.Figure()

                fig.add_trace(
                    go.Histogram(
                        x=returns.values.ravel(),
                        nbinsx=50,
                        histnorm="probability density",
                        name="Distribution of Returns",
                        opacity=0.6,
                        marker=dict(color="#4ade80")
                    )
                )

                fig.update_layout(
                    title=f"{selected_ticker} {selected_type} Returns Distribution",
                    xaxis_title="Returns (%)",
                    yaxis_title="Probability Density",
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    config={"scrollZoom":False}
                )

else:

    with st.container(border=True):

        fig = go.Figure()

        fig.add_trace(
            go.Histogram(
                x=data[f"{selected_type}"].values.ravel(),
                nbinsx=50,
                histnorm="probability density",
                name="Distribution of Returns",
                opacity=0.6,
                marker=dict(color="#4ade80")
            )
        )

        fig.update_layout(
            title=f"{selected_ticker} {selected_type} Distribution",
            xaxis_title="Volume",
            yaxis_title="Probability Density",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={"scrollZoom":False}
        )