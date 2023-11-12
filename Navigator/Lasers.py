import pygame,math
import Settings as settings
from Explosion import Explosion

# LASERS
class Laser(pygame.sprite.Sprite):
    def __init__(self,game,player,obstacles):
        super().__init__()
        self.laserType = player.laserType
        self.speed = player.laserSpeed
        self.angle = player.angle
        newBlit = game.rotateImage(player.laserImage,player.laserImage.get_rect(center = player.rect.center),self.angle)
        self.image = newBlit[0]
        self.rect = newBlit[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.target, self.seek, self.seekWaitTime, self.seekDelay = None, False, 0, settings.heatSeekDelay # For heat seeking lasers


    # MOVE LASERS
    def update(self,game,player,lasers,obstacles):
        # Remove offscreen lasers
        if self.rect.centerx > settings.screenSize[0] or self.rect.centery > settings.screenSize[1] or self.rect.centerx < 0 or self.rect.centery < 0: self.kill()
        elif self.laserType == "NORMAL": self.normalMove(player)
        elif self.laserType == "HOME": self.homingMove(game,player,lasers,obstacles)
        else: self.normalMove(player)


    # Simple movement
    def normalMove(self,player):
        angle = math.radians( (self.angle-90))
        velX = 1.414 * self.speed * math.cos(angle)
        velY = 1.414 * self.speed * math.sin(angle)
        self.rect.centerx -= velX
        self.rect.centery += velY


    def homingMove(self,game,player,lasers,obstacles):
        if self.seekWaitTime < settings.heatSeekDelay:
            self.seekWaitTime += 1
            self.normalMove(player)
        elif self.seek == False: self.target, self.seek = self.getClosestPoint(obstacles), True # Get target
        else:
            if self.target is None or not obstacles.has(self.target):
                if settings.heatSeekNeedsTarget:
                    game.explosions.append(Explosion(game,self,None))
                    self.kill()
                else:
                    self.rect.centerx +=self.speed * math.cos(self.angle) # Horizontal movement
                    self.rect.centery +=self.speed * math.sin(self.angle) # Vertical movement

            else: # Homing
                dirX = (self.target.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
                dirY = (self.target.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
                direction = math.atan2(dirY,dirX) # Angle to shortest path
                self.rect.centerx += (self.speed) * math.cos(direction) # Horizontal movement
                self.rect.centery += (self.speed) * math.sin(direction) # Vertical movement
                self.angle = math.degrees(direction)


    # Get closest target out of a group
    def getClosestPoint(self, points):
        closest,shortest = None,None
        for pt in points:
            if pt.active:
                if closest is None or math.dist(self.rect.center,closest.rect.center) > math.dist(self.rect.center,pt.rect.center):
                    closest,shortest = pt, math.dist(self.rect.center,pt.rect.center)
        return closest



# ENEMY LASERS
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, game, obs, player):
        super().__init__()
        self.speed = obs.speed * 1.5
        self.angle = obs.angle
        if type(self.angle) == str: self.angle = game.getAngle(self.angle)  # Convert to degrees
        self.laserType = obs.laserType
        newBlit = game.rotateImage(game.assets.enemyLaserImage, game.assets.enemyLaserImage.get_rect(center=obs.rect.center), self.angle)
        self.image = newBlit[0]
        self.rect = newBlit[1]
        self.mask = pygame.mask.from_surface(self.image)

        self.target, self.seek, self.seekWaitTime, self.seekDelay = None, False, 0, settings.heatSeekDelay  # For heat seeking lasers
        if self.laserType == "TARGET": # For targeted lasers
            dirX = (player.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
            dirY = (player.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
            self.direction = math.atan2(dirY,dirX) # Angle to shortest path
            self.angle = math.degrees(self.direction)

        else: self.direction = [math.cos(math.radians(-self.angle)), math.sin(math.radians(-self.angle))]


    # UPDATE
    def update(self,player):
        # Remove offscreen lasers
        if self.rect.centerx > settings.screenSize[0] or self.rect.centery > settings.screenSize[1] or self.rect.centerx < 0 or self.rect.centery < 0: self.kill()
        if self.laserType == "HOME": self.homingMove(player)
        elif self.laserType == "TARGET": self.targetMove()
        else: self.normalMove()


    # Linear movement
    def normalMove(self):
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]


    # Heat seeking movement
    def homingMove(self,game,player):
        if self.seekWaitTime < settings.heatSeekDelay:
            self.seekWaitTime += 1
            self.normalMove()
        elif self.seek == False: self.target, self.seek = player, True # Get target
        else:
            if self.target is None:
                if settings.heatSeekNeedsTarget:
                    game.explosions.append(Explosion(game,self,None))
                    self.kill()
                else:
                    self.rect.centerx +=self.speed * math.cos(self.angle) # Horizontal movement
                    self.rect.centery +=self.speed * math.sin(self.angle) # Vertical movement

            else: # Homing
                dirX = (self.target.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
                dirY = (self.target.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
                direction = math.atan2(dirY,dirX) # Angle to shortest path
                self.rect.centerx += self.speed * math.cos(direction) # Horizontal movement
                self.rect.centery += self.speed * math.sin(direction) # Vertical movement
                self.angle = math.degrees(direction)

    # Targeted movement
    def targetMove(self):
        self.rect.centerx += self.speed * math.cos(self.direction)
        self.rect.centery += self.speed * math.sin(self.direction)
