import numpy as np, pandas as pd, board, agentForest, random
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from joblib import dump, load
from scipy import stats
import keras



#Set defaults for number of training runs and weather to keep the computer awake automatically
inputFile = "moveTrainer.txt"

data = pd.read_csv(inputFile).dropna()



X = np.array(data.iloc[:,range(0,42)])
#keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)
Y = keras.utils.to_categorical(np.array(data['next move'])-1, num_classes = 7)
#print(Y.head(10))
players = data['player']
print(np.shape(players))

model = Sequential()
model.add(Conv2D(filters=20, kernel_size = (2,2), strides = (1,1), input_shape=(6,7,1)))
#model.add(MaxPooling2D(strides = (1,1)))
model.add(Conv2D(filters=10, kernel_size = (2,2), strides = (1,1)))
model.add(Conv2D(filters=10, kernel_size = (2,2), strides = (1,1)))
#model.add(MaxPooling2D(strides = (1,1)))
model.add(Dense(units=7, activation='relu'))
model.add(Dense(units=7, activation='relu'))
model.add(Dense(units=7, activation='relu'))
model.add(Dense(units=7, activation='relu'))
model.add(Flatten())
model.add(Dense(7, activation='sigmoid'))
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

#model.fit(X.reshape(len(data),6,7,1), Y, epochs = 4, batch_size = 100)
#dump(model, 'Agent JobLib/moveAgent.joblib') 
model = load('Agent JobLib/moveAgent.joblib')

choices = range(0,len(data))
print(np.shape(choices))
for cycle in range(0,30):
    row = random.choice(choices)
    state = X[row]
    player = players[row]
    print(state.reshape(6,7,))
    prediction = model.predict(state.reshape(1,6,7,1))[0]
    print(np.argmax(prediction),player,Y[row])