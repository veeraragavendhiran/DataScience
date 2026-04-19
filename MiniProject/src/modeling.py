import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import json
import os

def evaluate(y_true, y_pred, name):
    return {
        "Model": name,
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAE": mean_absolute_error(y_true, y_pred),
        "R2": r2_score(y_true, y_pred)
    }

def modeling_pipeline(data_path, output_dir="../outputs/results/"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    
    # Predict LST_day based on other features
    features = ['ambient_temp', 'humidity', 'wind_speed', 'NDVI', 'NDBI', 'albedo']
    X = df[features].fillna(0)
    y = df['LST_day']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    results = []
    
    # 1. Baseline: Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    results.append(evaluate(y_test, lr.predict(X_test), "Linear Regression"))
    
    # 2. Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X_train, y_train)
    results.append(evaluate(y_test, rf.predict(X_test), "Random Forest"))
    
    # 3. XGBoost
    xg_reg = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=50, random_state=42)
    xg_reg.fit(X_train, y_train)
    results.append(evaluate(y_test, xg_reg.predict(X_test), "XGBoost"))
    
    # Determine feature importances from RF
    importances = list(zip(features, rf.feature_importances_))
    importances.sort(key=lambda x: x[1], reverse=True)
    
    # Save results
    with open(os.path.join(output_dir, "model_metrics.json"), "w") as f:
        json.dump(results, f, indent=4)
        
    with open(os.path.join(output_dir, "feature_importances.json"), "w") as f:
        json.dump(importances, f, indent=4)
        
    print("Modeling pipeline completed.")
    print("Results:", results)

if __name__ == "__main__":
    modeling_pipeline("../dataset/processed_urban_heat.csv")
