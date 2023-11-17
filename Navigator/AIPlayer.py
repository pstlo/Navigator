import math,random,pygame
from Player import Player
import Settings as settings
from Lasers import Laser

class AIPlayer(Player):
    def __init__(self,game):
        super().__init__(game)

        self.dangerZoneStart = 50 # Dist at which OBS are considered dangerous
        self.safeZoneStart = 60 # Dist at which obs are considered safe
        self.maxObsConsidered = 3 # maximum obstacles considered per frame
        self.futureDistance = 50 # OBS Path length
        self.leapDistance = 80 # Target distance from player
        self.destinationDistance = 2 # Destination size
        self.precision = 5 # must be positive, lower value = higher precision angle
        self.returnToCenter = False # True -> find path back to center / False -> find path away from danger
        self.loopForAvoid = False # Find path out of danger including looping around screen
        self.loopForFollow = False # Find path to point including looping around screen
        self.useVectors = True
        self.boostByDefault = not self.hasGuns

        self.target = []
        self.direction = None
        self.dangerZone = self.dangerZoneStart
        self.safeZone = self.safeZoneStart
        self.drawThreats = True
        self.drawPaths = True



    def movement(self, game):
        pointPath = [self.rect.center, game.thisPoint.rect.center] # Path to point
        if self.target is not None and len(self.target) == 2:
            targetPath = [self.rect.center, self.target] # Path to target
            prevTarget = [self.target[0],self.target[1]]

        else: targetPath = None

        if self.drawPaths:
            pygame.draw.line(game.screen,[0,255,0],pointPath[0],pointPath[1])
            if targetPath is not None: pygame.draw.line(game.screen,[0,255,255],targetPath[0],targetPath[1])

        if self.drawThreats:
            pygame.draw.circle(game.screen,[255,0,0], self.rect.center, self.dangerZone, 3) # Draw danger zone

        # Threat detection
        threats = self.getThreats(game)
        if threats is not None and len(threats) > 0: closestThreatDist = math.dist(threats[0].rect.center,self.rect.center)
        else: closestThreatDist = None

        # First call
        if closestThreatDist is None or self.direction is None:
            self.target = game.thisPoint.rect.center # Go to point
            self.getDirection(self.loopForFollow)

        # In danger
        elif closestThreatDist < self.dangerZone: 
            self.getTarget(game,threats,self.direction)
            self.getDirection(self.loopForAvoid)

        # No longer in danger
        elif closestThreatDist > self.safeZone:
            self.target = game.thisPoint.rect.center # Go to point
            self.getDirection(self.loopForFollow)


        if self.direction is not None and math.dist(self.target,self.rect.center) > self.destinationDistance:
            newRect = self.getNextRect(game,self.speed,self.direction) # Rect at next frame
            self.angle = round(-math.degrees(self.direction) - 90)  # ROTATE PLAYER
            self.rect = newRect


    
    def getTarget(self,game,threats,direction):
        options = {
                'next' : {
                    "target" : self.getNextRect(game,self.speed,direction),
                    "aim" : self.getNextRect(game,self.leapDistance,direction),
                    "invalid" : False },
                'stop' : {
                    "target" : self.rect,
                    "aim" : self.rect,
                    "invalid" : False }
            }

        num = 0
        while num <= 360: # Populate movement options
            newDict = {
                "target" : self.getNextRect(game,self.speed,num),
                "aim" : self.getNextRect(game,self.leapDistance,num),
                "invalid" : False
            }
            options.update({'Angle '+str(num): newDict})
            num += self.precision

        centers = []
        screenCenter = [settings.screenSize[0]/2,settings.screenSize[1]/2]
        for threat in threats:
            i = self.getFutureRect(game,threat.rect,threat.speed,threat.direction)
            centers.append(i.center)

            for k in options:
                if not options[k]['invalid'] and options[k]['target'].colliderect(i): options[k]['invalid'] = True

            danger = self.getFutureCollision([self.rect.center, game.thisPoint.rect.center],[threat.rect.center,self.getFutureRect(game,threat.rect,threat.speed * self.futureDistance, threat.direction).center]) # Check if this obstacle path intersects with current path
            if danger is not None:
                if self.drawThreats: pygame.draw.circle(game.screen,[255,0,0], danger, 3) # Draw collision point

        avgX, avgY = 0,0
        for x,y in centers:
            avgX += x
            avgY += y
        centersLen = len(centers)
        if centersLen > 0:
            avgX /= centersLen
            avgY /= centersLen
            avgCenter = [avgX, avgY]
        else: avgCenter = screenCenter

        closest,closestDist = None,None # shortest distance to center
        longest, longestDist= None,None # longest avg dist from danger
        targ,targDist = None,None # shortest distance to target
        pt,ptDist= None,None # shortest distance to point

        for k in options: # Find safe paths
            if not options[k]['invalid']:

                tempDist = math.dist(options[k]['target'].center, avgCenter)
                if (longest is None or longestDist is None) or tempDist > longestDist:
                    longest = k # Farthest from danger
                    longestDist = tempDist

                tempDist = math.dist(options[k]['target'].center,screenCenter)
                if (closest is None or closestDist is None) or tempDist < closestDist:
                    closest = k # Closest to center
                    closestDist = tempDist

                tempDist = math.dist(options[k]['target'].center,self.target)
                if (targ is None or targDist is None) or tempDist < targDist:
                    targ = k # Closest to target
                    targDist = tempDist

                tempDist = math.dist(options[k]['target'].center,game.thisPoint.rect.center)
                if (pt is None or ptDist is None) or tempDist < ptDist:
                    pt = k # Closest to point
                    ptDist = tempDist


        if self.drawPaths:
            if longest is not None: pygame.draw.circle(game.screen,[0,255,255], options[longest]['aim'].center, 4)
            if closest is not None: pygame.draw.circle(game.screen,[255,255,0], options[closest]['aim'].center, 4)
            if targ is not None: pygame.draw.circle(game.screen,[0,0,255], options[targ]['aim'].center, 4)
            if pt is not None: pygame.draw.circle(game.screen,[255,0,255], options[pt]['aim'].center, 4)


        if self.returnToCenter:
            if closest is not None:
                settings.debug("Avoiding: " + closest) # Debug
                self.target = options[closest]['aim'].center

        elif longest is not None:
            settings.debug("Avoiding: " + longest) # Debug
            self.target = options[longest]['aim'].center

        else:
            settings.debug("Cannot avoid obstacle with current algorithm") # Debug
            return


    


    def getDirection(self,looping):

        if self.useVectors:
            playerV = pygame.Vector2(self.rect.center[0],self.rect.center[1])
            targetV = pygame.Vector2(self.target[0],self.target[1])
            finalV =  targetV - playerV
            self.direction = math.atan2(finalV.y, finalV.x)

        else:
            if looping:
                dirX = (self.target[0] - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path to target including around screen
                dirY = (self.target[1] - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path to target including around screen
            else:
                dirX = self.target[0] - self.rect.centerx # Shortest horizontal path to target
                dirY = self.target[1] - self.rect.centery  # Shortest vetical path to target
            self.direction = math.atan2(dirY,dirX) # Angle to shortest path to target



    def getClosestOBS(self,game,threats):
        closest = None
        for obs in game.obstacles:
            if threats is None or (obs.active and not obs in threats):
                if closest is None or math.dist(self.rect.center,closest.rect.center) > math.dist(self.rect.center,obs.rect.center): closest = obs
        return closest



    def getNextRect(self,game,speed,direction): # Get rect at next position in path
        newRect = self.rect.copy()
        newRect.centerx += (speed) * math.cos(direction) # Horizontal movement
        newRect.centery += (speed) * math.sin(direction) # Vertical movement
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


    
    def getThreats(self,game):
        # Detect Danger
        count = 0
        threats = [] # Closest obstacles
        for i in range(len(game.obstacles)):
            if count < self.maxObsConsidered:
                threat = self.getClosestOBS(game,threats)

                if threat is not None:
                    threats.append(threat)
                    if self.drawPaths: self.drawPath(game,threat)
            else: break
            count += 1
        return threats
    
    

    def shoot(self,game,lasers,events,obstacles):
        if self.hasGuns and self.laserReady:
            if self.fuel - self.laserCost > 0:
                lasers.add(Laser(game,self))
                self.fuel -= self.laserCost
                if not game.musicMuted: game.assets.laserNoise.play()
                events.laserCharge(self)



    def boost(self,game,events):
        if self.boostByDefault: self.autoBoost(game,events)



    def autoBoost(self,game,events):
        if self.boostReady:
            if self.fuel - self.boostDrain > self.boostDrain:
                self.speed = self.boostSpeed
                self.fuel -= self.boostDrain
                if not self.boosting: self.boosting = True
                if self.boostState + 1 < len(game.assets.spaceShipList[game.savedShipLevel]['boost']): self.boostState += 1
                else: self.boostState = 0
            else:
                if self.speed != self.baseSpeed: self.speed = self.baseSpeed
                if self.boosting: self.boosting = False
                events.boostCharge(self)


