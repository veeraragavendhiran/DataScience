import pandas as pd
import numpy as np
import os

def generate_datasets(output_dir="dataset/"):
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)
    
    # 1. MODIS Land Surface Temperature (LST) Dataset
    n_samples = 1000
    lat_base = 34.0522  # Los Angeles center
    lon_base = -118.2437
    
    lats = lat_base + np.random.uniform(-0.5, 0.5, n_samples)
    lons = lon_base + np.random.uniform(-0.5, 0.5, n_samples)
    
    # Calculate distance from center to simulate urban core (heat island)
    dist_from_center = np.sqrt((lats - lat_base)**2 + (lons - lon_base)**2)
    
    # Base temperature 25C, urban core up to +7C hotter
    lst = 25.0 + (0.5 - dist_from_center) * 14.0 + np.random.normal(0, 1.5, n_samples)
    
    modis_df = pd.DataFrame({
        'sensor_id': [f"M_{i}" for i in range(n_samples)],
        'latitude': lats,
        'longitude': lons,
        'LST_day': lst,
        'LST_night': lst - 8.0 + np.random.normal(0, 1.0, n_samples), # Cooler at night
        'timestamp': pd.date_range(start='2023-01-01', periods=n_samples, freq='h')
    })
    
    # 2. Sentinel-2 Urban Features (NDVI, NDBI)
    # Inverse relationship with LST: vegetation cools, built-up area heats
    ndvi = 0.8 - (0.5 - dist_from_center) * 1.2 + np.random.normal(0, 0.1, n_samples)
    ndvi = np.clip(ndvi, -0.1, 0.9)
    
    ndbi = 0.2 + (0.5 - dist_from_center) * 1.0 + np.random.normal(0, 0.1, n_samples)
    ndbi = np.clip(ndbi, -0.2, 0.8)
    
    sentinel_df = pd.DataFrame({
        'sensor_id': modis_df['sensor_id'].values,
        'NDVI': ndvi,
        'NDBI': ndbi,
        'albedo': np.random.uniform(0.1, 0.4, n_samples)
    })
    
    # Add some missing values for data engineering
    idx_missing = np.random.choice(n_samples, 50, replace=False)
    sentinel_df.loc[idx_missing, 'NDVI'] = np.nan
    
    # 3. OpenWeatherMap Historical (Ambient Temperature)
    weather_df = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=n_samples, freq='h'),
        'ambient_temp': 22.0 + np.sin(np.linspace(0, 10*np.pi, n_samples)) * 5 + np.random.normal(0, 1, n_samples),
        'humidity': np.random.uniform(30, 80, n_samples),
        'wind_speed': np.random.uniform(0, 10, n_samples)
    })
    
    modis_df.to_csv(os.path.join(output_dir, "modis_lst.csv"), index=False)
    sentinel_df.to_csv(os.path.join(output_dir, "sentinel_features.csv"), index=False)
    weather_df.to_csv(os.path.join(output_dir, "historical_weather.csv"), index=False)
    
    print(f"Datasets generated successfully in {output_dir}")

if __name__ == "__main__":
    import sys
    base_dir = sys.argv[1] if len(sys.argv) > 1 else "../dataset/"
    generate_datasets(base_dir)
