import  numpy as np, random, pandas as pd, board, agent, time
from joblib import dump, load

# Agent Types
# 1 Retrain SBE
# 2 Load SBE
# 5 Retrain next move
# 6 Load next move

def shuffle(df, n=1, axis=0):     
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df

class agentForest:
    def __init__(self, size, file = "gamelog.txt", agentType = 1):
        start = time.time()
        
        self.k = size
        self.fileName = file
        self.agentList = []
        if agentType == 1 or agentType == 5:
            data = pd.read_csv(self.fileName).dropna()
            data['score'] = data['score'].apply(lambda x: 0 if x < 0 else 1)
            data = data.sample(frac=1).reset_index(drop=True)
            dataSet = np.array_split(data, self.k)
        for agentIndex in range(1,self.k+1):
            if agentType == 1 or agentType == 2:
                prefix = "Agent JobLib/agent" 
            else:
                prefix = "Agent JobLib/moveAgent" 
            fileName = prefix + str(agentIndex) + ".joblib"
            if agentType == 1 or agentType == 5:
                #dataSet = data.sample(frac=2/5).reset_index(drop=True)
                self.agentList.append(agent.agent(agentType, 7, dataSet[agentIndex-1], fileName))
            else:
                self.agentList.append(agent.agent(agentType, 7, ['null'], fileName))
                #dump(self.agentList[agentIndex-1].nn, fileName)
        currentTime = time.time() - start
        print("Done intitializing agentForest Type", agentType, currentTime)
                
    
    def get_move(self, board, player, numAgents):
        score = 0
        choice = -1
        min = 100
        max = -100
        agents = range(0,self.k)
        for col in board.get_valid_columns():
            score = 0
            state = board.copy()
            state.do_move(col,player)
            #print("starting choice")
            for agent in self.agentList:
            #for cycle in range(0,numAgents):
                #agent = random.choice(agents)
                #score = score + self.agentList[agent].calc_nn_move(state, player)
                score = score + agent.calc_nn_move(state, player)
                #print("Using agent ",agent)
            if(player==1):
                if(score < min):
                    min = score
                    choice = col
            else:
                if(score > max):
                    max = score
                    choice = col
        return choice

    def get_learned_move(self, board, player):
        agents =  range(0,len(self.agentList))
        agent = random.choice(agents)
        return self.agentList[agent].get_move(board, player)

    def evaluate_board(self, board, player):
        agents = range(0,self.k)
        agent = random.choice(agents)
        return self.agentList[agent].calc_nn_move(board, player)

    def debug_move(self, board, player):
        for agent in range(0,self.k):
            print(self.agentList[agent].calc_nn_move(board, player))
        