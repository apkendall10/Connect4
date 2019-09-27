import numpy as np, random, pandas as pd, sklearn.neural_network, timeit
from sklearn.neural_network import MLPRegressor

file = open("gameoutput.txt","a") 
size = 7

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
clf.fit(features, target)

win = 4
board = pd.DataFrame(data = 0, index = range(1,size) , columns = range(1,size+1))


def find_row(column, board):
    ret = size-1
    for i in board.index:
        if(board.loc[i,column]>0):
            return i-1
    return ret

def check_tie(board):
    for column in board.columns:
        if(board.loc[1,column]==0):
            return False
    return True

def check_helper(board, player, row, column, count, dir):
    x , y = dir
    newRow = row + x
    newColumn = column + y
    if(newRow not in board.index):
        return 0
    if(newColumn not in board.columns):
        return 0
    if(board.loc[newRow, newColumn] != player):
        return 0
    if(count==1):
        #print(player, newRow, newColumn, dir, sep=" ")
        return 1
    return check_helper(board, player, newRow, newColumn, count-1, dir)

def check_win(board,player):
    for row in board.index:
        for column in board.columns:
            if(board.loc[row, column]==player):
                for x in (-1, 0, 1):
                    for y in (-1,0,1):
                        dir = (x,y)
                        if(dir != (0,0)):
                            if(check_helper(board,player, row,column, 3, dir)==1):
                                return True
    return False

def print_board(board):
    val = ""
    for row in board.index:
        for col in board.columns:
            val = val + str(board.loc[row, col]) + ","
    return val

def learn_move(board,player):
    min = 1
    max = -1
    choice = 1
    for col in board.columns:
        row = find_row(col,board)
        if(row > 0):
            state = board.copy()
            state.loc[row, col] = player
            vals = (print_board(state) + str(player)).split(',')
            for s in vals:
                s = float(s)
            features = np.array(vals).astype(float).reshape(1,-1)
            score = clf.predict(features)
            if(player==1):
                if(score < min):
                    min = score
                    choice = col
            else:
                if(score > max):
                    max = score
                    choice = col
    return choice

def get_move(board,player):
    return learn_move(board,player)


gameStates = []
turnCount = 0
startPlayer = random.randint(1,2)
player = startPlayer
trainingstep = 2500
for it in range(1,trainingstep+1):
    if(it % 100 == 0):
        print("reprocessing")
        data = pd.read_csv("gameoutput.txt")
        target_col = size * (size -1)+2
        target = data["score"]
        target = np.array(target)
        target = target.astype('float32')
        features = data.iloc[:,range(0,target_col-1)]
        features = features.astype('float32')
        clf.fit(features, target)
    board = pd.DataFrame(data = 0, index = range(1,size) , columns = range(1,size+1))
    gameStates = []
    turnCount = 0
    print(it)
    startPlayer = random.randint(1,2)
    player = startPlayer
    win = False
    while not (win or check_tie(board)):
        start = timeit.timeit()
        row = -1
        while(row not in board.index):
            column = get_move(board,player)
            row = find_row(column, board)
            end = timeit.timeit()
            if(end - start > 100):
                print(row)
        board.loc[row,column] = player
        win = check_win(board, player)
        turnCount = turnCount +1
        gameStates.append(print_board(board))
        player = 3 - player
    player = 3 - player
    outcome = (player - 1.5) * 2
    if(check_tie(board)): outcome = 0
    counter = -1
    player = startPlayer
    for state in gameStates:
        counter = counter + 1
        val = "\n" + state + str(player) + "," + str(outcome/(turnCount - counter))
        file.write(val)   
        player = 3- player
file.close()