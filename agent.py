import numpy as np, random, pandas as pd, sklearn.neural_network, board, time, math
from sklearn.neural_network import MLPRegressor

class agent:

    def __init__(self, type, size, file = "gameoutput.txt"):
        self.game_size = size
        self.agentType = type
        if(type == 1 or type == 2):
            self.nn  = MLPRegressor(activation='relu', early_stopping=True, hidden_layer_sizes=(42,7),
                            learning_rate='adaptive', 
                            max_iter=200, momentum=0.9, n_iter_no_change=10,
                            nesterovs_momentum=True, power_t=0.5,  random_state=1,
                            solver='adam', tol=0.001,
                            validation_fraction=0.1, verbose=False, warm_start=False)
            self.fileName = file
            self.train()

    def train(self):
        #start = time.time()
        data = pd.read_csv(self.fileName)
        for val in data['score']:
            if val < 0:
                val = -1
            else:
                val = 1
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
            denom = board.count_near_win(3-player, 2)
            if denom == 0: denom = 1
            return (board.count_near_win(player, 2)/denom -1) * (player - 1.5)
        return self.move_helper_explore(state, 3 - player , calls, alpha, beta)

    def move_helper_explore(self, board, player, calls, alpha, beta):
        state = board.copy()
        maxi = -1
        mini = 1
        ret = 0
        columns = state.get_valid_columns()
        for col in columns:
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

    def learn_move(self, board, player):
        min = 100
        max = -100
        v = 0
        choice = 1
        columns = board.get_valid_columns()
        for col in columns:
            state = board.copy()
            state.do_move(col,player)
            vals = (state.print_board() + str(player)).split(',')
            for s in vals:
                s = float(s)
            features = np.array(vals).astype(float).reshape(1,-1)
            score = self.nn.predict(features)
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

    def get_move(self, board, player):
        if(self.agentType == 1):
            return self.learn_move(board,player)
        if(self.agentType == 2):
            return self.monte_carlo_move(board, player)
        else:
            return self.get_move_minMax(board,player)

    def simulate_move(self, board, player):
        #columns = board.get_valid_columns()
        #pick = random.randint(0,len(columns))
        #target = 0
        #while(target <= pick):
        #    for col in columns:
        #        if target == pick: return col
        #        target = target + 1
        return self.learn_move(board, player)

    def simulate_game(self, startState, startPlayer):
        currentState = startState.copy()
        currentPlayer = startPlayer
        while(not(currentState.check_win(currentPlayer) or currentState.check_tie())):
            currentPlayer = 3 - currentPlayer
            col = self.simulate_move(currentState, currentPlayer)
            currentState.do_move(col, currentPlayer)
        if(currentState.check_win(currentPlayer)):
            #print("Win",currentState.print_board(),currentPlayer)
            return currentPlayer
        else:
            return 0

    def monte_carlo_move(self, board, player):
        bestColumn = 0
        bestVal = -1
        for col in board.get_valid_columns():
            state = board.copy()
            state.do_move(col, player)
            count = 0
            wins = 0
            for sim in range(1,20):
                count = count + 1
                outcome = self.simulate_game(board, player) 
                if outcome == player:
                    wins = wins + 1
                elif outcome == 0:
                    count = count - 1
            if((wins/count) > bestVal):
                bestVal = (wins/count)
                bestColumn = col
        print(bestVal, bestColumn)
        return bestColumn

    def monte_carlo_move_explore(self, board, player):
        bestColumn = 0
        bestVal = -1
        startBranch = [board,0,0,0]
        bestPath = []
        currentPlayer = player
        for sim in range(1,50):
            currentBranch = startBranch
            currentBoard = currentBranch[0]
            for step in bestPath:
                currentBranch = currentBranch[step][0]
                currentBoard = currentBranch[0]
                currentPlayer = 3 - currentPlayer
            column = self.get_next_monte(currentBoard,currentPlayer,currentBranch)
            newBoard = currentBoard.copy()
            newBoard.do_move(column, currentPlayer)
            outcome = self.simulate_game(newBoard, player)
            count = 1
            win = 0
            if outcome == player:
                win = 1
            newState = [newBoard, count, win, win / count]
            currentBranch.append((newState, column))
            currentBranch = startBranch
            currentBranch[1] = currentBranch[1] + count
            currentBranch[2] = currentBranch[2] + win
            currentBranch[3] = currentBranch[2] / currentBranch[1]
            for step in bestPath:
                currentBranch = currentBranch[step][0]
                #print("currentBranch[1]",currentBranch[1])
                currentBranch[1] = currentBranch[1] + count
                currentBranch[2] = currentBranch[2] + win
                currentBranch[3] = currentBranch[2] / currentBranch[1]
            bestPath = []
            currentBranch = startBranch
            currentPlayer = player
            while len(currentBranch) > 4:
                currentBoard = currentBranch[0]
                columns = currentBoard.get_valid_columns()
                bestChild = 0
                max = 0
                if len(currentBranch) - 4 < len(columns): 
                    #print("not all explored")
                    max = 1
                #print("lenght of current branch", len(currentBranch))
                for child in range(4, len(currentBranch)):
                    childLink = currentBranch[child]
                    childBranch = childLink[0]
                    score = math.sqrt(math.log(sim)/childBranch[1])
                    score = childBranch[3] + score
                    if score >= max:
                        max = score
                        bestChild = child
                if bestChild == 0: break
                #print("best child",bestChild)
                bestPath.append(bestChild)
                currentLink = currentBranch[bestChild]
                currentBranch = currentLink[0]
                currentPlayer = 3 - currentPlayer
        print(startBranch[3], len(bestPath))
        return startBranch[bestPath[0]][1]

    def get_next_monte(self, board, player, branch):
        usedCol = []
        validCol = []
        for child in range(4, len(branch)):
            childLink = branch[child]
            column = childLink[1]
            usedCol.append(column)
        targetCol = board.get_valid_columns()
        for col in targetCol:
            if col not in usedCol: validCol.append(col)
        pick = random.randint(0,len(validCol))
        target = 0
        while(target <= pick):
            for col in validCol:
                if target == pick: return col
                target = target + 1