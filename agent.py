import numpy as np, random, pandas as pd, sklearn.neural_network, board, time, math, agentForest
from sklearn.neural_network import MLPRegressor
from joblib import load, dump
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
import keras
#from tensorflow.python import keras.models.Sequential
#from tensorflow.python import keras.layers.Dense

#agent types:
#   1. retrain single SBE
#   2. single SBE
#   3. single min-max with SBE
#   4. min-max with multi-agent SBE
#   5. retrain next move predictor
#   6. next move predictor
#   7. monte_carlo

class agent:

    def __init__(self, agentTypeInput, size, dataSet, fileName = "Agent JobLib/cnnAgent.joblib"):
        print("Creating agent")
        self.game_size = size
        self.agentType = agentTypeInput
        if self.agentType == 6 or self.agentType == 7:
            fileName = "Agent JobLib/moveAgent.joblib"
        if(self.agentType == 1 or self.agentType == 5):
            self.nn  = self.build_model()
            self.train(dataSet,fileName)
        else:
            print("loading " + fileName)
            self.nn = load(fileName)
        if(self.agentType == 4): self.forest = agentForest.agentForest(10, "nullFile", 2)
        if(self.agentType == 7): self.forest = agentForest.agentForest(10, "nullFile", 6)

    def build_model(self):
        if self.agentType == 1:
            outerLayer = 1
            lossFunc = 'sigmoid'
        else:
            outerLayer = 7
            lossFunc = 'categorical_crossentropy'
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
        model.add(Dense(outerLayer, activation='sigmoid'))
        model.compile(loss=lossFunc,
                    optimizer='sgd',
                    metrics=['accuracy'])
        return model

    def train(self, data, fileName):
        if self.agentType == 1:
            Y = data['score'].astype('int')
        else:
            Y = keras.utils.to_categorical(np.array(data['next move'])-1, num_classes = 7)
        X = np.array(data.iloc[:,range(0,42)]).reshape(len(data),6,7,1)
        self.nn.fit(X, Y,epochs = 1, batch_size = 100)
        dump(self.nn,fileName)
        print("writing " + fileName)
           

    def move_helper_check(self,board,player,column, calls, alpha, beta):
        state = board.copy()
        state.do_move(column, player)
        if(state.check_tie()):
            return 0.0
        if(state.check_win(player)):
            return (player - 1.5) * 2
        if(calls > 1):
            return self.static_board_eval(state,player)
        return self.move_helper_explore(state, 3 - player , calls, alpha, beta)

    def static_board_eval(self, board, player):
        if self.agentType == 3:
            return self.calc_nn_move(board,player)
        else:
            return self.forest.evaluate_board(board, player)
        

    def move_helper_explore(self, board, player, calls, alpha, beta):
        state = board.copy()
        maxi = -1
        mini = 1
        ret = 0
        columns = state.get_valid_columns()
        for col in columns:
            temp = self.move_helper_check(state, player, col, calls+1, alpha, beta)
            #print(temp, calls, player)
            if(player==1):
                if(temp < mini):
                    mini = temp
                    ret = mini
                    beta = min(beta,mini)
                if(temp < alpha):
                    return temp
            else:
                if(temp > maxi):
                    maxi = temp
                    ret = maxi
                    alpha = max(alpha,maxi)
                if(temp > beta):
                    return temp
        return ret

    def get_move_minMax(self, board, player):
        state = board.copy()
        alpha = -1
        beta = 1
        max = -1
        min = 1
        maxCols = [random.randint(1,self.game_size)]
        columns = state.get_valid_columns()
        for col in columns:
            temp = self.move_helper_check(state, player, col, 1, alpha, beta)
            if(player==2):
                if(temp == max):
                    maxCols.append(col)
                if(temp > max):
                    maxCols = [col]
                    max = temp
            else:
                if(temp == min):
                    maxCols.append(col)
                if(temp < min):
                    maxCols = [col]
                    min = temp 
        return maxCols[random.randint(1,self.game_size) % len(maxCols)]

    def calc_nn_move(self, board, player):
        val = board.print_board()
        val = val[0:len(val)-1] 
        vals = val.split(',')
        features = np.array(vals).astype(float)
        features = features.reshape(1,6,7,1)
        return self.nn.predict(features)[0]

    def learn_move(self, board, player):
        min = 100
        max = -100
        v = 0
        choice = 1
        columns = board.get_valid_columns()
        for col in columns:
            state = board.copy()
            state.do_move(col,player)
            score = self.calc_nn_move(state, player)
            if(player==1):
                if(score < min):
                    min = score
                    choice = col
                    v = min
            else:
                if(score > max):
                    max = score
                    choice = col
                    v = max
        #print(v, choice, player)
        return choice

    def learn_next_move(self, board, player):
        cols = np.array(board.get_valid_columns()) - 1
        val = board.print_board()
        val = val[0:len(val)-1] 
        vals = val.split(',')
        sample = np.array(vals).astype(float)
        sample = sample.reshape(1,6,7,1)
        prediction = self.nn.predict(sample)[0]
        prediction = prediction[cols]
        return cols[np.argmax(prediction)]

    def monte_carlo(self, board, player):
        min = 100
        max = -100
        choice = 1
        columns = board.get_valid_columns()
        for col in columns:
            #print("column" , col)
            state = board.copy()
            state.do_move(col,player)
            score = self.simulate_game(state, player)
            #print(score)
            if(player==1):
                if(score < min):
                    min = score
                    choice = col
            else:
                if(score > max):
                    max = score
                    choice = col
        #print(v, choice, player)
        return choice

    def simulate_game(self, board, player):
        state = board.copy()
        currentPlayer = player
        while (not (state.check_win(currentPlayer) or state.check_tie())):
            currentPlayer = 3 - currentPlayer
            move = self.forest.get_learned_move(board, player)
            #print(currentPlayer, move)
            state.do_move(move,currentPlayer)
        return 2 * (1.5 - currentPlayer)


    def get_move(self, board, player):
        if(self.agentType == 3 or self.agentType == 4):
            return self.get_move_minMax(board,player)
        elif(self.agentType == 5 or self.agentType == 6):
            return self.learn_next_move(board, player) + 1
        elif(self.agentType == 7):
            return self.monte_carlo(board, player)
        else:
            return self.learn_move(board,player)
            