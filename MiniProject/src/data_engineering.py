import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def perform_data_engineering(modis_path, sentinel_path, weather_path):
    print("Loading datasets...")
    modis_df = pd.read_csv(modis_path)
    sentinel_df = pd.read_csv(sentinel_path)
    weather_df = pd.read_csv(weather_path)
    
    # 1. Spatial Alignment (Merge MODIS and Sentinel on sensor_id)
    print("Merging spatial datasets...")
    spatial_df = pd.merge(modis_df, sentinel_df, on='sensor_id')
    
    # 2. Temporal Synchronization (Merge spatial with weather on timestamp)
    # Ensure datetime format
    spatial_df['timestamp'] = pd.to_datetime(spatial_df['timestamp'])
    weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'])
    
    # Sort and merge asof or exact
    print("Synchronizing temporal datasets...")
    df = pd.merge(spatial_df, weather_df, on='timestamp', how='left')
    
    # 3. Missing Value Imputation (KNN on NDVI/NDBI)
    print("Imputing missing values using KNN...")
    imputer = KNNImputer(n_neighbors=5)
    cols_to_impute = ['NDVI', 'NDBI', 'albedo']
    df[cols_to_impute] = imputer.fit_transform(df[cols_to_impute])
    
    # 4. Feature Engineering: Temperature difference (UHI intensity proxy)
    df['UHI_intensity'] = df['LST_day'] - df['ambient_temp']
    
    # 5. Extract temporal features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_year'] = df['timestamp'].dt.dayofyear
    
    return df

if __name__ == "__main__":
    df = perform_data_engineering(
        "../dataset/modis_lst.csv", 
        "../dataset/sentinel_features.csv", 
        "../dataset/historical_weather.csv"
    )
    df.to_csv("../dataset/processed_urban_heat.csv", index=False)
    print("Data Engineering pipeline completed.")
