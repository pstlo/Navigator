# Navigator
# Copyright (c) 2023 Mike Pistolesi
# All rights reserved


import os,sys,random,math,platform,json,base64,time,pypresence,asyncio
from cryptography.fernet import Fernet
from dotenv import load_dotenv
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.display.init()
pygame.font.init()
pygame.mixer.init()

pygame.mouse.set_visible(False)

version = "v0.4.7"
#------------------GAME CONSTANTS--------------------------------------------------------------------------
# SCREEN
screenSize = [800,800] # Default = [800,800]
scaler = (screenSize[0] + screenSize[1]) / 1600 # Default = x + y / 2  / 800 == 1 / Make game difficulty scale to screen size
roundedScaler = int(round(scaler)) # For values that require whole numbers
fullScreen = False # Default = False
fps = 60 # Default = 60
performanceMode = False # Default = False / Overrules quality mode
qualityMode = False # Default = False

# HUD
showHUD = True
shieldColor = [0,0,255] # Default = [0,0,255] / Color of shield gauge
fullShieldColor = [0,255,255] # Default = [0,255,255] / Color of active shield gauge
fuelColor = [255,0,0] # Default = [255,0,0] / Color of fuel gauge
timerSize = 30 * roundedScaler # Default = 30
timerColor = [255,255,255] # Default = [255,255,255]
timerDelay = 1000 # Default = 1000
levelSize = 30 * roundedScaler # Default = 30
levelColor = [255,255,255] # Default = [255,255,255]
scoreSize = 30 * roundedScaler # Default = 30

# POWER UPS
spawnRange = [0.15, 0.85]
spawnVertices = 8 # Default = 8 / Vertices in shape of point spawn area (Octagon)
pointSize = 25  # Default = 20
shieldChunkSize = screenSize[0]/40 # Default = screen width / 40
boostCooldownTime = 2000 # Default = 2000 / Activates when fuel runs out to allow regen
showSpawnArea = False # Default = False
powerUpList = ["Shield", "Fuel", "Default", "Default"] # Shield/Fuel/Default, chances of spawn
playerShieldSize = 48 # Default = 64 / Shield visual size
shieldVisualDuration = 250 # Default = 250 / Shield visual duration
minDistanceToPoint = (screenSize[0] + screenSize[1]) / 16 # Default = 100
maxRandomAttempts = 100 # For random generator distances / max random attempts at finding a valid point

# BACKGROUND CLOUD
showBackgroundCloud = True # Default = True
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
versionSize = 25 # Default = 25
versionColor = [0,255,0] # Default = [0,255,0]

# STAGE UP
stageUpColor = [0,255,0] # Default = [0,255,0]
stageUpSize = 90 * roundedScaler # Default = 90
stageUpCloudStartPos = -900 # Default = -900
stageUpCloudSpeed = 8 * roundedScaler # Default = 8

# CREDITS
creditsFontSize = 55 * roundedScaler # Default = 55
creditsColor = [255,255,255] # Default = [255,255,255]
mainCreditsSpeed = 1 # Default = 1
mainCreditsDelay = 10 # Default = 10
extraCreditsSize = 30 * roundedScaler # Default = 30 / background ships text size
extraCreditsColor = [0,0,0] # Background ships text color
maxExtras = 3 # Default = 3 # max background ships
minBackgroundShipSpeed = 2 # Default = 1
maxBackgroundShipSpeed = 3 # Default = 3
minBackgroundShipSize = 50 # Default = 50
maxBackgroundShipSize = 100 # Default = 150
backgroundShipDelay = 15 # Default = 15 / Higher is slower
minBackgroundShipSpawnDelay = 500 # / Min delay (ms) before a ship spawns
maxBackgroundShipSpawnDelay = 3000 # / Max delay (ms) before a ship spawns
showBackgroundShips = True # Default = True
showSupporterNames = True # Default = True

# SOUNDS
musicMuted = False # Default = False
musicVolume = 10 # Default = 10 / Music volume / 100
sfxVolume = 5 # Default = 5 / SFX volume / 100

# MUSIC LOOP DURATION
menuLoopStart = 1100 # Default = 1100
menuLoopEnd = 12800 # Default = 12800
musicLoopStart = 25000 # Default = 25000
musicLoopEnd = 76000 # Default = 76000

# PLAYER
exhaustUpdateDelay = 50 # Default = 50 / Delay (ms) between exhaust animation frames
defaultToHighSkin = True # Default = True / Default to highest skin unlocked on game launch
defaultToHighShip = False # Default = False / Default to highest ship unlocked on game launch
drawExhaust = True # Default = True
# SHIP CONSTANTS
#                       [speed,fuel,maxFuel,regen,delay,boostSpeed,hasGuns,laserCost,laserSpeed,fireRate,boostDrain,collats,hasShields,shields,shieldPieces,piecesNeeded,laserDmg]
defaultShipAttributes = [ 5,    1,  20,     0.05, 50,   7,         False,  0,        0,         0,       0.4,        False, True,       0,      0,           5,          0       ]
gunShipAttributes =     [ 3,   10,  20,     0.05, 50,   10,        True,   0.4,      10,        250,     0.3,        False, False,      0,      0,           0,          1       ]
laserShipAttributes =   [ 2,   1,   1,      0,    0,    2,         True,   0,        10,        50,      0,          False, False,      0,      0,           0,          0.5     ]
hyperYachtAttributes =  [ 3,   20,  30,     0.1,  25,   12,        False,  0,        0,         0,       0.25,       False, False,      0,      0,           0,          0       ]
oldReliableAttributes = [ 4,   10,  15,     0.05, 50,   6,         True,   1,        5,         1000,    0.25,       True,  False,      0,      0,           0,          3       ]

#ADD SHIPS TO LIST
shipAttributes = [defaultShipAttributes,gunShipAttributes,laserShipAttributes,hyperYachtAttributes,oldReliableAttributes]

# LEVELS
levelTimer = 15 # Default = 15 / Time (seconds) between levels (can be overridden)
levelUpCloudSpeed = 25 # Default = 25 / Only affects levels preceded by wipe

# OBSTACLES
explosionDelay = 1 # Default = 1
obstacleSpawnRange = [0,1] # Default = [0,1]

# CAVES
caveStartPos = screenSize[1]*-2 # Default = -1600 / Cave start Y coordinate
caveSpeed = 20 # Default = 20 / Cave flyby speed

# SAVING
encryptGameRecords = True # Hide game records from user to prevent manual unlocks
invalidKeyMessage = "Get a key to save progress :)" # Saved to game records file if encryptGameRecords == True and key is invalid

# DISCORD PRESENCE
showPresence = True # Default = True
#----------------------------------------------------------------------------------------------------------------------


# FOR EXE/APP RESOURCES
def resources(relative):
    try: base = sys._MEIPASS # Running from EXE
    except Exception: base = os.path.abspath(".") # Running fron script
    return os.path.join(base, relative)


# SPECIFY UPDATE SCREEN UPDATE METHOD
if qualityMode: updateNotFlip = False
else: updateNotFlip = True # use update instead of flip for display updates

# GET SCREEN SIZE
displayInfo = pygame.display.Info()
displayInfo = displayInfo.current_w,displayInfo.current_h
displayInfo = pygame.Rect(0, 0, displayInfo[0], displayInfo[1]).center

# PERFORMANCE SETTINGS
if performanceMode:
    showBackgroundCloud = False
    drawExhaust = False


# GET SCREEN
def getScreen():
    if performanceMode:
        if fullScreen: return pygame.display.set_mode(screenSize, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED , depth = 16)
        else: return pygame.display.set_mode(screenSize,pygame.DOUBLEBUF,depth=16)
    elif qualityMode:
        if fullScreen: return pygame.display.set_mode(screenSize, pygame.FULLSCREEN| pygame.NOFRAME | pygame.SCALED | pygame.SRCALPHA,depth = 32)
        else: return pygame.display.set_mode(screenSize, pygame.NOFRAME | pygame.SRCALPHA,depth = 32)
    # Default
    else:
        if fullScreen: return pygame.display.set_mode(screenSize,pygame.FULLSCREEN | pygame.SCALED, depth = 0)
        else: return pygame.display.set_mode(screenSize,depth = 0)


# UPDATE DISPLAY
def displayUpdate():
    if not updateNotFlip: pygame.display.flip()
    else: pygame.display.update()


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
load_dotenv(os.path.join(currentDirectory,'.env'))

# INITIALIZE SCREEN
screen = getScreen()

# WINDOW
windowIcon = pygame.image.load(resources(os.path.join(currentDirectory,'Icon.png'))).convert_alpha()
pygame.display.set_caption('Navigator')
pygame.display.set_icon(windowIcon)
screenColor = [0,0,0] # Screen fill color

# DISCORD PRESENCE
presence = None


# ASYNCHRONOUSLY UPDATE DISCORD PRESENCE
async def getPresence(presence):
    try:
        await asyncio.wait_for(presence.connect(),timeout = 0.5)
        await presence.update(details='Playing Navigator', state='Navigating the depths of space', large_image='background', small_image = 'icon', buttons=[{'label': 'Play Navigator', 'url': 'https://pstlo.github.io/Navigator'}],start=int(time.time()))
    except:
        return None


if showPresence:
    try:
        presence = pypresence.AioPresence((Fernet(base64.b64decode(os.getenv('KEY1'))).decrypt(os.getenv('TOKEN'))).decode())
        asyncio.run(getPresence(presence))
    except: presence = None


# QUIT GAME
def quitGame():
    pygame.quit()
    sys.exit()


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


# Get path to game records based on OS
def getRecordsPath():
    if platform.system().lower() == 'windows' or platform.system().lower == 'linux': return './gameRecords.txt' # For windows and linux
    else: return resources('gameRecords.txt') # For MacOS


# ASSET LOADING
obstacleDirectory = os.path.join(currentDirectory, 'Obstacles') # Obstacle asset directory
meteorDirectory = os.path.join(obstacleDirectory, 'Meteors') # Meteor asset directory
ufoDirectory = os.path.join(obstacleDirectory, 'UFOs') # UFO asset directory
shipDirectory = os.path.join(currentDirectory, 'Spaceships') # Spaceship asset directory
caveDirectory = os.path.join(currentDirectory,'Caves') # Cave asset directory
backgroundDirectory = os.path.join(currentDirectory, 'Backgrounds') # Background asset directory
menuDirectory = os.path.join(currentDirectory, 'MainMenu') # Start menu asset directory
explosionDirectory = os.path.join(currentDirectory, 'Explosion') # Explosion animation directory
pointsDirectory = os.path.join(currentDirectory, 'Points') # Point image directory
soundDirectory = os.path.join(currentDirectory, 'Sounds') # Sound assets directory
supportersDirectory = os.path.join(currentDirectory,'Supporters') # Supporters directory
recordsPath = getRecordsPath() # Game records directory

# LOAD LEVELS
stageList = []
with open(resources(os.path.join(currentDirectory, 'Levels.json')), 'r') as file:
    stages = json.load(file)
    for stage in stages.values():
        levels = []
        for level in stage.values():
            level["START"] = False
            levels.append(level)
        stageList.append(levels)

# GET KEY
def getKey():
    try: return base64.b64decode(os.getenv('KEY'))
    except: return None # Could not load key


# STORE GAME RECORDS
def storeRecords(records):
    # No encryption
    if not encryptGameRecords:
        try:
            with open(recordsPath, 'w') as file: file.write(json.dumps(records))
        except: return # Continue without saving game records
    # With encryption
    else:
        if getKey() is None:
            with open(recordsPath,'w') as file: file.write(invalidKeyMessage)
            return # No key, continue without saving
        else:
            try:
                encrypted = Fernet(getKey()).encrypt(json.dumps(records).encode())
                with open(recordsPath,'wb') as file: file.write(encrypted)
            except:
                return # Failed to load encrypted records, continue without saving


# LOAD GAME RECORDS
def loadRecords():
    # No encryption
    if not encryptGameRecords:
        try:
            with open(recordsPath,'r') as file: return json.load(file)
        except:
            # Could not load records, try overwrite with default values
            gameRecords = {'highScore':0, 'longestRun':0, 'attempts':0, 'timePlayed':0}
            storeRecords(gameRecords)
            return gameRecords
    # With encryption
    else:
        try:
            # Return dictionary from encrypted records file
            with open(recordsPath,'rb') as file: encrypted = file.read()
            return json.loads(Fernet(getKey()).decrypt(encrypted))
        except:
            # Failed to load records
            gameRecords = {'highScore':0, 'longestRun':0, 'attempts':0, 'timePlayed':0}
            storeRecords(gameRecords) # Try creating new encrypted records file
            return gameRecords


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

# CAVE ASSETS
caveImages = []
for filename in sorted(os.listdir(caveDirectory)):
    if filename.endswith('.png'): caveImages.append(pygame.image.load(resources(os.path.join(caveDirectory,filename))).convert_alpha())

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
        pointsList.append(pygame.image.load(resources(path)).convert_alpha())

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

# PLAYER SHIELD ASSET
playerShield = pygame.transform.scale(pygame.image.load(resources(os.path.join(currentDirectory,"Shield.png"))),(playerShieldSize,playerShieldSize)).convert_alpha()

# MUSIC ASSET
pygame.mixer.music.load(resources(os.path.join(soundDirectory,"Soundtrack.mp3")))

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
    "startingShields" : i[13],
    "startingShieldPieces" : i[14],
    "piecesNeeded" : i[15],
    "laserDmg" : i[16]
    }
    shipConstants.append(levelConstantsDict)

for i in range(len(spaceShipList)): spaceShipList[i].append(shipConstants[i])
# Stores as -> [ ( [Exhaust frames],Laser Image,[Ship Skins],{Player Constants} ) ]

# MAIN MENU ASSETS
menuList = []
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'A.png'))).convert_alpha()) # 'A' icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'O.png'))).convert_alpha()) # 'O' icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'center.png'))).convert_alpha()) # Center icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'left.png'))).convert_alpha()) # Left icon
menuList.append(pygame.image.load(resources(os.path.join(menuDirectory,'right.png'))).convert_alpha()) # Right icon

menuMeteorDir = os.path.join(menuDirectory,'FlyingObjects')
for objPath in sorted(os.listdir(menuMeteorDir)): menuList.append(pygame.image.load(resources(os.path.join(menuMeteorDir,objPath))).convert_alpha())

# LOAD DONATION RECORDS
donations = {}
try:
    path = os.path.join(supportersDirectory,'Supporters.txt')
    with open(path,'r') as file:
        for line in file:
            try:
                key,value = line.strip().split(':')
                donations[key] = int(value)
            except:pass
except: pass

if len(donations) > 0:
    maxDon = max(donations.values())
    lowDon = min(donations.values())
else: maxDon,lowDon = None,None

# LOAD DONATION SHIP ASSETS
donationShips = []
donationShipsDir = os.path.join(supportersDirectory,'Images')
for filename in sorted(os.listdir(donationShipsDir)):
    if filename.endswith('.png'):
        path = os.path.join(donationShipsDir, filename)
        donationShips.append(pygame.image.load(resources(path)).convert_alpha())

# UNLOCKS
unlockTimePerLevels = [] # For time based unlocks
totalLevels = 0

for stage in stageList: totalLevels += len(stage) # Get total number of levels
totalTime = totalLevels * levelTimer # multiply by time per level

# Calculate time per unlock for each ship level
for shipInd in range(len(spaceShipList)):
    timePerUnlock = totalTime/len(spaceShipList[shipInd][2])
    if timePerUnlock == totalTime: unlockTimePerLevels.append(None) # No other skins for this level
    else: unlockTimePerLevels.append(int(timePerUnlock))

expectedPointsPerLevel = 12 # In testing
totalShipTypes = len(spaceShipList) # For score based unlocks
totalPointsForUnlock = totalLevels * expectedPointsPerLevel # Points in game for all unlocks
pointsForUnlock = int(totalPointsForUnlock/expectedPointsPerLevel)

timerFont = pygame.font.Font(gameFont, timerSize)

# POINT SPAWN AREA
spawnWidth = int(screenSize[0] * (spawnRange[1] - spawnRange[0]))
spawnHeight = int(screenSize[1] * (spawnRange[1] - spawnRange[0]))
spawnOffsetX = int((screenSize[0] - spawnWidth) / 2)
spawnOffsetY = int((screenSize[1] - spawnHeight) / 2)
spawnAreaPoints = []

for i in range(spawnVertices):
    angle = i * 2 * 3.14159 / spawnVertices + (3.14159 / spawnVertices)
    x = screenSize[0]/2 + (spawnWidth / 2) * math.cos(angle)
    y = screenSize[1]/2 + (spawnHeight / 2) * math.sin(angle)
    spawnAreaPoints.append((x, y)) # Vertices of spawn area

# "ALL" Spawn pattern / also used for random bounces in credits screen
topDir = ["S", "E", "W", "SE", "SW"]
leftDir = ["E", "S", "N", "NE", "SE"]
bottomDir = ["N", "W", "E", "NE", "NW"]
rightDir = ["W", "N", "S", "NW", "SW"]



# GAME
class Game:
    def __init__(self,records):

        self.gameConstants = stageList

        # Level constants
        self.obstacleSpeed = self.gameConstants[0][0]["obstacleSpeed"]
        self.obstacleSize = self.gameConstants[0][0]["obstacleSize"]
        self.maxObstacles = self.gameConstants[0][0]["maxObstacles"]
        self.spawnPattern = self.gameConstants[0][0]["obstacleSpawn"]
        self.obstacleBoundaries = self.gameConstants[0][0]["obstacleBounds"] # Obstacle handling at screen border
        self.levelType = self.gameConstants[0][0]["levelType"]
        self.wipe = self.gameConstants[0][0]["wipeObstacles"] # Old obstacle handling
        self.spinSpeed = self.gameConstants[0][0]["obstacleSpin"] # Obstacle spin speed
        self.angle = self.gameConstants[0][0]["levelAngle"] # Game rotation
        self.target = self.gameConstants[0][0]["obstacleTarget"]
        self.obsHealth = self.gameConstants[0][0]["obstacleHealth"]
        self.cloudSpeed = cloudSpeed

        self.currentLevel = 1
        self.currentStage = 1
        self.score = 0 # Points collected
        self.thisPoint = Point(None,None) # Currently active point (starts with default)
        self.lastPointPos = self.thisPoint.rect.center # Last point's position for spacing
        self.gameClock = 1
        self.pauseCount = 0
        self.attemptNumber = 1
        self.mainMenu = True # Assures start menu only runs when called
        self.sessionLongRun = 0 # Longest run this session
        self.skipAutoSkinSelect = False # For re-entering home menu from game over screen
        self.savedSkin = 0 # Saved ship skin
        self.savedShipLevel = 0 # Saved ship type
        self.shipUnlockNumber = 0 # Number of unlocked ships
        self.skinUnlockNumber = 0 # Number of unlocked skins for current ship
        self.cloudPos = cloudStart # Background cloud position
        self.explosions = [] # Obstacle explosions
        self.cave,self.caveIndex = None, 0 # For cave levels
        self.musicMuted = musicMuted
        self.clk = pygame.time.Clock() # Gameclock
        self.records = records # Game records dictionary

        # STORE LEVEL 1 VALUES
        self.savedConstants = {
                "obstacleSpeed" : self.obstacleSpeed,
                "obstacleSize" : self.obstacleSize,
                "maxObstacles" : self.maxObstacles,
                "obstacleBounds" : self.obstacleBoundaries,
                "obstacleSpin" : self.spinSpeed,
                "obstacleSpawn" : self.spawnPattern,
                "wipeObstacles" : self.wipe,
                "levelType":self.levelType,
                "levelAngle":self.angle,
                "obstacleTarget":self.target,
                "obstacleHealth":self.obsHealth
                }


    # MAIN GAME LOOP
    def update(self,player,obstacles,menu,events,lasers):
        for event in pygame.event.get():

            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
                quitGame()

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

            # SHIELD VISUAL
            if event.type == events.shieldVisualDuration: player.showShield = False

        # BACKGROUND
        screen.fill(screenColor)
        screen.blit(bgList[self.currentStage - 1][0], (0,0) )

        # CLOUD ANIMATION
        if showBackgroundCloud:
            cloudImg = bgList[self.currentStage - 1][1]
            cloudRect = cloudImg.get_rect(center = (screenSize[0]/2,self.cloudPos))
            if cloudRect.bottom >= 0 and cloudRect.top <= screenSize[1]: screen.blit(cloudImg, cloudRect) # Draw cloud
            elif cloudRect.top > screenSize[1]: self.cloudPos = cloudStart
            self.cloudPos += self.cloudSpeed

        # SHOW POINT SPAWN AREA (Testing)
        if showSpawnArea: pygame.draw.polygon(screen, (255, 0, 0), spawnAreaPoints,1)

        # DRAW POINT
        screen.blit(self.thisPoint.image, self.thisPoint.rect)

        # CAVES
        if self.levelType == "CAVE" or self.levelType == "BOTH":
            if self.cave is None: # SPAWN A CAVE
                self.cave = Caves(self.caveIndex)
                if self.caveIndex + 1 < len(caveImages) - 1: self.caveIndex+=1

            self.cave.update()
            if self.cave.rect.top <= screenSize[1] and self.cave.rect.bottom >= 0:
                screen.blit(self.cave.image,self.cave.rect) # DRAW CAVE
                # COLLISION DETECTION
                if pygame.sprite.collide_mask(self.cave,player):
                    if player.shields > 0: player.shieldDown(events)
                    else:
                        player.explode(game,obstacles) # explosion
                        if not self.musicMuted: explosionNoise.play()
                        menu.gameOver(self,player,obstacles) # Game over

        # EXITING CAVE
        elif self.cave is not None and self.cave.leave:
            if self.cave.rect.top > screenSize[1]:
                self.cave.kill()
                self.cave = None
            else:
                self.cave.update()
                screen.blit(self.cave.image,self.cave.rect)

        # HUD
        if showHUD: self.showHUD(player)

        # PLAYER/POWERUP COLLISION DETECTION
        if pygame.sprite.collide_mask(player,self.thisPoint):
            if self.thisPoint.powerUp == "Fuel": # Fuel cell collected
                player.fuel += player.maxFuel/4 # Replenish quarter tank
                if player.fuel > player.maxFuel: player.fuel = player.maxFuel

            elif self.thisPoint.powerUp == "Shield": player.shieldUp() # Shield piece collected
            self.score += 1
            self.thisPoint.kill()
            if not self.musicMuted: powerUpNoise.play()
            self.lastPointPos = self.thisPoint.rect.center # Save last points position
            self.thisPoint = Point(player,self.lastPointPos) # spawn new point

        # UPDATE PLAYER
        player.movement()
        player.shoot(self,lasers,events)
        player.boost(events)
        player.wrapping()

        # ROTATE PLAYER
        newBlit = rotateImage(player.image,player.rect,player.angle)

        # ROTATE EXHAUST
        if drawExhaust: newExhaustBlit = rotateImage(spaceShipList[game.savedShipLevel][0][player.exhaustState-1],player.rect,player.angle)

        # DRAW PLAYER
        screen.blit(newBlit[0],newBlit[1])

        # DRAW EXHAST
        if drawExhaust:
            if game.savedShipLevel != 1: screen.blit(newExhaustBlit[0],newExhaustBlit[1])

        # DRAW SHIELD
        if player.showShield:
            shieldImg,shieldImgRect = rotateImage(playerShield, player.rect, player.angle)
            screen.blit(shieldImg,shieldImgRect)

        # UPDATE BOOST ANIMATION / currently only 3 frames
        if drawExhaust:
            player.lastThreeExhaustPos[2] = player.lastThreeExhaustPos[1]
            player.lastThreeExhaustPos[1] = player.lastThreeExhaustPos[0]
            player.lastThreeExhaustPos[0] =  newExhaustBlit

        # DRAW LASERS
        self.laserUpdate(lasers,player)

        # UPDATE OBSTACLES
        if self.levelType == "OBS" or self.levelType == "BOTH":

            # OBSTACLE/PLAYER COLLISION DETECTION
            if pygame.sprite.spritecollide(player,obstacles,False,pygame.sprite.collide_mask):
                if player.shields > 0:
                    player.shieldDown(events)

                else:
                    player.explode(game,obstacles) # Animation
                    if not self.musicMuted: explosionNoise.play()
                    menu.gameOver(self,player,obstacles) # Game over

            # OBSTACLE MOVEMENT
            for obs in obstacles:
                obs.move(player)
                obs.activate() # Activate if on screen
                if obs.active:
                    # OBSTACLE/LASER COLLISION DETECTION
                    if pygame.sprite.spritecollide(obs,lasers,not player.laserCollat,pygame.sprite.collide_mask):
                        if obs.health - player.damage > 0: obs.health -= player.damage
                        else:
                            obs.kill()
                            obstacles.remove(obs)
                            if not self.musicMuted: impactNoise.play()
                            self.explosions.append(Explosion(self,obs))

                    # OBSTACLE/CAVE COLLISION DETECTION
                    elif self.cave is not None and pygame.sprite.collide_mask(obs,self.cave):
                        if not self.musicMuted: impactNoise.play()
                        self.explosions.append(Explosion(self,obs))
                        obs.kill()

                    # ROTATE AND DRAW OBSTACLE
                    if not performanceMode:
                        obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle
                        if obs.angle >= 360: obs.angle = -360
                        if obs.angle < 0: obs.angle +=360
                        newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
                        screen.blit(newBlit[0],newBlit[1]) # Blit obstacles

                    # OBSTACLE BOUNDARY HANDLING
                    obs.bound(obstacles)

            if performanceMode:obstacles.draw(screen) # Potential performance improvement

            # DRAW OBSTACLE EXPLOSIONS
            for debris in self.explosions:
                if debris.finished: self.explosions.remove(debris)
                else: debris.update()

        # UPDATE HIGH SCORE
        if self.gameClock > self.sessionLongRun: self.sessionLongRun = self.gameClock

        # LEVEL UP
        self.levelUpdater(player,obstacles,events)

        if self.levelType == "OBS" or self.levelType == "BOTH": self.spawner(obstacles,player) # Spawn obstacles

        musicLoop() # Loop music

        # UPDATE SCREEN
        player.lastAngle = player.angle # Save recent player orientation
        player.angle = game.angle # Reset player orientation
        displayUpdate()
        self.clk.tick(fps)


    # SET GAME CONSTANTS TO DEFAULT
    def resetGameConstants(self):
        self.obstacleSpeed = self.savedConstants["obstacleSpeed"]
        self.obstacleSize = self.savedConstants["obstacleSize"]
        self.maxObstacles = self.savedConstants["maxObstacles"]
        self.obstacleBoundaries = self.savedConstants["obstacleBounds"]
        self.spinSpeed = self.savedConstants["obstacleSpin"]
        self.spawnPattern = self.savedConstants["obstacleSpawn"]
        self.wipe = self.savedConstants["wipeObstacles"]
        self.levelType = self.savedConstants["levelType"]
        self.angle = self.savedConstants["levelAngle"]
        self.target = self.savedConstants["obstacleTarget"]
        self.health = self.savedConstants["obstacleHealth"]
        self.cloudSpeed = cloudSpeed
        self.cloudPos = cloudStart


    # DRAW CLOUD OUTSIDE OF MAIN LOOP
    def showBackgroundCloud(self):
        if showBackgroundCloud:
            cloudImg = bgList[game.currentStage - 1][1]
            cloudRect = cloudImg.get_rect(center = (screenSize[0]/2,game.cloudPos))
            if cloudRect.bottom >= 0 and cloudRect.top <= screenSize[1]: screen.blit(cloudImg, cloudRect) # Draw cloud


    # Draw frame outside of main loop **** revisit
    def alternateUpdate(self,player,obstacles,events):
        player.alternateMovement(self) # not sure why
        player.movement()              # this works
        player.wrapping()
        screen.fill(screenColor)
        screen.blit(bgList[self.currentStage-1][0],(0,0)) # Draw background
        self.showBackgroundCloud()
        self.cloudPos += self.cloudSpeed
        if self.cave is not None and self.levelType == "CAVE" or self.levelType == "BOTH":
            self.cave.update()
            if self.cave.rect.top <= screenSize[1] and self.cave.rect.bottom >= 0: screen.blit(self.cave.image,self.cave.rect) # DRAW CAVE

        obstacleMove(player,obstacles)
        for obs in obstacles:
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1])
            obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle


    # UPDATE GAME CONSTANTS
    def levelUpdater(self,player,obstacles,events):

        # UPDATES STAGE
        if self.currentStage < len(self.gameConstants): # Make sure there is a next stage
            if self.gameConstants[self.currentStage][0]["startTime"] == self.gameClock and not self.gameConstants[self.currentStage][0]["START"]: # Next stage's first level's activation time reached
                self.gameConstants[self.currentStage][0]["START"] = True # Mark as activated
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
                        if obs.rect.top <= stageUpRect.bottom: obs.kill()

                    screen.blit(stageUpCloud,stageUpRect) # Draw cloud
                    screen.blit(stageUpDisplay,(stageUpRect.centerx - screenSize[0]/5, stageUpRect.centery)) # Draw "STAGE UP" text
                    game.showHUD(player)
                    screen.blit(img,imgRect) # Draw player
                    displayUpdate()
                    stageUpRect.centery += stageUpCloudSpeed
                    self.clk.tick(fps)

                    if stageUpRect.centery >= screenSize[1]/2 and stageWipe:
                        self.currentStage += 1
                        self.currentLevel = 1
                        stageWipe = False

                    elif stageUpRect.centery >= screenSize[1] * 2: stageUp = False

        # UPDATES LEVEL
        for levelDict in self.gameConstants[self.currentStage-1]:
            if levelDict["startTime"] == self.gameClock and not levelDict["START"] and ( (self.currentLevel > 1 or self.currentStage > 1) or (len(self.gameConstants[0]) > 1 and self.gameClock >= self.gameConstants[0][1]["startTime"]) ):
                if self.gameConstants[self.currentStage-1][self.currentLevel-1]["wipeObstacles"]:
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
                        displayUpdate()
                        levelUpRect.centery += levelUpCloudSpeed

                        if levelUpRect.top >= screenSize[1]: levelUp = False
                        self.clk.tick(fps)

                levelDict["START"] = True
                self.obstacleBoundaries = levelDict["obstacleBounds"]
                self.obstacleSpeed = levelDict["obstacleSpeed"]
                self.maxObstacles = levelDict["maxObstacles"]
                self.obstacleSize = levelDict["obstacleSize"]
                self.spinSpeed = levelDict["obstacleSpin"]
                self.spawnPattern = levelDict["obstacleSpawn"]
                self.wipe = levelDict["wipeObstacles"]
                self.levelType = levelDict["levelType"]
                self.angle = levelDict["levelAngle"]
                self.target = levelDict["obstacleTarget"]
                self.obsHealth = levelDict["obstacleHealth"]
                if self.cave is not None: self.cave.leave = True # Set cave for exit
                self.cloudSpeed += cloudSpeedAdder
                self.currentLevel += 1
                break


    # RESET LEVEL PROGRESS
    def resetAllLevels(self):
        for stage in self.gameConstants:
            for levels in stage:
                levels["START"] = False


    # REMOVE ALL OBSTACLES
    def killAllObstacles(self,obstacles):
        for obstacle in obstacles: obstacle.kill()


    # HUD ( Needs optimization )
    def showHUD(self,player):

        # BORDER
        barBorder = pygame.Rect(screenSize[0]/3, 0, (screenSize[0]/3), 10)
        if player.hasShields or player.laserCost>0 or player.boostSpeed > player.baseSpeed or player.boostDrain > 0: pygame.draw.rect(screen,[0,0,0],barBorder)

        # SHIELDS DISPLAY
        if player.hasShields:
            currentShieldPieces = player.shieldPieces/player.shieldPiecesNeeded
            shieldRectWidth = (0.9*barBorder.width) * currentShieldPieces
            if player.shields > 0: shieldRectWidth = barBorder.width*0.99
            shieldRect = pygame.Rect(screenSize[0]/3, 5, shieldRectWidth, 5)
            shieldRect.centerx = barBorder.centerx
            fullShieldRectWidth = shieldChunkSize * player.shieldPiecesNeeded
            if player.shields > 0: pygame.draw.rect(screen,fullShieldColor,shieldRect)
            elif player.shieldPieces > 0: pygame.draw.rect(screen,shieldColor,shieldRect)

        # FUEL DISPLAY
        if player.boostDrain > 0 or player.laserCost > 0:
            currentFuel = player.fuel/player.maxFuel
            fuelRectWidth = currentFuel * (0.99*barBorder.width)
            fuelRect = pygame.Rect(screenSize[0]/3, 0, fuelRectWidth, 5)
            if player.hasShields:fuelRect.centerx = barBorder.centerx
            else: fuelRect.center = barBorder.center
            pygame.draw.rect(screen, fuelColor,fuelRect)

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
    def spawner(self,obstacles,player):
        if len(obstacles) < self.maxObstacles:
            obstacle = Obstacle(self.spawnPattern,self.target,[player.rect.centerx,player.rect.centery]) # Create new obstacle with specified spawn pattern
            obstacles.add(obstacle)


    # Update all lasers
    def laserUpdate(self,lasers,player):
        for laser in lasers:
            laser.move(player)
            screen.blit(laser.image,laser.rect)


    # Reset gameclock to 0
    def resetClock(self): self.gameClock = 0


    # Gets number of skins unlocked
    def getUnlocks(self,numSkins,time):
        if time == None: return 0
        else:
            unlockTime = totalTime
            prevUnlockIndex = 0
            unlockNum = 0
            for unlock in range(numSkins-1):
                if self.records["longestRun"] >= unlockTime: return numSkins - prevUnlockIndex
                else:
                    prevUnlockIndex +=1
                    unlockTime -= time
            if unlockNum <= 0:
                if self.records["longestRun"] >= time: return 1
                else: return 0
            else: return unlockNum


    # Get number of skins unlocked for a specified level number
    def skinsUnlocked(self,level): return self.getUnlocks(len(spaceShipList[level][2]),unlockTimePerLevels[level])


    # RESTART GAME
    def reset(self,player,obstacles):
        self.gameClock = 0
        self.currentLevel = 1
        self.currentStage = 1
        self.score = 0
        self.attemptNumber += 1
        self.cave = None
        self.killAllObstacles(obstacles)
        self.resetAllLevels()
        player.kill()



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

        # PLAYER SHIELD VISUAL DURATION
        self.shieldVisualDuration = pygame.USEREVENT + 5


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

    def showShield(self): pygame.time.set_timer(self.shieldVisualDuration,shieldVisualDuration)



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

        # UPDATE UNLOCKS
        if game.records["highScore"] < pointsForUnlock: game.shipUnlockNumber = 0
        elif game.records["highScore"] >= totalPointsForUnlock: game.shipUnlockNumber = len(spaceShipList) - 1
        else:
            if game.records["highScore"] == pointsForUnlock or game.records["highScore"] < 2 * pointsForUnlock: game.shipUnlockNumber = 1
            else:
                game.shipUnlockNumber = 0
                startPoints = pointsForUnlock
                for i in range(totalShipTypes):
                    if game.records["highScore"] >= startPoints:
                        game.shipUnlockNumber += 1
                    else: break
                    startPoints += pointsForUnlock

        game.skinUnlockNumber = game.skinsUnlocked(game.savedShipLevel)

        if defaultToHighSkin and not game.skipAutoSkinSelect:
            for i in range(game.skinUnlockNumber): player.nextSkin() # Gets highest unlocked skin by default
        elif game.skipAutoSkinSelect:
            for i in range(game.savedSkin): player.nextSkin()
        if defaultToHighShip:
            if game.savedShipLevel != game.shipUnlockNumber:
                for i in range(game.shipUnlockNumber): player.toggleSpaceShip(game,True) # Gets highest unlocked ship by default

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

                    game.savedSkin = player.currentImageNum

                    while iconPosition > 0:

                        if startDelayCounter >= startDelay: startDelayCounter = 0
                        else: startDelayCounter +=1

                        # Start animation
                        screen.fill(screenColor)
                        screen.blit(bgList[game.currentStage - 1][0],(0,0))
                        screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Current spaceship
                        displayUpdate()

                        if startDelayCounter >= startDelay: iconPosition-=1

                    game.mainMenu = False
                    return

                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # NEXT SPACESHIP SKIN
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                    player.nextSkin()

                # PREVIOUS SPACESHIP SKIN
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    player.lastSkin()

                # NEXT SHIP TYPE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_w or event.key == pygame.K_UP):
                    player.toggleSpaceShip(game,True)

                # PREVIOUS SHIP TYPE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_s or event.key == pygame.K_DOWN):
                    player.toggleSpaceShip(game,False)

                # MUTE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m): toggleMusic(game)

                # CREDITS
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c: menu.creditScreen()

                # QUIT
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE): quitGame()

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
            screen.blit(versionDisplay,versionRect) # Version info
            screen.blit(startHelpDisplay, startHelpRect) # Game controls

            # SHOW SHIP CONTROLS
            if player.hasGuns: screen.blit(shootHelp,shootHelpRect)
            if player.boostSpeed > player.baseSpeed: screen.blit(boostHelp,boostHelpRect)
            if unlockTimePerLevels[game.savedShipLevel] != None and game.records["longestRun"] >= unlockTimePerLevels[game.savedShipLevel] and len(spaceShipList[game.savedShipLevel][2]) > 1: screen.blit(skinHelpDisplay,skinHelpRect) # Show switch skin controls
            if game.shipUnlockNumber > 0: screen.blit(shipHelpDisplay,shipHelpRect)
            screen.blit(player.image, (player.rect.x,player.rect.y + startOffset)) # Current spaceship
            # LOGO LETTERS
            screen.blit(menuList[0],(-14 + startRect.left + menuList[0].get_width() - menuList[0].get_width()/8,screenSize[1]/2 - 42)) # "A" symbol
            screen.blit(menuList[1],(-42 + screenSize[0] - startRect.centerx + menuList[1].get_width() * 2,screenSize[1]/2 - 42)) # "O" symbol

            # UFO ICONS
            screen.blit(menuList[2],(screenSize[0]/2 - menuList[2].get_width()/2,screenSize[1]/8)) # Big icon
            screen.blit(menuList[3],leftRect) # Left UFO
            screen.blit(menuList[4],rightRect) # Right UFO

            displayUpdate()


    # PAUSE SCREEN
    def pause(self,game,player,obstacles,lasers):
        global screen
        pygame.mixer.music.pause()
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
            game.showBackgroundCloud()

            if game.levelType == "CAVE" or game.levelType == "BOTH":
                screen.blit(game.cave.image,game.cave.rect)

            game.showHUD(player)
            screen.blit(game.thisPoint.image, game.thisPoint.rect)
            screen.blit(playerBlit[0],playerBlit[1])

            if player.showShield:
                shieldImg,shieldImgRect = rotateImage(playerShield, player.rect, player.angle)
                screen.blit(shieldImg,shieldImgRect)

            if not performanceMode:
                for obs in obstacles: # Draw obstacles
                    newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
                    screen.blit(newBlit[0],newBlit[1])
            else: obstacles.draw(screen)

            lasers.draw(screen)

            screen.blit(pauseDisplay, pauseRect)
            screen.blit(pausedDisplay,pausedRect)
            displayUpdate()

            for event in pygame.event.get():
                # EXIT
                if event.type == pygame.QUIT: quitGame()

                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # UNPAUSE
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE):
                    pygame.mixer.music.unpause()
                    paused = False


    # GAME OVER SCREEN
    def gameOver(self,game,player,obstacles):
        global screen
        gameOver = True
        game.thisPoint = Point(None,None)
        pygame.mixer.music.stop()

        # Update game records
        newLongRun = False
        newHighScore = False

        game.records["timePlayed"] += game.gameClock # Update total time played
        game.records["attempts"] += 1 # Update total attempts

        if game.sessionLongRun > game.records["longestRun"]:
            newLongRun = True
            game.records["longestRun"] = game.sessionLongRun

        if game.score > game.records["highScore"]:
            newHighScore = True
            game.records["highScore"] = game.score

        storeRecords(game.records)

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
        highScoreLine = "High Score " + str(game.records["highScore"])
        newHighScoreLine = "New High Score! " + str(game.score)
        survivedLine = "Survived for " + str(game.gameClock) + " seconds"
        overallLongestRunLine = "Longest run  =  " + str(game.records["longestRun"]) + " seconds"
        newLongestRunLine = "New longest run! " + str(game.sessionLongRun) + " seconds"
        levelLine = "Died at stage " + str(game.currentStage) + "  -  level " + str(game.currentLevel)
        attemptLine = str(game.attemptNumber) + " attempts this session, " + str(game.records["attempts"]) + " overall"
        timeWasted = "Time played = " + str(game.records["timePlayed"]) + " seconds"

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
            game.showBackgroundCloud()

            if game.levelType == "CAVE" or game.levelType == "BOTH": screen.blit(game.cave.image,game.cave.rect)
            screen.blit(player.finalImg,player.finalRect) # Explosion

            pygame.draw.rect(screen, screenColor, [gameOverRect.x - 12,gameOverRect.y + 4,gameOverRect.width + 16, gameOverRect.height - 16],0,10)
            screen.blit(gameOverDisplay,gameOverRect)
            drawGameOverLabels(displayTextList,newHighScore,newLongRun)
            screen.blit(exitDisplay,exitRect)
            displayUpdate()

            for event in pygame.event.get():

                # EXIT
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT: quitGame()

                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # CREDITS
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_c): menu.creditScreen()

                # WIPE

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB):
                    # SET DEFAULTS AND GO BACK TO MENU
                    game.reset(player,obstacles)
                    game.mainMenu = True
                    game.skipAutoSkinSelect = True
                    gameLoop()

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    # SET DEFAULTS AND RESTART GAME
                    game.reset(player,obstacles)
                    player.updatePlayerConstants(game)
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

        extras = []
        bgShips = []
        waitToSpawn = True
        backGroundShipSpawnEvent = pygame.USEREVENT + 6
        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(minBackgroundShipSpawnDelay,maxBackgroundShipSpawnDelay))

        if len(donations) == 0: extrasCap = maxExtras

        elif len(donations) > 0:
            if len(donations) < maxExtras: extrasCap = len(donations)
            else: extrasCap = maxExtras

        while rollCredits:

            menuMusicLoop()

            for event in pygame.event.get():
                # EXIT
                if event.type == pygame.QUIT: quitGame()

                # TOGGLE FULLSCREEN
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    pygame.mouse.set_visible(False)
                    screen = toggleScreen()

                # SHIP SPAWN DELAY
                if event.type == backGroundShipSpawnEvent:
                    waitToSpawn = False

                # MUTE
                elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m): toggleMusic(game)

                # RETURN TO GAME
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_c or event.key == pygame.K_SPACE or event.key == pygame.K_TAB):
                    rollCredits = False

            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            game.showBackgroundCloud()

            for ship in bgShips:
                ship.move()
                if ship.active:
                    if len(donations) == 0: ship.draw(False,showSupporterNames)
                    else: ship.draw(showBackgroundShips,showSupporterNames)
                    # off screen, add name back to pool and remove
                    if ship.offScreen():
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(minBackgroundShipSpawnDelay,maxBackgroundShipSpawnDelay))
                        bgShips.remove(ship)
                        for i in extras:
                            if i[0] == ship.text:
                                extras.remove(i)
                                break

            # Assign a background ship object
            if not waitToSpawn and extrasCap-len(bgShips) > 0: # make sure there is room
                if len(donations) == 0: # If failed to load dictionary, display defaults to version number
                    if len(bgShips)==0:
                        bgShips.append(BackgroundShip(version,1))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(minBackgroundShipSpawnDelay,maxBackgroundShipSpawnDelay))

                elif len(donations) == 1:
                    if len(bgShips) == 0:
                        name,value = list(donations.items())[0]
                        bgShips.append(BackgroundShip(name,value))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(minBackgroundShipSpawnDelay,maxBackgroundShipSpawnDelay))

                else:
                    pool = list(donations.keys())

                    for xtra in extras:
                        if xtra[0] in pool: pool.remove(xtra[0]) # Already on screen

                    if len(pool) > 0:
                        chosen = random.choice(pool) # get name from pool
                        extra = chosen,donations[chosen]
                        extras.append(extra)
                        bgShips.append(BackgroundShip(extra[0],extra[1]))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(minBackgroundShipSpawnDelay,maxBackgroundShipSpawnDelay))

            screen.blit(createdByDisplay,createdByRect)
            screen.blit(creditsDisplay,creditsRect)
            screen.blit(musicCreditsDisplay,musicCreditsRect)
            displayUpdate()

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
            if bounceCount >= mainCreditsDelay: bounceCount = 0



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
            self.shields = spaceShipList[game.savedShipLevel][3]["startingShields"]
            self.shieldPieces = spaceShipList[game.savedShipLevel][3]["startingShieldPieces"]
            self.shieldPiecesNeeded = spaceShipList[game.savedShipLevel][3]["piecesNeeded"]
            self.damage = spaceShipList[game.savedShipLevel][3]["laserDmg"]
            self.showShield = False


        # PLAYER MOVEMENT ( will be revisited for more accurate angular movement)
        def movement(self):
            key = pygame.key.get_pressed()
            if not key[pygame.K_LALT] and not key[pygame.K_RALT]:
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

            else: # ROTATION ONLY
                if key[pygame.K_w] or key[pygame.K_UP]:
                    self.angle = 0

                if key[pygame.K_s] or key[pygame.K_DOWN]:
                    self.angle = 180

                if key[pygame.K_a] or key[pygame.K_LEFT]:
                    self.angle = 90

                if key[pygame.K_d] or key[pygame.K_RIGHT]:
                    self.angle = -90

            # DIAGONAL MOVEMENT ANGLES
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
        def alternateMovement(self,game):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): quitGame()

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
                else: self.angle = game.angle


        # WRAP AROUND SCREEN
        def wrapping(self):
            if self.rect.centery > screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = screenSize[1]
            if self.rect.centerx > screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = screenSize[0]


        # GET NEXT SKIN
        def nextSkin(self):
            if self.currentImageNum + 1 < len(spaceShipList[game.savedShipLevel][2]):
                if self.currentImageNum + 1 > game.skinUnlockNumber:
                    self.image = spaceShipList[game.savedShipLevel][2][0]
                    self.currentImageNum = 0
                else:
                    self.image = spaceShipList[game.savedShipLevel][2][self.currentImageNum+1]
                    self.currentImageNum+=1
            else:
                self.image = spaceShipList[game.savedShipLevel][2][0]
                self.currentImageNum = 0
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)


        # GET PREVIOUS SKIN
        def lastSkin(self):
            if self.currentImageNum >= 1:
                self.image = spaceShipList[game.savedShipLevel][2][self.currentImageNum - 1]
                self.currentImageNum-=1
            else:
                if game.skinUnlockNumber == 0:return
                else:
                    self.image = spaceShipList[game.savedShipLevel][2][game.skinUnlockNumber]
                    self.currentImageNum = game.skinUnlockNumber
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)


        # SWITCH SHIP TYPE
        def toggleSpaceShip(self,game,toggleDirection): # toggleDirection == True -> next ship / False -> last ship
            if game.shipUnlockNumber == 0: return
            else:
                if toggleDirection:
                    if game.savedShipLevel + 1 <= game.shipUnlockNumber: game.savedShipLevel +=1
                    else: game.savedShipLevel = 0
                else:
                    if game.savedShipLevel - 1 < 0: game.savedShipLevel = game.shipUnlockNumber
                    else: game.savedShipLevel -=1
                game.skinUnlockNumber = game.skinsUnlocked(game.savedShipLevel) # Get skin unlocks for new ship type
                self.updatePlayerConstants(game) # Update attributes


        # Update player attributes
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
            self.shields = spaceShipList[game.savedShipLevel][3]["startingShields"]
            self.shieldPieces = spaceShipList[game.savedShipLevel][3]["startingShieldPieces"]
            self.shieldPiecesNeeded = spaceShipList[game.savedShipLevel][3]["piecesNeeded"]
            self.damage = spaceShipList[game.savedShipLevel][3]["laserDmg"]


        def updateExhaust(self,game):
            if self.exhaustState+1 > len(spaceShipList[game.savedShipLevel][0]): self.exhaustState = 0
            else: self.exhaustState += 1


        def explode(self,game,obstacles):
            while self.explosionState < len(explosionList):
                height = explosionList[self.explosionState].get_height()
                width = explosionList[self.explosionState].get_width()
                screen.blit(bgList[game.currentStage-1][0],(0,0))
                game.showBackgroundCloud()

                if game.levelType == "CAVE" or game.levelType == "BOTH": screen.blit(game.cave.image,game.cave.rect) # Draw cave
                # Draw obstacles during explosion
                obstacleMove(self,obstacles)
                for obs in obstacles:
                    newBlit = rotateImage(obs.image,obs.rect,obs.angle)
                    screen.blit(newBlit[0],newBlit[1])

                img = pygame.transform.scale(explosionList[self.explosionState], (height * self.explosionState, width * self.explosionState)) # Blow up explosion
                img, imgRect = rotateImage(img, self.rect, self.lastAngle) # Rotate

                screen.blit(img,imgRect) # Draw explosion
                screen.blit(explosionList[self.explosionState],self.rect)
                displayUpdate()
                game.clk.tick(fps)
                self.explosionState += 1
                self.finalImg,self.finalRect = img,imgRect # Explosion effect on game over screen


        def shieldUp(self):
            self.shieldPieces += 1
            if self.shieldPieces >= self.shieldPiecesNeeded:
                self.shieldPieces = 0
                self.shields += 1


        def shieldDown(self,events):
            self.shields -= 1
            self.showShield = True
            events.showShield()



# OBSTACLES
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,spawnPattern,targeting,playerPos):
        super().__init__()
        self.attributeIndex = None
        self.spawnPattern = self.getAttributes(spawnPattern)
        self.target = self.getAttributes(targeting)
        self.movement = getMovement(self.spawnPattern)
        self.speed = self.getAttributes(game.obstacleSpeed)
        self.size = self.getAttributes(game.obstacleSize)
        self.spinSpeed = self.getAttributes(game.spinSpeed)
        self.health = self.getAttributes(game.obsHealth)
        self.bounds = self.getAttributes(game.obstacleBoundaries)
        try: self.image = obstacleImages[game.currentStage - 1][game.currentLevel-1]
        except: self.image = meteorList[random.randint(0,len(meteorList)-1)] # Not enough assets for this level yet
        self.image = pygame.transform.scale(self.image, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.getDirection(playerPos)
        self.angle = 0 # Image rotation
        spins = [-1,1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.active = False
        

    # For levels with multiple obstacle types
    def getAttributes(self,attribute):
        if type(attribute) == list:
            if self.attributeIndex is None: self.attributeIndex = random.randint(0,len(attribute)-1)
            if self.attributeIndex > len(attribute): return attribute[random.randint(0,len(attribute)-1)]
            return attribute[self.attributeIndex]
        else: return attribute


    def getDirection(self,playerPos):
        if self.target == "NONE": self.direction = self.movement[1]
        else: self.direction = math.atan2(playerPos[1] - self.rect.centery, playerPos[0] - self.rect.centerx)


    def move(self,player):
        if self.target == "NONE": self.basicMove()
        elif self.target == "LOCK": self.targetMove()
        elif self.target == "HOME": self.homingMove(player)


    # BASIC MOVEMENT (8-direction) -> direction is a string
    def basicMove(self):
        if "N" in self.direction: self.rect.centery -= self.speed
        if "S" in self.direction: self.rect.centery += self.speed
        if "E" in self.direction: self.rect.centerx += self.speed
        if "W" in self.direction: self.rect.centerx -= self.speed


    # AIMED AT PLAYER -> direction is an angle
    def targetMove(self):
        self.rect.centerx +=self.speed * math.cos(self.direction)
        self.rect.centery +=self.speed * math.sin(self.direction)


    # HEAT SEEKING -> direction is an angle
    def homingMove(self,player):
        dirX = (player.rect.centerx - self.rect.centerx + screenSize[0]/2) % screenSize[0]-screenSize[0]/2 # Shortest horizontal path
        dirY = (player.rect.centery - self.rect.centery + screenSize[1]/2) % screenSize[1]-screenSize[1]/2 # Shortest vetical path
        self.direction = math.atan2(dirY,dirX) # Angle to shortest path
        self.targetMove()


    # BOUNDARY HANDLING
    def bound(self,obstacles):
        if self.bounds == "KILL": # Remove obstacle
            if self.rect.centerx > screenSize[0] or self.rect.centerx < 0:
                obstacles.remove(self)
                self.kill()
            elif self.rect.centery > screenSize[1] or self.rect.centery < 0:
                obstacles.remove(self)
                self.kill()

        elif self.bounds == "BOUNCE": # Bounce off walls
            direction = self.direction
            if self.rect.centery  > screenSize[1]: self.direction = movementReverse(direction)
            if self.rect.centery < 0: self.direction = movementReverse(direction)
            if self.rect.centerx > screenSize[0]: self.direction = movementReverse(direction)
            if self.rect.centerx < 0: self.direction = movementReverse(direction)

        elif self.bounds == "WRAP": # Wrap around screen
            if self.rect.centery > screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = screenSize[1]
            if self.rect.centerx > screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = screenSize[0]


    def activate(self):
        if not self.active:
            if self.rect.right >= 0 or self.rect.left <= screenSize[0] or self.rect.top <= 0 or self.rect.bottom >= screenSize[1]: self.active = True



# CAVES
class Caves(pygame.sprite.Sprite):
    def __init__(self,index):
        super().__init__()
        self.speed = caveSpeed
        self.image = caveImages[index]
        self.rect = self.image.get_rect(bottomleft = (0,caveStartPos))
        self.mask = pygame.mask.from_surface(self.image)
        self.leave = False # Mark cave for exit


    def update(self):
        self.rect.centery += self.speed # Move
        if not self.leave and self.rect.top > screenSize[1] * -1: self.rect.bottom = screenSize[1]*2



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
    def __init__(self,player,lastPos):
        super().__init__()
        self.powerUp = ''
        pointChoices = powerUpList[:]
        if not player or (not player.hasShields and player.boostDrain == 0 and player.laserCost == 0  and player.baseSpeed == player.boostSpeed): self.powerUp = "Default"
        else:
            powerUps = pointChoices
            if not player.hasShields and "Shield" in powerUps: pointChoices.remove("Shield")
            if not player.hasGuns and player.baseSpeed == player.boostSpeed and "Fuel" in powerUps: pointChoices.remove("Fuel")
            self.powerUp = random.choice(pointChoices)
        if self.powerUp == "Shield": self.image = pointsList[2]
        elif self.powerUp == "Fuel": self.image = pointsList[1]
        elif self.powerUp == "Default": self.image = pointsList[0]
        self.image = pygame.transform.scale(self.image, (pointSize, pointSize))
        if lastPos == None: self.rect = self.image.get_rect(center = positionGenerator())
        else:self.rect = self.image.get_rect(center = spacedPositionGenerator(lastPos))
        self.mask = pygame.mask.from_surface(self.image)



# MENU METEOR ICONS
class Icon:
    def __init__(self):
        spins = [-1,1]
        self.speed = random.randint(1,maxIconSpeed)
        self.movement = getMovement("ALL")
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.image = menuList[random.randint(5,len(menuList)-1)]
        size = random.randint(minIconSize,maxIconSize)
        self.image = pygame.transform.scale(self.image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0
        self.active = False


    def move(self):
        if "N" in self.direction: self.rect.centery -= self.speed
        if "S" in self.direction: self.rect.centery += self.speed
        if "E" in self.direction: self.rect.centerx += self.speed
        if "W" in self.direction: self.rect.centerx -= self.speed
        self.activate()

        if self.angle >= 360 or self.angle <= -360: self.angle = 0

        self.angle += self.spinDirection * random.uniform(0, maxIconRotationSpeed)

        randomTimerUX = random.randint(screenSize[0] * 2,screenSize[0] * 4)
        randomTimerUY = random.randint(screenSize[1] * 2,screenSize[1] * 4)
        randomTimerLX = -1 * random.randint(screenSize[0], screenSize[0] * 3)
        randomTimerLY = -1 * random.randint(screenSize[0], screenSize[1] * 3)

        if self.active and ( (self.rect.centery > randomTimerUY) or (self.rect.centery < randomTimerLY) or (self.rect.centerx> randomTimerUX) or (self.rect.centerx < randomTimerLX) ):
            self.movement = getMovement("ALL")
            self.direction = self.movement[1]
            self.image = menuList[random.randint(5,len(menuList)-1)]
            self.speed = random.randint(1,maxIconSpeed)
            self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
            size = random.randint(minIconSize,maxIconSize)
            self.image = pygame.transform.scale(self.image, (size, size))


    def activate(self):
        if not self.active:
            if self.rect.right >= 0 or self.rect.left <= screenSize[0] or self.rect.top <= 0 or self.rect.bottom >= screenSize[1]: self.active = True


    def draw(self):
        if self.active:
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
        self.movement = getMovement("ALL")
        self.direction = self.movement[1]
        self.angle = getAngle(self.direction)
        self.text = text
        self.image = pygame.transform.scale(donationShips[random.randint(0, len(donationShips) - 1)], (self.size, self.size) ).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.count = 0
        self.font = pygame.font.Font(gameFont, int(self.size * 2/3))
        self.display = self.font.render(self.text, True, extraCreditsColor)
        self.displayRect = self.display.get_rect(center = self.rect.center)
        self.active = False


    def move(self):
        if self.count >= backgroundShipDelay:
            if "N" in self.direction: self.rect.centery -= self.speed
            if "S" in self.direction: self.rect.centery += self.speed
            if "E" in self.direction: self.rect.centerx += self.speed
            if "W" in self.direction: self.rect.centerx -= self.speed
            self.displayRect.center = self.rect.center
            self.count = 0
        self.count +=1
        self.activate()


    def draw(self,showImage,showText):
        if self.active:
            if not showImage and not showText: return
            else:
                drawing, drawee = rotateImage(self.image,self.rect,self.angle)
                supporterRect = self.display.get_rect(center = drawee.center)
                if showImage: screen.blit(drawing,drawee)
                if showText: screen.blit(self.display,supporterRect)


    # Returns true if off screen
    def offScreen(self):
        if showSupporterNames and not showBackgroundShips:
            if self.displayRect.bottom < 0 or self.displayRect.top > screenSize[1] or self.displayRect.left > screenSize[0] or self.displayRect.right < 0: return True
        else:
            if self.rect.bottom < 0 or self.rect.top > screenSize[1] or self.rect.left > screenSize[0] or self.rect.right < 0: return True


    def activate(self):
        if not self.active:
            if not self.offScreen(): self.active = True



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


# MOVEMENT AND POSITION GENERATION
def getMovement(spawnPattern):
    top,bottom,left,right = [],[],[],[]
    if spawnPattern == "AGGRO": top, bottom, left, right, = ["SE", "SW", "S"], ["N", "NE", "NW"], ["E", "NE", "SE"], ["NW", "SW", "W"]
    elif spawnPattern == "TOP": top = ["SE", "SW", "S"]
    elif spawnPattern == "VERT": top, bottom = ["SE", "SW", "S"], ["N", "NE", "NW"]
    else: top, bottom, left, right = topDir, bottomDir, leftDir, rightDir # Default / "All"

    X = random.randint(0, screenSize[0])
    Y = random.randint(0, screenSize[1])

    lowerX = random.randint(-obstacleSpawnRange[1],obstacleSpawnRange[0])
    upperX =  random.randint(screenSize[0], screenSize[0] + obstacleSpawnRange[1])
    lowerY  = random.randint(-obstacleSpawnRange[1],obstacleSpawnRange[0])
    upperY = random.randint(screenSize[1],screenSize[1]+obstacleSpawnRange[1])

    possible = []
    if len(top) != 0: possible.append([X, lowerY, top[random.randint(0, len(top) - 1)]])
    if len(bottom) != 0: possible.append([X, upperY, bottom[random.randint(0, len(bottom) - 1)]])
    if len(left) != 0: possible.append([lowerX, Y, left[random.randint(0, len(left) - 1)]])
    if len(right) != 0: possible.append([upperX, Y, right[random.randint(0, len(right) - 1)]])

    movement = possible[ random.randint(0, len(possible) - 1) ]
    position = [movement[0], movement[1]]
    direction = movement[2]
    move = [position,direction]
    return move


# OBSTACLE MOVEMENT (outside of main loop)
def obstacleMove(player,obstacles):
    for obs in obstacles:
        obs.move(player)
        obs.activate()


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
    attempts = 0
    while True:
        point = getPosition()
        if attempts < maxRandomAttempts and pointValid(point):return point
        else: attempts+=1


# Get new position at valid distance from last position
def spacedPositionGenerator(lastPos):
    attempts = 0
    while True:
        point = positionGenerator()
        if attempts < maxRandomAttempts and math.dist(point,lastPos) >= minDistanceToPoint: return point
        else: attempts+=1


# GET ANGLE FOR CORRESPONDING DIRECTION
def getAngle(direction):
    if direction == "N": return 0
    elif direction == "S": return 180
    elif direction == "E": return -90
    elif direction == "W": return 90
    elif direction == "NW": return 45
    elif direction == "NE": return -45
    elif direction == "SE": return -135
    elif direction == "SW": return 135


# GET SCALED VALUE
def valueScaler(amount, minimum, maximum, bottom, top):
    if bottom is None or top is None:
        return minimum
    elif top - bottom == 0:
        return (maximum + minimum) / 2
    else:
        scaled = (amount - bottom) / (top - bottom) * (maximum - minimum) + minimum
        return min(max(scaled, minimum), maximum)


# INITIALIZE GAME
game = Game(loadRecords()) # Initialize game with records loaded
menu = Menu() # Initialize menus

# SET VOLUME
if not game.musicMuted: pygame.mixer.music.set_volume(musicVolume / 100)
else: pygame.mixer.music.set_volume(0)


# START GAME LOOP
def gameLoop():
    pygame.mixer.music.play()
    game.resetGameConstants() # Reset level settings
    game.pauseCount = 0 # Reset pause uses
    game.resetClock() # Restart game clock
    player = Player(game) # Initialize player
    if game.mainMenu: menu.home(game,player)
    else:
        for i in range(game.savedSkin): player.nextSkin()
    if game.savedShipLevel > 0: player.updatePlayerConstants(game)

    events = Event() # Initialize events
    events.set(player) # Events manipulate player cooldowns
    lasers = pygame.sprite.Group() # Laser group
    obstacles = pygame.sprite.Group() # Obstacle group
    running = True

    # GAME LOOP
    while running: game.update(player,obstacles,menu,events,lasers)


if __name__ == '__main__': gameLoop()