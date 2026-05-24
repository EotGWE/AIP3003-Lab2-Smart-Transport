import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("smart_transport_dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.title("Smart Transportation Performance Dashboard")

st.sidebar.header("Filter Options")
day_type_filter = st.sidebar.multiselect(
    "Select Day Type",
    options=df["Day_Type"].unique(),
    default=df["Day_Type"].unique()
)

route_filter = st.sidebar.multiselect(
    "Select Route",
    options=sorted(df["Route"].unique()),
    default=df["Route"].unique()
)

filtered_df = df[df["Day_Type"].isin(day_type_filter) & df["Route"].isin(route_filter)]

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Ridership", f"{filtered_df['Ridership'].sum():,}")
kpi2.metric("Average Delay (Mins)", f"{filtered_df['Delay_Minutes'].mean():.2f}")
kpi3.metric("Average Satisfaction", f"{filtered_df['Satisfaction_Score'].mean():.2f} / 5")

col1, col2 = st.columns(2)
with col1:
    fig_delay = px.bar(
        filtered_df.groupby("Route")["Delay_Minutes"].mean().reset_index(),
        x="Route", y="Delay_Minutes",
        title="Average Delay by Route",
        labels={"Delay_Minutes": "Average Delay (Minutes)"}
    )
    st.plotly_chart(fig_delay, use_container_width=True)

with col2:
    fig_sat = px.bar(
        filtered_df.groupby("Route")["Satisfaction_Score"].mean().reset_index(),
        x="Route", y="Satisfaction_Score",
        title="Average Satisfaction Score by Route",
        labels={"Satisfaction_Score": "Average Satisfaction"}
    )
    st.plotly_chart(fig_sat, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    fig_area = px.bar(
        filtered_df.groupby("Area")["Ridership"].sum().reset_index(),
        x="Area", y="Ridership",
        title="Total Ridership by Area",
        labels={"Ridership": "Total Ridership"}
    )
    st.plotly_chart(fig_area, use_container_width=True)

with col4:
    fig_scatter = px.scatter(
        filtered_df, x="Ridership", y="Delay_Minutes",
        color="Route", title="Ridership vs. Delay",
        labels={"Ridership": "Ridership", "Delay_Minutes": "Delay (Minutes)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

df_trend = filtered_df.groupby(filtered_df["Date"].dt.date)[["Ridership", "Delay_Minutes"]].mean().reset_index()
fig_trend = px.line(
        df_trend, x="Date", y=["Ridership", "Delay_Minutes"],
        title="Trend Analysis Over Time",
        labels={"value": "Metrics Value", "variable": "KPI"}
)
st.plotly_chart(fig_trend, use_container_width=True)
