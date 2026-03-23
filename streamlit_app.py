import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# 1. Configuration & Styling
st.set_page_config(page_title="Venosta Agro-Ecological Sentinel", layout="wide")
st.title("🍏 Venosta Valley: Agro-Ecological Explorer")
st.sidebar.header("Control Panel")

# 2. User Persona Selector - FIXED: Added the required options list
user_mode = st.sidebar.radio("Select View Mode:", ["Resident/Tourist", "Policy Maker / Researcher"])

# 3. Data Load
# FIXED: Added 13 placeholder municipalities and 13 species richness values to match the other columns
vinschgau_data = pd.DataFrame({
    'Municipality': ['Mals', 'Schlanders', 'Latsch', 'Prad', 'Laas', 'Kastelbell', 'Graun', 'Glurns', 'Schluderns', 'Martell', 'Schnals', 'Stilfs', 'Taufers'],
    'Organic_Share': [0.05, 0.15, 0.12, 0.10, 0.05, 0.75, 0.18, 0.40, 0.20, 0.15, 0.05, 0.05, 0.10],
    'Species_Richness': [45, 50, 48, 42, 44, 85, 55, 70, 60, 58, 40, 41, 46],
    'Soil_Carbon': [2.1, 5.5, 2.3, 1.9, 2.4, 5.8, 4.2, 5.1, 2.8, 3.8, 5.5, 4.8, 5.2]
})

# 4. Atmospheric Drift Simulator Logic
st.sidebar.subheader("Atmospheric Drift Simulator")
wind_speed = st.sidebar.slider("Valley Wind Intensity (km/h):", 0, 50, 15)
# FIXED: Added options for the select slider based on your multiplier logic
thermal_updraft = st.sidebar.select_slider("Thermal Condition:", options=["Weak", "Moderate", "Strong"])

def predict_peak_contamination(wind, thermal):
    # Research identified 27 substances transported to peaks via thermal updrafts
    base_load = 27 
    multiplier = 1.2 if thermal == "Strong" else 1.0
    return round(base_load * (wind / 15) * multiplier)

# 5. Map Visualization
st.subheader("Geospatial Landscape Analysis")
m = folium.Map(location=[46.615, 10.705], zoom_start=11, tiles="CartoDB positron")

# FIXED: Added representative coordinates for sensitive sites
sensitive_sites = [
    (46.632, 10.710, "Local School"), 
    (46.601, 10.680, "Public Playground")
]

# Overlay: Buffer Zone Simulation
if user_mode == "Resident/Tourist":
    st.info("Visualizing current 30m legal buffer vs. the 100m distance recommended by scientists.")
    for lat, lon, name in sensitive_sites:
        folium.Circle([lat, lon], radius=30, color='red', fill=True, popup=f"{name}: 30m Legal Limit").add_to(m)
        folium.Circle([lat, lon], radius=100, color='green', fill=False, popup=f"{name}: 100m Safety Goal").add_to(m)
        folium.Marker([lat, lon], tooltip=name).add_to(m)
else:
    # Choropleth simulation: Highlighting organic hubs for policy makers
    for i, row in vinschgau_data.iterrows():
        folium.CircleMarker(
            location=[46.62 - (i*0.01), 10.6 + (i*0.02)],
            radius=10,
            # FIXED: Specified row['Organic_Share'] instead of just 'row'
            popup=f"{row['Municipality']}: {row['Organic_Share']*100}% Organic",
            color='green' if row['Organic_Share'] > 0.3 else 'blue',
            fill=True
        ).add_to(m)

st_folium(m, width=1200, height=500)

# 6. Biological Health Dashboard
st.divider()
st.subheader("Biological Health Metrics: Organic vs. Integrated Effectiveness")
col1, col2 = st.columns(2)

with col1:
    fig_species = px.bar(vinschgau_data, x='Municipality', y='Species_Richness', 
                         title="Biodiversity Index (Butterfly & Bee Indicators)",
                         color='Organic_Share', color_continuous_scale='Greens',
                         labels={'Species_Richness': 'Indicator Species Count'})
    st.plotly_chart(fig_species, use_container_width=True)

with col2:
    fig_soil = px.scatter(vinschgau_data, x='Organic_Share', y='Soil_Carbon', 
                          size='Species_Richness', hover_name='Municipality',
                          title="Correlation: Organic Share vs. Soil Vitality (SOM %)",
                          labels={'Organic_Share': 'Organic Land Share %', 'Soil_Carbon': 'Soil Organic Matter %'})
    st.plotly_chart(fig_soil, use_container_width=True)

# 7. Policy Insight
if user_mode == "Policy Maker / Researcher":
    st.sidebar.divider()
    st.sidebar.warning("Target: 50% Reduction by 2030 (Farm to Fork Strategy)")
    drift_risk = predict_peak_contamination(wind_speed, thermal_updraft)
    st.metric("Predicted High-Altitude Contaminants", f"{drift_risk} Substances")
    st.write("Over 590,000 spray applications per season ensure landscape-wide presence of chemical cocktails.[3]")
    st.write("Current research confirms that 27 different pesticides travel from valleys to remote peaks.")
