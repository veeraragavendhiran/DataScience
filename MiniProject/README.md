# UrbanHeat: Data Analysis of Urban Heat Island Effects

## Abstract
Urban areas experience significantly higher temperatures than rural counterparts due to dense infrastructure and human activities. This project identifies urban heat island (UHI) zones, analyzes temperature variations using remote sensing data, and offers actionable climate insights aligned with SDG 13 (Climate Action).

## Project Workflow
1. **Data Acquisition**: Synthetic data generation mirroring NASA MODIS, Sentinel-2, and OpenWeatherMap.
2. **Data Engineering**: Spatial-temporal alignment, KNN imputation, feature engineering (NDVI, UHI intensity).
3. **Exploratory Data Analysis**: Time-series analysis, correlation matrices, LST vs. Vegetation analysis.
4. **Geospatial Analysis**: DBSCAN clustering of UHI hotspots visually plotted using GeoPandas.
5. **Modeling**: Machine learning prediction modeling (Linear Regression, Random Forest, XGBoost) to predict day-time land surface temperatures based on environmental and physical features.
6. **Insight Generation**: Top heat zones, vegetation cooling impact, interactive Streamlit dashboard.

## Folder Structure
- `dataset/`: Contains raw and processed CSV data.
- `notebooks/`: Jupyter Notebook containing EDA and Modeling.
- `src/`: Python source code scripts for data pipelines.
- `outputs/`: Generated graphs and model results.
- `docs/`: Additional documentation.
- `report/`: IEEE format project report.

## Tools Used
- pandas, numpy, scikit-learn
- matplotlib, seaborn, geopandas
- xgboost, streamlit
