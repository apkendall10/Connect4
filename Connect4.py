import sys, pygame, numpy as np, random, pandas as pd, board, agent

agentType = 1
if(len(sys.argv) > 1 and not sys.argv[1].isalpha()):    
    agentType = int(sys.argv[1])
pygame.init
size = width, height = 600, 480
screen = pygame.display.set_mode(size)
fileName = "gameoutput.txt"
file = open(fileName,"a") 
size = 7
white = (255, 255, 255)
blue = (100,100,200)
red = (200,100,100)
green = (100,200,100)
black=(0,0,0)
colorMap = {
        0: white,
        1: red,
        2: black
        }
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)
b = board.board(size)
agent1 = agent.agent(agentType, size, fileName)

def draw_circle(pos,color,r=20):
    x, y = pos
    pygame.draw.circle(screen,color,(x,y),r)
    pygame.draw.circle(screen,black,(x,y),r,1)
def display_piece(row, column, player):
    color = colorMap[player]
    draw_circle((int(column * 60),int(row * 60)), color)
def display_board(board):
    state = board.get_array()
    for row in state.index:
        for col in state.columns:
            display_piece(row,col,0)
def find_column(pos):
    x,y = pos
    return round((x)/60)
class button:
    def __init__(self,pos,name,color,screen,size=(80,50)):
        self.tile=pygame.Rect(pos,size)
        pygame.draw.rect(screen,color,self.tile)
        pygame.draw.rect(screen,black,self.tile,3)
        textsurface = myfont.render(name,False,black)
        x,y=self.tile.center
        x=x-len(name)*2.5
        screen.blit(textsurface,(x,y))
    def has(self,pos):
        return self.tile.collidepoint(pos)

player_0=button((0,0),"0 Players",green,screen,(200,480))
player_1=button((200,0),"1 Players",blue,screen,(200,480))
player_2=button((400,0),"2 Players",red,screen,(200,480))
numPlayers=-1

while numPlayers==-1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos=pygame.mouse.get_pos()
            if player_1.has(pos):
                numPlayers=1
            if player_2.has(pos):
                numPlayers=2
            if player_0.has(pos):
                numPlayers=0
    pygame.display.flip()

screen.fill(blue)
trainingstep = 1
if (numPlayers==0):
    trainingstep = 20
for it in range(1,trainingstep+1):
    b = board.board(size)
    display_board(b)
    gameStates = []
    turnCount = 0
    startPlayer = random.randint(1,2)
    player = startPlayer
    win = False
    while not (win or b.check_tie()):
        moveDone = False
        pygame.display.flip()
        for event in pygame.event.get():
            pygame.display.flip()
            if event.type == pygame.QUIT: 
                sys.exit()
            if(not numPlayers==0 and (player==1 or numPlayers == 2)):
                if event.type == pygame.MOUSEBUTTONUP:
                    pos=pygame.mouse.get_pos()
                    column = find_column(pos)
                    if column not in b.get_valid_columns(): 
                        break
                    moveDone = True          
            else:
                column = agent1.get_move(b,player)
                if column not in b.get_valid_columns(): 
                        break
                moveDone = True
            if(moveDone):
                row = b.find_row(column)
                b.do_move(column, player)
                display_piece(row, column, player)
                win = b.check_win(player)
                turnCount = turnCount +1
                gameStates.append(b.print_board())
                player = 3 - player
        pygame.display.flip()
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
file.close()

sys.exit()