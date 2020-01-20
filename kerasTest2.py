import numpy as np, pandas as pd, board, agentForest, random
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from joblib import dump, load
from scipy import stats



#Set defaults for number of training runs and weather to keep the computer awake automatically
inputFile = "moveLearner.txt"

data = pd.read_csv(inputFile)

#data = data.sample(frac=1/3).reset_index(drop=True)
print(data.head(10))
#data = shuffle(data)
#dataSet = np.array_split(data, 10)
#data = dataSet[0]

data['score'] = data['score'].apply(lambda x: 0 if x < 0 else 1)
Y = data['score'].astype('int')

players = data['player']
print(np.shape(players))
X = np.array(data.iloc[:,range(0,42)])

model = Sequential()
model.add(Conv2D(filters=10, kernel_size = (2,2), strides = (1,1), input_shape=(6,7,1)))
#model.add(MaxPooling2D(strides = (1,1)))
#model.add(Dropout(0.25))
model.add(Conv2D(filters=20, kernel_size = (2,2), strides = (1,1)))
#model.add(Dropout(0.25))
model.add(Conv2D(filters=30, kernel_size = (2,2), strides = (1,1)))
#model.add(Dropout(0.25))
model.add(Conv2D(filters=40, kernel_size = (2,2), strides = (1,1)))
#model.add(Dropout(0.25))
#model.add(MaxPooling2D(strides = (1,1)))
model.add(Dense(units=7, activation='relu'))
model.add(Dense(units=7, activation='relu'))
model.add(Dense(units=7, activation='relu'))
model.add(Dense(units=7, activation='relu'))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

model.fit(X.reshape(len(data),6,7,1), Y, epochs = 2, batch_size = 100)
dump(model, 'Agent JobLib/cnnAgent2.joblib') 
#model = load('Agent JobLib/cnnAgent.joblib'

choices = range(0,len(data))
print(np.shape(choices))
for cycle in range(0,30):
    row = random.choice(choices)
    state = X[row]
    player = players[row]
    print(state.reshape(6,7,))
    print(model.predict(state.reshape(1,6,7,1)),player,Y[row])