import numpy as np, random, pandas as pd, sklearn.neural_network, board, time
from sklearn.neural_network import MLPRegressor

class agent:

    def __init__(self, type, size):
        self.game_size = size
        self.ml = (type == 1)
        self.nn = clf = MLPRegressor(activation='relu', alpha=1e-05, batch_size='auto',
                beta_1=0.9, beta_2=0.999, early_stopping=False,
                epsilon=1e-08, hidden_layer_sizes=(15,),
                learning_rate='constant', learning_rate_init=0.001,
                max_iter=200, momentum=0.9, n_iter_no_change=10,
                nesterovs_momentum=True, power_t=0.5,  random_state=1,
                shuffle=True, solver='lbfgs', tol=0.0001,
                validation_fraction=0.1, verbose=False, warm_start=False)
        self.train()

    def train(self):
        #start = time.time()
        data = pd.read_csv("gameoutput.txt")
        #end = time.time()
        #print("reading data took", (end - start))
        target_col = self.game_size * (self.game_size -1) +2
        target = data["score"]
        target = np.array(target)
        target = target.astype('float32')
        features = data.iloc[:,range(0,target_col-1)]
        features = features.astype('float32')
        #start = time.time()
        self.nn.fit(features, target)
        #end = time.time()
        #print("fitting data took", (end - start))

    

    def move_helper_check(self,board,player,column, calls, alpha, beta):
        state = board.copy()
        state.do_move(column, player)
        if(state.check_tie()):
            return 0.0
        if(state.check_win(player)):
            return (player - 1.5) * 2
        if(calls > 3):
            return self.eval_board(state,player)
        return self.move_helper_add(state, 3 - player , calls, alpha, beta)

    def move_helper_add(self, board, player, calls, alpha, beta):
        state = board.copy()
        maxi = -1
        mini = 1
        ret = 0
        columns = state.get_valid_columns()
        for col in columns:
            row = state.find_row(col)
            if(row > 0):
                temp = self.move_helper_check(state, player, col, calls+1, alpha, beta)
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

    def eval_board(self, board, player):
        vals = (board.print_board() + str(player)).split(',')
        for s in vals:
            s = float(s)
        features = np.array(vals).astype(float).reshape(1,-1)
        score = self.nn.predict(features)
        return score

    def learn_move(self, board,player):
        min = 100
        max = -100
        choice = 1
        columns = board.get_valid_columns()
        for col in columns:
            state = board.copy()
            state.do_move(col,player)
            score = self.eval_board(state, player)
            if(player==1):
                if(score < min):
                    min = score
                    choice = col
            else:
                if(score > max):
                    max = score
                    choice = col
        return choice

    def get_move(self, board, player):
        if(self.ml):
            return self.learn_move(board,player)
        else:
            return self.get_move_minMax(board,player)