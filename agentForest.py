import  numpy as np, random, pandas as pd, board, agent

def shuffle(df, n=1, axis=0):     
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df

class agentForest:
    def __init__(self, size, file = "gamelog.txt"):
        self.k = size
        self.fileName = file
        self.agentList = []
        data = pd.read_csv(self.fileName)
        for val in data['score']:
            if val < 0:
                val = -1
            else:
                val = 1
        data = shuffle(data)
        dataSet = np.array_split(data, self.k)
        for agentIndex in range(1,self.k):
            self.agentList.append(agent.agent(1, 7, dataSet[agentIndex]))
    
    def get_move(self, board, player, numAgents):
        picks = np.random.permutation(self.k)
        score = 0
        choice = -1
        min = 100
        max = -100
        for col in board.get_valid_columns():
            state = board.copy()
            state.do_move(col,player)
            for agent in picks:
                score = score + self.agentList[agent-1].calc_nn_move(state, player)
            if(player==1):
                if(score < min):
                    min = score
                    choice = col
            else:
                if(score > max):
                    max = score
                    choice = col
        return choice
        