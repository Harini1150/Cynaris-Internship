
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Indian Business Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "indian_business_orders.csv"


# --------------------------------------------------
# LOAD AND PREPARE DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    )

    df["Profit"] = pd.to_numeric(
        df["Profit"], errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )

    df = df.dropna(
        subset=["Order Date", "Amount", "Profit"]
    )

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset not found. Please check "
        "data/indian_business_orders.csv."
    )
    st.stop()


# --------------------------------------------------
# DASHBOARD HEADER
# --------------------------------------------------

st.title("📊 Indian Business Forecasting Dashboard")

st.markdown(
    "Interactive sales analysis and short-term "
    "forecasting using the Indian Business Orders dataset."
)

st.caption(
    "Technology: Python | Pandas | Scikit-learn | "
    "Plotly | Streamlit"
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select categories",
    categories,
    default=categories
)

states = sorted(df["State"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "Select states",
    states,
    default=states
)

forecast_horizon = st.sidebar.selectbox(
    "Forecast horizon",
    [3, 6, 12],
    index=0,
    format_func=lambda x: f"{x} months"
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df[
    (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
    & (df["Category"].isin(selected_categories))
    & (df["State"].isin(selected_states))
].copy()

if filtered_df.empty:
    st.warning(
        "No records match the selected filters. "
        "Please change your filters."
    )
    st.stop()


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_sales = filtered_df["Amount"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
average_order_value = (
    total_sales / total_orders if total_orders else 0
)

st.subheader("Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Average Order Value", f"₹{average_order_value:,.0f}")


# --------------------------------------------------
# MONTHLY SALES TREND
# --------------------------------------------------

st.divider()
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .set_index("Order Date")
    .resample("MS")["Amount"]
    .sum()
    .reset_index()
)

monthly_sales.columns = ["Month", "Sales"]

fig_trend = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Performance",
    labels={
        "Month": "Month",
        "Sales": "Sales (₹)"
    }
)

fig_trend.update_layout(
    hovermode="x unified",
    yaxis_tickprefix="₹"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# --------------------------------------------------
# SALES FORECAST
# --------------------------------------------------

st.divider()
st.subheader("Future Sales Forecast")

st.info(
    "Forecasting method: Linear Regression. "
    "The forecast extends the historical monthly trend. "
    "Only 12 months of original data are available, so "
    "predictions are indicative, not guaranteed."
)

forecast_data = monthly_sales[
    monthly_sales["Sales"] > 0
].copy()

if len(forecast_data) < 4:
    st.warning(
        "At least four months with sales are required "
        "to generate a forecast. Expand the date range "
        "or adjust the filters."
    )
else:
    forecast_data["Month_Index"] = np.arange(
        len(forecast_data)
    )

    # Hold out the last three observations for a
    # simple chronological evaluation.
    train = forecast_data.iloc[:-3]
    test = forecast_data.iloc[-3:]

    evaluation_model = LinearRegression()

    evaluation_model.fit(
        train[["Month_Index"]],
        train["Sales"]
    )

    test_predictions = evaluation_model.predict(
        test[["Month_Index"]]
    )

    validation_mae = mean_absolute_error(
        test["Sales"],
        test_predictions
    )

    # Train the final model on all available months.
    final_model = LinearRegression()

    final_model.fit(
        forecast_data[["Month_Index"]],
        forecast_data["Sales"]
    )

    future_indices = np.arange(
        len(forecast_data),
        len(forecast_data) + forecast_horizon
    )

    future_dates = pd.date_range(
        start=forecast_data["Month"].max()
        + pd.offsets.MonthBegin(1),
        periods=forecast_horizon,
        freq="MS"
    )

    future_predictions = final_model.predict(
        future_indices.reshape(-1, 1)
    )

    # Sales cannot be negative.
    future_predictions = np.maximum(
        future_predictions, 0
    )

    forecast_df = pd.DataFrame({
        "Month": future_dates,
        "Forecast Sales": future_predictions
    })

    metric_col1, metric_col2 = st.columns(2)

    metric_col1.metric(
        "Holdout MAE",
        f"₹{validation_mae:,.0f}"
    )

    metric_col2.metric(
        "Average Forecast Sales",
        f"₹{forecast_df['Forecast Sales'].mean():,.0f}"
    )

    fig_forecast = go.Figure()

    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_data["Month"],
            y=forecast_data["Sales"],
            mode="lines+markers",
            name="Historical Sales"
        )
    )

    # Connect the forecast to the last historical point.
    forecast_x = [
        forecast_data["Month"].iloc[-1]
    ] + forecast_df["Month"].tolist()

    forecast_y = [
        forecast_data["Sales"].iloc[-1]
    ] + forecast_df["Forecast Sales"].tolist()

    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_x,
            y=forecast_y,
            mode="lines+markers",
            name="Forecast",
            line=dict(dash="dash")
        )
    )

    fig_forecast.update_layout(
        title="Historical Sales vs Future Forecast",
        xaxis_title="Month",
        yaxis_title="Sales (₹)",
        hovermode="x unified",
        yaxis_tickprefix="₹"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

    st.markdown("**Forecast Values**")

    display_forecast = forecast_df.copy()
    display_forecast["Forecast Sales"] = (
        display_forecast["Forecast Sales"]
        .map(lambda value: f"₹{value:,.2f}")
    )

    st.dataframe(
        display_forecast,
        use_container_width=True,
        hide_index=True
    )

    csv_data = forecast_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download Forecast CSV",
        data=csv_data,
        file_name="indian_business_sales_forecast.csv",
        mime="text/csv"
    )


# --------------------------------------------------
# CATEGORY PERFORMANCE
# --------------------------------------------------

st.divider()
st.subheader("Category Performance")

category_sales = (
    filtered_df.groupby("Category", as_index=False)
    .agg(
        Sales=("Amount", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Sales", ascending=False)
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Product Category",
    labels={"Sales": "Sales (₹)"}
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# --------------------------------------------------
# STATE-WISE SALES
# --------------------------------------------------

st.subheader("State-wise Sales Analysis")

state_sales = (
    filtered_df.groupby("State", as_index=False)
    .agg(
        Sales=("Amount", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Sales", ascending=False)
)

fig_state = px.bar(
    state_sales,
    x="State",
    y="Sales",
    color="Profit",
    title="Sales Distribution Across States",
    labels={"Sales": "Sales (₹)", "Profit": "Profit (₹)"}
)

st.plotly_chart(
    fig_state,
    use_container_width=True
)


# --------------------------------------------------
# DETAILED DATA
# --------------------------------------------------

st.divider()
st.subheader("Filtered Order Records")

st.dataframe(
    filtered_df.sort_values(
        "Order Date", ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Forecasts are trend-based estimates and should "
    "not be treated as guaranteed future sales."
)

st.success(
    "Dashboard loaded successfully. "
    "Use the sidebar to explore the business data."
)
