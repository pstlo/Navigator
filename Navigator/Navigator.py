# NAVIGATOR

import random
import math
import sys
import os
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
pygame.init()
pygame.mouse.set_visible(False)

# GAME CONSTANTS
#------------------------------------------------------------------------------------------------------------------

# SCREEN                                                                                                                            
screenSize = [800,800] # Default = [800,800]                                  
screenColor = [0,0,0] # Default = [0,0,0]                                                                
fps = 60 # Default = 60                                    
timerSize = 75 # Default = 100                             
timerColor = [255,255,255] # Default = [255,255,255] 
timerDelay = 1000 # Default = 1000
levelSize = 50 # Default = 50                                                                                                                                                                   
levelColor = [255,255,255] # Default = [255,255,255]                                                                                                                                            
cloudSpeed = 1 # Default = 1
cloudStart = -1000 # Default = -1000
cloudSpeedMult = 1.5 # Default = 1.5
startSize = 150 # Default = 150
startColor = [0,255,0] # Default = [0,255,0]
gameOverColor = [255,0,0] # Default = [255,0,0]
gameOverSize = 100 # Default = 100
helpSize = 30 # Default = 30 
helpColor = [0,255,0] # Default = [0,255,0]
finalScoreSize = 35 # Default = 35
finalScoreColor = [0,255,0] # Default = [0,255,0]
creditsFontSize = 55
creditsColor = [255,255,255]

# PLAYER           
playerSpeed = 5 # Default = 5

# OBSTACLES
obstacleSpeed = 4  # Default = 4           
obstacleSize = 30    # Default = 30
maxObstacles = 12  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" (Can be updated by level)

# LEVELS  
levelTimer = 15 # Default = 15 / Time between levels

speedIncrement = 0.3 # Default = 0.3
sizeIncrement = 4 # Default = 4
numIncrement = 3 # Default = 3

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
overTime = [ False, 10 * levelTimer, "KILL", speedIncrement, sizeIncrement, numIncrement ]

# DIVIDE INTO STAGES
stageOneLevels = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen,overTime] # Stage 1
overTimeLevels = [overTime]

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
screen = pygame.display.set_mode(screenSize)

# ASSET LOADING
baseDir = str(os.getcwd()) # Game directory
curDir = os.path.join(baseDir, 'Assets') # Asset directory
mDir = os.path.join(curDir, 'Meteors') # Meteor asset directory
sDir = os.path.join(curDir, 'Spaceships') # Spaceship asset directory
bDir = os.path.join(curDir, 'Backgrounds') # Background asset directory

# FONT
gameFont = ''
for filename in os.listdir(curDir):
    if filename.endswith('.ttf'):
        path = os.path.join(curDir, filename)
        gameFont = path
        break
            
# METEOR ASSETS
meteorDict = {}
meteorList = []
for filename in os.listdir(mDir):
    if filename.endswith('.png'):
        path = os.path.join(mDir, filename)
        key = filename[:-4]
        meteorDict[key] = pygame.image.load(path).convert_alpha()
        meteorList.append(meteorDict[key])

# BACKGROUND ASSETS
bgList = []
for filename in os.listdir(bDir):
    bgPath = os.path.join(bDir,filename)
    for nextBg in os.listdir(bgPath):
        
        stageBgPath = os.path.join(bgPath,'Background.png')
        stageCloudPath = os.path.join(bgPath,'Cloud.png')

        bg = pygame.image.load(stageBgPath).convert_alpha()
        cloud = pygame.image.load(stageCloudPath).convert_alpha()
        
        bgList.append([bg,cloud])

# SPACESHIP ASSETS
spaceShipList = []
for filename in os.listdir(sDir):
    if filename.endswith('.png'):
        path = os.path.join(sDir, filename)
        spaceShipList.append(pygame.image.load(path).convert_alpha())
        

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
            self.image = spaceShipList[self.currentImageNum + 1]
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            
                
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = obstacleSpeed
        self.size = obstacleSize
        self.movement = getMovement()
        self.direction = self.movement[1]
        try:
            self.image = meteorList[currentLevel - 1].convert_alpha()
        except:
            self.image = meteorList[random.randint(0,len(meteorList)-1)]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        

# ROTATE IMAGE
def rotateImage(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    rotatedRect = rotated.get_rect(center=rect.center)
    return rotated,rotatedRect
    

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
              

# OBSTACLE POSITION GENERATION
def getMovement():
        X = random.randint(0, screenSize[0])
        Y = random.randint(0, screenSize[1])

        lowerX = random.randint(0, screenSize[0] * 0.05)
        upperX =  random.randint(screenSize[0] * 0.95, screenSize[0])
        lowerY  = random.randint(0, screenSize[1] * 0.05)
        upperY = random.randint(screenSize[1] * 0.95, screenSize[1])
        
        topDir = ["S", "E", "W", "SE", "SW"]
        leftDir = ["E", "S", "N", "NE", "SE"]
        bottomDir = ["N", "W", "E", "NE", "NW"]
        rightDir = ["W", "N", "S", "NW", "SW"]
        
        topDirection = topDir[random.randint(0, len(topDir) - 1)]
        leftDirection = leftDir[random.randint(0, len(leftDir) - 1)]
        bottomDirection = bottomDir[random.randint(0, len(bottomDir) - 1)]
        rightDirection = rightDir[random.randint(0, len(rightDir) - 1)]
        
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
    
    if currentStage <= len(gameConstants) - 1:
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


# START MENU
def startMenu():
    global mainMenu,currentStage
    if mainMenu:
        while True:
            
            startFont = pygame.font.Font(gameFont, startSize)
            startDisplay = startFont.render("NAVIGATOR", True, startColor)
            startRect = startDisplay.get_rect(center = screen.get_rect().center)
            
            startHelpFont = pygame.font.Font(gameFont, helpSize)
            startHelpDisplay = startHelpFont.render("Press SPACE to start or ESCAPE to quit", True, helpColor)
            startHelpRect = startHelpDisplay.get_rect()
            startHelpRect.center = (screenSize[0]/2,screenSize[1]-screenSize[1]/3)
            
            for event in pygame.event.get():
                # START
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    mainMenu = False
                    return
                
                # CREDITS
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    creditScreen()
                
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
                else:
                    screen.fill([0,0,0])
                    screen.blit(bgList[currentStage - 1][0],(0,0))
                    screen.blit(startDisplay,startRect)
                    screen.blit(startHelpDisplay, startHelpRect)
                    pygame.display.update()
 

# GAME OVER SCREEN 
def gameOver(gameClock,running,player,obstacles):
    global attemptNumber, currentLevel, currentStage
    gameOver = True
    
    while gameOver:
        
        # "GAME OVER" text
        gameOverFont = pygame.font.Font(gameFont, gameOverSize)
        gameOverDisplay = gameOverFont.render("Game Over", True, gameOverColor)
        gameOverRect = gameOverDisplay.get_rect(center = screen.get_rect().center)
        
        exitFont = pygame.font.Font(gameFont, helpSize)
        exitDisplay = exitFont.render("Press SPACE to restart or ESCAPE to quit", True, helpColor)
        exitRect = exitDisplay.get_rect()
        exitRect.center = (screenSize[0]/2, screenSize[1] - screenSize[1]/6)
        
        # Stats display
        statLineFontSize = round(finalScoreSize * 0.75)
        statLine = "Attempt " + str(attemptNumber) + " You survived for " + str(gameClock) + " seconds and died at level " + str(currentLevel)
        statFont = pygame.font.Font(gameFont, statLineFontSize)
        statDisplay = statFont.render(statLine, True, finalScoreColor)
        statRect = statDisplay.get_rect()
        statRect.center = (screenSize[0]/2, screenSize[1] - screenSize[1]/3)
        
        # Background
        screen.blit(bgList[currentStage - 1][0],(0,0))
        screen.blit(gameOverDisplay,gameOverRect)
        screen.blit(exitDisplay,exitRect)
        screen.blit(statDisplay,statRect)
        pygame.display.flip()
       
        for event in pygame.event.get():
            
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                creditScreen()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = True
                
                # SET DEFAULTS AND RESTART GAME
                gameClock = 0
                currentLevel = 1
                currentStage = 1
                player.kill()
                killAllObjects(obstacles)
                resetAllLevels(gameConstants)
                attemptNumber += 1
                main()
                

def creditScreen():
    
    rollCredits = True 
    posX = screenSize[0]/2
    posY = screenSize[1]/2
    creditsFont = pygame.font.Font(gameFont, creditsFontSize)
    
    createdByLine = "Created by Mike Pistolesi"
    creditsLine = "visuals by Collin Guetta"
    
    createdByDisplay = creditsFont.render(createdByLine, True, creditsColor)
    creditsDisplay = creditsFont.render(creditsLine, True, creditsColor)
    
    creditsRect = creditsDisplay.get_rect()
    createdByRect = createdByDisplay.get_rect()
    
    creditsRect.center = (posX,posY)
    createdByRect.center = (posX, posY - screenSize[1]/15) 
    
    bounceCount = 0
    
    directions = ["N","S","E","W","NW","SW","NE","SE"]
    direction = directions[random.randint(0, len(directions)-1)]
    
    topDir = ["S", "E", "W", "SE", "SW"]
    leftDir = ["E", "S", "N", "NE", "SE"]
    bottomDir = ["N", "W", "E", "NE", "NW"]
    rightDir = ["W", "N", "S", "NW", "SW"]
    
    while rollCredits:
        
        for event in pygame.event.get():
            # EXIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # RETURN TO GAME
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_c or event.key == pygame.K_SPACE): 
                rollCredits = False
                
        screen.blit(bgList[currentStage - 1][0],(0,0))
        screen.blit(createdByDisplay,createdByRect)
        screen.blit(creditsDisplay,creditsRect)
        pygame.display.flip()

        # BOUNCE OFF EDGES
        if creditsRect.right > screenSize[0]: direction = rightDir[random.randint(0, len(rightDir) - 1)]
        if creditsRect.left < 0: direction = leftDir[random.randint(0, len(leftDir) - 1)]  
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
clk = pygame.time.Clock()


def main():
    resetGameConstants()
    global attemptNumber
    global mainMenu
    global currentStage
    
    if mainMenu:
        startMenu()
        
    player = Player()
    obstacles = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    sprites.add(player)
    gameClock = 0
    
    # TIMER DISPLAY
    timerFont = pygame.font.Font(gameFont, timerSize)
    timerDisplay = timerFont.render(str(gameClock), True, timerColor)
    timerEvent = pygame.USEREVENT + 1
    pygame.time.set_timer(timerEvent, timerDelay) 
 
    cloudPos = cloudStart
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
            
            elif event.type == timerEvent:
                gameClock +=1
                timerDisplay = timerFont.render(str(gameClock), True, (255,255,255))
        
        # BACKGROUND ANIMATION
        screen.blit(bgList[currentStage - 1][0], (0,0) )
        screen.blit(bgList[currentStage - 1][1], (0,cloudPos) )
            
        if cloudPos < screenSize[1]: cloudPos += cloudSpeed  
        else: cloudPos = cloudStart 
            
        # STAGE DISPLAY
        stageNum = "Stage " + str(currentStage)
        stageFont = pygame.font.Font(gameFont, levelSize)
        stageDisplay = stageFont.render( str(stageNum), True, levelColor )
        
        dashFont = pygame.font.SysFont(None, levelSize)
        dashDisplay = dashFont.render( "-", True, levelColor )
            
        # LEVEL DISPLAY
        levelNum = "Level " + str(currentLevel)
        levelFont = pygame.font.Font(gameFont, levelSize)
        levelDisplay = levelFont.render( str(levelNum), True, levelColor )
        
        # COLLISION DETECTION
        if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask):
            gameOver(gameClock,running,player,obstacles)
            
                    
        player.movement()
        player.wrapping()
        spawner(sprites,obstacles,maxObstacles)
        obstacleMove(obstacles)
        
        # OBSTACLE HANDLING
        if obstacleBoundaries == "KILL": obstacleRemove(obstacles)
        if obstacleBoundaries == "BOUNCE": bounceObstacle(obstacles)
        if obstacleBoundaries == "WRAP": wrapObstacle(obstacles)
               
        levelUpdater(gameConstants,gameClock)       
        
        # DRAW SPRITES
        newBlit = rotateImage(player.image,player.rect,player.angle) # Player rotation
        screen.blit(newBlit[0],newBlit[1]) # Draw player
        obstacles.draw(screen) # Draw obstacles
        
        # HUD
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright) 
        stageRect = stageDisplay.get_rect(topleft = screen.get_rect().topleft)
        dashRect = dashDisplay.get_rect()
        levelRect = levelDisplay.get_rect() 
        
        dashRect.center = (stageRect.right + dashRect.width, stageRect.centery + dashRect.height/5)
        levelRect.center = (stageRect.right + levelRect.width*0.65, stageRect.centery)
        
        screen.blit(timerDisplay, timerRect)
        screen.blit(stageDisplay, stageRect)
        screen.blit(dashDisplay, dashRect)
        screen.blit(levelDisplay, levelRect)
        
        # UPDATE SCREEN
        player.angle = 0 # Reset player orientation
        pygame.display.flip()
        screen.fill(screenColor)
        clk.tick(fps)
        
if __name__ == '__main__': main()
    
    
    
    



