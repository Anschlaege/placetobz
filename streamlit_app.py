import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# 1. Configuration & Styling
st.set_page_config(page_title="Venosta Agro-Ecological Sentinel", layout="wide")
st.title("🍏 Venosta Valley: Agro-Ecological Explorer")
st.sidebar.header("Control Panel")

# 2. User Persona Selector
user_mode = st.sidebar.radio("Select View Mode:",)

# 3. Data Integration (Based on Research Data)
# Municipalities of the Venosta district
# Data simulates relative biological health trends found in Eurac BMS & Laimburg studies
vinschgau_data = pd.DataFrame({
    'Municipality':,
    'Organic_Share': [0.10, 0.05, 0.20, 0.12, 0.15, 0.75, 0.05, 0.18, 0.10, 0.40, 0.05, 0.05, 0.10],
    'Species_Richness': , # Higher in organic/high-altitude zones [1]
    'Soil_Carbon': [2.1, 5.8, 3.8, 2.5, 2.8, 5.5, 5.1, 2.3, 2.4, 4.2, 5.8, 5.5, 4.8] # Higher in organic systems 
})

# 4. Atmospheric Drift Simulator Logic
st.sidebar.subheader("Atmospheric Drift Simulator")
wind_speed = st.sidebar.slider("Valley Wind Intensity (km/h):", 0, 50, 15)
thermal_updraft = st.sidebar.select_slider("Thermal Condition:", options=)

def predict_peak_contamination(wind, thermal):
    # Research identified 27 substances transported to peaks
    base_load = 27 
    multiplier = 1.2 if thermal == "Strong" else 1.0
    return round(base_load * (wind / 10) * multiplier)

# 5. Map Visualization
st.subheader("Geospatial Landscape Analysis")
m = folium.Map(location=[46.615, 10.705], zoom_start=11, tiles="CartoDB positron")

# Overlay: Buffer Zone Simulation for Residents
if user_mode == "Resident/Tourist":
    st.info("Visualizing current 30m legal buffer vs. the 100m distance recommended to minimize pediatric exposure.")
    # Coordinates for representative sensitive sites (e.g., Mals and Silandro)
    sensitive_sites =,]
    for lat, lon, name in sensitive_sites:
        folium.Circle([lat, lon], radius=30, color='red', fill=True, popup=f"{name}: Current 30m Legal Buffer").add_to(m)
        folium.Circle([lat, lon], radius=100, color='green', fill=False, popup=f"{name}: Scientific 100m Safety Limit").add_to(m)

st_folium(m, width=1200, height=500)

# 6. Biological Health Dashboard [1, 2]
st.divider()
st.subheader("Biological Health Metrics: Organic vs. Conventional Efficiency")
col1, col2 = st.columns(2)

with col1:
    fig_species = px.bar(vinschgau_data, x='Municipality', y='Species_Richness', 
                         title="Biodiversity Index (Butterfly & Bee Indicators)",
                         color='Organic_Share', color_continuous_scale='Greens',
                         labels={'Species_Richness': 'Species Count', 'Organic_Share': 'Organic %'})
    st.plotly_chart(fig_species, use_container_width=True)

with col2:
    fig_soil = px.scatter(vinschgau_data, x='Organic_Share', y='Soil_Carbon', 
                          size='Species_Richness', hover_name='Municipality',
                          title="Correlation: Organic Share vs. Soil Organic Matter",
                          labels={'Organic_Share': 'Organic Land Share', 'Soil_Carbon': 'Soil Organic Matter %'})
    st.plotly_chart(fig_soil, use_container_width=True)

# 7. Policy Insight
if user_mode == "Policy Maker / Researcher":
    st.sidebar.divider()
    st.sidebar.warning("Target: 50% Reduction by 2030 (Farm to Fork Strategy)")
    drift_risk = predict_peak_contamination(wind_speed, thermal_updraft)
    st.metric("Predicted High-Altitude Contaminants", f"{drift_risk} Substances")
    st.write("Over 590,000 spray applications per season ensure landscape-wide presence of 'chemical cocktails'.[3]")
    st.write("Even remote peaks in Stelvio National Park show residues of 27 different pesticides.")
