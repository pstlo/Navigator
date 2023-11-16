import math,random,pygame
from Player import Player
import Settings as settings

class AIPlayer(Player):
    def __init__(self,game):
        super().__init__(game)

        self.maxObsConsidered = 3
        self.target = []
        self.futureDistance = 50 # OBS Path length
        self.dangerZone = 100 # Dist at which OBS are considered danger
        self.leapDistance = 50
        self.destinationDistance = 5

        self.drawThreats = False
        self.drawPaths = False


    def movement(self, game):

        pointPath = [self.rect.center, game.thisPoint.rect.center] # Path to point
        if self.target is not None and len(self.target) == 2:
            targetPath = [self.rect.center, self.target] # Path to target
            prevTarget = [self.target[0],self.target[1]]
        else: targetPath = None

        if self.drawPaths:
            pygame.draw.line(game.screen,[0,255,0],pointPath[0],pointPath[1])
            if targetPath is not None: pygame.draw.line(game.screen,[0,255,255],targetPath[0],targetPath[1])

        count = 0
        threats = [] # Closest obstacles
        for i in range(len(game.obstacles)):
            if count < self.maxObsConsidered:
                threat = self.getClosestOBS(game,threats)
                if threat is not None: threats.append(threat)
            else: break
            count += 1

        if threats is not None and len(threats) > 0: closestThreatDist = math.dist(threats[0].rect.center,self.rect.center)
        else: closestThreatDist = None

        if closestThreatDist is not None and closestThreatDist < self.dangerZone:

            dirX = (self.target[0] - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path to target
            dirY = (self.target[1] - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path to target
            direction = math.atan2(dirY,dirX) # Angle to shortest path to target

            options = {
                'next' : {
                    "target" : self.getNextRect(game,self.speed,direction),
                    "aim" : self.getNextRect(game,self.leapDistance,direction),
                    "invalid" : False
                    },

                'back' : {
                    "target" : self.getNextRect(game,self.speed,direction + 180),
                    "aim" : self.getNextRect(game,self.leapDistance,direction + 180),
                    "invalid" : False
                    },

                'left' : {
                    "target" : self.getNextRect(game,self.speed,direction +90),
                    "aim" : self.getNextRect(game,self.leapDistance,direction +90),
                    "invalid" : False
                    },

                'right' : {
                    "target" : self.getNextRect(game,self.speed,direction -90),
                    "aim" : self.getNextRect(game,self.leapDistance,direction -90),
                    "invalid" : False
                    },

                'stop' : {
                    "target" : self.rect,
                    "aim" : self.rect,
                    "invalid" : False
                    }
            }
            
            
            num = 15
            while num < 360:
                
                newDict = {
                    "target" : self.getNextRect(game,self.speed,num),
                    "aim" : self.getNextRect(game,self.leapDistance,num),
                    "invalid" : False
                }
                
                options.update({'angle'+str(num): newDict})
                
                num += 15
            

            for threat in threats:
                i = self.getFutureRect(game,threat.rect,threat.speed,threat.direction)
                if self.drawPaths: self.drawPath(game,threat)

                for k in options:
                    if not options[k]['invalid'] and options[k]['target'].colliderect(i): options[k]['invalid'] = True

                danger = self.getFutureCollision(pointPath,[threat.rect.center,self.getFutureRect(game,threat.rect,threat.speed * self.futureDistance, threat.direction).center]) # Check if this obstacle path intersects with current path
                if danger is not None and self.drawThreats: pygame.draw.circle(game.screen,[255,0,0], danger, 7)
    
    
            validPath = None
            for k in options: # Pick first valid path
                if not options[k]['invalid']:
                    settings.debug("Avoiding: " + k)
                    validPath = options[k]['aim'].center
                    
            if validPath is not None: self.target = validPath
            else: 
                settings.debug("Cannot avoid obstacle with current algorithm")
            


        else: self.target = game.thisPoint.rect.center # Go to point

        if math.dist(self.target,self.rect.center) > self.destinationDistance:
            dirX = (self.target[0] - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path to target
            dirY = (self.target[1] - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path to target
            direction = math.atan2(dirY,dirX) # Angle to shortest path to target
            newRect = self.getNextRect(game,self.speed,direction) # Rect at next frame
            self.angle = -math.degrees(direction) - 90  # Rotate
            self.rect = newRect



    def getClosestOBS(self,game,threats):
        closest = None
        for obs in game.obstacles:
            if threats is None or (obs.active and not obs in threats):
                if closest is None or math.dist(self.rect.center,closest.rect.center) > math.dist(self.rect.center,obs.rect.center): closest = obs
        return closest


    def getNextRect(self,game,speed,direction): # Get rect at next position in path
        validDirection = direction
        if type(validDirection) == str: validDirection = game.getAngle(validDirection) # Will revisit obstacle nonsense direction mechanic
        newRect = self.rect.copy()
        newRect.centerx += (speed) * math.cos(validDirection) # Horizontal movement
        newRect.centery += (speed) * math.sin(validDirection) # Vertical movement
        return newRect


    def getFutureRect(self,game,oldRect,dist,angle):
        validDirection = angle
        if type(validDirection) == str: validDirection = game.getAngle(validDirection) # Will revisit obstacle nonsense direction mechanic
        validDirection = math.radians(-validDirection - 90)
        newRect = oldRect.copy()
        newRect.centerx += (dist) * math.cos(validDirection) # Horizontal movement
        newRect.centery += (dist) * math.sin(validDirection) # Vertical movement
        return newRect


    def drawPath(self,game,obj):
        newRect = self.getFutureRect(game,obj.rect,obj.speed * 400,obj.direction)
        pygame.draw.line(game.screen,[0,0,255],obj.rect.center,newRect.center)
        if self.drawThreats:pygame.draw.line(game.screen,[255,0,0],self.rect.center,obj.rect.center)
        pygame.draw.rect(game.screen,[0,0,255],newRect)


    def getFutureCollision(self, line1, line2):
        def orientation(x1, y1, x2, y2, x3, y3): return (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)

        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        o1 = orientation(x1, y1, x2, y2, x3, y3)
        o2 = orientation(x1, y1, x2, y2, x4, y4)
        o3 = orientation(x3, y3, x4, y4, x1, y1)
        o4 = orientation(x3, y3, x4, y4, x2, y2)

        if (o1 * o2 < 0) and (o3 * o4 < 0):
            intersectionX = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
            intersectionY = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
            return intersectionX, intersectionY
        else: return None
