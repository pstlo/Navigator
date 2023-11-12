import pygame,random,math
import Settings as settings
from Lasers import EnemyLaser

# OBSTACLES
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,game,playerPos,**kwargs):
        super().__init__()
        # Accept kwargs or default to level settings
        self.attributeIndex = None
        self.spawnPattern = kwargs.get('spawn', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSpawn"]))
        self.target = kwargs.get('target', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleTarget"]))
        self.movement = game.getMovement(self.spawnPattern)
        self.speed = int(kwargs.get('speed', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSpeed"])))
        self.size = int(kwargs.get('size', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSize"])))
        self.spinSpeed = int(kwargs.get('spin', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSpin"])))
        self.health = int(kwargs.get('health', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleHealth"])))
        self.bounds = kwargs.get('bounds', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleBounds"]))
        self.laserType = kwargs.get('lasers', self.getAttributes(game.assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleLaserType"]))

        try: self.image = kwargs.get('image', self.getAttributes(game.assets.obstacleImages[game.currentStage - 1][game.currentLevel-1]))
        except: self.image = game.assets.obstacleImages[0][random.randint(0,len(game.assets.obstacleImages[0])-1)] # Not enough assets for this level yet

        self.image = pygame.transform.scale(self.image, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.getDirection(playerPos)
        self.angle = random.randint(0,360) # Image rotation
        self.spinDirection = random.choice([-1,1])
        self.active = False
        self.slowerDiagonal = settings.slowerDiagonalObstacles
        self.laserDelay, self.lasersShot, self.maxLasers = 0, 0, settings.maxObsLasers


    # For levels with multiple obstacle types
    def getAttributes(self,attribute):
        if type(attribute) == list:
            if self.attributeIndex is None: self.attributeIndex = random.randint(0,len(attribute)-1)
            if self.attributeIndex > len(attribute): return attribute[random.randint(0,len(attribute)-1)]
            return attribute[self.attributeIndex] # Treat as parallel lists
        else: return attribute


    # Get correct type representation of angle
    def getDirection(self,playerPos):
        if self.target == "NONE": self.direction = self.movement[1] # Get a string representation of the direction
        else: self.direction = math.atan2(playerPos[1] - self.rect.centery, playerPos[0] - self.rect.centerx) # Get angle representation


    # Call corresponding movement function
    def move(self,game,player,enemyLasers):
        if self.target == "NONE": self.basicMove()
        elif self.target == "LOCK": self.targetMove()
        elif self.target == "HOME": self.homingMove(game,player)
        if self.laserType != "NONE": self.shoot(game,player,enemyLasers)


    # BASIC MOVEMENT (8-direction) -> direction is a string
    def basicMove(self):
        if self.slowerDiagonal: # Use sqrt(2) for correct diagonal movement
            if self.direction == "N": self.rect.centery -= self.speed
            elif self.direction == "S": self.rect.centery += self.speed
            elif self.direction == "E": self.rect.centerx += self.speed
            elif self.direction == "W": self.rect.centerx -= self.speed
            else:
                if "N" in self.direction: self.rect.centery -= self.speed / 1.414
                if "S" in self.direction: self.rect.centery += self.speed / 1.414
                if "E" in self.direction: self.rect.centerx += self.speed / 1.414
                if "W" in self.direction: self.rect.centerx -= self.speed / 1.414
        else:
            if "N" in self.direction: self.rect.centery -= self.speed
            if "S" in self.direction: self.rect.centery += self.speed
            if "E" in self.direction: self.rect.centerx += self.speed
            if "W" in self.direction: self.rect.centerx -= self.speed


    # AIMED AT PLAYER -> direction is an angle
    def targetMove(self):
        self.rect.centerx +=self.speed * math.cos(self.direction)
        self.rect.centery +=self.speed * math.sin(self.direction)


    # HEAT SEEKING -> direction is an angle, updated every frame
    def homingMove(self,player):
        dirX = (player.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
        dirY = (player.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
        self.direction = math.atan2(dirY,dirX) # Angle to shortest path
        self.angle = -math.degrees(self.direction)-90
        self.targetMove()


    # BOUNDARY HANDLING
    def bound(self,obstacles):
        if self.bounds == "KILL": # Remove obstacle
            if self.rect.left > settings.screenSize[0] + settings.spawnDistance or self.rect.right < -settings.spawnDistance:
                obstacles.remove(self)
                self.kill()
            elif self.rect.top > settings.screenSize[1] + settings.spawnDistance or self.rect.bottom < 0 - settings.spawnDistance:
                obstacles.remove(self)
                self.kill()

        elif self.bounds == "BOUNCE": # Bounce off walls
            if self.rect.left < 0:
                if self.target == "NONE": self.movementReverse()
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.left = 1

            elif self.rect.right > settings.screenSize[0]:
                if self.target == "NONE": self.movementReverse()
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.right = settings.screenSize[0] - 1

            elif self.rect.top < 0:
                if self.target == "NONE": self.movementReverse()
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.top = 1

            elif self.rect.bottom > settings.screenSize[1]:
                if self.target == "NONE": self.movementReverse()
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.bottom = settings.screenSize[1]-1

        elif self.bounds == "WRAP": # Wrap around screen
            if self.rect.centery > settings.screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = settings.screenSize[1]
            if self.rect.centerx > settings.screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = settings.screenSize[0]


    # ACTIVATE OBSTACLE
    def activate(self):
        if not self.active:
            if self.rect.right > 0 and self.rect.left < settings.screenSize[0] and self.rect.bottom > 0 and self.rect.top < settings.screenSize[1]: self.active = True


    # GET INVERSE MOVEMENT DIRECTION
    def movementReverse(self):
        if self.direction == "N": self.direction = "S"
        elif self.direction == "S": self.direction = "N"
        elif self.direction == "E": self.direction = "W"
        elif self.direction == "W": self.direction = "E"
        elif self.direction == "NW": self.direction = "SE"
        elif self.direction == "NE": self.direction = "SW"
        elif self.direction == "SE": self.direction = "NW"
        elif self.direction == "SW": self.direction = "NE"


    # Shoot lasers
    def shoot(self,game,player,enemyLasers):
        if enemyLasers is not None:
            if self.lasersShot < self.maxLasers and self.laserDelay >= settings.obsLaserDelay:
                enemyLasers.add(EnemyLaser(game,self,player))
                self.lasersShot += 1
                self.laserDelay = 0
            else: self.laserDelay += 1



# CAVES
class Cave(pygame.sprite.Sprite):
    def __init__(self,game,index):
        super().__init__()
        self.speed = settings.caveSpeed
        self.background = game.assets.caveList[index][0]
        self.image = game.assets.caveList[index][1]
        self.rect = self.image.get_rect(bottomleft = (0,settings.caveStartPos))
        self.mask = pygame.mask.from_surface(self.image)
        self.leave = False # Mark cave for exit


    # True if cave is covering screen
    def inside(self):
        if self.rect.top < 0 and self.rect.bottom > settings.screenSize[1]: return True
        else: return False


    def update(self):
        self.rect.centery += self.speed # Move
        if not self.leave and self.rect.top > settings.screenSize[1] * -1: self.rect.bottom = settings.screenSize[1]*2