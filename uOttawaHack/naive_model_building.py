import pandas as pd
import numpy as np
import re
import random
import pickle
import joblib
from sklearn.naive_bayes import CategoricalNB
random.seed(7)
X_train = pd.read_pickle('Data_prep/X_train.pkl')
y_train = pd.read_pickle('Data_prep/y_train.pkl')

X_test = pd.read_pickle('Data_prep/X_test.pkl')
y_test = pd.read_pickle('Data_prep/y_train.pkl')

categoricalNaive = CategoricalNB(force_alpha=True)
categoricalNaive.fit(X_train,y_train)

test_predictions = categoricalNaive.predict(X_test)
test_predictions = categoricalNaive.predict(X_test)

comparison_dataframe = pd.Dataframe()
comparison_dataframe['prediction']=test_prediction

comparison_dataframe['actual']=y_test
comparison_dataframe['is_right'] = comparison_dataframe['prediction']== comparison_dataframe['actual']

comparison_dataframe.to_pickle('Prediction_results/NaiveClassifierPredictions.pkl')

joblib.dump(categoricalNaive,"models/naive.sav")
