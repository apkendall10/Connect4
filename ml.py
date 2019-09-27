import  numpy as np, pandas as pd, sklearn.neural_network, board
from sklearn.neural_network import MLPRegressor
size = 7
#ML stuff
#
#
#
#

b = board.board(5)
print(b.print_board())

data = pd.read_csv("gameoutput.txt")
target_col = size * (size -1)+2
target = data["score"]
target = np.array(target)
target = target.astype('float32')
features = data.iloc[:,range(0,target_col-1)]
features = features.astype('float32')
clf = MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
              beta_1=0.9, beta_2=0.999, early_stopping=False,
              epsilon=1e-08, hidden_layer_sizes=(15,),
              learning_rate='constant', learning_rate_init=0.001,
              max_iter=200, momentum=0.9, n_iter_no_change=10,
              nesterovs_momentum=True, power_t=0.5,  random_state=1,
              shuffle=True, solver='lbfgs', tol=0.0001,
              validation_fraction=0.1, verbose=False, warm_start=False)
print(features.shape)
print(target.shape)
clf.fit(features, target)
test = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,2,0,0,0,0,0,0,2,1,1,1,1,1,0,1,1,1])
test = test.reshape(1,-1)
print(test.shape)
print(clf.predict(test))


