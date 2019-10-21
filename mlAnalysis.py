import numpy as np, random, pandas as pd, sklearn.neural_network, sklearn.metrics 
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy import stats
nn = MLPRegressor(activation='relu', early_stopping=True, hidden_layer_sizes=(42,7,7,7),
        learning_rate='adaptive', 
        max_iter=200, momentum=0.9, n_iter_no_change=10,
        nesterovs_momentum=True, power_t=0.5,  random_state=1,
        solver='adam', tol=0.001,
        validation_fraction=0.1, verbose=True, warm_start=False)       

data = pd.read_csv("gamelog.txt")
for val in data['score']:
   if val < 0:
        val = -1
   else:
       val = 1
train, test = train_test_split(data, test_size=0.2)
target_col = 44
target = train["score"]
target = np.array(target)
target = target.astype('float32')
features = train.iloc[:,range(0,target_col-1)]
features = features.astype('float32')
print(stats.describe(target))
nn.fit(features, target)
test_features = test.iloc[:,range(0,target_col-1)]
test_features = test_features.astype('float32')
test_target = test["score"]
test_target = np.array(test_target)
test_target = test_target.astype('float32')
test_prediction = nn.predict(test_features)
print(mean_squared_error(test_target, test_prediction))