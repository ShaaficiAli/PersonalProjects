import pandas as pd
import joblib
naiveBayesModel = joblib.load('models/naive.sav')
mlpModel = joblib.load('models/naive.sav')

X_train = pd.read_pickle('Data_prep/X_train.pkl')
y_train = pd.read_pickle('Data_prep/y_train.pkl')

X_test = pd.read_pickle('Data_prep/X_test.pkl')
y_test = pd.read_pickle('Data_prep/y_test.pkl')

train_num_rows = y_train.shape
test_num_rows = y_test.shape
num_metrics = X_train.shape

num_diagnosis = y_train.unique().shape
