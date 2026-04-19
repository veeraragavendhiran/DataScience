import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("UrbanHeat: Data Analysis of Urban Heat Island Effects")

st.markdown("""
This dashboard provides a visualization of the Urban Heat Island (UHI) analysis,
combining MODIS LST, Sentinel-2 Vegetation data, and OpenWeatherMap metrics.
""")

@st.cache_data
def load_data():
    try:
        return pd.pd.read_csv("../dataset/processed_urban_heat.csv")
    except:
        return None

df = load_data()

if df is not None:
    st.header("Dataset Overview")
    st.dataframe(df.head())
    
    st.header("Temperature Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['LST_day'], bins=30, kde=True, ax=ax, color='red', label='Day LST')
    sns.histplot(df['LST_night'], bins=30, kde=True, ax=ax, color='blue', label='Night LST')
    plt.legend()
    st.pyplot(fig)
    
    st.header("UHI vs Vegetation (NDVI)")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='NDVI', y='UHI_intensity', data=df, alpha=0.5, ax=ax2)
    st.pyplot(fig2)
else:
    st.warning("Data not generated yet. Please run the engineering pipeline.")
