# Navigator v0.4.5
# Copyright (c) 2023 Mike Pistolesi
# All rights reserved

import random,math,sys,platform,os,pickle
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.display.init()
pygame.font.init()
pygame.mixer.init()

pygame.mouse.set_visible(False)

version = "v0.4.5"
#------------------GAME CONSTANTS--------------------------------------------------------------------------
# SCREEN
screenSize = [800,800] # Default = [800,800]
scaler = (screenSize[0] + screenSize[1]) / 1600 # Default = x + y / 2  / 800 == 1
roundedScaler = int(round(scaler)) # Assure scaled values are whole numbers
fullScreen = False # Default = False
fps = 60 # Default = 60

# HUD
shieldColor = [0,0,255] # Default = [0,0,255] / Color of shield gauge
fullShieldColor = [0,255,255] # Default = [0,255,255] / Color of active shield gauge
fuelColor = [255,0,0] # Default = [255,0,0] / Color of fuel gauge
timerSize = 30 * roundedScaler # Default = 50
timerColor = [255,255,255] # Default = [255,255,255]
timerDelay = 1000 # Default = 1000

# LEVEL COUNTER
levelSize = 30 * roundedScaler # Default = 30
levelColor = [255,255,255] # Default = [255,255,255]

# SCORE
scoreSize = 30 * roundedScaler # Default = 50

# POWER UPS
spawnRange = [0.1, 0.9]
spawnVertices = 8 # Default = 8 / Vertices in shape of point spawn area ( Octagon )
pointSize = 25  # Default = 20 ( Waiting for assets )
shieldChunkSize = screenSize[0]/40 # Default = screen width / 40
boostCooldownTime = 2000 # Default = 2000 / Activates when fuel runs out to allow regen
shieldPiecesNeeded = 10 # Default = 10 / Pieces needed for an extra life
showSpawnArea = False # Default = False
powerUpList = ["Blue", "Red", "White", "White", "White", "White"] # Red/White/Blue, chances of spawn

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
versionSize = 25
versionColor = [255,255,255]

# STAGE UP
stageUpColor = [0,255,0] # Default = [0,255,0]
stageUpSize = 90 * roundedScaler # Default = 90
stageUpCloudStartPos = -900 # Default = -900
stageUpCloudSpeed = 8 * roundedScaler # Default = 8

# CREDITS
creditsFontSize = 55 * roundedScaler # Default = 55
creditsColor = [255,255,255] # Default = [255,255,255]
mainCreditsSpeed = 1
extraCreditsSize = 30 * roundedScaler # background ships text size
extraCreditsColor = [0,0,0]
maxExtras = 3 # Default = 3 # max background ships
minBackgroundShipSpeed = 1 # Default = 1
maxBackgroundShipSpeed = 3 # Default = 3
minBackgroundShipSize = 50 # Default = 50
maxBackgroundShipSize = 150 # Default = 150
backgroundShipDelay = 20 # Default = 20
showBackgroundShips = False # Default = True / Waiting for assets
showSupporterNames = False # Default = True / Not started yet

# PLAYER
exhaustUpdateDelay = 50 # Default = 50 / Delay (ms) between exhaust animation frames

# SOUNDS
musicMuted = False # Default = False
musicVolume = 10 # Default = 10 / Music volume / 100
sfxVolume = 5 # Default = 5 / SFX volume / 100

# MUSIC LOOP DURATION
menuLoopStart = 1100 # Default = 1100
menuLoopEnd = 12800 # Default = 12800
musicLoopStart = 25000 # Default = 25000
musicLoopEnd = 76000 # Default = 76000

# SHIP CONSTANTS
#                       [speed,fuel,maxFuel,fuelRegenNum,fuelRegenDelay,boostSpeed,hasGuns,laserCost,laserSpeed,laserFireRate,boostDrain,lasersStop,hasShields,piecesNeeded]
defaultShipAttributes = [ 5,    1,  20,     0.05,        50,            7,         False,   0,        0,         0,           0.4,       True,      True,      10          ]
gunShipAttributes =     [ 3,   10,  20,     0.05,        50,            10,        True,    0.4,      10,        250,         0.3,       True,      False,      0          ]
laserShipAttributes =   [ 2,   1,   1,      0,           0,             2,         True,    0,        10,        50,          0,         True,      False,      0          ]
hyperYachtAttributes =  [ 3,   20,  30,     0.1,         25,            12,        False,   0,        0,         0,           0.25,      True,      False,      0          ]
oldReliableAttributes = [ 4,   10,  15,     0.05,        50,            6,         True,    1,        5,         1000,        0.25,      False,     False,      0          ]

shipAttributes = [defaultShipAttributes,gunShipAttributes,laserShipAttributes,hyperYachtAttributes,oldReliableAttributes]

# OBSTACLES
explosionDelay = 1 # Default = 1
obstacleSpawnRange = [0,1] # Default = [0,1]
# Starting values
obstacleSpeed = 4 *scaler  # Default = 4
obstacleSize = 30 *scaler  # Default = 30
maxObstacles = 12 *scaler  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL"
aggro = True # Default = True / Removes restriction on obstacle movement - False = more difficult
spinSpeed = 1 # Default = 1
obstacleWipe = False # Default = False / Wipe before level

# LEVELS
levelTimer = 15 # Default = 15 / Time (seconds) between levels
levelUpCloudSpeed = 25 # Default = 25 / Only affects levels preceded by wipe

# ADD LEVELS HERE:   [ STARTED, (level-1)Timer, BOUNDS, SPEED,       SIZE,       NUMBER,     SPIN, AGGRO, WIPE  ]
levelTwo =           [ False,       levelTimer, "KILL", 5*scaler,    32*scaler,  16*scaler,  1,    True,  False ]
levelThree =         [ False,   2 * levelTimer, "KILL", 5*scaler,    34*scaler,  16*scaler,  2,    True,  False ]
levelFour =          [ False,   3 * levelTimer, "KILL", 5.5*scaler,  36*scaler,  16*scaler,  3,    True,  False ]
levelFive =          [ False,   4 * levelTimer, "KILL", 6*scaler,    38*scaler,  16*scaler,  4,    True,  False ]
levelSix =           [ False,   5 * levelTimer, "KILL", 6.5*scaler,  40*scaler,  18*scaler,  3,    True,  False ]
levelSeven =         [ False,   6 * levelTimer, "KILL", 2.2*scaler,  50*scaler,  65*scaler,  1,    True,  False ]
levelEight =         [ False,   7 * levelTimer, "KILL", 7*scaler,    44*scaler,  20*scaler,  4,    True,  True  ]
levelNine =          [ False,   8 * levelTimer, "KILL", 7*scaler,    46*scaler,  21*scaler,  5,    True,  False ]
levelTen =           [ False,   9 * levelTimer, "KILL", 7.5*scaler,  48*scaler,  22*scaler,  5,    True,  False ]
stageTwoLevelOne =   [ False,  10 * levelTimer, "KILL", 7.5*scaler,  50*scaler,  23*scaler,  0,    False, False ]
stageTwoLevelTwo =   [ False,  11 * levelTimer, "KILL", 8*scaler,    52*scaler,  24*scaler,  0,    False, False ]
stageTwoLevelThree = [ False,  12 * levelTimer, "KILL", 8*scaler,    54*scaler,  25*scaler,  3,    False, False ]
stageTwoLevelFour =  [ False,  13 * levelTimer, "KILL", 8.5*scaler,  56*scaler,  26*scaler,  0,    False, False ]

# DIVIDE INTO STAGES
stageOneLevels = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen] # Stage 1
stageTwoLevels = [stageTwoLevelOne,stageTwoLevelTwo,stageTwoLevelThree,stageTwoLevelFour] # Stage 2

# STORE IN LIST
stageList = [stageOneLevels, stageTwoLevels] # List of stages

#----------------------------------------------------------------------------------------------------------------------
# FOR EXE RESOURCES
def resources(relative):
    try: base = sys._MEIPASS
    except Exception: base = os.path.abspath(".")
    return os.path.join(base, relative)


# GET SCREEN SIZE
displayInfo = pygame.display.Info()
displayInfo = displayInfo.current_w,displayInfo.current_h
displayInfo = pygame.Rect(0, 0, displayInfo[0], displayInfo[1]).center


# GET SCREEN
def getScreen():
    if fullScreen: return pygame.display.set_mode(screenSize,pygame.FULLSCREEN + pygame.SCALED)
    else: return pygame.display.set_mode(screenSize)


# TOGGLE FULLSCREEN
def toggleScreen():
    global fullScreen
    fullScreen = not fullScreen
    return getScreen()


# MENU MUSIC LOOP
def menuMusicLoop():
    if pygame.mixer.music.get_pos() >= menuLoopEnd:
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(menuLoopStart)
        pygame.mixer.music.play()


# GAMEPLAY MUSIC LOOP
def musicLoop():
    if pygame.mixer.music.get_pos() >= musicLoopEnd:
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(musicLoopStart)
        pygame.mixer.music.play()


# TOGGLE MUSIC MUTE
def toggleMusic(game):
    game.musicMuted = not game.musicMuted
    if pygame.mixer.music.get_volume() == 0: pygame.mixer.music.set_volume(musicVolume/100)
    else: pygame.mixer.music.set_volume(0)


# ASSET DIRECTORY
currentDirectory = resources('Assets')

# INITIALIZE SCREEN
screen = getScreen()

# WINDOW
windowIcon = pygame.image.load(resources(os.path.join(currentDirectory,'Icon.png'))).convert_alpha()
pygame.display.set_caption('Navigator')
pygame.display.set_icon(windowIcon)
screenColor = [0,0,0] # Screen fill color


# Get dictionary from plain text
def readTxt(filename):
    namesList = {}
    path = os.path.join(os.getcwd(),filename+'.txt')
    with open(path,'r') as file:
        for line in file:
            key, val = line.strip().split(':')
            namesList[key] = val
    return namesList


# Draw labels from formatted list of rects and displays, first 4 lines arranged based on truth value of two booleans
def drawGameOverLabels(textList, conditionOne, conditionTwo):
    statsSpacingY = 50
    statsOffsetY = 10
    skipped = 0
    # Both true
    if conditionOne and conditionTwo:
        for x in range(len(textList)):
            if x != 0 and x!= 1 and x!= 3 and x!= 4: # Skip 1st, 2nd, 4th, and 5th items
                textList[x][1].center = screenSize[0]/2, screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                screen.blit(textList[x][0],textList[x][1])
            else: skipped+=1

    # newHighScore
    elif conditionOne and not conditionTwo:
        for x in range(len(textList)):
            if x != 0 and x!= 1 and x!= 5: # Skip 1st, 2nd, and 6th items
                textList[x][1].center = screenSize[0]/2, screenSize[1]/3+ statsOffsetY + statsSpacingY * (x+1 - skipped)
                screen.blit(textList[x][0],textList[x][1])
            else: skipped+=1

    # newLongestRun
    elif conditionTwo and not conditionOne:
        for x in range(len(textList)):
            if x != 2 and x!= 3 and x!= 4: # Skip 3rd, 4th, and 5th items
                textList[x][1].center = screenSize[0]/2, screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                screen.blit(textList[x][0],textList[x][1])
            else: skipped+=1

    else:
        for x in range(len(textList)):
            if x != 2 and x != 5: # Skip 3rd and 6th items
                textList[x][1].center = screenSize[0]/2, screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                screen.blit(textList[x][0],textList[x][1])
            else: skipped+=1


# ASSET LOADING
obstacleDirectory = os.path.join(currentDirectory, 'Obstacles') # Obstacle asset directory
meteorDirectory = os.path.join(obstacleDirectory, 'Meteors') # Meteor asset directory
ufoDirectory = os.path.join(obstacleDirectory, 'UFOs') # UFO asset directory
shipDirectory = os.path.join(currentDirectory, 'Spaceships') # Spaceship asset directory
backgroundDirectory = os.path.join(currentDirectory, 'Backgrounds') # Background asset directory
menuDirectory = os.path.join(currentDirectory, 'MainMenu') # Start menu asset directory
explosionDirectory = os.path.join(currentDirectory, 'Explosion') # Explosion animation directory
pointsDirectory = os.path.join(currentDirectory, 'Points') # Point image directory
soundDirectory = os.path.join(currentDirectory, 'Sounds') # Sound assets directory
supportersDirectory = os.path.join(currentDirectory,'Supporters') # Supporters directory

# FONT
gameFont = os.path.join(currentDirectory, 'Font.ttf')

# STAGE WIPE CLOUD
stageCloudImg = pygame.image.load(resources(os.path.join(currentDirectory,'StageCloud.png') ) ).convert_alpha()

# METEOR ASSETS
meteorList = []
for filename in sorted(os.listdir(meteorDirectory)):
    if filename.endswith('.png'):
        path = os.path.join(meteorDirectory, filename)
        meteorList.append(pygame.image.load(resources(path)).convert_alpha())

# UFO ASSETS
ufoList = []
for filename in sorted(os.listdir(ufoDirectory)):
    if filename.endswith('.png'):
        path = os.path.join(ufoDirectory, filename)
        ufoList.append(pygame.image.load(resources(path)).convert_alpha())

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
            bg = pygame.transform.scale(pygame.image.load(resources(stageBgPath)).convert_alpha(), (screenSize[0], screenSize[1]))
            cloud = pygame.transform.scale(pygame.image.load(resources(stageCloudPath)).convert_alpha(), (screenSize[0], screenSize[1]))

        else:
            bg = pygame.image.load(resources(stageBgPath)).convert_alpha()
            cloud = pygame.image.load(resources(stageCloudPath)).convert_alpha()

        bgList.append([bg,cloud])

# EXPLOSION ASSETS
explosionList = []
for filename in sorted(os.listdir(explosionDirectory)):
    if filename.endswith('.png'):
        path = os.path.join(explosionDirectory, filename)
        explosionList.append(pygame.image.load(resources(path)).convert_alpha())


# POINTS ASSETS
pointsList = []
for filename in sorted(os.listdir(pointsDirectory)):

    if filename.endswith('png'):

        path = os.path.join(pointsDirectory, filename)
        pointPng = pygame.image.load(resources(path))

        if filename == 'default.png': pointPng.set_colorkey([0,0,0])
        else: pointPng.set_colorkey([255,255,255])

        pointsList.append(pointPng.convert_alpha())


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
                        imageAssetPng = pygame.image.load(resources((imageAssetPath)))
                        if imageAsset in toRemoveBackground: imageAssetPng.set_colorkey([255,255,255]) # Remove white background if specified in list
                        assetList.append(imageAssetPng.convert_alpha())

                shipLevelList.append(assetList)

            elif shipAsset == 'Laser.png':
                laserPng = pygame.image.load(resources(shipAssetPath))
                laserPng.set_colorkey([255,255,255])
                shipLevelList.append(laserPng.convert_alpha())

        spaceShipList.append(shipLevelList) # Add to main list

# MUSIC ASSET
pygame.mixer.music.load(resources(os.path.join(soundDirectory,"Soundtrack.mp3")))

# LICENSE FREE SOUND ASSETS

# EXPLOSION NOISE ASSET
explosionNoise = pygame.mixer.Sound(resources(os.path.join(soundDirectory,"Explosion.wav")))
explosionNoise.set_volume(sfxVolume/100)

# POINT NOISE ASSET
powerUpNoise = pygame.mixer.Sound(resources(os.path.join(soundDirectory,"Point.wav")))
powerUpNoise.set_volume(sfxVolume/100)

# LASER NOISE ASSET
laserNoise = pygame.mixer.Sound(resources(os.path.join(soundDirectory,"Laser.wav")))
laserNoise.set_volume(sfxVolume/100)

# LASER IMPACT NOISE ASSET
impactNoise = pygame.mixer.Sound(resources(os.path.join(soundDirectory,"Impact.wav")))
impactNoise.set_volume(sfxVolume/100)


# SHIP ATTRIBUTES DATA
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
    "laserCollat" : i[11],
    "hasShields" : i[12],
    "piecesNeeded" : i[13]
    }
    shipConstants.append(levelConstantsDict)

for i in range(len(spaceShipList)): spaceShipList[i].append(shipConstants[i])
# [   ( [Exhaust frames],Laser Image,[Ship Skins],{Player Constants} )   ]

# MAIN MENU ASSETS
menuList = []
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'A.png'))).convert_alpha()) # 'A' icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'O.png'))).convert_alpha()) # 'O' icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'center.png'))).convert_alpha()) # Center icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'left.png'))).convert_alpha()) # Left icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'right.png'))).convert_alpha()) # Right icon

menuMeteorDir = os.path.join(menuDirectory,'FlyingObjects')

for objPath in sorted(os.listdir(menuMeteorDir)): menuList.append(pygame.image.load(resources(os.path.join(menuMeteorDir,objPath))).convert_alpha())

# possible errors
recordsLoaded = False
donationsLoaded = False
cannotSave = False

# LOAD GAME RECORDS
if platform.system().lower() == 'windows' or platform.system().lower == 'linux': recordsPath = './gameRecords.txt' # For windows and linux
else: recordsPath = resources('gameRecords.txt') # For MacOS
try:
    with open(recordsPath,'rb') as file:
        gameRecords = pickle.load(file)
    recordsLoaded = True

except:
    gameRecords = {'highScore':0, 'longestRun':0, 'attempts':0, 'timePlayed':0}
    try:
        with open(recordsPath,'wb') as file:
            pickle.dump(gameRecords, file) # Try overwriting records
    except: cannotSave = True # Continue game without saving

# LOAD DONATION RECORDS
donations = {}
try:
    path = os.path.join(supportersDirectory,'Supporters.txt')
    with open(path,'r') as file:
        for line in file:
            key,value = line.strip().split(':')
            donations[key] = int(value)
        donationsLoaded = True
except: donationsLoaded = False

if len(donations) == 0: donationsLoaded = False
if donationsLoaded:
    maxDon = max(donations.values())
    lowDon = min(donations.values())
else: maxDon,lowDon = None,None

# LOAD DONATION SHIP ASSETS
donationShips = []
if donationsLoaded:
    donationShipsDir = os.path.join(supportersDirectory,'Images')
    for filename in sorted(os.listdir(donationShipsDir)):
        if filename.endswith('.png'):
            path = os.path.join(donationShipsDir, filename)
            donationShips.append(pygame.image.load(resources(path)).convert_alpha())

if len(donationShips)==0: donationsLoaded = False # Asset folder is empty, proceed without

timerFont = pygame.font.Font(gameFont, timerSize)

# SPAWN AREA
spawnWidth = int(screenSize[0] * (spawnRange[1] - spawnRange[0]))
spawnHeight = int(screenSize[1] * (spawnRange[1] - spawnRange[0]))
spawnOffsetX = int((screenSize[0] - spawnWidth) / 2)
spawnOffsetY = int((screenSize[1] - spawnHeight) / 2)
spawnAreaPoints = []
for i in range(spawnVertices):
    angle = i * 2 * 3.14159 / spawnVertices + (3.14159 / spawnVertices)
    x = screenSize[0]/2 + (spawnWidth / 2) * math.cos(angle)
    y = screenSize[1]/2 + (spawnHeight / 2) * math.sin(angle)
    spawnAreaPoints.append((x, y))

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
        self.score = 0
        self.thisPoint = Point(None)
        self.gameClock = 1
        self.pauseCount = 0
        self.clk = pygame.time.Clock()
        self.savedHighScore = gameRecords["highScore"]
        self.savedLongestRun = gameRecords["longestRun"]
        self.savedTotalAttempts = gameRecords["attempts"]
        self.obstacleSpeed = obstacleSpeed
        self.obstacleSize = obstacleSize
        self.maxObstacles = maxObstacles
        self.aggro = aggro
        self.obstacleBoundaries = obstacleBoundaries
        self.cloudSpeed = cloudSpeed
        self.attemptNumber = 1
        self.mainMenu = True # Assures start menu only runs when called
        self.sessionLongRun = 0 # Longest run this session
        self.gameConstants = []
        self.savedShipNum = 0
        self.savedShipLevel = 0
        self.unlockNumber = 0
        self.spinSpeed = spinSpeed
        self.cloudPos = cloudStart
        self.wipe = obstacleWipe
        self.explosions = []
        self.musicMuted = musicMuted

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

             # MUTE
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m): toggleMusic(game)

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

        # SHOW POINT SPAWN AREA
        if showSpawnArea: pygame.draw.polygon(screen, (255, 0, 0), spawnAreaPoints,1)

        # HUD
        self.showHUD(player)

        # PLAYER/POWERUP COLLISION DETECTION
        if pygame.sprite.collide_rect(player,self.thisPoint):
            if self.thisPoint.powerUp == "Red":
                player.fuel += player.maxFuel/4 # Replenish quarter tank
                if player.fuel > player.maxFuel: player.fuel = player.maxFuel
    
            elif self.thisPoint.powerUp == "Blue": player.shieldUp()
            self.score += 1
            self.thisPoint.kill()
            if not self.musicMuted: powerUpNoise.play()
            self.thisPoint = Point(player)

        # OBSTACLE/PLAYER COLLISION DETECTION
        if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask):
            if player.shields > 0: player.shieldDown()
            else:
                player.explode(game,obstacles) # Animation
                if not self.musicMuted: explosionNoise.play()
                menu.gameOver(self,player,obstacles) # Game over

        # OBSTACLE/LASER COLLISION DETECTION
        for laser in lasers:
            if pygame.sprite.spritecollide(laser,obstacles,True,pygame.sprite.collide_mask):
                if player.laserCollat: laser.kill()
                if not self.musicMuted: impactNoise.play()
                self.explosions.append(Explosion(self,laser))

        # DRAW OBSTACLE EXPLOSIONS
        for debris in self.explosions:
            if debris.finished: self.explosions.remove(debris)
            else: debris.update()


        # DRAW AND MOVE SPRITES
        player.movement()
        player.shoot(self,lasers,events)
        player.boost(events)
        player.wrapping()
        self.spawner(obstacles)
        obstacleMove(obstacles)

        # UPDATE HIGH SCORE
        if self.gameClock > self.sessionLongRun: self.sessionLongRun = self.gameClock

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

        # DRAW POINT
        screen.blit(self.thisPoint.image, self.thisPoint.rect)

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

        musicLoop() # Loop music

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

        # SHIELDS DISPLAY
        shieldRectWidth = shieldChunkSize * player.shieldPieces
        if player.shields > 0: shieldRectWidth = shieldChunkSize * player.shieldPiecesNeeded
        shieldRect = pygame.Rect(screenSize[0]/3, 5, shieldRectWidth, 5)
        fullShieldRectWidth = shieldChunkSize * player.shieldPiecesNeeded

        if player.hasShields:
            if player.shields > 0: pygame.draw.rect(screen,fullShieldColor,shieldRect)
            elif player.shieldPieces > 0: pygame.draw.rect(screen,shieldColor,shieldRect)

        else: fullShieldRectWidth = shieldChunkSize * 10

        # FUEL DISPLAY
        widthMultiplier = fullShieldRectWidth / (screenSize[0]/4)
        fuelRectWidth  = (screenSize[0]/4) * (player.fuel / player.maxFuel) * widthMultiplier
        fuelRect = pygame.Rect(screenSize[0]/3, 0, fuelRectWidth, 5)
        if player.boostDrain > 0 or player.laserCost > 0: pygame.draw.rect(screen, fuelColor,fuelRect)

        # TIMER DISPLAY
        timerDisplay = timerFont.render(str(self.gameClock), True, timerColor)
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright)

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

        # SCORE DISPLAY
        scoreNum = "Score " + str(self.score)
        scoreFont = pygame.font.Font(gameFont, scoreSize)
        scoreDisplay = scoreFont.render(scoreNum, True, levelColor)
        scoreRect = scoreDisplay.get_rect()
        scoreRect.topleft = (screenSize[0] - (2*scoreRect.width), levelRect.y)

        screen.blit(timerDisplay, timerRect)
        screen.blit(stageDisplay, stageRect)
        screen.blit(levelDisplay, levelRect)
        screen.blit(scoreDisplay, scoreRect)


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
        startRect = startDisplay.get_rect(center = (screenSize[0]/2,screenSize[1]/2))

        startHelpFont = pygame.font.Font(gameFont, helpSize)
        startHelpDisplay = startHelpFont.render("ESCAPE = Quit   SPACE = Start   F = Fullscreen   M = Mute   C = Credits", True, helpColor)
        startHelpRect = startHelpDisplay.get_rect(center = (screenSize[0]/2,screenSize[1]-screenSize[1]/7))

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

        versionFont = pygame.font.Font(gameFont,versionSize)
        versionDisplay = versionFont.render(version,True,versionColor)
        versionRect = versionDisplay.get_rect(topright = (startRect.right-versionSize,startRect.bottom-versionSize))

        bounceDelay = 5
        bounceCount = 0

        # DEFAULT SHIP SKIN UNLOCKS   ( spaceShipList[0] )
        if game.savedLongestRun >= 330: game.unlockNumber = len(spaceShipList[0][2])
        elif game.savedLongestRun >= 300: game.unlockNumber = len(spaceShipList[0][2]) - 1
        elif game.savedLongestRun >= 270: game.unlockNumber = len(spaceShipList[0][2]) - 2
        elif game.savedLongestRun >= 240: game.unlockNumber = len(spaceShipList[0][2]) - 3
        elif game.savedLongestRun >= 210: game.unlockNumber = len(spaceShipList[0][2]) - 4
        elif game.savedLongestRun >= 180: game.unlockNumber = len(spaceShipList[0][2]) - 5
        elif game.savedLongestRun >= 150: game.unlockNumber = len(spaceShipList[0][2]) - 6
        elif game.savedLongestRun >= 120: game.unlockNumber = len(spaceShipList[0][2]) - 7
        elif game.savedLongestRun >= 90: game.unlockNumber = len(spaceShipList[0][2]) - 8
        elif game.savedLongestRun >= 60: game.unlockNumber = len(spaceShipList[0][2]) - 9
        elif game.savedLongestRun >= 30: game.unlockNumber = len(spaceShipList[0][2]) - 10

        if game.unlockNumber < 0: game.unlockNumber = 0
        for imageNum in range(game.unlockNumber-1): player.nextSpaceShip() # Gets highest unlocked ship by default

        startOffset = 100
        startDelay = 1
        iconPosition, startDelayCounter = startOffset, 0

        while game.mainMenu:

            menuMusicLoop() # Keep music looping

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

                # MUTE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m): toggleMusic(game)

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
            screen.blit(versionDisplay,versionRect)
            screen.blit(startHelpDisplay, startHelpRect) # Game controls

            # SHOW SHIP CONTROLS
            if player.hasGuns: screen.blit(shootHelp,shootHelpRect)
            if player.boostSpeed > player.baseSpeed: screen.blit(boostHelp,boostHelpRect)
            if game.savedLongestRun >= 30 and len(spaceShipList[game.savedShipLevel][2]) > 1: screen.blit(skinHelpDisplay,skinHelpRect) # Show switch skin controls
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

    # PAUSE SCREEN
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
        pauseDisplay = pauseCountFont.render(pauseNum,True,levelColor)
        pauseRect = pauseDisplay.get_rect()
        pauseRect.center = (screenSize[0]/2,screenSize[1]-16)

        while paused:
            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage-1][0],(0,0))
            screen.blit(cloud,(0,game.cloudPos))
            game.showHUD(player)
            screen.blit(game.thisPoint.image, game.thisPoint.rect)
            screen.blit(playerBlit[0],playerBlit[1])
            pygame.mixer.music.pause()

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

                # UNPAUSE
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE):
                    pygame.mixer.music.unpause()
                    paused = False


    # GAME OVER SCREEN
    def gameOver(self,game,player,obstacles):
        global screen
        gameOver = True
        game.thisPoint = Point(None)
        pygame.mixer.music.stop()

        # Update game records
        newLongRun = False
        newHighScore = False

        try:
            with open(recordsPath,'rb') as file: outdatedRecords = pickle.load(file) # Load old records
        except: outdatedRecords = gameRecords # Continue with outdated records

        savedClock = outdatedRecords["timePlayed"] + game.gameClock # Update total time played
        game.savedTotalAttempts += 1 # Update total attempts

        updatedRecordsDict = {"highScore":game.savedHighScore, "longestRun":game.savedLongestRun, "attempts":game.savedTotalAttempts,"timePlayed":savedClock} # Updated records
        if game.sessionLongRun > game.savedLongestRun:
            newLongRun = True
            game.savedLongestRun = game.sessionLongRun
            updatedRecordsDict["longestRun"] = game.sessionLongRun

        if game.score > game.savedHighScore:
            newHighScore = True
            game.savedHighScore = game.score
            updatedRecordsDict["highScore"] = game.score

        try:
            with open(recordsPath,'wb') as file: pickle.dump(updatedRecordsDict,file) # Save updated records
        except: pass

        statsOffsetY = screenSize[1]/10
        statsSpacingY = screenSize[1]/20

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
        scoreLine = "Score " + str(game.score)
        highScoreLine = "High Score " + str(game.savedHighScore)
        newHighScoreLine = "New High Score! " + str(game.score)
        survivedLine = "Survived for " + str(game.gameClock) + " seconds"
        overallLongestRunLine = "Longest run  =  " + str(game.savedLongestRun) + " seconds"
        newLongestRunLine = "New longest run! " + str(game.sessionLongRun) + " seconds"
        levelLine = "Died at stage " + str(game.currentStage) + "  -  level " + str(game.currentLevel)
        attemptLine = str(game.attemptNumber) + " attempts this session, " + str(game.savedTotalAttempts) + " overall"
        timeWasted = "Time played = " + str(savedClock) + " seconds"

        # Display
        scoreDisplay = statFont.render(scoreLine, True, finalScoreColor)
        highScoreDisplay = statFont.render(highScoreLine, True, finalScoreColor)
        newHighScoreDisplay = statFont.render(newHighScoreLine, True, finalScoreColor)
        longestRunDisplay = statFont.render(overallLongestRunLine, True, finalScoreColor)
        survivedDisplay = statFont.render(survivedLine, True, finalScoreColor)
        levelDisplay = statFont.render(levelLine, True, finalScoreColor)
        newLongestRunDisplay = statFont.render(newLongestRunLine, True, finalScoreColor)
        attemptDisplay = statFont.render(attemptLine, True, finalScoreColor)
        timeWastedDisplay = statFont.render(timeWasted,True,finalScoreColor)
        exitDisplay = exitFont.render("TAB = Menu     SPACE = Restart    ESCAPE = Quit    C = Credits", True, helpColor)

        # Rects
        scoreRect = scoreDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 + statsOffsetY +statsSpacingY * 1))
        highScoreRect = highScoreDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 + statsOffsetY +statsSpacingY * 2))
        newHighScoreRect = newHighScoreDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 + statsOffsetY +statsSpacingY * 1.5))
        survivedRect = survivedDisplay.get_rect(center =(screenSize[0]/2, screenSize[1]/3 + statsOffsetY + statsSpacingY * 3))
        longestRunRect = longestRunDisplay.get_rect(center =(screenSize[0]/2, screenSize[1]/3 + statsOffsetY +statsSpacingY * 4))
        newLongestRunRect = newLongestRunDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 + statsOffsetY +statsSpacingY * 3.5))
        levelRect = levelDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 +statsOffsetY +statsSpacingY * 5))
        attemptRect = attemptDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 + statsOffsetY +statsSpacingY * 6))
        wastedRect = timeWastedDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]/3 +statsOffsetY +statsSpacingY * 7))
        exitRect = exitDisplay.get_rect(center =(screenSize[0]/2, screenSize[1]/3 + 2* statsOffsetY +statsSpacingY * 8))

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

        displayTextList = [scoreText, highScoreText, newHighScoreText, survivedText, longestRunText, newLongestRunText, levelText, attemptText, wastedText]


        while gameOver:

            # Background
            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            screen.blit(bgList[game.currentStage-1][1],(0,game.cloudPos))
            screen.blit(player.finalImg,player.finalRect) # Explosion

            pygame.draw.rect(screen, screenColor, [gameOverRect.x - 12,gameOverRect.y + 4,gameOverRect.width + 16, gameOverRect.height - 16],0,10)
            screen.blit(gameOverDisplay,gameOverRect)
            drawGameOverLabels(displayTextList,newHighScore,newLongRun)
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

                # WIPE

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB):
                    # SET DEFAULTS AND GO BACK TO MENU
                    game.gameClock = 0
                    game.currentLevel = 1
                    game.currentStage = 1
                    game.score = 0
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
                    game.score = 0
                    player.kill()
                    player.updatePlayerConstants(game)
                    game.killAllObstacles(obstacles)
                    game.resetAllLevels()
                    game.attemptNumber += 1
                    running = True
                    gameLoop()


    # CREDITS
    def creditScreen(self):
        global screen
        rollCredits = True
        posX = screenSize[0]/2
        posY = screenSize[1]/2

        creatorFont = pygame.font.Font(gameFont, creditsFontSize)
        creditsFont = pygame.font.Font(gameFont, creditsFontSize - 15)

        createdByLine = "Created by Mike Pistolesi"
        creditsLine = "with art by Collin Guetta"
        musicCreditsLine = '& music by Dylan Kusenko'

        createdByDisplay = creatorFont.render(createdByLine, True, creditsColor)
        creditsDisplay = creditsFont.render(creditsLine, True, creditsColor)
        musicCreditsDisplay = creditsFont.render(musicCreditsLine, True, creditsColor)

        createdByRect = createdByDisplay.get_rect(center = (posX, posY - screenSize[1]/15) )
        creditsRect = creditsDisplay.get_rect(center = (posX,posY))
        musicCreditsRect = musicCreditsDisplay.get_rect(center = (posX,posY+ screenSize[1]/15))

        bounceCount = 0
        direction = randomEightDirection()

        # random select names and contributions from dictionary
        if donationsLoaded:
            if len(donations) < maxExtras: extrasCap = len(donations)
            else: extrasCap = maxExtras
            extras = []
            if extrasCap == 1:
                extra = list(donations.items())[0]
                extras.append(extra)
                del donations[extra[0]]
            else:
                for i in range(extrasCap):
                    extra = random.choice(list(donations.items()))
                    extras.append(extra) # add to list
                    del donations[extra[0]] # pop from dictionary

            bgShips = []
            for ship in extras: bgShips.append(BackgroundShip(ship[0],ship[1]))

        while rollCredits:

            menuMusicLoop()

            for event in pygame.event.get():
                # EXIT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # MUTE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m): toggleMusic(game)

                # RETURN TO GAME
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_c or event.key == pygame.K_SPACE or event.key == pygame.K_TAB):
                    rollCredits = False

            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            screen.blit(bgList[game.currentStage-1][1],(0,game.cloudPos))

            # Load donations
            if donationsLoaded:
                for ship in bgShips:
                    ship.draw()
                    ship.move()
                    # off screen, add name back to pool and remove
                    if ship.offScreen():
                        bgShips.remove(ship)
                        donations[ship.text] = ship.scale
                        for i in extras:
                            if i[0] == ship.text:
                                extras.remove(i)
                                break

                # Assign a background ship object
                for newShip in range(maxExtras-len(bgShips)):
                    # get name from pool
                    if len(donations)==0:break
                    elif len(donations) == 1: extra = list(donations.items())[0]
                    else: extra = random.choice(list(donations.items()))
                    extras.append(extra)
                    del donations[extra[0]]
                    bgShips.append(BackgroundShip(extra[0],extra[1]))

            screen.blit(createdByDisplay,createdByRect)
            screen.blit(creditsDisplay,creditsRect)
            screen.blit(musicCreditsDisplay,musicCreditsRect)
            pygame.display.flip()

            # BOUNCE OFF EDGES
            if createdByRect.right > screenSize[0]: direction = rightDir[random.randint(0, len(rightDir) - 1)]
            if createdByRect.left < 0: direction = leftDir[random.randint(0, len(leftDir) - 1)]
            if musicCreditsRect.bottom > screenSize[1]: direction = bottomDir[random.randint(0, len(bottomDir) - 1)]
            if createdByRect.top < 0 : direction = topDir[random.randint(0, len(topDir) - 1)]

            if bounceCount == 0:
                if "N" in direction:
                    createdByRect.centery-= mainCreditsSpeed
                    creditsRect.centery-= mainCreditsSpeed
                    musicCreditsRect.centery-= mainCreditsSpeed

                if "S" in direction:
                    createdByRect.centery+= mainCreditsSpeed
                    creditsRect.centery+= mainCreditsSpeed
                    musicCreditsRect.centery+= mainCreditsSpeed

                if "E" in direction:
                    createdByRect.centerx+= mainCreditsSpeed
                    creditsRect.centerx+= mainCreditsSpeed
                    musicCreditsRect.centerx+= mainCreditsSpeed

                if "W" in direction:
                    createdByRect.centerx-= mainCreditsSpeed
                    creditsRect.centerx-= mainCreditsSpeed
                    musicCreditsRect.centerx-= mainCreditsSpeed

            bounceCount +=1
            if bounceCount >= 10: bounceCount = 0

        # Refill donation list
        if donationsLoaded:
            for supporter, contribution in extras:
                donations.update({supporter:contribution})


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
            self.hasShields = spaceShipList[game.savedShipLevel][3]["hasShields"]
            self.shieldPiecesNeeded,self.shieldPieces,self.shields = spaceShipList[game.savedShipLevel][3]["piecesNeeded"],0,0
            self.shieldPieces = 0
            self.shields = 0


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

                        # Boost animation
                        try:
                            screen.blit(self.lastThreeExhaustPos[0][0],self.lastThreeExhaustPos[0][1])
                            screen.blit(self.lastThreeExhaustPos[1][0],self.lastThreeExhaustPos[1][1])
                            screen.blit(self.lastThreeExhaustPos[2][0],self.lastThreeExhaustPos[2][1])
                        except: pass # will not have assets loaded in class variable until frame 3

                    else: self.speed = self.baseSpeed

                else:
                    self.speed = self.baseSpeed
                    events.boostCharge(self)


        # SHOOT ROCKETS/LASERS
        def shoot(self,game,lasers,events):
            if self.hasGuns and self.laserReady:
                key = pygame.key.get_pressed()
                if  (key[pygame.K_LCTRL] or key[pygame.K_RCTRL]) and self.fuel - self.laserCost > 0:
                    lasers.add(Laser(self))
                    if not game.musicMuted: laserNoise.play()
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
            self.hasShields = spaceShipList[game.savedShipLevel][3]["hasShields"]
            self.shieldPiecesNeeded = spaceShipList[game.savedShipLevel][3]["piecesNeeded"]


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


        def shieldUp(self):
            self.shieldPieces += 1
            if self.shieldPieces >= self.shieldPiecesNeeded:
                self.shieldPieces = 0
                self.shields += 1


        def shieldDown(self):
            self.shields -= 1
            # Waiting for assets


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
        try: self.image = obstacleImages[game.currentStage - 1][game.currentLevel-1]
        except: self.image = meteorList[random.randint(0,len(meteorList)-1)]
        self.image = pygame.transform.scale(self.image, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0
        spins = [-1,1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.active = False
        
    def activate(self):
        if self.rect.right >= 0 or self.rect.left <= screenSize[0] or self.rect.top <= 0 or self.rect.bottom >= screenSize[1]: self.active = True


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
        self.rect = laser.rect.copy()
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



# POWER UPS
class Point(pygame.sprite.Sprite):
    def __init__(self,player):
        super().__init__()
        self.powerUp = ''
        if not player or (not player.hasShields and player.boostDrain == 0 and player.laserCost == 0  and player.baseSpeed == player.boostSpeed): self.powerUp = "White"
        else:
            powerUps = powerUpList
            if not player.hasShields: powerUps.remove("Blue")
            if not player.hasGuns and player.baseSpeed == player.boostSpeed: powerUps.remove("Red")
            self.powerUp = powerUps[random.randint(0,len(powerUps)-1)]

        if self.powerUp == "Blue": self.image = pointsList[2]
        elif self.powerUp == "Red": self.image = pointsList[1]
        elif self.powerUp == "White": self.image = pointsList[0]
        self.image = pygame.transform.scale(self.image, (pointSize, pointSize))
        self.rect = self.image.get_rect(center = positionGenerator())
        self.mask = pygame.mask.from_surface(self.image)


# MENU METEOR ICONS
class Icon:
    def __init__(self):
        spins = [-1,1]
        self.speed = random.randint(1,maxIconSpeed)
        self.movement = getMovement(False)
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.image = menuList[random.randint(5,len(menuList)-1)]
        size = random.randint(minIconSize,maxIconSize)
        self.image = pygame.transform.scale(self.image, (size, size)).convert_alpha()
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

# BACKGROUND SHIPS
class BackgroundShip:
    def __init__(self,text,scale):
        self.scale = scale
        self.size = int(valueScaler(scale,minBackgroundShipSize,maxBackgroundShipSize,lowDon,maxDon))
        if self.size < minBackgroundShipSize:
            self.size = minBackgroundShipSize
            self.speed = maxBackgroundShipSpeed
        elif self.size > maxBackgroundShipSize:
            self.size = minBackgroundShipSize
            self.speed = minBackgroundShipSpeed

        self.speed = maxBackgroundShipSpeed/self.size
        if self.speed > maxBackgroundShipSpeed: self.speed = maxBackgroundShipSpeed
        elif self.speed < minBackgroundShipSpeed: self.speed = minBackgroundShipSpeed

        self.movement = getMovement(False)
        self.direction = self.movement[1]
        self.angle = getAngle(self.direction)
        self.text = text
        self.image = pygame.transform.scale(donationShips[random.randint(0, len(donationShips) - 1)], (self.size, self.size) ).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.count = 0
        self.font = pygame.font.Font(gameFont, int(self.size * 2/3))
        self.display = self.font.render(self.text, True, extraCreditsColor)
        self.displayRect = self.display.get_rect(center = self.rect.center)

    def move(self):
        if self.count >= backgroundShipDelay:
            if "N" in self.direction: self.rect.centery -= self.speed
            if "S" in self.direction: self.rect.centery += self.speed
            if "E" in self.direction: self.rect.centerx += self.speed
            if "W" in self.direction: self.rect.centerx -= self.speed
            self.displayRect.center = self.rect.center
            self.count = 0
        self.count +=1

    def draw(self):
        if not showBackgroundShips and not showSupporterNames: return
        drawing, drawee = rotateImage(self.image,self.rect,self.angle)
        supporterRect = self.display.get_rect(center = drawee.center)
        if showBackgroundShips: screen.blit(drawing,drawee)
        if showSupporterNames: screen.blit(self.display,supporterRect)

    # Returns true if off screen
    def offScreen(self):
        if showSupporterNames and not showBackgroundShips:
            if self.displayRect.bottom < 0 or self.displayRect.top > screenSize[1] or self.displayRect.left > screenSize[0] or self.displayRect.right < 0: return True
        else:
            if self.rect.bottom < 0 or self.rect.top > screenSize[1] or self.rect.left > screenSize[0] or self.rect.right < 0: return True


# ROTATE IMAGE
def rotateImage(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    rotatedRect = rotated.get_rect(center=rect.center)
    return rotated,rotatedRect


# GET INVERSE MOVEMENT DIRECTION
def movementReverse(direction):
    if direction == "N": return "S"
    elif direction == "S": return "N"
    elif direction == "E": return "W"
    elif direction == "W": return "E"
    elif direction == "NW": return "SE"
    elif direction == "NE": return "SW"
    elif direction == "SE": return "NW"
    elif direction == "SW": return "NE"


# GET RANDOM DIRECTION - include diagonal
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

    lowerX = random.randint(-obstacleSpawnRange[1],obstacleSpawnRange[0])
    upperX =  random.randint(screenSize[0], screenSize[0] + obstacleSpawnRange[1])
    lowerY  = random.randint(-obstacleSpawnRange[1],obstacleSpawnRange[0])
    upperY = random.randint(screenSize[1],screenSize[1]+obstacleSpawnRange[1])

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
        obs.activate()


# OFF SCREEN OBSTACLE REMOVAL
def obstacleRemove(obstacles):
    for obs in obstacles:
        if obs.active:
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
        if obs.rect.centery > screenSize[1]: obs.rect.centery = 0
        if obs.rect.centery < 0: obs.rect.centery = screenSize[1]
        if obs.rect.centerx > screenSize[0]: obs.rect.centerx = 0
        if obs.rect.centerx < 0: obs.rect.centerx = screenSize[0]


# POINT POSITION GENERATION
def getPosition():
    xRange = [screenSize[0] * spawnRange[0] , screenSize[0] * spawnRange[1] ]
    yRange = [screenSize[1] * spawnRange[0] , screenSize[1] * spawnRange[1] ]
    xNum = random.randint(xRange[0],xRange[1])
    yNum = random.randint(yRange[0],yRange[1])
    return [xNum,yNum]


# CHECK IF POINT IS IN SPAWN AREA
def pointValid(point):
    centerX, centerY = screenSize[0]/2, screenSize[1]/2
    lines = [((centerX + math.cos(angle + math.pi/spawnVertices)*spawnWidth/2, centerY + math.sin(angle + math.pi/spawnVertices)*spawnHeight/2), (centerX + math.cos(angle - math.pi/spawnVertices)*spawnWidth/2, centerY + math.sin(angle - math.pi/spawnVertices)*spawnHeight/2)) for angle in (i * math.pi/4 for i in range(8))]
    sameSide = [((point[0]-l[0][0])*(l[1][1]-l[0][1]) - (point[1]-l[0][1])*(l[1][0]-l[0][0]))  * ((centerX-l[0][0])*(l[1][1]-l[0][1]) - (centerY-l[0][1])*(l[1][0]-l[0][0])) >= 0  for l in lines]
    return all(sameSide)


# GET POSITION IN SPAWN AREA
def positionGenerator():
    while True:
        point = getPosition()
        if pointValid(point):
            return point


# GET ANGLE
def getAngle(direction):
    if direction == "N": return 0
    elif direction == "S": return 180
    elif direction == "E": return -90
    elif direction == "W": return 90
    elif direction == "NW": return 45
    elif direction == "NE": return -45
    elif direction == "SE": return 135
    elif direction == "SW": return -135


# GET SCALED VALUE
def valueScaler(amount, minimum, maximum, bottom, top):
    if bottom is None or top is None:
        return minimum
    elif top - bottom == 0:
        return (maximum + minimum) / 2
    else:
        scaled = (amount - bottom) / (top - bottom) * (maximum - minimum) + minimum
        return min(max(scaled, minimum), maximum)


game = Game() # Initialize game
menu = Menu() # Initialize menus

if not game.musicMuted: pygame.mixer.music.set_volume(musicVolume / 100)
else: pygame.mixer.music.set_volume(0)


def gameLoop():
    pygame.mixer.music.play()
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

