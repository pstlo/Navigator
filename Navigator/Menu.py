import pygame,random,math
import Settings as settings
from Explosion import Explosion
from Point import Point
import Leaderboard


# MENUS
class Menu:
    # LOGO SCREEN
    def logoScreen(self,game):
        game.showLogoScreen = False
        game.screen.blit(game.assets.bgList[game.currentStage - 1][0],(0,0))
        logoRect = game.assets.mainLogo.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
        game.screen.blit(game.assets.mainLogo,logoRect)

        startText = game.assets.mediumFont.render("PRESS ANY BUTTON", True, settings.primaryFontColor)
        startTextRect = startText.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1] * 0.9))
        game.screen.blit(startText,startTextRect)
        game.displayUpdate()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: game.quitGame()
                if (event.type == pygame.KEYDOWN) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerSelect) == 1) or (event.type == pygame.MOUSEBUTTONDOWN): return


    # START MENU
    def home(self,game,player):

        if game.showLogoScreen: self.logoScreen(game)

        # TITLE TEXT
        startRect = game.assets.titleText.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/3 +30))

        # Foreground icons
        fgIcons = []

        for icon in range(settings.maxFgIcons): fgIcons.append(Icon(game,"FG"))

        # Background icons
        bgIcons = []
        for bgIcon in range(settings.maxBgIcons): bgIcons.append(Icon(game,"BG"))

        # Colliding icons
        cgIcons = []
        for cgIcon in range(settings.maxCgIcons): cgIcons.append(Icon(game,"CG"))

        # PLANET
        planet = pygame.sprite.Sprite()
        planet.image = game.assets.planets[0]
        planet.rect = planet.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/3 +50))
        planet.mask = pygame.mask.from_surface(planet.image)
        planetSize = planet.rect.size[0]

        # HELP CONTEXT
        if not game.usingController or game.gamePad is None:
            startDisplays = self.getHelpLabels(game,False)
            controlDisplays = self.getControlLabels(game,player,False)

        else:
            startDisplays = self.getHelpLabels(game,True)
            controlDisplays = self.getControlLabels(game,player,True)

        versionDisplay = game.assets.versionFont.render(game.version,True,settings.primaryFontColor)
        versionRect = versionDisplay.get_rect(center = (startRect.right - 45,startRect.bottom-100))

        # Coin Display
        coinDisplay = game.assets.mediumFont.render(str(game.records['coins']), True, settings.secondaryFontColor)
        coinDisplayRect = coinDisplay.get_rect(center = (settings.screenSize[0] -25, 25))
        coinIconRect = game.assets.coinIcon.get_rect(center = (settings.screenSize[0] -60, 25))

        try:
            game.unlocks.update(game) # GET NEW UNLOCKS
            settings.debug("Refreshed unlocks") # Debug
        except:
            settings.debug("Version incompatibility detected") # Debug
            game.records['unlocks'] = game.assets.getDefaultUnlocks()
            game.assets.storeRecords(game.records)
            game.unlocks.update(game)
            settings.debug("Updated successfully") # Debug

        if settings.defaultToHighShip:
            if game.unlocks.hasShipUnlock(): player.getShip(game.unlocks.highestShip()) # Gets highest unlocked ship by default

        if settings.defaultToHighSkin and not game.skipAutoSkinSelect: player.getSkin(game,game.unlocks.highestSkin(game.savedShipLevel)) # Gets highest unlocked skin by default
        elif game.skipAutoSkinSelect: player.getSkin(game,game.savedSkin)

        shipAttributes = self.shipStatsDisplay(game) # Ship stats display
        iconPosition = 100 # Icon position at game start (offset from original)

        while game.mainMenu:
            for event in pygame.event.get():
                # START
                if (event.type == pygame.KEYDOWN and event.key in settings.startInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerSelect) == 1) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1):
                    if (event.type == pygame.KEYDOWN and event.key in settings.startInput):
                        game.usingCursor, game.usingController = False, False
                        pygame.mouse.set_visible(False)

                    elif (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerSelect) == 1):
                        game.usingController,game.usingCursor = True,False
                        pygame.mouse.set_visible(False)

                    elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1):
                        game.usingCursor, game.usingController = True, False
                        pygame.mouse.set_visible(not settings.rawCursorMode)

                    game.savedSkin = player.currentImageNum

                    while iconPosition > 0:
                        if planetSize-25 > 0:
                            planetSize -= 25
                            planet.rect.centery -= 10
                        planet.image = pygame.transform.scale(game.assets.planets[game.planetIndex],(planetSize,planetSize))
                        planet.rect = planet.image.get_rect(center = planet.rect.center)

                        # Start animation
                        game.screen.fill(settings.screenColor)
                        game.screen.blit(game.assets.bgList[game.currentStage - 1][0],(0,0))
                        game.screen.blit(planet.image,planet.rect)
                        game.screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Current spaceship
                        game.displayUpdate()
                        iconPosition -= (player.speed+1)

                    game.planetImage = planet.image
                    game.planetRect = planet.rect
                    game.planetStartPos = planet.rect.center
                    game.planetStartSize = planet.rect.size[0]

                    game.explosions.clear()
                    game.mainMenu = False
                    game.assets.loadSoundtrack()
                    pygame.mixer.music.play()
                    return

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in settings.fullScreenInput) or (game.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and game.gamePad.get_button(game.controller.controllerFullScreen) == 1):
                    game.toggleScreen()

                # NEXT SPACESHIP SKIN
                if (event.type == pygame.KEYDOWN and event.key in settings.rightInput) or (game.gamePad is not None and (game.gamePad.get_numhats() > 0 and (game.gamePad.get_hat(0) == game.controller.controllerNextSkin) or (event.type == pygame.JOYBUTTONDOWN and type(game.controller.controllerNextSkin) == int and game.gamePad.get_button(game.controller.ontrollerNextSkin)==1))):
                    player.toggleSkin(game,True)

                # PREVIOUS SPACESHIP SKIN
                elif (event.type == pygame.KEYDOWN and event.key in settings.leftInput) or (game.gamePad is not None and (game.gamePad.get_numhats() > 0 and (game.gamePad.get_hat(0) == game.controller.controllerLastSkin) or (event.type == pygame.JOYBUTTONDOWN and type(game.controller.controllerLastSkin) == int and game.gamePad.get_button(game.controller.controllerLastSkin)==1))):
                    player.toggleSkin(game,False)

                # NEXT SHIP TYPE
                if (event.type == pygame.KEYDOWN and event.key in settings.upInput) or (game.gamePad is not None and (game.gamePad.get_numhats() > 0 and (game.gamePad.get_hat(0) == game.controller.controllerNextShip) or (event.type == pygame.JOYBUTTONDOWN and type(game.controller.controllerNextShip) == int and game.gamePad.get_button(game.controller.controllerNextShip)==1))):
                    player.toggleSpaceShip(game,True)
                    shipAttributes = self.shipStatsDisplay(game)
                    controlDisplays = self.getControlLabels(game,player,game.usingController)

                # PREVIOUS SHIP TYPE
                elif (event.type == pygame.KEYDOWN and event.key in settings.downInput) or (game.gamePad is not None and (game.gamePad.get_numhats() > 0 and (game.gamePad.get_hat(0) == game.controller.controllerLastShip) or (event.type == pygame.JOYBUTTONDOWN and type(game.controller.controllerLastShip) == int and game.gamePad.get_button(game.controller.controllerLastShip)==1))):
                    player.toggleSpaceShip(game,False)
                    shipAttributes = self.shipStatsDisplay(game)
                    controlDisplays = self.getControlLabels(game,player,game.usingController)

                # EXIT
                if (event.type == pygame.KEYDOWN and event.key in settings.escapeInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerExit) == 1) or event.type == pygame.QUIT: game.quitGame()

                # MUTE
                if (event.type == pygame.KEYDOWN) and (event.key in settings.muteInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerMute) == 1): game.toggleMusic()

                # LEADERBOARD
                if (event.type == pygame.KEYDOWN) and (event.key in settings.leadersInput):
                    self.leaderboard(game)
                    if not settings.connectToLeaderboard: startDisplays = self.getHelpLabels(game,game.usingController) # Disable leaderboard keybind display if unable to connect

                # CREDITS
                if (event.type == pygame.KEYDOWN and event.key in settings.creditsInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerCredits) == 1): self.creditScreen(game)

                # HANGER
                if event.type == pygame.KEYDOWN and event.key in settings.hangerInput: self.hanger(game,player,game.unlocks)

                # SWITCH CONTROL TYPE
                if game.usingController and event.type == pygame.KEYDOWN:
                    startDisplays = self.getHelpLabels(game,False)
                    controlDisplays = self.getControlLabels(game,player,False)
                    game.usingController = False

                elif game.gamePad is not None and not game.usingController and (event.type == pygame.JOYHATMOTION or event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONUP):
                    startDisplays = self.getHelpLabels(game,True)
                    controlDisplays = self.getControlLabels(game,player,True)
                    game.usingController = True

            game.screen.fill(settings.screenColor)
            game.screen.blit(game.assets.bgList[game.currentStage - 1][0],(0,0)) # Background

            # Background icons
            if settings.showMenuIcons:
                for icon in bgIcons:
                    icon.move(game)
                    icon.draw(game)

            game.screen.blit(game.assets.planets[game.planetIndex],planet.rect)

            # Foreground icons
            if settings.showMenuIcons:
                for icon in fgIcons:
                    icon.move(game)
                    icon.draw(game)

            # Colliding icons
            if settings.showMenuIcons:
                for icon in cgIcons:
                    icon.draw(game)
                    icon.move(game)
                    if pygame.sprite.collide_mask(icon,planet):
                        game.explosions.append(Explosion(game,icon,None))
                        icon = icon.getNew(game)

            # DRAW EXPLOSIONS
            for debris in game.explosions:
                if debris.finished: game.explosions.remove(debris)
                else: debris.update(game)

            # PLAYER SKIN ANIMATION
            player.updateAnimation(game)

            game.screen.blit(game.assets.titleText,startRect) # Title Text
            if settings.showVersion: game.screen.blit(versionDisplay,versionRect) # Version info

            # Game controls
            self.drawLabels(game,startDisplays)
            self.drawLabels(game,controlDisplays)

            game.screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Draw current spaceship

            # Coin display
            game.screen.blit(coinDisplay,coinDisplayRect)
            game.screen.blit(game.assets.coinIcon,coinIconRect)

            # Ship stats display
            self.drawStats(game,shipAttributes)

            game.displayUpdate()


    # PAUSE SCREEN
    def pause(self,game,player,obstacles,lasers,enemyLasers):
        pygame.mixer.music.pause()
        playerBlit = game.rotateImage(player.image,player.rect,player.lastAngle)
        paused = True

        pausedDisplay = game.assets.largeFont.render("Paused", True, settings.secondaryFontColor)
        pausedRect = pausedDisplay.get_rect()
        pausedRect.center = (settings.screenSize[0]/2, settings.screenSize[1]/2)

        # REMAINING PAUSES
        pauseNum = str(settings.pauseMax - game.pauseCount) + " Pauses left"

        if game.pauseCount >= settings.pauseMax: pauseNum = "Out of pauses"

        pauseDisplay = game.assets.pauseCountFont.render(pauseNum,True,settings.secondaryFontColor)
        pauseRect = pauseDisplay.get_rect()
        pauseRect.center = (settings.screenSize[0]/2,settings.screenSize[1]-16)

        while paused:
            game.screen.fill(settings.screenColor)
            game.screen.blit(game.assets.bgList[game.currentStage - 1][0], (0,0) )
            game.showPlanet()
            game.showBackgroundCloud()

            if game.cave is not None:
                game.screen.blit(game.cave.background,game.cave.rect)
                game.screen.blit(game.cave.image,game.cave.rect) # Draw cave

            if settings.showHUD: game.showHUD(player) # Draw HUD

            game.screen.blit(game.thisPoint.image, game.thisPoint.rect)
            game.screen.blit(playerBlit[0],playerBlit[1])

            if player.showShield: # Draw shield
                shieldImg,shieldImgRect = game.rotateImage(game.assets.playerShield, player.rect, player.angle)
                game.screen.blit(shieldImg,shieldImgRect)

            game.obstacles.draw(game.screen)

            lasers.draw(game.screen)
            enemyLasers.draw(game.screen)
            game.screen.blit(pauseDisplay, pauseRect)
            game.screen.blit(pausedDisplay,pausedRect)
            game.displayUpdate()

            for event in pygame.event.get():
                # EXIT
                if event.type == pygame.QUIT: game.quitGame()

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in settings.fullScreenInput) or (game.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and game.gamePad.get_button(game.controller.controllerFullScreen) == 1):
                    game.toggleScreen()

                # UNPAUSE
                if (event.type == pygame.KEYDOWN and (event.key in settings.escapeInput or event.key in settings.startInput)) or (game.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and (game.gamePad.get_button(game.controller.controllerBack) == 1 or game.gamePad.get_button(game.controller.controllerPause) == 1)):
                    pygame.mixer.music.unpause()
                    paused = False


    # GAME OVER SCREEN
    def gameOver(self,game,player,obstacles):
        gameOver = True
        game.thisPoint = Point(game,None,None)
        game.assets.loadGameOverMusic()
        if game.musicMuted: pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1)

        # Show cursor
        pygame.mouse.set_visible(settings.cursorMode)

        # Update game records
        newLongRun = False
        newHighScore = False

        game.records["timePlayed"] += game.gameClock # Update total time played
        game.records["attempts"] += 1 # Update total attempts
        game.records["points"] += game.score # Update saved points
        game.records["coins"] += game.coinsCollected # Update coin balance

        # NEW LONGEST RUN
        if game.sessionLongRun > game.records["longestRun"]:
            newLongRun = True
            game.records["longestRun"] = game.sessionLongRun

        # NEW HIGH SCORE
        if game.score > game.records["highScore"]:
            newHighScore = True
            game.records["highScore"] = game.score

        game.assets.storeRecords(game.records) # SAVE UPDATED RECORDS
        if settings.connectToLeaderboard and (newHighScore or newLongRun):
            newRecordDisplay = game.assets.mediumFont.render("NEW RECORD!",True,(0,0,0))
            newRecordRect = newRecordDisplay.get_rect(center = player.rect.center)
            game.screen.blit(newRecordDisplay,newRecordRect)
            pygame.display.update()
            Leaderboard.uploadRecords(game.records,game.assets.userName) # upload to database

        statsOffsetY = settings.screenSize[1]/10
        statsSpacingY = settings.screenSize[1]/20

        # "GAME OVER" text
        gameOverDisplay = game.assets.largeFont.render("GAME OVER", True, [255,0,0])
        gameOverRect = gameOverDisplay.get_rect()
        gameOverRect.center = (settings.screenSize[0]/2, settings.screenSize[1]/3)

        # Text
        scoreLine = "Score " + str(game.score)
        highScoreLine = "High Score " + str(game.records["highScore"])
        newHighScoreLine = "New High Score! " + str(game.score)
        survivedLine = "Survived for " + str(game.gameClock) + " seconds"
        overallLongestRunLine = "Longest run  =  " + str(game.records["longestRun"]) + " seconds"
        newLongestRunLine = "New longest run! " + str(game.sessionLongRun) + " seconds"
        if not game.endlessModeStarted: levelLine = "Died at stage " + str(game.currentStage) + "  -  level " + str(game.currentLevel)
        else: levelLine = "Died in overtime"
        attemptLine = str(game.attemptNumber) + " attempts this session, " + str(game.records["attempts"]) + " overall"
        timeWasted = self.simplifyTime(game.records["timePlayed"])

        # Display
        scoreDisplay = game.assets.mediumFont.render(scoreLine, True, settings.primaryFontColor)
        highScoreDisplay = game.assets.mediumFont.render(highScoreLine, True, settings.primaryFontColor)
        newHighScoreDisplay = game.assets.mediumFont.render(newHighScoreLine, True, settings.primaryFontColor)
        longestRunDisplay = game.assets.mediumFont.render(overallLongestRunLine, True, settings.primaryFontColor)
        survivedDisplay = game.assets.mediumFont.render(survivedLine, True, settings.primaryFontColor)
        levelDisplay = game.assets.mediumFont.render(levelLine, True, settings.primaryFontColor)
        newLongestRunDisplay = game.assets.mediumFont.render(newLongestRunLine, True, settings.primaryFontColor)
        attemptDisplay = game.assets.mediumFont.render(attemptLine, True, settings.primaryFontColor)
        timeWastedDisplay = game.assets.mediumFont.render(timeWasted,True,settings.primaryFontColor)
        if not game.usingController or game.gamePad is None: exitDisplay = game.assets.mediumFont.render("TAB = Menu     SPACE = Restart    ESCAPE = Quit    C = Credits", True, settings.primaryFontColor)
        else: exitDisplay = game.assets.mediumFont.render("SELECT = Menu    A = Restart    START = Quit    Y = Credits", True, settings.primaryFontColor)

        # Rects
        survivedRect = survivedDisplay.get_rect()
        longestRunRect = longestRunDisplay.get_rect()
        newLongestRunRect = newLongestRunDisplay.get_rect()
        scoreRect = scoreDisplay.get_rect()
        highScoreRect = highScoreDisplay.get_rect()
        newHighScoreRect = newHighScoreDisplay.get_rect()
        levelRect = levelDisplay.get_rect()
        attemptRect = attemptDisplay.get_rect()
        wastedRect = timeWastedDisplay.get_rect()
        exitRect = exitDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 + 2* statsOffsetY +statsSpacingY * 8))

        # [display,rect] lists
        scoreText = scoreDisplay,scoreRect
        highScoreText = highScoreDisplay,highScoreRect
        newHighScoreText = newHighScoreDisplay,newHighScoreRect
        survivedText = survivedDisplay, survivedRect
        longestRunText = longestRunDisplay, longestRunRect
        newLongestRunText = newLongestRunDisplay, newLongestRunRect
        levelText = levelDisplay, levelRect
        attemptText = attemptDisplay, attemptRect
        wastedText = timeWastedDisplay, wastedRect

        displayTextList = [survivedText, longestRunText, newLongestRunText, scoreText, highScoreText, newHighScoreText, levelText, attemptText, wastedText]

        if newHighScore: settings.debug("New high score")
        if newLongRun: settings.debug("New longest run")

        while gameOver:
            # BACKGROUND
            game.screen.fill(settings.screenColor)
            game.screen.blit(game.assets.bgList[game.currentStage - 1][0], (0,0) )
            game.showPlanet()
            game.showBackgroundCloud()
            if game.cave is not None:
                game.screen.blit(game.cave.background,game.cave.rect)
                game.screen.blit(game.cave.image,game.cave.rect) # Draw cave

            if type(player.finalImg) != str: game.screen.blit(player.finalImg,player.finalRect) # Explosion / skip if explosion not initialized yet

            pygame.draw.rect(game.screen, settings.screenColor, [gameOverRect.x - 12,gameOverRect.y + 4,gameOverRect.width + 16, gameOverRect.height - 16],0,10)
            game.screen.blit(gameOverDisplay,gameOverRect)
            self.drawGameOverLabels(game,displayTextList,newHighScore,newLongRun)
            game.screen.blit(exitDisplay,exitRect)
            game.displayUpdate()

            for event in pygame.event.get():

                # CREDITS
                if event.type == pygame.KEYDOWN and event.key in settings.creditsInput or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerCredits) == 1): self.creditScreen(game)

                # EXIT
                if (event.type == pygame.KEYDOWN and event.key in settings.escapeInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerExit) == 1) or event.type == pygame.QUIT: game.quitGame()

                # MUTE
                if (event.type == pygame.KEYDOWN) and (event.key in settings.muteInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerMute) == 1): game.toggleMusic()

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in settings.fullScreenInput) or (game.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and game.gamePad.get_button(game.controller.controllerFullScreen) == 1): game.toggleScreen()

                # BACK TO MENU
                elif (event.type == pygame.KEYDOWN and event.key in settings.backInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerMenu) == 1) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] == 1):
                    if (event.type == pygame.KEYDOWN and event.key in settings.backInput): game.usingController,game.usingCursor = False,False
                    elif (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerBack) == 1): game.usingController,game.usingCursor = True,False
                    elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]==1): game.usingCursor, game.usingController = True, False
                    pygame.mouse.set_visible(settings.cursorMode) # Show cursor at menu
                    game.reset(player,obstacles)
                    game.mainMenu = True
                    game.skipAutoSkinSelect = True
                    game.start()

                # RESTART GAME
                elif (event.type == pygame.KEYDOWN and event.key in settings.startInput) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerSelect) == 1) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1):
                    if (event.type == pygame.KEYDOWN and event.key in settings.startInput): game.usingController,game.usingCursor = False,False
                    elif (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerSelect) == 1): game.usingController,game.usingCursor = True,False
                    elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1): game.usingCursor, game.usingController = True, False
                    pygame.mouse.set_visible(game.usingCursor and not settings.rawCursorMode)
                    game.reset(player,obstacles)
                    player.updatePlayerConstants(game)
                    game.start()


    # GET LABEL
    def getLabel(self,game,text,pos,font):
        if type(font) == pygame.font.Font: labelDisplay = font.render(text,True,settings.primaryFontColor)
        else: labelDisplay = game.assets.labelFont.render(text,True,settings.primaryFontColor)
        labelRect = labelDisplay.get_rect(center = pos)
        return [labelDisplay,labelRect]


    # DRAW LABELS
    def drawLabels(self,game,textList):
        for text in textList: game.screen.blit(text[0],text[1])


    # Draw labels from formatted list of rects and displays, first 4 lines arranged based on truth value of two booleans / will be revisited
    def drawGameOverLabels(self,game,textList, conditionOne, conditionTwo):
        statsSpacingY = 50
        statsOffsetY = 10
        skipped = 0
        # Both true
        if conditionOne and conditionTwo:
            for x in range(len(textList)):
                if x != 0 and x!= 1 and x!= 3 and x!= 4: # Skip 1st, 2nd, 4th, and 5th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                    game.screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1

        # newHighScore
        elif conditionTwo and not conditionOne:
            for x in range(len(textList)):
                if x != 0 and x!= 1 and x!= 5: # Skip 1st, 2nd, and 6th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3+ statsOffsetY + statsSpacingY * (x+1 - skipped)
                    game.screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1

        # newLongestRun
        elif conditionOne and not conditionTwo:
            for x in range(len(textList)):
                if x != 2 and x!= 3 and x!= 4: # Skip 3rd, 4th, and 5th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                    game.screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1

        else:
            for x in range(len(textList)):
                if x != 2 and x != 5: # Skip 3rd and 6th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                    game.screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1


    # LEADERBOARD
    def leaderboard(self,game):
        if settings.connectToLeaderboard:
            self.loadingScreen(game)
            game.assets.leaderboard = Leaderboard.getLeaders()
            if game.assets.leaderboard is None: showLeaderboard = False
            else: showLeaderboard = True
            titleDisplay = game.assets.leaderboardTitleFont.render("LEADER BOARD", True, settings.primaryFontColor)
            titleRect = titleDisplay.get_rect(center=(settings.screenSize[0]/2, 70))
            cellW = settings.screenSize[0] * 0.6
            cellH = 40
            leaderboardX = (settings.screenSize[0] - cellW) / 2  # Center the table horizontally
            leaderboardY = 100
            headerText = "#       Name                              Time       Score"
            headerDisplay = game.assets.mediumFont.render(headerText, True, settings.primaryFontColor)
            headerRect = headerDisplay.get_rect(topleft=(settings.screenSize[0]*0.2, leaderboardY))
            leaderSpacing = 40
            cellBorder = 2
            maxUsernameLength = 15

            helpText = "ESCAPE or TAB = Back"
            label = self.getLabel(game,helpText,[settings.screenSize[0]/2,settings.screenSize[1]*0.9],None)

            while showLeaderboard:
                for event in pygame.event.get():
                    # QUIT GAME
                    if event.type == pygame.QUIT: game.quitGame()

                    # RETURN TO GAME
                    if ((event.type == pygame.KEYDOWN and (event.key in settings.escapeInput or event.key in settings.leadersInput or event.key in settings.startInput or event.key in settings.backInput)) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerBack) == 1)) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]==1): showLeaderboard = False

                game.screen.fill(settings.screenColor)
                game.screen.blit(game.assets.bgList[game.currentStage - 1][0], (0, 0))

                game.screen.blit(titleDisplay,titleRect) # 'Leaderboard' text
                game.screen.blit(headerDisplay, headerRect) # Leaderboard table header

                # DRAW LEADERBOARD
                for index, leader in enumerate(game.assets.leaderboard):

                    # Name coloring
                    if leader['id'] == game.records['id']:
                        if index == 0: thisColor = (255,0,0)
                        else: thisColor = (255,255,255)
                    else: thisColor = (0,0,0)

                    cellX = leaderboardX
                    cellY = leaderboardY + (index + 1) * leaderSpacing
                    pygame.draw.rect(game.screen, settings.primaryFontColor, (cellX, cellY, cellW, cellH))
                    pygame.draw.rect(game.screen, (0, 0, 0), (cellX, cellY, cellW, cellH), cellBorder)

                    rankText = f"{index + 1}."
                    rankDisplay = game.assets.mediumFont.render(rankText, True, thisColor)
                    rankRect = rankDisplay.get_rect(midleft=(cellX + 10, cellY + cellH // 2))
                    game.screen.blit(rankDisplay, rankRect)

                    nameText = leader['name'][:maxUsernameLength]
                    nameDisplay = game.assets.mediumFont.render(nameText, True, thisColor)
                    nameRect = nameDisplay.get_rect(midleft=(cellX + cellW //12, cellY + cellH // 2))
                    game.screen.blit(nameDisplay, nameRect)

                    timeText= str(leader['time']) + "s"
                    timeDisplay = game.assets.mediumFont.render(timeText, True, thisColor)
                    timeRect = timeDisplay.get_rect(center=(cellX + cellW * 0.7, cellY + cellH // 2))
                    game.screen.blit(timeDisplay, timeRect)

                    scoreText = str(leader['score'])
                    scoreDisplay = game.assets.mediumFont.render(scoreText, True, thisColor)
                    scoreRect = scoreDisplay.get_rect(center=(cellX + cellW * 0.88, cellY + cellH // 2))
                    game.screen.blit(scoreDisplay, scoreRect)

                for index in range(len(game.assets.leaderboard) + 1):pygame.draw.line(game.screen, (0, 0, 0), (leaderboardX, leaderboardY + (index + 1) * leaderSpacing),(leaderboardX + cellW, leaderboardY + (index + 1) * leaderSpacing), 1)
                game.screen.blit(label[0],label[1])
                game.displayUpdate()


    # HANGER
    def hanger(self,game,player,unlocks):
        game.savedSkin = player.currentImageNum
        ships = []
        unlocked = game.records['unlocks']
        startPos,pos = [100,100],[100,100]
        spacingY = 80
        spacingX = 90
        scale = 2

        backLabel = self.getLabel(game,"ESCAPE/TAB = Back",[120,settings.screenSize[1]*0.9 + 20],None)
        selectLabel = self.getLabel(game,"SPACE = Select",[120,settings.screenSize[1]*0.9],None)
        viewLabel = self.getLabel(game,"V = View",[120,settings.screenSize[1]*0.9 - 20],None)

        # Coin Display
        coinDisplay = game.assets.mediumFont.render(str(game.records['coins']), True, settings.secondaryFontColor)
        coinDisplayRect = coinDisplay.get_rect(center = (settings.screenSize[0] -25, 25))
        coinIconRect = game.assets.coinIcon.get_rect(center = (settings.screenSize[0] -60, 25))

        for shipIndex in range(len(game.assets.spaceShipList)):
            skins = []
            images = game.assets.spaceShipList[shipIndex]['skins']
            for skinIndex in range(len(images)):
                if unlocked[shipIndex][skinIndex] or settings.devMode:
                    if type(images[skinIndex]) == list: # ANIMATED SKIN
                        shipFrames = []
                        for frame in images[skinIndex]:
                            oldScale = frame.get_rect().size
                            newScale = [oldScale[0]*scale,oldScale[1]*scale]
                            newImg = pygame.transform.scale(frame,newScale)
                            shipFrames.append(newImg)
                        skins.append([shipFrames,shipFrames[0].get_rect(center = (pos[0],pos[1])),0])

                    else: # STATIC SKIN
                        oldScale = images[skinIndex].get_rect().size
                        newScale = [oldScale[0]*scale,oldScale[1]*scale]
                        newImg = pygame.transform.scale(images[skinIndex],newScale)
                        skins.append([newImg,newImg.get_rect(center = (pos[0],pos[1]))])
                else:
                    if (skinIndex == 0 and not unlocked[shipIndex][0]) or unlocked[shipIndex][0]:  # Not unlocked ship yet
                        oldScale = game.assets.spaceShipList[shipIndex]['skins'][0].get_rect().size
                        newScale = [oldScale[0]*scale,oldScale[1]*scale]
                        newImg = pygame.transform.scale(game.assets.spaceShipList[shipIndex]['skins'][0],newScale)
                        newImg.fill([0,0,0], special_flags=pygame.BLEND_RGBA_MIN)
                        skins.append([newImg,newImg.get_rect(center = (pos[0],pos[1]))])

                pos[1]+= spacingY
            pos[1] = startPos[1]
            pos[0] += spacingX
            ships.append(skins)

        # Selected
        selectedShip = game.savedShipLevel
        selectedSkin = game.savedSkin
        selectRect = game.assets.selectIcon.get_rect()
        textPos = [settings.screenSize[0]/2,settings.screenSize[1]/2 - 80]

        animationCount = 0
        surfSize = [settings.screenSize[0]*1.5,settings.screenSize[1]*1.5]
        iconSurf = pygame.surface.Surface(surfSize, pygame.SRCALPHA)
        iconsPos = [0,0]

        showHanger = True
        while showHanger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: game.quitGame()

                # TOGGLE MUTE
                if ((event.type == pygame.KEYDOWN) and (event.key in settings.muteInput)) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerMute) == 1): game.toggleMusic()

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in settings.fullScreenInput) or (game.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and game.gamePad.get_button(game.controller.controllerFullScreen) == 1): game.toggleScreen()

                # RETURN TO GAME
                elif (event.type == pygame.KEYDOWN and (event.key in settings.escapeInput or event.key in settings.backInput or event.key in settings.hangerInput) ) or (game.gamePad is not None and (game.gamePad.get_button(game.controller.controllerBack) == 1)): showHanger = False

                # SELECT SHIP + RETURN TO GAME
                elif event.type == pygame.KEYDOWN and event.key in settings.startInput:
                    # switch to selected ship and return to menu
                    if unlocked[selectedShip][selectedSkin] or settings.devMode:
                        player.getShip(game,selectedShip)
                        player.getSkin(game,selectedSkin)
                        if not game.musicMuted: game.assets.pointNoise.play()
                        showHanger = False

                # SWITCH SHIPS
                elif (event.type == pygame.KEYDOWN and (event.key in settings.leftInput)):
                    if selectedShip == 0: selectedShip = len(ships) - 1
                    else: selectedShip -= 1
                    selectedSkin = 0
                elif (event.type == pygame.KEYDOWN and (event.key in settings.rightInput)):
                    if selectedShip + 1 >= len(ships): selectedShip = 0
                    else: selectedShip += 1
                    selectedSkin = 0

                # SWITCH SKINS
                elif (event.type == pygame.KEYDOWN and (event.key in settings.upInput)):
                    if selectedSkin == 0: selectedSkin = len(ships[selectedShip]) - 1
                    else: selectedSkin -= 1
                elif (event.type == pygame.KEYDOWN and (event.key in settings.downInput)):
                    if selectedSkin + 1 >= len(ships[selectedShip]): selectedSkin = 0
                    else: selectedSkin += 1

                # VIEW SELECTED SHIP
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                    if unlocked[selectedShip][selectedSkin] or settings.devMode: self.viewShip(game,game.assets.spaceShipList[selectedShip]['skins'][selectedSkin])

            iconSurf.fill((255,255,255,0))
            game.screen.blit(game.assets.bgList[game.currentStage - 1][0], (0, 0))

            for shipIndex in range(len(ships)):
                for skinIndex in range(len(ships[shipIndex])):
                    # Animated skin
                    if len(ships[shipIndex][skinIndex]) == 3 and type(ships[shipIndex][skinIndex][0]) == list:
                        iconSurf.blit(ships[shipIndex][skinIndex][0][ships[shipIndex][skinIndex][2]],ships[shipIndex][skinIndex][1])
                        if ships[shipIndex][skinIndex][2]+1 < len(ships[shipIndex][skinIndex][0]):
                            if animationCount >= settings.skinAnimationDelay:
                                ships[shipIndex][skinIndex][2] += 1
                                animationCount = 0
                            else: animationCount += 1
                        else: ships[shipIndex][skinIndex][2] = 0
                    # Static skin
                    else: iconSurf.blit(ships[shipIndex][skinIndex][0],ships[shipIndex][skinIndex][1])

            selectRect.center = ships[selectedShip][selectedSkin][1].center # Selection position
            iconSurf.blit(game.assets.selectIcon,selectRect)
            game.screen.blit(iconSurf,[settings.screenSize[0]/2 + iconsPos[0]-selectRect.center[0], settings.screenSize[1]/2 + iconsPos[1]-selectRect.center[1]]) # Draw icons surface on screen

            # Controls labels
            game.screen.blit(backLabel[0],backLabel[1])
            if unlocked[selectedShip][selectedSkin] or settings.devMode:
                game.screen.blit(viewLabel[0],viewLabel[1])
                game.screen.blit(selectLabel[0],selectLabel[1])

            # Coin count
            game.screen.blit(coinDisplay,coinDisplayRect)
            game.screen.blit(game.assets.coinIcon,coinIconRect)

            # Ship Name
            if unlocked[selectedShip][0]: shipName = unlocks.messages[selectedShip][1]
            else: shipName = " ? "
            nameDisplay = game.assets.mediumFont.render(" " + str(shipName) + " ",True,settings.primaryFontColor)
            nameRect = nameDisplay.get_rect(center = [textPos[0],textPos[1]])

            # Unlock Messages
            unlockMessage = unlocks.messages[selectedShip][0][selectedSkin][0]
            unlockMessageDisplay = game.assets.labelFont.render(" " + str(unlockMessage) + " ",True,settings.secondaryFontColor)
            unlockMessageRect = unlockMessageDisplay.get_rect(center = [textPos[0],textPos[1] + 25])

            # Variant name
            if unlocked[selectedShip][selectedSkin]: variantName = unlocks.messages[selectedShip][0][selectedSkin][1]
            else: variantName = " ? "
            variantNameDisplay = game.assets.mediumFont.render(" " + str(variantName) + " ", True, settings.secondaryFontColor)
            variantNameRect = variantNameDisplay.get_rect()
            variantNameRect.center = [nameRect.right + variantNameRect.width/2, textPos[1]]

            # Ship name display
            pygame.draw.rect(game.screen,settings.screenColor,nameRect,0,5)
            game.screen.blit(nameDisplay,nameRect)

            # Variant name display
            if variantName is not None:
                pygame.draw.rect(game.screen,settings.screenColor,variantNameRect,0,5)
                game.screen.blit(variantNameDisplay,variantNameRect)

            if not unlocked[selectedShip][selectedSkin] and not settings.devMode:
                pygame.draw.rect(game.screen,settings.screenColor,unlockMessageRect,0,5)
                game.screen.blit(unlockMessageDisplay,unlockMessageRect) # unlock hint

            game.displayUpdate()


    # VIEW SHIP
    def viewShip(self,game,image):
        scale = 2
        angle = 0
        zoomSpeed = 0.5
        maxZoom = 15
        minZoom = 0.5
        rotateSpeed = 3

        if type(image) == list:
            img = image[0]
            animationIndex,animationCount = 0,0
        else: img = image

        oldScale = img.get_rect().size
        newScale = [oldScale[0]*scale,oldScale[1]*scale]
        newImg = pygame.transform.scale(img,newScale)
        imgRect = newImg.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
        backLabel = self.getLabel(game,"ESCAPE/TAB/V = Back",[120,settings.screenSize[1]*0.9 + 20],None)

        viewing = True
        while viewing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: game.quitGame()

                # TOGGLE MUTE
                if ((event.type == pygame.KEYDOWN) and (event.key in settings.muteInput)) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerMute) == 1): game.toggleMusic()

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in settings.fullScreenInput) or (game.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and game.gamePad.get_button(game.controller.controllerFullScreen) == 1): game.toggleScreen()

                # RETURN TO HANGER
                elif (event.type == pygame.KEYDOWN and (event.key in settings.escapeInput or event.key in settings.backInput or event.key in settings.hangerInput or event.key == pygame.K_v) ) or (game.gamePad is not None and (game.gamePad.get_button(game.controller.controllerBack) == 1)): viewing = False

            key = pygame.key.get_pressed()
            if any(key[bind] for bind in settings.upInput) or any(key[bind] for bind in settings.downInput) or any(key[bind] for bind in settings.leftInput) or any(key[bind] for bind in settings.rightInput):
                prevAngle,prevScale = angle,scale
                if any(key[bind] for bind in settings.upInput) and scale+zoomSpeed <= maxZoom: scale += zoomSpeed
                if any(key[bind] for bind in settings.downInput) and scale - zoomSpeed > minZoom: scale -= zoomSpeed
                if any(key[bind] for bind in settings.leftInput): angle += rotateSpeed
                if any(key[bind] for bind in settings.rightInput): angle -= rotateSpeed

                # STATIC SKIN
                if angle != prevAngle or scale != prevScale: # ROTATE AND ZOOM
                    if angle <= -360 or angle >= 360: angle = 0
                    newScale = [oldScale[0]*scale,oldScale[1]*scale]
                    if type(image) != list:
                        newBlit = game.rotateImage(pygame.transform.scale(img,newScale),imgRect,angle)
                        newImg = newBlit[0]
                        imgRect = newBlit[1]

            # ANIMATED SKIN
            if type(image) == list:
                if animationCount < settings.skinAnimationDelay: animationCount += 1
                else:
                    animationCount = 0
                    if animationIndex + 1 >= len(image): animationIndex = 0
                    else: animationIndex += 1
                newBlit = game.rotateImage(pygame.transform.scale(image[animationIndex],newScale),imgRect,angle) # ROTATE AND ZOOM
                newImg = newBlit[0]
                imgRect = newBlit[1]

            game.screen.fill(settings.screenColor)
            game.screen.blit(game.assets.bgList[game.currentStage - 1][0], (0,0) )
            game.screen.blit(newImg,imgRect)
            game.screen.blit(backLabel[0],backLabel[1])
            game.displayUpdate()


    # CREDITS
    def creditScreen(self,game):
        global screen
        rollCredits = True
        posX = settings.screenSize[0]/2
        posY = settings.screenSize[1]/2

        topDir = ["S", "E", "W", "SE", "SW"]
        leftDir = ["E", "S", "N", "NE", "SE"]
        bottomDir = ["N", "W", "E", "NE", "NW"]
        rightDir = ["W", "N", "S", "NW", "SW"]

        createdByLine = "Created by Mike Pistolesi"
        creditsLine = "with art by Collin Guetta"
        musicCreditsLine = "music by Dylan Kusenko"
        moreMusicCreditsLine = "& game over music by Simon Colker"

        createdByDisplay = game.assets.creatorFont.render(createdByLine, True, settings.secondaryFontColor)
        creditsDisplay = game.assets.mediumFont.render(creditsLine, True, settings.secondaryFontColor)
        musicCreditsDisplay = game.assets.mediumFont.render(musicCreditsLine, True, settings.secondaryFontColor)
        moreMusicCreditsDisplay = game.assets.mediumFont.render(moreMusicCreditsLine, True, settings.secondaryFontColor)

        createdByRect = createdByDisplay.get_rect(center = (posX,posY))
        creditsRect = creditsDisplay.get_rect(center = (posX, posY +45))
        musicCreditsRect = musicCreditsDisplay.get_rect(center = (posX,posY+75))
        moreMusicCreditsRect = moreMusicCreditsDisplay.get_rect(center = (posX,posY+105))

        direction = self.randomEightDirection()

        extras = []
        bgShips = []
        waitToSpawn = True
        backGroundShipSpawnEvent = pygame.USEREVENT + 7
        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

        if len(game.assets.donations) == 0: extrasCap = settings.maxExtras

        elif len(game.assets.donations) > 0:
            if len(game.assets.donations) < settings.maxExtras: extrasCap = len(game.assets.donations)
            else: extrasCap = settings.maxExtras

        while rollCredits:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: game.quitGame()

                # TOGGLE MUTE
                if ((event.type == pygame.KEYDOWN) and (event.key in settings.muteInput)) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerMute) == 1): game.toggleMusic()

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in settings.fullScreenInput) or (game.gamePad is not None and event.type == pygame.JOYBUTTONDOWN and game.gamePad.get_button(game.controller.controllerFullScreen) == 1): game.toggleScreen()

                # SHIP SPAWN DELAY
                if event.type == backGroundShipSpawnEvent: waitToSpawn = False

                # RETURN TO GAME
                elif (event.type == pygame.KEYDOWN and (event.key in settings.escapeInput or event.key in settings.creditsInput or event.key in settings.startInput or event.key in settings.backInput) ) or (game.gamePad is not None and (game.gamePad.get_button(game.controller.controllerBack) == 1 or game.gamePad.get_button(game.controller.controllerCredits) == 1)): rollCredits = False

            game.screen.fill(settings.screenColor)
            game.screen.blit(game.assets.bgList[game.currentStage - 1][0],(0,0))
            game.showBackgroundCloud()

            for ship in bgShips:
                ship.move()
                if ship.active:
                    if len(game.assets.donations) == 0: ship.draw(game,False,settings.showSupporterNames)
                    else: ship.draw(game,settings.showBackgroundShips,settings.showSupporterNames)
                    # off screen, add name back to pool and remove
                    if ship.offScreen():
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))
                        bgShips.remove(ship)
                        for i in extras:
                            if i[0] == ship.text:
                                extras.remove(i)
                                break

            # Assign a background ship object
            if not waitToSpawn and extrasCap-len(bgShips) > 0: # make sure there is room
                if len(game.assets.donations) == 0: # If failed to load dictionary, display defaults to version number
                    if len(bgShips)==0:
                        bgShips.append(BackgroundShip(game,game.version,1))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

                elif len(game.assets.donations) == 1:
                    if len(bgShips) == 0:
                        name,value = list(game.assets.donations.items())[0]
                        bgShips.append(BackgroundShip(game,name,value))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

                else:
                    pool = list(game.assets.donations.keys())

                    for xtra in extras:
                        if xtra[0] in pool: pool.remove(xtra[0]) # Already on screen

                    if len(pool) > 0:
                        chosen = random.choice(pool) # get name from pool
                        extra = chosen,game.assets.donations[chosen]
                        extras.append(extra)
                        bgShips.append(BackgroundShip(extra[0],extra[1]))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

            # BOUNCE OFF EDGES
            if createdByRect.right > settings.screenSize[0]: direction = rightDir[random.randint(0, len(rightDir) - 1)]
            if createdByRect.left < 0: direction = leftDir[random.randint(0, len(leftDir) - 1)]
            if moreMusicCreditsRect.bottom > settings.screenSize[1]: direction = bottomDir[random.randint(0, len(bottomDir) - 1)]
            if createdByRect.top < 0 : direction = topDir[random.randint(0, len(topDir) - 1)]

            if "N" in direction:
                createdByRect.centery-= settings.mainCreditsSpeed
                creditsRect.centery-= settings.mainCreditsSpeed
                musicCreditsRect.centery-= settings.mainCreditsSpeed
                moreMusicCreditsRect.centery-= settings.mainCreditsSpeed

            if "S" in direction:
                createdByRect.centery+= settings.mainCreditsSpeed
                creditsRect.centery+= settings.mainCreditsSpeed
                musicCreditsRect.centery+= settings.mainCreditsSpeed
                moreMusicCreditsRect.centery+= settings.mainCreditsSpeed

            if "E" in direction:
                createdByRect.centerx+= settings.mainCreditsSpeed
                creditsRect.centerx+= settings.mainCreditsSpeed
                musicCreditsRect.centerx+= settings.mainCreditsSpeed
                moreMusicCreditsRect.centerx+= settings.mainCreditsSpeed

            if "W" in direction:
                createdByRect.centerx-= settings.mainCreditsSpeed
                creditsRect.centerx-= settings.mainCreditsSpeed
                musicCreditsRect.centerx-= settings.mainCreditsSpeed
                moreMusicCreditsRect.centerx-= settings.mainCreditsSpeed

            game.screen.blit(createdByDisplay,createdByRect)
            game.screen.blit(creditsDisplay,creditsRect)
            game.screen.blit(musicCreditsDisplay,musicCreditsRect)
            game.screen.blit(moreMusicCreditsDisplay,moreMusicCreditsRect)
            game.displayUpdate()


    # LOADING SCREEN
    def loadingScreen(self,game):
        loadingLine = "Loading..."
        loadingDisplay = game.assets.leaderboardTitleFont.render(loadingLine, True, settings.primaryFontColor)
        loadingRect = loadingDisplay.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
        game.screen.fill(settings.screenColor)
        game.screen.blit(game.assets.bgList[game.currentStage - 1][0], (0,0) )
        if game.cave is not None: game.screen.blit(game.cave.background,game.cave.rect)
        game.showBackgroundCloud()
        game.screen.blit(loadingDisplay,loadingRect)
        game.displayUpdate()


    # GET RANDOM DIRECTION - include diagonal
    def randomEightDirection(self):
        directions = ["N","S","E","W","NW","SW","NE","SE"]
        direction = directions[random.randint(0, len(directions)-1)]
        return direction


    # GET TIME PLAYED
    def simplifyTime(self,time):
        timePlayedLine = "Time played = "
        mins = int(time / 60)
        hours = int(mins / 60)
        secs = int(time % 60)
        remMins = int(mins - (hours * 60))
        if hours >= 1: timePlayed = timePlayedLine + str(hours) + " hours " + str(remMins) + " minutes " + str(secs) + " seconds"
        elif mins >= 1: timePlayed = timePlayedLine + str(mins) + " minutes + " + str(secs) + " seconds"
        else: timePlayed = timePlayedLine + str(secs) + " seconds"
        return timePlayed


    # Get ship attributes display
    def shipStatsDisplay(self,game):
        height = 5
        statsMultiplier = 10
        statsX = settings.screenSize[0]/2 -20
        statsY = settings.screenSize[1]/2 +125
        statsSpacingY = 10
        leftSpacing = -15
        topSpacing = 2

        shipStats = game.assets.spaceShipList[game.savedShipLevel]['stats']
        speed = shipStats['speed'] * statsMultiplier
        boostSpeed = shipStats['boostSpeed'] * statsMultiplier

        lasers = 0
        if shipStats["hasGuns"]:
            if shipStats["collats"]: lasers+=5
            if shipStats["laserType"] == "HOME": lasers+=25
            lasers+=shipStats["laserDamage"] * 2
            lasers+=shipStats["laserSpeed"]
            lasers-=shipStats["laserCost"] * 10
            if shipStats["fireRate"] > 0: lasers += (7000/shipStats["fireRate"])
            lasers = int(lasers)

        shields = 0
        if shipStats["hasShields"]:
            if shipStats["shieldPiecesNeeded"] > 0: shields += 100/shipStats["shieldPiecesNeeded"]
            shields += shipStats["startingShields"] * 5
            shields += shipStats["startingShieldPieces"] * 2
            shields = int(shields)

        speedBar = pygame.Rect(statsX,statsY, speed, height)
        speedDisplay = game.assets.shipStatsFont.render("Speed", True, settings.secondaryFontColor)

        boostSpeedBar = pygame.Rect(statsX, statsY + statsSpacingY, boostSpeed, height)
        boostSpeedDisplay = game.assets.shipStatsFont.render("Boost", True, settings.secondaryFontColor)

        laserBar = pygame.Rect(statsX, statsY + (2*statsSpacingY), lasers, height)
        laserDisplay = game.assets.shipStatsFont.render("Laser", True, settings.secondaryFontColor)

        shieldBar = pygame.Rect(statsX,statsY + (3*statsSpacingY), shields, height)
        shieldDisplay =  game.assets.shipStatsFont.render("Shield", True, settings.secondaryFontColor)

        blitList = [
                    [speedDisplay,speedDisplay.get_rect(center = (speedBar.left + leftSpacing,speedBar.y+topSpacing))],
                    [boostSpeedDisplay,boostSpeedDisplay.get_rect(center = (boostSpeedBar.left + leftSpacing,boostSpeedBar.y+topSpacing))],
                    [laserDisplay,laserDisplay.get_rect(center = (laserBar.left + leftSpacing,laserBar.y+topSpacing))],
                    [shieldDisplay,shieldDisplay.get_rect(center = (shieldBar.left + leftSpacing,shieldBar.y+topSpacing))]
                ]

        barList = [
                    [True,settings.fuelColor,speedBar],
                    [boostSpeed!=speed, settings.fuelColor, boostSpeedBar],
                    [lasers!=0,settings.fuelColor,laserBar],
                    [shields!=0,settings.shieldColor,shieldBar]
                ]
        return [blitList,barList]


    # Draw ship attributes display
    def drawStats(self,game,statsList):
        for i in statsList[0]: game.screen.blit(i[0],i[1])

        for i in statsList[1]:
            if i[0]: pygame.draw.rect(game.screen,i[1],i[2])


    # GET HELP LABELS
    def getHelpLabels(self,game,usingController):
        labelsX, labelsY, labelSpacing = 100,650,25
        startLabelPos = [settings.screenSize[0]/2,settings.screenSize[1]*0.75]
        if not usingController:
            startLabels = [
                            ["Press SPACE to start", startLabelPos],
                            ["ESCAPE = Quit", [labelsX,labelsY]],
                            ["H = Hanger", [labelsX,labelsY + (labelSpacing * 1)]],
                            ["F = Fullscreen", [labelsX,labelsY + (labelSpacing * 2)]],
                            ["M = Mute", [labelsX,labelsY + (labelSpacing *3)]],
                            ["C = Credits", [labelsX,labelsY + (labelSpacing *4)]]
                          ]
        else:
            startLabels = [
                            ["Press A to start", startLabelPos],
                            ["START = Quit", [labelsX,labelsY]],
                            ["??? = Hanger", [labelsX,labelsY + (labelSpacing * 1)]],
                            ["GUIDE = Fullscreen", [labelsX,labelsY + (labelSpacing * 2)]],
                            ["LB = Mute", [labelsX,labelsY + (labelSpacing *3)]],
                            ["Y = Credits", [labelsX,labelsY + (labelSpacing *4)]]
                          ]
        if settings.connectToLeaderboard: startLabels.append(["L = Leaderboard", [labelsX,labelsY + (labelSpacing *5)]])
        startDisplays = []
        first = True
        for label in startLabels:
            if first:
                first = False
                startDisplays.append(self.getLabel(game,label[0],label[1],game.assets.mediumFont))

            else:
                startDisplays.append(self.getLabel(game,label[0],label[1],None))
        return startDisplays


    def getControlLabels(self,game,player,usingController):
        controlsPos = [settings.screenSize[0]*0.75, settings.screenSize[1]*0.85]
        labels = []
        spacer = 25
        spacing = 0
        if not usingController:
            if len(game.assets.spaceShipList[game.savedShipLevel]['skins']) > 1 and (settings.devMode or game.unlocks.hasSkinUnlock(game.savedShipLevel)):
                labels.append(["A/LEFT = Last skin     D/RIGHT = Next skin",[controlsPos[0],controlsPos[1]]])
                spacing += spacer
            if len(game.assets.spaceShipList) > 1 and (settings.devMode or game.unlocks.hasShipUnlock()):
                labels.append(["S/DOWN = Last ship     W/UP = Next ship",[controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
            if player.hasGuns and player.boostSpeed > player.baseSpeed:
                labels.append(["SHIFT = Boost", [controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
                labels.append(["CTRL = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.hasGuns: labels.append(["CTRL = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.boostSpeed > player.baseSpeed: labels.append(["SHIFT = Boost", [controlsPos[0],controlsPos[1]+spacing]])
        else:
            if len(game.assets.spaceShipList[game.savedShipLevel]['skins']) > 1 and (settings.devMode or game.unlocks.hasSkinUnlock(game.savedShipLevel)):
                labels.append(["D-PAD LEFT = Last skin   D-PAD RIGHT = Next skin",[controlsPos[0],controlsPos[1]]])
                spacing += spacer
            if len(game.assets.spaceShipList) > 1 and (settings.devMode or game.unlocks.hasShipUnlock()):
                labels.append(["D-PAD DOWN = Last ship   D-PAD UP = Next ship",[controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
            if player.hasGuns and player.boostSpeed > player.baseSpeed:
                labels.append(["LT = Boost", [controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
                labels.append(["RT = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.hasGuns: labels.append(["RT = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.boostSpeed > player.baseSpeed: labels.append(["LT = Boost", [controlsPos[0],controlsPos[1]+spacing]])

        controlLabels = []
        for label in labels: controlLabels.append(self.getLabel(game,label[0],label[1],None))
        return controlLabels


# MENU ICONS
class Icon(pygame.sprite.Sprite):
    def __init__(self, game, iconType):
        super().__init__()
        self.iconType = iconType
        self.getNew(game)
        self.active = False


    def move(self,game):
        self.rect.centerx +=self.speed * math.cos(self.direction)
        self.rect.centery +=self.speed * math.sin(self.direction)
        self.activate()

        if self.angle >= 360 or self.angle <= -360: self.angle = 0

        self.angle += self.spinDirection * random.uniform(settings.minIconRotationSpeed, settings.maxIconRotationSpeed)

        randomTimerUX = random.randint(settings.screenSize[0] * 2,settings.screenSize[0] * 4)
        randomTimerUY = random.randint(settings.screenSize[1] * 2,settings.screenSize[1] * 4)
        randomTimerLX = -1 * random.randint(settings.screenSize[0], settings.screenSize[0] * 3)
        randomTimerLY = -1 * random.randint(settings.screenSize[0], settings.screenSize[1] * 3)

        if self.active and ( (self.rect.centery > randomTimerUY) or (self.rect.centery < randomTimerLY) or (self.rect.centerx> randomTimerUX) or (self.rect.centerx < randomTimerLX) ):
            self.getNew(game)
            self.active = False


    def activate(self):
        if not self.active:
            if self.rect.right > 0 and self.rect.left < settings.screenSize[0] and self.rect.bottom > 0 and self.rect.top < settings.screenSize[1]: self.active = True


    def draw(self,game):
        if self.active:
            drawing, drawee = game.rotateImage(self.image,self.rect,self.angle)
            game.screen.blit(drawing,drawee)


    def getNew(self,game):
        if self.iconType is None or self.iconType == "FG": self.getNewFg(game)
        elif self.iconType == "BG": self.getNewBg(game)
        elif self.iconType == "CG" or self.iconType == "COLLIDE": self.getNewCg(game)
        else: self.getNewFg(game) # Default


    # Get new foreground icon
    def getNewFg(self,game):
        spins = [-1,1]
        self.speed = random.randint(settings.minIconSpeed,settings.maxIconSpeed)
        self.movement = game.getMovement("LEFT")
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        if random.randint(0,10) < 7: self.image = game.assets.menuList[0]
        else: self.image = game.assets.menuList[random.randint(1,len(game.assets.menuList)-1)]
        size = random.randint(settings.minIconSize,settings.maxIconSize)
        self.image = pygame.transform.scale(self.image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = random.randint(0,360)


    # Get new background icon
    def getNewBg(self,game):
        self.speed = random.randint(5,15)
        self.movement = game.getMovement("LEFT")
        self.direction = self.movement[1]
        self.spinDirection = 1
        if random.randint(0,10) < 7: self.image = game.assets.menuList[0]
        else: self.image = game.assets.menuList[random.randint(1,len(game.assets.menuList)-1)]
        size = random.randint(5,15)
        self.image = pygame.transform.scale(self.image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0


    # Get new colliding icon
    def getNewCg(self,game):
        spins = [-1,1]
        self.speed = random.randint(settings.minIconSpeed,settings.maxIconSpeed)
        self.movement = game.getMovement("LEFT")
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        size = random.randint(10,20)
        self.image = pygame.transform.scale(game.assets.menuList[random.randint(0,len(game.assets.menuList)-1)], (size, size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = random.randint(0,360)



# CREDITS SCREEN BACKGROUND SHIPS
class BackgroundShip:
    def __init__(self,game,text,scale):
        self.scale = scale
        self.size = self.valueScaler(scale,settings.minBackgroundShipSize,settings.maxBackgroundShipSize,game.assets.lowDon,game.assets.maxDon)
        if self.size < settings.minBackgroundShipSize:
            self.size = settings.minBackgroundShipSize
            self.speed = settings.maxBackgroundShipSpeed
        elif self.size > settings.maxBackgroundShipSize:
            self.size = settings.minBackgroundShipSize
            self.speed = settings.minBackgroundShipSpeed
        self.speed = settings.maxBackgroundShipSpeed/self.size
        if self.speed > settings.maxBackgroundShipSpeed: self.speed = settings.maxBackgroundShipSpeed
        elif self.speed < settings.minBackgroundShipSpeed: self.speed = settings.minBackgroundShipSpeed
        self.movement = game.getMovement(None)
        self.direction = self.movement[1]
        self.text = text
        self.image = pygame.transform.scale(game.assets.donationShips[random.randint(0, len(game.assets.donationShips) - 1)], (self.size, self.size) ).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.font = pygame.font.Font(game.assets.gameFont, int(self.size * 2/3))
        self.display = self.font.render(self.text, True, [0,0,0])
        self.displayRect = self.display.get_rect(center = self.rect.center)
        self.active = False


    def move(self):
        self.rect.centerx +=self.speed * math.cos(self.direction)
        self.rect.centery +=self.speed * math.sin(self.direction)
        self.displayRect.center = self.rect.center
        self.activate()


    def draw(self,game,showImage,showText):
        if self.active:
            if not showImage and not showText: return
            else:
                drawing, drawee = game.rotateImage(self.image,self.rect,self.direction)
                supporterRect = self.display.get_rect(center = drawee.center)
                if showImage: game.screen.blit(drawing,drawee)
                if showText: game.screen.blit(self.display,supporterRect)


    # Returns true if off screen
    def offScreen(self):
        if settings.showSupporterNames and not settings.showBackgroundShips:
            if self.displayRect.bottom < 0 or self.displayRect.top > settings.screenSize[1] or self.displayRect.left > settings.screenSize[0] or self.displayRect.right < 0: return True
        else:
            if self.rect.bottom < 0 or self.rect.top > settings.screenSize[1] or self.rect.left > settings.screenSize[0] or self.rect.right < 0: return True


    def activate(self):
        if not self.active and not self.offScreen(): self.active = True


    # GET SCALED VALUE
    def valueScaler(self, amount, minimum, maximum, bottom, top):
        if bottom is None or top is None: return minimum
        elif top - bottom == 0: return (maximum + minimum) / 2
        else:
            scaled = (amount - bottom) / (top - bottom) * (maximum - minimum) + minimum
            return int(min(max(scaled, minimum), maximum))