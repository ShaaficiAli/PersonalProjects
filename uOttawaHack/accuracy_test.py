from sklearn.metrics import accuracy_score
import pandas as pd
naivePredictions = pd.read_pickle('prediction_results/NaiveClassifierPredictions.pkl')
mlpPredictions = pd.read_pickle('prediction_results/MLPPredictions.pkl')

naiveAccuracy = accuracy_score(naivePredictions['actual'],naivePredictions['prediction'])

mlpAccuracy =  accuracy_score(mlpPredictions['actual'],mlpPredictions['prediction'])

