import pandas as pd
import numpy as np
import re
import random
import pickle
from sklearn.neural_network import MLPClassifier
import joblib
random.seed(7)
X_train = pd.read_pickle('Data_prep/X_train.pkl')
y_train = pd.read_pickle('Data_prep/y_train.pkl')

X_test = pd.read_pickle('Data_prep/X_test.pkl')
y_test = pd.read_pickle('Data_prep/y_train.pkl')
print("read data")
model = MLPClassifier(hidden_layer_sizes=(100,100))
model.fit(X_train,y_train)
print("fit mode")

test_predictions = model.predict(X_test)
test_predictions = model.predict(X_test)

comparison_dataframe = pd.DataFrame()
comparison_dataframe['prediction']=test_predictions

comparison_dataframe['actual']=y_test
comparison_dataframe['is_right'] = comparison_dataframe['prediction']== comparison_dataframe['actual']

comparison_dataframe.to_pickle('Prediction_results/MLPPredictions.pkl')

joblib.dump(model,"models/mlp.sav")
