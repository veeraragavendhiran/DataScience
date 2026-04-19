import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import DBSCAN
import os

def geospatial_pipeline(data_path, output_dir="../outputs/graphs/"):
    df = pd.read_csv(data_path)
    
    # Create GeoDataFrame
    geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    
    # Clustering Hotspots with DBSCAN
    # Extract points with high UHI intensity for clustering
    high_heat = gdf[gdf['UHI_intensity'] > gdf['UHI_intensity'].quantile(0.75)]
    coords = high_heat[['latitude', 'longitude']].values
    
    db = DBSCAN(eps=0.05, min_samples=5).fit(coords)
    high_heat['cluster'] = db.labels_
    
    # To keep it simple (as Folium maps might need browser to view), we'll do matplotlib basic map
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 8))
    gdf.plot(ax=ax, column='UHI_intensity', legend=True, cmap='OrRd', markersize=50, alpha=0.7)
    plt.title("Spatial Distribution of UHI Intensity")
    plt.savefig(os.path.join(output_dir, "uhi_spatial_distribution.png"))
    plt.close()
    
    # Save hotspots
    hotspots = high_heat[high_heat['cluster'] != -1]
    hotspots.to_csv(os.path.join(output_dir, "identified_hotspots.csv"), index=False)
    
    print("Geospatial analysis completed.")

if __name__ == "__main__":
    geospatial_pipeline("../dataset/processed_urban_heat.csv")
