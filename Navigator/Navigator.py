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
cloudSpeed = 1
cloudStart = -1000
cloudSpeedMult = 1.5
startSize = 150
startColor = [0,255,0]
gameOverColor = [255,0,0]
gameOverSize = 100
helpSize = 30
helpColor = [0,255,0]
finalScoreSize = 35
finalScoreColor = [0,255,0]

# PLAYER
playerSize = 10 # Default = 10            
playerSpeed = 5 # Default = 5

# OBSTACLES
obstacleSpeed = 4  # Default = 4           
obstacleSize = 30    # Default = 30
maxObstacles = 12  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" (Can be updated by level)

# LEVELS:   [ False , TIME, BOUNDS, SPEED, SIZE, NUMBER ] , then add to levelSettingsList
levelTwo = [ False, 15, "KILL", 1, 1, 1.5 ] 
levelThree = [ False, 30, "KILL", 1, 1.5, 1 ] 
levelFour = [ False, 45, "KILL", 1, 1.5, 1 ] 
levelFive = [ False, 60, "KILL", 1.25, 1, 1 ] 
levelSix = [ False, 75, "WRAP", 1, 1.5, 1 ] 
levelSeven = [ False, 90, "KILL", 1, 1, 10 ] 
levelEight = [ False, 105, "BOUNCE", 1.25, 1.25, 1.0 ] 
levelNine = [ False, 120, "KILL", 1.1, 1.1, 1.1 ]
levelTen = [ False, 135, "WRAP", 1.1, 1.1, 1.1 ] 
overTime = [ False, 150, "KILL", 1.1, 1.1, 1.1 ] 
levelSettingsList = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen,overTime]
#---------------------------------------------------------------------------------------------------------------------------------

savedConstants = {
                "obstacleSpeed" : obstacleSpeed, 
                "obstacleSize" : obstacleSize, 
                "maxObstacles" : maxObstacles, 
                "obstacleBoundaries" : obstacleBoundaries,
                "cloudSpeed" : cloudSpeed
                }
                
currentLevel = 1
mainMenu = True
screen = pygame.display.set_mode(screenSize)

# ASSETS
curDir = str(os.getcwd())

# METEORS
mDir = os.path.join(curDir, 'Meteors')
meteorDict = {}
meteorList = []

for filename in os.listdir(mDir):
    if filename.endswith('.png'):
        path = os.path.join(mDir, filename)
        key = filename[:-4]
        meteorDict[key] = pygame.image.load(path).convert_alpha()
        meteorList.append(meteorDict[key])

# BACKGROUND
bg = pygame.image.load('Background.png').convert_alpha()
cloud = pygame.image.load('Cloud.png').convert_alpha()

class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__() 
            self.size = playerSize        
            self.speed = playerSpeed
            self.image = pygame.image.load('spaceShip.png').convert_alpha()
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.angle = 0
        
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
 
        def wrapping(self):
            if self.rect.centery  > screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = screenSize[1]
            if self.rect.centerx > screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = screenSize[0]
                
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
        
def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect
    
def movementReverse(direction):
        if direction == "N": return "S"           
        elif direction == "S": return "N"                     
        elif direction == "E": return "W"           
        elif direction == "W": return "E"          
        elif direction == "NW": return "SE"         
        elif direction == "NE": return "SW"          
        elif direction == "SE": return "NW"
        elif direction == "SW": return "NE"
              
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

def killAllObjects(obstacles):
    for obstacle in obstacles:
        obstacle.kill()
        
def resetAllLevels(levelDictList):
    for levelDict in levelDictList:
        levelDict["START"] = False
        
def resetGameConstants():
    global savedConstants, obstacleSpeed, obstacleSize, maxObstacles, obstacleBoundaries, cloudSpeed
    obstacleSpeed = savedConstants["obstacleSpeed"]
    obstacleSize = savedConstants["obstacleSize"]
    maxObstacles = savedConstants["maxObstacles"]
    obstacleBoundaries = savedConstants["obstacleBoundaries"]
    cloudSpeed = savedConstants["cloudSpeed"]  

def levelDictSetter():
    global levelSettingsList
    levelDictList = []
    for settings in levelSettingsList:
        levelDict = {
                        "START" : settings[0], 
                        "TIME" : settings[1],
                        "bound" : settings[2],  
                        "speedMult" : settings[3],
                        "obsSizeMult" : settings[4],
                        "maxObsMult" : settings[5],                    
                    }              
        levelDictList.append(levelDict)   
    return levelDictList   
    
def levelUpdater(levelDictList,gameClock):
    global obstacleBoundaries, obstacleSpeed, obstacleColor, maxObstacles, obstacleSize, cloudSpeedMult,cloudSpeed, currentLevel

    for levelDict in levelDictList:
        if levelDict["TIME"] == gameClock:
           if not levelDict["START"]:
                levelDict["START"] = True
                obstacleBoundaries = levelDict["bound"]
                obstacleSpeed *= levelDict["speedMult"]
                maxObstacles *= levelDict["maxObsMult"]
                obstacleSize *= levelDict["obsSizeMult"]
                cloudSpeed *= cloudSpeedMult
                currentLevel += 1 
            
def spawner(sprites,obstacles,maxObstacles):
        if len(obstacles) < maxObstacles:
            obstacle = Obstacle()
            obstacles.add(obstacle)
            sprites.add(obstacle) 
            
def obstacleMove(obstacles):
    for obs in obstacles:
        position = obs.rect.center 
        if "N" in obs.direction: obs.rect.centery -= obs.speed    
        if "S" in obs.direction: obs.rect.centery += obs.speed      
        if "E" in obs.direction: obs.rect.centerx += obs.speed 
        if "W" in obs.direction: obs.rect.centerx -= obs.speed
         
def obstacleRemove(obstacles):
    for obs in obstacles:
   
        if obs.rect.centerx > screenSize[0] or obs.rect.centerx < 0:
            obstacles.remove(obs)
            obs.kill()

        elif obs.rect.centery > screenSize[1] or obs.rect.centery < 0:
            obs.kill()
            obstacles.remove(obs)
            
def bounceObstacle(obstacles):
    for obs in obstacles:
        direction = obs.direction
        if obs.rect.centery  > screenSize[1]: obs.direction = movementReverse(direction)    
        if obs.rect.centery < 0: obs.direction = movementReverse(direction) 
        if obs.rect.centerx > screenSize[0]: obs.direction = movementReverse(direction)   
        if obs.rect.centerx < 0: obs.direction = movementReverse(direction)
           
def wrapObstacle(obstacles):
    for obs in obstacles:
        if obs.rect.centery  > screenSize[1]: obs.rect.centery = 0  
        if obs.rect.centery < 0: obs.rect.centery = screenSize[1]                      
        if obs.rect.centerx > screenSize[0]: obs.rect.centerx = 0      
        if obs.rect.centerx < 0: obs.rect.centerx = screenSize[0]

def startMenu():
    global mainMenu
    if mainMenu:
        while True:
            
            startFont = pygame.font.Font('8bitFont.ttf', startSize)
            startDisplay = startFont.render("NAVIGATOR", True, startColor)
            startRect = startDisplay.get_rect(center = screen.get_rect().center)
            
            startHelpFont = pygame.font.Font('8bitFont.ttf', helpSize)
            startHelpDisplay = startHelpFont.render("Press SPACE to start or ESCAPE to quit", True, helpColor)
            startHelpRect = startHelpDisplay.get_rect()
            startHelpRect.center = (screenSize[0]/2,screenSize[1]-screenSize[1]/3)
            
            for event in pygame.event.get():
                # START
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    mainMenu = False
                    return
                
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
                else:
                    screen.fill([0,0,0])
                    screen.blit(bg,(0,0))
                    screen.blit(startDisplay,startRect)
                    screen.blit(startHelpDisplay, startHelpRect)
                    pygame.display.update()
           
def gameOver(gameClock,running,player,obstacles):
    global attemptNumber,currentLevel
    gameOver = True
    
    while gameOver:
        
        gameOverFont = pygame.font.Font('8bitFont.ttf', gameOverSize)
        gameOverDisplay = gameOverFont.render("Game Over", True, gameOverColor)
        gameOverRect = gameOverDisplay.get_rect(center = screen.get_rect().center)
        
        exitFont = pygame.font.Font('8bitFont.ttf', helpSize)
        exitDisplay = exitFont.render("Press SPACE to restart or ESCAPE to quit", True, helpColor)
        exitRect = exitDisplay.get_rect()
        exitRect.center = (screenSize[0]/2, screenSize[1] - screenSize[1]/6)
        
        statLineFontSize = round(finalScoreSize * 0.75)
        statLine = "Attempt " + str(attemptNumber) + " You survived for " + str(gameClock) + " seconds and died at level " + str(currentLevel)
        statFont = pygame.font.Font('8bitFont.ttf', statLineFontSize)
        statDisplay = statFont.render(statLine, True, finalScoreColor)
        statRect = statDisplay.get_rect()
        statRect.center = (screenSize[0]/2, screenSize[1] - screenSize[1]/3)
        
        screen.blit(bg,(0,0))
        screen.blit(gameOverDisplay,gameOverRect)
        screen.blit(exitDisplay,exitRect)
        screen.blit(statDisplay,statRect)
        pygame.display.flip()
        for event in pygame.event.get():
            
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = True
                
                # SET DEFAULTS AND RESTART GAME
                gameClock = 0
                currentLevel = 1
                player.kill()
                killAllObjects(obstacles)
                resetAllLevels(levelDictList)
                attemptNumber += 1
                main()
    
levelDictList = levelDictSetter()
attemptNumber = 1
clk = pygame.time.Clock()



def main():
    resetGameConstants()
    global attemptNumber
    global mainMenu
    
    if mainMenu:
        startMenu()
        
    player = Player()
    obstacles = pygame.sprite.Group()
    sprites = pygame.sprite.Group()
    sprites.add(player)
    gameClock = 0
    
    # TIMER DISPLAY
    timerFont = pygame.font.Font('8bitFont.ttf', timerSize)
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
        screen.blit(bg,(0,0))
        if cloudPos < screenSize[1]: cloudPos += cloudSpeed  
        else: cloudPos = cloudStart      
        screen.blit(cloud,(0,cloudPos))
        
        # LEVEL DISPLAY
        levelNum = "Level " + str(currentLevel)
        levelFont = pygame.font.Font('8bitFont.ttf', levelSize)
        levelDisplay = levelFont.render( str(levelNum), True, levelColor )
        
        # COLLISION DETECTION
        if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask):
            gameOver(gameClock,running,player,obstacles)
                    
        player.movement()
        player.wrapping()
        spawner(sprites,obstacles,maxObstacles)
        obstacleMove(obstacles)
        
        if obstacleBoundaries == "KILL": obstacleRemove(obstacles)
        if obstacleBoundaries == "BOUNCE": bounceObstacle(obstacles)
        if obstacleBoundaries == "WRAP": wrapObstacle(obstacles)
               
        levelUpdater(levelDictList,gameClock)        
        
        newBlit = rot_center(player.image,player.rect,player.angle)
        screen.blit(newBlit[0],newBlit[1])
        obstacles.draw(screen) # Draws all sprites
        
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright)
        levelRect = levelDisplay.get_rect(topleft = screen.get_rect().topleft)
        
        screen.blit(timerDisplay, timerRect)
        screen.blit(levelDisplay, levelRect)
        player.angle = 0
        pygame.display.flip()
        screen.fill(screenColor)
        clk.tick(fps)
        
    
if __name__ == '__main__': main()
    
    
    
    



