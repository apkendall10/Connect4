import  numpy as np, random, pandas as pd, board, agent, sys, pyautogui, time

#Set defaults for number of training runs and weather to keep the computer awake automatically
trainingstep = 100
stayAwake = False
agentType = 1
#check user input for these variables
if(len(sys.argv) > 1 and not sys.argv[1].isalpha()):    
    trainingstep = int(sys.argv[1])
if(len(sys.argv) > 2 and sys.argv[2].isalpha()):
    stayAwake = (sys.argv[2]=='awake')
pyautogui.FAILSAFE = False

#Initialize variables and objects=
file = open("gameoutput.txt","a")
size = 7
agent1 = agent.agent(agentType, size)
updatestep = (trainingstep / 10)
firstrun = False
#iteratively run through the model
start = time.time()
for currentstep in range(1,trainingstep+1):
    #set up game state for each model
    if(currentstep % updatestep == 0):
        print(currentstep, (time.time() - start))
    firstrun = not firstrun
    if not firstrun: agent1.train()
    b = board.board(size)
    gameStates = []
    turnCount = 0
    if firstrun: startPlayer = random.randint(1,2)
    else: startPlayer = 3 - startPlayer
    player = startPlayer
    win = False
    #run the model
    while not (win or b.check_tie()):
        column = agent1.get_move(b,player)
        if column not in b.get_valid_columns(): 
                break
        row = b.find_row(column)
        b.do_move(column, player)
        win = b.check_win(player)
        turnCount = turnCount +1
        gameStates.append(b.print_board())
        player = 3 - player
    #capture game outcome and store as future input for the  ml agent
    #end = time.time()
    #print("playing took", (end - start))
    player = 3 - player
    outcome = (player - 1.5) * 2
    if(b.check_tie()): outcome = 0
    counter = -1
    player = startPlayer
    for state in gameStates:
        counter = counter + 1
        val = "\n" + state + str(player) + "," + str(outcome/(turnCount - counter))
        file.write(val)   
        player = 3- player
    #keep the computer awake
    if(stayAwake):
        for i in range(0,3):
            pyautogui.moveTo(0,i*100)
        pyautogui.moveTo(1,1)
        for i in range(0,3):
            pyautogui.press("shift")
file.close()