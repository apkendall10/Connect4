import numpy as np, random, pandas as pd
class board:
    board_data = pd.DataFrame()
    def __init__(self, size):
        self.game_size=size
        self.board_data = pd.DataFrame(data = 0, index = range(1,size) , columns = range(1,size+1))

    def find_row(self, column):
        ret = self.game_size-1
        for row in self.board_data.index:
            if(self.board_data.loc[row,column]>0):
                return row-1
        return ret

    def check_tie(self):
        for column in self.board_data.columns:
            if(self.board_data.loc[1,column]==0):
                return False
        return True

    def check_helper(self, player, row, column, count, dir):
        x , y = dir
        newRow = row + x
        newColumn = column + y
        if(newRow not in self.board_data.index):
            return 0
        if(newColumn not in self.board_data.columns):
            return 0
        if(self.board_data.loc[newRow, newColumn] != player):
            return 0
        if(count==1):
            #print(player, newRow, newColumn, dir, sep=" ")
            return 1
        return self.check_helper(player, newRow, newColumn, count-1, dir)
    def count_near_win(self, player, length):
        count = 0
        for row in self.board_data.index:
            for column in self.board_data.columns:
                if(self.board_data.loc[row, column]==player):
                    for x in (-1, 0, 1):
                        for y in (-1,0,1):
                            dir = (x,y)
                            if(dir != (0,0)):
                                count = count + self.check_helper(player, row,column, length, dir)
        return count
    
    def check_win(self ,player):
        for row in self.board_data.index:
            for column in self.board_data.columns:
                if(self.board_data.loc[row, column]==player):
                    for x in (-1, 0, 1):
                        for y in (-1,0,1):
                            dir = (x,y)
                            if(dir != (0,0)):
                                if(self.check_helper(player, row, column, 3, dir)==1):
                                    return True
        return False
    def print_board(self):
        val = ""
        for row in self.board_data.index:
            for col in self.board_data.columns:
                val = val + str(self.board_data.loc[row, col]) + ","
        return val

    def set_loc(self, row, column, val):
        self.board_data.loc[row,column] = val

    def do_move(self, column, player):
        row = self.find_row(column)
        if(row in self.board_data.index):
            self.set_loc(row, column, player)
    def copy(self):
        newBoard = board(self.game_size)
        for row in self.board_data.index:
            for col in self.board_data.columns:
                newBoard.set_loc(row,col,self.board_data.loc[row,col])
        return newBoard
    
    def get_valid_columns(self):
        ret = []
        for col in self.board_data.columns:
            if(self.find_row(col)>0):
                ret.append(col)
        return ret
        
    def get_array(self):
        return self.board_data