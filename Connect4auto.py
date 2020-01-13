import  numpy as np, random, pandas as pd, board, agent, sys, pyautogui, time, agentForest

#Set defaults for number of training runs and weather to keep the computer awake automatically
trainingstep = 2
stayAwake = False
agentType = 1
timedBasedTraining = False
fileName = "rivalLog.txt"
recalc = False
#check user input for these variables
if(len(sys.argv) > 1 and not sys.argv[1].isalpha()):    
    trainingstep = float(sys.argv[1])
if(len(sys.argv) > 2 and sys.argv[2].isalpha()):
    timedBasedTraining = (sys.argv[2]=='T')
if(len(sys.argv) > 3):
    fileName = sys.argv[3]
if(len(sys.argv) > 4 and sys.argv[4].isalpha()):
    recalc = (sys.argv[5]=='recalc')
pyautogui.FAILSAFE = False

#Initialize variables and objects
start = time.time()
currentTime = time.time() - start
if timedBasedTraining: trainingstep = trainingstep * 3600
file = open(fileName,"a")
size = 7
#agent1 = agentForest.agentForest(4, "cnnLog2.txt",2)
agent1 = agent.agent(4, 7, "noData")
agent2 = agent.agent(3, 7, "noData")
updatestep = (trainingstep / 10)
updatestepsize = updatestep

#iteratively run through the model
currentstep = 1
while((not timedBasedTraining and currentstep < trainingstep) or (timedBasedTraining and currentTime < trainingstep)):
    
    #set up game state for each model
    if((not timedBasedTraining and (currentstep % updatestep == 0)) or (timedBasedTraining and (currentTime > updatestep))):
        print(currentstep, currentTime)
        if(timedBasedTraining): updatestep = updatestep + updatestepsize
    currentstep = currentstep + 1
    currentTime = time.time() - start
    b = board.board(size)
    gameStates = []
    turnCount = 0
    startPlayer = 1
    agentPlayer = random.randint(1,2)
    player = startPlayer
    win = False
    
    #run the model
    while not (win or b.check_tie()):
        if player == agentPlayer:
            column = agent1.get_move(b,player)
        else:
            column = agent2.get_move(b,player)
        if column not in b.get_valid_columns(): 
                break
        #row = b.find_row(column)
        gameStates.append(b.print_board() + str(column) + ",")
        b.do_move(column, player)
        win = b.check_win(player)
        #turnCount = turnCount +1
        
        player = 3 - player
    
    #capture game outcome and store as future input for the  ml agent
    player = 3 - player
    gameStates.append(b.print_board() + str(column) + ",")
    outcome = (player - 1.5) * 2
    if(b.check_tie()): outcome = 0
    counter = -1
    player = startPlayer
    for state in gameStates:
        val = "\n" + state + str(player) + "," + str(outcome) 
        file.write(val)   
        player = 3- player
    
    
file.close()
if recalc:
    agent1 = agentForest.agentForest(3, fileName, 1)