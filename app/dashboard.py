import os
import yaml
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Fraud Intelligence Command Center",
    layout="wide"
)

sns.set_theme(style="darkgrid")

# ================== LOAD CONFIG ==================
CONFIG_PATH = os.path.join("config", "system_config.yaml")

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

RISK_THRESHOLD_DEFAULT = CONFIG["thresholds"]["high_risk"]

# ================== LOAD DATA ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "processed", "final_risk_table.csv")

df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ================== SIDEBAR ==================
st.sidebar.title("Risk Controls")

risk_threshold = st.sidebar.slider(
    "Minimum Risk Score",
    0.0, 1.0,
    RISK_THRESHOLD_DEFAULT,
    0.05
)

selected_clusters = st.sidebar.multiselect(
    "Fraud Patterns",
    sorted(df["cluster"].unique()),
    default=sorted(df["cluster"].unique())
)

selected_users = st.sidebar.multiselect(
    "Users",
    options=df["user_id"].unique()
)

show_only_fraud = st.sidebar.checkbox("Show Only Confirmed Fraud")

# ================== HEADER ==================
st.title("Fraud Intelligence Command Center")
st.caption("Live monitoring • Pattern intelligence • Explainable risk")
st.divider()

# ================== LIVE INTELLIGENCE ==================
left_col, right_col = st.columns([1.3, 2.7])

with left_col:
    st.subheader("Live Intelligence")

    date_range = st.date_input(
        "Analysis window",
        [df["timestamp"].min(), df["timestamp"].max()],
        min_value=df["timestamp"].min(),
        max_value=df["timestamp"].max()
    )

# ================== FILTER DATA ==================
filtered_df = df[
    (df["risk_score"] >= risk_threshold) &
    (df["cluster"].isin(selected_clusters)) &
    (df["timestamp"].between(
        pd.to_datetime(date_range[0]),
        pd.to_datetime(date_range[1])
    ))
]

if selected_users:
    filtered_df = filtered_df[filtered_df["user_id"].isin(selected_users)]

if show_only_fraud:
    filtered_df = filtered_df[filtered_df["is_fraud"] == 1]

if filtered_df.empty:
    st.warning("No activity detected — showing recent transactions.")
    filtered_df = df.sort_values("timestamp", ascending=False).head(1000)

# ================== KPIs ==================
with right_col:
    k1, k2, k3, k4 = st.columns(4)
    k5, k6, k7, k8 = st.columns(4)

    k1.metric("Transactions", f"{len(filtered_df):,}")
    k2.metric("High-Risk %", f"{(filtered_df['risk_score'] > 0.7).mean()*100:.1f}%")
    k3.metric("Avg Risk", f"{filtered_df['risk_score'].mean():.2f}")
    k4.metric("Active Users", filtered_df["user_id"].nunique())

    k5.metric("Median Risk", f"{filtered_df['risk_score'].median():.2f}")
    k6.metric("90th % Risk", f"{filtered_df['risk_score'].quantile(0.9):.2f}")
    k7.metric("Fraud Rate", f"{filtered_df['is_fraud'].mean()*100:.1f}%")
    k8.metric("Risk Volatility", f"{filtered_df['risk_score'].std():.2f}")

st.divider()

# ================== ALERTS + RISK DRIVERS ==================
alert_col, drivers_col = st.columns([1.3, 2.7])

with alert_col:
    if filtered_df["risk_score"].mean() > 0.65:
        st.error("Overall risk level elevated")

with drivers_col:
    st.subheader("Top Risk Drivers")

    if "risk_explanation" in filtered_df.columns:
        top_reasons = (
            filtered_df["risk_explanation"]
            .str.split(";")
            .explode()
            .value_counts()
            .head(4)
        )

        for reason, count in top_reasons.items():
            l, r = st.columns([4, 1])
            l.write(reason.strip())
            r.markdown(
                f"<div style='text-align:right; font-weight:600'>{count}</div>",
                unsafe_allow_html=True
            )

st.divider()

# ================== RISK TREND + BANDS ==================
colA, colB = st.columns([3, 2])

with colA:
    st.subheader("Risk Trend Over Time")

    risk_trend = (
        filtered_df
        .set_index("timestamp")
        .resample("D")["risk_score"]
        .mean()
    )

    st.line_chart(risk_trend)

with colB:
    st.subheader("Risk Evolution Bands")

    risk_band = (
        filtered_df
        .set_index("timestamp")
        .resample("D")["risk_score"]
        .agg(
            median="median",
            p10=lambda x: x.quantile(0.1),
            p90=lambda x: x.quantile(0.9)
        )
        .dropna()
    )

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(risk_band.index, risk_band["median"], label="Median", linewidth=2)
    ax.fill_between(
        risk_band.index,
        risk_band["p10"],
        risk_band["p90"],
        alpha=0.3,
        label="10–90% band"
    )
    ax.axhline(risk_threshold, linestyle="--", color="red")
    ax.legend()
    st.pyplot(fig)

st.divider()

# ================== RISK ACCELERATION ==================
st.subheader("Risk Acceleration")

risk_accel = risk_trend.diff()
st.line_chart(risk_accel)

st.divider()

# ================== FRAUD SHARE OVER TIME ==================
st.subheader("Fraud Share Over Time")

fraud_share = (
    filtered_df
    .set_index("timestamp")
    .resample("D")["is_fraud"]
    .mean()
)

st.line_chart(fraud_share)

st.divider()

# ================== USER RISK CONCENTRATION ==================
st.subheader("User Risk Concentration")

user_risk = (
    filtered_df.groupby("user_id")["risk_score"]
    .mean()
    .sort_values(ascending=False)
)

st.area_chart(user_risk.head(50))

st.divider()

# ================== FRAUD PATTERN RISK (LOLLIPOP) ==================
st.subheader("Fraud Pattern Risk Profile")

cluster_risk = (
    filtered_df.groupby("cluster")["risk_score"]
    .mean()
    .sort_values()
)

fig, ax = plt.subplots(figsize=(6, 3))
ax.hlines(cluster_risk.index.astype(str), 0, cluster_risk.values)
ax.plot(cluster_risk.values, cluster_risk.index.astype(str), "o")
ax.set_xlim(0, 1)
ax.set_xlabel("Average Risk Score")
st.pyplot(fig)

st.divider()

# ================== TABLE ==================
st.subheader("High-Risk Transactions")

st.dataframe(
    filtered_df[
        [
            "user_id",
            "timestamp",
            "amount",
            "risk_score",
            "risk_explanation",
            "cluster"
        ]
    ]
    .sort_values("risk_score", ascending=False)
    .head(50),
    use_container_width=True
)

st.caption(
    "Fully interactive fraud intelligence dashboard • "
    "Designed for real-world analyst workflows"
)
