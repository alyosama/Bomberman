#BomberMan Game
#by Aly Osama alyosama@hotmail.com
#Beta edition 

import pygame,sys,os,random,time,traceback
from pygame.locals import *

#Constants
FPS=25
SCREENX=550
SCREENY=500
ELEMENTSIZE=50

BROKENBLOCK='B'
FIXEDBLOCK='X'
EMPTY=' '
PLAYER='P'
BOMB='BOMB'

BONUSLIVE=1
BONUSPOWER=2
BONUSBOMB=3
BONUSSPEED=4
BONUS=[BONUSLIVE,BONUSPOWER,BONUSBOMB]

#set up the colors
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

players=[]
class Player(object):
    playerName=''
    playerSpeed=5
    playerBombs=1
    playerPower=1
    playerLives=1
    is_alive=True
    is_gameOver=False
    bombs=[]
    img=''
    def __init__(self,pos,img,name):
        players.append(self)
        self.playerName=name
        self.rect = pygame.Rect(pos[0],pos[1], ELEMENTSIZE, ELEMENTSIZE)
        self.img=pygame.image.load(img)
    def move(self, dx, dy):     
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    def move_single_axis(self, dx, dy):   
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
        for block in blocks:
            if self.rect.colliderect(block.rect) and ( blocks[block]==FIXEDBLOCK or blocks[block]==BROKENBLOCK ) :
                if dx > 0: # Moving right
                    self.rect.right = block.rect.left
                if dx < 0: # Moving left
                    self.rect.left = block.rect.right
                if dy > 0: # Moving down
                    self.rect.bottom = block.rect.top
                if dy < 0: # Moving up
                    self.rect.top = block.rect.bottom
            if self.rect.colliderect(block.rect) and blocks[block] in BONUS:
                block.getBonus(self)
                    
    def setPlayer(self,pos):
        self.rect.x,self.rect.y=pos[0],pos[1]
        self.is_alive=True
        self.playerSpeed=5
        self.playerBombs=1
        self.playerPower=1
        self.playerLives=1
        self.bombs=[]
        self.is_gameOver=False
    def throwBomb(self,startTime):
        if(self.playerBombs>0):
            self.bombs.append(Bomb((self.rect.x,self.rect.y),startTime))#Create Bombs
            self.playerBombs-=1
    def playerDie(self):
        self.playerLives-=1
        if self.playerLives==0:
            self.is_alive=False
            self.is_gameOver=True
            
#Create the Players            
player = Player((ELEMENTSIZE,ELEMENTSIZE),'img/man.png','Player One')
player2=Player((SCREENX-2*ELEMENTSIZE,SCREENY-3*ELEMENTSIZE),'img/player2.png','Player Two')

blocks={}
class Block(object):
    def __init__(self, pos,BlockType):
        blocks[self]=BlockType
        self.rect = pygame.Rect(pos[0], pos[1], ELEMENTSIZE, ELEMENTSIZE)
    def getBonus(self,player):
        if blocks[self]==BONUSLIVE:
            player.playerLives+=1
        #elif blocks[self]==BONUSSPEED:
          #  player.playerSpeed+=0.5
        elif blocks[self]==BONUSBOMB:
            player.playerBombs+=1
        elif blocks[self]==BONUSPOWER:
            player.playerPower+=1
        blocks[self]=EMPTY
        bonusSound.play()

K_SPACE_FLAG1=True
K_SPACE_FLAG2=True

class Bomb(object):
    bombTime=3
    bombExplodedTime=0
    def __init__(self,pos,startTime):
        self.bombExplodedTime=startTime+self.bombTime
        self.rect = pygame.Rect(pos[0], pos[1], ELEMENTSIZE, ELEMENTSIZE)
    def getBombExplodedTime(self):
        return self.bombExplodedTime
    def bombExploded(self,player):
        bombSound.play()
        DISPLAYSURF.blit(bomb3Img,bomb.rect)
        player.bombs.remove(self)
        player.playerBombs+=1 
        #removeBlocks
        coordinatesBomb=coordinatesManipulation((self.rect.x,self.rect.y))
        for i in range(-ELEMENTSIZE*player.playerPower,player.playerPower*ELEMENTSIZE+ELEMENTSIZE,ELEMENTSIZE):
            for block in blocks:
                if not blocks[block]==FIXEDBLOCK and block.rect==(coordinatesBomb[0],coordinatesBomb[1]+i,ELEMENTSIZE,ELEMENTSIZE) :
                    DISPLAYSURF.blit(fireImg,(coordinatesBomb[0],coordinatesBomb[1]+i,ELEMENTSIZE,ELEMENTSIZE))
                    if blocks[block]==BROKENBLOCK:
                        blocks[block]=EMPTY
                        if self.is_Bonus():
                            Bonus((coordinatesBomb[0],coordinatesBomb[1]+i),block)
                if not blocks[block]==FIXEDBLOCK and block.rect==(coordinatesBomb[0]+i,coordinatesBomb[1],ELEMENTSIZE,ELEMENTSIZE) :
                    DISPLAYSURF.blit(fireImg,(coordinatesBomb[0]+i,coordinatesBomb[1],ELEMENTSIZE,ELEMENTSIZE))
                    if blocks[block]==BROKENBLOCK:
                        blocks[block]=EMPTY
                        if self.is_Bonus():
                            Bonus((coordinatesBomb[0]+i,coordinatesBomb[1]),block)
                #player Dies
                for person in players:
                    if coordinatesManipulation((person.rect.x,person.rect.y))==(coordinatesBomb[0]+i,coordinatesBomb[1]):
                            person.playerDie()
                            break
                    if coordinatesManipulation((person.rect.x,person.rect.y))==(coordinatesBomb[0],coordinatesBomb[1]+i):
                            person.playerDie()
                            break
    def is_Bonus(self):
        randB=random.randint(0,2)
        if randB==1:
            return True
        else:
            return False
                    
class Bonus(Block):
    def __init__(self,pos,block):
       self.rect = pygame.Rect(pos[0], pos[1], ELEMENTSIZE, ELEMENTSIZE)
       blocks[block]=self.generateBonus()    
    def generateBonus(self):
        return random.randint(BONUS[0],BONUS[len(BONUS)-1])
        
def coordinatesManipulation(pos):
        x,y=pos[0],pos[1]
        deflectx,deflecty=x%ELEMENTSIZE,y%ELEMENTSIZE
        if deflectx>ELEMENTSIZE:
            x=x-deflectx+ELEMENTSIZE
        else:
            x=x-deflectx
        if deflecty>ELEMENTSIZE:
            y=y-deflecty+ELEMENTSIZE
        else:
            y=y-deflecty   
        return (x,y)
    

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
fpsClock=pygame.time.Clock()
DISPLAYSURF=pygame.display.set_mode((SCREENX,SCREENY),0,32)
pygame.display.set_caption('Bomber Man | Aly Osama')

#music bakground and Sounds Effects
pygame.mixer.music.load('sound/background.mp3')
bombSound = pygame.mixer.Sound('sound/bomb.wav')
gameoverSound = pygame.mixer.Sound('sound/gameover.wav')
bonusSound = pygame.mixer.Sound('sound/bonus.wav')


#Fonts
fontObj=pygame.font.Font(None,24)
fontObj1=pygame.font.Font(None,70)
fontObj2=pygame.font.Font(None,20)
gameOverText=fontObj1.render("Game Over",True,WHITE,BLACK)
gameOverTextRect=gameOverText.get_rect()
gameOverTextRect.center=(SCREENX//2,SCREENY//2)
continueText=fontObj2.render("Press \"ESCAPE\" to Exit or \"SPACE\" to New Game",True,WHITE,BLACK)
continueTextRect=continueText.get_rect()
continueTextRect.center=(275,475)
wonText=fontObj.render("Winner",True,WHITE,BLACK)
#Images
bblockImg=pygame.image.load('img/bblock.png')
fblockImg=pygame.image.load('img/fblock.png')
bomb1Img=pygame.image.load('img/bomb1.png')
bomb2Img=pygame.image.load('img/bomb2.png')
bomb3Img=pygame.image.load('img/bomb3.png')
fireImg=pygame.image.load('img/fire.png')
bonusImg=pygame.image.load('img/bonus.png')


#Map
def generateMap():
    blocks.clear()
    player.setPlayer((ELEMENTSIZE,ELEMENTSIZE))
    player2.setPlayer((SCREENX-2*ELEMENTSIZE,SCREENY-3*ELEMENTSIZE))
    pygame.mixer.music.play(-1, 0.0)
    gameoverSound.stop()
    
    LEVEL =["XXXXXXXXXXX",
            "XPP       X",
            "XPX X X X X",
            "X         X",
            "X X X X X X",
            "X         X",
            "X X X X XPX",
            "X       PPX",
            "XXXXXXXXXXX"]

    #Create Blocks
    blockx=0
    blocky=0
    for row in LEVEL:
        for element in row:
            if element==FIXEDBLOCK:
                Block((blockx, blocky),FIXEDBLOCK)
            elif element==EMPTY:
                if random.randint(0,1)==0:
                    Block((blockx, blocky),EMPTY)
                else:
                    Block((blockx, blocky),BROKENBLOCK)
            elif element==PLAYER:
                Block((blockx, blocky),EMPTY)
            blockx+=50
        blockx=0
        blocky+=50
        
generateMap()

def gameOver():
    pygame.draw.rect(DISPLAYSURF,BLACK,(0,0,SCREENX,SCREENY))
    DISPLAYSURF.blit(gameOverText,gameOverTextRect)
    DISPLAYSURF.blit(continueText,continueTextRect)
    bombSound.stop()
    pygame.mixer.music.stop()
    for person in players:
        if  person.is_gameOver:
            gameoverSound.play()
            person.is_gameOver=False
        if person.is_alive:
            wonText=fontObj.render(person.playerName+" Win the Game",True,WHITE,BLACK)
            wonTextRect=wonText.get_rect()
            wonTextRect.center=(SCREENX//2,SCREENY//2+ELEMENTSIZE)
            DISPLAYSURF.blit(wonText,wonTextRect)
            DISPLAYSURF.blit(person.img,(SCREENX//2-ELEMENTSIZE//2,SCREENY//2+2*ELEMENTSIZE))
    

    
running=True
def terminate():
    running=False
    pygame.mixer.music.stop()
    pygame.quit()
    os._exit(1)

while running:
    fpsClock.tick(FPS)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            terminate()
        if e.type == pygame.KEYDOWN and e.key ==pygame.K_ESCAPE:
            terminate()
        if e.type==pygame.KEYUP and e.key==K_SPACE and K_SPACE_FLAG1 == False:
            K_SPACE_FLAG1=True
        if e.type==pygame.KEYUP and e.key==K_k and K_SPACE_FLAG2 == False:
            K_SPACE_FLAG2=True
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[K_LEFT]:
        player.move(-player.playerSpeed, 0)
    if key[K_RIGHT]:
        player.move(player.playerSpeed, 0)
    if key[K_UP]:
        player.move(0, -player.playerSpeed)
    if key[K_DOWN]:
        player.move(0,player.playerSpeed)
    if key[K_SPACE]  and K_SPACE_FLAG1 == True :
        player.throwBomb(time.time())
        K_SPACE_FLAG1 = False
    #PlayerTwo
    if key[K_a]:
        player2.move(-player2.playerSpeed, 0)
    if key[K_d]:
        player2.move(player2.playerSpeed, 0)
    if key[K_w]:
        player2.move(0, -player2.playerSpeed)
    if key[K_s]:
        player2.move(0,player2.playerSpeed)
    if key[K_k]  and K_SPACE_FLAG2 == True :
        player2.throwBomb(time.time())
        K_SPACE_FLAG2 = False
    #new Game
    if key[K_SPACE] and (player.is_alive==False or player2.is_alive==False) :
        generateMap()

    # Draw the scene 
    DISPLAYSURF.fill((240,197,192))
    pygame.draw.rect(DISPLAYSURF,BLACK,(0,450,550,50))
    textSurfaceObj=fontObj.render("Lives: "+str(player.playerLives)
                                  +" "+"Power: "+str(player.playerPower)
                                  +" "+"Bombs: "+str(player.playerBombs),True,WHITE)
    DISPLAYSURF.blit(textSurfaceObj,(52,460))
    DISPLAYSURF.blit(player.img,(0,450))
    textSurfaceObj=fontObj.render("Lives: "+str(player2.playerLives)
                                  +" "+"Power: "+str(player2.playerPower)
                                  +" "+"Bombs: "+str(player2.playerBombs),True,WHITE)
    DISPLAYSURF.blit(textSurfaceObj,(285,475))
    DISPLAYSURF.blit(player2.img,(500,450))
    for block in blocks:
        if blocks[block]==FIXEDBLOCK:
            DISPLAYSURF.blit(fblockImg,block.rect)
        elif blocks[block]==BROKENBLOCK:
            DISPLAYSURF.blit(bblockImg,block.rect)
        if blocks[block] in BONUS:
            DISPLAYSURF.blit(bonusImg,block.rect)
    for person in players:
        for bomb in person.bombs:
            DISPLAYSURF.blit(bomb2Img,bomb.rect)
            if bomb.getBombExplodedTime()<=time.time():
                bomb.bombExploded(person)
        if person.is_alive: 
            DISPLAYSURF.blit(person.img,person.rect)
        else:
            gameOver()
            
    pygame.display.update()
