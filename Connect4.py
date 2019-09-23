import sys, pygame, numpy as np, random, pandas as pd
pygame.init
size = width, height = 600, 480
white= 255,255,255
screen = pygame.display.set_mode(size)

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
board = pd.DataFrame(data = 0, index = range(1,7) , columns = range(1,8))

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
    ret = 6
    for i in board.index:
        if(board.loc[i,column]>0):
            return i-1
    return ret

def check_helper(board, player, row, column, count, dir):
    x , y = dir
    newRow = row + x
    newColumn = column + y
    if(newRow < 1 or newRow > 6):
        return False
    if(newColumn < 1 or newColumn > 7):
        return False
    if(board.loc[newRow, newColumn] != player):
        return False
    if(count==1):
        #print(player, newRow, newColumn, dir, sep=" ")
        return True
    return check_helper(board, player, newRow, newColumn, count-1, dir)
def check_tie(board):
    for column in board.columns:
        if(board.loc[1,column]==0):
            return False
    return True

def check_win(board,player):
    if(check_tie(board)):
        return False
    for row in board.index:
        for column in board.columns:
            if(board.loc[row, column]==player):
                for x in (-1, 0, 1):
                    for y in (-1,0,1):
                        dir = (x,y)
                        if(dir != (0,0)):
                            if(check_helper(board,player, row,column, 3, dir)):
                                return True
    return False
def print_board(board):
    for row in board.index:
        val = ""
        for col in board.columns:
            val = val + str(board.loc[row, col]) + " "
        print(val)

def move_helper_check(board,player,column, calls):
    state = board.copy()
    row = find_row(column, state)
    state.loc[row,column]=player
    if(check_tie(state)):
        print("Tie Reached")
        return 0.0
    if(check_win(state,player)):
        #print_board(state)
        print(player, " wins in " , calls)
        return (player - 1.5) * 2 / calls
    return move_helper_add(state, 3 - player , calls+1)

def move_helper_add(board, player, calls):
    if(calls > 6):
        return 0
    state = board.copy()
    max = -1
    min = 1
    ret = 0
    for col in state.columns:
        row = find_row(col,state)
        if(row > 0):
            temp = move_helper_check(state, player, col, calls)
            if(player==1):
                if(temp < min):
                    min = temp
                    ret = min
                    
            else:
                if(temp > max):
                    max = temp
                    ret = max
    print("least bad move for turn ", calls, "val is", ret)
    return ret

def get_move(board):
    state = board.copy()
    max = -.25
    maxCol = random.randint(1,7)
    test = maxCol
    for col in state.columns:
        row = find_row(col, state)
        if(row > 0):
            temp = move_helper_check(state, 2, col, 1)
            print("best move for column: ",col, " is ",temp)
            if(temp > max):
                maxCol = col
                max = temp
    if(max==0):
        maxCol = test
    return maxCol


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

player_1=button((0,0),"1 Player",blue,screen,(300,480))
player_2=button((300,0),"2 Player",red,screen,(300,480))
#screen.fill(white)
numPlayers=0

while numPlayers==0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            if player_1.has(pos):
                numPlayers=1
            if player_2.has(pos):
                numPlayers=2
    pygame.display.flip()

screen.fill(blue)
draw_board(board)

player=1
win = False
while not win:
        pygame.display.flip()
        for event in pygame.event.get():
            pygame.display.flip()
            if event.type == pygame.QUIT: 
                sys.exit()
            if(player==1 or numPlayers == 2):
                if event.type == pygame.MOUSEBUTTONUP:
                    pos=pygame.mouse.get_pos()
                    column = find_column(pos)
                    if column > 7: break
                    if column < 1: break
                    row = find_row(column, board)
                    #print(column)
                    if row < 1: break
                    #print(find_row(column))
                    board.loc[row,column] = player
                    add_piece(row, column, player)
                    win = check_win(board, player)
                    #if(win): print("you win")
                    player = 3 - player
                    pygame.display.flip()
            else:
                row = -1
                while(row < 1):
                    column = get_move(board)
                    row = find_row(column, board)
                board.loc[row,column] = player
                add_piece(row, column, player)
                win = check_win(board, player)
                player = 3 - player
                pygame.display.flip()
        pygame.display.flip()
            


sys.exit()