import agentForest, sys


fileName = "gamedata.txt"
#check user input for these variables
if(len(sys.argv) > 1):
    fileName = sys.argv[1]

agent1 = agentForest.agentForest(5, fileName, 5)