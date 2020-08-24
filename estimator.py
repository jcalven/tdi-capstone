# estimator.py
import numpy as np
import pandas as pd 
from joblib import load
from datetime import date, datetime

from model import Preprocesser

data_columns = ["num_reviews", "rating", "days_from_search", "distance_centre", "rating_sentiment", "amenities", "star_rating"]

class Estimator:

    amenities_classes = [
        'Free parking', 'Pool', 'Airport transfer', 'Bar', 'Pet-friendly', 
        'Gym', 'Kitchen', 'Air ', 'Conditioning', 'Bathtub', 'Kitchenette', 'Parking available'
        ]    

    def __init__(self, estimator_path):
        self.estimator_path = estimator_path

    def load(self):
        self.estimator = load(self.estimator_path)

    @staticmethod
    def _generate(num_reviews=10, rating=5., days_from_search=30, 
                  distance_centre=3., rating_sentiment="Good", 
                  amenities=("Parking available", "Bar", "Gym"), 
                  star_rating=3.):
        
        data = pd.DataFrame([(num_reviews, rating, day, distance_centre, 
                              rating_sentiment, amenities, star_rating) for day in range(1, days_from_search+1)],
                              columns=data_columns)
        return data

    @staticmethod
    def _get_n_days(checkin_date):
        return (checkin_date - date.today()).days
        # return (datetime.strptime(date, '%Y-%m-%d').date() - date.today()).days

    def predict(self, checkin_date, num_reviews=10, rating=5., #days_from_search=30, 
                  distance_centre=3., rating_sentiment="Good", 
                  amenities=("Parking available", "Bar", "Gym"), 
                  star_rating=3.):

        days_from_search = self._get_n_days(checkin_date)

        data = self._generate(num_reviews, rating, days_from_search, 
                  distance_centre, rating_sentiment, amenities, star_rating)

        predictions = self.estimator.predict(data)
        return pd.DataFrame({"day": range(days_from_search, 0, -1), "price": predictions})