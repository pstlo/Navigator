import pygame,math,random
import Settings as settings

# POWER UP SPAWNS
class Point(pygame.sprite.Sprite):
    def __init__(self,game,player,lastPos):
        super().__init__()
        self.powerUp = ''
        pointChoices = settings.powerUpList.copy()
        if not player or (not player.hasShields and player.boostDrain == 0 and player.laserCost == 0  and player.baseSpeed == player.boostSpeed): self.powerUp = "Default"
        else:
            powerUps = pointChoices
            if not player.hasShields and "Shield" in powerUps: del pointChoices["Shield"]
            if not player.hasGuns and player.baseSpeed == player.boostSpeed and "Fuel" in powerUps: del pointChoices["Fuel"]
            self.powerUp = random.choices(list(pointChoices.keys()),weights = list(pointChoices.values()) )[0]

        self.image = pygame.transform.scale(game.assets.pointsList[self.powerUp], (settings.pointSize, settings.pointSize)) # GET SCALED IMAGE / not ideal

        if lastPos == None: self.rect = self.image.get_rect(center = self.positionGenerator())
        else:self.rect = self.image.get_rect(center = self.spacedPositionGenerator(lastPos))
        self.mask = pygame.mask.from_surface(self.image)


    # POINT POSITION GENERATION
    def getPosition(self):
        xRange = [settings.screenSize[0] * settings.spawnRange[0] , settings.screenSize[0] * settings.spawnRange[1] ]
        yRange = [settings.screenSize[1] * settings.spawnRange[0] , settings.screenSize[1] * settings.spawnRange[1] ]
        xNum = random.randint(int(xRange[0]),int(xRange[1]))
        yNum = random.randint(int(yRange[0]),int(yRange[1]))
        return [xNum,yNum]


    # CHECK IF POINT IS IN SPAWN AREA
    def pointValid(self,point):
        centerX, centerY = settings.screenSize[0]/2, settings.screenSize[1]/2
        lines = [((centerX + math.cos(angle + math.pi/settings.spawnVertices)*settings.spawnWidth/2, centerY + math.sin(angle + math.pi/settings.spawnVertices)*settings.spawnHeight/2), (centerX + math.cos(angle - math.pi/settings.spawnVertices)*settings.spawnWidth/2, centerY + math.sin(angle - math.pi/settings.spawnVertices)*settings.spawnHeight/2)) for angle in (i * math.pi/4 for i in range(8))]
        sameSide = [((point[0]-l[0][0])*(l[1][1]-l[0][1]) - (point[1]-l[0][1])*(l[1][0]-l[0][0]))  * ((centerX-l[0][0])*(l[1][1]-l[0][1]) - (centerY-l[0][1])*(l[1][0]-l[0][0])) >= 0  for l in lines]
        return all(sameSide)


    # GET POSITION IN SPAWN AREA
    def positionGenerator(self):
        attempts = 0
        while True:
            point = self.getPosition()
            if attempts < settings.maxRandomAttempts and self.pointValid(point):return point
            else: attempts+=1


    # Get new position at valid distance from last position
    def spacedPositionGenerator(self,lastPos):
        attempts = 0
        while True:
            point = self.positionGenerator()
            if attempts < settings.maxRandomAttempts and math.dist(point,lastPos) >= settings.minDistanceToPoint: return point
            else: attempts+=1