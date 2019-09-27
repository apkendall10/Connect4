import numpy as np, random, pandas as pd
class board:
    board_data = pd.DataFrame()
    def __init__(self, size):
        self.game_size=size
        self.board_data = pd.DataFrame(data = 0, index = range(1,size) , columns = range(1,size+1))

    def find_row(self, column):
        ret = self.game_size-1
        for i in board_data.index:
            if(board_data.loc[i,column]>0):
                return i-1
        return ret

    def check_tie(self):
        for column in board_data.columns:
            if(board_data.loc[1,column]==0):
                return False
        return True

    def check_helper(self, player, row, column, count, dir):
        x , y = dir
        newRow = row + x
        newColumn = column + y
        if(newRow not in board_data.index):
            return 0
        if(newColumn not in board_data.columns):
            return 0
        if(board_data.loc[newRow, newColumn] != player):
            return 0
        if(count==1):
            #print(player, newRow, newColumn, dir, sep=" ")
            return 1
        return check_helper(player, newRow, newColumn, count-1, dir)

    def check_win(self ,player):
        for row in board_data.index:
            for column in board_data.columns:
                if(board_data.loc[row, column]==player):
                    for x in (-1, 0, 1):
                        for y in (-1,0,1):
                            dir = (x,y)
                            if(dir != (0,0)):
                                if(check_helper(player, row, column, 3, dir)==1):
                                    return True
        return False
    def print_board(self):
        val = ""
        for row in self.board_data.index:
            for col in self.board_data.columns:
                val = val + str(self.board_data.loc[row, col]) + ","
        return val