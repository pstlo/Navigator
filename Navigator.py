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

# PLAYER
playerSize = 10 # Default = 10            
playerSpeed = 5 # Default = 5

# OBSTACLES
obstacleSpeed = 3  # Default = 3           
obstacleSize = 30    # Default = 30
maxObstacles = 12  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" (Can be updated by level)

# LEVELS:   [ False , TIME, BOUNDS, SPEED, SIZE, NUMBER ] , then add to levelSettingsList
levelTwo = [ False, 15, "KILL", 1, 1, 1.5 ] 
levelThree = [ False, 30, "KILL", 1, 1.5, 1 ] 
levelFour = [ False, 45, "KILL", 1, 1.5, 1 ] 
levelFive = [ False, 60, "KILL", 1.25, 1, 1 ] 
levelSix = [ False, 75, "WRAP", 0.5, 10, 0.1 ] 
levelSeven = [ False, 90, "KILL", 2, 0.1, 10 ] 
levelEight = [ False, 105, "BOUNCE", 1.25, 1.25, 1.0 ] 
levelNine = [ False, 120, "KILL", 1.25, 1.25, 1.25 ]
levelTen = [ False, 135, "WRAP", 1, 1, 1 ] 
overTime = [ False, 150, "KILL", 1.1, 1.1, 1.1 ] 
levelSettingsList = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen,overTime]
#---------------------------------------------------------------------------------------------------------------------------------

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

currentLevel = 1    

player = Player()

obstacles = pygame.sprite.Group()
sprites = pygame.sprite.Group()
sprites.add(player)

clk = pygame.time.Clock()

gameClock = 0        
        
def levelDictSetter(levelSettingsList):
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

levelDictList = levelDictSetter(levelSettingsList)


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
 
def movementReverse(direction):
        if direction == "N":
            return "S"
        elif direction == "S":
            return "N"          
        elif direction == "E":
            return "W"
        elif direction == "W":
            return "E"
        elif direction == "NW":
            return "SE"
        elif direction == "NE":
            return "SW"
        elif direction == "SE":
            return "NW"
        elif direction == "SW":
            return "NE"     
              
def main():
    
    global gameClock
    
    # TIMER DISPLAY
    timerFont = pygame.font.SysFont(None, timerSize)
    timerDisplay = timerFont.render(str(gameClock), True, timerColor)
    timerEvent = pygame.USEREVENT + 1
    pygame.time.set_timer(timerEvent, timerDelay)
    
    running = True

    def levelDictSelector(levelDictList):
            for levelDict in levelDictList:
                if levelDict["TIME"] == gameClock:
                    return levelDict
                else:
                    continue

    
    def levelUpdater(levelDict):   # PASS THE CORRESPONDING DICT TO THIS FUNCTION
        global obstacleBoundaries, obstacleSpeed, obstacleColor, maxObstacles, obstacleSize, currentLevel
    
        try:
            if not levelDict["START"] and levelDict["TIME"] == gameClock:
                    levelDict["START"] = True
                    obstacleBoundaries = levelDict["bound"]
                    obstacleSpeed *= levelDict["speedMult"]
                    maxObstacles *= levelDict["maxObsMult"]
                    obstacleSize *= levelDict["obsSizeMult"]
                    currentLevel += 1
                    cloudSpeed *= cloudSpeedMult            
        except:
            pass


    def movement():
        
        key = pygame.key.get_pressed()
        
        if key[pygame.K_w] or key[pygame.K_UP]:
            player.rect.centery -= player.speed
            
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            player.rect.centery += player.speed
            
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            player.rect.centerx -= player.speed 
            
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            player.rect.centerx += player.speed
        
    def wrapping():
        if player.rect.centery  > screenSize[1]:
            player.rect.centery = 0
        
        if player.rect.centery < 0:
            player.rect.centery = screenSize[1]
        
        if player.rect.centerx > screenSize[0]:
            player.rect.centerx = 0

        if player.rect.centerx < 0:
            player.rect.centerx = screenSize[0]
    
    def spawner():
        if len(obstacles) < maxObstacles:
            obstacle = Obstacle()
            obstacles.add(obstacle)
            sprites.add(obstacle)
         
   
    def obstacleMove():
        for obs in obstacles:
            position = obs.rect.center
            
            if "N" in obs.direction:
                obs.rect.centery -= obs.speed
                
            if "S" in obs.direction:
                obs.rect.centery += obs.speed
                
            if "E" in obs.direction:
                obs.rect.centerx += obs.speed
                
            if "W" in obs.direction:
                obs.rect.centerx -= obs.speed
   
                
    def obstacleRemove():
        for obs in obstacles:
            position = obs.rect.center
            
            if obs.rect.centerx > screenSize[0] or obs.rect.centerx < 0:
                obstacles.remove(obs)
                obs.kill()

            elif obs.rect.centery > screenSize[1] or obs.rect.centery < 0:
                obs.kill()
                obstacles.remove(obs)
                
    def bounceObstacle():
        for obs in obstacles:
            direction = obs.direction
            
            if obs.rect.centery  > screenSize[1]:
                obs.direction = movementReverse(direction) 
                
            if obs.rect.centery < 0:
                obs.direction = movementReverse(direction)
                
            if obs.rect.centerx > screenSize[0]:
                obs.direction = movementReverse(direction) 
                
            if obs.rect.centerx < 0:
                obs.direction = movementReverse(direction)
                

    def wrapObstacle():
        for obs in obstacles:
            
            if obs.rect.centery  > screenSize[1]:
                obs.rect.centery = 0  
                
            if obs.rect.centery < 0:
                obs.rect.centery = screenSize[1]    
                
            if obs.rect.centerx > screenSize[0]:
                obs.rect.centerx = 0        
                
            if obs.rect.centerx < 0:
                obs.rect.centerx = screenSize[0]
    
    cloudPos = cloudStart
    # GAME LOOP
    while running:
        
        for event in pygame.event.get():
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
            
            elif event.type == timerEvent:
                gameClock +=1
                timerDisplay = timerFont.render(str(gameClock), True, (255,255,255))
        
        # BACKGROUND ANIMATION
        screen.blit(bg,(0,0))
        
        if cloudPos < screenSize[1]:
            cloudPos += cloudSpeed
        else:
            cloudPos = cloudStart
            
        screen.blit(cloud,(0,cloudPos))
        
        # LEVEL DISPLAY
        levelNum = "Level " + str(currentLevel)
        levelFont = pygame.font.SysFont(None, levelSize)
        levelDisplay = levelFont.render( str(levelNum), True, levelColor )
        
        # COLLISION DETECTION
        if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask):
            running = False
                    
        movement()
        wrapping()
        spawner()
        obstacleMove()
        
        if obstacleBoundaries == "KILL":
            obstacleRemove()
        
        if obstacleBoundaries == "BOUNCE":
            bounceObstacle()
        
        if obstacleBoundaries == "WRAP":
            wrapObstacle()
            
        levelDict = levelDictSelector(levelDictList)
        levelUpdater(levelDict)    
                   
        sprites.draw(screen) # Draws all sprites
        
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright)
        levelRect = levelDisplay.get_rect(topleft = screen.get_rect().topleft)
        
        screen.blit(timerDisplay, timerRect)
        screen.blit(levelDisplay, levelRect)
        
        pygame.display.flip()
        screen.fill(screenColor)
        clk.tick(fps)
    
    print("You survived for", gameClock, "seconds and made it to level", currentLevel)
    pygame.quit()
        
if __name__ == '__main__':
    main()
    
    
    



