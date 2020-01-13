import pyautogui, time, sys

#Set defaults for number of training runs and weather to keep the computer awake automatically
trainingTime = 100

#check user input for these variables
if(len(sys.argv) > 1 and not sys.argv[1].isalpha()):    
    trainingTime = float(sys.argv[1])

pyautogui.FAILSAFE = False
start = time.time()
currentTime = time.time() - start
trainingTime = trainingTime * 3600
while(currentTime < trainingTime):
    for i in range(0,3):
        pyautogui.moveTo(0,i*100)
    pyautogui.moveTo(1,1)
    for i in range(0,3):
        pyautogui.press("shift")
    currentTime = time.time() - start
