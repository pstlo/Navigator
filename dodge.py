import random
import math
import sys
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

# PLAYER
playerColor = [255,255,255] # Default = [255,255,255]
playerSize = 10 # Default = 10            
playerGrowth = 3 # Default = 3
playerSpeed = 5 # Default = 5

# OBSTACLES
obstacleSpeed = 3  # Default = 3           
obstacleSize = 5    # Default = 5
obstacleColor = [255,0,0] # Default = [255,0,0]
maxObstacles = 12  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" (Can be updated by level)

# LEVELS:   [ False , TIME, BOUNDS, SPEED, SIZE, NUMBER, COLOR ] , then add to levelSettingsList
levelTwo = [ False, 15, "KILL", 1, 1, 1.5, [255,255,0] ] # Default = [ False, 15, "KILL", 1, 1, 1.5, [255,255,0] ]
levelThree = [ False, 30, "KILL", 1, 1.5, 1, [0,0,255] ] # Default = [False, 30, "KILL", 1, 1.5, 1, [0,0,255] ]
levelFour = [ False, 45, "KILL", 1, 1.5, 1, [0,255,0] ] # Default = [False, 45, "KILL", 1, 1.5, 1, [0,255,0] ]
levelFive = [ False, 60, "KILL", 1.25, 1, 1, [0,255,255] ] # Default = [False, 60, "KILL", 1.25, 1, 1, [0,255,255] ]
levelSix = [ False, 75, "WRAP", 0.5, 10, 0.1, [255,0,255] ] # Default = [False, 75, "WRAP", 0.5, 10, 0.1, [255,0,255] ]
levelSeven = [ False, 90, "KILL", 2, 0.1, 10, [100,0,50] ] # Default = [False, 90, "KILL", 2, 0.1, 10, [100,0,50] ]
levelEight = [ False, 105, "BOUNCE", 1.25, 1.25, 1.0, [0,150,50] ] # Default = [False, 105, "BOUNCE", 1.25, 1.25, 1.0, [0,150,50] ]
levelNine = [ False, 120, "KILL", 1.25, 1.25, 1.25, [255,255,0] ] # Default = [ False, 120, "KILL", 1.25, 1.25, 1.25, [255,255,0] ]
levelTen = [ False, 135, "WRAP", 1, 1, 1, [255,255,255] ] # Default = [ False, 135, "WRAP", 1, 1, 1, [255,255,255] ]
overTime = [ False, 150, "KILL", 1.1, 1.1, 1.1, [255,0,0] ] # Default = [ False, 150, "KILL", 1.1, 1.1, 1.1, [255,0,0] ]
levelSettingsList = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen,overTime]
#---------------------------------------------------------------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.color = playerColor 
            self.size = playerSize        
            self.pos = [screenSize[0] / 2 , screenSize[1] / 2]
            self.speed = playerSpeed              
            self.growth = playerGrowth            
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = obstacleColor
        self.speed = obstacleSpeed
        self.size = obstacleSize
        self.movement = getMovement()
        self.pos = [self.movement[0][0], self.movement[0][1]]
        self.direction = self.movement[1]

currentLevel = 1    
player = Player()
obstacles = []
clk = pygame.time.Clock()
screen = pygame.display.set_mode(screenSize)
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
                        "COLOR" :  settings[6]                    
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

    def levelUpdater(levelDict):   # PASS THE CORRESPONDING DICT TO THIS FUNCTION
        global obstacleBoundaries, obstacleSpeed, obstacleColor, maxObstacles, obstacleSize, currentLevel
    
        try:
            if not levelDict["START"] and levelDict["TIME"] == gameClock:
                    obstacleBoundaries = levelDict["bound"]
                    obstacleSpeed *= levelDict["speedMult"]
                    obstacleColor = levelDict["COLOR"]
                    maxObstacles *= levelDict["maxObsMult"]
                    obstacleSize *= levelDict["obsSizeMult"]
                    currentLevel += 1
                    levelDict["START"] = True
        except:
            pass



    def movement():
        
        key = pygame.key.get_pressed()
        
        if key[pygame.K_w] or key[pygame.K_UP]:
            player.pos[1] -= player.speed
            
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            player.pos[1] += player.speed
            
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            player.pos[0] -= player.speed 
            
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            player.pos[0] += player.speed
        
    def wrapping():
        if player.pos[1]  > screenSize[1]:
            player.pos[1] = 0
            player.size += player.growth
        
        if player.pos[1] < 0:
            player.pos[1] = screenSize[1]
            player.size += player.growth
        
        if player.pos[0] > screenSize[0]:
            player.pos[0] = 0
            player.size += player.growth
        
        if player.pos[0] < 0:
            player.pos[0] = screenSize[0]
            player.size += player.growth
    
    def spawner():
        if len(obstacles) < maxObstacles:
            obstacle = Obstacle()
            obstacles.append(obstacle)
    
    def drawObstacles():
        for obstacle in obstacles:
            pygame.draw.circle(screen, (obstacle.color), obstacle.pos, obstacle.size)
   
    def obstacleMove():
        for obs in obstacles:
            position = obs.pos
            
            if "N" in obs.direction:
                obs.pos[1] -= obs.speed
                
            if "S" in obs.direction:
                obs.pos[1] += obs.speed
                
            if "E" in obs.direction:
                obs.pos[0] += obs.speed
                
            if "W" in obs.direction:
                obs.pos[0] -= obs.speed
   
                
    def obstacleRemove():
        for obs in obstacles:
            position = obs.pos
            
            if obs.pos[0] > screenSize[0] or obs.pos[0] < 0:
                obstacles.remove(obs)
                obs.kill()

            elif obs.pos[1] > screenSize[1] or obs.pos[1] < 0:
                obs.kill()
                obstacles.remove(obs)
                
    def bounceObstacle():
        for obs in obstacles:
            direction = obs.direction
            
            if obs.pos[1]  > screenSize[1]:
                obs.direction = movementReverse(direction) 
                
            if obs.pos[1] < 0:
                obs.direction = movementReverse(direction)
                
            if obs.pos[0] > screenSize[0]:
                obs.direction = movementReverse(direction) 
                
            if obs.pos[0] < 0:
                obs.direction = movementReverse(direction)
                

    def wrapObstacle():
        for obs in obstacles:
            
            if obs.pos[1]  > screenSize[1]:
                obs.pos[1] = 0  
                
            if obs.pos[1] < 0:
                obs.pos[1] = screenSize[1]    
                
            if obs.pos[0] > screenSize[0]:
                obs.pos[0] = 0        
                
            if obs.pos[0] < 0:
                obs.pos[0] = screenSize[0]
    
    
    

    # GAME LOOP
    while running:
        
        for event in pygame.event.get():
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
            
            elif event.type == timerEvent:
                gameClock +=1
                timerDisplay = timerFont.render(str(gameClock), True, (255,255,255))
                
        # LEVEL DISPLAY
        levelNum = "Level " + str(currentLevel)
        levelFont = pygame.font.SysFont(None, levelSize)
        levelDisplay = levelFont.render( str(levelNum), True, levelColor )
        
        # COLLISION DETECTION
        playerCenter = player.pos
        for obs in obstacles:
            obsCenter = obs.pos
            if ( (math.dist(playerCenter,obsCenter)) < (player.size + obs.size) ):
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
                
        drawObstacles()    
        pygame.draw.circle(screen, player.color, player.pos, player.size)
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright)
        levelRect = levelDisplay.get_rect(topleft = screen.get_rect().topleft)
        screen.blit(timerDisplay, timerRect)
        screen.blit(levelDisplay, levelRect)
        pygame.display.flip()
        screen.fill(screenColor)
        clk.tick(fps)
        
if __name__ == '__main__':
    main()
    
    
    



