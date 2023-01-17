# NAVIGATOR
import random
import math
import sys
import os
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.display.init()
pygame.font.init()

pygame.mouse.set_visible(False)

# GAME CONSTANTS
#------------------------------------------------------------------------------------------------------------------

# SCREEN                                                                                                                            
screenSize = [800,800] # Default = [800,800]                                                        
fps = 60 # Default = 60                                    
timerSize = 75 # Default = 100                             
timerColor = [255,255,255] # Default = [255,255,255] 
timerDelay = 1000 # Default = 1000

# LEVEL COUNTER
levelSize = 50 # Default = 50                                                                                                                                                                   
levelColor = [255,255,255] # Default = [255,255,255] 

# BACKGROUND CLOUD
cloudSpeed = 1 # Default = 1
cloudStart = -1000 # Default = -1000
cloudSpeedMult = 1.5 # Default = 1.5

# GAME OVER SCREEN
gameOverColor = [255,0,0] # Default = [255,0,0]
gameOverSize = 100 # Default = 100
helpSize = 30 # Default = 30 
helpColor = [0,255,0] # Default = [0,255,0]
finalScoreSize = 40 # Default = 40
finalScoreColor = [0,255,0] # Default = [0,255,0]
pausedSize = 100 # Default = 100
pausedColor = [255,255,255] # Default = [255,255,255]
pauseMax = 6

# START MENU
maxIcons = 3
maxIconSpeed = 5
maxIconRotationSpeed = 3
startSize = 120 # Default = 150
startColor = [0,255,0] # Default = [0,255,0]
minIconSize = 30
maxIconSize = 100

# PLAYER           
playerSpeed = 5 # Default = 5
savedShipNum = 0

# OBSTACLES
obstacleSpeed = 4  # Default = 4           
obstacleSize = 30    # Default = 30
maxObstacles = 12  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" (Can be updated by level)

# LEVELS  
levelTimer = 15 # Default = 15 / Time between levels

speedIncrement = obstacleSpeed / 16 # Default = obstacleSpeed / 15
sizeIncrement = round(obstacleSize/8) # Default = round(obstacleSize/7)
numIncrement = maxObstacles / 6 # Default = maxObstacles / 4

# [ False , (levelNumber - 1) * levelTimer , BOUNDS, SPEED, SIZE, NUMBER ]
levelTwo = [ False, levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ] 
levelThree = [ False, 2 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ] 
levelFour = [ False, 3 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ] 
levelFive = [ False, 4 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ] 
levelSix = [ False, 5 * levelTimer, "WRAP", speedIncrement, sizeIncrement, numIncrement ] 
levelSeven = [ False, 6 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ] 
levelEight = [ False, 7 * levelTimer, "BOUNCE", speedIncrement, sizeIncrement, numIncrement ] 
levelNine = [ False, 8 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ]
levelTen = [ False, 9 * levelTimer, "WRAP", speedIncrement, sizeIncrement, numIncrement ]

overTimeOne = [ False, 10 * levelTimer, "KILL", speedIncrement, sizeIncrement * 2, - numIncrement/2 ]
overTimeTwo = [ False, 11 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ]
overTimeThree = [ False, 12 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ]

# DIVIDE INTO STAGES
stageOneLevels = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen] # Stage 1
overTimeLevels = [overTimeOne,overTimeTwo,overTimeThree]

# STORE IN LIST
stageList = [stageOneLevels, overTimeLevels] # List of stages

#---------------------------------------------------------------------------------------------------------------------------------

# STORE LEVEL DEFAULTS
savedConstants = {
                "obstacleSpeed" : obstacleSpeed, 
                "obstacleSize" : obstacleSize, 
                "maxObstacles" : maxObstacles, 
                "obstacleBoundaries" : obstacleBoundaries,
                "cloudSpeed" : cloudSpeed
                }

# LOAD GAME CONSTANTS
gameConstants = []

# GAME STATE
currentLevel = 1 
currentStage = 1

mainMenu = True # Assures start menu only runs once
screen = pygame.display.set_mode(screenSize) # Initialize screen

screenColor = [0,0,0] # Screen fill color 
creditsFontSize = 55 
creditsColor = [255,255,255]


def resource_path(relative_path):
    try: base_path = sys._MEIPASS    
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ASSET LOADING
curDir = resource_path('Assets')
obsDir = os.path.join(curDir, 'Obstacles') # Obstacle asset directory
mDir = os.path.join(obsDir, 'Meteors') # Meteor asset directory
uDir = os.path.join(obsDir, 'UFOs') # UFO asset directory
sDir = os.path.join(curDir, 'Spaceships') # Spaceship asset directory
bDir = os.path.join(curDir, 'Backgrounds') # Background asset directory
menuDir = os.path.join(curDir, 'MainMenu') # Start menu asset directory
rDir = os.path.join(os.getcwd(), 'Records') # Game records directory

# FONT
gameFont = ''
for filename in os.listdir(curDir):
    if filename.endswith('.ttf'):
        path = os.path.join(curDir, filename)
        gameFont = path
        break

# METEOR ASSETS
meteorList = []
for filename in os.listdir(mDir):
    if filename.endswith('.png'):
        path = os.path.join(mDir, filename)
        meteorList.append(pygame.image.load(resource_path(path)).convert_alpha())

# UFO ASSETS
ufoList = []
for filename in os.listdir(uDir):
    if filename.endswith('.png'):
        path = os.path.join(uDir, filename)
        ufoList.append(pygame.image.load(resource_path(path)).convert_alpha())

# BACKGROUND ASSETS
bgList = []
for filename in os.listdir(bDir):
    bgPath = os.path.join(bDir,filename)
    for nextBg in os.listdir(bgPath):
        
        stageBgPath = os.path.join(bgPath,'Background.png')
        stageCloudPath = os.path.join(bgPath,'Cloud.png')

        bg = pygame.image.load(resource_path(stageBgPath)).convert_alpha()
        cloud = pygame.image.load(resource_path(stageCloudPath)).convert_alpha()
        
        bgList.append([bg,cloud])
        break
        
# SPACESHIP ASSETS
spaceShipList = []
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'spaceShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'yellowShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'blackAndGoldShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'blackAndRedShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'blueShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'purpleShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'taxiShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'greyAndRedShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'greenShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'orangeShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'rastaShip.png'))).convert_alpha())

# ALL OBSTACLE ASSETS
obstacleImages = [meteorList,ufoList]
        
# MAIN MENU ASSETS
menuList = []
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'A.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'O.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'big.png'))).convert_alpha()) 
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'left.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'right.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'dblue.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'lblue.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'lgreen.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'dgreen.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'orange.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'red.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'white.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'yellow.png'))).convert_alpha())

# WINDOW
pygame.display.set_caption('Navigator')
pygame.display.set_icon(menuList[0])

# LOAD GAME RECORDS
overallHighScorePath = os.path.join(rDir,'OverallHighScore.txt')
totalAttemptsPath = os.path.join(rDir,'TotalAttempts.txt')

if not os.path.exists(rDir):
    os.mkdir('Records')
    newFile = open(overallHighScorePath,'w')
    newFile.write('0')
    newFile.close()
    newFile = open(totalAttemptsPath,'w')
    newFile.write('0')
    newFile.close()

highScoreFile = open(overallHighScorePath,'r') # Open saved high score
attemptFile = open(totalAttemptsPath,'r')  # Open saved attempts count

savedOverallHighScore = int( highScoreFile.readline() ) # Loads high score
savedTotalAttempts = int ( attemptFile.readline() ) # Loads number of game attempts

highScoreFile.close()
attemptFile.close()

timerFont = pygame.font.Font(gameFont, timerSize)

# FOR RANDOM MOVEMENT    
topDir = ["S", "E", "W", "SE", "SW"]
leftDir = ["E", "S", "N", "NE", "SE"]
bottomDir = ["N", "W", "E", "NE", "NW"]
rightDir = ["W", "N", "S", "NW", "SW"]

restrictedTopDir = ["SE", "SW", "S"]
restrictedLeftDir = ["E", "NE", "SE"]
restrictedBottomDir = ["N", "NE", "NW"]
restrictedRightDir = ["NW", "SW", "W"]


# ROTATE IMAGE
def rotateImage(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    rotatedRect = rotated.get_rect(center=rect.center)
    return rotated,rotatedRect


class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.currentImageNum = 0         
            self.speed = playerSpeed
            self.image = spaceShipList[self.currentImageNum]
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.angle = 0
 
        # PLAYER MOVEMENT
        def movement(self):
            key = pygame.key.get_pressed()
            
            if key[pygame.K_w] or key[pygame.K_UP]: 
                self.rect.centery -= self.speed
                self.angle = 0
                
            if key[pygame.K_s] or key[pygame.K_DOWN]: 
                self.rect.centery += self.speed
                self.angle = 180
            
            if key[pygame.K_a] or key[pygame.K_LEFT]: 
                self.rect.centerx -= self.speed
                self.angle = 90
            
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.rect.centerx += self.speed
                self.angle = -90
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = 45
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = -45
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
                self.angle = -120
                
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
                self.angle = 120
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_a] or key[pygame.K_LEFT]): 
                self.angle = 0

            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]): 
                self.angle = 180
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]): 
                self.angle = -90
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_d] or key[pygame.K_RIGHT]): 
                self.angle = 0
 
        # WRAP AROUND SCREEN
        def wrapping(self):
            if self.rect.centery  > screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = screenSize[1]
            if self.rect.centerx > screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = screenSize[0]
                
        # GET NEXT SPACESHIP IMAGE
        def nextSpaceShip(self):
            if self.currentImageNum < len(spaceShipList)-1:
                self.image = spaceShipList[self.currentImageNum + 1]
                self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
                self.mask = pygame.mask.from_surface(self.image)
                self.currentImageNum+=1
            
        # GET NEXT SPACESHIP IMAGE
        def lastSpaceShip(self):
            if self.currentImageNum >= 1: 
                self.image = spaceShipList[self.currentImageNum - 1]
                self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
                self.mask = pygame.mask.from_surface(self.image)
                self.currentImageNum-=1
  

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = obstacleSpeed
        self.size = obstacleSize
        self.movement = getMovement(True)
        self.direction = self.movement[1]
        try:
            self.image = obstacleImages[currentStage - 1][currentLevel-1].convert_alpha()
        except:
            self.image = meteorList[random.randint(0,len(meteorList)-1)]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0
        
        spins = [-1,1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        

class Icon(pygame.sprite.Sprite):
    def __init__(self):
        spins = [-1,1]
        self.speed = random.randint(1,maxIconSpeed)
        self.movement = getMovement(False)
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.image = menuList[random.randint(5,len(menuList)-1)]
        size = random.randint(minIconSize,maxIconSize)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0
     

    def move(self):
        
        if "N" in self.direction: self.rect.centery -= self.speed                       
        if "S" in self.direction: self.rect.centery += self.speed                        
        if "E" in self.direction: self.rect.centerx += self.speed               
        if "W" in self.direction: self.rect.centerx -= self.speed  
        
        if self.angle >= 360 or self.angle <= -360: self.angle = 0
            
        self.angle += self.spinDirection * random.uniform(0, maxIconRotationSpeed)
        
        randomTimerUX = random.randint(screenSize[0] * 2,screenSize[0] * 4)
        randomTimerUY = random.randint(screenSize[1] * 2,screenSize[1] * 4)
        randomTimerLX = -1 * random.randint(screenSize[0], screenSize[0] * 3)
        randomTimerLY = -1 * random.randint(screenSize[0], screenSize[1] * 3)
        
        if (self.rect.centery > randomTimerUY) or (self.rect.centery < randomTimerLY) or (self.rect.centerx> randomTimerUX) or (self.rect.centerx < randomTimerLX):
            self.movement = getMovement(False)
            self.direction = self.movement[1]
            self.image = menuList[random.randint(5,len(menuList)-1)]
            self.speed = random.randint(1,maxIconSpeed)
            self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
            size = random.randint(minIconSize,maxIconSize)
            self.image = pygame.transform.scale(self.image, (size, size))

    def draw(self):
        drawing, drawee = rotateImage(self.image,self.rect,self.angle)
        screen.blit(drawing,drawee)


# REVERSE OBSTACLE MOVEMENT DIRECTION
def movementReverse(direction):
    if direction == "N": return "S"           
    elif direction == "S": return "N"                     
    elif direction == "E": return "W"           
    elif direction == "W": return "E"          
    elif direction == "NW": return "SE"         
    elif direction == "NE": return "SW"          
    elif direction == "SE": return "NW"
    elif direction == "SW": return "NE"


def randomEightDirection():
    directions = ["N","S","E","W","NW","SW","NE","SE"]
    direction = directions[random.randint(0, len(directions)-1)]
    return direction
    
    
# OBSTACLE POSITION GENERATION
def getMovement(eightDirections):
    top,bottom,left,right = [],[],[],[]
    
    if eightDirections: top, bottom, left, right = topDir, bottomDir, leftDir, rightDir
    else: top, bottom, left, right, = restrictedTopDir, restrictedBottomDir, restrictedLeftDir, restrictedRightDir
    X = random.randint(0, screenSize[0])
    Y = random.randint(0, screenSize[1])
    
    lowerX = random.randint(0, screenSize[0] * 0.05)
    upperX =  random.randint(screenSize[0] * 0.95, screenSize[0])
    lowerY  = random.randint(0, screenSize[1] * 0.05)
    upperY = random.randint(screenSize[1] * 0.95, screenSize[1])
    
    topDirection = top[random.randint(0, len(top) - 1)]
    leftDirection = left[random.randint(0, len(left) - 1)]
    bottomDirection = bottom[random.randint(0, len(bottom) - 1)]
    rightDirection = right[random.randint(0, len(right) - 1)]
    
    topBound = [X, lowerY, topDirection]
    leftBound = [lowerX, Y, leftDirection]
    bottomBound = [X, upperY, bottomDirection]
    rightBound = [upperX, Y, rightDirection]
 
    possible = [topBound, leftBound, rightBound, bottomBound]
    movement = possible[ random.randint(0, len(possible) - 1) ]
    
    position = [movement[0], movement[1]]
    direction = movement[2]
    move = [position,direction]
    return move 


# REMOVE ALL OBSTACLES
def killAllObjects(obstacles):
    for obstacle in obstacles:
        obstacle.kill()


# RESET LEVEL PROGRESS
def resetAllLevels(gameConstants):
    for stage in gameConstants:
        for levels in stage:
            levels["START"] = False


# SET GAME CONSTANTS TO DEFAULT
def resetGameConstants():
    global savedConstants, obstacleSpeed, obstacleSize, maxObstacles, obstacleBoundaries, cloudSpeed
    obstacleSpeed = savedConstants["obstacleSpeed"]
    obstacleSize = savedConstants["obstacleSize"]
    maxObstacles = savedConstants["maxObstacles"]
    obstacleBoundaries = savedConstants["obstacleBoundaries"]
    cloudSpeed = savedConstants["cloudSpeed"]  


# LOAD GAME CONSTANTS
def gameConstantsSetter(stageList):
    returnList = []
    for stage in stageList:
        stageConstants = []
        for settings in stage:
            levelDict = {
                            "START" : settings[0], 
                            "TIME" : settings[1],
                            "bound" : settings[2],  
                            "speedMult" : settings[3],
                            "obsSizeMult" : settings[4],
                            "maxObsMult" : settings[5],                    
                }
                
            stageConstants.append(levelDict)
        returnList.append(stageConstants)
    return returnList   
    

# UPDATE GAME CONSTANTS
def levelUpdater(gameConstants,gameClock):
    global obstacleBoundaries,obstacleSpeed,obstacleColor,maxObstacles,obstacleSize,cloudSpeedMult,cloudSpeed,currentLevel,currentStage
    if currentStage < len(gameConstants):
        if gameConstants[currentStage][0]["TIME"] == gameClock and not gameConstants[currentStage][0]["START"]:
            gameConstants[currentStage][0]["START"] = True
            currentStage += 1
            currentLevel = 1
        
    for levelDict in gameConstants[currentStage-1]:
        if levelDict["TIME"] == gameClock:
            if not levelDict["START"]:
                levelDict["START"] = True
                obstacleBoundaries = levelDict["bound"]
                obstacleSpeed += levelDict["speedMult"]
                maxObstacles += levelDict["maxObsMult"]
                obstacleSize += levelDict["obsSizeMult"]
                cloudSpeed *= cloudSpeedMult
                currentLevel += 1


# SPAWN OBSTACLES
def spawner(sprites,obstacles,maxObstacles):
        if len(obstacles) < maxObstacles:
            obstacle = Obstacle()
            obstacles.add(obstacle)
            sprites.add(obstacle) 
            

# OBSTACLE MOVEMENT
def obstacleMove(obstacles):
    for obs in obstacles:
        position = obs.rect.center 
        if "N" in obs.direction: obs.rect.centery -= obs.speed    
        if "S" in obs.direction: obs.rect.centery += obs.speed      
        if "E" in obs.direction: obs.rect.centerx += obs.speed 
        if "W" in obs.direction: obs.rect.centerx -= obs.speed


# OFF SCREEN OBSTACLE REMOVAL
def obstacleRemove(obstacles):
    for obs in obstacles:
   
        if obs.rect.centerx > screenSize[0] or obs.rect.centerx < 0:
            obstacles.remove(obs)
            obs.kill()

        elif obs.rect.centery > screenSize[1] or obs.rect.centery < 0:
            obs.kill()
            obstacles.remove(obs)


# OBSTACLE BOUNCING
def bounceObstacle(obstacles):
    for obs in obstacles:
        direction = obs.direction
        if obs.rect.centery  > screenSize[1]: obs.direction = movementReverse(direction)    
        if obs.rect.centery < 0: obs.direction = movementReverse(direction) 
        if obs.rect.centerx > screenSize[0]: obs.direction = movementReverse(direction)   
        if obs.rect.centerx < 0: obs.direction = movementReverse(direction)
 
 
# OBSTACLE WRAPPING
def wrapObstacle(obstacles):
    for obs in obstacles:
        if obs.rect.centery  > screenSize[1]: obs.rect.centery = 0  
        if obs.rect.centery < 0: obs.rect.centery = screenSize[1]                      
        if obs.rect.centerx > screenSize[0]: obs.rect.centerx = 0      
        if obs.rect.centerx < 0: obs.rect.centerx = screenSize[0]


# HUD
def showHUD(gameClock,currentStage,currentLevel):
    
    # TIMER DISPLAY
    timerDisplay = timerFont.render(str(gameClock), True, timerColor)
    
    # STAGE DISPLAY
    stageNum = "Stage " + str(currentStage)
    stageFont = pygame.font.Font(gameFont, levelSize)
    stageDisplay = stageFont.render( str(stageNum), True, levelColor )
    stageRect = stageDisplay.get_rect(topleft = screen.get_rect().topleft)
    
    dashFont = pygame.font.SysFont(None, levelSize)
    dashDisplay = dashFont.render( "-", True, levelColor )
    dashRect = dashDisplay.get_rect()
    dashRect.center = (stageRect.right + dashRect.width, stageRect.centery + dashRect.height/5)

    # LEVEL DISPLAY
    levelNum = "Level " + str(currentLevel)
    levelFont = pygame.font.Font(gameFont, levelSize)
    levelDisplay = levelFont.render( str(levelNum), True, levelColor )
    levelRect = levelDisplay.get_rect() 
    levelRect.center = (stageRect.right + levelRect.width*0.65, stageRect.centery)

    timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright) 
    
    screen.blit(timerDisplay, timerRect)
    screen.blit(stageDisplay, stageRect)
    screen.blit(dashDisplay, dashRect)
    screen.blit(levelDisplay, levelRect)


# START MENU
def startMenu(player):
    global currentStage, mainMenu, savedShipNum
    
    icons = []
    for icon in range(maxIcons): icons.append(Icon())
 
    startFont = pygame.font.Font(gameFont, startSize)
    startDisplay = startFont.render("N  VIGAT  R", True, startColor)
    startRect = startDisplay.get_rect()
    startRect.center = (screenSize[0]/2,screenSize[1]/2)
    
    startHelpFont = pygame.font.Font(gameFont, helpSize)
    startHelpDisplay = startHelpFont.render("Press SPACE to start or ESCAPE to quit", True, helpColor)
    startHelpRect = startHelpDisplay.get_rect()
    startHelpRect.center = (screenSize[0]/2,screenSize[1]-screenSize[1]/3)
    
    leftRect = menuList[3].get_rect(center = (screenSize[0] * 0.2 , screenSize[1]/3) )
    rightRect = menuList[4].get_rect(center = (screenSize[0] * 0.8 , screenSize[1]/3) )
    
    bounceDelay = 5
    bounceCount = 0
    
    # SHIP UNLOCKS   
    unlockNumber = 0
    if savedOverallHighScore >= 300: unlockNumber = len(spaceShipList)
    elif savedOverallHighScore >= 270: unlockNumber = len(spaceShipList) - 1
    elif savedOverallHighScore >= 240: unlockNumber = len(spaceShipList) - 2
    elif savedOverallHighScore >= 210: unlockNumber = len(spaceShipList) - 3
    elif savedOverallHighScore >= 180: unlockNumber = len(spaceShipList) - 4
    elif savedOverallHighScore >= 150: unlockNumber = len(spaceShipList) - 5    
    elif savedOverallHighScore >= 120: unlockNumber = len(spaceShipList) - 6 
    elif savedOverallHighScore >= 90: unlockNumber = len(spaceShipList) - 7   
    elif savedOverallHighScore >= 60: unlockNumber = len(spaceShipList) - 8    
    elif savedOverallHighScore >= 30: unlockNumber = len(spaceShipList) - 9

    for imageNum in range(unlockNumber-1):
        player.nextSpaceShip()
    
    startOffset = 100
    startDelay = 1
    iconPosition, startDelayCounter = startOffset, 0
    
    if mainMenu:
        while True:
            
            if bounceCount >= bounceDelay: bounceCount = 0
            else: bounceCount +=1
                
            for event in pygame.event.get():
                # START
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    
                    savedShipNum = player.currentImageNum
                    
                    while iconPosition > 0:
                        
                        if startDelayCounter >= startDelay:  startDelayCounter = 0
                        else: startDelayCounter +=1
                             
                        # Start animation
                        screen.fill([0,0,0])
                        screen.blit(bgList[currentStage - 1][0],(0,0))
                        screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Current spaceship
                        
                        pygame.display.update()
                        
                        if startDelayCounter >= startDelay: iconPosition-=1
 
                    mainMenu = False    
                    return
                
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                    if unlockNumber > player.currentImageNum + 1: player.nextSpaceShip()
                    
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    player.lastSpaceShip()
                
                # CREDITS
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c: creditScreen()
                
                # QUIT
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
  
            screen.fill([0,0,0])
            screen.blit(bgList[currentStage - 1][0],(0,0))
            
            for icon in icons:
                if bounceCount == bounceDelay: icon.move()    
                icon.draw()
                    
            
            screen.blit(startDisplay,startRect)
            screen.blit(startHelpDisplay, startHelpRect)
            screen.blit(player.image, (player.rect.x,player.rect.y + startOffset)) # Current spaceship
            screen.blit(menuList[0],(-14 + startRect.left + menuList[0].get_width() - menuList[0].get_width()/8,screenSize[1]/2 - 42)) # "A" symbol
            screen.blit(menuList[1],(-42 + screenSize[0] - startRect.centerx + menuList[1].get_width() * 2,screenSize[1]/2 - 42)) # "O" symbol
            
            # UFO icons
            screen.blit(menuList[2],(screenSize[0]/2 - menuList[2].get_width()/2,screenSize[1]/8)) # Big icon
            screen.blit(menuList[3],leftRect) # Left UFO
            screen.blit(menuList[4],rightRect) # Right UFO
            
            pygame.display.update()


def pauseMenu(player,obstacles,currentStage,lastAngle,cloudPos,gameClock,currentLevel,pauseCount):
    
    playerBlit = rotateImage(player.image,player.rect,lastAngle)
    paused = True
    pausedFont = pygame.font.Font(gameFont, pausedSize)
    pausedDisplay = pausedFont.render("Paused", True, pausedColor)
    pausedRect = pausedDisplay.get_rect()
    pausedRect.center = (screenSize[0]/2, screenSize[1]/2)
    
    # REMAINING PAUSES
    pauseCountSize = 40
    pauseNum = str(pauseMax - pauseCount) + " Pauses Remaining"
    
    if pauseCount >= pauseMax:
        pauseNum = "Out of pauses"

    pauseCountFont = pygame.font.Font(gameFont,pauseCountSize)
    pauseDisplay = pauseCountFont.render( pauseNum , True, levelColor )
    pauseRect = pauseDisplay.get_rect() 
    pauseRect.center = (screenSize[0] * .5 , screenSize[1] -16)
    
    while paused:
        screen.fill(screenColor)
        screen.blit(bgList[currentStage-1][0],(0,0))
        showHUD(gameClock,currentStage,currentLevel)
        screen.blit(cloud,(0,cloudPos))
        screen.blit(playerBlit[0],playerBlit[1])
        obstacles.draw(screen) # Draw obstacles
        screen.blit(pauseDisplay, pauseRect)
        screen.blit(pausedDisplay,pausedRect)
        pygame.display.flip()
        for event in pygame.event.get():
            # EXIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE): paused = False
 

# GAME OVER SCREEN 
def gameOver(gameClock,running,player,obstacles):
    global attemptNumber, currentLevel, currentStage, savedTotalAttempts, mainMenu, savedOverallHighScore
    gameOver = True
    newHighScore = False
    
    if sessionHighScore > savedOverallHighScore:
        updatedHighScoreFile = open(overallHighScorePath,'w')
        updatedHighScoreFile.write(str(sessionHighScore))
        updatedHighScoreFile.close()
        savedOverallHighScore = sessionHighScore
        newHighScore = True

    savedTotalAttempts += 1
    statsSpacingY = screenSize[1]/16
    
    # "GAME OVER" text
    gameOverFont = pygame.font.Font(gameFont, gameOverSize)
    gameOverDisplay = gameOverFont.render("Game Over", True, gameOverColor)
    gameOverRect = gameOverDisplay.get_rect()
    gameOverRect.center = (screenSize[0]/2, screenSize[1]/3)
    
    # Stats display
    statLineFontSize = round(finalScoreSize * 0.75)
    statFont = pygame.font.Font(gameFont, statLineFontSize)
    exitFont = pygame.font.Font(gameFont, helpSize)
    
    # Text
    attemptLine = str(attemptNumber) + " attempts this session and " + str(savedTotalAttempts) + " attempts overall"
    survivedLine = " You survived for " + str(gameClock) + " seconds"
    levelLine = "Died at stage " + str(currentStage) + " level " + str(currentLevel)
    overallHighScoreLine = "Your high score is " + str(savedOverallHighScore) + " seconds"
    newHighScoreLine = "New high score " + str(sessionHighScore) + " seconds"
    
    # Display
    recordDisplay = statFont.render(overallHighScoreLine, True, finalScoreColor)
    attemptDisplay = statFont.render(attemptLine, True, finalScoreColor)
    survivedDisplay = statFont.render(survivedLine, True, finalScoreColor)
    levelDisplay = statFont.render(levelLine, True, finalScoreColor)
    newHighScoreDisplay = statFont.render(newHighScoreLine, True, finalScoreColor)
    exitDisplay = exitFont.render("Press SPACE to restart or ESCAPE to quit", True, helpColor)
    
    # Rects
    attemptRect = attemptDisplay.get_rect()
    survivedRect = survivedDisplay.get_rect()
    levelRect = levelDisplay.get_rect()
    recordRect = recordDisplay.get_rect()
    exitRect = exitDisplay.get_rect()
    
    # Rect position
    survivedRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 3)
    recordRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 4)
    levelRect.center = (screenSize[0]/2, screenSize[1]/3 +statsSpacingY * 5)
    attemptRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 6)
    exitRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 7)
    
    # Updated game records
    updatedAttemptFile = open(totalAttemptsPath,'w')
    updatedAttemptFile.write(str(savedTotalAttempts))
    updatedAttemptFile.close()
    updatedRecords = True
    
    while gameOver:
        
        # Background
        screen.fill(screenColor)
        screen.blit(bgList[currentStage - 1][0],(0,0))
        if newHighScore: screen.blit(newHighScoreDisplay,recordRect)   
        else: screen.blit(recordDisplay,recordRect)
        screen.blit(gameOverDisplay,gameOverRect)
        screen.blit(attemptDisplay,attemptRect)
        screen.blit(survivedDisplay,survivedRect)
        screen.blit(levelDisplay,levelRect)
        screen.blit(exitDisplay,exitRect)
        pygame.display.flip()
       
        for event in pygame.event.get():
            
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # CREDITS
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_c): creditScreen()
                
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB): 
                # SET DEFAULTS AND GO BACK TO MENU
                gameClock = 0
                currentLevel = 1
                currentStage = 1
                player.kill()
                killAllObjects(obstacles)
                resetAllLevels(gameConstants)
                attemptNumber += 1
                mainMenu = True
                main()
                
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                # SET DEFAULTS AND RESTART GAME
                gameClock = 0
                currentLevel = 1
                currentStage = 1
                player.kill()
                killAllObjects(obstacles)
                resetAllLevels(gameConstants)
                attemptNumber += 1
                running = True
                main()


def creditScreen():
    
    rollCredits = True 
    posX = screenSize[0]/2
    posY = screenSize[1]/2
    creditsFont = pygame.font.Font(gameFont, creditsFontSize)
    
    createdByLine = "Created by Mike Pistolesi"
    creditsLine = "Art by Collin Guetta"
    
    createdByDisplay = creditsFont.render(createdByLine, True, creditsColor)
    creditsDisplay = creditsFont.render(creditsLine, True, creditsColor)
    
    creditsRect = creditsDisplay.get_rect()
    createdByRect = createdByDisplay.get_rect()
    
    creditsRect.center = (posX,posY)
    createdByRect.center = (posX, posY - screenSize[1]/15) 
    
    bounceCount = 0
    direction = randomEightDirection()
    
    while rollCredits:
        
        for event in pygame.event.get():
            # EXIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # RETURN TO GAME
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_c or event.key == pygame.K_SPACE):
                #screen.fill(screenColor)
                rollCredits = False
        
        screen.fill(screenColor)
        screen.blit(bgList[currentStage - 1][0],(0,0))
        screen.blit(createdByDisplay,createdByRect)
        screen.blit(creditsDisplay,creditsRect)
        pygame.display.flip()

        # BOUNCE OFF EDGES
        if createdByRect.right > screenSize[0]: direction = rightDir[random.randint(0, len(rightDir) - 1)]
        if createdByRect.left < 0: direction = leftDir[random.randint(0, len(leftDir) - 1)]  
        if creditsRect.bottom > screenSize[1]: direction = bottomDir[random.randint(0, len(bottomDir) - 1)]
        if createdByRect.top < 0 : direction = topDir[random.randint(0, len(topDir) - 1)]

        if bounceCount == 0:
            if "N" in direction:
                creditsRect.centery-= 1
                createdByRect.centery-= 1
                
            if "S" in direction: 
                creditsRect.centery+= 1
                createdByRect.centery+= 1
                
            if "E" in direction:
                creditsRect.centerx+= 1
                createdByRect.centerx+= 1
                
            if "W" in direction:
                creditsRect.centerx-= 1
                createdByRect.centerx-= 1

        bounceCount +=1
        if bounceCount >= 10: bounceCount = 0


gameConstants = gameConstantsSetter(stageList)
attemptNumber = 1
sessionHighScore = 0

clk = pygame.time.Clock()

def main():
    
    resetGameConstants()
    global attemptNumber,sessionHighScore,currentStage,mainMenu,savedShipNum
    pauseCount = 0

    player = Player()    
    if mainMenu: startMenu(player)
    else:
        for i in range(savedShipNum):
            player.nextSpaceShip()
    
    obstacles = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    sprites.add(player)
    gameClock = 0
    
    timerEvent = pygame.USEREVENT + 1
    pygame.time.set_timer(timerEvent, timerDelay) 
    
    cloudPos = cloudStart
    lastAngle = 0
    
    running = True
    
    # GAME LOOP
    while running:
        
        for event in pygame.event.get():
            
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                break
            
            # INCREMENT TIMER
            elif event.type == timerEvent:
                gameClock +=1
            
            # PAUSE GAME
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and pauseCount < pauseMax :
                pauseCount += 1
                pauseMenu(player,obstacles,currentStage,lastAngle,cloudPos,gameClock,currentLevel,pauseCount)

        # BACKGROUND ANIMATION
        screen.blit(bgList[currentStage - 1][0], (0,0) )
        screen.blit(bgList[currentStage - 1][1], (0,cloudPos) )
        if cloudPos < screenSize[1]: cloudPos += cloudSpeed  
        else: cloudPos = cloudStart 
        
        # HUD
        showHUD(gameClock,currentStage,currentLevel)
        
        # COLLISION DETECTION
        if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask): gameOver(gameClock,running,player,obstacles)
        
        # DRAW AND MOVE SPRITES
        player.movement()
        player.wrapping()
        spawner(sprites,obstacles,maxObstacles)
        obstacleMove(obstacles)

        # UPDATE HIGH SCORE
        if gameClock > sessionHighScore: sessionHighScore = gameClock
        
        # OBSTACLE HANDLING
        if obstacleBoundaries == "KILL": obstacleRemove(obstacles)
        if obstacleBoundaries == "BOUNCE": bounceObstacle(obstacles)
        if obstacleBoundaries == "WRAP": wrapObstacle(obstacles)
        
        # LEVEL UP 
        levelUpdater(gameConstants,gameClock)   
        
        # DRAW SPRITES
        newBlit = rotateImage(player.image,player.rect,player.angle) # Player rotation
        screen.blit(newBlit[0],newBlit[1]) # Draw player
        
        # DRAW OBSTACLES
        for obs in obstacles:
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1])
            obs.angle += (currentLevel * currentStage * obs.spinDirection) # Update angle 
        
        # UPDATE SCREEN
        lastAngle = player.angle
        player.angle = 0 # Reset player orientation
        pygame.display.flip()
        clk.tick(fps)

if __name__ == '__main__': main()
    
    
    
    


