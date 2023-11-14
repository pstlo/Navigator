import math,pygame
from Player import Player
import Settings as settings

class AIPlayer(Player):
    def __init__(self,game):
        super().__init__(game)
        self.maxObsConsidered = 3


    def getClosestOBS(self,game,threats):
        closest = None
        for obs in game.obstacles:
            if obs.active and not obs in threats:
                if closest is None or math.dist(self.rect.center,closest.rect.center) > math.dist(self.rect.center,obs.rect.center): closest = obs
        return closest
    

    def movement(self, game):
        dirX = (game.thisPoint.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
        dirY = (game.thisPoint.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
        direction = math.atan2(dirY,dirX) # Angle to shortest path
        
        self.angle = -math.degrees(direction) - 90 # Rotate
        newRect = self.getNextRect(game,self.rect,self.speed,direction)
    
        count = 0
        threats = []
        for i in game.obstacles:
            if count < self.maxObsConsidered: 
                threat = self.getClosestOBS(game,threats)
                if threat is not None: threats.append(threat)
            count += 1

        willCollide = False
        for i in threats: # Stop for obstacles
            if newRect.colliderect(i.rect): 
                willCollide = True 
                break

            newObsRect = self.getNextRect(game,i.rect,i.speed,i.direction)

        if not willCollide: self.rect = newRect


    def getNextRect(self,game,oldRect,speed,direction): # Get rect at next position in path
        validDirection = direction
        if type(validDirection) == str: validDirection = game.getAngle(validDirection) # Will revisit obstacle nonsense direction mechanic
        newRect = oldRect.copy()
        newRect.centerx += (speed) * math.cos(validDirection) # Horizontal movement
        newRect.centery += (speed) * math.sin(validDirection) # Vertical movement
        return newRect

