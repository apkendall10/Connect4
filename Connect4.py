import sys, pygame, numpy as np, random, pandas as pd, sklearn.neural_network
from sklearn.neural_network import MLPRegressor
pygame.init
size = width, height = 600, 480
white= 255,255,255
screen = pygame.display.set_mode(size)
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
pos=(0,0)
blue = (100,100,200)
red = (200,100,100)
green = (100,200,100)
brown = (100,100,100)
gray = (200,200,200)
black=(0,0,0)
yellow=(200,200,100)
colorMap = {
        0: white,
        1: red,
        2: black,
        3: brown,
        4: gray}
screen.fill(blue)
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 10)
board = pd.DataFrame(data = 0, index = range(1,size) , columns = range(1,size+1))

def draw_circle(pos,color,r=20):
    x, y = pos
    pygame.draw.circle(screen,color,(x,y),r)
    pygame.draw.circle(screen,black,(x,y),r,1)

def add_piece(row, column, player):
    color = colorMap[player]
    draw_circle((int(column * 60),int(row * 60)), color)

def draw_board(board):
    for i in board.index:
        for j in board.columns:
            add_piece(i,j,0)

def find_column(pos):
    x,y = pos
    return round((x+30)/60)

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
def count_near_win(board,player):
    count = 0
    for row in board.index:
        for column in board.columns:
            if(board.loc[row, column]==player):
                for x in (-1, 0, 1):
                    for y in (-1,0,1):
                        dir = (x,y)
                        if(dir != (0,0)):
                            count = count + check_helper(board,player, row,column, 2, dir)
    return count
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

def move_helper_check(board,player,column, calls, alpha, beta):
    state = board.copy()
    row = find_row(column, state)
    state.loc[row,column]=player
    if(check_tie(state)):
        #print("Tie Reached")
        return 0.0
    if(check_win(state,player)):
        #print_board(state)
        #print(player, " wins in " , calls)
        return (player - 1.5) * 2 / calls
    return move_helper_add(state, 3 - player , calls+1, alpha, beta)

def move_helper_add(board, player, calls, alpha, beta):
    if(calls > 3):
        return count_near_win(board,player)
    state = board.copy()
    maxi = -1
    mini = 1
    ret = 0
    for col in state.columns:
        row = find_row(col,state)
        if(row > 0):
            temp = move_helper_check(state, player, col, calls, alpha, beta)
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
    #print("least bad move for turn ", calls, "val is", ret)
    return ret
def get_move_minMax(baord,player):
    state = board.copy()
    alpha = -1
    beta = 1
    max = -1
    min = 1
    maxCols = [random.randint(1,size)]
    for col in state.columns:
        row = find_row(col, state)
        if(row > 0):
            temp = move_helper_check(state, player, col, 1, alpha, beta)
            #print("best move for column: ",col, " is ",temp)
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
    return maxCols[random.randint(1,size) % len(maxCols)]

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
    #return get_move_minMax(board,player)

class button:
    def __init__(self,pos,name,color,screen,size=(80,50)):
        self.tile=pygame.Rect(pos,size)
        pygame.draw.rect(screen,color,self.tile)
        pygame.draw.rect(screen,black,self.tile,3)
        textsurface = myfont.render(name,False,black)
        x,y=self.tile.center
        x=x-len(name)*2.5
        screen.blit(textsurface,(x,y))
    def has(self,pos):
        return self.tile.collidepoint(pos)




player_0=button((0,0),"0 Players",green,screen,(200,480))
player_1=button((200,0),"1 Players",blue,screen,(200,480))
player_2=button((400,0),"2 Players",red,screen,(200,480))
#screen.fill(white)
numPlayers=-1

while numPlayers==-1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            if player_1.has(pos):
                numPlayers=1
            if player_2.has(pos):
                numPlayers=2
            if player_0.has(pos):
                numPlayers=0
    pygame.display.flip()

screen.fill(blue)
draw_board(board)
gameStates = []
turnCount = 0
startPlayer = random.randint(1,2)
player = startPlayer
trainingstep = 1
if (numPlayers==0):
    trainingstep = 20
for it in range(1,trainingstep+1):
    board = pd.DataFrame(data = 0, index = range(1,size) , columns = range(1,size+1))
    draw_board(board)
    gameStates = []
    turnCount = 0
    print(it)
    startPlayer = random.randint(1,2)
    player = startPlayer
    win = False
    while not (win or check_tie(board)):
            pygame.display.flip()
            for event in pygame.event.get():
                pygame.display.flip()
                if event.type == pygame.QUIT: 
                    sys.exit()
                if(not numPlayers==0 and (player==1 or numPlayers == 2)):
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos=pygame.mouse.get_pos()
                        column = find_column(pos)
                        if column not in board.columns: 
                            break
                        row = find_row(column, board)
                        #print(column)
                        if row not in board.index: 
                            break
                        #print(find_row(column))
                        board.loc[row,column] = player
                        add_piece(row, column, player)
                        win = check_win(board, player)
                        #if(win): print("you win")
                        turnCount = turnCount +1
                        gameStates.append(print_board(board))
                        player = 3 - player
                        pygame.display.flip()
                else:
                    row = -1
                    while(row not in board.index):
                        column = get_move(board,player)
                        row = find_row(column, board)
                    board.loc[row,column] = player
                    add_piece(row, column, player)
                    win = check_win(board, player)
                    turnCount = turnCount +1
                    gameStates.append(print_board(board))
                    player = 3 - player
                    pygame.display.flip()
            pygame.display.flip()
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

sys.exit()