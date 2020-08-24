# Standard libraries
import pandas as pd
import numpy as np
from joblib import dump

# Scikit-learn libraries
# from sklearn.preprocessing import StandardScaler, OneHotEncoder, MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
# from sklearn import base

from model import Preprocesser, OneHotList, MultiOneHot, MultiStandardScaler

def train():
    # Load data
    db_path = "./data/combined_db_las_vegas.csv"
    df_data = pd.read_csv(db_path, parse_dates=["checkin_datetime", "checkout_datetime"])

    feature_cols = ["num_reviews", "rating", "days_from_search", 
                "distance_centre", "rating_sentiment", "amenities", "star_rating",
                #"price_sale",  
                "checkin_datetime"
               ]

    df_features = df_data[feature_cols]#.sort_values("checkin_datetime")
    df_features["checkin_datetime"] = df_data["checkin_datetime"].dt.date#.sort_values("checkin_datetime")
    df_target = df_data["price"]

    # Train
    amenities_classes = ['Free parking', 'Pool', 'Airport transfer', 'Bar', 'Pet-friendly', 'Gym', 
                     'Kitchen', 'Air ', 'Conditioning', 'Bathtub', 'Kitchenette', 'Parking available']

    numerical_cols = ["num_reviews", "rating", "days_from_search", "distance_centre", "star_rating"]

    categorical_cols = ["rating_sentiment"]

    best_params = {'n_estimators': 150, 
               'min_samples_split': 2, 
               'min_samples_leaf': 4, 
               'max_features': 'sqrt', 
               'max_depth': 70}
        
    pipeline = Pipeline([
        ("preprocess", Preprocesser()),
        ("onehotlist", OneHotList("amenities")),
        ("multionehot", MultiOneHot(categorical_cols)),
        ("multiscaler", MultiStandardScaler(numerical_cols)),
        ("estimator", RandomForestRegressor(**best_params))
    ])
    
    clf = pipeline.fit(df_features, df_target)
    dump(clf, 'rf_pipeline_las_vegas.joblib')
    # return clf

if __name__ == "__main__":
    train()