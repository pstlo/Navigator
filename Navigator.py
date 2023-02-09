# NAVIGATOR
import random,math,sys,platform,os,pickle
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.display.init()
pygame.font.init()

pygame.mouse.set_visible(False)

#------------------GAME CONSTANTS--------------------------------------------------------------------------
# SCREEN                                                                                                                            
screenSize = [800,800] # Default = [800,800]
scaler = (screenSize[0] + screenSize[1])  / 1600 # Default = x + y / 2  / 800 == 1
roundedScaler = int(round(scaler))
fullScreen = False # Default = False

fuelColor = [255,0,0] # Default = [255,0,0] / Color of fuel gauge
fps = 60 # Default = 60                                    
timerSize = 75 * roundedScaler # Default = 75                            
timerColor = [255,255,255] # Default = [255,255,255] 
timerDelay = 1000 # Default = 1000

# LEVEL COUNTER
levelSize = 30 * roundedScaler # Default = 30                                                                                                                                                                   
levelColor = [255,255,255] # Default = [255,255,255] 

# BACKGROUND CLOUD
cloudSpeed = 1 # Default = 1
cloudStart = -1000 # Default = -1000
cloudSpeedAdder = 0.5 # Default = 0.5

# GAME OVER SCREEN
gameOverColor = [255,0,0] # Default = [255,0,0]
gameOverSize = 100 * roundedScaler # Default = 100
helpSize = 30 * roundedScaler # Default = 30 
helpColor = [0,255,0] # Default = [0,255,0]
finalScoreSize = 40 # Default = 40
finalScoreColor = [0,255,0] # Default = [0,255,0]
pausedSize = 100 * roundedScaler # Default = 100
pausedColor = [255,255,255] # Default = [255,255,255]
pauseMax = 5 # Default = 5

# START MENU
maxIcons = 5 # Default = 5
maxIconSpeed = 5 # Default = 5
maxIconRotationSpeed = 3 # Default = 3
startSize = 120 * roundedScaler # Default = 120
startColor = [0,255,0] # Default = [0,255,0]
minIconSize = 30 * roundedScaler # Default = 30
maxIconSize = 100 * roundedScaler # Default = 100

# STAGE UP
stageUpColor = [0,255,0] # Default = [0,255,0]
stageUpSize = 90 * roundedScaler # Default = 90
stageUpCloudStartPos = -900 # Default = -900
stageUpCloudSpeed = 8 * roundedScaler # Default = 8

# CREDITS
creditsFontSize = 55 * roundedScaler # Default = 55
creditsColor = [255,255,255] # Default = [255,255,255] 

# PLAYER           
exhaustUpdateDelay = 50 # Default = 50 / Delay (ms) between exhaust animation frames
boostCooldownTime = 500 # Default = 500 / Activates when fuel runs out to allow regen

# SHIP CONSTANTS
#                       [speed,fuel,maxFuel,fuelRegenNum,fuelRegenDelay,boostSpeed,hasGuns,laserCost,laserSpeed,laserFireRate,boostDrain,lasersStop]
defaultShipAttributes = [ 5,   10,  20,     0.05,        50,            7,         False,   0,        0,         0,           0.4,       True  ]
gunShipAttributes =     [ 3,   10,  20,     0.05,        50,            10,        True,    0.4,      10,        250,         0.3,       True  ]
laserShipAttributes =   [ 2,   1,   1,      0,           0,             2,         True,    0,        10,        50,          0,         True  ]
hyperYachtAttributes =  [ 3,   20,  30,     0.1,         25,            12,        False,   0,        0,         0,           0.25,      True  ]
oldReliableAttributes = [ 4,   10,  15,     0.05,        50,            6,         True,    1,        5,         1000,        0.25,      False ]

shipAttributes = [defaultShipAttributes,gunShipAttributes,laserShipAttributes,hyperYachtAttributes,oldReliableAttributes]

# OBSTACLES  (Can be updated by level)
obstacleSpeed = 4 *scaler  # Default = 4           
obstacleSize = 30 *scaler  # Default = 30
maxObstacles = 12 *scaler  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" 
aggro = True # Default = True / Removes restriction on obstacle movement - False = more difficult
spinSpeed = 1 # Default = 1
obstacleWipe = False # Default = False / Wipe before level
explosionDelay = 1 # Default = 1

# LEVELS  
levelTimer = 15 # Default = 15 / Time (seconds) between levels
levelUpCloudSpeed = 25 # Default = 25 / Only affects levels preceded by wipe

# ADD LEVELS HERE:   [ STARTED, (level-1)Timer, BOUNDS, SPEED ,      SIZE ,      NUMBER,     SPIN, AGGRO,      WIPE  ]
levelTwo =           [ False,       levelTimer, "KILL", 5.5*scaler,  32*scaler,  16*scaler,  1,    True,       False ]  
levelThree =         [ False,   2 * levelTimer, "KILL", 6*scaler,    34*scaler,  16*scaler,  2,    True,       False ] 
levelFour =          [ False,   3 * levelTimer, "KILL", 6.5*scaler,  36*scaler,  18*scaler,  3,    True,       False ] 
levelFive =          [ False,   4 * levelTimer, "KILL", 6*scaler,    38*scaler,  20*scaler,  4,    True,       False ] 
levelSix =           [ False,   5 * levelTimer, "KILL", 6.5*scaler,  40*scaler,  18*scaler,  3,    True,       False ] 
levelSeven =         [ False,   6 * levelTimer, "KILL", 2.2*scaler,  50*scaler,  65*scaler,  1,    True,       False ] 
levelEight =         [ False,   7 * levelTimer, "KILL", 7*scaler,    44*scaler,  20*scaler,  4,    True,       True  ] 
levelNine =          [ False,   8 * levelTimer, "KILL", 7*scaler,    46*scaler,  21*scaler,  5,    True,       False ]
levelTen =           [ False,   9 * levelTimer, "KILL", 7.5*scaler,  48*scaler,  22*scaler,  5,    True,       False ]
stageTwoLevelOne =   [ False,  10 * levelTimer, "KILL", 7.5*scaler,  50*scaler,  23*scaler,  0,    False,      False ]
stageTwoLevelTwo =   [ False,  11 * levelTimer, "KILL", 8*scaler,    52*scaler,  24*scaler,  0,    False,      False ]
stageTwoLevelThree = [ False,  12 * levelTimer, "KILL", 8*scaler,    54*scaler,  25*scaler,  3,    False,      False ]
stageTwoLevelFour =  [ False,  13 * levelTimer, "KILL", 8.5*scaler,  56*scaler,  26*scaler,  0,    False,      False ]

# DIVIDE INTO STAGES
stageOneLevels = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen] # Stage 1
stageTwoLevels = [stageTwoLevelOne,stageTwoLevelTwo,stageTwoLevelThree,stageTwoLevelFour] # Stage 2

# STORE IN LIST
stageList = [stageOneLevels, stageTwoLevels] # List of stages

#----------------------------------------------------------------------------------------------------------------------
# FOR EXE
def resource_path(relative_path):
    try: base_path = sys._MEIPASS    
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
# GET SCREEN SIZE
displayInfo = pygame.display.Info()
displayInfo = displayInfo.current_w,displayInfo.current_h
displayInfo = pygame.Rect(0, 0, displayInfo[0], displayInfo[1]).center

def getScreen():
    if fullScreen: return pygame.display.set_mode(screenSize,pygame.FULLSCREEN + pygame.SCALED) 
    else: return pygame.display.set_mode(screenSize)

# TOGGLE FULLSCREEN
def toggleScreen():
    global fullScreen
    fullScreen = not fullScreen
    return getScreen()

# ASSET DIRECTORY
currentDirectory = resource_path('Assets')

# INITIALIZE SCREEN
screen = getScreen()
 
# WINDOW
windowIcon = pygame.image.load(resource_path(os.path.join(currentDirectory,'Icon.png'))).convert_alpha()
pygame.display.set_caption('Navigator')
pygame.display.set_icon(windowIcon)
screenColor = [0,0,0] # Screen fill color

# ASSET LOADING
obstacleDirectory = os.path.join(currentDirectory, 'Obstacles') # Obstacle asset directory
meteorDirectory = os.path.join(obstacleDirectory, 'Meteors') # Meteor asset directory
ufoDirectory = os.path.join(obstacleDirectory, 'UFOs') # UFO asset directory
shipDirectory = os.path.join(currentDirectory, 'Spaceships') # Spaceship asset directory
backgroundDirectory = os.path.join(currentDirectory, 'Backgrounds') # Background asset directory
menuDirectory = os.path.join(currentDirectory, 'MainMenu') # Start menu asset directory
explosionDirectory = os.path.join(currentDirectory, 'Explosion') # Explosion animation directory

# FONT
gameFont = os.path.join(currentDirectory, 'Font.ttf')

# STAGE WIPE CLOUD
stageCloudImg = pygame.image.load(resource_path(os.path.join(currentDirectory,'StageCloud.png') ) ).convert_alpha()

# METEOR ASSETS
meteorList = []
for filename in sorted(os.listdir(meteorDirectory)):
    if filename.endswith('.png'):
        path = os.path.join(meteorDirectory, filename)
        meteorList.append(pygame.image.load(resource_path(path)).convert_alpha())

# UFO ASSETS
ufoList = []
for filename in sorted(os.listdir(ufoDirectory)):
    if filename.endswith('.png'):
        path = os.path.join(ufoDirectory, filename)
        ufoList.append(pygame.image.load(resource_path(path)).convert_alpha())

# ALL OBSTACLE ASSETS
obstacleImages = [meteorList,ufoList] # Seperated by stage

# BACKGROUND ASSETS 
bgList = []
for filename in sorted(os.listdir(backgroundDirectory)):
    filePath = os.path.join(backgroundDirectory,filename)
    if os.path.isdir(filePath):

        bgPath = os.path.join(backgroundDirectory,filename)  
        stageBgPath = os.path.join(bgPath,'Background.png')
        stageCloudPath = os.path.join(bgPath,'Cloud.png')
        
        if screenSize != [800,800]: # Stretching resolution
            bg = pygame.transform.scale(pygame.image.load(resource_path(stageBgPath)).convert_alpha(), (screenSize[0], screenSize[1]))
            cloud = pygame.transform.scale(pygame.image.load(resource_path(stageCloudPath)).convert_alpha(), (screenSize[0], screenSize[1]))
        
        else:
            bg = pygame.image.load(resource_path(stageBgPath)).convert_alpha()
            cloud = pygame.image.load(resource_path(stageCloudPath)).convert_alpha()

        bgList.append([bg,cloud])


# EXPLOSION ASSETS
explosionList = []
for filename in sorted(os.listdir(explosionDirectory)):
    if filename.endswith('.png'):
        path = os.path.join(explosionDirectory, filename)
        explosionList.append(pygame.image.load(resource_path(path)).convert_alpha())

# SPACESHIP ASSETS
spaceShipList = [] 
toRemoveBackground = ['gunShip.png','laserShip.png','f1Laser.png','hyperYacht.png', 'HYf1.png','HYf2.png','HYf3.png','olReliableShip.png','oRf1.png','oRf2.png','oRf3.png'] # List of PNGs in ships folder with white backgrounds

for levelFolder in sorted(os.listdir(shipDirectory)):
    levelFolderPath = os.path.join(shipDirectory,levelFolder) # level folder path
    
    if os.path.isdir(levelFolderPath): # Ignore DS_STORE on MacOS
        shipLevelList = []
        for shipAsset in sorted(os.listdir(levelFolderPath)): # Ship assets per level
            shipAssetPath = os.path.join(levelFolderPath,shipAsset) # Ship asset path        
            
            if os.path.isdir(shipAssetPath): # Ignore DS_STORE on MacOS
                assetList = []
                for imageAsset in sorted(os.listdir(shipAssetPath)): # Iterate through image folders
                    
                    if imageAsset.endswith('.png'): 
                        imageAssetPath = os.path.join(shipAssetPath,imageAsset)
                        imageAssetPng = pygame.image.load(resource_path((imageAssetPath)))
                        if imageAsset in toRemoveBackground: imageAssetPng.set_colorkey([255,255,255]) # Remove white background if specified in list
                        assetList.append(imageAssetPng.convert_alpha())

                shipLevelList.append(assetList)
            
            elif shipAsset == 'Laser.png':
                laserPng = pygame.image.load(resource_path(shipAssetPath))
                laserPng.set_colorkey([255,255,255]) 
                shipLevelList.append(laserPng.convert_alpha())

        spaceShipList.append(shipLevelList) # Add to main list

shipConstants = []
for i in shipAttributes: 
    levelConstantsDict = {
    "playerSpeed" : i[0],
    "fuel" : i[1],
    "maxFuel" : i[2],
    "fuelRegenNum" : i[3],
    "fuelRegenDelay" : i[4],
    "boostSpeed" : i[5],
    "hasGuns" : i[6],
    "laserCost" : i[7],
    "laserSpeed" : i[8],
    "laserFireRate" : i[9],
    "boostDrain" : i[10],
    "laserCollat" : i[11]
    }
    shipConstants.append(levelConstantsDict)
    
for i in range(len(spaceShipList)): spaceShipList[i].append(shipConstants[i])
# [   ( [Exhaust frames],Laser Image,[Ship Skins],{Player Constants} )   ]

# MAIN MENU ASSETS
menuList = []
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'A.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'O.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'big.png'))).convert_alpha()) 
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'left.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'right.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'dblue.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'lblue.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'lgreen.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'dgreen.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'orange.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'red.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'white.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDirectory,'yellow.png'))).convert_alpha())

# LOAD GAME RECORDS
if platform.system().lower() == 'windows' or platform.system().lower == 'linux': recordsPath = './gameRecords.txt' # For windows and linux
else: recordsPath = resource_path('gameRecords.txt') # For MacOS
try: 
    with open(recordsPath,'rb') as file:
        gameRecords = pickle.load(file)
except:
    gameRecords = {'highScore':0, 'attempts':0, 'timePlayed':0}
    try:
        with open(recordsPath,'wb') as file: 
            pickle.dump(gameRecords, file)
    except: pass # Continue game without saving
    
timerFont = pygame.font.Font(gameFont, timerSize)  

# for not aggro
topDir = ["S", "E", "W", "SE", "SW"]
leftDir = ["E", "S", "N", "NE", "SE"]
bottomDir = ["N", "W", "E", "NE", "NW"]
rightDir = ["W", "N", "S", "NW", "SW"]

# for aggro  
restrictedTopDir = ["SE", "SW", "S"]
restrictedLeftDir = ["E", "NE", "SE"]
restrictedBottomDir = ["N", "NE", "NW"]
restrictedRightDir = ["NW", "SW", "W"]
    

# GAME 
class Game:
    def __init__(self):
        self.currentLevel = 1
        self.currentStage = 1
        self.gameClock = 1
        self.pauseCount = 0
        self.clk = pygame.time.Clock()
        self.savedOverallHighScore = gameRecords["highScore"]
        self.savedTotalAttempts = gameRecords["attempts"]
        self.obstacleSpeed = obstacleSpeed         
        self.obstacleSize = obstacleSize  
        self.maxObstacles = maxObstacles
        self.aggro = aggro
        self.obstacleBoundaries = obstacleBoundaries 
        self.cloudSpeed = cloudSpeed
        self.attemptNumber = 1
        self.mainMenu = True # Assures start menu only runs when called
        self.sessionHighScore = 0
        self.gameConstants = []
        self.savedShipNum = 0
        self.savedShipLevel = 0
        self.unlockNumber = 0
        self.spinSpeed = spinSpeed
        self.cloudPos = cloudStart
        self.wipe = obstacleWipe
        self.explosions = []
        
        contantList = []
        for stage in stageList:
            stageConstants = []
            for settings in stage:
                levelDict = {
                                "START" : settings[0], 
                                "TIME" : settings[1],
                                "bound" : settings[2],  
                                "speedMult" : settings[3],
                                "obsSizeMult" : settings[4],
                                "maxObsMult" : settings[5],
                                "spinSpeed" : settings[6],
                                "aggro" : settings[7],
                                "wipe" : settings[8]
                    }
                stageConstants.append(levelDict)
            contantList.append(stageConstants)
        self.gameConstants = contantList 
        
        # LOAD GAME CONSTANTS
        self.savedConstants = {
                "obstacleSpeed" : self.obstacleSpeed, 
                "obstacleSize" : self.obstacleSize, 
                "maxObstacles" : self.maxObstacles, 
                "obstacleBoundaries" : self.obstacleBoundaries,
                "cloudSpeed" : self.cloudSpeed,
                "spinSpeed" : self.spinSpeed,
                "aggro" : self.aggro,
                "wipe" : self.wipe
                }

    
    # MAIN GAME LOOP
    def update(self,player,obstacles,menu,events,lasers):
        for event in pygame.event.get():
            
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            # INCREMENT TIMER
            if event.type == events.timerEvent: self.gameClock +=1
            
            # PAUSE GAME
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game.pauseCount < pauseMax :
                game.pauseCount += 1
                menu.pause(game,player,obstacles,lasers)
            
            # FUEL REPLENISH
            if event.type == events.fuelReplenish and player.fuel < player.maxFuel: player.fuel += player.fuelRegenNum
            
            # EXHAUST UPDATE
            if event.type == events.exhaustUpdate: player.updateExhaust(game)
            
            # GUN COOLDOWN
            if event.type == events.laserCooldown: player.laserReady = True
            
            # BOOST COOLDOWN
            if event.type == events.boostCooldown: player.boostReady = True

        # BACKGROUND ANIMATION
        screen.fill(screenColor)
        screen.blit(bgList[self.currentStage - 1][0], (0,0) )
        screen.blit(bgList[self.currentStage - 1][1], (0,self.cloudPos) )
        if self.cloudPos < screenSize[1]: self.cloudPos += self.cloudSpeed  
        else: self.cloudPos = cloudStart 
        
        # HUD
        self.showHUD(player)
        
        # OBSTACLE/PLAYER COLLISION DETECTION
        if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask):
            player.explode(game,obstacles)
            menu.gameOver(self,player,obstacles)
        
        # OBSTACLE/LASER COLLISION DETECTION
        for laser in lasers:
            if pygame.sprite.spritecollide(laser,obstacles,True,pygame.sprite.collide_mask):
                if player.laserCollat: laser.kill()
                self.explosions.append(Explosion(self,laser))
    
        for debris in self.explosions: 
            if debris.finished: self.explosions.remove(debris)
            else: debris.update()

        
        # DRAW AND MOVE SPRITES
        player.movement()
        player.shoot(lasers,events)
        player.boost(events)
        player.wrapping()
        self.spawner(obstacles)
        obstacleMove(obstacles)

        # UPDATE HIGH SCORE
        if self.gameClock > self.sessionHighScore: self.sessionHighScore = self.gameClock
        
        # OBSTACLE HANDLING
        if self.obstacleBoundaries == "KILL": obstacleRemove(obstacles)
        if self.obstacleBoundaries == "BOUNCE": bounceObstacle(obstacles)
        if self.obstacleBoundaries == "WRAP": wrapObstacle(obstacles)
        
        # LEVEL UP 
        self.levelUpdater(player,obstacles,events)   
        
        # ROTATE PLAYER
        newBlit = rotateImage(player.image,player.rect,player.angle)
        
        # ROTATE EXHAUST
        newExhaustBlit = rotateImage(spaceShipList[game.savedShipLevel][0][player.exhaustState-1],player.rect,player.angle)
        
        # DRAW PLAYER
        screen.blit(newBlit[0],newBlit[1])
        
        # DRAW EXHAST
        if game.savedShipLevel != 1: screen.blit(newExhaustBlit[0],newExhaustBlit[1])
        
        # UPDATE BOOST ANIMATION / currently only 3 frames
        player.lastThreeExhaustPos[2] = player.lastThreeExhaustPos[1]
        player.lastThreeExhaustPos[1] = player.lastThreeExhaustPos[0]
        player.lastThreeExhaustPos[0] =  newExhaustBlit
        
        # DRAW LASERS
        self.laserUpdate(lasers,player)
        
        # DRAW OBSTACLES
        for obs in obstacles:
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1]) # Blit obstacles
            obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle 
        
        # UPDATE SCREEN
        player.lastAngle = player.angle # Save recent player orientation
        player.angle = 0 # Reset player orientation
        pygame.display.flip()
        self.tick()
    
    
    def tick(self): self.clk.tick(fps)


    # SET GAME CONSTANTS TO DEFAULT
    def resetGameConstants(self):
        self.obstacleSpeed = self.savedConstants["obstacleSpeed"]
        self.obstacleSize = self.savedConstants["obstacleSize"]
        self.maxObstacles = self.savedConstants["maxObstacles"]
        self.obstacleBoundaries = self.savedConstants["obstacleBoundaries"]
        self.cloudSpeed = self.savedConstants["cloudSpeed"]
        self.spinSpeed = self.savedConstants["spinSpeed"]
        self.aggro = self.savedConstants["aggro"]
        self.wipe = self.savedConstants["wipe"]
        self.cloudPos = cloudStart
    
    
    def alternateUpdate(self,player,obstacles,events):
        player.alternateMovement()
        player.movement()
        player.wrapping()
        screen.fill(screenColor)
        screen.blit(bgList[self.currentStage-1][0],(0,0)) # Draw background
        screen.blit(bgList[self.currentStage-1][1],(0,self.cloudPos)) # Draw background cloud
        self.cloudPos += self.cloudSpeed
        obstacleMove(obstacles)
        
        for obs in obstacles:
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1])
            obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle 


    # UPDATE GAME CONSTANTS
    def levelUpdater(self,player,obstacles,events):
        
        # UPDATES STAGE
        if self.currentStage < len(self.gameConstants):
            if self.gameConstants[self.currentStage][0]["TIME"] == self.gameClock and not self.gameConstants[self.currentStage][0]["START"]:
                self.gameConstants[self.currentStage][0]["START"] = True
                stageUpCloud = stageCloudImg
                stageUpFont = pygame.font.Font(gameFont, stageUpSize)
                stageUpDisplay = stageUpFont.render("STAGE UP", True, stageUpColor)
                stageUpRect = stageUpCloud.get_rect()
                stageUpRect.center = (screenSize[0]/2, stageUpCloudStartPos)
                stageUp , stageWipe = True , True
                
                # STAGE UP ANIMATION / Removes old obstacles
                while stageUp:
                    
                    img, imgRect = rotateImage(player.image, player.rect, player.angle)
                    self.alternateUpdate(player,obstacles,events)
                    
                    for obs in obstacles:
                        if obs.rect.centery <= stageUpRect.centery: obs.kill()

                    screen.blit(stageUpCloud,stageUpRect) # Draw cloud
                    screen.blit(stageUpDisplay,(stageUpRect.centerx - screenSize[0]/5, stageUpRect.centery)) # Draw "STAGE UP" text
                    game.showHUD(player)
                    screen.blit(img,imgRect) # Draw player
                    pygame.display.flip()
                    stageUpRect.centery += stageUpCloudSpeed
                    self.tick()
                    
                    if stageUpRect.centery >= screenSize[1]/2 and stageWipe: 
                        self.currentStage += 1
                        self.currentLevel = 1
                        stageWipe = False
        
                    elif stageUpRect.centery >= screenSize[1] * 2: stageUp = False

        # UPDATES LEVEL
        for levelDict in self.gameConstants[self.currentStage-1]:
            if levelDict["TIME"] == self.gameClock:
                if not levelDict["START"]:
                    
                    if self.gameConstants[self.currentStage-1][self.currentLevel-1]["wipe"]:
                        # REMOVE OLD OBSTACLES
                        levelUpCloud = stageCloudImg
                        levelUpRect = levelUpCloud.get_rect()
                        levelUpRect.center = (screenSize[0]/2, stageUpCloudStartPos)
                        levelUp = True  
                        
                        # LEVEL UP ANIMATION / Removes old obstacles
                        while levelUp:
                            
                            img, imgRect = rotateImage(player.image, player.rect, player.angle)                        
                            self.alternateUpdate(player,obstacles,events)
                            for obs in obstacles:
                                if obs.rect.centery <= levelUpRect.centery: obs.kill()

                            screen.blit(levelUpCloud,levelUpRect) # Draw cloud
                            game.showHUD(player)
                            screen.blit(img,imgRect) # Draw player
                            pygame.display.flip()
                            levelUpRect.centery += levelUpCloudSpeed

                            if levelUpRect.top >= screenSize[1]: levelUp = False
 
                            self.tick()
                     
                    levelDict["START"] = True
                    self.obstacleBoundaries = levelDict["bound"]
                    self.obstacleSpeed = levelDict["speedMult"]
                    self.maxObstacles = levelDict["maxObsMult"]
                    self.obstacleSize = levelDict["obsSizeMult"]
                    self.spinSpeed = levelDict["spinSpeed"]
                    self.aggro = levelDict["aggro"]
                    self.wipe = levelDict["wipe"]
                    self.cloudSpeed += cloudSpeedAdder
                    self.currentLevel += 1
    

    # RESET LEVEL PROGRESS
    def resetAllLevels(self):
        for stage in self.gameConstants:
            for levels in stage:
                levels["START"] = False


    # REMOVE ALL OBSTACLES
    def killAllObstacles(self,obstacles):
        for obstacle in obstacles: obstacle.kill()


    # HUD
    def showHUD(self,player):
        
        # TIMER DISPLAY
        timerDisplay = timerFont.render(str(self.gameClock), True, timerColor)
        
        # STAGE DISPLAY
        stageNum = "Stage " + str(self.currentStage)
        stageFont = pygame.font.Font(gameFont, levelSize)
        stageDisplay = stageFont.render( str(stageNum), True, levelColor )
        stageRect = stageDisplay.get_rect(topleft = screen.get_rect().topleft)
        
        # LEVEL DISPLAY
        levelNum = "-  Level " + str(self.currentLevel)
        levelFont = pygame.font.Font(gameFont, levelSize)
        levelDisplay = levelFont.render( str(levelNum), True, levelColor )
        levelRect = levelDisplay.get_rect() 
        levelRect.center = (stageRect.right + levelRect.width*0.65, stageRect.centery)

        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright) 
        
        screen.blit(timerDisplay, timerRect)
        screen.blit(stageDisplay, stageRect)
        screen.blit(levelDisplay, levelRect)
        if player.boostDrain > 0 or player.laserCost > 0:
            rectWidth = (screenSize[0]/4) * (player.fuel / player.maxFuel)
            pygame.draw.rect(screen, fuelColor,[screenSize[0]/3, 0, rectWidth, 10]) # FUEL DISPLAY
    
    
    # SPAWN OBSTACLES
    def spawner(self,obstacles):
            if len(obstacles) < self.maxObstacles:
                obstacle = Obstacle(self.aggro)
                obstacles.add(obstacle)
    
    def laserUpdate(self,lasers,player):
        for laser in lasers:
            laser.move(player)
            screen.blit(laser.image,laser.rect)
    
    
    def resetClock(self): self.gameClock = 0


# GAME EVENTS
class Event:
    def __init__(self):
        
        # GAMECLOCK
        self.timerEvent = pygame.USEREVENT
        
        # BOOST
        self.fuelReplenish = pygame.USEREVENT + 1
        
        # EXHAUST UPDATE
        self.exhaustUpdate = pygame.USEREVENT + 2
        
        # LASER COOLDOWN
        self.laserCooldown = pygame.USEREVENT + 3
        
        # BOOST COOLDOWN
        self.boostCooldown = pygame.USEREVENT + 4

    # SETS EVENTS
    def set(self,player):
        pygame.time.set_timer(self.timerEvent, timerDelay)
        pygame.time.set_timer(self.fuelReplenish, player.fuelRegenDelay)
        pygame.time.set_timer(self.exhaustUpdate, exhaustUpdateDelay)
    
    def laserCharge(self,player):
        pygame.time.set_timer(self.laserCooldown, player.laserFireRate)
        player.laserReady = False
    
    def boostCharge(self,player):
        pygame.time.set_timer(self.boostCooldown, boostCooldownTime)
        player.boostReady = False


# MENUS
class Menu:
    
    # START MENU
    def home(self,game,player):
        
        global screen
        icons = []
        for icon in range(maxIcons): icons.append(Icon())
     
        startFont = pygame.font.Font(gameFont, startSize)
        startDisplay = startFont.render("N  VIGAT  R", True, startColor)
        startRect = startDisplay.get_rect()
        startRect.center = (screenSize[0]/2,screenSize[1]/2)
        
        startHelpFont = pygame.font.Font(gameFont, helpSize)
        startHelpDisplay = startHelpFont.render("ESCAPE = Quit     SPACE = Start     F = Fullscreen     C = Credits", True, helpColor)   
        startHelpRect = startHelpDisplay.get_rect()
        startHelpRect.center = (screenSize[0]/2,screenSize[1]-screenSize[1]/7)
        
        shipHelpFont = pygame.font.Font(gameFont, round(helpSize * .65))
        skinHelpDisplay = shipHelpFont.render("A/LEFT = Last skin     D/RIGHT = Next skin", True, helpColor)
        shipHelpDisplay = shipHelpFont.render("S/DOWN = Last ship     W/UP = Next ship", True, helpColor)
        skinHelpRect = skinHelpDisplay.get_rect(center = (screenSize[0]/4 + 40, screenSize[1]-screenSize[1]/7 + 70))
        shipHelpRect = shipHelpDisplay.get_rect(center = (screenSize[0]/4 + 40, screenSize[1]-screenSize[1]/7 + 40))
        
        boostHelp = shipHelpFont.render("SHIFT = Boost", True, helpColor)
        shootHelp = shipHelpFont.render("CTRL = Shoot", True, helpColor)
        boostHelpRect = boostHelp.get_rect()
        shootHelpRect = shootHelp.get_rect()
        
        leftRect = menuList[3].get_rect(center = (screenSize[0] * 0.2 , screenSize[1]/3) )
        rightRect = menuList[4].get_rect(center = (screenSize[0] * 0.8 , screenSize[1]/3) )
        
        bounceDelay = 5
        bounceCount = 0
        
        # DEFAULT SHIP SKIN UNLOCKS   ( spaceShipList[0] )
        if game.savedOverallHighScore >= 330: game.unlockNumber = len(spaceShipList[0][2])
        elif game.savedOverallHighScore >= 300: game.unlockNumber = len(spaceShipList[0][2]) - 1
        elif game.savedOverallHighScore >= 270: game.unlockNumber = len(spaceShipList[0][2]) - 2
        elif game.savedOverallHighScore >= 240: game.unlockNumber = len(spaceShipList[0][2]) - 3
        elif game.savedOverallHighScore >= 210: game.unlockNumber = len(spaceShipList[0][2]) - 4
        elif game.savedOverallHighScore >= 180: game.unlockNumber = len(spaceShipList[0][2]) - 5    
        elif game.savedOverallHighScore >= 150: game.unlockNumber = len(spaceShipList[0][2]) - 6 
        elif game.savedOverallHighScore >= 120: game.unlockNumber = len(spaceShipList[0][2]) - 7   
        elif game.savedOverallHighScore >= 90: game.unlockNumber = len(spaceShipList[0][2]) - 8    
        elif game.savedOverallHighScore >= 60: game.unlockNumber = len(spaceShipList[0][2]) - 9
        elif game.savedOverallHighScore >= 30: game.unlockNumber = len(spaceShipList[0][2]) - 10

        if game.unlockNumber < 0: game.unlockNumber = 0
        for imageNum in range(game.unlockNumber-1): player.nextSpaceShip() # Gets highest unlocked ship by default

        startOffset = 100
        startDelay = 1
        iconPosition, startDelayCounter = startOffset, 0
        
        while game.mainMenu:   
            if bounceCount >= bounceDelay: bounceCount = 0
            else: bounceCount +=1
                
            for event in pygame.event.get():
                # START
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    
                    game.savedShipNum = player.currentImageNum
                    
                    while iconPosition > 0:
                        
                        if startDelayCounter >= startDelay: startDelayCounter = 0
                        else: startDelayCounter +=1
                             
                        # Start animation
                        screen.fill(screenColor)
                        screen.blit(bgList[game.currentStage - 1][0],(0,0))
                        screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Current spaceship
                        
                        pygame.display.update()
                        
                        if startDelayCounter >= startDelay: iconPosition-=1

                    game.mainMenu = False    
                    return
                
                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # NEXT SPACESHIP SKIN
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                    player.nextSpaceShip()
                
                # PREVIOUS SPACESHIP SKIN                
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    player.lastSpaceShip()
                
                # NEXT SHIP TYPE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_w or event.key == pygame.K_UP):
                    player.toggleSpaceShip(game,True,game.unlockNumber)
                
                # PREVIOUS SHIP TYPE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_s or event.key == pygame.K_DOWN):
                    player.toggleSpaceShip(game,False,game.unlockNumber)

                # CREDITS
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c: menu.creditScreen()
                
                # QUIT
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                
            # GET SHIP CONTROLS
            if player.hasGuns and player.boostSpeed > player.baseSpeed: # has guns and boost
                boostHelpRect.center = screenSize[0]*3/4 - 60, screenSize[1]-screenSize[1]/7 + 40
                shootHelpRect.center = screenSize[0]*3/4 + 60, screenSize[1]-screenSize[1]/7 + 40
            elif player.hasGuns: shootHelpRect.center = screenSize[0]*3/4, screenSize[1]-screenSize[1]/7 + 40 # has guns only 
            elif player.boostSpeed > player.baseSpeed: boostHelpRect.center = screenSize[0]*3/4, screenSize[1]-screenSize[1]/7 + 40 # has boost only

            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            
            for icon in icons:
                if bounceCount == bounceDelay: icon.move()    
                icon.draw()
    
            screen.blit(startDisplay,startRect) # Menu Logo
            screen.blit(startHelpDisplay, startHelpRect) # Game controls
            
            # SHOW SHIP CONTROLS
            if player.hasGuns: screen.blit(shootHelp,shootHelpRect)
            if player.boostSpeed > player.baseSpeed: screen.blit(boostHelp,boostHelpRect)
            if game.savedOverallHighScore >= 30 and len(spaceShipList[game.savedShipLevel][2]) > 1: screen.blit(skinHelpDisplay,skinHelpRect) # Show switch skin controls
            screen.blit(shipHelpDisplay,shipHelpRect)
            screen.blit(player.image, (player.rect.x,player.rect.y + startOffset)) # Current spaceship
            
            # LOGO LETTERS
            screen.blit(menuList[0],(-14 + startRect.left + menuList[0].get_width() - menuList[0].get_width()/8,screenSize[1]/2 - 42)) # "A" symbol
            screen.blit(menuList[1],(-42 + screenSize[0] - startRect.centerx + menuList[1].get_width() * 2,screenSize[1]/2 - 42)) # "O" symbol
            
            # UFO ICONS
            screen.blit(menuList[2],(screenSize[0]/2 - menuList[2].get_width()/2,screenSize[1]/8)) # Big icon
            screen.blit(menuList[3],leftRect) # Left UFO
            screen.blit(menuList[4],rightRect) # Right UFO
            
            pygame.display.update()

    
    def pause(self,game,player,obstacles,lasers):
        global screen
        playerBlit = rotateImage(player.image,player.rect,player.lastAngle)
        paused = True
        pausedFont = pygame.font.Font(gameFont, pausedSize)
        pausedDisplay = pausedFont.render("Paused", True, pausedColor)
        pausedRect = pausedDisplay.get_rect()
        pausedRect.center = (screenSize[0]/2, screenSize[1]/2)
        
        # REMAINING PAUSES
        pauseCountSize = 40 * roundedScaler
        pauseNum = str(pauseMax - game.pauseCount) + " Pauses left"
        
        if game.pauseCount >= pauseMax: pauseNum = "Out of pauses"

        pauseCountFont = pygame.font.Font(gameFont,pauseCountSize)
        pauseDisplay = pauseCountFont.render( pauseNum , True, levelColor )
        pauseRect = pauseDisplay.get_rect() 
        pauseRect.center = (screenSize[0] * .5 , screenSize[1] - 16)
        
        while paused:
            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage-1][0],(0,0))
            screen.blit(cloud,(0,game.cloudPos))
            game.showHUD(player)
            
            screen.blit(playerBlit[0],playerBlit[1])
            
            for obs in obstacles: # Draw obstacles
                newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
                screen.blit(newBlit[0],newBlit[1])
            
            lasers.draw(screen)
            
            screen.blit(pauseDisplay, pauseRect)
            screen.blit(pausedDisplay,pausedRect)
            pygame.display.flip()
            for event in pygame.event.get():
            
                # EXIT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE): paused = False


    # GAME OVER SCREEN 
    def gameOver(self,game,player,obstacles):
        global screen
        gameOver = True
        
        # Update game records
        newHighScore = False
        
        try:
            with open(recordsPath,'rb') as file: outdatedRecords = pickle.load(file) # Load old records
        except: outdatedRecords = gameRecords # Continue with outdated records
            
        savedClock = outdatedRecords["timePlayed"] + game.gameClock # Update total time played
        game.savedTotalAttempts += 1 # Update total attempts
        
        updatedRecordsDict = {"highScore":game.savedOverallHighScore, "attempts":game.savedTotalAttempts,"timePlayed":savedClock} # Updated records
        if game.sessionHighScore > game.savedOverallHighScore: 
            newHighScore = True 
            game.savedOverallHighScore = game.sessionHighScore
            updatedRecordsDict["highScore"] = game.sessionHighScore
            
        try: 
            with open(recordsPath,'wb') as file: pickle.dump(updatedRecordsDict,file) # Save updated records
        except: pass  
   
        statsSpacingY = screenSize[1]/16
        
        # "GAME OVER" text
        gameOverFont = pygame.font.Font(gameFont, gameOverSize)
        gameOverDisplay = gameOverFont.render("GAME OVER", True, gameOverColor)
        gameOverRect = gameOverDisplay.get_rect()
        gameOverRect.center = (screenSize[0]/2, screenSize[1]/3)
        
        # Stats display
        statLineFontSize = round(finalScoreSize * 0.75)
        statFont = pygame.font.Font(gameFont, statLineFontSize)
        exitFont = pygame.font.Font(gameFont, helpSize)
        
        # Text
        attemptLine = str(game.attemptNumber) + " attempts this session, " + str(game.savedTotalAttempts) + " overall"
        survivedLine = "Survived for " + str(game.gameClock) + " seconds"
        levelLine = "Died at stage " + str(game.currentStage) + "  -  level " + str(game.currentLevel)
        overallHighScoreLine = "High score  =  " + str(game.savedOverallHighScore) + " seconds"
        newHighScoreLine = "New high score! " + str(game.sessionHighScore) + " seconds"
        timeWasted = "Time played = " + str(savedClock) + " seconds"
        
        # Display
        recordDisplay = statFont.render(overallHighScoreLine, True, finalScoreColor)
        attemptDisplay = statFont.render(attemptLine, True, finalScoreColor)
        survivedDisplay = statFont.render(survivedLine, True, finalScoreColor)
        levelDisplay = statFont.render(levelLine, True, finalScoreColor)
        newHighScoreDisplay = statFont.render(newHighScoreLine, True, finalScoreColor)
        timeWastedDisplay = statFont.render(timeWasted,True,finalScoreColor)
        exitDisplay = exitFont.render("TAB = Menu     SPACE = Restart    ESCAPE = Quit    C = Credits", True, helpColor)
        
        # Rects
        
        survivedRect = survivedDisplay.get_rect(center =(screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 3))
        recordRect = recordDisplay.get_rect(center =(screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 4))
        levelRect = levelDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 +statsSpacingY * 5))
        attemptRect = attemptDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 6))
        wastedRect = timeWastedDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 +statsSpacingY * 7))
        exitRect = exitDisplay.get_rect(center =(screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 8))
      
        while gameOver:
        
            # Background
            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            screen.blit(bgList[game.currentStage-1][1],(0,game.cloudPos))
            screen.blit(player.finalImg,player.finalRect) # Explosion
            if newHighScore: screen.blit(newHighScoreDisplay,recordRect)   
            else: screen.blit(recordDisplay,recordRect)
            pygame.draw.rect(screen, screenColor, [gameOverRect.x - 12,gameOverRect.y + 4,gameOverRect.width + 16, gameOverRect.height - 16],0,10)
            screen.blit(gameOverDisplay,gameOverRect)
            screen.blit(attemptDisplay,attemptRect)
            screen.blit(survivedDisplay,survivedRect)
            screen.blit(levelDisplay,levelRect)
            screen.blit(timeWastedDisplay,wastedRect)
            screen.blit(exitDisplay,exitRect)
            pygame.display.flip()
           
            for event in pygame.event.get():
                
                # EXIT
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # CREDITS
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_c): menu.creditScreen()

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB): 
                    # SET DEFAULTS AND GO BACK TO MENU
                    game.gameClock = 0
                    game.currentLevel = 1
                    game.currentStage = 1
                    player.kill()
                    game.killAllObstacles(obstacles)
                    game.resetAllLevels()
                    game.attemptNumber += 1
                    game.mainMenu = True
                    gameLoop()

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    # SET DEFAULTS AND RESTART GAME
                    game.gameClock = 0
                    game.currentLevel = 1
                    game.currentStage = 1
                    player.kill()
                    player.updatePlayerConstants(game)
                    game.killAllObstacles(obstacles)
                    game.resetAllLevels()
                    game.attemptNumber += 1
                    running = True
                    gameLoop()


    def creditScreen(self):
        global screen
        rollCredits = True 
        posX = screenSize[0]/2
        posY = screenSize[1]/2
        
        creatorFont = pygame.font.Font(gameFont, creditsFontSize)
        creditsFont = pygame.font.Font(gameFont, creditsFontSize - 15)
        
        createdByLine = "Created by Mike Pistolesi"
        creditsLine = "with art by Collin Guetta"
        
        createdByDisplay = creatorFont.render(createdByLine, True, creditsColor)
        creditsDisplay = creditsFont.render(creditsLine, True, creditsColor)
        
        creditsRect = creditsDisplay.get_rect()
        createdByRect = createdByDisplay.get_rect()
        
        creditsRect.center = (posX,posY)
        createdByRect.center = (posX, posY - screenSize[1]/15) 
        
        bounceCount = 0
        direction = randomEightDirection()
        
        while rollCredits:
            
            for event in pygame.event.get():
                # EXIT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # RETURN TO GAME
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_c or event.key == pygame.K_SPACE):
                    rollCredits = False
            
            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            screen.blit(createdByDisplay,createdByRect)
            screen.blit(creditsDisplay,creditsRect)
            pygame.display.flip()

            # BOUNCE OFF EDGES
            if createdByRect.right > screenSize[0]: direction = rightDir[random.randint(0, len(rightDir) - 1)]
            if createdByRect.left < 0: direction = leftDir[random.randint(0, len(leftDir) - 1)]  
            if creditsRect.bottom > screenSize[1]: direction = bottomDir[random.randint(0, len(bottomDir) - 1)]
            if createdByRect.top < 0 : direction = topDir[random.randint(0, len(topDir) - 1)]

            if bounceCount == 0:
                if "N" in direction:
                    creditsRect.centery-= 1
                    createdByRect.centery-= 1
                    
                if "S" in direction: 
                    creditsRect.centery+= 1
                    createdByRect.centery+= 1
                    
                if "E" in direction:
                    creditsRect.centerx+= 1
                    createdByRect.centerx+= 1
                    
                if "W" in direction:
                    creditsRect.centerx-= 1
                    createdByRect.centerx-= 1

            bounceCount +=1
            if bounceCount >= 10: bounceCount = 0


# PLAYER
class Player(pygame.sprite.Sprite):
        def __init__(self,game):
            super().__init__()
            
            # GET DEFAULT SHIP CONSTANTS
            self.currentImageNum = 0
            self.speed,self.baseSpeed,self.boostSpeed = spaceShipList[game.savedShipLevel][3]["playerSpeed"],spaceShipList[game.savedShipLevel][3]["playerSpeed"],spaceShipList[game.savedShipLevel][3]["boostSpeed"]
            self.image = spaceShipList[game.savedShipLevel][2][self.currentImageNum]
            self.laserImage = spaceShipList[game.savedShipLevel][1]
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.fuel, self.maxFuel = spaceShipList[game.savedShipLevel][3]["fuel"], spaceShipList[game.savedShipLevel][3]["maxFuel"]
            self.angle, self.lastAngle = 0, 0
            self.exhaustState, self.explosionState = 0, 0 # Index of animation frame
            self.finalImg, self.finalRect = '','' # Last frame of exhaust animation for boost
            self.lastThreeExhaustPos = [[0,0],[0,0],[0,0]] # Will be updated with rotateImage(recent player blits)
            self.fuelRegenNum = spaceShipList[game.savedShipLevel][3]["fuelRegenNum"]
            self.fuelRegenDelay = spaceShipList[game.savedShipLevel][3]["fuelRegenDelay"]
            self.boostDrain = spaceShipList[game.savedShipLevel][3]["boostDrain"]
            self.laserCost = spaceShipList[game.savedShipLevel][3]["laserCost"]
            self.laserSpeed = spaceShipList[game.savedShipLevel][3]["laserSpeed"]
            self.laserFireRate = spaceShipList[game.savedShipLevel][3]["laserFireRate"]
            self.laserCollat = spaceShipList[game.savedShipLevel][3]["laserCollat"]
            self.hasGuns, self.laserReady, self.boostReady = spaceShipList[game.savedShipLevel][3]["hasGuns"], True, True
        

        # PLAYER MOVEMENT
        def movement(self):
            key = pygame.key.get_pressed()
            
            if key[pygame.K_w] or key[pygame.K_UP]: 
                self.rect.centery -= self.speed
                self.angle = 0
                
            if key[pygame.K_s] or key[pygame.K_DOWN]: 
                self.rect.centery += self.speed
                self.angle = 180
            
            if key[pygame.K_a] or key[pygame.K_LEFT]: 
                self.rect.centerx -= self.speed
                self.angle = 90
            
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.rect.centerx += self.speed
                self.angle = -90
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = 45
                
            if (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = 0
                
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_d] or key[pygame.K_RIGHT]):
                self.angle = 0
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = -45
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
                self.angle = -135
                
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
                self.angle = 135
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_a] or key[pygame.K_LEFT]): 
                self.angle = 0
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = 90

            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]): 
                self.angle = 180
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]): 
                self.angle = -90
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_d] or key[pygame.K_RIGHT]): 
                self.angle = 0


        # SPEED BOOST
        def boost(self,events):
            if self.boostReady:
                if self.fuel - self.boostDrain > self.boostDrain:
                    key = pygame.key.get_pressed()
                    
                    if (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]) and ( (key[pygame.K_a] or key[pygame.K_LEFT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_d] or key[pygame.K_RIGHT]) ):
                        pass
                        
                    elif (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]) and ( (key[pygame.K_a] or key[pygame.K_LEFT]) or ( key[pygame.K_w] or key[pygame.K_UP]) or (key[pygame.K_s] or key[pygame.K_DOWN]) or (key[pygame.K_d] or key[pygame.K_RIGHT]) ):
                        self.speed = self.boostSpeed
                        self.fuel -= (self.boostDrain)
                        
                        try:
                            screen.blit(self.lastThreeExhaustPos[0][0],self.lastThreeExhaustPos[0][1])
                            screen.blit(self.lastThreeExhaustPos[1][0],self.lastThreeExhaustPos[1][1])
                            screen.blit(self.lastThreeExhaustPos[2][0],self.lastThreeExhaustPos[2][1])
                        except: pass

                    else: self.speed = self.baseSpeed
                
                else:
                    self.speed = self.baseSpeed
                    events.boostCharge(self)


        # SHOOT ROCKETS/LASERS
        def shoot(self,lasers,events):
            if self.hasGuns and self.laserReady:
                key = pygame.key.get_pressed()
                if  (key[pygame.K_LCTRL] or key[pygame.K_RCTRL]) and self.fuel - self.laserCost > 0:
                    lasers.add(Laser(self))
                    self.fuel -= self.laserCost
                    events.laserCharge(self)


        # MOVEMENT DURING STAGE UP
        def alternateMovement(self):    
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_UP): 
                    self.rect.centery -=1
                    self.angle = 0

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT): 
                    self.rect.centerx -=1
                    self.angle = 90

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN): 
                    self.rect.centery +=1
                    self.angle = 180  

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT): 
                    self.rect.centerx +=1
                    self.angle = -90 

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = -45
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = -45  
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT): self.angle = 135  
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT): self.angle = -135 
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_a or event.key == pygame.K_LEFT): self.angle = 0
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT): self.angle = 180
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = -90
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = 90
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = 0
                else: self.angle = 0

 
        # WRAP AROUND SCREEN
        def wrapping(self):
            if self.rect.centery  > screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = screenSize[1]
            if self.rect.centerx > screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = screenSize[0]


        # GET NEXT SPACESHIP IMAGE
        def nextSpaceShip(self):
            
            if self.currentImageNum + 1 < len(spaceShipList[game.savedShipLevel][2]):
            
                if (game.savedShipLevel == 0 and self.currentImageNum + 1 >= game.unlockNumber): 
                    self.image = spaceShipList[game.savedShipLevel][2][0]
                    self.currentImageNum = 0
                
                else:   
                    self.image = spaceShipList[game.savedShipLevel][2][self.currentImageNum + 1]
                    self.currentImageNum+=1
            
            else:
                self.image = spaceShipList[game.savedShipLevel][2][0]
                self.currentImageNum = 0

            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)


        # GET PREVIOUS SPACESHIP IMAGE
        def lastSpaceShip(self):
            if self.currentImageNum >= 1: 
                self.image = spaceShipList[game.savedShipLevel][2][self.currentImageNum - 1]
                self.currentImageNum-=1
            
            else:
                if game.savedShipLevel == 0 and game.unlockNumber == 0:
                    self.image = spaceShipList[0][2][game.unlockNumber]
                    self.currentImageNum = game.unlockNumber
                elif game.savedShipLevel == 0 and game.unlockNumber > 0:
                    self.image = spaceShipList[0][2][game.unlockNumber-1]
                    self.currentImageNum = game.unlockNumber-1
                else:
                    self.image = spaceShipList[game.savedShipLevel][2][len(spaceShipList[game.savedShipLevel][2]) - 1]
                    self.currentImageNum = len(spaceShipList[game.savedShipLevel][2]) - 1

            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)

        # SWITCH SHIP TYPE
        def toggleSpaceShip(self,game,toggleDirection,skinUnlocks): # Skin unlocks == True -> next ship, False -> Last
            if toggleDirection:
                if game.savedShipLevel + 1 < len(spaceShipList): game.savedShipLevel +=1
                else: game.savedShipLevel = 0
            
            else:
                if game.savedShipLevel - 1 < 0: game.savedShipLevel = len(spaceShipList) - 1
                else: game.savedShipLevel -=1

            self.updatePlayerConstants(game)


        def updatePlayerConstants(self,game):
            self.image = spaceShipList[game.savedShipLevel][2][0]
            self.laserImage = spaceShipList[game.savedShipLevel][1]
            self.currentImageNum = 0
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.speed,self.baseSpeed = spaceShipList[game.savedShipLevel][3]["playerSpeed"],spaceShipList[game.savedShipLevel][3]["playerSpeed"]
            self.fuel = spaceShipList[game.savedShipLevel][3]["fuel"]
            self.maxFuel = spaceShipList[game.savedShipLevel][3]["maxFuel"]
            self.fuelRegenNum = spaceShipList[game.savedShipLevel][3]["fuelRegenNum"]
            self.fuelRegenDelay = spaceShipList[game.savedShipLevel][3]["fuelRegenDelay"]
            self.boostSpeed = spaceShipList[game.savedShipLevel][3]["boostSpeed"]
            self.boostDrain = spaceShipList[game.savedShipLevel][3]["boostDrain"]
            self.laserCost = spaceShipList[game.savedShipLevel][3]["laserCost"]
            self.laserSpeed = spaceShipList[game.savedShipLevel][3]["laserSpeed"]
            self.laserFireRate = spaceShipList[game.savedShipLevel][3]["laserFireRate"]
            self.hasGuns = spaceShipList[game.savedShipLevel][3]["hasGuns"]
            self.laserCollat = spaceShipList[game.savedShipLevel][3]["laserCollat"]


        def updateExhaust(self,game):
            if self.exhaustState+1 > len(spaceShipList[game.savedShipLevel][0]): self.exhaustState = 0
            else: self.exhaustState += 1
        
        
        def explode(self,game,obstacles):
            while self.explosionState < len(explosionList):
                height = explosionList[self.explosionState].get_height()   
                width = explosionList[self.explosionState].get_width()
                screen.blit(bgList[game.currentStage-1][0],(0,0))
                screen.blit(bgList[game.currentStage-1][1],(0,game.cloudPos))
                obstacleMove(obstacles)
                
                for obs in obstacles:
                    newBlit = rotateImage(obs.image,obs.rect,obs.angle)
                    screen.blit(newBlit[0],newBlit[1])
                    
                img = pygame.transform.scale(explosionList[self.explosionState], (height * self.explosionState, width * self.explosionState))
                img, imgRect = rotateImage(img, self.rect, self.lastAngle)
                
                
                screen.blit(img,imgRect)    
                screen.blit(explosionList[self.explosionState],self.rect)
                pygame.display.update()
                game.tick()
                self.explosionState += 1
                self.finalImg,self.finalRect = img,imgRect


# OBSTACLES
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,aggro):
        super().__init__()
        self.aggro = aggro
        self.speed = game.obstacleSpeed
        self.size = game.obstacleSize
        self.spinSpeed = game.spinSpeed
        self.movement = getMovement(self.aggro)
        self.direction = self.movement[1]
        try: self.image = obstacleImages[game.currentStage - 1][game.currentLevel-1].convert_alpha()
        except: self.image = meteorList[random.randint(0,len(meteorList)-1)]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0
        spins = [-1,1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]


# LASERS
class Laser(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.speed = player.laserSpeed
        self.angle = player.angle
        newBlit = rotateImage(player.laserImage,player.laserImage.get_rect(center = player.rect.center),player.angle)
        self.image = newBlit[0]
        self.rect = newBlit[1]
        self.mask = pygame.mask.from_surface(self.image)

    # MOVE LASERS 
    def move(self,player): 
        # Laser angles = player angles, hard coded here
        if self.angle == 0: self.rect.centery -= (self.speed + player.speed) 
        elif self.angle == 180: self.rect.centery +=  (self.speed + player.speed) 
        elif self.angle == 90: self.rect.centerx -=  (self.speed + player.speed) 
        elif self.angle == -90: self.rect.centerx +=  (self.speed + player.speed) 

        elif self.angle == 45: 
            self.rect.centery -=  (self.speed + player.speed) 
            self.rect.centerx -= (self.speed + player.speed) 

        elif self.angle == -45: 
            self.rect.centery -=  (self.speed + player.speed) 
            self.rect.centerx += (self.speed + player.speed) 

        elif self.angle == 135: 
            self.rect.centery +=  (self.speed + player.speed) 
            self.rect.centerx -= (self.speed + player.speed) 

        elif self.angle == -135: 
            self.rect.centery +=  (self.speed + player.speed) 
            self.rect.centerx += (self.speed + player.speed) 
        
        # Remove lasers off screen
        if self.rect.centerx > screenSize[0] or self.rect.centery > screenSize[1] or self.rect.centerx < 0 or self.rect.centery < 0: self.kill()


# EXPLOSIONS
class Explosion:
    def __init__(self,game,laser):
        self.state,self.finalState,self.finished = 0,len(explosionList)-1,False
        self.rect = laser.rect
        self.image = explosionList[self.state]
        self.updateFrame = 0
        self.delay = explosionDelay
        
    def update(self):
        self.updateFrame +=1
        if self.updateFrame >= self.delay:
            self.updateFrame = 0
            if self.state +1 >= len(explosionList): self.finished = True
            else: 
                self.state +=1
                self.image = explosionList[self.state]

        screen.blit(self.image,self.rect)    


# MENU METEOR ICONS
class Icon(pygame.sprite.Sprite):
    def __init__(self):
        spins = [-1,1]
        self.speed = random.randint(1,maxIconSpeed)
        self.movement = getMovement(False)
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.image = menuList[random.randint(5,len(menuList)-1)]
        size = random.randint(minIconSize,maxIconSize)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0


    def move(self): 
        if "N" in self.direction: self.rect.centery -= self.speed                       
        if "S" in self.direction: self.rect.centery += self.speed                        
        if "E" in self.direction: self.rect.centerx += self.speed               
        if "W" in self.direction: self.rect.centerx -= self.speed  
        
        if self.angle >= 360 or self.angle <= -360: self.angle = 0
            
        self.angle += self.spinDirection * random.uniform(0, maxIconRotationSpeed)
        
        randomTimerUX = random.randint(screenSize[0] * 2,screenSize[0] * 4)
        randomTimerUY = random.randint(screenSize[1] * 2,screenSize[1] * 4)
        randomTimerLX = -1 * random.randint(screenSize[0], screenSize[0] * 3)
        randomTimerLY = -1 * random.randint(screenSize[0], screenSize[1] * 3)
        
        if (self.rect.centery > randomTimerUY) or (self.rect.centery < randomTimerLY) or (self.rect.centerx> randomTimerUX) or (self.rect.centerx < randomTimerLX):
            self.movement = getMovement(False)
            self.direction = self.movement[1]
            self.image = menuList[random.randint(5,len(menuList)-1)]
            self.speed = random.randint(1,maxIconSpeed)
            self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
            size = random.randint(minIconSize,maxIconSize)
            self.image = pygame.transform.scale(self.image, (size, size))


    def draw(self):
        drawing, drawee = rotateImage(self.image,self.rect,self.angle)
        screen.blit(drawing,drawee)


# ROTATE IMAGE
def rotateImage(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    rotatedRect = rotated.get_rect(center=rect.center)
    return rotated,rotatedRect


# REVERSE OBSTACLE MOVEMENT DIRECTION
def movementReverse(direction):
    if direction == "N": return "S"           
    elif direction == "S": return "N"                     
    elif direction == "E": return "W"           
    elif direction == "W": return "E"          
    elif direction == "NW": return "SE"         
    elif direction == "NE": return "SW"          
    elif direction == "SE": return "NW"
    elif direction == "SW": return "NE"


def randomEightDirection():
    directions = ["N","S","E","W","NW","SW","NE","SE"]
    direction = directions[random.randint(0, len(directions)-1)]
    return direction
    
    
# OBSTACLE POSITION GENERATION
def getMovement(eightDirections):
    top,bottom,left,right = [],[],[],[]
    
    if eightDirections: top, bottom, left, right = topDir, bottomDir, leftDir, rightDir
    else: top, bottom, left, right, = restrictedTopDir, restrictedBottomDir, restrictedLeftDir, restrictedRightDir
    X = random.randint(0, screenSize[0])
    Y = random.randint(0, screenSize[1])
    
    lowerX = random.randint(0, screenSize[0] * 0.05)
    upperX =  random.randint(screenSize[0] * 0.95, screenSize[0])
    lowerY  = random.randint(0, screenSize[1] * 0.05)
    upperY = random.randint(screenSize[1] * 0.95, screenSize[1])
    
    topDirection = top[random.randint(0, len(top) - 1)]
    leftDirection = left[random.randint(0, len(left) - 1)]
    bottomDirection = bottom[random.randint(0, len(bottom) - 1)]
    rightDirection = right[random.randint(0, len(right) - 1)]
    
    topBound = [X, lowerY, topDirection]
    leftBound = [lowerX, Y, leftDirection]
    bottomBound = [X, upperY, bottomDirection]
    rightBound = [upperX, Y, rightDirection]
 
    possible = [topBound, leftBound, rightBound, bottomBound]
    movement = possible[ random.randint(0, len(possible) - 1) ]
    
    position = [movement[0], movement[1]]
    direction = movement[2]
    move = [position,direction]
    return move 


# OBSTACLE MOVEMENT
def obstacleMove(obstacles):
    for obs in obstacles:
        position = obs.rect.center 
        if "N" in obs.direction: obs.rect.centery -= obs.speed    
        if "S" in obs.direction: obs.rect.centery += obs.speed      
        if "E" in obs.direction: obs.rect.centerx += obs.speed 
        if "W" in obs.direction: obs.rect.centerx -= obs.speed


# OFF SCREEN OBSTACLE REMOVAL
def obstacleRemove(obstacles):
    for obs in obstacles:
   
        if obs.rect.centerx > screenSize[0] or obs.rect.centerx < 0:
            obstacles.remove(obs)
            obs.kill()

        elif obs.rect.centery > screenSize[1] or obs.rect.centery < 0:
            obs.kill()
            obstacles.remove(obs)


# OBSTACLE BOUNCING
def bounceObstacle(obstacles):
    for obs in obstacles:
        direction = obs.direction
        if obs.rect.centery  > screenSize[1]: obs.direction = movementReverse(direction)    
        if obs.rect.centery < 0: obs.direction = movementReverse(direction) 
        if obs.rect.centerx > screenSize[0]: obs.direction = movementReverse(direction)   
        if obs.rect.centerx < 0: obs.direction = movementReverse(direction)
 
 
# OBSTACLE WRAPPING
def wrapObstacle(obstacles):
    for obs in obstacles:
        if obs.rect.centery  > screenSize[1]: obs.rect.centery = 0  
        if obs.rect.centery < 0: obs.rect.centery = screenSize[1]                      
        if obs.rect.centerx > screenSize[0]: obs.rect.centerx = 0      
        if obs.rect.centerx < 0: obs.rect.centerx = screenSize[0]


game = Game() # Initialize game
menu = Menu() # Initialize menus


def gameLoop():
    
    game.resetGameConstants() # Reset level settings
    game.pauseCount = 0 # Reset pause uses
    game.resetClock() # Restart game clock
    player = Player(game) # Initialize player
    
    if game.mainMenu: menu.home(game,player)
    else:
        for i in range(game.savedShipNum): player.nextSpaceShip()
    if game.savedShipLevel > 0: player.updatePlayerConstants(game)
    
    events = Event() # Initialize events 
    events.set(player) # Events manipulate player cooldowns
    lasers = pygame.sprite.Group() # Laser group
    obstacles = pygame.sprite.Group() # Obstacle group
    running = True
    
    # GAME LOOP
    while running: game.update(player,obstacles,menu,events,lasers)
 

if __name__ == '__main__': gameLoop()
    
