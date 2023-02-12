import pandas as pd
#from sklearn.naive_bayes import MultinomialNB
#from sklearn import svm
import numpy as np
import re
import random
import pickle
random.seed(7)
from sklearn.preprocessing import MultiLabelBinarizer,LabelEncoder
def convert_str_list(stringGiven):
    remove_non_delimiter = re.sub("\]|\[|\'","",stringGiven)
    return_list = re.split("\,",remove_non_delimiter)
    return return_list
training_set = pd.read_csv('Data/release_train_patients.csv')
training_set['EVIDENCES'] = training_set['EVIDENCES'].apply(lambda x:convert_str_list(x))
print("evidence is parsed correctly")
test_set = pd.read_csv('Data/release_test_patients.csv')
test_set['EVIDENCES'] = test_set['EVIDENCES'].apply(lambda x:convert_str_list(x))

#labeling the target class
print("label encoding")
le = LabelEncoder()
le.fit(training_set['PATHOLOGY'])
training_set['target'] = le.transform(training_set['PATHOLOGY'])
test_set['target'] = le.transform(test_set['PATHOLOGY'])

#encoding the features for training

mlb_evidence = MultiLabelBinarizer(sparse_output=True)

mlb_sex = MultiLabelBinarizer(sparse_output=True)

print("mlb1")
training_set = training_set.join(pd.DataFrame.sparse.from_spmatrix(
                mlb_evidence.fit_transform(training_set.pop('EVIDENCES')),
                index=training_set.index,
                columns=mlb_evidence.classes_))

print("mlb2")
training_set = training_set.join(pd.DataFrame.sparse.from_spmatrix(
                mlb_sex.fit_transform(training_set.pop('SEX')),
                index=training_set.index,
                columns=mlb_sex.classes_))


feature_columns = list(mlb_sex.classes_)+list(mlb_evidence.classes_)+['AGE']
X_train = training_set[feature_columns]
y_train = training_set['target']

#repeat for test


print("test_split start")
test_set = test_set.join(pd.DataFrame.sparse.from_spmatrix(
                mlb_evidence.transform(test_set.pop('EVIDENCES')),
                index=test_set.index,
                columns=mlb_evidence.classes_))

print("mlb2 test")
test_set = test_set.join(pd.DataFrame.sparse.from_spmatrix(
                mlb_sex.transform(test_set.pop('SEX')),
                index=test_set.index,
                columns=mlb_sex.classes_))


X_test = test_set[feature_columns]
y_test = test_set['target']

#repeat for validate



#pickle the prepped data

print("pickling")
X_train.to_pickle('Data_prep/X_train.pkl')
X_test.to_pickle('Data_prep/X_test.pkl')

y_train.to_pickle('Data_prep/y_train.pkl')
y_test.to_pickle('Data_prep/y_test.pkl')


