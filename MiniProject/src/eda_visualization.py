import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def eda_pipeline(data_path, output_dir="../outputs/graphs/"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    
    # Heatmap of correlations
    plt.figure(figsize=(10, 8))
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix of Urban Heat Variables")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "correlation_matrix.png"))
    plt.close()
    
    # Time-series of Temperatures
    plt.figure(figsize=(12, 6))
    subset = df.head(168) # first week
    plt.plot(subset['timestamp'], subset['LST_day'], label='LST (Day)', color='red')
    plt.plot(subset['timestamp'], subset['ambient_temp'], label='Ambient Temp', color='blue')
    plt.title("Temperature Time-Series (First Week)")
    plt.xlabel("Time")
    plt.ylabel("Temperature (Celsius)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "temperature_timeseries.png"))
    plt.close()
    
    # LST vs NDVI scatter
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='NDVI', y='LST_day', data=df, alpha=0.5, hue='UHI_intensity', palette='inferno')
    plt.title("LST vs NDVI (Vegetation Index)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "lst_vs_ndvi.png"))
    plt.close()
    
    print(f"EDA Visualization completed. Graphs saved to {output_dir}")

if __name__ == "__main__":
    eda_pipeline("../dataset/processed_urban_heat.csv")
