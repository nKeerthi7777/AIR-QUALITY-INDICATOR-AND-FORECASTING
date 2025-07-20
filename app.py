import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
from prophet import Prophet
import folium
from streamlit_folium import folium_static
from folium.plugins import FloatImage
from datetime import datetime

st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

# --- Force Dark Theme ---
st.markdown(
    """
    <style>
    body { background-color: #1E1E1E; color: white; }
    .stApp { background-color: #1E1E1E; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load Data ---
@st.cache_data

def load_data():
    df = pd.read_csv("city_day_cleaned.csv", parse_dates=["Date"])
    return df

df = load_data()

# --- Sidebar Filters ---
cities = df['City'].unique()
selected_city = st.sidebar.selectbox("Choose a city", sorted(cities))
city_df = df[df['City'] == selected_city]

min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input("Select date range", [min_date, max_date], min_value=min_date, max_value=max_date)

pollutant = st.sidebar.selectbox("Select pollutant", ["AQI", "PM2.5", "PM10", "NO2", "CO", "SO2", "O3"])

# --- Filter Data ---
filtered_df = city_df[(city_df['Date'] >= pd.to_datetime(date_range[0])) & (city_df['Date'] <= pd.to_datetime(date_range[1]))]

# --- Health Risk Scoring ---
def get_health_risk(aqi):
    if pd.isna(aqi):
        return "No Data", "gray"
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Moderate", "yellow"
    elif aqi <= 200:
        return "Unhealthy for Sensitive Groups", "orange"
    elif aqi <= 300:
        return "Unhealthy", "red"
    elif aqi <= 400:
        return "Very Unhealthy", "purple"
    else:
        return "Hazardous", "maroon"

latest_aqi_value = city_df.sort_values("Date", ascending=False)["AQI"].dropna().iloc[0]
risk_label, risk_color = get_health_risk(latest_aqi_value)

st.sidebar.markdown(f"### Health Risk: **{risk_label}**")
st.sidebar.markdown(f"<div style='color:{risk_color}; font-weight:bold;'>AQI: {latest_aqi_value:.0f}</div>", unsafe_allow_html=True)

# --- Tabs Layout ---
tab1, tab2, tab3, tab4 = st.tabs(["AQI Trends", "Map", "Forecast", "Export"])

# --- Tab 1: AQI Trends ---
with tab1:
    st.title(f"{pollutant} Trends – {selected_city}")
    df_monthly = filtered_df.copy()
    df_monthly["YearMonth"] = df_monthly["Date"].dt.to_period("M")
    monthly_avg = df_monthly.groupby("YearMonth")[pollutant].mean().reset_index()
    monthly_avg["YearMonth"] = monthly_avg["YearMonth"].astype(str)

    fig = px.line(monthly_avg, x="YearMonth", y=pollutant, markers=True, title=f"{pollutant} Trend in {selected_city}")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 2: Map ---
with tab2:
    st.title("AQI Map")
    latest_dates = df.groupby("City")["Date"].max().reset_index()
    latest_aqi = pd.merge(latest_dates, df, on=["City", "Date"])
    latest_aqi = latest_aqi.dropna(subset=["AQI"])

    city_coords = {
        "Delhi": [28.61, 77.23],
        "Mumbai": [19.07, 72.87],
        "Kolkata": [22.57, 88.36],
        "Chennai": [13.08, 80.27],
        "Bengaluru": [12.97, 77.59],
        "Ahmedabad": [23.03, 72.58],
        "Hyderabad": [17.38, 78.48],
        "Pune": [18.52, 73.85],
        "Lucknow": [26.85, 80.95],
        "Jaipur": [26.92, 75.82]
    }

    latest_aqi["lat"] = latest_aqi["City"].map(lambda x: city_coords.get(x, [0, 0])[0])
    latest_aqi["lon"] = latest_aqi["City"].map(lambda x: city_coords.get(x, [0, 0])[1])
    latest_aqi = latest_aqi[(latest_aqi["lat"] != 0) & (latest_aqi["lon"] != 0)]

    map_center = [21.0, 78.0]
    m = folium.Map(location=map_center, zoom_start=5, tiles='CartoDB dark_matter')

    for _, row in latest_aqi.iterrows():
        label, color = get_health_risk(row["AQI"])
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{row['City']}: AQI {row['AQI']} ({label})"
        ).add_to(m)

    # Add Legend
    legend_html = '''
     <div style="position: fixed; 
     bottom: 50px; left: 50px; width: 200px; height: 200px; 
     background-color: white; z-index:9999; font-size:14px;
     border:2px solid grey; border-radius:10px; padding: 10px;">
     <b>AQI Legend</b><br>
     <i style="background:green;">&nbsp;&nbsp;&nbsp;</i> Good (0-50)<br>
     <i style="background:yellow;">&nbsp;&nbsp;&nbsp;</i> Moderate (51-100)<br>
     <i style="background:orange;">&nbsp;&nbsp;&nbsp;</i> Unhealthy for Sensitive (101-200)<br>
     <i style="background:red;">&nbsp;&nbsp;&nbsp;</i> Unhealthy (201-300)<br>
     <i style="background:purple;">&nbsp;&nbsp;&nbsp;</i> Very Unhealthy (301-400)<br>
     <i style="background:maroon;">&nbsp;&nbsp;&nbsp;</i> Hazardous (401+)<br>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))
    folium_static(m)

# --- Tab 3: Forecast ---
with tab3:
    st.title(f"Forecast AQI for {selected_city}")
    forecast_df = filtered_df[["Date", "AQI"]].dropna()
    forecast_df = forecast_df.rename(columns={"Date": "ds", "AQI": "y"})

    model = Prophet()
    model.fit(forecast_df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    fig_forecast = px.line(forecast, x='ds', y='yhat', title=f"30-Day AQI Forecast for {selected_city}")
    fig_forecast.update_layout(template="plotly_dark")
    st.plotly_chart(fig_forecast, use_container_width=True)

# --- Tab 4: Export ---
with tab4:
    st.title("Download Data")
    st.write("Download the filtered data below:")
    st.download_button(
        label="Download as CSV",
        data=filtered_df.to_csv(index=False),
        file_name=f"{selected_city}_filtered_aqi.csv",
        mime="text/csv"
    )