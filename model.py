# Standard libraries
import pandas as pd
import numpy as np

# Scikit-learn libraries
from sklearn.preprocessing import StandardScaler, OneHotEncoder, MultiLabelBinarizer
# from sklearn.pipeline import Pipeline
from sklearn import base

def amenities(df):
    # Split ameneities into lists of amenity classes, replace NaNs
    df.loc[:,"amenities"] = df.loc[:,"amenities"].str.findall('[A-Z][^A-Z]*')
    df.fillna({"amenities": "M"}, inplace=True)
    return df

def rating_sentiment(df):
    return df.fillna({"rating_sentiment": "M"}, inplace=False)
    
def preprocess(df):
    df = amenities(df)
    df = rating_sentiment(df)
    return df

class OneHotList(base.TransformerMixin, base.BaseEstimator):
    """One-hot encode multivalued column values from a given column"""
    
    def __init__(self, column, classes=None, nan_col="M"):
        self.column = column
        self.classes = classes
        self.nan_col = nan_col
    
    def fit(self, X, y=None):
        self.mlb = MultiLabelBinarizer(sparse_output=False, classes=self.classes)
        self.mlb.fit(X.get(self.column))
        return self
    
    def transform(self, X):
        #mlb = MultiLabelBinarizer(sparse_output=False, classes=self.classes)
        #X = X.join(pd.DataFrame(mlb.fit_transform(X.get(self.column)),
        #                      columns=mlb.classes_,
        #                      index=X.index))
        X_res = X.copy()
        X_res = X_res.join(pd.DataFrame(self.mlb.transform(X_res.get(self.column)),
                              columns=self.mlb.classes_,
                              index=X_res.index))
        columns = [self.column]
        if self.nan_col in X_res:
            columns.append(self.nan_col)
        X_res.drop(columns=columns, axis=1, inplace=True)
        return X_res
    

class MultiOneHot(base.TransformerMixin, base.BaseEstimator):
    """One-hot encode column values from multiple columns"""
    
    def __init__(self, columns, classes="auto", nan_col="M"):
        self.columns = columns
        if not isinstance(self.columns, (list)):
            self.columns = [self.columns]
        self.classes = classes
        self.nan_col = nan_col
    
    def fit(self, X, y=None):
        self.onehot = OneHotEncoder(sparse=False, categories=self.classes)
        self.onehot.fit(X[self.columns])
        return self
    
    def transform(self, X):
        X_res = X.copy()
        X_res = X_res.join(pd.DataFrame(self.onehot.transform(X_res[self.columns]),
                                      columns=[labels for encodings in self.onehot.categories_ 
                                               for labels in encodings],
                                      index=X_res.index))
        if self.nan_col in X_res:
            X_res.drop(columns=self.columns+[self.nan_col], axis=1, inplace=True)
        else:
            X_res.drop(columns=self.columns, axis=1, inplace=True)
        return X_res
    

class MultiStandardScaler(base.TransformerMixin, base.BaseEstimator):
    """Apply standard scaler to mulitple columns"""
    
    def __init__(self, columns):
        self.columns = columns
        if not isinstance(self.columns, (list)):
            self.columns = [self.columns]
    
    def fit(self, X, y=None):
        self.scaler = StandardScaler()
        self.scaler.fit(X[self.columns])
        return self
    
    def transform(self, X):
        X.loc[:, self.columns] = self.scaler.transform(X[self.columns])
        return X
    

class Preprocesser(base.TransformerMixin, base.BaseEstimator):
    """Apply standard scaler to mulitple columns"""
    
    def __init__(self):
        pass
       
    @staticmethod
    def amenities(X):
        # Split ameneities into lists of amenity classes, replace NaNs
        X.loc[:,"amenities"] = X.loc[:,"amenities"].str.findall('[A-Z][^A-Z]*')
        return X.fillna({"amenities": "M"}, inplace=False)

    @staticmethod
    def rating_sentiment(X):
        return X.fillna({"rating_sentiment": "M"}, inplace=False)

    def _preprocess(self, X):
        df = X.copy()
        df = self.amenities(df)
        df = self.rating_sentiment(df)
        df.drop(columns=["checkin_datetime"], errors="ignore", inplace=True)
        return df
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return self._preprocess(X)