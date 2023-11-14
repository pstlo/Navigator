import pygame,math
import Settings as settings
from Lasers import Laser

# PLAYER
class Player(pygame.sprite.Sprite):
        def __init__(self,game):
            super().__init__()

            # GET DEFAULT SHIP CONSTANTS
            self.currentImageNum = 0
            self.speed,self.baseSpeed,self.boostSpeed = game.assets.spaceShipList[game.savedShipLevel]['stats']["speed"],game.assets.spaceShipList[game.savedShipLevel]['stats']["speed"],game.assets.spaceShipList[game.savedShipLevel]['stats']["boostSpeed"]
            self.image = game.assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]
            self.laserImage = game.assets.spaceShipList[game.savedShipLevel]['laser']
            self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.fuel, self.maxFuel = game.assets.spaceShipList[game.savedShipLevel]['stats']["startingFuel"], game.assets.spaceShipList[game.savedShipLevel]['stats']["maxFuel"]
            self.angle, self.lastAngle = 0, 0
            self.exhaustState, self.boostState, self.explosionState = 0, 0, 0 # Indexes of animation frames
            self.finalImg, self.finalRect = '','' # Last frame of exhaust animation for boost
            self.fuelRegenNum = game.assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegen"]
            self.fuelRegenDelay = game.assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegenDelay"]
            self.boostDrain = game.assets.spaceShipList[game.savedShipLevel]['stats']["boostDrain"]
            self.laserCost = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserCost"]
            self.laserSpeed = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserSpeed"]
            self.laserFireRate = game.assets.spaceShipList[game.savedShipLevel]['stats']["fireRate"]
            self.laserCollat = game.assets.spaceShipList[game.savedShipLevel]['stats']["collats"]
            self.hasGuns, self.laserReady, self.boostReady = game.assets.spaceShipList[game.savedShipLevel]['stats']["hasGuns"], True, True
            self.hasShields = game.assets.spaceShipList[game.savedShipLevel]['stats']["hasShields"]
            self.shields = game.assets.spaceShipList[game.savedShipLevel]['stats']["startingShields"]
            self.shieldPieces = game.assets.spaceShipList[game.savedShipLevel]['stats']["startingShieldPieces"]
            self.shieldPiecesNeeded = game.assets.spaceShipList[game.savedShipLevel]['stats']["shieldPiecesNeeded"]
            self.damage = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserDamage"]
            self.laserType = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserType"]
            self.showShield,self.boosting = False,False
            if settings.cursorMode: self.lastCursor = pygame.Vector2(0,0)
            self.animated,self.skinAnimationCount,self.skinAnimationFrame,self.skinAnimationFrames = False, 0, 0, 0


        # VECTOR BASED MOVEMENT
        def movement(self,game):
            # KEYBOARD
            if not game.usingController and not game.usingCursor:
                key = pygame.key.get_pressed()
                direction = pygame.Vector2(0, 0) # Get new vector
                if any(key[bind] for bind in settings.upInput): direction += pygame.Vector2(0, -1)
                if any(key[bind] for bind in settings.downInput): direction += pygame.Vector2(0, 1)
                if any(key[bind] for bind in settings.leftInput): direction += pygame.Vector2(-1, 0)
                if any(key[bind] for bind in settings.rightInput): direction += pygame.Vector2(1, 0)
                if direction.length() > 0: direction.normalize_ip()
                if not any(key[bind] for bind in settings.brakeInput): self.rect.move_ip((math.sqrt(2)*direction) * self.speed) # MOVE PLAYER
                if direction.x != 0 or direction.y != 0: self.angle = direction.angle_to(pygame.Vector2(0, -1)) # GET PLAYER ANGLE

            # CONTROLLER
            elif game.gamePad is not None and game.usingController:
                direction = pygame.Vector2(0, 0) # Get new vector
                xLeft,yLeft,xRight,yRight = game.gamePad.get_axis(self.controller.controllerMoveX),game.gamePad.get_axis(self.controller.controllerMoveY),game.gamePad.get_axis(self.controller.controllerRotateX),game.gamePad.get_axis(self.controller.controllerRotateY)
                if abs(xRight) > 0.3 or abs(yRight) > 0.3: xTilt, yTilt, braking = xRight, yRight, True
                else: xTilt, yTilt, braking = xLeft, yLeft, False
                if yTilt < -0.3: direction += pygame.Vector2(0, -1)
                if yTilt > 0.3: direction += pygame.Vector2(0, 1)
                if xTilt < -0.3: direction += pygame.Vector2(-1, 0)
                if xTilt > 0.3: direction += pygame.Vector2(1, 0)
                if direction.length() > 1: direction.normalize_ip()
                if not braking: self.rect.move_ip((math.sqrt(2)*direction) * self.speed) # MOVE PLAYER
                if direction.x != 0 or direction.y != 0:self.angle = direction.angle_to(pygame.Vector2(0, -1)) # GET PLAYER ANGLE

            # CURSOR BASED MOVEMENT
            elif game.usingCursor:
                game.resetCursor()
                # RAW CURSOR MODE
                if settings.rawCursorMode:
                    cursor = pygame.Vector2(pygame.mouse.get_pos())
                    self.rect.center = cursor
                    if pygame.Vector2.distance_to(cursor, self.lastCursor) > 0.5: self.angle = (cursor - self.lastCursor).angle_to(pygame.Vector2(1, 0))-90
                    self.lastCursor = cursor

                else:
                    # CURSOR MODE
                    cursorDeadzone = [0.2,0.8]
                    cursorX, cursorY = pygame.mouse.get_pos()
                    if settings.showCursorPath: pygame.draw.aaline(game.screen,(0,255,0),(cursorX,cursorY),self.rect.center)
                    cursorDirection = pygame.Vector2(cursorX, cursorY)
                    if math.dist(self.rect.midtop,(cursorX,cursorY)) > settings.cursorRotateDistance:
                        direction = cursorDirection - pygame.Vector2(self.rect.centerx, self.rect.centery)
                        if direction.length() > 0: direction.normalize_ip()

                        self.angle = direction.angle_to(pygame.Vector2(0, -1))
                        if math.dist(self.rect.center,(cursorX,cursorY)) >= settings.cursorFollowDistance:
                            # Auto align
                            if direction.x >= cursorDeadzone[1] and direction.x <= 1: direction.x  = 1
                            elif direction.x <= -cursorDeadzone[1] and direction.x >= -1: direction.x = -1
                            elif (direction.x <= cursorDeadzone[0] and direction.x >= 0) or (direction.x >= -cursorDeadzone[0] and direction.x <= 0): direction.x = 0

                            if direction.y >= cursorDeadzone[1] and direction.y <= 1: direction.y  = 1
                            elif direction.y <= -cursorDeadzone[1] and direction.y >= -1: direction.y = -1
                            elif (direction.y <= cursorDeadzone[0] and direction.y >= 0) or (direction.y >= -cursorDeadzone[0] and direction.y <= 0): direction.y = 0

                            self.rect.move_ip((1.414*direction) * self.speed) # MOVE PLAYER


        # SPEED BOOST
        def boost(self,game,events):
            if self.boostReady:
                if self.fuel - self.boostDrain > self.boostDrain:
                    # KEYBOARD
                    if (game.gamePad is None or not game.usingController) and (not game.usingCursor):
                        key = pygame.key.get_pressed()
                        if (any(key[bind] for bind in settings.brakeInput)) or (any(key[bind] for bind in settings.boostInput) and ( any(key[bind] for bind in settings.leftInput) and  any(key[bind] for bind in settings.upInput) and any(key[bind] for bind in settings.downInput) and any(key[bind] for bind in settings.rightInput) )):
                            return # Cannot boost with all directional inputs held together

                        elif any(key[bind] for bind in settings.boostInput) and ( any(key[bind] for bind in settings.leftInput) or any(key[bind] for bind in settings.upInput) or any(key[bind] for bind in settings.downInput) or any(key[bind] for bind in settings.rightInput)):
                            self.speed = self.boostSpeed
                            self.fuel -= self.boostDrain
                            if not self.boosting: self.boosting = True
                            if self.boostState + 1 < len(game.assets.spaceShipList[game.savedShipLevel]['boost']): self.boostState += 1
                            else: self.boostState = 0

                        else: self.speed = self.baseSpeed

                    # CONTROLLER
                    elif game.usingController and not game.usingCursor:
                        xTilt,yTilt = game.gamePad.get_axis(self.controller.controllerMoveX),game.gamePad.get_axis(self.controller.controllerMoveY)
                        xRot,yRot = game.gamePad.get_axis(self.controller.controllerRotateX),game.gamePad.get_axis(self.controller.controllerRotateY)
                        if (abs(xRot) > 0.1 and abs(yRot) > 0.1) or (abs(xTilt) <= 0.1 and abs(yTilt) <= 0.1): pass # Cannot boost in place
                        elif (abs(xTilt) > 0.1 or abs(yTilt)) > 0.1 and game.gamePad.get_axis(self.controller.controllerBoost) > 0.5:
                            self.speed = self.boostSpeed
                            self.fuel -= self.boostDrain
                            if not self.boosting: self.boosting = True
                            if self.boostState + 1 < len(game.assets.spaceShipList[game.savedShipLevel]['boost']): self.boostState += 1
                            else: self.boostState = 0

                        else: self.speed = self.baseSpeed

                    elif game.usingCursor:
                        button = pygame.mouse.get_pressed()
                        pygame.mouse.get_pos()
                        if math.dist(self.rect.center,pygame.mouse.get_pos()) >= settings.cursorFollowDistance and pygame.mouse.get_pressed()[2] == 1:
                            self.speed = self.boostSpeed
                            self.fuel -= self.boostDrain
                            if not self.boosting: self.boosting = True
                            if self.boostState + 1 < len(game.assets.spaceShipList[game.savedShipLevel]['boost']): self.boostState += 1
                            else: self.boostState = 0

                        else: self.speed = self.baseSpeed

                else:
                    if self.speed != self.baseSpeed: self.speed = self.baseSpeed
                    if self.boosting: self.boosting = False
                    events.boostCharge(self)


        # SHOOT ROCKETS/LASERS
        def shoot(self,game,lasers,events,obstacles):
            if self.hasGuns and self.laserReady:

                # KEYBOARD
                if (game.gamePad is None or not game.usingController) and (not game.usingCursor):
                    key = pygame.key.get_pressed()
                    if any(key[bind] for bind in settings.shootInput) and self.fuel - self.laserCost > 0:
                        lasers.add(Laser(game,self))
                        if not game.musicMuted: game.assets.laserNoise.play()
                        self.fuel -= self.laserCost
                        events.laserCharge(self)

                # CONTROLLER
                elif game.usingController and not game.usingCursor:
                    if game.gamePad.get_axis(self.controller.controllerShoot) > 0.5 and self.fuel - self.laserCost > 0:
                        lasers.add(Laser(game,self))
                        if not game.musicMuted: game.assets.laserNoise.play()
                        self.fuel -= self.laserCost
                        events.laserCharge(self)

                # CURSOR
                elif game.usingCursor:
                    if pygame.mouse.get_pressed()[0]== 1 and self.fuel - self.laserCost > 0:
                        lasers.add(Laser(game,self))
                        if not game.musicMuted: game.assets.laserNoise.play()
                        self.fuel -= self.laserCost
                        events.laserCharge(self)


        # WRAP AROUND SCREEN
        def wrapping(self):
            if self.rect.centery > settings.screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = settings.screenSize[1]
            if self.rect.centerx > settings.screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = settings.screenSize[0]


        # SWITCH SHIP SKIN
        def toggleSkin(self,game,toggleDirection):
            if toggleDirection: # Next skin
                if not settings.devMode:
                    skin = game.unlocks.nextUnlockedSkin(game.savedShipLevel,self.currentImageNum)
                    if skin is not None: self.getSkin(game,skin)
                    elif skin != self.currentImageNum: self.getSkin(game,0) # Wrap to first skin
                else:
                    if self.currentImageNum +1 < len(game.assets.spaceShipList[game.savedShipLevel]['skins']): self.getSkin(game,self.currentImageNum+1)
                    elif len(game.assets.spaceShipList[game.savedShipLevel]['skins'])-1 != 0: self.getSkin(game,0)
            else: # Last skin
                if self.currentImageNum >= 1:
                    if not settings.devMode: skin = game.unlocks.lastUnlockedSkin(game.savedShipLevel,self.currentImageNum) # previous skin
                    else: skin = self.currentImageNum - 1
                else: # Wrap to last skin
                    if not settings.devMode: skin = game.unlocks.highestSkin(game.savedShipLevel)
                    else: skin = len(game.assets.spaceShipList[game.savedShipLevel]['skins'])-1
                if skin is not None: self.getSkin(game,skin)


        # SWITCH TO SPECIFIC SKIN
        def getSkin(self,game,skinNum):
            if game.assets.spaceShipList[game.savedShipLevel]['skins'][skinNum] or settings.devMode:
                self.currentImageNum = skinNum
                skinImage = game.assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]

                # Animated skin
                if type(skinImage) == list:
                    self.image = skinImage[0]
                    self.skinAnimationFrame, self.skinAnimationFrames = 0, len(game.assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]) - 1
                    if not self.animated: self.animated = True # Set flag
                # Static skin
                else:
                    self.image = skinImage
                    if self.animated: self.animated = False
                self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
                self.mask = pygame.mask.from_surface(self.image)


        # SWITCH SHIP TYPE
        def toggleSpaceShip(self,game,toggleDirection): # toggleDirection == True -> next ship / False -> last ship
            if toggleDirection:
                if not settings.devMode:
                    ship = game.unlocks.nextUnlockedShip(game.savedShipLevel)
                    if ship is not None: self.getShip(game,ship)
                    elif game.savedShipLevel != 0: self.getShip(game,0)
                else:
                    if game.savedShipLevel +1 < len(game.assets.spaceShipList): self.getShip(game,game.savedShipLevel+1) # get next ship
                    elif game.savedShipLevel != 0: self.getShip(game,0) # Wrap to first ship
            else:
                if not settings.devMode:
                    ship = game.unlocks.lastUnlockedShip(game.savedShipLevel)
                    if ship is not None: self.getShip(game,ship)
                    elif ship != game.savedShipLevel: self.getShip(game,game.unlocks.highestShip()) # Wrap to first ship
                else:
                    if game.savedShipLevel >= 1: self.getShip(game,game.savedShipLevel-1)
                    else: self.getShip(game,len(game.assets.spaceShipList)-1) # Wrap to last ship


        # SWITCH TO SPECIFIC SHIP TYPE
        def getShip(self,game,shipNum):
            if len(game.assets.spaceShipList) >= shipNum:
                if game.unlocks.hasShipUnlock() or settings.devMode:
                    if game.unlocks.ships[shipNum][0] or settings.devMode:
                        game.savedShipLevel = shipNum
                        self.updatePlayerConstants(game)
                        self.getSkin(game,0)


        # Update player attributes
        def updatePlayerConstants(self,game):
            self.image = game.assets.spaceShipList[game.savedShipLevel]['skins'][0]
            self.laserImage = game.assets.spaceShipList[game.savedShipLevel]['laser']
            self.currentImageNum = 0
            self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.speed,self.baseSpeed = game.assets.spaceShipList[game.savedShipLevel]['stats']["speed"],game.assets.spaceShipList[game.savedShipLevel]['stats']["speed"]
            self.fuel = game.assets.spaceShipList[game.savedShipLevel]['stats']["startingFuel"]
            self.maxFuel = game.assets.spaceShipList[game.savedShipLevel]['stats']["maxFuel"]
            self.fuelRegenNum = game.assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegen"]
            self.fuelRegenDelay = game.assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegenDelay"]
            self.boostSpeed = game.assets.spaceShipList[game.savedShipLevel]['stats']["boostSpeed"]
            self.boostDrain = game.assets.spaceShipList[game.savedShipLevel]['stats']["boostDrain"]
            self.laserCost = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserCost"]
            self.laserSpeed = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserSpeed"]
            self.laserFireRate = game.assets.spaceShipList[game.savedShipLevel]['stats']["fireRate"]
            self.hasGuns = game.assets.spaceShipList[game.savedShipLevel]['stats']["hasGuns"]
            self.laserCollat = game.assets.spaceShipList[game.savedShipLevel]['stats']["collats"]
            self.hasShields = game.assets.spaceShipList[game.savedShipLevel]['stats']["hasShields"]
            self.shields = game.assets.spaceShipList[game.savedShipLevel]['stats']["startingShields"]
            self.shieldPieces = game.assets.spaceShipList[game.savedShipLevel]['stats']["startingShieldPieces"]
            self.shieldPiecesNeeded = game.assets.spaceShipList[game.savedShipLevel]['stats']["shieldPiecesNeeded"]
            self.damage = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserDamage"]
            self.laserType = game.assets.spaceShipList[game.savedShipLevel]['stats']["laserType"]


        # ROCKET EXHAUST ANIMATION
        def updateExhaust(self,game):
            if self.exhaustState+1 > len(game.assets.spaceShipList[game.savedShipLevel]['exhaust']): self.exhaustState = 0
            else: self.exhaustState += 1


        # SKIN ANIMATION
        def updateAnimation(self,game):
            if self.animated:
                if self.skinAnimationCount >= settings.skinAnimationDelay:
                    if self.skinAnimationFrame + 1 > self.skinAnimationFrames: self.skinAnimationFrame = 0
                    else: self.skinAnimationFrame += 1
                    self.image = game.assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum][self.skinAnimationFrame]
                    self.skinAnimationCount = 0
                self.skinAnimationCount += 1


        # PLAYER EXPLOSION ANIMATION
        def explode(self,game,obstacles):
            while self.explosionState < len(game.assets.explosionList):
                height = game.assets.explosionList[self.explosionState].get_height()
                width = game.assets.explosionList[self.explosionState].get_width()
                game.screen.fill(settings.screenColor)
                game.screen.blit(game.assets.bgList[game.currentStage - 1][0], (0,0) )
                game.showPlanet()
                game.showBackgroundCloud()
                if game.cave is not None:
                    game.screen.blit(game.cave.background,game.cave.rect)
                    game.screen.blit(game.cave.image,game.cave.rect) # Draw cave

                # Draw obstacles during explosion
                for obs in obstacles:
                    obs.move(game,self,None)
                    obs.activate()
                    newBlit = game.rotateImage(obs.image,obs.rect,obs.angle)
                    game.screen.blit(newBlit[0],newBlit[1])

                img = pygame.transform.scale(game.assets.explosionList[self.explosionState], (height * self.explosionState, width * self.explosionState)) # Blow up explosion
                img, imgRect = game.rotateImage(img, self.rect, self.lastAngle) # Rotate
                game.screen.blit(img,imgRect) # Draw explosion
                game.screen.blit(game.assets.explosionList[self.explosionState],self.rect)
                self.explosionState += 1
                self.finalImg,self.finalRect = img,imgRect # Explosion effect on game over screen
                game.displayUpdate()


        # GAIN SHIELD
        def shieldUp(self):
            self.shieldPieces += 1
            if self.shieldPieces >= self.shieldPiecesNeeded:
                self.shieldPieces = 0
                self.shields += 1


        # LOSE SHIELD
        def shieldDown(self,events):
            self.shields -= 1
            self.showShield = True
            events.showShield()


