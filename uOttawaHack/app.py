from dash import Dash, html, dcc,Input,Output,State,dash_table
import plotly.express as px
import pandas as pd
import joblib
import math
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score

app = Dash(__name__)

naiveBayesModel = joblib.load('models/naive.sav')
mlpModel = joblib.load('models/naive.sav')

X_train = pd.read_pickle('Data_prep/X_train.pkl')
y_train = pd.read_pickle('Data_prep/y_train.pkl')

X_test = pd.read_pickle('Data_prep/X_test.pkl')
y_test = pd.read_pickle('Data_prep/y_test.pkl')

naivePredictions = pd.read_pickle('prediction_results/NaiveClassifierPredictions.pkl')
mlpPredictions = pd.read_pickle('prediction_results/MLPPredictions.pkl')

naiveAccuracy = accuracy_score(naivePredictions['actual'],naivePredictions['prediction'])

mlpAccuracy =  accuracy_score(mlpPredictions['actual'],mlpPredictions['prediction'])

non_symptoms = ['F','M','AGE']
symptoms =[symptom for symptom in X_train.columns.values.tolist() if symptom not in non_symptoms]
symptom_series_training = pd.Series()
symptom_series_test = pd.Series()

for symptom in symptoms:
    try:
        symptom_series_test[symptom] = X_test[symptom].value_counts()[1]
    except:
        print(symptom)
    symptom_series_training[symptom] = X_train[symptom].value_counts()[1]
symptom_count_training =symptom_series_training.reset_index().rename(columns = {0:"count",'index':"symptom"})
symptom_count_training_barplot = px.bar(symptom_count_training,x='symptom',y='count',color='symptom')

symptom_count_test = symptom_series_test.reset_index().rename(columns = {0:"count",'index':"symptom"})
symptom_count_test_barplot = px.bar(symptom_count_test,x='symptom',y='count',color='symptom')

age_histogram_train = px.histogram(X_train,x='AGE',color='AGE')
gender_dataframe_train = pd.DataFrame()
gender_dataframe_train['SEX'] = X_train['F'].apply(lambda x:'F' if x==1 else 'M')
gender_histogram_train = px.histogram(gender_dataframe_train,x='SEX',color='SEX')


age_histogram_test = px.histogram(X_test,x='AGE',title='Age break of test set',color='AGE')

gender_dataframe_test = pd.DataFrame()
gender_dataframe_test['SEX'] = X_test['F'].apply(lambda x:'F' if x==1 else 'M')
gender_histogram_test = px.histogram(gender_dataframe_test,x='SEX',color='SEX')




app.layout = html.Div([html.Div([html.H2("Training set infographics"),
              html.H5("Age breakdown"),
              dcc.Graph(id='training_age',
                        figure=age_histogram_train),
                                 html.H5("Gender breakdown"),
                                 dcc.Graph(id='train_sex',
                                           figure=gender_histogram_train),
                                 html.H5("Symptom breakdown"),
                                 dcc.Graph(id='train_symptoms',
                                           figure=symptom_count_training_barplot)                              
                                 ]),html.Div([html.H2("Test set infographics"),
              html.H5("Age breakdown"),
              dcc.Graph(id='test_age',
                        figure=age_histogram_test),
                                 html.H5("Gender breakdown"),
                                 dcc.Graph(id='test_sex',
                                           figure=gender_histogram_test),
                                 html.H5("Symptom breakdown"),
                                 dcc.Graph(id='test_symptoms',
                                           figure=symptom_count_test_barplot)                              
                                 ]),
    html.Div([html.H2('Prediction models demo'),
        html.H5('Age of patient:'),
        dcc.Dropdown(
            sorted(X_train['AGE'].unique().tolist()),
            'Select AGE:',
            id='predictAge'),
        html.H5("Patient's Gender"),
        dcc.Dropdown(
            ['F','M'],
            'Select SEX:',
            id='predictSEX'),
        html.H5("Patient's symptoms"),
        dcc.Dropdown(
            symptoms,
            'List of symptoms',
            id='predictSymptoms',
            multi=True),
        html.Button('Submit',id='submit-predict',n_clicks=0),
        html.H4("Prediction results"),
              html.H5("MLP Model prediction"),
              html.Div(id='container-button-mlp',children='Enter a value and press submit'),
              html.H5("Categorical naive bayes model prediction"),
              html.Div(id='container-button-naive',children='Enter a value and press submit')]),
                       html.Div([html.H2("Accuracy metric and prediction results:"),
                                 html.H5("Data table for naive bayes prediction:"),
                                 dash_table.DataTable(naivePredictions.sample(n=10).to_dict('records')),
                                 html.H5("Accuracy naive bayes prediction:"+str(naiveAccuracy)),
                                 html.H5("Data table for MLP prediction:"),
                                 dash_table.DataTable(mlpPredictions.sample(n=10).to_dict('records')),
                                 html.H5("Accuracy of MLP prediction:"+str(mlpAccuracy)),
                                ])])
@app.callback(
    Output('container-button-mlp', 'children'),
    Input('submit-predict','n_clicks'),
    State('predictAge','value'),
    State('predictSEX','value'),
    State('predictSymptoms','value')
    )
def update_prediction_mlp(n_clicks,predictAge,predictSEX,predictSymptoms):
    
    prediction_columns = symptoms+non_symptoms
    initial_values = [0]*len(prediction_columns)
    prediction_df = pd.DataFrame(columns = prediction_columns)
    prediction_df.loc[0]=initial_values
    prediction_df=prediction_df.assign(AGE=predictAge)
    for symptom in predictSymptoms:
        prediction_df.iloc[0,prediction_df.columns.get_loc(symptom)]=1
    if predictSEX =='M':
        prediction_df.iloc[0,prediction_df.columns.get_loc('M')]=1
    else:
        prediction_df.iloc[0,prediction_df.columns.get_loc('F')]=1

    columns_as_fit = mlpModel.feature_names_in_
    prediction_df = prediction_df[columns_as_fit]
    results = mlpModel.predict(prediction_df)
    return results

@app.callback(
    Output('container-button-naive', 'children'),
    Input('submit-predict','n_clicks'),
    State('predictAge','value'),
    State('predictSEX','value'),
    State('predictSymptoms','value')
    )
def update_prediction_naive(n_clicks,predictAge,predictSEX,predictSymptoms):
    
    prediction_columns = symptoms+non_symptoms
    initial_values = [0]*len(prediction_columns)
    prediction_df = pd.DataFrame(columns = prediction_columns)
    prediction_df.loc[0]=initial_values
    prediction_df=prediction_df.assign(AGE=predictAge)
    for symptom in predictSymptoms:
        prediction_df.iloc[0,prediction_df.columns.get_loc(symptom)]=1
    if predictSEX =='M':
        prediction_df.iloc[0,prediction_df.columns.get_loc('M')]=1
    else:
        prediction_df.iloc[0,prediction_df.columns.get_loc('F')]=1

    columns_as_fit = mlpModel.feature_names_in_
    prediction_df = prediction_df[columns_as_fit]
    results = naiveBayesModel.predict(prediction_df)
    return results
                      


#Demo part

if __name__ == '__main__':
    app.run_server(debug=True)



