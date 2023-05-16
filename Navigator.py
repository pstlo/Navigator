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

version = "v0.4.8"



# GAME SETTINGS
class Settings:
    def __init__(self):
        # SCREEN
        self.screenSize = [800,800] # Default = [800,800]
        self.fps = 60 # Default = 60
        self.fullScreen = False

        # INPUT
        self.useController = True # Default = True / Allow controller input
        self.cursorMode = True # Default = True / Allow cursor input
        self.cursorFollowDistance = 25 # Default = 30 / Cursor follow deadzone
        self.cursorRotateDistance = 10 # Default = 15 / Cursor rotate deadzone
        self.cursorThickness = 2 # Default = 2

        # HUD
        self.showHUD = True
        self.shieldColor = [0,0,255] # Default = [0,0,255] / Color of shield gauge / Blue
        self.fullShieldColor = [0,255,255] # Default = [0,255,255] / Color of active shield gauge / Cyan
        self.fuelColor = [255,0,0] # Default = [255,0,0] / Color of fuel gauge /  Red
        self.timerDelay = 1000 # Default = 1000
        self.pauseMax = 5 # Default = 5 / max pauses per game

        # POWER UPS
        self.spawnRange = [0.15, 0.85]
        self.spawnVertices = 8 # Default = 8 / Vertices in shape of point spawn area (Octagon)
        self.pointSize = 25  # Default = 20
        self.shieldChunkSize = self.screenSize[0]/40 # Default = screen width / 40
        self.boostCooldownTime = 2000 # Default = 2000 / Activates when fuel runs out to allow regen
        self.powerUpList = ["Shield", "Fuel", "Default", "Default"] # Shield/Fuel/Default, chances of spawn
        self.playerShieldSize = 48 # Default = 64 / Shield visual size
        self.shieldVisualDuration = 250 # Default = 250 / Shield visual duration
        self.minDistanceToPoint = (self.screenSize[0] + self.screenSize[1]) / 16 # Default = 100
        self.maxRandomAttempts = 100 # Default = 100 / For random generator distances / max random attempts at finding a valid point

        # BACKGROUND CLOUD
        self.showBackgroundCloud = True # Default = True
        self.cloudSpeed = 1 # Default = 1
        self.cloudStart = -1000 # Default = -1000
        self.cloudSpeedAdder = 0.5 # Default = 0.5 / cloud speed increment per level

        # FONT COLORS
        self.primaryFontColor = [0,255,0] # Default = [0,255,0] / Green
        self.secondaryFontColor = [255,255,255] # Default = [255,255,255] / White

        # START MENU
        self.maxIcons = 5 # Default = 5
        self.maxIconSpeed = 5 # Default = 5
        self.maxIconRotationSpeed = 3 # Default = 3
        self.minIconSize = 30 # Default = 30
        self.maxIconSize = 100  # Default = 100
        self.showVersion = True # show version info
        self.showMenuIcons = True # show menu icons

        # STAGE UP
        self.stageUpCloudStartPos = -900 # Default = -900
        self.stageUpCloudSpeed = 8  # Default = 8

        # CREDITS
        self.mainCreditsSpeed = 1 # Default = 1
        self.mainCreditsDelay = 10 # Default = 10
        self.extraCreditsSize = 30  # Default = 30 / background ships text size
        self.maxExtras = 3 # Default = 3 / # max background ships
        self.minBackgroundShipSpeed = 2 # Default = 1
        self.maxBackgroundShipSpeed = 3 # Default = 3
        self.minBackgroundShipSize = 50 # Default = 50
        self.maxBackgroundShipSize = 100 # Default = 150
        self.backgroundShipDelay = 15 # Default = 15 / Higher is slower
        self.minBackgroundShipSpawnDelay = 500 # / Min delay (ms) before a ship spawns
        self.maxBackgroundShipSpawnDelay = 3000 # / Max delay (ms) before a ship spawns
        self.showBackgroundShips = True # Default = True
        self.showSupporterNames = True # Default = True

        # SOUNDS
        self.musicVolume = 10 # Default = 10 / Music volume / 100
        self.sfxVolume = 5 # Default = 5 / SFX volume / 100
        self.musicMuted = False

        # MUSIC LOOP DURATION
        self.menuLoopStart = 1100 # Default = 1100
        self.menuLoopEnd = 12800 # Default = 12800
        self.musicLoopStart = 25000 # Default = 25000
        self.musicLoopEnd = 76000 # Default = 76000

        # PLAYER
        self.resetPlayerOrientation = True # Default = True / reset orientation if player is not moving
        self.drawExhaust = True # Default = True / draw exhaust animation
        self.exhaustUpdateDelay = 50 # Default = 50 / Delay (ms) between exhaust animation frames
        self.defaultToHighSkin = True # Default = True / Default to highest skin unlocked on game launch
        self.defaultToHighShip = False # Default = False / Default to highest ship unlocked on game launch
        self.heatSeekDelay = 15 # Default = 15 / time before projectile starts homing
        self.heatSeekNeedsTarget = False # Default = False / projectile will explode if target not found

        # LEVELS
        self.levelUpCloudSpeed = 25 # Default = 25 / Only affects levels preceded by wipe

        # OBSTACLES
        self.explosionDelay = 1 # Default = 1
        self.slowerDiagonalObstacles = True # Default = True / use the hypotenuse or whatever
        self.spawnDistance = 0 # Default = 0 / Distance past screen border required before new obstacle spawned
        self.activationDelay = 2 # Default = 2 / frames before activation after entering screen

        # CAVES
        self.caveStartPos = self.screenSize[1]*-2 # Default = -1600 / Cave start Y coordinate
        self.caveSpeed = 20 # Default = 20 / Cave flyby speed

        # SAVING
        self.encryptGameRecords = True # Hide game records from user to prevent manual unlocks
        self.invalidKeyMessage = "Invalid key, could not save records." # Saved to game records file if settings.encryptGameRecords == True and key is invalid

        # EXPERIMENTAL
        self.loadPreferencesFromFile = False # Default = False / load settings from txt file / WORK IN PROGRESS
        self.devMode = False # Default = False
        self.showSpawnArea = False # Default = False / show powerup spawn area
        self.rawCursorMode = False # Default = False / sets player position to cursor position
        self.playerMovement = "DEFAULT" # Default = "DEFAULT" /  (DEFAULT, ORIGINAL)
        self.performanceMode = False
        self.qualityMode = False
        self.showPresence = True

        # SET SCREEN UPDATE METHOD
        if self.qualityMode and not self.performanceMode: self.updateNotFlip = False
        else: self.updateNotFlip = True # use update instead of flip for display updates

        # SET PERFORMANCE SETTINGS
        if self.performanceMode:self.showBackgroundCloud,self.drawExhaust = False,False

        # CONTROLLER BINDS
        self.controllerBinds = {
            'PS': # Dualshock
                {
                'name': ["PS4 Controller"],
                'moveX': 0,
                'moveY': 1,
                'rotX' : 2,
                'rotY' : 3,
                'boost':4,
                'shoot':5,
                'nextShip':11,
                'lastShip':12,
                'nextSkin':14,
                'lastSkin':13,
                'select':0,
                'back':1,
                'mute':9,
                'exit':6,
                'pause':15,
                'menu':15,
                'settings.fullScreen': 4,
                'credits':3
                },

            'XB': # Xbox controller
                {
                'name': ["Controller (Xbox One For Windows)", "Controller (XBOX 360 For Windows)"],
                'moveX': 0,
                'moveY': 1,
                'rotX' : 2,
                'rotY' : 3,
                'boost':4,
                'shoot':5,
                'nextShip':(0,1),
                'lastShip':(0,-1),
                'nextSkin':(1,0),
                'lastSkin':(-1,0),
                'select':0,
                'back':1,
                'mute':4,
                'exit':7,
                'pause':6,
                'menu':6,
                'settings.fullScreen': 10,
                'credits':3
                },

            'NS': # Switch pro controller
                {
                'name': ["Nintendo Switch Pro Controller"],
                'moveX': 0,
                'moveY': 1,
                'rotX' : 2,
                'rotY' : 3,
                'boost':4,
                'shoot':5,
                'nextShip':11,
                'lastShip':12,
                'nextSkin':14,
                'lastSkin':13,
                'select':0,
                'back':1,
                'mute':9,
                'exit':6,
                'pause':4,
                'menu':4,
                'settings.fullScreen': 15,
                'credits':2
                }
            }



# ASSETS
class Assets:
    def __init__(self):
        # RECORD AND PREFERENCE PATHS
        if platform.system().lower() == 'windows' or platform.system().lower == 'linux': self.recordsPath,self.preferencesPath = './gameRecords.txt','./gamePreferences.txt'  # For windows and linux
        else: self.recordsPath,self.preferencesPath = self.resources('gameRecords.txt'), self.resources('gamePreferences.txt') # For MacOS

        # ASSET PATHS
        assetDirectory = self.resources('Assets') # ASSET DIRECTORY
        load_dotenv(os.path.join(assetDirectory,'.env')) # LOAD ENV VARS
        obstacleDirectory = os.path.join(assetDirectory, 'Obstacles') # Obstacle asset directory
        meteorDirectory = os.path.join(obstacleDirectory, 'Meteors') # Meteor asset directory
        ufoDirectory = os.path.join(obstacleDirectory, 'UFOs') # UFO asset directory
        shipDirectory = os.path.join(assetDirectory, 'Spaceships') # Spaceship asset directory
        caveDirectory = os.path.join(assetDirectory,'Caves') # Cave asset directory
        backgroundDirectory = os.path.join(assetDirectory, 'Backgrounds') # Background asset directory
        menuDirectory = os.path.join(assetDirectory, 'MainMenu') # Start menu asset directory
        explosionDirectory = os.path.join(assetDirectory, 'Explosion') # Explosion animation directory
        pointsDirectory = os.path.join(assetDirectory, 'Points') # Point image directory
        soundDirectory = os.path.join(assetDirectory, 'Sounds') # Sound assets directory
        supportersDirectory = os.path.join(assetDirectory,'Supporters') # Supporters directory

        self.windowIcon = pygame.image.load(self.resources(os.path.join(assetDirectory,'Icon.png'))).convert_alpha()
        self.stageCloudImg = pygame.image.load(self.resources(os.path.join(assetDirectory,'StageCloud.png') ) ).convert_alpha() # STAGE WIPE CLOUD

        # LOAD LEVELS
        self.stageList = []
        with open(self.resources(os.path.join(assetDirectory, 'Levels.json')), 'r') as file:
            stages = json.load(file)
            for stage in stages.values():
                levels = []
                for level in stage.values():
                    level["START"] = False
                    levels.append(level)
                self.stageList.append(levels)

        # OBSTACLE ASSETS
        meteorList = []
        for filename in sorted(os.listdir(meteorDirectory)):
            if filename.endswith('.png'):
                path = os.path.join(meteorDirectory, filename)
                meteorList.append(pygame.image.load(self.resources(path)).convert_alpha())

        # UFO ASSETS
        ufoList = []
        for filename in sorted(os.listdir(ufoDirectory)):
            if filename.endswith('.png'):
                path = os.path.join(ufoDirectory, filename)
                ufoList.append(pygame.image.load(self.resources(path)).convert_alpha())

        self.obstacleImages = [meteorList,ufoList] # Seperated by stage

        # CAVE ASSETS
        self.caveList = []
        for caveNum in sorted(os.listdir(caveDirectory)):
            caveAssets = os.path.join(caveDirectory,caveNum)
            cave = []
            cave.append(pygame.image.load(self.resources(os.path.join(caveAssets,"Background.png"))).convert_alpha())
            cave.append(pygame.image.load(self.resources(os.path.join(caveAssets,"Cave.png"))).convert_alpha())
            self.caveList.append(cave)

        # BACKGROUND ASSETS
        self.bgList = []
        for filename in sorted(os.listdir(backgroundDirectory)):
            filePath = os.path.join(backgroundDirectory,filename)
            if os.path.isdir(filePath):
                bgPath = os.path.join(backgroundDirectory,filename)
                stageBgPath = os.path.join(bgPath,'Background.png')
                stageCloudPath = os.path.join(bgPath,'Cloud.png')
                bg = pygame.image.load(self.resources(stageBgPath)).convert_alpha()
                cloud = pygame.image.load(self.resources(stageCloudPath)).convert_alpha()
                self.bgList.append([bg,cloud])

        # EXPLOSION ASSETS
        self.explosionList = []
        for filename in sorted(os.listdir(explosionDirectory)):
            if filename.endswith('.png'):
                path = os.path.join(explosionDirectory, filename)
                self.explosionList.append(pygame.image.load(self.resources(path)).convert_alpha())

        # POINTS ASSETS
        self.pointsList = []
        for filename in sorted(os.listdir(pointsDirectory)):
            if filename.endswith('png'):
                path = os.path.join(pointsDirectory, filename)
                self.pointsList.append(pygame.image.load(self.resources(path)).convert_alpha())

        # SPACESHIP ASSETS
        self.spaceShipList = []
        for levelFolder in sorted(os.listdir(shipDirectory)):
            levelFolderPath = os.path.join(shipDirectory,levelFolder) # level folder path
            if os.path.isdir(levelFolderPath): # Ignore DS_STORE on MacOS
                shipLevelDict = {'skins':[],'exhaust':[], 'boost':[], 'laser':'', 'stats':''}

                # Load ship skins
                skinsPath = os.path.join(levelFolderPath,'Skins')
                for imageAsset in sorted(os.listdir(skinsPath)):
                    if imageAsset.endswith('.png'):
                        imageAssetPath = os.path.join(skinsPath,imageAsset)
                        shipLevelDict['skins'].append(pygame.image.load(self.resources((imageAssetPath))).convert_alpha())

                # Load exhaust frames
                exhaustPath = os.path.join(levelFolderPath,'Exhaust')
                for imageAsset in sorted(os.listdir(exhaustPath)):
                    if imageAsset.endswith('.png'):
                        imageAssetPath = os.path.join(exhaustPath,imageAsset)
                        shipLevelDict['exhaust'].append(pygame.image.load(self.resources((imageAssetPath))).convert_alpha())

                # Load boost frames
                boostPath = os.path.join(levelFolderPath,'Boost')
                for imageAsset in sorted(os.listdir(boostPath)):
                    if imageAsset.endswith('.png'):
                        imageAssetPath = os.path.join(boostPath,imageAsset)
                        shipLevelDict['boost'].append(pygame.image.load(self.resources((imageAssetPath))).convert_alpha())

                # Load laser image
                laserPath = os.path.join(levelFolderPath,'Laser.png')
                shipLevelDict['laser'] = pygame.image.load(self.resources(laserPath)).convert_alpha()

                # Load ship stats
                statsPath = os.path.join(levelFolderPath,'Stats.json')
                with open(self.resources(statsPath), 'r') as file: shipLevelDict['stats'] = json.load(file)

                self.spaceShipList.append(shipLevelDict)

        # SHIP ATTRIBUTES DATA
        self.shipConstants = []
        for i in range(len(self.spaceShipList)): self.shipConstants.append(self.spaceShipList[i]["stats"])

        # PLAYER SHIELD ASSET
        self.playerShield = pygame.transform.scale(pygame.image.load(self.resources(os.path.join(assetDirectory,"Shield.png"))),(settings.playerShieldSize,settings.playerShieldSize))

        # MAIN MENU ASSETS
        self.menuList = []
        self.menuList.append(pygame.image.load(self.resources(os.path.join(menuDirectory,'A.png'))).convert_alpha()) # 'A' icon
        self.menuList.append(pygame.image.load(self.resources(os.path.join(menuDirectory,'O.png'))).convert_alpha()) # 'O' icon
        self.menuList.append(pygame.image.load(self.resources(os.path.join(menuDirectory,'center.png'))).convert_alpha()) # Center icon
        self.menuList.append(pygame.image.load(self.resources(os.path.join(menuDirectory,'left.png'))).convert_alpha()) # Left icon
        self.menuList.append(pygame.image.load(self.resources(os.path.join(menuDirectory,'right.png'))).convert_alpha()) # Right icon

        menuMeteorDir = os.path.join(menuDirectory,'FlyingObjects')
        for objPath in sorted(os.listdir(menuMeteorDir)): self.menuList.append(pygame.image.load(self.resources(os.path.join(menuMeteorDir,objPath))).convert_alpha())

        # MUSIC ASSET
        pygame.mixer.music.load(self.resources(os.path.join(soundDirectory,"Soundtrack.mp3")))

        # EXPLOSION NOISE ASSET
        self.explosionNoise = pygame.mixer.Sound(self.resources(os.path.join(soundDirectory,"Explosion.wav")))
        self.explosionNoise.set_volume(settings.sfxVolume/100)

        # POINT NOISE ASSET
        self.powerUpNoise = pygame.mixer.Sound(self.resources(os.path.join(soundDirectory,"Point.wav")))
        self.powerUpNoise.set_volume(settings.sfxVolume/100)

        # LASER NOISE ASSET
        self.laserNoise = pygame.mixer.Sound(self.resources(os.path.join(soundDirectory,"Laser.wav")))
        self.laserNoise.set_volume(settings.sfxVolume/100)

        # LASER IMPACT NOISE ASSET
        self.impactNoise = pygame.mixer.Sound(self.resources(os.path.join(soundDirectory,"Impact.wav")))
        self.impactNoise.set_volume(settings.sfxVolume/100)

        # LOAD DONATION RECORDS
        self.donations = {}
        try:
            path = os.path.join(supportersDirectory,'Supporters.txt')
            with open(path,'r') as file:
                for line in file:
                    try:
                        key,value = line.strip().split(':')
                        self.donations[key] = int(value)
                    except:pass
        except: pass

        if len(self.donations) > 0:
            self.maxDon = max(self.donations.values())
            self.lowDon = min(self.donations.values())
        else: self.maxDon,self.lowDon = None,None

        # LOAD DONATION SHIP ASSETS
        self.donationShips = []
        donationShipsDir = os.path.join(supportersDirectory,'Images')
        for filename in sorted(os.listdir(donationShipsDir)):
            if filename.endswith('.png'):
                path = os.path.join(donationShipsDir, filename)
                self.donationShips.append(pygame.image.load(self.resources(path)).convert_alpha())

        # FONTS
        self.gameFont = os.path.join(assetDirectory, 'Font.ttf')
        self.stageFont = pygame.font.Font(self.gameFont, 30)
        self.levelFont = pygame.font.Font(self.gameFont, 30)
        self.scoreFont = pygame.font.Font(self.gameFont, 30)
        self.timerFont = pygame.font.Font(self.gameFont, 30)
        self.stageUpFont = pygame.font.Font(self.gameFont, 90)
        self.startFont = pygame.font.Font(self.gameFont, 120)
        self.shipHelpFont = pygame.font.Font(self.gameFont, 20)
        self.startHelpFont = pygame.font.Font(self.gameFont, 30)
        self.pausedFont = pygame.font.Font(self.gameFont, 100)
        self.pauseCountFont = pygame.font.Font(self.gameFont,40)
        self.versionFont = pygame.font.Font(self.gameFont,25)
        self.gameOverFont = pygame.font.Font(self.gameFont, 100)
        self.statFont = pygame.font.Font(self.gameFont, 30)
        self.exitFont = pygame.font.Font(self.gameFont, 30)
        self.creatorFont = pygame.font.Font(self.gameFont, 55)
        self.creditsFont = pygame.font.Font(self.gameFont, 40)


    # EXE/APP RESOURCES
    def resources(self,relative):
        try: base = sys._MEIPASS # Running from EXE/APP
        except: base = os.path.abspath(".") # Running fron script
        return os.path.join(base, relative)


    # GET KEY
    def getKey(self):
        try: return base64.b64decode(os.getenv('KEY'))
        except: return None # Could not load key


    # STORE GAME RECORDS
    def storeRecords(self,records):
        # No encryption
        if not settings.encryptGameRecords:
            try:
                with open(self.recordsPath, 'w') as file: file.write(json.dumps(records))
            except: return # Continue without saving game records
        # With encryption
        else:
            if self.getKey() is None:
                with open(self.recordsPath,'w') as file: file.write(settings.invalidKeyMessage)
                return # No key, continue without saving
            else:
                try:
                    encrypted = Fernet(self.getKey()).encrypt(json.dumps(records).encode())
                    with open(self.recordsPath,'wb') as file: file.write(encrypted)
                except: return # Failed to load encrypted records, continue without saving


    # LOAD GAME RECORDS
    def loadRecords(self):
        # No encryption
        if not settings.encryptGameRecords:
            try:
                with open(self.recordsPath,'r') as file: return json.load(file)
            except:
                # Could not load records, try overwrite with default values
                gameRecords = {'highScore':0, 'longestRun':0, 'attempts':0, 'timePlayed':0, 'points':0}
                self.storeRecords(gameRecords)
                return gameRecords
        # With encryption
        else:
            try:
                # Return dictionary from encrypted records file
                with open(self.recordsPath,'rb') as file: encrypted = file.read()
                return json.loads(Fernet(self.getKey()).decrypt(encrypted))
            except:
                # Failed to load records
                gameRecords = {'highScore':0, 'longestRun':0, 'attempts':0, 'timePlayed':0, 'points':0}
                self.storeRecords(gameRecords) # Try creating new encrypted records file
                return gameRecords



# GET SCREEN
def getScreen():
    if settings.performanceMode:
        if settings.fullScreen: return pygame.display.set_mode(settings.screenSize, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED , depth = 16)
        else: return pygame.display.set_mode(settings.screenSize,pygame.DOUBLEBUF,depth=16)
    elif settings.qualityMode:
        if settings.fullScreen: return pygame.display.set_mode(settings.screenSize, pygame.FULLSCREEN| pygame.NOFRAME | pygame.SRCALPHA,depth = 32)
        else: return pygame.display.set_mode(settings.screenSize, pygame.NOFRAME | pygame.SRCALPHA,depth = 32)
    # Default
    else:
        if settings.fullScreen: return pygame.display.set_mode(settings.screenSize,pygame.FULLSCREEN | pygame.SCALED, depth = 0)
        else: return pygame.display.set_mode(settings.screenSize,pygame.SCALED,depth = 0)


# TOGGLE FULLSCREEN
def toggleScreen():
    if settings.qualityMode and not settings.performanceMode:
        global screen
        pygame.display.quit()
        settings.settings.fullScreen = not settings.settings.fullScreen
        pygame.display.set_caption('Navigator')
        pygame.display.set_icon(assets.windowIcon)
        screen = getScreen()
    else: pygame.display.toggle_fullscreen()


# GAMEPLAY MUSIC LOOP
def musicLoop():
    if pygame.mixer.music.get_pos() >= settings.musicLoopEnd:
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(settings.musicLoopStart)
        pygame.mixer.music.play()


# TOGGLE MUSIC MUTE
def toggleMusic(game):
    game.musicMuted = not game.musicMuted
    if pygame.mixer.music.get_volume() == 0: pygame.mixer.music.set_volume(settings.musicVolume/100)
    else: pygame.mixer.music.set_volume(0)


settings = Settings() # INITIALIZE SETTINGS
screen = getScreen() # INITIALIZE SCREEN
assets = Assets() # LOAD ASSETS

# KEY BINDS
leftInput = [pygame.K_a, pygame.K_LEFT]
rightInput = [pygame.K_d,pygame.K_RIGHT]
upInput = [pygame.K_w,pygame.K_UP]
downInput = [pygame.K_s,pygame.K_DOWN]
boostInput = [pygame.K_LSHIFT,pygame.K_RSHIFT]
pauseInput = [pygame.K_SPACE]
shootInput = [pygame.K_LCTRL,pygame.K_RCTRL]
escapeInput = [pygame.K_ESCAPE]
backInput = [pygame.K_TAB]
creditsInput = [pygame.K_c]
brakeInput = [pygame.K_LALT,pygame.K_RALT]
muteInput = [pygame.K_m]
fullScreenInput = [pygame.K_f]
startInput = [pygame.K_SPACE]


# UPDATE DISPLAY
def displayUpdate():
    if not settings.updateNotFlip: pygame.display.flip()
    else: pygame.display.update()


# WINDOW
pygame.display.set_caption('Navigator')
pygame.display.set_icon(assets.windowIcon)
screenColor = [0,0,0] # Screen fill color
presence = None # DISCORD PRESENCE


# ASYNCHRONOUSLY UPDATE DISCORD PRESENCE
async def getPresence(presence):
    try:
        await asyncio.wait_for(presence.connect(),timeout = 0.5)
        await presence.update(details='Playing Navigator', state='Navigating the depths of space', large_image='background', small_image = 'icon', buttons=[{'label': 'Play Navigator', 'url': 'https://pstlo.github.io/navigator'}],start=int(time.time()))
    except:
        return None


if settings.showPresence:
    try:
        presence = pypresence.AioPresence((Fernet(base64.b64decode(os.getenv('KEY1'))).decrypt(os.getenv('TOKEN'))).decode())
        asyncio.run(getPresence(presence))
    except: presence = None

# CURSOR
curSurf = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.line(curSurf, (0, 255, 0), (10, 20), (30, 20), settings.cursorThickness)
pygame.draw.line(curSurf, (0, 255, 0), (20, 10), (20, 30), settings.cursorThickness)
cursor = pygame.cursors.Cursor((20, 20), curSurf)
pygame.mouse.set_cursor(cursor)
pygame.mouse.set_visible(settings.cursorMode)


def resetCursor():
    if settings.cursorMode:
        pos = list(pygame.mouse.get_pos())
        if pos[0] <= 1: pygame.mouse.set_pos(5,pos[1])
        if pos[0] >= settings.screenSize[0]-2: pygame.mouse.set_pos(settings.screenSize[0]-5,pos[1])
        if pos[1] <= 1: pygame.mouse.set_pos(pos[0],5)
        if pos[1] >= settings.screenSize[1]-1: pygame.mouse.set_pos(pos[0],settings.screenSize[1]-5)


# CONTROLLER INPUT
gamePad = None
compatibleController = False
if settings.useController:
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        gamePad = pygame.joystick.Joystick(0)
        gamePad.init()
        for controllerType in settings.controllerBinds:
            if gamePad.get_name() in settings.controllerBinds[controllerType]['name']:
                controllerMoveX = settings.controllerBinds[controllerType]['moveX']
                controllerMoveY = settings.controllerBinds[controllerType]['moveY']
                controllerRotateX = settings.controllerBinds[controllerType]['rotX']
                controllerRotateY = settings.controllerBinds[controllerType]['rotY']
                controllerBoost = settings.controllerBinds[controllerType]['boost']
                controllerShoot = settings.controllerBinds[controllerType]['shoot']
                controllerNextShip =settings.controllerBinds[controllerType]['nextShip']
                controllerLastShip =settings.controllerBinds[controllerType]['lastShip']
                controllerNextSkin =settings.controllerBinds[controllerType]['nextSkin']
                controllerLastSkin = settings.controllerBinds[controllerType]['lastSkin']
                controllerSelect = settings.controllerBinds[controllerType]['select']
                controllerBack = settings.controllerBinds[controllerType]['back']
                controllerMute = settings.controllerBinds[controllerType]['mute']
                controllerExit = settings.controllerBinds[controllerType]['exit']
                controllerPause = settings.controllerBinds[controllerType]['pause']
                controllerMenu = settings.controllerBinds[controllerType]['menu']
                controllerFullScreen = settings.controllerBinds[controllerType]['settings.fullScreen']
                controllerCredits = settings.controllerBinds[controllerType]['credits']
                compatibleController = True
                break

        # Incompatible controller
        if not compatibleController:
            pygame.joystick.quit()
            if settings.useController: settings.useController = False

    else:
        pygame.joystick.quit() # This may be causing delay on startup ?
        if settings.useController: settings.useController = False


# UNLOCKS
unlockTimePerLevels = [] # For time based unlocks
totalLevels = 0

for stage in assets.stageList: totalLevels += len(stage) # Get total number of levels
totalTime = totalLevels * 15 # multiply by (average) time per level

# Calculate time per unlock for each ship level
for shipInd in range(len(assets.spaceShipList)):
    timePerUnlock = totalTime/len(assets.spaceShipList[shipInd]['skins'])
    if timePerUnlock == totalTime: unlockTimePerLevels.append(None) # No other skins for this level
    else: unlockTimePerLevels.append(int(timePerUnlock))

expectedPointsPerLevel = 12 # Temporary solution
totalShipTypes = len(assets.spaceShipList) # For score based unlocks
totalPointsForUnlock = totalLevels * expectedPointsPerLevel # Points in game for all unlocks
pointsForUnlock = int(totalPointsForUnlock/expectedPointsPerLevel)

# POINT SPAWN AREA
spawnWidth = int(settings.screenSize[0] * (settings.spawnRange[1] - settings.spawnRange[0]))
spawnHeight = int(settings.screenSize[1] * (settings.spawnRange[1] - settings.spawnRange[0]))
spawnOffsetX = int((settings.screenSize[0] - spawnWidth) / 2)
spawnOffsetY = int((settings.screenSize[1] - spawnHeight) / 2)
spawnAreaPoints = []

for i in range(settings.spawnVertices):
    angle = i * 2 * 3.14159 / settings.spawnVertices + (3.14159 / settings.spawnVertices)
    x = settings.screenSize[0]/2 + (spawnWidth / 2) * math.cos(angle)
    y = settings.screenSize[1]/2 + (spawnHeight / 2) * math.sin(angle)
    spawnAreaPoints.append((x, y)) # Vertices of spawn area

# "ALL" Spawn pattern / also used for random bounces in credits screen
topDir = ["S", "E", "W", "SE", "SW"]
leftDir = ["E", "S", "N", "NE", "SE"]
bottomDir = ["N", "W", "E", "NE", "NW"]
rightDir = ["W", "N", "S", "NW", "SW"]


# QUIT GAME
def quitGame():
    pygame.quit()
    sys.exit()


# ROTATE IMAGES
def rotateImage(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    rotatedRect = rotated.get_rect(center=rect.center)
    return rotated,rotatedRect


# MOVEMENT AND POSITION GENERATION
def getMovement(spawnPattern):
    top,bottom,left,right = [],[],[],[]
    if spawnPattern == "AGGRO": top, bottom, left, right, = ["SE", "SW", "S"], ["N", "NE", "NW"], ["E", "NE", "SE"], ["NW", "SW", "W"]
    elif spawnPattern == "TOP": top = ["SE", "SW", "S"]
    elif spawnPattern == "VERT": top, bottom = ["SE", "SW", "S"], ["N", "NE", "NW"]
    else: top, bottom, left, right = topDir, bottomDir, leftDir, rightDir # Default / "All"

    X = random.randint(settings.screenSize[0] * 0.1, settings.screenSize[0] * 0.99)
    Y = random.randint(settings.screenSize[1] * 0.1, settings.screenSize[1] * 0.99)

    lowerX = random.randint(-1,0)
    upperX =  random.randint(settings.screenSize[0], settings.screenSize[0] + 1)
    lowerY  = random.randint(-1,0)
    upperY = random.randint(settings.screenSize[1],settings.screenSize[1] + 1)

    possible = []
    if len(top) != 0: possible.append([X, lowerY, random.choice(top)])
    if len(bottom) != 0: possible.append([X, upperY, random.choice(bottom)])
    if len(left) != 0: possible.append([lowerX, Y, random.choice(left)])
    if len(right) != 0: possible.append([upperX, Y, random.choice(right)])

    movement = random.choice(possible)
    position = [movement[0], movement[1]]
    direction = movement[2]
    move = [position,direction]
    return move



# GAME
class Game:
    def __init__(self,records):
        
        self.gameConstants = assets.stageList

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
        self.cloudSpeed = settings.cloudSpeed

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
        self.cloudPos = settings.cloudStart # Background cloud position
        self.explosions = [] # Obstacle explosions
        self.cave,self.caveIndex = None, 0 # For cave levels
        self.musicMuted = settings.musicMuted
        self.clk = pygame.time.Clock() # Gameclock
        self.records = records # Game records dictionary
        self.usingController = settings.useController # Using controller for movement
        self.usingCursor = False # Using cursor for movement

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
                
        # SET VOLUME
        if not self.musicMuted: pygame.mixer.music.set_volume(settings.musicVolume / 100)
        else: pygame.mixer.music.set_volume(0)



    # MAIN GAME LOOP
    def update(self,player,obstacles,menu,events,lasers):
        for event in pygame.event.get():

            # EXIT
            if (event.type == pygame.KEYDOWN and event.key in escapeInput) or (gamePad is not None and gamePad.get_button(controllerExit) == 1) or event.type == pygame.QUIT:
                running = False
                quitGame()

            # MUTE
            if (event.type == pygame.KEYDOWN and event.key in muteInput) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

            # PAUSE GAME
            if game.pauseCount < settings.pauseMax and ( (event.type == pygame.KEYDOWN and event.key in pauseInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerPause)==1) ):
                game.pauseCount += 1
                menu.pause(game,player,obstacles,lasers)

            # INCREMENT TIMER
            if event.type == events.timerEvent: self.gameClock +=1

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
        screen.blit(assets.bgList[self.currentStage - 1][0], (0,0) )

        # CLOUD ANIMATION
        if settings.showBackgroundCloud:
            cloudImg = assets.bgList[self.currentStage - 1][1]
            cloudRect = cloudImg.get_rect(center = (settings.screenSize[0]/2,self.cloudPos))
            if cloudRect.bottom >= 0 and cloudRect.top <= settings.screenSize[1]: screen.blit(cloudImg, cloudRect) # Draw cloud
            elif cloudRect.top > settings.screenSize[1]: self.cloudPos = settings.cloudStart
            self.cloudPos += self.cloudSpeed

        # SHOW POINT SPAWN AREA (Testing)
        if settings.showSpawnArea: pygame.draw.polygon(screen, (255, 0, 0), spawnAreaPoints,1)

        # DRAW POINT
        screen.blit(self.thisPoint.image, self.thisPoint.rect)

        # CAVES
        if self.levelType == "CAVE":
            if self.cave is None: # SPAWN A CAVE
                self.cave = Cave(self.caveIndex)
                if self.caveIndex + 1 < len(assets.caveList) - 1: self.caveIndex+=1
            self.cave.update()
            screen.blit(self.cave.background,self.cave.rect)
            screen.blit(self.cave.image,self.cave.rect) # DRAW CAVE
            # COLLISION DETECTION
            if pygame.sprite.collide_mask(self.cave,player):
                if player.shields > 0: player.shieldDown(events)
                else:
                    player.explode(game,obstacles) # explosion
                    if not self.musicMuted: assets.explosionNoise.play()
                    menu.gameOver(self,player,obstacles) # Game over

        # EXITING CAVE
        elif self.cave is not None and self.cave.leave:
            if self.cave.rect.top > settings.screenSize[1]:
                self.cave.kill()
                self.cave = None
            else:
                self.cave.update()
                screen.blit(self.cave.background,self.cave.rect)
                screen.blit(self.cave.image,self.cave.rect) # DRAW CAVE
                # COLLISION DETECTION
                if pygame.sprite.collide_mask(self.cave,player):
                    if player.shields > 0: player.shieldDown(events)
                    else:
                        player.explode(game,obstacles) # explosion
                        if not self.musicMuted: assets.explosionNoise.play()
                        menu.gameOver(self,player,obstacles) # Game over

        # HUD
        if settings.showHUD: self.showHUD(player)

        # PLAYER/POWERUP COLLISION DETECTION
        if pygame.sprite.collide_mask(player,self.thisPoint):
            if self.thisPoint.powerUp == "Fuel": # Fuel cell collected
                player.fuel += player.maxFuel/4 # Replenish quarter tank
                if player.fuel > player.maxFuel: player.fuel = player.maxFuel

            elif self.thisPoint.powerUp == "Shield": player.shieldUp() # Shield piece collected
            self.score += 1
            self.thisPoint.kill()
            if not self.musicMuted: assets.powerUpNoise.play()
            self.lastPointPos = self.thisPoint.rect.center # Save last points position
            self.thisPoint = Point(player,self.lastPointPos) # spawn new point

        # UPDATE PLAYER
        player.movement(self)
        player.shoot(self,lasers,events,obstacles)
        player.boost(self,events)
        player.wrapping()

        # ROTATE PLAYER
        if player.angle != game.angle: newBlit = rotateImage(player.image,player.rect,player.angle)
        else: newBlit = player.image,player.rect

        # DRAW PLAYER
        screen.blit(newBlit[0],newBlit[1])

        # DRAW EXHAUST/BOOST
        if settings.drawExhaust:
            if player.boosting: newBlit = rotateImage(assets.spaceShipList[game.savedShipLevel]['boost'][player.boostState],player.rect,player.angle) # Boost frames
            else: newBlit = rotateImage(assets.spaceShipList[game.savedShipLevel]['exhaust'][player.exhaustState-1],player.rect,player.angle) # Regular exhaust frames
            screen.blit(newBlit[0],newBlit[1])

        # DRAW SHIELD
        if player.showShield:
            shieldImg,shieldImgRect = rotateImage(assets.playerShield, player.rect, player.angle)
            screen.blit(shieldImg,shieldImgRect)

        # DRAW LASERS
        self.laserUpdate(lasers,player,obstacles)

        # UPDATE OBSTACLES
        if len(obstacles) > 0:
            # OBSTACLE/PLAYER COLLISION DETECTION
            if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask):
                if player.shields > 0:player.shieldDown(events)
                else:
                    player.explode(game,obstacles) # Animation
                    if not self.musicMuted: assets.explosionNoise.play()
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
                            if not self.musicMuted: assets.impactNoise.play()
                            self.explosions.append(Explosion(obs))

                    # OBSTACLE/CAVE COLLISION DETECTION
                    elif self.cave is not None and pygame.sprite.collide_mask(obs,self.cave):
                        if not self.musicMuted: assets.impactNoise.play()
                        self.explosions.append(Explosion(obs))
                        obs.kill()

                    # ROTATE AND DRAW OBSTACLE
                    if not settings.performanceMode:
                        obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle
                        if obs.angle >= 360: obs.angle = -360
                        if obs.angle < 0: obs.angle +=360
                        newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
                        screen.blit(newBlit[0],newBlit[1]) # Blit obstacles

                    # OBSTACLE BOUNDARY HANDLING
                    obs.bound(obstacles)

            if settings.performanceMode:obstacles.draw(screen) # Potential performance improvement

            # DRAW EXPLOSIONS
            for debris in self.explosions:
                if debris.finished: self.explosions.remove(debris)
                else: debris.update()

        # UPDATE HIGH SCORE
        if self.gameClock > self.sessionLongRun: self.sessionLongRun = self.gameClock

        self.levelUpdater(player,obstacles,events) # LEVEL UP

        self.spawner(obstacles,player) # Spawn obstacles

        musicLoop() # Loop music

        # UPDATE SCREEN
        player.lastAngle = player.angle # Save recent player orientation
        if settings.resetPlayerOrientation: player.angle = self.angle # Reset player orientation
        player.boosting = False
        displayUpdate()
        self.clk.tick(settings.fps)


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
        self.obsHealth = self.savedConstants["obstacleHealth"]
        self.cloudSpeed = settings.cloudSpeed
        self.cloudPos = settings.cloudStart


    # DRAW CLOUD OUTSIDE OF MAIN LOOP
    def showBackgroundCloud(self):
        if settings.showBackgroundCloud:
            cloudImg = assets.bgList[game.currentStage - 1][1]
            cloudRect = cloudImg.get_rect(center = (settings.screenSize[0]/2,game.cloudPos))
            if cloudRect.bottom >= 0 and cloudRect.top <= settings.screenSize[1]: screen.blit(cloudImg, cloudRect) # Draw cloud


    # Draw frame outside of main loop
    def alternateUpdate(self,player,obstacles,events):
        for event in pygame.event.get(): pass # Pull events

        player.movement(self)
        player.wrapping()
        screen.fill(screenColor)
        screen.blit(assets.bgList[self.currentStage - 1][0], (0,0) )
        if self.cave is not None: screen.blit(self.cave.background,self.cave.rect)
        self.showBackgroundCloud()
        self.cloudPos += self.cloudSpeed
        if self.cave is not None:
            self.cave.update()
            if self.cave.rect.top <= settings.screenSize[1] and self.cave.rect.bottom >= 0: screen.blit(self.cave.image,self.cave.rect) # DRAW CAVE

        for obs in obstacles:
            obs.move(player)
            obs.activate()
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1])
            obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle

        self.clk.tick(settings.fps)


    # UPDATE GAME CONSTANTS
    def levelUpdater(self,player,obstacles,events):

        # UPDATES STAGE
        if self.currentStage < len(self.gameConstants): # Make sure there is a next stage
            if self.gameConstants[self.currentStage][0]["startTime"] == self.gameClock and not self.gameConstants[self.currentStage][0]["START"]: # Next stage's first level's activation time reached
                self.gameConstants[self.currentStage][0]["START"] = True # Mark as activated
                stageUpCloud = assets.stageCloudImg

                stageUpDisplay = assets.stageUpFont.render("STAGE UP", True, settings.primaryFontColor)
                stageUpRect = stageUpCloud.get_rect()
                stageUpRect.center = (settings.screenSize[0]/2, settings.stageUpCloudStartPos)
                stageUp , stageWipe = True , True

                # STAGE UP ANIMATION / Removes old obstacles
                while stageUp:
                    self.alternateUpdate(player,obstacles,events)

                    for obs in obstacles:
                        if obs.rect.top <= stageUpRect.bottom: obs.kill()

                    screen.blit(stageUpCloud,stageUpRect) # Draw cloud
                    screen.blit(stageUpDisplay,(stageUpRect.centerx - settings.screenSize[0]/5, stageUpRect.centery)) # Draw "STAGE UP" text
                    game.showHUD(player)
                    img, imgRect = rotateImage(player.image, player.rect, player.angle)
                    screen.blit(img,imgRect) # Draw player
                    stageUpRect.centery += settings.stageUpCloudSpeed

                    if stageUpRect.centery >= settings.screenSize[1]/2 and stageWipe:
                        self.currentStage += 1
                        self.currentLevel = 1
                        stageWipe = False

                    elif stageUpRect.centery >= settings.screenSize[1] * 2: stageUp = False
                    displayUpdate()
                    player.angle = self.angle

        # UPDATES LEVEL
        for levelDict in self.gameConstants[self.currentStage-1]:
            if levelDict["startTime"] == self.gameClock and not levelDict["START"] and ( (self.currentLevel > 1 or self.currentStage > 1) or (len(self.gameConstants[0]) > 1 and self.gameClock >= self.gameConstants[0][1]["startTime"]) ):
                if self.gameConstants[self.currentStage-1][self.currentLevel-1]["wipeObstacles"]:
                    levelUpCloud = assets.stageCloudImg
                    levelUpRect = levelUpCloud.get_rect()
                    levelUpRect.center = (settings.screenSize[0]/2, settings.stageUpCloudStartPos)
                    levelUp = True

                    # LEVEL UP ANIMATION / Removes old obstacles
                    while levelUp:

                        self.alternateUpdate(player,obstacles,events)
                        for obs in obstacles:
                            if obs.rect.centery <= levelUpRect.centery: obs.kill()

                        screen.blit(levelUpCloud,levelUpRect) # Draw cloud
                        game.showHUD(player)
                        img, imgRect = rotateImage(player.image, player.rect, player.angle)
                        screen.blit(img,imgRect) # Draw player

                        levelUpRect.centery += settings.levelUpCloudSpeed
                        if levelUpRect.top >= settings.screenSize[1]: levelUp = False
                        displayUpdate()
                        player.angle = self.angle

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
                self.cloudSpeed += settings.cloudSpeedAdder
                self.currentLevel += 1
                break


    # RESET LEVEL PROGRESS
    def resetAllLevels(self):
        for stage in self.gameConstants:
            for levels in stage: levels["START"] = False


    # REMOVE ALL OBSTACLES
    def killAllObstacles(self,obstacles):
        for obstacle in obstacles: obstacle.kill()
        obstacles.empty()


    # HUD
    def showHUD(self,player):

        # BORDER
        barBorder = pygame.Rect(settings.screenSize[0]/3, 0, (settings.screenSize[0]/3), 10)
        if player.hasShields or player.laserCost>0 or player.boostSpeed > player.baseSpeed or player.boostDrain > 0: pygame.draw.rect(screen,[0,0,0],barBorder)

        # SHIELDS DISPLAY
        if player.hasShields:
            currentShieldPieces = player.shieldPieces/player.shieldPiecesNeeded
            shieldRectWidth = (0.9*barBorder.width) * currentShieldPieces
            if player.shields > 0: shieldRectWidth = barBorder.width*0.99
            shieldRect = pygame.Rect(settings.screenSize[0]/3, 5, shieldRectWidth, 5)
            shieldRect.centerx = barBorder.centerx
            fullShieldRectWidth = settings.shieldChunkSize * player.shieldPiecesNeeded
            if player.shields > 0: pygame.draw.rect(screen,settings.fullShieldColor,shieldRect)
            elif player.shieldPieces > 0: pygame.draw.rect(screen,settings.shieldColor,shieldRect)

        # FUEL DISPLAY
        if player.boostDrain > 0 or player.laserCost > 0:
            currentFuel = player.fuel/player.maxFuel
            fuelRectWidth = currentFuel * (0.99*barBorder.width)
            fuelRect = pygame.Rect(settings.screenSize[0]/3, 0, fuelRectWidth, 5)
            if player.hasShields:fuelRect.centerx = barBorder.centerx
            else: fuelRect.center = barBorder.center
            pygame.draw.rect(screen, settings.fuelColor,fuelRect)

        # TIMER DISPLAY
        timerDisplay = assets.timerFont.render(str(self.gameClock), True, settings.secondaryFontColor)
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright)

        # STAGE DISPLAY
        stageNum = "Stage " + str(self.currentStage)
        stageDisplay = assets.stageFont.render( str(stageNum), True, settings.secondaryFontColor )
        stageRect = stageDisplay.get_rect(topleft = screen.get_rect().topleft)

        # LEVEL DISPLAY
        levelNum = "-  Level " + str(self.currentLevel)
        levelDisplay = assets.levelFont.render( str(levelNum), True, settings.secondaryFontColor )
        levelRect = levelDisplay.get_rect()
        levelRect.center = (stageRect.right + levelRect.width*0.65, stageRect.centery)

        # SCORE DISPLAY
        scoreNum = "Score " + str(self.score)
        scoreDisplay = assets.scoreFont.render(scoreNum, True, settings.secondaryFontColor)
        scoreRect = scoreDisplay.get_rect()
        scoreRect.topleft = (settings.screenSize[0] - (2*scoreRect.width), levelRect.y)

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
    def laserUpdate(self,lasers,player,obstacles):
        for laser in lasers:
            laser.update(player,lasers,obstacles)
            screen.blit(laser.image,laser.rect)


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
            else:
                if unlockNum >= numSkins: unlockNum = numSkins - 1
                return unlockNum


    # Get number of skins unlocked for a specified level number
    def skinsUnlocked(self,level): return self.getUnlocks(len(assets.spaceShipList[level]['skins']),unlockTimePerLevels[level])


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
        pygame.time.set_timer(self.timerEvent, settings.timerDelay)
        pygame.time.set_timer(self.fuelReplenish, player.fuelRegenDelay)
        pygame.time.set_timer(self.exhaustUpdate, settings.exhaustUpdateDelay)

    def laserCharge(self,player):
        pygame.time.set_timer(self.laserCooldown, player.laserFireRate)
        player.laserReady = False

    def boostCharge(self,player):
        pygame.time.set_timer(self.boostCooldown, settings.boostCooldownTime)
        player.boostReady = False

    def showShield(self): pygame.time.set_timer(self.shieldVisualDuration,settings.shieldVisualDuration)



# MENUS
class Menu:

    # START MENU
    def home(self,game,player):

        icons = []
        for icon in range(settings.maxIcons): icons.append(Icon())

        startDisplay = assets.startFont.render("N  VIGAT  R", True, settings.primaryFontColor)
        startRect = startDisplay.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))

        if not game.usingController or gamePad is None:
            startHelpDisplay = assets.startHelpFont.render("ESCAPE = Quit   SPACE = Start   F = Fullscreen   M = Mute   C = Credits", True, settings.primaryFontColor)
            skinHelpDisplay = assets.shipHelpFont.render("A/LEFT = Last skin     D/RIGHT = Next skin", True, settings.primaryFontColor)
            shipHelpDisplay = assets.shipHelpFont.render("S/DOWN = Last ship     W/UP = Next ship", True, settings.primaryFontColor)
            boostHelp = assets.shipHelpFont.render("SHIFT = Boost", True, settings.primaryFontColor)
            shootHelp = assets.shipHelpFont.render("CTRL = Shoot", True, settings.primaryFontColor)

        else:
            startHelpDisplay = assets.startHelpFont.render("START = Quit   A = Start   GUIDE = Fullscreen   LB = Mute   Y = Credits", True, settings.primaryFontColor)
            boostHelp = assets.shipHelpFont.render("LT = Boost", True, settings.primaryFontColor)
            shootHelp = assets.shipHelpFont.render("RT = Shoot", True, settings.primaryFontColor)
            skinHelpDisplay = assets.shipHelpFont.render("D-PAD LEFT = Last skin   D-PAD RIGHT = Next skin", True, settings.primaryFontColor)
            shipHelpDisplay = assets.shipHelpFont.render("D-PAD DOWN = Last ship   D-PAD UP = Next ship", True, settings.primaryFontColor)

        startHelpRect = startHelpDisplay.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]-settings.screenSize[1]/7))
        skinHelpRect = skinHelpDisplay.get_rect(center = (settings.screenSize[0]/4 + 40, settings.screenSize[1]-settings.screenSize[1]/7 + 70))
        shipHelpRect = shipHelpDisplay.get_rect(center = (settings.screenSize[0]/4 + 40, settings.screenSize[1]-settings.screenSize[1]/7 + 40))
        boostHelpRect = boostHelp.get_rect()
        shootHelpRect = shootHelp.get_rect()
        leftRect = assets.menuList[3].get_rect(center = (settings.screenSize[0] * 0.2 , settings.screenSize[1]/3) )
        rightRect = assets.menuList[4].get_rect(center = (settings.screenSize[0] * 0.8 , settings.screenSize[1]/3) )

        versionDisplay = assets.versionFont.render(version,True,settings.primaryFontColor)
        versionRect = versionDisplay.get_rect(topright = (startRect.right-25,startRect.bottom-25))
        bounceDelay = 5
        bounceCount = 0

        # UPDATE UNLOCKS
        if game.records["highScore"] < pointsForUnlock: game.shipUnlockNumber = 0
        elif game.records["highScore"] >= totalPointsForUnlock: game.shipUnlockNumber = len(assets.spaceShipList) - 1
        else:
            if game.records["highScore"] == pointsForUnlock or game.records["highScore"] < 2 * pointsForUnlock: game.shipUnlockNumber = 1
            else:
                game.shipUnlockNumber = 0
                startPoints = pointsForUnlock
                for i in range(totalShipTypes):
                    if game.records["highScore"] >= startPoints: game.shipUnlockNumber += 1
                    else: break
                    startPoints += pointsForUnlock

        if game.shipUnlockNumber >= len(assets.spaceShipList): game.shipUnlockNumber = len(assets.spaceShipList)-1
        game.skinUnlockNumber = game.skinsUnlocked(game.savedShipLevel)
        if game.skinUnlockNumber >= len(assets.spaceShipList[game.savedShipLevel]['skins']): game.skinUnlockNumber = len(assets.spaceShipList[game.savedShipLevel]['skins']) - 1

        if settings.defaultToHighSkin and not game.skipAutoSkinSelect:
            for i in range(game.skinUnlockNumber): player.nextSkin() # Gets highest unlocked skin by default
        elif game.skipAutoSkinSelect:
            for i in range(game.savedSkin): player.nextSkin()
        if settings.defaultToHighShip:
            if game.savedShipLevel != game.shipUnlockNumber:
                for i in range(game.shipUnlockNumber): player.toggleSpaceShip(game,True) # Gets highest unlocked ship by default

        startOffset = 100
        startDelay = 1
        iconPosition, startDelayCounter = startOffset, 0

        while game.mainMenu:

            self.menuMusicLoop() # Keep music looping
            if bounceCount >= bounceDelay: bounceCount = 0
            else: bounceCount +=1

            for event in pygame.event.get():
                # START
                if (event.type == pygame.KEYDOWN and event.key in startInput) or (gamePad is not None and gamePad.get_button(controllerSelect) == 1) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1):
                    if (event.type == pygame.KEYDOWN and event.key in startInput):
                        game.usingCursor, game.usingController = False, False
                        pygame.mouse.set_visible(False)

                    elif (gamePad is not None and gamePad.get_button(controllerSelect) == 1):
                        game.usingController,game.usingCursor = True,False
                        pygame.mouse.set_visible(False)

                    elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1):
                        game.usingCursor, game.usingController = True, False
                        pygame.mouse.set_visible(not settings.rawCursorMode)

                    game.savedSkin = player.currentImageNum

                    while iconPosition > 0:

                        if startDelayCounter >= startDelay: startDelayCounter = 0
                        else: startDelayCounter +=1

                        # Start animation
                        screen.fill(screenColor)
                        screen.blit(assets.bgList[game.currentStage - 1][0],(0,0))
                        screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Current spaceship
                        displayUpdate()

                        if startDelayCounter >= startDelay: iconPosition-=1
                    game.mainMenu = False
                    return

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1):
                    toggleScreen()

                # NEXT SPACESHIP SKIN
                elif (event.type == pygame.KEYDOWN and event.key in rightInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerNextSkin) or (event.type == pygame.JOYBUTTONDOWN and type(controllerNextSkin) == int and gamePad.get_button(controllerNextSkin)==1))):
                    player.nextSkin()

                # PREVIOUS SPACESHIP SKIN
                elif (event.type == pygame.KEYDOWN and event.key in leftInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerLastSkin) or (event.type == pygame.JOYBUTTONDOWN and type(controllerLastSkin) == int and gamePad.get_button(controllerLastSkin)==1))):
                    player.lastSkin()

                # NEXT SHIP TYPE
                elif (event.type == pygame.KEYDOWN and event.key in upInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerNextShip) or (event.type == pygame.JOYBUTTONDOWN and type(controllerNextShip) == int and gamePad.get_button(controllerNextShip)==1))):
                    player.toggleSpaceShip(game,True)

                # PREVIOUS SHIP TYPE
                elif (event.type == pygame.KEYDOWN and event.key in downInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerLastShip) or (event.type == pygame.JOYBUTTONDOWN and type(controllerLastShip) == int and gamePad.get_button(controllerLastShip)==1))):
                    player.toggleSpaceShip(game,False)

                # EXIT
                if (event.type == pygame.KEYDOWN and event.key in escapeInput) or (gamePad is not None and gamePad.get_button(controllerExit) == 1) or event.type == pygame.QUIT:
                    running = False
                    quitGame()

                # MUTE
                if (event.type == pygame.KEYDOWN) and (event.key in muteInput) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

                # CREDITS
                if (event.type == pygame.KEYDOWN and event.key in creditsInput) or (gamePad is not None and gamePad.get_button(controllerCredits) == 1): menu.creditScreen()

                 # SWITCH CONTROL TYPE
                if game.usingController and event.type == pygame.KEYDOWN:
                    game.usingController = False
                    startHelpDisplay = assets.startHelpFont.render("ESCAPE = Quit   SPACE = Start   F = Fullscreen   M = Mute   C = Credits", True, settings.primaryFontColor)
                    boostHelp = assets.shipHelpFont.render("SHIFT = Boost", True, settings.primaryFontColor)
                    shootHelp = assets.shipHelpFont.render("CTRL = Shoot", True, settings.primaryFontColor)
                    skinHelpDisplay = assets.shipHelpFont.render("A/LEFT = Last skin     D/RIGHT = Next skin", True, settings.primaryFontColor)
                    shipHelpDisplay = assets.shipHelpFont.render("S/DOWN = Last ship     W/UP = Next ship", True, settings.primaryFontColor)

                elif gamePad is not None and not game.usingController and (event.type == pygame.JOYHATMOTION or event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONUP):
                    game.usingController = True
                    startHelpDisplay = assets.startHelpFont.render("START = Quit   A = Start   GUIDE = Fullscreen   LB = Mute   Y = Credits", True, settings.primaryFontColor)
                    boostHelp = assets.shipHelpFont.render("LT = Boost", True, settings.primaryFontColor)
                    shootHelp = assets.shipHelpFont.render("RT = Shoot", True, settings.primaryFontColor)
                    skinHelpDisplay = assets.shipHelpFont.render("D-PAD LEFT = Last skin   D-PAD RIGHT = Next skin", True, settings.primaryFontColor)
                    shipHelpDisplay = assets.shipHelpFont.render("D-PAD DOWN = Last ship   D-PAD UP = Next ship", True, settings.primaryFontColor)

            # GET SHIP CONTROLS
            if player.hasGuns and player.boostSpeed > player.baseSpeed: # has guns and boost
                boostHelpRect.center = settings.screenSize[0]*3/4 - 60, settings.screenSize[1]-settings.screenSize[1]/7 + 40
                shootHelpRect.center = settings.screenSize[0]*3/4 + 60, settings.screenSize[1]-settings.screenSize[1]/7 + 40
            elif player.hasGuns: shootHelpRect.center = settings.screenSize[0]*3/4, settings.screenSize[1]-settings.screenSize[1]/7 + 40 # has guns only
            elif player.boostSpeed > player.baseSpeed: boostHelpRect.center = settings.screenSize[0]*3/4, settings.screenSize[1]-settings.screenSize[1]/7 + 40 # has boost only

            screen.fill(screenColor)
            screen.blit(assets.bgList[game.currentStage - 1][0],(0,0))

            # ANIMATION
            if settings.showMenuIcons:
                for icon in icons:
                    if bounceCount == bounceDelay: icon.move()
                    icon.draw()

            screen.blit(startDisplay,startRect) # Menu Logo
            if settings.showVersion: screen.blit(versionDisplay,versionRect) # Version info
            screen.blit(startHelpDisplay, startHelpRect) # Game controls

            # SHOW SHIP CONTROLS
            if player.hasGuns: screen.blit(shootHelp,shootHelpRect)
            if player.boostSpeed > player.baseSpeed: screen.blit(boostHelp,boostHelpRect)
            if unlockTimePerLevels[game.savedShipLevel] != None and game.records["longestRun"] >= unlockTimePerLevels[game.savedShipLevel] and len(assets.spaceShipList[game.savedShipLevel]['skins']) > 1: screen.blit(skinHelpDisplay,skinHelpRect) # Show switch skin controls
            if game.shipUnlockNumber > 0: screen.blit(shipHelpDisplay,shipHelpRect)
            screen.blit(player.image, (player.rect.x,player.rect.y + startOffset)) # Current spaceship

            # LOGO LETTERS
            screen.blit(assets.menuList[0],(-14 + startRect.left + assets.menuList[0].get_width() - assets.menuList[0].get_width()/10,settings.screenSize[1]/2 - 42)) # "A" symbol
            screen.blit(assets.menuList[1],(-16 + settings.screenSize[0] - startRect.centerx + assets.menuList[1].get_width() * 2,settings.screenSize[1]/2 - 35)) # "O" symbol

            # UFO ICONS
            if settings.showMenuIcons:
                screen.blit(assets.menuList[2],(settings.screenSize[0]/2 - assets.menuList[2].get_width()/2,settings.screenSize[1]/8)) # Big icon
                screen.blit(assets.menuList[3],leftRect) # Left UFO
                screen.blit(assets.menuList[4],rightRect) # Right UFO

            displayUpdate()


    # PAUSE SCREEN
    def pause(self,game,player,obstacles,lasers):
        pygame.mixer.music.pause()
        playerBlit = rotateImage(player.image,player.rect,player.lastAngle)
        paused = True

        pausedDisplay = assets.pausedFont.render("Paused", True, settings.secondaryFontColor)
        pausedRect = pausedDisplay.get_rect()
        pausedRect.center = (settings.screenSize[0]/2, settings.screenSize[1]/2)

        # REMAINING PAUSES
        pauseNum = str(settings.pauseMax - game.pauseCount) + " Pauses left"

        if game.pauseCount >= settings.pauseMax: pauseNum = "Out of pauses"

        pauseDisplay = assets.pauseCountFont.render(pauseNum,True,settings.secondaryFontColor)
        pauseRect = pauseDisplay.get_rect()
        pauseRect.center = (settings.screenSize[0]/2,settings.screenSize[1]-16)

        while paused:
            screen.fill(screenColor)
            screen.blit(assets.bgList[game.currentStage - 1][0], (0,0) )
            game.showBackgroundCloud()
            if game.cave is not None:
                screen.blit(game.cave.background,game.cave.rect)
                screen.blit(game.cave.image,game.cave.rect) # Draw cave

            game.showHUD(player)
            screen.blit(game.thisPoint.image, game.thisPoint.rect)
            screen.blit(playerBlit[0],playerBlit[1])

            if player.showShield:
                shieldImg,shieldImgRect = rotateImage(assets.playerShield, player.rect, player.angle)
                screen.blit(shieldImg,shieldImgRect)

            if not settings.performanceMode:
                for obs in obstacles: # Draw obstacles
                    newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
                    screen.blit(newBlit[0],newBlit[1])
            else: obstacles.draw(screen)

            for laser in lasers: screen.blit(laser.image,laser.rect)

            screen.blit(pauseDisplay, pauseRect)
            screen.blit(pausedDisplay,pausedRect)
            displayUpdate()

            for event in pygame.event.get():
                # EXIT
                if event.type == pygame.QUIT: quitGame()

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1):
                    toggleScreen()

                # UNPAUSE
                if (event.type == pygame.KEYDOWN and (event.key in escapeInput or event.key in startInput)) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and (gamePad.get_button(controllerBack) == 1 or gamePad.get_button(controllerPause) == 1)):
                    pygame.mixer.music.unpause()
                    paused = False


    # GAME OVER SCREEN
    def gameOver(self,game,player,obstacles):
        gameOver = True
        game.thisPoint = Point(None,None)
        pygame.mixer.music.stop()

        # Show cursor
        pygame.mouse.set_visible(settings.cursorMode)

        # Update game records
        newLongRun = False
        newHighScore = False

        game.records["timePlayed"] += game.gameClock # Update total time played
        game.records["attempts"] += 1 # Update total attempts
        game.records["points"] += game.score # Update saved points

        # NEW LONGEST RUN
        if game.sessionLongRun > game.records["longestRun"]:
            newLongRun = True
            game.records["longestRun"] = game.sessionLongRun

        # NEW HIGH SCORE
        if game.score > game.records["highScore"]:
            newHighScore = True
            game.records["highScore"] = game.score

        assets.storeRecords(game.records)

        statsOffsetY = settings.screenSize[1]/10
        statsSpacingY = settings.screenSize[1]/20

        # "GAME OVER" text
        gameOverDisplay = assets.gameOverFont.render("GAME OVER", True, [255,0,0])
        gameOverRect = gameOverDisplay.get_rect()
        gameOverRect.center = (settings.screenSize[0]/2, settings.screenSize[1]/3)

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
        scoreDisplay = assets.statFont.render(scoreLine, True, settings.primaryFontColor)
        highScoreDisplay = assets.statFont.render(highScoreLine, True, settings.primaryFontColor)
        newHighScoreDisplay = assets.statFont.render(newHighScoreLine, True, settings.primaryFontColor)
        longestRunDisplay = assets.statFont.render(overallLongestRunLine, True, settings.primaryFontColor)
        survivedDisplay = assets.statFont.render(survivedLine, True, settings.primaryFontColor)
        levelDisplay = assets.statFont.render(levelLine, True, settings.primaryFontColor)
        newLongestRunDisplay = assets.statFont.render(newLongestRunLine, True, settings.primaryFontColor)
        attemptDisplay = assets.statFont.render(attemptLine, True, settings.primaryFontColor)
        timeWastedDisplay = assets.statFont.render(timeWasted,True,settings.primaryFontColor)
        if not game.usingController or gamePad is None: exitDisplay = assets.exitFont.render("TAB = Menu     SPACE = Restart    ESCAPE = Quit    C = Credits", True, settings.primaryFontColor)
        else: exitDisplay = assets.exitFont.render("SELECT = Menu    A = Restart    START = Quit    Y = Credits", True, settings.primaryFontColor)

        # Rects
        scoreRect = scoreDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY +statsSpacingY * 1))
        highScoreRect = highScoreDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY +statsSpacingY * 2))
        newHighScoreRect = newHighScoreDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY +statsSpacingY * 1.5))
        survivedRect = survivedDisplay.get_rect(center =(settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY + statsSpacingY * 3))
        longestRunRect = longestRunDisplay.get_rect(center =(settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY +statsSpacingY * 4))
        newLongestRunRect = newLongestRunDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY +statsSpacingY * 3.5))
        levelRect = levelDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 +statsOffsetY +statsSpacingY * 5))
        attemptRect = attemptDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY +statsSpacingY * 6))
        wastedRect = timeWastedDisplay.get_rect(center = (settings.screenSize[0]/2, settings.screenSize[1]/3 +statsOffsetY +statsSpacingY * 7))
        exitRect = exitDisplay.get_rect(center =(settings.screenSize[0]/2, settings.screenSize[1]/3 + 2* statsOffsetY +statsSpacingY * 8))

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
            # BACKGROUND
            screen.fill(screenColor)
            screen.blit(assets.bgList[game.currentStage - 1][0], (0,0) )
            game.showBackgroundCloud()
            if game.cave is not None:
                screen.blit(game.cave.background,game.cave.rect)
                screen.blit(game.cave.image,game.cave.rect) # Draw cave

            screen.blit(player.finalImg,player.finalRect) # Explosion

            pygame.draw.rect(screen, screenColor, [gameOverRect.x - 12,gameOverRect.y + 4,gameOverRect.width + 16, gameOverRect.height - 16],0,10)
            screen.blit(gameOverDisplay,gameOverRect)
            self.drawGameOverLabels(displayTextList,newHighScore,newLongRun)
            screen.blit(exitDisplay,exitRect)
            displayUpdate()

            for event in pygame.event.get():

                # CREDITS
                if event.type == pygame.KEYDOWN and event.key in creditsInput or (gamePad is not None and gamePad.get_button(controllerCredits) == 1): menu.creditScreen()

                # EXIT
                if (event.type == pygame.KEYDOWN and event.key in escapeInput) or (gamePad is not None and gamePad.get_button(controllerExit) == 1) or event.type == pygame.QUIT:
                    running = False
                    quitGame()

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1): toggleScreen()

                # BACK TO MENU
                elif (event.type == pygame.KEYDOWN and event.key in backInput) or (gamePad is not None and gamePad.get_button(controllerMenu) == 1) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] == 1):
                    if (event.type == pygame.KEYDOWN and event.key in backInput): game.usingController,game.usingCursor = False,False
                    elif (gamePad is not None and gamePad.get_button(controllerBack) == 1): game.usingController,game.usingCursor = True,False
                    elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]==1): game.usingCursor, game.usingController = True, False
                    pygame.mouse.set_visible(settings.cursorMode) # Show cursor at menu
                    game.reset(player,obstacles)
                    game.mainMenu = True
                    game.skipAutoSkinSelect = True
                    gameLoop()

                # RESTART GAME
                elif (event.type == pygame.KEYDOWN and event.key in startInput) or (gamePad is not None and gamePad.get_button(controllerSelect) == 1) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == 1):
                    if (event.type == pygame.KEYDOWN and event.key in startInput): game.usingController,game.usingCursor = False,False
                    elif (gamePad is not None and gamePad.get_button(controllerBack) == 1): game.usingController,game.usingCursor = True,False
                    elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1): game.usingCursor, game.usingController = True, False
                    pygame.mouse.set_visible(game.usingCursor and not settings.rawCursorMode)
                    game.reset(player,obstacles)
                    player.updatePlayerConstants(game)
                    running = True
                    gameLoop()


    # Draw labels from formatted list of rects and displays, first 4 lines arranged based on truth value of two booleans
    def drawGameOverLabels(self,textList, conditionOne, conditionTwo):
        statsSpacingY = 50
        statsOffsetY = 10
        skipped = 0
        # Both true
        if conditionOne and conditionTwo:
            for x in range(len(textList)):
                if x != 0 and x!= 1 and x!= 3 and x!= 4: # Skip 1st, 2nd, 4th, and 5th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                    screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1

        # newHighScore
        elif conditionOne and not conditionTwo:
            for x in range(len(textList)):
                if x != 0 and x!= 1 and x!= 5: # Skip 1st, 2nd, and 6th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3+ statsOffsetY + statsSpacingY * (x+1 - skipped)
                    screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1

        # newLongestRun
        elif conditionTwo and not conditionOne:
            for x in range(len(textList)):
                if x != 2 and x!= 3 and x!= 4: # Skip 3rd, 4th, and 5th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                    screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1

        else:
            for x in range(len(textList)):
                if x != 2 and x != 5: # Skip 3rd and 6th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3 + statsOffsetY + statsSpacingY * (x+1 - skipped)
                    screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1


    # CREDITS
    def creditScreen(self):
        global screen
        rollCredits = True
        posX = settings.screenSize[0]/2
        posY = settings.screenSize[1]/2

        createdByLine = "Created by Mike Pistolesi"
        creditsLine = "with art by Collin Guetta"
        musicCreditsLine = '& music by Dylan Kusenko'

        createdByDisplay = assets.creatorFont.render(createdByLine, True, settings.secondaryFontColor)
        creditsDisplay = assets.creditsFont.render(creditsLine, True, settings.secondaryFontColor)
        musicCreditsDisplay = assets.creditsFont.render(musicCreditsLine, True, settings.secondaryFontColor)

        createdByRect = createdByDisplay.get_rect(center = (posX, posY - settings.screenSize[1]/15) )
        creditsRect = creditsDisplay.get_rect(center = (posX,posY))
        musicCreditsRect = musicCreditsDisplay.get_rect(center = (posX,posY+ settings.screenSize[1]/15))

        bounceCount = 0
        direction = self.randomEightDirection()

        extras = []
        bgShips = []
        waitToSpawn = True
        backGroundShipSpawnEvent = pygame.USEREVENT + 6
        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

        if len(assets.donations) == 0: extrasCap = settings.maxExtras

        elif len(assets.donations) > 0:
            if len(assets.donations) < settings.maxExtras: extrasCap = len(assets.donations)
            else: extrasCap = settings.maxExtras

        while rollCredits:
            self.menuMusicLoop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quitGame()

                # TOGGLE MUTE
                if ((event.type == pygame.KEYDOWN) and (event.key in muteInput)) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1):
                    toggleScreen()

                # SHIP SPAWN DELAY
                if event.type == backGroundShipSpawnEvent:
                    waitToSpawn = False

                # RETURN TO GAME
                elif (event.type == pygame.KEYDOWN and (event.key in escapeInput or event.key in creditsInput or event.key in startInput or event.key in backInput) ) or (gamePad is not None and (gamePad.get_button(controllerBack) == 1 or gamePad.get_button(controllerCredits) == 1)):
                    rollCredits = False

            screen.fill(screenColor)
            screen.blit(assets.bgList[game.currentStage - 1][0],(0,0))
            game.showBackgroundCloud()

            for ship in bgShips:
                ship.move()
                if ship.active:
                    if len(assets.donations) == 0: ship.draw(False,settings.showSupporterNames)
                    else: ship.draw(settings.showBackgroundShips,settings.showSupporterNames)
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
                if len(assets.donations) == 0: # If failed to load dictionary, display defaults to version number
                    if len(bgShips)==0:
                        bgShips.append(BackgroundShip(version,1))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

                elif len(assets.donations) == 1:
                    if len(bgShips) == 0:
                        name,value = list(assets.donations.items())[0]
                        bgShips.append(BackgroundShip(name,value))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

                else:
                    pool = list(assets.donations.keys())

                    for xtra in extras:
                        if xtra[0] in pool: pool.remove(xtra[0]) # Already on screen

                    if len(pool) > 0:
                        chosen = random.choice(pool) # get name from pool
                        extra = chosen,assets.donations[chosen]
                        extras.append(extra)
                        bgShips.append(BackgroundShip(extra[0],extra[1]))
                        waitToSpawn = True
                        pygame.time.set_timer(backGroundShipSpawnEvent, random.randint(settings.minBackgroundShipSpawnDelay,settings.maxBackgroundShipSpawnDelay))

            screen.blit(createdByDisplay,createdByRect)
            screen.blit(creditsDisplay,creditsRect)
            screen.blit(musicCreditsDisplay,musicCreditsRect)
            displayUpdate()

            # BOUNCE OFF EDGES
            if createdByRect.right > settings.screenSize[0]: direction = rightDir[random.randint(0, len(rightDir) - 1)]
            if createdByRect.left < 0: direction = leftDir[random.randint(0, len(leftDir) - 1)]
            if musicCreditsRect.bottom > settings.screenSize[1]: direction = bottomDir[random.randint(0, len(bottomDir) - 1)]
            if createdByRect.top < 0 : direction = topDir[random.randint(0, len(topDir) - 1)]

            if bounceCount == 0:
                if "N" in direction:
                    createdByRect.centery-= settings.mainCreditsSpeed
                    creditsRect.centery-= settings.mainCreditsSpeed
                    musicCreditsRect.centery-= settings.mainCreditsSpeed

                if "S" in direction:
                    createdByRect.centery+= settings.mainCreditsSpeed
                    creditsRect.centery+= settings.mainCreditsSpeed
                    musicCreditsRect.centery+= settings.mainCreditsSpeed

                if "E" in direction:
                    createdByRect.centerx+= settings.mainCreditsSpeed
                    creditsRect.centerx+= settings.mainCreditsSpeed
                    musicCreditsRect.centerx+= settings.mainCreditsSpeed

                if "W" in direction:
                    createdByRect.centerx-= settings.mainCreditsSpeed
                    creditsRect.centerx-= settings.mainCreditsSpeed
                    musicCreditsRect.centerx-= settings.mainCreditsSpeed

            bounceCount +=1
            if bounceCount >= settings.mainCreditsDelay: bounceCount = 0


    # GET RANDOM DIRECTION - include diagonal
    def randomEightDirection(self):
        directions = ["N","S","E","W","NW","SW","NE","SE"]
        direction = directions[random.randint(0, len(directions)-1)]
        return direction


    # MENU MUSIC LOOP
    def menuMusicLoop(self):
        if pygame.mixer.music.get_pos() >= settings.menuLoopEnd:
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(settings.menuLoopStart)
            pygame.mixer.music.play()



# PLAYER
class Player(pygame.sprite.Sprite):
        def __init__(self,game):
            super().__init__()

            # GET DEFAULT SHIP CONSTANTS
            self.currentImageNum = 0
            self.speed,self.baseSpeed,self.boostSpeed = assets.spaceShipList[game.savedShipLevel]['stats']["speed"],assets.spaceShipList[game.savedShipLevel]['stats']["speed"],assets.spaceShipList[game.savedShipLevel]['stats']["boostSpeed"]
            self.image = assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]
            self.laserImage = assets.spaceShipList[game.savedShipLevel]['laser']
            self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.fuel, self.maxFuel = assets.spaceShipList[game.savedShipLevel]['stats']["startingFuel"], assets.spaceShipList[game.savedShipLevel]['stats']["maxFuel"]
            self.angle, self.lastAngle = 0, 0
            self.exhaustState, self.boostState, self.explosionState = 0, 0, 0 # Indexes of animation frames
            self.finalImg, self.finalRect = '','' # Last frame of exhaust animation for boost
            self.fuelRegenNum = assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegen"]
            self.fuelRegenDelay = assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegenDelay"]
            self.boostDrain = assets.spaceShipList[game.savedShipLevel]['stats']["boostDrain"]
            self.laserCost = assets.spaceShipList[game.savedShipLevel]['stats']["laserCost"]
            self.laserSpeed = assets.spaceShipList[game.savedShipLevel]['stats']["laserSpeed"]
            self.laserFireRate = assets.spaceShipList[game.savedShipLevel]['stats']["fireRate"]
            self.laserCollat = assets.spaceShipList[game.savedShipLevel]['stats']["collats"]
            self.hasGuns, self.laserReady, self.boostReady = assets.spaceShipList[game.savedShipLevel]['stats']["hasGuns"], True, True
            self.hasShields = assets.spaceShipList[game.savedShipLevel]['stats']["hasShields"]
            self.shields = assets.spaceShipList[game.savedShipLevel]['stats']["startingShields"]
            self.shieldPieces = assets.spaceShipList[game.savedShipLevel]['stats']["startingShieldPieces"]
            self.shieldPiecesNeeded = assets.spaceShipList[game.savedShipLevel]['stats']["shieldPiecesNeeded"]
            self.damage = assets.spaceShipList[game.savedShipLevel]['stats']["laserDamage"]
            self.laserType = assets.spaceShipList[game.savedShipLevel]['stats']["laserType"]
            self.showShield,self.boosting = False,False
            self.movementType = settings.playerMovement
            if settings.cursorMode: self.lastCursor = pygame.Vector2(0,0)


        # MOVEMENT
        def movement(self,game):
            if self.movementType == "DEFAULT": self.vectorMovement(True)
            elif self.movementType == "ORIGINAL": self.vectorMovement(False)
            else: self.vectorMovement(True)


        # VECTOR BASED MOVEMENT
        def vectorMovement(self,defaultMovement):
            # KEYBOARD
            if not game.usingController and not game.usingCursor:
                key = pygame.key.get_pressed()
                direction = pygame.Vector2(0, 0) # Get new vector
                if any(key[bind] for bind in upInput): direction += pygame.Vector2(0, -1)
                if any(key[bind] for bind in downInput): direction += pygame.Vector2(0, 1)
                if any(key[bind] for bind in leftInput): direction += pygame.Vector2(-1, 0)
                if any(key[bind] for bind in rightInput): direction += pygame.Vector2(1, 0)
                if direction.magnitude_squared() > 0:
                    if defaultMovement:
                        direction.normalize_ip()
                        direction *= 1.414  # sqrt(2)
                    if not any(key[bind] for bind in brakeInput): self.rect.move_ip(direction * self.speed) # MOVE PLAYER
                    if direction.x != 0 or direction.y != 0: self.angle = direction.angle_to(pygame.Vector2(0, -1)) # GET PLAYER ANGLE

            # CONTROLLER
            elif gamePad is not None and game.usingController:
                direction = pygame.Vector2(0, 0) # Get new vector
                xLeft = gamePad.get_axis(controllerMoveX)
                yLeft = gamePad.get_axis(controllerMoveY)
                xRight = gamePad.get_axis(controllerRotateX)
                yRight = gamePad.get_axis(controllerRotateY)

                if abs(xRight) > 0.3 or abs(yRight) > 0.3: xTilt, yTilt, braking = xRight, yRight, True
                else: xTilt, yTilt, braking = xLeft, yLeft, False

                if yTilt < -0.5: direction += pygame.Vector2(0, -1)
                if yTilt > 0.5: direction += pygame.Vector2(0, 1)
                if xTilt < -0.5: direction += pygame.Vector2(-1, 0)
                if xTilt > 0.5: direction += pygame.Vector2(1, 0)
                if direction.magnitude_squared() > 0:
                    if defaultMovement:
                        direction.normalize_ip()
                        direction *= 1.414  # sqrt(2)
                    if not braking: self.rect.move_ip(direction * self.speed) # MOVE PLAYER
                    if direction.x != 0 or direction.y != 0:self.angle = direction.angle_to(pygame.Vector2(0, -1)) # GET PLAYER ANGLE

            # CURSOR BASED MOVEMENT
            elif game.usingCursor:
                resetCursor()
                # RAW CURSOR MODE
                if settings.rawCursorMode:
                    cursor = pygame.Vector2(pygame.mouse.get_pos())
                    self.rect.center = cursor
                    if pygame.Vector2.distance_to(cursor, self.lastCursor) > 0.5: self.angle = (cursor - self.lastCursor).angle_to(pygame.Vector2(1, 0))-90
                    self.lastCursor = cursor

                else:
                    # FOLLOW CURSOR MODE
                    cursorX, cursorY = pygame.mouse.get_pos()
                    cursorDirection = pygame.Vector2(cursorX, cursorY)
                    if math.dist(self.rect.center,(cursorX,cursorY)) >= settings.cursorRotateDistance:
                        direction = cursorDirection - pygame.Vector2(self.rect.centerx, self.rect.centery)
                        if direction.magnitude_squared() > 0:
                            direction.normalize_ip()
                            direction *= 1.414
                        velocity = direction * self.speed
                        self.angle = direction.angle_to(pygame.Vector2(0, -1))
                        if math.dist(self.rect.center,(cursorX,cursorY)) >= settings.cursorFollowDistance:
                            self.rect.centerx += velocity.x
                            self.rect.centery += velocity.y


        # SPEED BOOST
        def boost(self,game,events):
            if self.boostReady:
                if self.fuel - self.boostDrain > self.boostDrain:
                    # KEYBOARD
                    if (gamePad is None or not game.usingController) and (not game.usingCursor):
                        key = pygame.key.get_pressed()
                        if (any(key[bind] for bind in brakeInput)) or (any(key[bind] for bind in boostInput) and ( any(key[bind] for bind in leftInput) and  any(key[bind] for bind in upInput) and any(key[bind] for bind in downInput) and any(key[bind] for bind in rightInput) )):
                            return # Cannot boost with all directional inputs held together

                        elif any(key[bind] for bind in boostInput) and ( any(key[bind] for bind in leftInput) or any(key[bind] for bind in upInput) or any(key[bind] for bind in downInput) or any(key[bind] for bind in rightInput)):
                            self.speed = self.boostSpeed
                            self.fuel -= self.boostDrain
                            if not self.boosting: self.boosting = True
                            if self.boostState + 1 < len(assets.spaceShipList[game.savedShipLevel]['boost']): self.boostState += 1
                            else: self.boostState = 0

                        else: self.speed = self.baseSpeed

                    # CONTROLLER
                    elif game.usingController and not game.usingCursor:
                        xTilt,yTilt = gamePad.get_axis(controllerMoveX),gamePad.get_axis(controllerMoveY)
                        xRot,yRot = gamePad.get_axis(controllerRotateX),gamePad.get_axis(controllerRotateY)
                        if (abs(xRot) > 0.1 and abs(yRot) > 0.1) or (abs(xTilt) <= 0.1 and abs(yTilt) <= 0.1): pass # Cannot boost in place
                        elif (abs(xTilt) > 0.1 or abs(yTilt)) > 0.1 and gamePad.get_axis(controllerBoost) > 0.5:
                            self.speed = self.boostSpeed
                            self.fuel -= self.boostDrain
                            if not self.boosting: self.boosting = True
                            if self.boostState + 1 < len(assets.spaceShipList[game.savedShipLevel]['boost']): self.boostState += 1
                            else: self.boostState = 0

                        else: self.speed = self.baseSpeed

                    elif game.usingCursor:
                        button = pygame.mouse.get_pressed()
                        pygame.mouse.get_pos()
                        if math.dist(self.rect.center,pygame.mouse.get_pos()) >= settings.cursorFollowDistance and pygame.mouse.get_pressed()[2] == 1:
                            self.speed = self.boostSpeed
                            self.fuel -= self.boostDrain
                            if not self.boosting: self.boosting = True
                            if self.boostState + 1 < len(assets.spaceShipList[game.savedShipLevel]['boost']): self.boostState += 1
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
                if (gamePad is None or not game.usingController) and (not game.usingCursor):
                    key = pygame.key.get_pressed()
                    if any(key[bind] for bind in shootInput) and self.fuel - self.laserCost > 0:
                        lasers.add(Laser(self,obstacles))
                        if not game.musicMuted: assets.laserNoise.play()
                        self.fuel -= self.laserCost
                        events.laserCharge(self)

                # CONTROLLER
                elif game.usingController and not game.usingCursor:
                    if gamePad.get_axis(controllerShoot) > 0.5 and self.fuel - self.laserCost > 0:
                        lasers.add(Laser(self,obstacles))
                        if not game.musicMuted: assets.laserNoise.play()
                        self.fuel -= self.laserCost
                        events.laserCharge(self)

                # CURSOR
                elif game.usingCursor:
                    if pygame.mouse.get_pressed()[0]== 1 and self.fuel - self.laserCost > 0:
                        lasers.add(Laser(self,obstacles))
                        if not game.musicMuted: assets.laserNoise.play()
                        self.fuel -= self.laserCost
                        events.laserCharge(self)


        # WRAP AROUND SCREEN
        def wrapping(self):
            if self.rect.centery > settings.screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = settings.screenSize[1]
            if self.rect.centerx > settings.screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = settings.screenSize[0]


        # GET NEXT SKIN
        def nextSkin(self):
            if self.currentImageNum + 1 < len(assets.spaceShipList[game.savedShipLevel]['skins']):
                if not settings.devMode and self.currentImageNum + 1 > game.skinUnlockNumber:
                    self.image = assets.spaceShipList[game.savedShipLevel]['skins'][0]
                    self.currentImageNum = 0
                else:
                    self.currentImageNum+=1
                    self.image = assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]
            else:
                self.image = assets.spaceShipList[game.savedShipLevel]['skins'][0]
                self.currentImageNum = 0
            self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)


        # GET PREVIOUS SKIN
        def lastSkin(self):
            if self.currentImageNum >= 1:
                self.currentImageNum-=1
                self.image = assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]
            else:
                if game.skinUnlockNumber == 0 and not settings.devMode: return
                else:
                    if settings.devMode: self.currentImageNum = len(assets.spaceShipList[game.savedShipLevel]['skins']) - 1
                    else: self.currentImageNum = game.skinUnlockNumber
                    self.image = assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]

            self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)


        # SWITCH SHIP TYPE
        def toggleSpaceShip(self,game,toggleDirection): # toggleDirection == True -> next ship / False -> last ship
            if game.shipUnlockNumber == 0 and not settings.devMode: return
            else:
                if toggleDirection:
                    if game.savedShipLevel + 1  < len(assets.spaceShipList) and (settings.devMode or game.savedShipLevel + 1 <= game.shipUnlockNumber): game.savedShipLevel +=1
                    else: game.savedShipLevel = 0
                else:
                    if game.savedShipLevel - 1 < 0:
                        if settings.devMode: game.savedShipLevel = len(assets.spaceShipList) - 1
                        else:game.savedShipLevel = game.shipUnlockNumber
                    else: game.savedShipLevel -=1
                game.skinUnlockNumber = game.skinsUnlocked(game.savedShipLevel) # Get skin unlocks for new ship type
                self.updatePlayerConstants(game) # Update attributes


        # Update player attributes
        def updatePlayerConstants(self,game):
            self.image = assets.spaceShipList[game.savedShipLevel]['skins'][0]
            self.laserImage = assets.spaceShipList[game.savedShipLevel]['laser']
            self.currentImageNum = 0
            self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.speed,self.baseSpeed = assets.spaceShipList[game.savedShipLevel]['stats']["speed"],assets.spaceShipList[game.savedShipLevel]['stats']["speed"]
            self.fuel = assets.spaceShipList[game.savedShipLevel]['stats']["startingFuel"]
            self.maxFuel = assets.spaceShipList[game.savedShipLevel]['stats']["maxFuel"]
            self.fuelRegenNum = assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegen"]
            self.fuelRegenDelay = assets.spaceShipList[game.savedShipLevel]['stats']["fuelRegenDelay"]
            self.boostSpeed = assets.spaceShipList[game.savedShipLevel]['stats']["boostSpeed"]
            self.boostDrain = assets.spaceShipList[game.savedShipLevel]['stats']["boostDrain"]
            self.laserCost = assets.spaceShipList[game.savedShipLevel]['stats']["laserCost"]
            self.laserSpeed = assets.spaceShipList[game.savedShipLevel]['stats']["laserSpeed"]
            self.laserFireRate = assets.spaceShipList[game.savedShipLevel]['stats']["fireRate"]
            self.hasGuns = assets.spaceShipList[game.savedShipLevel]['stats']["hasGuns"]
            self.laserCollat = assets.spaceShipList[game.savedShipLevel]['stats']["collats"]
            self.hasShields = assets.spaceShipList[game.savedShipLevel]['stats']["hasShields"]
            self.shields = assets.spaceShipList[game.savedShipLevel]['stats']["startingShields"]
            self.shieldPieces = assets.spaceShipList[game.savedShipLevel]['stats']["startingShieldPieces"]
            self.shieldPiecesNeeded = assets.spaceShipList[game.savedShipLevel]['stats']["shieldPiecesNeeded"]
            self.damage = assets.spaceShipList[game.savedShipLevel]['stats']["laserDamage"]
            self.laserType = assets.spaceShipList[game.savedShipLevel]['stats']["laserType"]


        def updateExhaust(self,game):
            if self.exhaustState+1 > len(assets.spaceShipList[game.savedShipLevel]['exhaust']): self.exhaustState = 0
            else: self.exhaustState += 1


        def explode(self,game,obstacles):
            while self.explosionState < len(assets.explosionList):
                height = assets.explosionList[self.explosionState].get_height()
                width = assets.explosionList[self.explosionState].get_width()
                screen.fill(screenColor)
                screen.blit(assets.bgList[game.currentStage - 1][0], (0,0) )
                game.showBackgroundCloud()
                if game.cave is not None:
                    screen.blit(game.cave.background,game.cave.rect)
                    screen.blit(game.cave.image,game.cave.rect) # Draw cave

                # Draw obstacles during explosion
                for obs in obstacles:
                    obs.move(self)
                    obs.activate()
                    newBlit = rotateImage(obs.image,obs.rect,obs.angle)
                    screen.blit(newBlit[0],newBlit[1])

                img = pygame.transform.scale(assets.explosionList[self.explosionState], (height * self.explosionState, width * self.explosionState)) # Blow up explosion
                img, imgRect = rotateImage(img, self.rect, self.lastAngle) # Rotate

                screen.blit(img,imgRect) # Draw explosion
                screen.blit(assets.explosionList[self.explosionState],self.rect)
                displayUpdate()
                game.clk.tick(settings.fps)
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
        try: self.image = assets.obstacleImages[game.currentStage - 1][game.currentLevel-1]
        except: self.image = assets.meteorList[random.randint(0,len(assets.meteorList)-1)] # Not enough assets for this level yet
        self.image = pygame.transform.scale(self.image, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.getDirection(playerPos)
        self.validate()
        self.angle = 0 # Image rotation
        spins = [-1,1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.active = False
        self.activating = False
        self.activationDelay = 0
        self.slowerDiagonal = settings.slowerDiagonalObstacles


    # For levels with multiple obstacle types
    def getAttributes(self,attribute):
        if type(attribute) == list:
            if self.attributeIndex is None: self.attributeIndex = random.randint(0,len(attribute)-1)
            if self.attributeIndex > len(attribute): return attribute[random.randint(0,len(attribute)-1)]
            return attribute[self.attributeIndex] # Treat as parallel lists
        else: return attribute


    def getDirection(self,playerPos):
        if self.target == "NONE": self.direction = self.movement[1] # Get a string representation of the direction
        else: self.direction = math.atan2(playerPos[1] - self.rect.centery, playerPos[0] - self.rect.centerx) # Get angle representation


    def move(self,player):
        if self.target == "NONE": self.basicMove()
        elif self.target == "LOCK": self.targetMove()
        elif self.target == "HOME": self.homingMove(player)


    # BASIC MOVEMENT (8-direction) -> direction is a string
    def basicMove(self):
        if self.slowerDiagonal: # Use sqrt(2) for correct diagonal movement
            if self.direction  == "N": self.rect.centery -= self.speed
            elif self.direction == "S": self.rect.centery += self.speed
            elif self.direction == "E": self.rect.centerx += self.speed
            elif self.direction == "W": self.rect.centerx -= self.speed
            else:
                if "N" in self.direction: self.rect.centery -= self.speed / 1.414
                if "S" in self.direction: self.rect.centery += self.speed / 1.414
                if "E" in self.direction: self.rect.centerx += self.speed / 1.414
                if "W" in self.direction: self.rect.centerx -= self.speed / 1.414
        else:
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
        dirX = (player.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
        dirY = (player.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
        self.direction = math.atan2(dirY,dirX) # Angle to shortest path
        self.targetMove()


    # BOUNDARY HANDLING
    def bound(self,obstacles):
        if self.bounds == "KILL": # Remove obstacle
            if self.rect.left > settings.screenSize[0] + settings.spawnDistance or self.rect.right < -settings.spawnDistance:
                obstacles.remove(self)
                self.kill()
            elif  self.rect.top > settings.screenSize[1] + settings.spawnDistance or self.rect.bottom < 0 - settings.spawnDistance:
                obstacles.remove(self)
                self.kill()

        elif self.bounds == "BOUNCE": # Bounce off walls
            if self.rect.left < 0:
                if self.target == "NONE": self.direction = self.movementReverse(self.direction)
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.left = 1

            elif self.rect.right > settings.screenSize[0]:
                if self.target == "NONE": self.direction = self.movementReverse(self.direction)
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.right = settings.screenSize[0] - 1

            elif self.rect.top < 0:
                if self.target == "NONE": self.direction = self.movementReverse(self.direction)
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.top = 1

            elif self.rect.bottom > settings.screenSize[1]:
                if self.target == "NONE": self.direction = self.movementReverse(self.direction)
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.bottom = settings.screenSize[1]-1

        elif self.bounds == "WRAP": # Wrap around screen
            if self.rect.centery > settings.screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = settings.screenSize[1]
            if self.rect.centerx > settings.screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = settings.screenSize[0]


    # ACTIVATE OBSTACLE
    def activate(self):
        if not self.active:
            if self.rect.right > 0 and self.rect.left < settings.screenSize[0] and self.rect.bottom > 0 and self.rect.top < settings.screenSize[1]: self.activating = True
        if self.activating:
            if self.activationDelay >= settings.activationDelay: self.active = True
            else: self.activationDelay +=1


    # VALIDATE OBSTACLE POSTITION
    def validate(self):
        if type(self.direction) == str:
            if self.rect.right > settings.screenSize[0] or self.rect.left < 0:
                if self.direction == "N": self.rect.center = (random.randint(settings.screenSize[0]*0.02, settings.screenSize[0]*0.98) , settings.screenSize[1])
                elif self.direction == "S": self.rect.center= (random.randint(settings.screenSize[0]*0.02, settings.screenSize[0]*0.98) , 0)
            if self.rect.top < 0 or self.rect.bottom > settings.screenSize[1]:
                if self.direction == "W":self.rect.center = (settings.screenSize[0], random.randint(settings.screenSize[1]*0.02, settings.screenSize[1]*0.98))
                elif self.direction == "E":self.rect.center = (0, random.randint(settings.screenSize[1]*0.02, settings.screenSize[1]*0.98))


    # GET INVERSE MOVEMENT DIRECTION
    def movementReverse(self):
        if self.direction == "N": self.direction = "S"
        elif self.direction == "S": self.direction = "N"
        elif self.direction == "E": self.direction = "W"
        elif self.direction == "W": self.direction = "E"
        elif self.direction == "NW": self.direction = "SE"
        elif self.direction == "NE": self.direction = "SW"
        elif self.direction == "SE": self.direction = "NW"
        elif self.direction == "SW": self.direction = "NE"



# CAVES
class Cave(pygame.sprite.Sprite):
    def __init__(self,index):
        super().__init__()
        self.speed = settings.caveSpeed
        self.background = assets.caveList[index][0]
        self.image = assets.caveList[index][1]
        self.rect = self.image.get_rect(bottomleft = (0,settings.caveStartPos))
        self.mask = pygame.mask.from_surface(self.image)
        self.leave = False # Mark cave for exit


    def update(self):
        self.rect.centery += self.speed # Move
        if not self.leave and self.rect.top > settings.screenSize[1] * -1: self.rect.bottom = settings.screenSize[1]*2



# LASERS
class Laser(pygame.sprite.Sprite):
    def __init__(self,player,obstacles):
        super().__init__()
        self.laserType = player.laserType
        self.speed = player.laserSpeed
        self.angle = player.angle
        newBlit = rotateImage(player.laserImage,player.laserImage.get_rect(center = player.rect.center),self.angle)
        self.image = newBlit[0]
        self.rect = newBlit[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.target, self.seek, self.seekWaitTime, self.seekDelay = None, False, 0, settings.heatSeekDelay # For heat seeking lasers


    # MOVE LASERS
    def update(self,player,lasers,obstacles):
        # Remove offscreen lasers
        if self.rect.centerx > settings.screenSize[0] or self.rect.centery > settings.screenSize[1] or self.rect.centerx < 0 or self.rect.centery < 0: self.kill()
        elif self.laserType == "NORMAL": self.normalMove(player)
        elif self.laserType == "HOME": self.homingMove(player,lasers,obstacles)
        else: self.normalMove(player)


    # Simple movement
    def normalMove(self,player):
        # Laser angles correspond to player angles ( second is for vector based movement )
        if self.angle == 0: self.rect.centery -= self.speed + player.speed
        elif self.angle == 180 or self.angle == -180: self.rect.centery +=  self.speed + player.speed
        elif self.angle == 90 or self.angle == -270: self.rect.centerx -=  self.speed + player.speed
        elif self.angle == -90: self.rect.centerx +=  self.speed + player.speed

        elif self.angle == 45:
            speed = self.speed / 1.414 # sqrt(2)
            self.rect.centery -= speed + player.speed
            self.rect.centerx -= speed + player.speed
        elif self.angle == -45:
            speed = self.speed / 1.414 # sqrt(2)
            self.rect.centery -= speed + player.speed
            self.rect.centerx += speed + player.speed
        elif self.angle == 135 or self.angle == -225:
            speed = self.speed / 1.414 # sqrt(2)
            self.rect.centery += speed + player.speed
            self.rect.centerx -= speed + player.speed
        elif self.angle == -135:
            speed = self.speed / 1.414 # sqrt(2)
            self.rect.centery += speed + player.speed
            self.rect.centerx += speed + player.speed
        else:
            angle = math.radians( (self.angle-90))
            velX = self.speed * math.cos(angle)
            velY = self.speed * math.sin(angle)
            self.rect.centerx -= velX
            self.rect.centery += velY


    def homingMove(self,player,lasers,obstacles):
        if self.seekWaitTime < settings.heatSeekDelay:
            self.seekWaitTime += 1
            self.normalMove(player)
        elif self.seek == False: self.target, self.seek = self.getClosestPoint(obstacles), True # Get target
        else:
            if self.target is None or not obstacles.has(self.target):
                if settings.heatSeekNeedsTarget:
                    game.explosions.append(Explosion(self))
                    self.kill()
                else:
                    self.rect.centerx +=self.speed * math.cos(self.angle) # Horizontal movement
                    self.rect.centery +=self.speed * math.sin(self.angle) # Vertical movement

            else: # Homing
                dirX = (self.target.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
                dirY = (self.target.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
                self.angle = math.atan2(dirY,dirX) # Angle to shortest path
                self.rect.centerx += (player.speed + self.speed) * math.cos(self.angle) # Horizontal movement
                self.rect.centery +=self.speed * math.sin(self.angle) # Vertical movement


    # Get closest target out of a group
    def getClosestPoint(self, points):
        closest,shortest = None,None
        for pt in points:
            if closest is None or math.dist(self.rect.center,closest.rect.center) > math.dist(self.rect.center,pt.rect.center):
                closest,shortest = pt, math.dist(self.rect.center,pt.rect.center)
        return closest



# EXPLOSIONS
class Explosion:
    def __init__(self,laser):
        self.state,self.finalState,self.finished = 0,len(assets.explosionList)-1,False
        self.rect = laser.rect.copy()
        self.image = assets.explosionList[self.state]
        self.updateFrame = 0
        self.delay = settings.explosionDelay


    def update(self):
        self.updateFrame +=1
        if self.updateFrame >= self.delay:
            self.updateFrame = 0
            if self.state +1 >= len(assets.explosionList): self.finished = True
            else:
                self.state +=1
                self.image = assets.explosionList[self.state]

        screen.blit(self.image,self.rect)



# POWER UPS
class Point(pygame.sprite.Sprite):
    def __init__(self,player,lastPos):
        super().__init__()
        self.powerUp = ''
        pointChoices = settings.powerUpList[:]
        if not player or (not player.hasShields and player.boostDrain == 0 and player.laserCost == 0  and player.baseSpeed == player.boostSpeed): self.powerUp = "Default"
        else:
            powerUps = pointChoices
            if not player.hasShields and "Shield" in powerUps: pointChoices.remove("Shield")
            if not player.hasGuns and player.baseSpeed == player.boostSpeed and "Fuel" in powerUps: pointChoices.remove("Fuel")
            self.powerUp = random.choice(pointChoices)
        if self.powerUp == "Shield": self.image = assets.pointsList[2]
        elif self.powerUp == "Fuel": self.image = assets.pointsList[1]
        elif self.powerUp == "Default": self.image = assets.pointsList[0]
        self.image = pygame.transform.scale(self.image, (settings.pointSize, settings.pointSize))
        if lastPos == None: self.rect = self.image.get_rect(center = self.positionGenerator())
        else:self.rect = self.image.get_rect(center = self.spacedPositionGenerator(lastPos))
        self.mask = pygame.mask.from_surface(self.image)


    # POINT POSITION GENERATION
    def getPosition(self):
        xRange = [settings.screenSize[0] * settings.spawnRange[0] , settings.screenSize[0] * settings.spawnRange[1] ]
        yRange = [settings.screenSize[1] * settings.spawnRange[0] , settings.screenSize[1] * settings.spawnRange[1] ]
        xNum = random.randint(xRange[0],xRange[1])
        yNum = random.randint(yRange[0],yRange[1])
        return [xNum,yNum]


    # CHECK IF POINT IS IN SPAWN AREA
    def pointValid(self,point):
        centerX, centerY = settings.screenSize[0]/2, settings.screenSize[1]/2
        lines = [((centerX + math.cos(angle + math.pi/settings.spawnVertices)*spawnWidth/2, centerY + math.sin(angle + math.pi/settings.spawnVertices)*spawnHeight/2), (centerX + math.cos(angle - math.pi/settings.spawnVertices)*spawnWidth/2, centerY + math.sin(angle - math.pi/settings.spawnVertices)*spawnHeight/2)) for angle in (i * math.pi/4 for i in range(8))]
        sameSide = [((point[0]-l[0][0])*(l[1][1]-l[0][1]) - (point[1]-l[0][1])*(l[1][0]-l[0][0]))  * ((centerX-l[0][0])*(l[1][1]-l[0][1]) - (centerY-l[0][1])*(l[1][0]-l[0][0])) >= 0  for l in lines]
        return all(sameSide)


    # GET POSITION IN SPAWN AREA
    def positionGenerator(self):
        attempts = 0
        while True:
            point = self.getPosition()
            if attempts < settings.maxRandomAttempts and self.pointValid(point):return point
            else: attempts+=1


    # Get new position at valid distance from last position
    def spacedPositionGenerator(self,lastPos):
        attempts = 0
        while True:
            point = self.positionGenerator()
            if attempts < settings.maxRandomAttempts and math.dist(point,lastPos) >= settings.minDistanceToPoint: return point
            else: attempts+=1



# MENU METEOR ICONS
class Icon:
    def __init__(self):
        spins = [-1,1]
        self.speed = random.randint(1,settings.maxIconSpeed)
        self.movement = getMovement("AGGRO")
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        if random.randint(0,10) < 7: self.image = assets.menuList[1]
        else: self.image = assets.menuList[random.randint(5,len(assets.menuList)-1)]
        size = random.randint(settings.minIconSize,settings.maxIconSize)
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

        self.angle += self.spinDirection * random.uniform(0, settings.maxIconRotationSpeed)

        randomTimerUX = random.randint(settings.screenSize[0] * 2,settings.screenSize[0] * 4)
        randomTimerUY = random.randint(settings.screenSize[1] * 2,settings.screenSize[1] * 4)
        randomTimerLX = -1 * random.randint(settings.screenSize[0], settings.screenSize[0] * 3)
        randomTimerLY = -1 * random.randint(settings.screenSize[0], settings.screenSize[1] * 3)

        if self.active and ( (self.rect.centery > randomTimerUY) or (self.rect.centery < randomTimerLY) or (self.rect.centerx> randomTimerUX) or (self.rect.centerx < randomTimerLX) ):
            self.movement = getMovement("ALL")
            self.direction = self.movement[1]
            if random.randint(0,10) < 7: self.image = assets.menuList[1]
            else: self.image = assets.menuList[random.randint(5,len(assets.menuList)-1)]
            self.speed = random.randint(1,settings.maxIconSpeed)
            self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
            size = random.randint(settings.minIconSize,settings.maxIconSize)
            self.image = pygame.transform.scale(self.image, (size, size))
            self.active = False


    def activate(self):
        if not self.active:
            if ("W" in self.direction and self.rect.right >= 0) or ("E" in self.direction and self.rect.left <= settings.screenSize[0]) or ("N" in self.direction and self.rect.top <= settings.screenSize[1]) or ("S" in self.direction and self.rect.bottom >= 0): self.active = True


    def draw(self):
        if self.active:
            drawing, drawee = rotateImage(self.image,self.rect,self.angle)
            screen.blit(drawing,drawee)



# CREDITS SCREEN BACKGROUND SHIPS
class BackgroundShip:
    def __init__(self,text,scale):
        self.scale = scale
        self.size = self.valueScaler(scale,settings.minBackgroundShipSize,settings.maxBackgroundShipSize,assets.lowDon,assets.maxDon)
        if self.size < settings.minBackgroundShipSize:
            self.size = settings.minBackgroundShipSize
            self.speed = settings.maxBackgroundShipSpeed
        elif self.size > settings.maxBackgroundShipSize:
            self.size = settings.minBackgroundShipSize
            self.speed = settings.minBackgroundShipSpeed
        self.speed = settings.maxBackgroundShipSpeed/self.size
        if self.speed > settings.maxBackgroundShipSpeed: self.speed = settings.maxBackgroundShipSpeed
        elif self.speed < settings.minBackgroundShipSpeed: self.speed = settings.minBackgroundShipSpeed
        self.movement = getMovement("AGGRO")
        self.direction = self.movement[1]
        self.angle = self.getAngle()
        self.text = text
        self.image = pygame.transform.scale(assets.donationShips[random.randint(0, len(assets.donationShips) - 1)], (self.size, self.size) ).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.count = 0
        self.font = pygame.font.Font(assets.gameFont, int(self.size * 2/3))
        self.display = self.font.render(self.text, True, [0,0,0])
        self.displayRect = self.display.get_rect(center = self.rect.center)
        self.active = False


    def move(self):
        if self.count >= settings.backgroundShipDelay:
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
        if settings.showSupporterNames and not settings.showBackgroundShips:
            if self.displayRect.bottom < 0 or self.displayRect.top > settings.screenSize[1] or self.displayRect.left > settings.screenSize[0] or self.displayRect.right < 0: return True
        else:
            if self.rect.bottom < 0 or self.rect.top > settings.screenSize[1] or self.rect.left > settings.screenSize[0] or self.rect.right < 0: return True


    def activate(self):
        if not self.active and not self.offScreen(): self.active = True


    # GET ANGLE FOR CORRESPONDING DIRECTION
    def getAngle(self):
        if self.direction == "N": return 0
        elif self.direction == "S": return 180
        elif self.direction == "E": return -90
        elif self.direction == "W": return 90
        elif self.direction == "NW": return 45
        elif self.direction == "NE": return -45
        elif self.direction == "SE": return -135
        elif self.direction == "SW": return 135


    # GET SCALED VALUE
    def valueScaler(self, amount, minimum, maximum, bottom, top):
        if bottom is None or top is None: return minimum
        elif top - bottom == 0: return (maximum + minimum) / 2
        else:
            scaled = (amount - bottom) / (top - bottom) * (maximum - minimum) + minimum
            return int(min(max(scaled, minimum), maximum))



# INITIALIZE GAME
game = Game(assets.loadRecords()) # Initialize game with records loaded
menu = Menu() # Initialize menus


# START GAME LOOP
def gameLoop():
    pygame.mixer.music.play()
    game.resetGameConstants() # Reset level settings
    game.pauseCount = 0 # Reset pause uses
    game.gameClock = 0 # Restart game clock
    player = Player(game) # Initialize player
    if game.mainMenu: menu.home(game,player)
    else:
        for i in range(game.savedSkin): player.nextSkin()

    events = Event() # Initialize events
    events.set(player) # Events manipulate player cooldowns
    lasers = pygame.sprite.Group() # Laser group
    obstacles = pygame.sprite.Group() # Obstacle group
    running = True

    # GAME LOOP
    while running: game.update(player,obstacles,menu,events,lasers)


if __name__ == '__main__': gameLoop()