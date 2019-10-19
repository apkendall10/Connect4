import  numpy as np, random, pandas as pd, board, agent

def shuffle(df, n=1, axis=0):     
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df

class agentForest:
    def __init__(self, size, file = "gameoutput.txt"):
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
        #for agentIndex in range(1,self.k):
        #    agentList.add(agent.agent(1, 7, dataSet[agentIndex]))

agentForest(2)
        