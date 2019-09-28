import  numpy as np, random, pandas as pd, board, agent, sys, pyautogui, time

trainingstep = 100                                      #default number of times to run
stayAwake = False                                       #by default do not keep the computer awake
if(len(sys.argv) > 1 and not sys.argv[1].isalpha()):    #check user input for number of times to run
    trainingstep = int(sys.argv[1])
if(len(sys.argv) > 2 and sys.argv[2].isalpha()):        #check user input to see if we should keep the computer awake
    stayAwake = (sys.argv[2]=='awake')
pyautogui.FAILSAFE = False

file = open("gameoutput.txt","a")                       #file location for game logs. Will be used to store data from each game for the ml agent
size = 7                                                #size of the game board. In theory could expand to different size games
agent1 = agent.agent(1, size) #
updatestep = (trainingstep / 10)
for currentstep in range(1,trainingstep+1):
    if(currentstep % updatestep == 0):
        print(currentstep)
    agent1.train()
    b = board.board(size)
    gameStates = []
    turnCount = 0
    startPlayer = random.randint(1,2)
    player = startPlayer
    win = False
    while not (win or b.check_tie()):
        moveDone = False
        column = agent1.get_move(b,player)
        if column not in b.get_valid_columns(): 
                break
        moveDone = True
        if(moveDone):
            row = b.find_row(column)
            b.do_move(column, player)
            win = b.check_win(player)
            turnCount = turnCount +1
            gameStates.append(b.print_board())
            player = 3 - player
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
    if(stayAwake)
        for i in range(0,200):
            pyautogui.moveTo(0,i*4)
        pyautogui.moveTo(1,1)
        for i in range(0,3):
            pyautogui.press("shift")
file.close()