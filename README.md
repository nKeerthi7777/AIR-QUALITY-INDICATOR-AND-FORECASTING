# AIR-QUALITY-INDICATOR-AND-FORECASTING
“Air Quality Dashboard”, aims to provide an interactive and insightful platform for analyzing the Air Quality Index (AQI) of various Indian cities. Using historical AQI data, the dashboard enables users to visualize monthly trends, identify pollution hotspots, and assess health risks based on pollutant levels.

----------------------------------------------------------------------------------

## 📌 Project Overview

Air pollution has become a severe environmental challenge in urban India. This dashboard helps users—citizens, researchers, and policy-makers—track air quality trends and prepare for future pollution levels.

**Key Features:**
- 📈 Monthly AQI trends by city and pollutant
- 🗺️ Interactive geospatial AQI map using Folium
- 🔮 30-day AQI forecasting using Prophet
- 📤 Filtered data export in CSV format
- 🌙 Dark-themed UI for visual clarity

------------------------------------------------------------------------------------

## 🧠 Technologies Used

- **Python 3.7+**
- **Streamlit** – for the web interface
- **Pandas** – data manipulation
- **Plotly** – interactive line plots
- **Folium** – map-based AQI visualization
- **Prophet** – time series forecasting
- **PyDeck** – (optional) mapping extensions

----------------------------------------------------------------

## 🗃️ Dataset

- **File**: `city_day_cleaned.csv`
- **Source**: Central Pollution Control Board (https://www.cpcb.nic.in), OpenAQ (https://openaq.org)
- **Attributes**: Date, City, AQI, and pollutant values (PM2.5, PM10, NO2, CO, SO2, O3)

------------------------------------------------------------------

## 🔧 Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/air-quality-dashboard.git
   cd air-quality-dashboard

2.Install Dependencies
  (Recommended: Create a virtual environment)
  
    pip install -r requirements.txt

3.Run the App

    streamlit run app.py
---------------------------------------------------------------------
📷 Screenshots
You can insert screenshots here to showcase:


Trend visualization
<img width="1904" height="870" alt="Screenshot 2025-07-17 213831" src="https://github.com/user-attachments/assets/28239335-e702-4cf8-9e56-586528314a20" />

AQI map
<img width="1907" height="860" alt="Screenshot 2025-07-17 214011" src="https://github.com/user-attachments/assets/64bfb783-7e4b-48f2-8f8d-507cf2a92973" />

Forecast plots
<img width="1904" height="850" alt="Screenshot 2025-07-17 214035" src="https://github.com/user-attachments/assets/205d1934-598e-4acc-9b99-710b764ce777" />


--------------------------------------------------------------------------------------
📊 Application Modules
1. AQI Trends
Interactive time-series plots of pollutant levels using Plotly, filterable by city, pollutant, and date range.

2. AQI Map
Real-time air quality across cities using Folium with color-coded health risk indicators.

3. Forecast
30-day AQI prediction using Facebook Prophet to assist in environmental planning.

4. Export
Download filtered datasets for further analysis or reporting in CSV format.

---------------------------------------------------------------------------------------
### ✅ System Requirements

**💻 Software**
- Python 3.7+
- Streamlit
- Jupyter / VS Code (optional for development)
- Web browser (Chrome / Firefox)

**🖥️ Hardware**
- Dual-core CPU
- 4–8 GB RAM
- 1+ GB storage
- Internet connection (for initial setup)

---

### 🚀 Future Enhancements
- Real-time data integration via APIs
- Mobile responsiveness
- Email alerts for severe AQI
- Dashboard hosting (e.g., Streamlit Cloud / Heroku)


