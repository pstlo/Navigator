import random
import math
import sys
from os import environ
 
# GAME CONSTANTS
    
# SCREEN
screenSize = [800,800] # Default = [800,800]
screenColor = [0,0,0] # Default = [0,0,0]
fps = 60 # Default = 60
timerSize = 75 # Default = 100
timerColor = [255,255,255] # Default = [255,255,255]
timerDelay = 1000 # Default = 1000

# PLAYER
playerColor = [255,255,255] # Default = [255,255,255]
playerSize = 10 # Default = 10            
playerGrowth = 3 # Default = 3
playerSpeed = 5 # Default = 5

# OBSTACLES
obstacleSpeed = 3  # Default = 3           
obstacleSize = 5    # Default = 5
obstacleColor = [255,0,0] # Default = [255,0,0]
maxObstacles = 10  # Default = 10

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
pygame.init()


def main():
    
    def getPosition():
        X = random.randint(0, screenSize[0])
        Y = random.randint(0, screenSize[1])

        lowerX = random.randint(0, screenSize[0] * 0.1)
        upperX =  random.randint(screenSize[0] * 0.9, screenSize[0])
        lowerY  = random.randint(0, screenSize[1] * 0.1)
        upperY = random.randint(screenSize[1] * 0.9, screenSize[1])
        
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
        selected = possible[ random.randint(0, len(possible) - 1) ]
        
        return selected

    def getMovement():
        movement = getPosition()
        position = [movement[0], movement[1]]
        direction = movement[2]
        move = [position,direction]
        return move
                
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
            
    
    # GAME LOGIC
    player = Player()
    obstacles = []
    clk = pygame.time.Clock()
    screen = pygame.display.set_mode(screenSize)
    font = pygame.font.SysFont(None, timerSize)
    gameClock = 0
    timerDisplay = font.render(str(gameClock), True, timerColor)
    
    timerEvent = pygame.USEREVENT + 1
    pygame.time.set_timer(timerEvent, timerDelay)
    
    global running
    running = True

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
                

                
    def normalObstacleRemove():
        for obs in obstacles:
            position = obs.pos
            
            if obs.pos[0] > screenSize[0] or obs.pos[0] < 0:
                obstacles.remove(obs)
                obs.kill()

            elif obs.pos[1] > screenSize[1] or obs.pos[1] < 0:
                obs.kill()
                obstacles.remove(obs)
                
    def wrapObstacle():
        for obs in obstacles:
            position = obs.pos 
            print(position)            
            
            if obs.pos[1]  > screenSize[1]:
                obs.pos[1] = 0
                
            if obs.pos[1] < 0:
                obs.pos[1] = screenSize[1]

            if obs.pos[0] > screenSize[0]:
                obs.pos[0] = 0
                
            if obs.pos[0] < 0:
                obs.pos[0] = screenSize[0]
                
                            
    def update():
        pygame.draw.circle(screen, player.color, player.pos, player.size)
        textRect = timerDisplay.get_rect(topright = screen.get_rect().topright)
        screen.blit(timerDisplay, textRect)
        pygame.display.flip()
        screen.fill(screenColor)
        clk.tick(fps)
        
    
    
    # GAME LOOP
    
    obstacleBoundaries = "NORMAL"
    
    levelOne = True # Redundant
    levelTwo = False
    levelThree = False
    levelFour = False
    levelFive = False
    levelSix = False
    levelSeven = False
     
    global maxObstacles
    global obstacleSize
    global obstacleColor
    global obstacleSpeed
    
    while running:
        
        for event in pygame.event.get():
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
            
            elif event.type == timerEvent:
                gameClock +=1
                timerDisplay = font.render(str(gameClock), True, (255,255,255))
                
        
        # COLLISION DETECTION
        playerCenter = player.pos
        for obs in obstacles:
            obsCenter = obs.pos
            if ( (math.dist(playerCenter,obsCenter)) < (player.size + obs.size) ):
                running = False
                pygame.quit()
                sys.exit()
                
        # STARTS ON LEVEL 1
     
        # LEVEL 2
        if gameClock == 15 and levelTwo == False:
            maxObstacles *= 1.5
            obstacleColor = [255,255,0]
            levelTwo = True
        
        # LEVEL 3
        elif gameClock == 30 and levelThree == False:
            obstacleSize *= 1.5
            obstacleColor = [0,0,255]
            levelThree = True
        
        # LEVEL 4
        elif gameClock == 45 and levelFour == False:
            obstacleSize *= 1.5
            obstacleColor = [0,255,0]
            levelFour = True
        
        # LEVEL 5
        elif gameClock == 60 and levelFive == False:
            obstacleSpeed *= 1.5
            obstacleColor = [0,255,255]
            levelFive = True
        
        # LEVEL 6
        elif gameClock == 75 and levelSix == False:
            obstacleSize *= 10
            obstacleSpeed /= 2
            obstacleColor = [255,0,255]
            obstacleBoundaries = "WRAP"
            levelSix = True
        
        # LEVEL 7
        elif gameClock == 90 and levelSeven == False:
            obstacleSize /= 10
            maxObstacles *= 1.5
            obstacleSpeed *= 1.25
            obstacleBoundaries = "NORMAL"
            obstacleColor = [100, 0, 50]
            levelSeven = True
            
        movement()
        wrapping()
        spawner()
        
        obstacleMove()
        
        if obstacleBoundaries == "NORMAL":
            normalObstacleRemove()
        
        if obstacleBoundaries == "WRAP":
            wrapObstacle()
            
        drawObstacles()    
        update()
        
if __name__ == '__main__':
    main()
    
    
    



