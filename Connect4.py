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

def draw_circle(pos,color,r=20):
    x, y = pos
    pygame.draw.circle(screen,color,(x,y),r)
    pygame.draw.circle(screen,black,(x,y),r,1)

def add_piece(row, column, player):
    color = colorMap[player]
    draw_circle((column * 60, row * 60), color)

board = pd.DataFrame(data = 0, index = range(1,7) , columns = range(1,8))

def draw_board(board):
    for i in board.index:
        for j in board.columns:
            add_piece(i,j,0)
def find_column(pos):
    x,y = pos
    return round(x/60)
def find_row(column):
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
        print(player, newRow, newColumn, dir, sep=" ")
        return True
    return check_helper(board, player, newRow, newColumn, count-1, dir)

def check_win(board,player):
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

draw_board(board)

player=1
win = False
while not win:
    for event in pygame.event.get():
        pygame.display.flip()
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            column = find_column(pos)
            if column > 7: break
            row = find_row(column)
            #print(column)
            if row < 1: break
            #print(find_row(column))
            board.loc[row,column] = player
            add_piece(row, column, player)
            win = check_win(board, player)
            #if(win): print("you win")
            player = 3 - player
        pygame.display.flip()
            


sys.exit()