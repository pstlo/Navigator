import math,random,pygame
from Player import Player
import Settings as settings
from Lasers import Laser

class AIPlayer(Player):
    def __init__(self,game):
        super().__init__(game)

        # AI Config
        self.pointSafetyThreshold = 400 # Dist from nearest obs at which it is considered safe to go to point
        self.dangerZoneStart = 70 # Dist at which OBS are considered dangerous
        self.minDangerZone = 50 # Min danger zone for adapting
        self.maxDangerZone = 140 # Max danger zone for adapting
        self.safeZoneStart = 80 # Dist at which obs are considered safe
        self.minSafeZone = 55 # Min safe zone for adapting
        self.maxSafeZone = 150 # Max safe zone for adapting

        self.maxObsConsidered = 5 # maximum obstacles considered per frame
        self.futureDistance = 50 # OBS Path length for future collision detection
        self.leapDistance = 80 # Target distance from player

        # Path finding
        self.returnToCenter = False # True -> find path back to center
        self.straightToPoint = False # True -> find path straight to point
        self.continueToTarget = False # True -> find path straight to target
        self.avoidObstacles = True # True -> find path out of danger

        # Looping around screen
        self.loopForAvoid = False # Find path out of danger including looping around screen
        self.loopForFollow = False # Find path to point including looping around screen

        # Other logic
        self.zoneAdapt = False # Increment and decrement zone
        self.zoneIncrementer = 1
        self.zoneDecrementer = 1
        self.considerCenterSafe = False # Consider center of screen safest area
        self.restrictedPointFollowing = False # Only follow point if closer than nearest obstacle
        self.useVectors = False # Use pygame.Vector2 to calculate angles
        self.bogoPath = False # Pick random path method every time
        self.boostByDefault = not self.hasGuns # Always boost when able
        self.destinationDistance = 2 # Destination size
        self.precision = 5 # must be positive, lower value = higher precision angle

        # Visualize
        self.drawThreats = True
        self.drawPaths = True

        self.target = []
        self.direction = None
        self.dangerZone = self.dangerZoneStart
        self.safeZone = self.safeZoneStart




    def movement(self, game):
        pointPath = [self.rect.center, game.thisPoint.rect.center] # Path to point
        if self.target is not None and len(self.target) == 2:
            targetPath = [self.rect.center, self.target] # Path to target
            if self.drawPaths: pygame.draw.line(game.screen,[0,255,255],targetPath[0],targetPath[1]) # Draw path to target
        else: targetPath = None


        if self.drawThreats:
            pygame.draw.circle(game.screen,[255,0,0], self.rect.center, self.dangerZone, 3) # Draw danger zone

        # Threat detection
        threats = self.getThreats(game)
        if threats is not None and len(threats) > 0:
            closestThreatDist = math.dist(threats[0].rect.center,self.rect.center)
            closestThreatPos = [threats[0].rect.centerx,threats[0].rect.centery]
        else: closestThreatDist,closestThreatPos = None,None

        threatsPos = self.getObstaclesPos(threats)

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
            self.chooseTarget(game,threatsPos)
            self.getDirection(self.loopForFollow)

        # Move
        if self.direction is not None and math.dist(self.target,self.rect.center) > self.destinationDistance:
            newRect = self.getNextRect(game,self.speed,self.direction) # Rect at next frame
            self.angle = round(-math.degrees(self.direction) - 90)  # ROTATE PLAYER
            self.rect = newRect



    def chooseTarget(self,game,threats):
        closestObstacle = self.getClosestOBS(game,None)
        closestObsDist = math.dist(self.rect.center,closestObstacle.rect.center)
        closestObsPos = closestObstacle.rect.center
        if closestObsDist < self.pointSafetyThreshold and (not self.restrictedPointFollowing or math.dist(self.rect.center,game.thisPoint.rect.center) < math.dist(self.rect.center,closestObsPos)):
            chosenTarget = game.thisPoint.rect.center # Go to point

        else:
            chosenTarget = self.findSafeArea(threats,closestObsPos) # Find empty space
        self.target = chosenTarget



    def adapt(self,game,avgDist): # WIP
        if self.zoneAdapt:
            if avgDist < self.dangerZone and self.dangerZone - self.zoneDecrementer > self.minDangerZone:
                self.dangerZone -= self.zoneDecrementer
                self.safeZone -= self.zoneDecrementer
            elif avgDist > self.dangerZone and self.dangerZone + self.zoneIncrementer < self.maxDangerZone:
                self.dangerZone += self.zoneIncrementer
                self.safeZone += self.zoneIncrementer


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
        for threat in threats:
            i = self.getFutureRect(game,threat.rect,threat.speed,threat.direction)
            centers.append(i.center)

            for k in options:
                if not options[k]['invalid'] and options[k]['target'].colliderect(i): options[k]['invalid'] = True

        avgCenter = self.getDangerArea(centers,centers[0]) # Average threat position
        avgDist = math.dist(self.rect.center,avgCenter) # Average dist from threat

        self.adapt(game,avgDist)

        closest,closestDist = None,None # shortest distance to center
        longest, longestDist= None,None # longest avg dist from danger
        targ,targDist = None,None # shortest distance to target
        pt,ptDist= None,None # shortest distance to point

        for k in options: # Find safest paths
            if not options[k]['invalid']:

                tempDist = math.dist(options[k]['target'].center, avgCenter)
                if (longest is None or longestDist is None) or tempDist > longestDist:
                    longest = k # Farthest from danger
                    longestDist = tempDist

                tempDist = math.dist(options[k]['target'].center,[settings.screenSize[0]/2,settings.screenSize[1]/2])
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

        self.choosePath(game,options,longest,closest,targ,pt)



    def choosePath(self, game, options, longest, closest, targ, pt):
        if self.drawPaths:
            if longest is not None: pygame.draw.circle(game.screen,[0,255,255], options[longest]['aim'].center, 4)
            if closest is not None: pygame.draw.circle(game.screen,[255,255,0], options[closest]['aim'].center, 4)
            if targ is not None: pygame.draw.circle(game.screen,[0,0,255], options[targ]['aim'].center, 4)
            if pt is not None: pygame.draw.circle(game.screen,[255,0,255], options[pt]['aim'].center, 4)

        choices = [longest,closest,pt,targ]
        if self.bogoPath and None not in choices:
            choice = random.choice(choices)
            pathChoice = options[choice]['aim'].center

        elif self.returnToCenter and closest is not None:
            choice = closest
            pathChoice = options[closest]['aim'].center

        elif self.avoidObstacles and longest is not None:
            choice = longest
            pathChoice = options[longest]['aim'].center

        elif self.straightToPoint and pt is not None:
            choice = pt
            pathChoice = options[pt]['aim'].center

        elif self.continueToTarget and targ is not None:
            choice = targ
            pathChoice = options[targ]['aim'].center

        else:
            for choice in choices: # Pick first valid option
                if choice is not None:
                    pathChoice = options[choice]['aim'].center
                    break
            return

        self.target = pathChoice



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
        if self.drawThreats:
            newRect = self.getFutureRect(game,obj.rect,obj.speed * 400,obj.direction)
            pygame.draw.line(game.screen,[0,0,255],obj.rect.center,newRect.center)
            pygame.draw.line(game.screen,[255,0,0],self.rect.center,obj.rect.center)
            pygame.draw.rect(game.screen,[0,0,255],newRect)



    def getFutureCollisions(self, line1, line2):
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



    def getFutureCollision(self,threat):
        danger = self.getFutureCollisions([self.rect.center, selt.target],[threat.rect.center,self.getFutureRect(game,threat.rect,threat.speed * self.futureDistance, threat.direction).center]) # Check if this obstacle path intersects with current path
        if danger is not None:
            if self.drawThreats: pygame.draw.circle(game.screen,[255,0,0], danger, 3) # Draw collision point
            return danger



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



    def getObstaclesPos(self, obstacles):
        poss = []
        for obs in obstacles: poss.append(obs.rect.center)
        return poss



    def getDangerArea(self,threats,closest):
        avgX, avgY = 0,0
        for threat in threats:
            x = threat[0]
            y = threat[1]
            avgX += x
            avgY += y
        centersLen = len(threats)
        if centersLen > 0:
            avgX /= centersLen
            avgY /= centersLen
            return [avgX, avgY]
        else:
            if closest is not None: return closest
            else:
                # BOGO for now
                x = random.choice([0,settings.screenSize[0]])
                y = random.choice([0,settings.screenSize[1]])
                return [x,y]



    def findSafeArea(self,threats,closest):
        if self.considerCenterSafe: return [settings.screenSize[0]/2,settings.screenSize[1]/2]
        else:
            danger = self.getDangerArea(threats,closest)
            x = settings.screenSize[0] - danger[0]
            y = settings.screenSize[1] - danger[1]
            return [x,y]




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



