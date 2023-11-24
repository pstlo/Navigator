import sys,random,math,pygame
import Settings as settings
from Menu import Menu
from Player import Player
from AIPlayer import AIPlayer
from Obstacles import Obstacle,Cave
from Unlocks import Unlocks
from Point import Point
from Event import Event
from Explosion import Explosion
from Assets import Assets
from Menu import Menu
from Gamepad import Gamepad
import Leaderboard


# GAME
class Game:
    def __init__(self,screen):

        # CURSOR
        curSurf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.line(curSurf, (0, 255, 0), (10, 20), (30, 20), settings.cursorThickness)
        pygame.draw.line(curSurf, (0, 255, 0), (20, 10), (20, 30), settings.cursorThickness)
        cursor = pygame.cursors.Cursor((20, 20), curSurf)
        pygame.mouse.set_cursor(cursor)
        pygame.mouse.set_visible(settings.cursorMode)

        self.assets = Assets()
        self.version = self.assets.version
        self.screen = screen
        self.menu = Menu()
        self.controller = Gamepad() # Gamepad object
        self.gamePad = self.controller.gamePad # Joystick

        # GAME RECORDS
        self.records = self.assets.loadRecords()
        self.unlocks = Unlocks(self.records['unlocks']) # UNLOCKS

        # Level constants
        self.maxObstacles = self.assets.stageList[0][0]["maxObstacles"]
        self.levelType = self.assets.stageList[0][0]["levelType"]
        self.wipe = self.assets.stageList[0][0]["wipeObstacles"] # Old obstacle handling
        self.angle = self.assets.stageList[0][0]["levelAngle"] # Game rotation
        self.cloudSpeed = settings.cloudSpeed

        self.currentLevel = 1
        self.currentStage = 1
        self.score = 0 # Points collected
        self.coinsCollected = 0 # Coins collected

        self.thisPoint = Point(self,None,None) # Currently active point (starts with default)
        self.lastPointPos = self.thisPoint.rect.center # Last point's position for spacing
        self.gameClock = settings.gameStartTime
        self.pauseCount = 0
        self.attemptNumber = 1
        self.showLogoScreen = True
        self.mainMenu = True # Assures start menu only runs when called
        self.sessionLongRun = 0 # Longest run this session

        self.skipAutoSkinSelect = False # For re-entering home menu from game over screen
        self.savedSkin = 0 # Saved ship skin
        self.savedShipLevel = 0 # Saved ship type

        self.cloudPos = settings.cloudStart # Background cloud position
        self.explosions = [] # Obstacle explosions

        self.cave,self.caveIndex = None, 0 # For cave levels
        self.musicMuted = settings.musicMuted
        self.clk = pygame.time.Clock() # Gameclock
        self.usingController = settings.useController # Using controller for movement
        self.usingCursor = False # Using cursor for movement

        self.planetImage,self.planetRect = None,None
        self.planetStartPos,self.planetStartSize = None,None
        self.planetDelay,self.planetIndex = 0,0

        self.endlessModeStarted = False # Marks end of game reached
        self.nearObsList, self.nearMissCount = [],0

        # STORE LEVEL 1 VALUES
        self.savedConstants = {
                "maxObstacles" : self.maxObstacles,
                "wipeObstacles" : self.wipe,
                "levelType":self.levelType,
                "levelAngle":self.angle
                }

        # SET VOLUME
        if not self.musicMuted: pygame.mixer.music.set_volume(settings.musicVolume / 100)
        else: pygame.mixer.music.set_volume(0)


    # START GAME LOOP
    def start(self):
        self.resetGameConstants() # Reset level settings
        if settings.aiPlayer: player = AIPlayer(self) # Initialize player as AI
        else: player = Player(self) # Initialize player as user

        if self.mainMenu:
            self.assets.loadMenuMusic()
            pygame.mixer.music.play(-1)
            if self.musicMuted: pygame.mixer.music.set_volume(0)
            self.menu.home(self,player)

        else:
            self.assets.loadSoundtrack()
            player.getSkin(self,self.savedSkin)
            pygame.mixer.music.play()

        if self.musicMuted: pygame.mixer.music.set_volume(0)

        self.events = Event() # Initialize events
        self.events.set(player) # Events manipulate player cooldowns
        self.lasers = pygame.sprite.Group() # Laser group
        self.enemyLasers = pygame.sprite.Group() # Enemy laser group
        self.obstacles = pygame.sprite.Group() # Obstacle group
        self.collidingExplosions = pygame.sprite.Group() # Explosions with hitboxes

        # GAME LOOP
        while True: self.update(player)


    # MAIN GAME LOOP
    def update(self,player):
        for event in pygame.event.get():

            # EXIT GAME
            if event.type == pygame.QUIT: self.quitGame()

            # BACK TO MENU
            if (event.type == pygame.KEYDOWN and event.key in settings.escapeInput) or (self.gamePad is not None and self.gamePad.get_button(self.controller.controllerExit) == 1): self.menu.gameOver(self,player,self.obstacles)

            # MUTE
            if (event.type == pygame.KEYDOWN and event.key in settings.muteInput) or (self.gamePad is not None and self.gamePad.get_button(self.controller.controllerMute) == 1): self.toggleMusic()

            # PAUSE GAME
            if self.pauseCount < settings.pauseMax and ( (event.type == pygame.KEYDOWN and event.key in settings.pauseInput) or (self.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and self.gamePad.get_button(self.controller.controllerPause)==1) ):
                self.pauseCount += 1
                self.menu.pause(self,player,self.obstacles,self.lasers,self.enemyLasers)

            # INCREMENT TIMER
            if event.type == self.events.timerEvent: self.gameClock +=1

            # FUEL REPLENISH
            if event.type == self.events.fuelReplenish and player.fuel < player.maxFuel: player.fuel += player.fuelRegenNum

            # EXHAUST UPDATE
            if event.type == self.events.exhaustUpdate: player.updateExhaust(self)

            # GUN COOLDOWN
            if event.type == self.events.laserCooldown: player.laserReady = True

            # BOOST COOLDOWN
            if event.type == self.events.boostCooldown: player.boostReady = True

            # SHIELD VISUAL
            if event.type == self.events.shieldVisualDuration: player.showShield = False

            # NEAR MISS VISUAL
            if event.type == self.events.nearMissIndicator and self.nearMissCount > 0: self.nearMissCount = 0

        # BACKGROUND
        self.screen.fill(settings.screenColor)
        self.screen.blit(self.assets.bgList[self.currentStage - 1][0], (0,0) )
        self.showPlanet() # Draw planet

        # MOVE PLANET
        if self.planetDelay < settings.planetMoveDelay: self.planetDelay += 1
        else:
            self.planetRect.centery += 1
            self.planetDelay = 0

        # CLOUD ANIMATION
        if settings.showBackgroundCloud:
            cloudImg = self.assets.bgList[self.currentStage - 1][1]
            cloudRect = cloudImg.get_rect(center = (settings.screenSize[0]/2,self.cloudPos))
            if cloudRect.bottom >= 0 and cloudRect.top <= settings.screenSize[1]: self.screen.blit(cloudImg, cloudRect) # Draw cloud
            elif cloudRect.top > settings.screenSize[1]: self.cloudPos = settings.cloudStart
            self.cloudPos += self.cloudSpeed

        # SHOW POINT SPAWN AREA (Testing)
        if settings.showSpawnArea: pygame.draw.polygon(self.screen, (255, 0, 0), settings.spawnAreaPoints,1)

        # DRAW POINT
        if self.cave is None or (self.cave is not None and not self.cave.inside()): self.screen.blit(self.thisPoint.image, self.thisPoint.rect)

        # CAVES
        if "CAVE" in self.levelType or self.cave is not None:
            # LEAVING CAVE
            if self.cave is not None and self.cave.leave and self.cave.rect.top > settings.screenSize[1]:
                self.cave.kill()
                self.cave = None

            # IN CAVE
            else:
                if self.cave is None: # SPAWN A CAVE
                    self.cave = Cave(self,self.caveIndex)
                    if self.caveIndex + 1 < len(self.assets.caveList): self.caveIndex+=1
                self.cave.update()

                # DRAW CAVE
                self.screen.blit(self.cave.background,self.cave.rect)
                if self.cave.inside: self.screen.blit(self.thisPoint.image, self.thisPoint.rect) # draw point between cave layers
                self.screen.blit(self.cave.image,self.cave.rect)

                # COLLISION DETECTION
                if pygame.sprite.collide_mask(self.cave,player):
                    if player.shields > 0: player.shieldDown(self.events)
                    else:
                        player.explode(self,self.obstacles) # explosion
                        if not self.musicMuted: self.assets.explosionNoise.play()
                        self.menu.gameOver(self,player,self.obstacles) # Game over

                enemyLasersCollided = pygame.sprite.spritecollide(self.cave,self.enemyLasers,True,pygame.sprite.collide_mask) # Enemy lasers/cave
                lasersCollided = pygame.sprite.spritecollide(self.cave,self.lasers,True,pygame.sprite.collide_mask) # Lasers/cave
                for laser in lasersCollided: self.explosions.append(Explosion(self,laser,None))
                for laser in enemyLasersCollided: self.explosions.append(Explosion(self,laser,None))
                self.enemyLasers.remove(enemyLasersCollided)
                self.lasers.remove(lasersCollided)

        # HUD
        if settings.showHUD: self.showHUD(player)

        # PLAYER/POWERUP COLLISION DETECTION
        if pygame.sprite.collide_mask(player,self.thisPoint):
            if self.thisPoint.powerUp == "Fuel": # Fuel cell collected
                player.fuel += player.maxFuel/4 # Replenish quarter tank
                if player.fuel > player.maxFuel: player.fuel = player.maxFuel
                if not self.musicMuted: self.assets.powerUpNoise.play()

            elif self.thisPoint.powerUp == "Shield": # Shield piece collected
                player.shieldUp()
                if not self.musicMuted: self.assets.powerUpNoise.play()

            elif self.thisPoint.powerUp == "Coin": # Coin collected
                self.coinsCollected += 1
                self.score += 1 # Used as bonus point for now
                if not self.musicMuted: self.assets.coinNoise.play()

            elif self.thisPoint.powerUp == "Nuke":
                self.collidingExplosions.add(Explosion(self,self.thisPoint,settings.nukeSize))
                if not self.musicMuted: self.assets.explosionNoise.play()

            elif not self.musicMuted: self.assets.pointNoise.play()

            self.score += 1
            self.thisPoint.kill()
            self.lastPointPos = self.thisPoint.rect.center # Save last points position
            self.thisPoint = Point(self,player,self.lastPointPos) # spawn new point

        # UPDATE PLAYER
        player.movement(self)
        player.shoot(self,self.lasers,self.events,self.obstacles)
        player.boost(self,self.events)
        player.wrapping()
        player.updateAnimation(self)

        # ROTATE PLAYER
        newBlit = self.rotateImage(player.image,player.rect,player.angle)

        # DRAW PLAYER
        self.screen.blit(newBlit[0],newBlit[1])

        # DRAW EXHAUST/BOOST
        if settings.drawExhaust:
            if player.boosting: newBlit = self.rotateImage(self.assets.spaceShipList[self.savedShipLevel]['boost'][player.boostState],player.rect,player.angle) # Boost frames
            else: newBlit = self.rotateImage(self.assets.spaceShipList[self.savedShipLevel]['exhaust'][player.exhaustState-1],player.rect,player.angle) # Regular exhaust frames
            self.screen.blit(newBlit[0],newBlit[1])

        # DRAW SHIELD
        if player.showShield:
            shieldImg,shieldImgRect = self.rotateImage(self.assets.playerShield, player.rect, player.angle)
            self.screen.blit(shieldImg,shieldImgRect)

        # PLAYER/LASER COLLISION DETECTION
        collides = pygame.sprite.spritecollide(player,self.enemyLasers,False,pygame.sprite.collide_mask)
        for laser in collides:
            if player.shields > 0:
                player.shieldDown(self.events)
                laser.kill()
            else:
                player.explode(self,self.obstacles) # Animation
                if not self.musicMuted: self.assets.explosionNoise.play()
                self.menu.gameOver(self,player,self.obstacles) # Game over

        # DRAW LASERS
        self.laserUpdate(self.lasers,self.enemyLasers,player,self.obstacles)
        
        # OBSTACLE MOVEMENT
        self.obstacles.update(self,player)
        self.obstacles.draw(self.screen)
        
        # OBSTACLE/PLAYER COLLISION DETECTION
        if pygame.sprite.spritecollide(player,self.obstacles,False,pygame.sprite.collide_mask):
            if player.shields > 0:player.shieldDown(self.events)
            else:
                player.explode(self,self.obstacles) # Animation
                if not self.musicMuted: self.assets.explosionNoise.play()
                self.menu.gameOver(self,player,self.obstacles) # Game over

        # OBSTACLE/LASER COLLISION DETECTION
        for obs in pygame.sprite.groupcollide(self.obstacles,self.lasers,False,not player.laserCollat,pygame.sprite.collide_mask):
            if obs.health - player.damage > 0: obs.health -= player.damage
            else:
                obs.kill()
                self.obstacles.remove(obs)
                if not self.musicMuted: self.assets.impactNoise.play()
                self.explosions.append(Explosion(self,obs,None))

        # OBSTACLE/CAVE COLLISION DETECTION
        if self.cave is not None:
            for obs in pygame.sprite.spritecollide(self.cave,self.obstacles,True,pygame.sprite.collide_mask):
                if not self.musicMuted: self.assets.impactNoise.play()
                self.explosions.append(Explosion(self,obs,None))
                obs.kill()

        # OBSTACLE/EXPLOSION COLLISION DETECTION
        for obs in pygame.sprite.groupcollide(self.obstacles,self.collidingExplosions,False,False,pygame.sprite.collide_mask):
            if not self.musicMuted: self.assets.impactNoise.play()
            self.explosions.append(Explosion(self,obs,None))
            obs.kill()        

        # DRAW EXPLOSIONS
        for debris in self.explosions:
            if debris.finished: self.explosions.remove(debris)
            else: debris.update(self)

        # DRAW COLLIDING EXPLOSIONS
        for debris in self.collidingExplosions:
            if debris.finished: self.collidingExplosions.remove(debris)
            else: debris.update(self)

        if settings.nearMisses: self.nearMisses(player,self.events) # NEAR MISS CALCULATION
        if self.gameClock > self.sessionLongRun: self.sessionLongRun = self.gameClock # UPDATE HIGH SCORE
        if not self.endlessModeStarted: self.levelUpdater(player,self.obstacles,self.events) # LEVEL UP
        if "OBS" in self.levelType or self.endlessModeStarted: self.spawner(self.obstacles,player) # SPAWN OBSTACLES

        # UPDATE SCREEN
        player.lastAngle = player.angle # Save recent player orientation
        if settings.resetPlayerOrientation: player.angle = self.angle # Reset player orientation
        player.boosting = False
        if settings.showFPS: pygame.display.set_caption("Navigator {} FPS".format(int(self.clk.get_fps())))
        self.displayUpdate()


    # SET GAME CONSTANTS TO DEFAULT
    def resetGameConstants(self):
        self.maxObstacles = self.savedConstants["maxObstacles"]
        self.wipe = self.savedConstants["wipeObstacles"]
        self.levelType = self.savedConstants["levelType"]
        self.angle = self.savedConstants["levelAngle"]
        self.cloudSpeed = settings.cloudSpeed
        self.cloudPos = settings.cloudStart


    # DRAW CLOUD OUTSIDE OF MAIN LOOP
    def showBackgroundCloud(self):
        if settings.showBackgroundCloud:
            cloudImg = self.assets.bgList[self.currentStage - 1][1]
            cloudRect = cloudImg.get_rect(center = (settings.screenSize[0]/2,self.cloudPos))
            if cloudRect.bottom >= 0 and cloudRect.top <= settings.screenSize[1]: self.screen.blit(cloudImg, cloudRect) # Draw cloud


    # DRAW PLANET
    def showPlanet(self):
        if self.planetImage is not None:
            if self.planetRect.top < settings.screenSize[1]:
                self.screen.blit(self.planetImage,self.planetRect)
            else: self.getNewPlanet()


    # GET NEW PLANET
    def getNewPlanet(self):
        if self.planetIndex + 1 < len(self.assets.planets):
            self.planetIndex +=1
            self.planetImage = pygame.transform.scale(self.assets.planets[self.planetIndex],(self.planetStartSize,self.planetStartSize))
            self.planetRect = self.planetImage.get_rect()
            self.planetRect.center = (random.randint(100,settings.screenSize[0]-100),-10)

        elif settings.unlimitedPlanets:
            self.planetImage = pygame.transform.scale(self.assets.planets[random.randint(0,len(self.assets.planets)-1)],(self.planetStartSize,self.planetStartSize))
            self.planetRect = self.planetImage.get_rect()
            self.planetRect.center = (random.randint(100,settings.screenSize[0]-100),-10)


    # RESET PLANETS
    def resetPlanets(self):
        self.planetImage = pygame.transform.scale(self.assets.planets[0],(self.planetStartSize,self.planetStartSize))
        self.planetRect = self.planetImage.get_rect()
        self.planetRect.center = self.planetStartPos
        self.planetIndex = 0


    # Draw frame outside of main loop
    def alternateUpdate(self,player,obstacles,events):
        for event in pygame.event.get(): pass # Pull events

        player.updateAnimation(self)
        player.movement(self)
        player.wrapping()
        self.screen.fill(settings.screenColor)
        self.screen.blit(self.assets.bgList[self.currentStage - 1][0], (0,0) )
        self.showPlanet()
        if self.cave is not None: self.screen.blit(self.cave.background,self.cave.rect)
        self.showBackgroundCloud()
        self.cloudPos += self.cloudSpeed
        if self.cave is not None:
            self.cave.update()
            if self.cave.rect.top <= settings.screenSize[1] and self.cave.rect.bottom >= 0: self.screen.blit(self.cave.image,self.cave.rect) # DRAW CAVE

        self.obstacles.update(self,player)
        self.obstacles.draw(self.screen)

        if settings.showFPS: pygame.display.set_caption("Navigator {} FPS".format(int(self.clk.get_fps())))


    # UPDATE GAME CONSTANTS
    def levelUpdater(self,player,obstacles,events):
        # UPDATES STAGE
        if settings.oneLevel: return
        if self.currentStage < len(self.assets.stageList): # Make sure there is a next stage
            if self.gameClock == self.assets.stageList[self.currentStage][0]["startTime"]  and not self.assets.stageList[self.currentStage][0]["START"]: # Next stage's first level's activation time reached
                self.assets.stageList[self.currentStage][0]["START"] = True # Mark as activated

                if self.currentStage == len(self.assets.stageList)-1: self.endlessModeStarted = True # START OVERTIME/ENDLESS MODE

                stageUpCloud = self.assets.stageCloudImg

                if not self.endlessModeStarted: stageUpText = "STAGE UP"
                else: stageUpText = "OVERTIME"

                stageUpDisplay = self.assets.stageUpFont.render(stageUpText, True, settings.primaryFontColor)
                stageUpRect = stageUpCloud.get_rect()
                stageUpRect.center = (settings.screenSize[0]/2, settings.stageUpCloudStartPos)
                stageUp , stageWipe = True , True

                # STAGE UP ANIMATION / Removes old obstacles
                while stageUp:
                    self.alternateUpdate(player,obstacles,events)

                    for obs in obstacles:
                        if obs.rect.top <= stageUpRect.bottom: obs.kill()

                    self.screen.blit(stageUpCloud,stageUpRect) # Draw cloud
                    self.screen.blit(stageUpDisplay,(stageUpRect.centerx - settings.screenSize[0]/5, stageUpRect.centery)) # Draw "STAGE UP" text
                    if settings.showHUD: self.showHUD(player)
                    img, imgRect = self.rotateImage(player.image, player.rect, player.angle)
                    self.screen.blit(img,imgRect) # Draw player
                    stageUpRect.centery += settings.stageUpCloudSpeed

                    if stageUpRect.centery >= settings.screenSize[1]/2 and stageWipe:
                        self.currentStage += 1
                        self.currentLevel = 1
                        stageWipe = False

                    elif stageUpRect.centery >= settings.screenSize[1] * 2: stageUp = False
                    self.displayUpdate()
                    player.angle = self.angle # Update game orientation

        # UPDATES LEVEL
        for levelDict in self.assets.stageList[self.currentStage-1]:
            if self.gameClock == levelDict["startTime"] and not levelDict["START"] and ( (self.currentLevel > 1 or self.currentStage > 1) or (len(self.assets.stageList[0]) > 1 and self.gameClock >= self.assets.stageList[0][1]["startTime"]) ):
                if self.assets.stageList[self.currentStage-1][self.currentLevel-1]["wipeObstacles"]:
                    levelUpCloud = self.assets.stageCloudImg
                    levelUpRect = levelUpCloud.get_rect()
                    levelUpRect.center = (settings.screenSize[0]/2, settings.stageUpCloudStartPos)
                    levelUp = True

                    # LEVEL UP ANIMATION / Removes old obstacles
                    while levelUp:
                        self.alternateUpdate(player,obstacles,events)
                        for obs in obstacles:
                            if obs.rect.centery <= levelUpRect.centery: obs.kill()

                        self.screen.blit(levelUpCloud,levelUpRect) # Draw cloud
                        if settings.showHUD: self.showHUD(player)
                        img, imgRect = self.rotateImage(player.image, player.rect, player.angle)
                        self.screen.blit(img,imgRect) # Draw player
                        levelUpRect.centery += settings.levelUpCloudSpeed
                        if levelUpRect.top >= settings.screenSize[1]: levelUp = False
                        player.angle = self.angle
                        self.displayUpdate()

                levelDict["START"] = True
                self.maxObstacles = levelDict["maxObstacles"]
                self.wipe = levelDict["wipeObstacles"]
                self.levelType = levelDict["levelType"]
                self.angle = levelDict["levelAngle"]
                if self.cave is not None: self.cave.leave = True # Set cave for exit
                self.cloudSpeed += settings.cloudSpeedAdder
                self.currentLevel += 1
                break


    # RESET LEVEL PROGRESS
    def resetAllLevels(self):
        for stage in self.assets.stageList:
            for levels in stage: levels["START"] = False


    # REMOVE ALL OBSTACLES
    def killAllObstacles(self,obstacles):
        for obstacle in obstacles: obstacle.kill()
        obstacles.empty()


    # HUD
    def showHUD(self,player):

        # BORDER
        barBorder = pygame.Rect(settings.screenSize[0]/3, 0, (settings.screenSize[0]/3), 10)
        if player.hasShields or player.laserCost>0 or player.boostSpeed > player.baseSpeed or player.boostDrain > 0: pygame.draw.rect(self.screen,[0,0,0],barBorder)

        # SHIELDS DISPLAY
        if player.hasShields:

            if player.shields > 0:
                hasShieldRect,hasShieldRect.centerx = pygame.Rect(settings.screenSize[0]/3,5, barBorder.width*0.99, 5), barBorder.centerx
                pygame.draw.rect(self.screen,settings.fullShieldColor,hasShieldRect)
                shieldsCount = self.assets.labelFont.render(str(player.shields), True, settings.secondaryFontColor)
                shieldsCountRect = shieldsCount.get_rect(center = (barBorder.right + 5, barBorder.center[1] + 5))
                self.screen.blit(self.assets.shieldIcon,(shieldsCountRect.centerx + 2, shieldsCountRect.centery - 10))
                self.screen.blit(shieldsCount,shieldsCountRect)

            if player.shieldPieces > 0:
                currentShieldPieces = player.shieldPieces/player.shieldPiecesNeeded
                shieldRectWidth = (0.9*barBorder.width) * currentShieldPieces
                shieldRect = pygame.Rect(settings.screenSize[0]/3, 5, shieldRectWidth, 5)
                shieldRect.centerx = barBorder.centerx
                pygame.draw.rect(self.screen,settings.shieldColor,shieldRect)


        # FUEL DISPLAY
        if player.boostDrain > 0 or player.laserCost > 0:
            currentFuel = player.fuel/player.maxFuel
            fuelRectWidth = currentFuel * (0.99*barBorder.width)
            fuelRect = pygame.Rect(settings.screenSize[0]/3, 0, fuelRectWidth, 5)
            if player.hasShields:fuelRect.centerx = barBorder.centerx
            else: fuelRect.center = barBorder.center
            pygame.draw.rect(self.screen, settings.fuelColor,fuelRect)

        # TIMER DISPLAY
        timerDisplay = self.assets.mediumFont.render(str(self.gameClock), True, settings.secondaryFontColor)
        timerRect = timerDisplay.get_rect(topright = self.screen.get_rect().topright)

        # STAGE DISPLAY
        if not self.endlessModeStarted: stageNum = "Stage " + str(self.currentStage)
        else: stageNum = "Overtime"
        stageDisplay = self.assets.mediumFont.render( str(stageNum), True, settings.secondaryFontColor )
        stageRect = stageDisplay.get_rect(topleft = self.screen.get_rect().topleft)

        # LEVEL DISPLAY
        if not self.endlessModeStarted: levelNum = "-  Level " + str(self.currentLevel)
        else: levelNum = ""
        levelDisplay = self.assets.mediumFont.render( str(levelNum), True, settings.secondaryFontColor )
        levelRect = levelDisplay.get_rect()
        levelRect.center = (stageRect.right + levelRect.width*0.65, stageRect.centery)

        # SCORE DISPLAY
        scoreNum = "Score " + str(self.score)
        scoreDisplay = self.assets.mediumFont.render(scoreNum, True, settings.secondaryFontColor)
        scoreRect = scoreDisplay.get_rect()
        scoreRect.topleft = (settings.screenSize[0] - (2*scoreRect.width), levelRect.y)

        # NEAR MISSES DISPLAY
        if settings.nearMisses and self.nearMissCount > 0:
            if self.nearMissCount >1: nearMissText = "Near Miss! x" + str(self.nearMissCount)
            else: nearMissText = "Near Miss!"
            nearMissDisplay = self.assets.labelFont.render(nearMissText, True, settings.secondaryFontColor)
            nearMissRect = nearMissDisplay.get_rect(center = (scoreRect.midbottom[0],scoreRect.bottom + 5))
            self.screen.blit(nearMissDisplay,nearMissRect)

        self.screen.blit(timerDisplay, timerRect)
        self.screen.blit(stageDisplay, stageRect)
        if not self.endlessModeStarted: self.screen.blit(levelDisplay, levelRect)
        self.screen.blit(scoreDisplay, scoreRect)


    # SPAWN OBSTACLES
    def spawner(self,obstacles,player):
        if len(obstacles) < self.maxObstacles:
            if not self.endlessModeStarted: obstacle = Obstacle(self,[player.rect.centerx,player.rect.centery])
            else:
                attributes = {
                    "size" : random.randint(20,60),
                    "speed" : random.randint(5,10)
                }
                obstacle = Obstacle(self,[player.rect.centerx,player.rect.centery], size = attributes['size'], speed = attributes["speed"])
            obstacles.add(obstacle)


    # Update all lasers
    def laserUpdate(self,lasers,enemyLasers,player,obstacles):
        lasers.update(self,player,obstacles)
        enemyLasers.update(self,player)
        for laser in lasers: self.screen.blit(laser.image,laser.rect)
        for laser in enemyLasers: self.screen.blit(laser.image,laser.rect)


    # CALCULATE NEAR MISSES
    def nearMisses(self,player,events):
        for near in self.nearObsList:
            if math.dist(player.rect.center,near.rect.center) > settings.nearMissSafeDist:
                self.nearObsList.remove(near)
                self.nearMissCount += 1
                self.score += settings.nearMissValue
                events.nearMiss()


    # RESTART GAME
    def reset(self,player,obstacles):
        self.gameClock = settings.gameStartTime
        self.currentLevel = 1
        self.currentStage = 1
        self.endlessModeStarted = False
        self.score = 0
        self.pauseCount = 0
        self.explosions = []
        self.coinsCollected = 0
        self.attemptNumber += 1
        self.nearObsList,self.nearMissCount = [],0
        self.resetPlanets()
        self.cave = None
        self.killAllObstacles(obstacles)
        self.resetAllLevels()
        self.assets.loadSoundtrack()
        pygame.mixer.music.play()
        if self.musicMuted: pygame.mixer.music.set_volume(0)
        player.kill()



    # MOVEMENT AND POSITION GENERATION
    def getMovement(self,spawnPattern):
        top,bottom,left,right = [],[],[],[]
        if spawnPattern == "TOP": top = [45, 135, 90] # Top to bottom
        elif spawnPattern == "BOTTOM": bottom = [270,315,225] # Bottom to top
        elif spawnPattern == "LEFT":left = [0,315,45] # Left to right
        elif spawnPattern == "RIGHT":right = [180,225,135] # Right to left
        elif spawnPattern == "VERT": top, bottom = [45, 135, 90], [270, 315, 225]
        elif spawnPattern == "HORI": left, right = [0,315,45], [180,225,135]
        elif spawnPattern == "DIAG": top, bottom, left, right = [45, 135], [315, 225], [315, 45], [225, 135]
        else: top, bottom, left, right = [45, 135, 90], [270, 315, 225], [0, 315, 45], [225, 135,180]

        X = random.randint(int(settings.screenSize[0] * 0.02), int(settings.screenSize[0] * 0.98))
        Y = random.randint(int(settings.screenSize[1] * 0.02), int(settings.screenSize[1] * 0.98))

        lowerX = random.randint(-1,0)
        upperX = random.randint(settings.screenSize[0], settings.screenSize[0] + 1)
        lowerY = random.randint(-1,0)
        upperY = random.randint(settings.screenSize[1],settings.screenSize[1] + 1)

        possible = []
        if len(top) != 0: possible.append([X, lowerY, random.choice(top)])
        if len(bottom) != 0: possible.append([X, upperY, random.choice(bottom)])
        if len(left) != 0: possible.append([lowerX, Y, random.choice(left)])
        if len(right) != 0: possible.append([upperX, Y, random.choice(right)])

        movement = random.choice(possible)
        return [[movement[0], movement[1]],math.radians(movement[2])]


    # GET SCREEN
    def getScreen(self):
        if settings.fullScreen: return pygame.display.set_mode(settings.screenSize,pygame.FULLSCREEN | pygame.SCALED, depth = 0)
        else: return pygame.display.set_mode(settings.screenSize, pygame.SCALED, depth = 0)


    # TOGGLE FULLSCREEN
    def toggleScreen(self):
        pygame.display.toggle_fullscreen()
        settings.fullScreen = not settings.fullScreen
        if settings.fullScreen: settings.debug("Fullscreen toggled on")
        else: settings.debug("Fullscreen toggled off")


    # TOGGLE MUSIC MUTE
    def toggleMusic(self):
        self.musicMuted = not self.musicMuted
        if pygame.mixer.music.get_volume() == 0: pygame.mixer.music.set_volume(settings.musicVolume/100)
        else: pygame.mixer.music.set_volume(0)


    # UPDATE DISPLAY
    def displayUpdate(self):
        pygame.display.update()
        if self.clk is not None: self.clk.tick(settings.fps)


    # ROTATE IMAGES
    def rotateImage(self,image, rect, angle):
        rotated = pygame.transform.rotate(image, angle)
        rotatedRect = rotated.get_rect(center=rect.center)
        return rotated,rotatedRect


    # KEEP CURSOR ON SCREEN (Cursor mode only)
    def resetCursor(self):
        if settings.cursorMode:
            pos = list(pygame.mouse.get_pos())
            if pos[0] <= 1: pygame.mouse.set_pos(5,pos[1])
            if pos[0] >= settings.screenSize[0]-2: pygame.mouse.set_pos(settings.screenSize[0]-5,pos[1])
            if pos[1] <= 1: pygame.mouse.set_pos(pos[0],5)
            if pos[1] >= settings.screenSize[1]-1: pygame.mouse.set_pos(pos[0],settings.screenSize[1]-5)

    # QUIT GAME
    def quitGame(self):
        pygame.quit() # UNINITIALIZE PYGAME
        Leaderboard.uploadRecords(self.records,self.assets.userName) # UPLOAD TO LEADERBOARD
        sys.exit() # EXIT NAVIGATOR


