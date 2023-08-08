# Navigator
# Copyright (c) 2023 Mike Pistolesi
# All rights reserved

import os,sys,random,math,platform,json,base64,time,asyncio
from cryptography.fernet import Fernet
from dotenv import load_dotenv
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.display.init()
pygame.font.init()
pygame.mixer.init()

version = "v0.5.0"

# STARTUP SCREEN
pygame.display.set_caption('Navigator')


# GAME SETTINGS
class Settings:
    def __init__(self):

        # SCREEN
        self.screenSize = [800,800] # Default = [800,800]
        self.fps = 60 # Default = 60
        self.fullScreen = False # Default = False / start game in fullscreen
        self.showFPS = False # Default = False / shows fps counter in window caption

        # INPUT
        self.useController = True # Default = True / Allow controller input
        self.cursorMode = True # Default = True / Allow cursor input
        self.cursorFollowDistance = 15 # Default = 15 / Cursor follow deadzone
        self.cursorRotateDistance = 5 # Default = 5 / Cursor rotate deadzone
        self.cursorThickness = 2 # Default = 2

        # HUD
        self.showHUD = True
        self.shieldColor = [0,0,255] # Default = [0,0,255] / Color of shield gauge / Blue
        self.fullShieldColor = [0,255,255] # Default = [0,255,255] / Color of active shield gauge / Cyan
        self.fuelColor = [255,0,0] # Default = [255,0,0] / Color of fuel gauge /  Red
        self.timerDelay = 1000 # Default = 1000
        self.pauseMax = 5 # Default = 5 / max pauses per game
        self.nearMissIndicatorDuration = 1500 # Default = 1500 / visual duration of near miss indicator

        # POWER UPS
        self.spawnRange = [0.15, 0.85]
        self.spawnVertices = 8 # Default = 8 / Vertices in shape of point spawn area (Octagon)
        self.pointSize = 25  # Default = 25
        self.shieldChunkSize = self.screenSize[0]/40 # Default = screen width / 40
        self.nukeSize = 75 # Default = 75 / Nuke expansion rate
        self.boostCooldownTime = 2000 # Default = 2000 / Activates when fuel runs out to allow regen
        self.powerUpList = {"Default":55,"Shield":20, "Fuel":15, "Coin":5, "Nuke":5} # Default = {"Default":55,"Shield":20, "Fuel":15, "Coin":5, "Nuke":5} / power up odds
        self.playerShieldSize = 48 # Default = 48 / Shield visual size
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
        self.maxFgIcons = 1 # Default = 1 / foreground icons
        self.maxBgIcons = 5 # Default = 5 / background icons
        self.maxCgIcons = 1 # Default = 1 / colliding icons
        self.minIconSpeed = 6 # Default = 6
        self.maxIconSpeed = 12 # Default = 12
        self.minIconRotationSpeed = 3 # Default = 3
        self.maxIconRotationSpeed = 6 # Default = 6
        self.minIconSize = 30 # Default = 30
        self.maxIconSize = 100  # Default = 100
        self.showVersion = True # show version info
        self.showMenuIcons = True # show menu icons

        # STAGE UP
        self.stageUpCloudStartPos = -900 # Default = -900
        self.stageUpCloudSpeed = 8  # Default = 8

        # CREDITS
        self.mainCreditsSpeed = 2 # Default = 2
        self.extraCreditsSize = 30  # Default = 30 / background ships text size
        self.maxExtras = 3 # Default = 3 / # max background ships
        self.minBackgroundShipSpeed = 2 # Default = 2
        self.maxBackgroundShipSpeed = 3 # Default = 3
        self.minBackgroundShipSize = 50 # Default = 50
        self.maxBackgroundShipSize = 100 # Default = 100
        self.minBackgroundShipSpawnDelay = 500 # / Min delay (ms) before a ship spawns
        self.maxBackgroundShipSpawnDelay = 3000 # / Max delay (ms) before a ship spawns
        self.showBackgroundShips = True # Default = True
        self.showSupporterNames = True # Default = True

        # SOUNDS
        self.musicVolume = 10 # Default = 10 / Music volume / 100
        self.sfxVolume = 5 # Default = 5 / SFX volume / 100
        self.numChannels = 16 # Default = 16
        self.musicMuted = False # Default = False

        # PLAYER
        self.resetPlayerOrientation = True # Default = True / reset orientation if player is not moving
        self.drawExhaust = True # Default = True / draw exhaust animation
        self.exhaustUpdateDelay = 50 # Default = 50 / Delay (ms) between exhaust animation frames
        self.defaultToHighSkin = True # Default = True / Default to highest skin unlocked on game launch
        self.defaultToHighShip = False # Default = False / Default to highest ship unlocked on game launch
        self.heatSeekDelay = 15 # Default = 15 / time before projectile starts homing
        self.heatSeekNeedsTarget = False # Default = False / projectile will explode if target not found
        self.skinAnimationDelay = 5 # Default = 5 / Delay between skin animation frame updates

        # LEVELS
        self.levelUpCloudSpeed = 25 # Default = 25 / Only affects levels preceded by wipe

        # PLANETS
        self.planetMoveDelay = 2 # Default = 2
        self.unlimitedPlanets = True # Temporary until more planets added

        # OBSTACLES
        self.slowerDiagonalObstacles = True # Default = True / use the hypotenuse or whatever
        self.spawnDistance = 0 # Default = 0 / Distance past screen border required before new obstacle spawned
        self.obsLaserDelay = 10 # Default = 10 / delay before obstacle fires another laser
        self.obsLaserDamage = 1 # Default = 1
        self.maxObsLasers = 3 # Default = 3 / lasers per obstacle

        # EXPLOSIONS
        self.explosionIncrement = 0 # Default = 0 / explosion expansion rate
        self.explosionDelay = 2 # Default = 2 / delay between explosion frame updates

        # NEAR MISSES
        self.nearMisses = True # Default = True / register near misses
        self.nearMissDist = 40 # Default = 40 / distance for near miss start
        self.nearMissSafeDist = 60 # Default = 60 distance for near miss end
        self.nearMissValue = 0 # Default = 0 / point value for near misses

        # CAVES
        self.caveStartPos = self.screenSize[1]*-2 # Default = -1600 / Cave start Y coordinate
        self.caveSpeed = 20 # Default = 20 / Cave flyby speed

        # SAVING
        self.encryptGameRecords = True # Default = True / Hide game records from user to prevent manual unlocks
        self.invalidKeyMessage = "Invalid key, could not save records." # Saved to game records file if settings.encryptGameRecords == True and key is invalid

        # LEADERBOARD
        self.connectToLeaderboard = True # Default = True
        self.leaderboardSize = 10 # Number of players shown on leaderboard

        # EXPERIMENTAL
        self.rawCursorMode = False # Default = False / sets player position to cursor position
        self.performanceMode = False # Default = False
        self.qualityMode = False # Default = False # Overridden by performance mode

        # DISCORD
        self.showPresence = True # Default = True / Discord presence using pypresence

        # TESTING
        self.useArgs = True # Default = False / accept command line args
        self.devMode = False # Default = False
        self.showSpawnArea = False # Default = False / show powerup spawn area
        self.showCursorPath = False # Default = False / Draw line from cursor to ship
        self.debugging = False # Default = False / show status messages

        # ARGS
        if self.useArgs:
            self.arguments = sys.argv[1:]
            for arg in self.arguments: arg = arg.lower()
        else: self.arguments = None

        # APPLY ARGS
        if self.arguments is not None:
            if "debug" in self.arguments: self.debugging = True
            if "devmode" in self.arguments: self.devMode = True

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
        self.runningFromExe = hasattr(sys,'_MEIPASS') # Specify if running from EXE/app or Python script
        if self.runningFromExe: self.debug("Running from executable") # Debug
        else: self.debug("Running from Python script") # Debug
        self.debug("Loaded settings") # Debug


    # DEBUGGING MESSAGES
    def debug(self,text):
        if self.debugging:print(text)



# ASSETS
class Assets:
    def __init__(self):
        # RECORD AND PREFERENCE PATHS
        if platform.system().lower() == 'windows' or platform.system().lower() == 'linux': self.recordsPath,self.preferencesPath = './gameRecords.txt','./gamePreferences.txt'  # For windows and linux
        else: self.recordsPath,self.preferencesPath = self.resources('gameRecords.txt'), self.resources('gamePreferences.txt') # For MacOS

        # ASSET PATHS
        assetDirectory = self.resources('Assets') # ASSET DIRECTORY
        load_dotenv(os.path.join(assetDirectory,'.env')) # LOAD ENV VARS
        obstacleDirectory = os.path.join(assetDirectory, 'Obstacles') # Obstacle asset directory
        meteorDirectory = os.path.join(obstacleDirectory, 'Meteors') # Meteor asset directory
        ufoDirectory = os.path.join(obstacleDirectory, 'UFOs') # UFO asset directory
        shipDirectory = os.path.join(assetDirectory, 'Spaceships') # Spaceship asset directory
        caveDirectory = os.path.join(assetDirectory,'Caves') # Cave asset directory
        planetDirectory = os.path.join(assetDirectory,'Planets') # Planet asset directory
        backgroundDirectory = os.path.join(assetDirectory, 'Backgrounds') # Background asset directory
        menuDirectory = os.path.join(assetDirectory, 'MainMenu') # Start menu asset directory
        explosionDirectory = os.path.join(assetDirectory, 'Explosion') # Explosion animation directory
        pointsDirectory = os.path.join(assetDirectory, 'Points') # Point image directory
        supportersDirectory = os.path.join(assetDirectory,'Supporters') # Supporters directory
        self.windowIcon = pygame.image.load(self.resources(os.path.join(assetDirectory,'Icon.png'))).convert_alpha()
        self.stageCloudImg = pygame.image.load(self.resources(os.path.join(assetDirectory,'StageCloud.png') ) ).convert_alpha() # STAGE WIPE CLOUD
        self.soundDirectory = os.path.join(assetDirectory, 'Sounds') # Sound assets directory / will be referenced again for music loading

        pygame.display.set_icon(self.windowIcon)

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

        settings.debug("Loaded levels") # Debug

        # OBSTACLE ASSETS
        meteorList = []
        for filename in sorted(os.listdir(meteorDirectory)):
            if filename.endswith('.png'):
                path = os.path.join(meteorDirectory, filename)
                meteorList.append(pygame.image.load(self.resources(path)).convert_alpha())
            else:
                meteorFolder = os.path.join(meteorDirectory,filename)
                if os.path.isdir(meteorFolder):
                    meteorsList = []
                    for meteorFilename in sorted(os.listdir(meteorFolder)):
                        if meteorFilename.endswith('.png'):
                            path = os.path.join(meteorFolder,meteorFilename)
                            meteorsList.append(pygame.image.load(self.resources(path)).convert_alpha())
                    if len(meteorsList) > 0: meteorList.append(meteorsList)

        # UFO ASSETS
        ufoList = []
        for filename in sorted(os.listdir(ufoDirectory)):
            if filename.endswith('.png'):
                path = os.path.join(ufoDirectory, filename)
                ufoList.append(pygame.image.load(self.resources(path)).convert_alpha())

        self.obstacleImages = [meteorList,ufoList] # Seperated by stage
        enemyLaserPath = os.path.join(assetDirectory,'enemyLaser.png')
        self.enemyLaserImage = pygame.image.load(self.resources(enemyLaserPath)).convert_alpha()
        settings.debug("Loaded obstacles") # Debug

        # CAVE ASSETS
        self.caveList = []
        for caveNum in sorted(os.listdir(caveDirectory)):
            caveAssets = os.path.join(caveDirectory,caveNum)
            cave = []
            cave.append(pygame.image.load(self.resources(os.path.join(caveAssets,"Background.png"))).convert_alpha())
            cave.append(pygame.image.load(self.resources(os.path.join(caveAssets,"Cave.png"))).convert_alpha())
            self.caveList.append(cave)
        settings.debug("Loaded caves") # Debug

        # PLANET ASSETS
        self.planets = []
        self.planetSizes = [400] # Planet sizes for corresponding index
        planetIndex = 0
        for filename in sorted(os.listdir(planetDirectory)):
            if filename.endswith('.png'):
                path = os.path.join(planetDirectory, filename)
                self.planets.append(pygame.transform.scale(pygame.image.load(self.resources(path)).convert_alpha(), (self.planetSizes[planetIndex],self.planetSizes[planetIndex])))
                planetIndex += 1
        settings.debug("Loaded planets") # Debug

        # SELECT CURSOR
        self.selectIcon = pygame.transform.scale(pygame.image.load(self.resources(os.path.join(assetDirectory,"Select.png"))), (100,100)).convert_alpha()

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
        settings.debug("Loaded backgrounds") # Debug

        # EXPLOSION ASSETS
        self.explosionList = []
        for filename in sorted(os.listdir(explosionDirectory)):
            if filename.endswith('.png'):
                path = os.path.join(explosionDirectory, filename)
                self.explosionList.append(pygame.image.load(self.resources(path)).convert_alpha())
        settings.debug("Loaded explosions") # Debug

        # POINTS ASSETS
        self.pointsList = {}
        for filename in sorted(os.listdir(pointsDirectory)):
            if filename.endswith('png'):
                path = os.path.join(pointsDirectory, filename)
                self.pointsList[filename[:-4]] = pygame.image.load(self.resources(path)).convert_alpha()
        settings.debug("Loaded points") # Debug

        # For coin counter
        self.coinIcon = pygame.transform.scale(self.pointsList["Coin"],(25,25))

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

                    # ANIMATED SKINS
                    else:
                        skinAssetPath = os.path.join(skinsPath,imageAsset)
                        if os.path.isdir(skinAssetPath):
                            animatedSkin = []
                            for skinPath in os.listdir(skinAssetPath):
                                if skinPath.endswith('.png'):
                                    imageAssetPath = os.path.join(skinAssetPath,skinPath)
                                    animatedSkin.append(pygame.image.load(self.resources((imageAssetPath))).convert_alpha())
                            if len(animatedSkin) > 0: shipLevelDict['skins'].append(animatedSkin)

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

        settings.debug("Loaded ships") # Debug

        # PLAYER SHIELD ASSET
        self.playerShield = pygame.transform.scale(pygame.image.load(self.resources(os.path.join(assetDirectory,"Shield.png"))),(settings.playerShieldSize,settings.playerShieldSize))

        # MAIN MENU ASSETS
        self.titleText = pygame.image.load(self.resources(os.path.join(menuDirectory,'Title.png'))).convert_alpha()
        self.menuList = []
        menuMeteorDir = os.path.join(menuDirectory,'FlyingObjects')
        for objPath in sorted(os.listdir(menuMeteorDir)): self.menuList.append(pygame.image.load(self.resources(os.path.join(menuMeteorDir,objPath))).convert_alpha())

        settings.debug("Loaded menu assets") # Debug

        # LOAD SOUNDTRACK
        self.loadMenuMusic()

        # EXPLOSION NOISE ASSET
        self.explosionNoise = pygame.mixer.Sound(self.resources(os.path.join(self.soundDirectory,"Explosion.wav")))
        self.explosionNoise.set_volume(settings.sfxVolume/100)

        # POINT NOISE ASSET
        self.pointNoise = pygame.mixer.Sound(self.resources(os.path.join(self.soundDirectory,"Point.wav")))
        self.pointNoise.set_volume(settings.sfxVolume/100 *1.25)

        # POWERUP NOISE ASSET
        self.powerUpNoise = pygame.mixer.Sound(self.resources(os.path.join(self.soundDirectory,"PowerUp.wav")))
        self.powerUpNoise.set_volume(settings.sfxVolume/100)

        # COIN NOISE ASSET
        self.coinNoise = pygame.mixer.Sound(self.resources(os.path.join(self.soundDirectory,"Coin.wav")))
        self.coinNoise.set_volume(settings.sfxVolume/100)

        # LASER NOISE ASSET
        self.laserNoise = pygame.mixer.Sound(self.resources(os.path.join(self.soundDirectory,"Laser.wav")))
        self.laserNoise.set_volume(settings.sfxVolume/100)

        # LASER IMPACT NOISE ASSET
        self.impactNoise = pygame.mixer.Sound(self.resources(os.path.join(self.soundDirectory,"Impact.wav")))
        self.impactNoise.set_volume(settings.sfxVolume/100)

        settings.debug("Loaded sounds") # Debug

        # LOAD DONATION RECORDS
        self.donations = {}
        try:
            path = os.path.join(supportersDirectory,'Supporters.txt')
            with open(path,'r') as file:
                for line in file:
                    try:
                        key,value = line.strip().split(':')
                        self.donations[key] = int(value)
                    except:settings.debug("Could not load supporter")
        except: settings.debug("Could not load supporters list")

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
        self.shipStatsFont = pygame.font.Font(self.gameFont,10)
        self.labelFont = pygame.font.Font(self.gameFont, 20)
        self.versionFont = pygame.font.Font(self.gameFont,25)
        self.mediumFont = pygame.font.Font(self.gameFont, 30) # Medium font
        self.pauseCountFont = pygame.font.Font(self.gameFont,40)
        self.creatorFont = pygame.font.Font(self.gameFont, 55)
        self.leaderboardTitleFont = pygame.font.Font(self.gameFont, 60)
        self.stageUpFont = pygame.font.Font(self.gameFont, 90)
        self.largeFont = pygame.font.Font(self.gameFont, 100) # Large font
        settings.debug("Loaded fonts") # Debug

        self.userName = os.getlogin() # Leaderboard username
        self.leaderboard = self.getLeaders()


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
                settings.debug("Stored game records")
            except: settings.debug("Continuing without saving records")
        # With encryption
        else:
            if self.getKey() is None:
                with open(self.recordsPath,'w') as file: file.write(settings.invalidKeyMessage)
                settings.debug("Invalid key, continuing without saving")
                return # No key, continue without saving
            else:
                try:
                    encrypted = Fernet(self.getKey()).encrypt(json.dumps(records).encode())
                    with open(self.recordsPath,'wb') as file: file.write(encrypted)
                    settings.debug("Stored encrypted game records")
                except: settings.debug("Failed to save encrypted records")


    # LOAD GAME RECORDS
    def loadRecords(self):
        # No encryption
        if not settings.encryptGameRecords:
            try:
                with open(self.recordsPath,'r') as file: records = json.load(file)
                settings.debug("Loaded game records")
                return records
            except:
                settings.debug("Could not load records, attempting overwrite")
                defaultRecords = self.getDefaultRecords()
                self.storeRecords(defaultRecords)
                return defaultRecords
        # With encryption
        else:
            try:
                # Return dictionary from encrypted records file
                with open(self.recordsPath,'rb') as file: encrypted = file.read()
                settings.debug("Loaded encrypted game records")
                return json.loads(Fernet(self.getKey()).decrypt(encrypted))
            except:
                # Failed to load records
                settings.debug("Could not load encrypted records, attempting overwrite")
                defaultRecords = self.getDefaultRecords()
                self.storeRecords(defaultRecords) # Try creating new encrypted records file
                return defaultRecords


    def loadGameOverMusic(self):
        pygame.mixer.music.load(self.resources(os.path.join(self.soundDirectory,"GameOver.mp3")))
        pygame.mixer.music.set_volume(settings.musicVolume/100 *1.5)


    def loadMenuMusic(self):
        pygame.mixer.music.load(self.resources(os.path.join(self.soundDirectory,"Menu.mp3")))
        pygame.mixer.music.set_volume(settings.musicVolume/100)


    def loadSoundtrack(self):
        pygame.mixer.music.load(self.resources(os.path.join(self.soundDirectory,"Soundtrack.mp3")))
        pygame.mixer.music.queue(self.resources(os.path.join(self.soundDirectory,"GameLoop.mp3")),'mp3',-1)
        pygame.mixer.music.set_volume(settings.musicVolume/100 *1.5)


    # RETURN NEW RECORDS DICTIONARY
    def getDefaultRecords(self): return {'highScore':0, 'longestRun':0, 'attempts':0, 'timePlayed':0, 'points':0, 'coins':0, 'unlocks':self.getDefaultUnlocks(), 'id':self.getNewID()}


    # RETRUN NEW UNLOCKS LIST
    def getDefaultUnlocks(self):
        ships = []
        for ship in self.spaceShipList:
            skins = []
            for skin in ship['skins']: skins.append(False)
            ships.append(skins)
        ships[0][0] = True # default ship starts unlocked
        return ships


    # CONNECT TO LEADERBOARD CLIENT
    def getLeaderboardClient(self):
        if settings.connectToLeaderboard:
            # LOAD MODULES
            try:
                settings.debug("Loading leaderboard drivers") # Debug
                from pymongo.mongo_client import MongoClient
                import dns,certifi
            except:
                settings.debug("Failed to initialize leaderboard. Make sure pymongo, dnspython, and certifi are installed") # Debug
                settings.connectToLeaderboard = False
                return None

            # START CONNECTION
            try:
                database = MongoClient((Fernet(base64.b64decode(os.getenv('DBKEY'))).decrypt(os.getenv('DBTOKEN'))).decode(), connectTimeoutMS=3000, socketTimeoutMS=3000, tlsCAFile=certifi.where())
                settings.debug("Connected to leaderboard database")
                return database
            except:
                settings.debug("Could not connect to leaderboard database. Scores will not be uploaded") # Debug
                settings.connectToLeaderboard = False
                return None
        else: return None


    # GET LEADERBOARD FROM DATABASE
    def getLeaders(self):
        if settings.connectToLeaderboard:
            try:
                database = self.getLeaderboardClient()
                collection = database["navigator"]["leaderboard"]
                leaders = list(collection.find().sort('longestRun', -1).limit(settings.leaderboardSize))
                settings.debug("Refreshed leaderboard") # Debug
                database.close()
                settings.debug("Disconnected from leaderboard client") # Debug
                leaderBoard = []
                for leaderIndex in range(len(leaders)):
                    leader = leaders[leaderIndex]
                    leaderBoard.append( {'id': leader['_id'], 'name':leader['name'], 'time':leader['longestRun'], 'score':leader['highScore']} )
                return leaderBoard
            except:
                settings.debug("Could not get leaderboard") # Debug
                settings.connectToLeaderboard = False
                return None
        else: return None


    # UPLOAD RECORDS TO LEADERBOARD
    def uploadRecords(self,records):
        if settings.connectToLeaderboard:
            database = self.getLeaderboardClient()

            # UPLOAD RECORDS
            try:
                collection = database["navigator"]["leaderboard"]
                uploadData = {'_id':records['id'], 'name':self.userName, 'highScore': records['highScore'], 'longestRun':records['longestRun']} # Data for upload

                # Check if already exists in leaderboard
                settings.debug("Checking for previous records on leaderboard") # Debug
                data = collection.find_one({'_id':records['id']}) # Previous record
                repeat = collection.find_one({'name':self.userName}) # Repeat usernames

                repeatFound = False
                if repeat is not None:
                    if (data is None) or ( (data is not None) and (repeat != data or repeat['_id'] != data['_id']) ) :
                        if records['longestRun'] < repeat['longestRun']: repeatFound = True

                if not repeatFound and data is not None:
                    settings.debug("Records found") # Debug
                    longestRun = data.get('longestRun')
                    highScore = data.get('highScore')

                    if (uploadData['highScore'] > highScore or uploadData['longestRun'] > longestRun) and (uploadData['longestRun'] > 0):
                        uploadData['highScore'] = max(highScore,uploadData['highScore'])
                        uploadData['longestRun'] = max(longestRun,uploadData['longestRun'])
                        settings.debug("Updating leaderboard records") # Debug
                        collection.update_one({'_id': records['id']}, {'$set': uploadData}, upsert=True)
                        settings.debug("Successfully updated scores in database") # Debug
                    else: settings.debug("Skipped leaderboard update, scores unchanged") # Debug

                else: # Insert new data
                    if repeatFound: settings.debug("Repeat username found on leaderboard")
                    else:
                        settings.debug("Adding record to leaderboard") # Debug
                        collection.insert_one(uploadData)
                        settings.debug("Successfully inserted high score in database") # Debug

                database.close()
                settings.debug("Disconnected from leaderboard database") # Debug

            except:
                settings.debug("Failed to upload records to database") # Debug
                settings.connectToLeaderboard = False
                return


    # GET RECORDS ID
    def getNewID(self):
        settings.debug("Generating new ID") # Debug
        return Fernet.generate_key().decode('utf-8')



# UNLOCKS
class Unlocks:
    def __init__(self,records):
        self.ships = records
        self.messages = [] # [[Unlock Message,Variant Name], Ship Name  ]
        settings.debug("Loaded unlocks") # Debug


    # UPDATE UNLOCKS IN MENU
    def update(self,game):
        preUpdate = self.ships[:] # copy previous list to check for update

        # Default ship - L1
        if not self.ships[0][1] and game.records["longestRun"] >= 15: self.ships[0][1] = True
        if not self.ships[0][2] and game.records["longestRun"] >= 30: self.ships[0][2] = True
        if not self.ships[0][3] and game.records["longestRun"] >= 45: self.ships[0][3] = True
        if not self.ships[0][4] and game.records["longestRun"] >= 60: self.ships[0][4] = True
        if not self.ships[0][5] and game.records["longestRun"] >= 75: self.ships[0][5] = True
        if not self.ships[0][6] and game.records["longestRun"] >= 90: self.ships[0][6] = True
        if not self.ships[0][7] and game.records["longestRun"] >= 105:self.ships[0][7] = True
        if not self.ships[0][8] and game.records["longestRun"] >= 120:self.ships[0][8] = True
        if not self.ships[0][9] and game.records["longestRun"] >= 135:self.ships[0][9] = True
        if not self.ships[0][10] and game.records["longestRun"] >= 150:self.ships[0][10] = True
        if not self.ships[0][11] and game.records["longestRun"] >= 165:self.ships[0][11] = True
        levelMessages = [
                            [None,None],
                            ["Survive for 15 seconds",None],
                            ["Survive for 30 seconds",None],
                            ["Survive for 45 seconds",None],
                            ["Survive for 60 seconds",None],
                            ["Survive for 75 seconds",None],
                            ["Survive for 90 seconds",None],
                            ["Survive for 105 seconds","Taxigator"],
                            ["Survive for 120 seconds","WhatColorsYourSpaceship"],
                            ["Survive for 135 seconds",None],
                            ["Survive for 150 seconds",None],
                            ["Survive for 165 seconds",None] ]

        # Record holder unlocks
        if assets.leaderboard is not None and assets.leaderboard[0]['id'] == game.records['id']:
            settings.debug("User is record holder") # Debug
            if not self.ships[0][12]: self.ships[0][12] = True
        else:
        # Re locks
            if self.ships[0][12]: self.ships[0][12] = False

        levelMessages.append(["Be #1 on Leaderboard","Champion"])
        self.messages.append([levelMessages, "Classic Ship"])

        # Rocket buggy - L2
        if not self.ships[1][0] and game.records["highScore"] >= 25: self.ships[1][0] = True
        self.messages.append([[["Score 25 in a run", None]], "Rocket Buggy"])

        # Laser ship - L3
        if not self.ships[2][0] and game.records["highScore"] >= 50: self.ships[2][0] = True
        self.messages.append([[["Score 50 in a run", None]], "Lasership"])

        # Hyper yacht - L4
        if not self.ships[3][0] and game.records["points"] >= 200: self.ships[3][0] = True
        self.messages.append([[["Score 200 points total", None]], "Hyper Yacht"])

        # Ol reliable - L5
        if not self.ships[4][0] and game.records["timePlayed"] >= 1200: self.ships[4][0] = True
        self.messages.append([[["Play for 1200 seconds", None]], "Ol' Reliable"])

        # Icon ship - L6
        if not self.ships[5][0] and game.records["points"] >= 500: self.ships[5][0] = True
        if not self.ships[5][1] and game.records["points"] >= 600: self.ships[5][1] = True
        if not self.ships[5][2] and game.records["points"] >= 700: self.ships[5][2] = True
        if not self.ships[5][3] and game.records["points"] >= 800: self.ships[5][3] = True
        if not self.ships[5][4] and game.records["points"] >= 900:  self.ships[5][4] = True
        levelMessages = [
            ["Score 500 points total",None],
            ["Score 600 points total",None],
            ["Score 700 points total",None],
            ["Score 800 points total",None],
            ["Score 900 points total",None] ]
        self.messages.append([levelMessages, "Classic 2.0"])

        if preUpdate != self.ships: # Save unlocks if list was updated
            game.records["unlocks"] = self.ships
            assets.storeRecords(game.records)


    # Skin other than default for a specific ship is unlocked
    def hasSkinUnlock(self, shipIndex):
        if len(self.ships[shipIndex]) <= 1: return False
        else:
            for skin in self.ships[shipIndex][1:]:
                if skin: return True
            return False


    # Ship other than default is unlocked
    def hasShipUnlock(self):
        for ship in self.ships[1:]:
            if ship[0]: return True
        return False


    # Index of highest ship unlock
    def highestShip(self):
        highest = 0
        for shipIndex in range(len(self.ships)):
            if self.ships[shipIndex][0]: highest = shipIndex
        return highest


    # Index of highest skin unlock
    def highestSkin(self,shipNum):
        highest = 0
        for skinIndex in range(len(self.ships[shipNum])):
            if self.ships[shipNum][skinIndex]: highest = skinIndex
        return highest


    # Index of next unlocked skin
    def nextUnlockedSkin(self,shipNum,skinNum):
        if self.hasSkinUnlock(shipNum):
            for skinIndex in range(len(self.ships[shipNum])):
                if skinIndex > skinNum and self.ships[shipNum][skinIndex]: return skinIndex
        return None


    # Index of last unlocked skin
    def lastUnlockedSkin(self,shipNum,skinNum):
        if self.hasSkinUnlock(shipNum):
            for skinIndex in reversed(range(len(self.ships[shipNum]))):
                if skinIndex < skinNum and self.ships[shipNum][skinIndex]: return skinIndex
        return None


    # Index of next unlocked ship
    def nextUnlockedShip(self,shipNum):
        if self.hasShipUnlock():
            for shipIndex in range(len(self.ships)):
                if shipIndex > shipNum and self.ships[shipIndex][0]: return shipIndex
        return None


    # Index of last unlocked ship
    def lastUnlockedShip(self,shipNum):
        if self.hasShipUnlock():
            for shipIndex in reversed(range(len(self.ships))):
                if shipIndex < shipNum and self.ships[shipIndex][0]: return shipIndex
        return None



# GET SCREEN
def getScreen():
    if settings.performanceMode:
        if settings.fullScreen: return pygame.display.set_mode(settings.screenSize, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED , depth = 16)
        else: return pygame.display.set_mode(settings.screenSize,pygame.DOUBLEBUF,depth=16)
    elif settings.qualityMode:
        if settings.fullScreen: return pygame.display.set_mode(settings.screenSize, pygame.FULLSCREEN | pygame.SRCALPHA,depth = 32)
        else: return pygame.display.set_mode(settings.screenSize, pygame.NOFRAME | pygame.SRCALPHA,depth = 32)
    # Default
    else:
        if settings.fullScreen: return pygame.display.set_mode(settings.screenSize,pygame.FULLSCREEN | pygame.SCALED, depth = 0)
        else: return pygame.display.set_mode(settings.screenSize, pygame.SCALED, depth = 0)


# TOGGLE FULLSCREEN
def toggleScreen():
    if settings.qualityMode and not settings.performanceMode:
        global screen
        pygame.display.quit()
        settings.fullScreen = not settings.fullScreen
        pygame.display.set_caption('Navigator')
        pygame.display.set_icon(assets.windowIcon)
        screen = getScreen()
    else:
        pygame.display.toggle_fullscreen()
        settings.fullScreen = not settings.fullScreen
        if settings.fullScreen: settings.debug("Fullscreen toggled on")
        else: settings.debug("Fullscreen toggled off")


# TOGGLE MUSIC MUTE
def toggleMusic(game):
    game.musicMuted = not game.musicMuted
    if pygame.mixer.music.get_volume() == 0: pygame.mixer.music.set_volume(settings.musicVolume/100)
    else: pygame.mixer.music.set_volume(0)


settings = Settings() # INITIALIZE SETTINGS
screen = getScreen() # INITIALIZE SCREEN
loadingDisplay = pygame.font.SysFont("None", 30).render("Loading...", True, (0, 255, 0))
screen.blit(loadingDisplay, loadingDisplay.get_rect(midleft=(370, 400)))
pygame.display.update()
settings.debug("Initialized screen") # Debug
pygame.mixer.set_num_channels(settings.numChannels)
assets = Assets() # LOAD ASSETS
settings.debug("Assets loaded") # Debug


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
leadersInput = [pygame.K_l]
creditsInput = [pygame.K_c]
brakeInput = [pygame.K_LALT,pygame.K_RALT]
muteInput = [pygame.K_m]
hangerInput = [pygame.K_h]
fullScreenInput = [pygame.K_f]
startInput = [pygame.K_SPACE]
settings.debug("Loaded keybinds") # Debug


# UPDATE DISPLAY
def displayUpdate(gameClock):
    if not settings.updateNotFlip: pygame.display.flip()
    else: pygame.display.update()
    if gameClock is not None: gameClock.tick(settings.fps)


# WINDOW
screenColor = [0,0,0] # Screen fill color
presence = None # DISCORD PRESENCE


# ASYNCHRONOUSLY UPDATE DISCORD PRESENCE
async def getPresence(presence):
    try:
        await asyncio.wait_for(presence.connect(),timeout = 0.5)
        await presence.update(details='Playing Navigator', state='Navigating the depths of space', large_image='background', small_image = 'icon', buttons=[{'label': 'Play Navigator', 'url': 'https://pstlo.github.io/navigator'}],start=int(time.time()))
        settings.debug("Discord presence connected") # Debug
    except:
        settings.debug("Discord presence timed out, likely due to multiple launches in a short duration") # Debug
        return None


if settings.showPresence:
    try:
        import pypresence
        presence = pypresence.AioPresence((Fernet(base64.b64decode(os.getenv('DCKEY'))).decrypt(os.getenv('DCTOKEN'))).decode())
        settings.debug("Loading Discord presence") # Debug
        asyncio.run(getPresence(presence))
    except:
        presence = None
        settings.debug("Continuing without Discord presence") # Debug

# CURSOR
curSurf = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.line(curSurf, (0, 255, 0), (10, 20), (30, 20), settings.cursorThickness)
pygame.draw.line(curSurf, (0, 255, 0), (20, 10), (20, 30), settings.cursorThickness)
cursor = pygame.cursors.Cursor((20, 20), curSurf)
pygame.mouse.set_cursor(cursor)
pygame.mouse.set_visible(settings.cursorMode)
settings.debug("Initialized cursor") # Debug


# KEEP CURSOR ON SCREEN (Cursor mode only)
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
    settings.debug("Initialized controller module") # Debug
    if pygame.joystick.get_count() > 0:
        settings.debug("Joystick detected, checking for compatibility") # Debug
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
                controllerNextShip = settings.controllerBinds[controllerType]['nextShip']
                controllerLastShip = settings.controllerBinds[controllerType]['lastShip']
                controllerNextSkin = settings.controllerBinds[controllerType]['nextSkin']
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
                settings.debug("Compatible controller found, loaded corresponding binds") # Debug
                break

        # Incompatible controller
        if not compatibleController:
            settings.debug("Incompatible controller") # Debug
            pygame.joystick.quit()
            settings.debug("Uninitialized controller module") # Debug
            if settings.useController: settings.useController = False

    else:
        settings.debug("Controller not found") # Debug
        pygame.joystick.quit()
        settings.debug("Uninitialized controller module") # Debug
        if settings.useController: settings.useController = False

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


# QUIT GAME
def quitGame():
    pygame.quit() # UNINITIALIZE PYGAME
    assets.uploadRecords(game.records) # UPLOAD TO LEADERBOARD
    sys.exit() # EXIT NAVIGATOR


# ROTATE IMAGES
def rotateImage(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    rotatedRect = rotated.get_rect(center=rect.center)
    return rotated,rotatedRect


# MOVEMENT AND POSITION GENERATION
def getMovement(spawnPattern):
    top,bottom,left,right = [],[],[],[]
    if spawnPattern == "TOP": top = ["SE", "SW", "S"] # Top to bottom
    elif spawnPattern == "BOTTOM": bottom = ["N","NE","NW"] # Bottom to top
    elif spawnPattern == "LEFT":left = ["E","NE","SE"] # Left to right
    elif spawnPattern == "RIGHT":right = ["W","NW","SW"] # Right to left
    elif spawnPattern == "VERT": top, bottom = ["SE", "SW", "S"], ["N", "NE", "NW"]
    elif spawnPattern == "HORI": left, right = ["E","NE","SE"], ["W","NW","SW"]
    elif spawnPattern == "DIAG": top, bottom, left, right = ["SE", "SW"], ["NE", "NW"], ["NE", "SE"], ["NW", "SW"]
    else: top, bottom, left, right = ["SE", "SW", "S"], ["N", "NE", "NW"], ["E", "NE", "SE"], ["NW", "SW", "W"]

    X = random.randint(settings.screenSize[0] * 0.02, settings.screenSize[0] * 0.98)
    Y = random.randint(settings.screenSize[1] * 0.02, settings.screenSize[1] * 0.98)

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
    position = [movement[0], movement[1]]
    direction = movement[2]
    move = [position,direction]

    return move


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



# GAME
class Game:
    def __init__(self):

        # GAME RECORDS
        self.records = assets.loadRecords()
        self.unlocks = Unlocks(self.records['unlocks']) # UNLOCKS

        # Level constants
        self.maxObstacles = assets.stageList[0][0]["maxObstacles"]
        self.levelType = assets.stageList[0][0]["levelType"]
        self.wipe = assets.stageList[0][0]["wipeObstacles"] # Old obstacle handling
        self.angle = assets.stageList[0][0]["levelAngle"] # Game rotation
        self.cloudSpeed = settings.cloudSpeed

        self.currentLevel = 1
        self.currentStage = 1
        self.score = 0 # Points collected
        self.coinsCollected = 0 # Coins collected

        self.thisPoint = Point(None,None) # Currently active point (starts with default)
        self.lastPointPos = self.thisPoint.rect.center # Last point's position for spacing
        self.gameClock = 0
        self.pauseCount = 0
        self.attemptNumber = 1
        self.mainMenu = True # Assures start menu only runs when called
        self.sessionLongRun = 0 # Longest run this session

        self.skipAutoSkinSelect = False # For re-entering home menu from game over screen
        self.savedSkin = 0 # Saved ship skin
        self.savedShipLevel = 0 # Saved ship type

        self.cloudPos = settings.cloudStart # Background cloud position
        self.explosions = [] # Obstacle explosions
        self.collidingExplosions = [] # Explosions with hitboxes
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


    # MAIN GAME LOOP
    def update(self,player,obstacles,menu,events,lasers,enemyLasers):
        for event in pygame.event.get():

            # EXIT GAME
            if event.type == pygame.QUIT: quitGame()

            # BACK TO MENU
            if (event.type == pygame.KEYDOWN and event.key in escapeInput) or (gamePad is not None and gamePad.get_button(controllerExit) == 1): menu.gameOver(self,player,obstacles)

            # MUTE
            if (event.type == pygame.KEYDOWN and event.key in muteInput) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

            # PAUSE GAME
            if game.pauseCount < settings.pauseMax and ( (event.type == pygame.KEYDOWN and event.key in pauseInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerPause)==1) ):
                game.pauseCount += 1
                menu.pause(game,player,obstacles,lasers,enemyLasers)

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

            # NEAR MISS VISUAL
            if event.type == events.nearMissIndicator and self.nearMissCount > 0: self.nearMissCount = 0

        # BACKGROUND
        screen.fill(screenColor)
        screen.blit(assets.bgList[self.currentStage - 1][0], (0,0) )
        self.showPlanet() # Draw planet

        # MOVE PLANET
        if self.planetDelay < settings.planetMoveDelay: self.planetDelay += 1
        else:
            self.planetRect.centery += 1
            self.planetDelay = 0

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
        if self.cave is None or (self.cave is not None and not self.cave.inside()): screen.blit(self.thisPoint.image, self.thisPoint.rect)

        # CAVES
        if "CAVE" in self.levelType or self.cave is not None:
            # LEAVING CAVE
            if self.cave is not None and self.cave.leave and self.cave.rect.top > settings.screenSize[1]:
                self.cave.kill()
                self.cave = None

            # IN CAVE
            else:
                if self.cave is None: # SPAWN A CAVE
                    self.cave = Cave(self.caveIndex)
                    if self.caveIndex + 1 < len(assets.caveList): self.caveIndex+=1
                self.cave.update()

                # DRAW CAVE
                screen.blit(self.cave.background,self.cave.rect)
                if self.cave.inside: screen.blit(self.thisPoint.image, self.thisPoint.rect) # draw point between cave layers
                screen.blit(self.cave.image,self.cave.rect)

                # COLLISION DETECTION
                if pygame.sprite.collide_mask(self.cave,player):
                    if player.shields > 0: player.shieldDown(events)
                    else:
                        player.explode(game,obstacles) # explosion
                        if not self.musicMuted: assets.explosionNoise.play()
                        menu.gameOver(self,player,obstacles) # Game over
                enemyLasersCollided = pygame.sprite.spritecollide(self.cave,enemyLasers,True,pygame.sprite.collide_mask) # Enemy lasers/cave
                lasersCollided = pygame.sprite.spritecollide(self.cave,lasers,True,pygame.sprite.collide_mask) # Lasers/cave
                for laser in lasersCollided: self.explosions.append(Explosion(laser,None))
                for laser in enemyLasersCollided: self.explosions.append(Explosion(laser,None))
                enemyLasers.remove(enemyLasersCollided)
                lasers.remove(lasersCollided)

        # HUD
        if settings.showHUD: self.showHUD(player)

        # PLAYER/POWERUP COLLISION DETECTION
        if pygame.sprite.collide_mask(player,self.thisPoint):
            if self.thisPoint.powerUp == "Fuel": # Fuel cell collected
                player.fuel += player.maxFuel/4 # Replenish quarter tank
                if player.fuel > player.maxFuel: player.fuel = player.maxFuel
                if not self.musicMuted: assets.powerUpNoise.play()

            elif self.thisPoint.powerUp == "Shield": # Shield piece collected
                player.shieldUp()
                if not self.musicMuted: assets.powerUpNoise.play()

            elif self.thisPoint.powerUp == "Coin": # Coin collected
                self.coinsCollected += 1
                self.score += 1 # Used as bonus point for now
                if not self.musicMuted: assets.coinNoise.play()

            elif self.thisPoint.powerUp == "Nuke":
                self.collidingExplosions.append(Explosion(self.thisPoint,settings.nukeSize))
                if not self.musicMuted: assets.explosionNoise.play()

            else:
                if not self.musicMuted: assets.pointNoise.play()

            self.score += 1
            self.thisPoint.kill()
            self.lastPointPos = self.thisPoint.rect.center # Save last points position
            self.thisPoint = Point(player,self.lastPointPos) # spawn new point

        # DRAW COLLIDING EXPLOSIONS
        for debris in self.collidingExplosions:
            if debris.finished: self.collidingExplosions.remove(debris)
            else: debris.update()

        # UPDATE PLAYER
        player.movement()
        player.shoot(self,lasers,events,obstacles)
        player.boost(self,events)
        player.wrapping()
        player.updateAnimation()

        # ROTATE PLAYER
        newBlit = rotateImage(player.image,player.rect,player.angle)

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

        # PLAYER/LASER COLLISION DETECTION
        if pygame.sprite.spritecollide(player,enemyLasers,True,pygame.sprite.collide_mask):
            if player.shields > 0:player.shieldDown(events)
            else:
                player.explode(game,obstacles) # Animation
                if not self.musicMuted: assets.explosionNoise.play()
                menu.gameOver(self,player,obstacles) # Game over

        # DRAW LASERS
        self.laserUpdate(lasers,enemyLasers,player,obstacles)

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
                obs.move(player,enemyLasers)
                obs.activate() # Activate if on screen
                if obs.active:

                    # NEAR MISSES
                    if settings.nearMisses and obs not in self.nearObsList:
                        nearDist = math.dist(player.rect,obs.rect)
                        if nearDist <= settings.nearMissDist: self.nearObsList.append(obs)

                    # OBSTACLE/LASER COLLISION DETECTION
                    if pygame.sprite.spritecollide(obs,lasers,not player.laserCollat,pygame.sprite.collide_mask):
                        if obs.health - player.damage > 0: obs.health -= player.damage
                        else:
                            obs.kill()
                            obstacles.remove(obs)
                            if not self.musicMuted: assets.impactNoise.play()
                            self.explosions.append(Explosion(obs,None))

                    # OBSTACLE/CAVE COLLISION DETECTION
                    elif self.cave is not None and pygame.sprite.collide_mask(obs,self.cave):
                        if not self.musicMuted: assets.impactNoise.play()
                        self.explosions.append(Explosion(obs,None))
                        obs.kill()

                    # OBSTACLE/EXPLOSION COLLISION DETECTION
                    elif len(self.collidingExplosions) > 0:
                        for explosion in self.collidingExplosions:
                            if pygame.sprite.collide_mask(obs,explosion):
                                if not self.musicMuted: assets.impactNoise.play()
                                self.explosions.append(Explosion(obs,None))
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

        if settings.nearMisses: self.nearMisses(player,events) # NEAR MISS CALCULATION

        if self.gameClock > self.sessionLongRun: self.sessionLongRun = self.gameClock # UPDATE HIGH SCORE
        if not self.endlessModeStarted: self.levelUpdater(player,obstacles,events) # LEVEL UP
        if "OBS" in self.levelType or self.endlessModeStarted: self.spawner(obstacles,player) # SPAWN OBSTACLES

        # UPDATE SCREEN
        player.lastAngle = player.angle # Save recent player orientation
        if settings.resetPlayerOrientation: player.angle = self.angle # Reset player orientation
        player.boosting = False
        if settings.showFPS: pygame.display.set_caption("Navigator {} FPS".format(int(self.clk.get_fps())))
        displayUpdate(self.clk)


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
            cloudImg = assets.bgList[game.currentStage - 1][1]
            cloudRect = cloudImg.get_rect(center = (settings.screenSize[0]/2,game.cloudPos))
            if cloudRect.bottom >= 0 and cloudRect.top <= settings.screenSize[1]: screen.blit(cloudImg, cloudRect) # Draw cloud


    # DRAW PLANET
    def showPlanet(self):
        if self.planetImage is not None:
            if self.planetRect.top < settings.screenSize[1]:
                screen.blit(self.planetImage,self.planetRect)
            else: self.getNewPlanet()


    # GET NEW PLANET ( In progress )
    def getNewPlanet(self):
        if settings.unlimitedPlanets:
            self.planetRect.center = (random.randint(100,settings.screenSize[0]-100),-10)


    # RESET PLANETS
    def resetPlanets(self):
        self.planetImage = pygame.transform.scale(assets.planets[0],(self.planetStartSize,self.planetStartSize))
        self.planetRect = self.planetImage.get_rect()
        self.planetRect.center = self.planetStartPos
        self.planetIndex = 0


    # Draw frame outside of main loop
    def alternateUpdate(self,player,obstacles,events):
        for event in pygame.event.get(): pass # Pull events

        player.updateAnimation()
        player.movement()
        player.wrapping()
        screen.fill(screenColor)
        screen.blit(assets.bgList[self.currentStage - 1][0], (0,0) )
        self.showPlanet()
        if self.cave is not None: screen.blit(self.cave.background,self.cave.rect)
        self.showBackgroundCloud()
        self.cloudPos += self.cloudSpeed
        if self.cave is not None:
            self.cave.update()
            if self.cave.rect.top <= settings.screenSize[1] and self.cave.rect.bottom >= 0: screen.blit(self.cave.image,self.cave.rect) # DRAW CAVE

        for obs in obstacles:
            obs.move(player,None)
            obs.activate()
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1])
            obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle

        if settings.showFPS: pygame.display.set_caption("Navigator {} FPS".format(int(self.clk.get_fps())))


    # UPDATE GAME CONSTANTS
    def levelUpdater(self,player,obstacles,events):

        # UPDATES STAGE
        if self.currentStage < len(assets.stageList): # Make sure there is a next stage
            if self.gameClock == assets.stageList[self.currentStage][0]["startTime"]  and not assets.stageList[self.currentStage][0]["START"]: # Next stage's first level's activation time reached
                assets.stageList[self.currentStage][0]["START"] = True # Mark as activated

                if self.currentStage == len(assets.stageList)-1: self.endlessModeStarted = True # START OVERTIME/ENDLESS MODE

                stageUpCloud = assets.stageCloudImg

                if not self.endlessModeStarted: stageUpText = "STAGE UP"
                else: stageUpText = "OVERTIME"

                stageUpDisplay = assets.stageUpFont.render(stageUpText, True, settings.primaryFontColor)
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
                    if settings.showHUD: game.showHUD(player)
                    img, imgRect = rotateImage(player.image, player.rect, player.angle)
                    screen.blit(img,imgRect) # Draw player
                    stageUpRect.centery += settings.stageUpCloudSpeed

                    if stageUpRect.centery >= settings.screenSize[1]/2 and stageWipe:
                        self.currentStage += 1
                        self.currentLevel = 1
                        stageWipe = False

                    elif stageUpRect.centery >= settings.screenSize[1] * 2: stageUp = False
                    displayUpdate(self.clk)
                    player.angle = self.angle # Update game orientation

        # UPDATES LEVEL
        for levelDict in assets.stageList[self.currentStage-1]:
            if self.gameClock == levelDict["startTime"] and not levelDict["START"] and ( (self.currentLevel > 1 or self.currentStage > 1) or (len(assets.stageList[0]) > 1 and self.gameClock >= assets.stageList[0][1]["startTime"]) ):
                if assets.stageList[self.currentStage-1][self.currentLevel-1]["wipeObstacles"]:
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
                        if settings.showHUD: game.showHUD(player)
                        img, imgRect = rotateImage(player.image, player.rect, player.angle)
                        screen.blit(img,imgRect) # Draw player
                        levelUpRect.centery += settings.levelUpCloudSpeed
                        if levelUpRect.top >= settings.screenSize[1]: levelUp = False
                        player.angle = self.angle
                        displayUpdate(self.clk)

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
        for stage in assets.stageList:
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
        timerDisplay = assets.mediumFont.render(str(self.gameClock), True, settings.secondaryFontColor)
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright)

        # STAGE DISPLAY
        if not self.endlessModeStarted: stageNum = "Stage " + str(self.currentStage)
        else: stageNum = "Overtime"
        stageDisplay = assets.mediumFont.render( str(stageNum), True, settings.secondaryFontColor )
        stageRect = stageDisplay.get_rect(topleft = screen.get_rect().topleft)

        # LEVEL DISPLAY
        if not self.endlessModeStarted: levelNum = "-  Level " + str(self.currentLevel)
        else: levelNum = ""
        levelDisplay = assets.mediumFont.render( str(levelNum), True, settings.secondaryFontColor )
        levelRect = levelDisplay.get_rect()
        levelRect.center = (stageRect.right + levelRect.width*0.65, stageRect.centery)

        # SCORE DISPLAY
        scoreNum = "Score " + str(self.score)
        scoreDisplay = assets.mediumFont.render(scoreNum, True, settings.secondaryFontColor)
        scoreRect = scoreDisplay.get_rect()
        scoreRect.topleft = (settings.screenSize[0] - (2*scoreRect.width), levelRect.y)

        # NEAR MISSES DISPLAY
        if settings.nearMisses and self.nearMissCount > 0:
            if self.nearMissCount >1: nearMissText = "Near Miss! x" + str(self.nearMissCount)
            else: nearMissText = "Near Miss!"
            nearMissDisplay = assets.labelFont.render(nearMissText, True, settings.secondaryFontColor)
            nearMissRect = nearMissDisplay.get_rect(center = (scoreRect.midbottom[0],scoreRect.bottom + 5))
            screen.blit(nearMissDisplay,nearMissRect)

        screen.blit(timerDisplay, timerRect)
        screen.blit(stageDisplay, stageRect)
        if not self.endlessModeStarted: screen.blit(levelDisplay, levelRect)
        screen.blit(scoreDisplay, scoreRect)


    # SPAWN OBSTACLES
    def spawner(self,obstacles,player):
        if len(obstacles) < self.maxObstacles:
            if not self.endlessModeStarted: obstacle = Obstacle([player.rect.centerx,player.rect.centery])
            else:
                attributes = {
                    "size" : random.randint(20,60),
                    "speed" : random.randint(5,10)
                }
                obstacle = Obstacle([player.rect.centerx,player.rect.centery], size = attributes['size'], speed = attributes["speed"])
            obstacles.add(obstacle)


    # Update all lasers
    def laserUpdate(self,lasers,enemyLasers,player,obstacles):
        lasers.update(player,lasers,obstacles)
        enemyLasers.update(player)
        for laser in lasers: screen.blit(laser.image,laser.rect)
        for laser in enemyLasers: screen.blit(laser.image,laser.rect)


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
        self.gameClock = 0
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
        assets.loadSoundtrack()
        pygame.mixer.music.play()
        if self.musicMuted: pygame.mixer.music.set_volume(0)
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

        # NEAR MISS INDICATOR
        self.nearMissIndicator = pygame.USEREVENT + 6


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


    def nearMiss(self): pygame.time.set_timer(self.nearMissIndicator,settings.nearMissIndicatorDuration)


    # CHECK EVENTS
    def muteEvent(self,event):
        # TOGGLE MUTE
        if ((event.type == pygame.KEYDOWN) and (event.key in muteInput)) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)



# MENUS
class Menu:

    # START MENU
    def home(self,game,player):

        # TITLE TEXT
        startRect = assets.titleText.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/3))

        # Foreground icons
        fgIcons = []
        for icon in range(settings.maxFgIcons): fgIcons.append(Icon("FG"))

        # Background icons
        bgIcons = []
        for bgIcon in range(settings.maxBgIcons): bgIcons.append(Icon("BG"))

        # Colliding icons
        cgIcons = []
        for cgIcon in range(settings.maxCgIcons): cgIcons.append(Icon("CG"))

        # PLANET
        planet = pygame.sprite.Sprite()
        planet.image = assets.planets[0]
        planet.rect = planet.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/3 +50))
        planet.mask = pygame.mask.from_surface(planet.image)
        planetSize = planet.rect.size[0]

        # HELP CONTEXT
        if not game.usingController or gamePad is None:
            startDisplays = self.getHelpLabels(False)
            controlDisplays = self.getControlLabels(player,False)

        else:
            startDisplays = self.getHelpLabels(True)
            controlDisplays = self.getControlLabels(player,True)

        versionDisplay = assets.versionFont.render(version,True,settings.primaryFontColor)
        versionRect = versionDisplay.get_rect(center = (startRect.right-120,startRect.bottom-20))

        # Coin Display
        coinDisplay = assets.mediumFont.render(str(game.records['coins']), True, settings.secondaryFontColor)
        coinDisplayRect = coinDisplay.get_rect(center = (settings.screenSize[0] -25, 25))
        coinIconRect = assets.coinIcon.get_rect(center = (settings.screenSize[0] -60, 25))

        try:
            game.unlocks.update(game) # GET NEW UNLOCKS
            settings.debug("Refreshed unlocks") # Debug
        except:
            settings.debug("Version incompatibility detected") # Debug
            game.records['unlocks'] = assets.getDefaultUnlocks()
            assets.storeRecords(game.records)
            game.unlocks.update(game)
            settings.debug("Updated successfully") # Debug

        if settings.defaultToHighShip:
            if game.unlocks.hasShipUnlock(): player.getShip(game.unlocks.highestShip()) # Gets highest unlocked ship by default

        if settings.defaultToHighSkin and not game.skipAutoSkinSelect: player.getSkin(game.unlocks.highestSkin(game.savedShipLevel)) # Gets highest unlocked skin by default
        elif game.skipAutoSkinSelect: player.getSkin(game.savedSkin)

        shipAttributes = self.shipStatsDisplay() # Ship stats display

        iconPosition = 100 # Icon position at game start (offset from original)

        while game.mainMenu:
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
                        if planetSize-25 > 0:
                            planetSize -= 25
                            planet.rect.centery -= 10
                        planet.image = pygame.transform.scale(assets.planets[game.planetIndex],(planetSize,planetSize))
                        planet.rect = planet.image.get_rect(center = planet.rect.center)

                        # Start animation
                        screen.fill(screenColor)
                        screen.blit(assets.bgList[game.currentStage - 1][0],(0,0))
                        screen.blit(planet.image,planet.rect)
                        screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Current spaceship
                        displayUpdate(game.clk)
                        iconPosition -= (player.speed+1)

                    game.planetImage = planet.image
                    game.planetRect = planet.rect
                    game.planetStartPos = planet.rect.center
                    game.planetStartSize = planet.rect.size[0]

                    game.explosions.clear()
                    game.mainMenu = False
                    assets.loadSoundtrack()
                    pygame.mixer.music.play()
                    return

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1):
                    toggleScreen()

                # NEXT SPACESHIP SKIN
                if (event.type == pygame.KEYDOWN and event.key in rightInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerNextSkin) or (event.type == pygame.JOYBUTTONDOWN and type(controllerNextSkin) == int and gamePad.get_button(controllerNextSkin)==1))):
                    player.toggleSkin(True)

                # PREVIOUS SPACESHIP SKIN
                elif (event.type == pygame.KEYDOWN and event.key in leftInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerLastSkin) or (event.type == pygame.JOYBUTTONDOWN and type(controllerLastSkin) == int and gamePad.get_button(controllerLastSkin)==1))):
                    player.toggleSkin(False)

                # NEXT SHIP TYPE
                if (event.type == pygame.KEYDOWN and event.key in upInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerNextShip) or (event.type == pygame.JOYBUTTONDOWN and type(controllerNextShip) == int and gamePad.get_button(controllerNextShip)==1))):
                    player.toggleSpaceShip(True)
                    shipAttributes = self.shipStatsDisplay()
                    controlDisplays = self.getControlLabels(player,game.usingController)

                # PREVIOUS SHIP TYPE
                elif (event.type == pygame.KEYDOWN and event.key in downInput) or (gamePad is not None and (gamePad.get_numhats() > 0 and (gamePad.get_hat(0) == controllerLastShip) or (event.type == pygame.JOYBUTTONDOWN and type(controllerLastShip) == int and gamePad.get_button(controllerLastShip)==1))):
                    player.toggleSpaceShip(False)
                    shipAttributes = self.shipStatsDisplay()
                    controlDisplays = self.getControlLabels(player,game.usingController)

                # EXIT
                if (event.type == pygame.KEYDOWN and event.key in escapeInput) or (gamePad is not None and gamePad.get_button(controllerExit) == 1) or event.type == pygame.QUIT: quitGame()

                # MUTE
                if (event.type == pygame.KEYDOWN) and (event.key in muteInput) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

                # LEADERBOARD
                if (event.type == pygame.KEYDOWN) and (event.key in leadersInput):
                    menu.leaderboard()
                    if not settings.connectToLeaderboard: startDisplays = self.getHelpLabels(game.usingController) # Disable leaderboard keybind display if unable to connect

                # CREDITS
                if (event.type == pygame.KEYDOWN and event.key in creditsInput) or (gamePad is not None and gamePad.get_button(controllerCredits) == 1): self.creditScreen()

                # HANGER
                if event.type == pygame.KEYDOWN and event.key in hangerInput: self.hanger(player,game.unlocks)

                # SWITCH CONTROL TYPE
                if game.usingController and event.type == pygame.KEYDOWN:
                    startDisplays = self.getHelpLabels(False)
                    controlDisplays = self.getControlLabels(player,False)
                    game.usingController = False

                elif gamePad is not None and not game.usingController and (event.type == pygame.JOYHATMOTION or event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONUP):
                    startDisplays = self.getHelpLabels(True)
                    controlDisplays = self.getControlLabels(player,True)
                    game.usingController = True

            screen.fill(screenColor)
            screen.blit(assets.bgList[game.currentStage - 1][0],(0,0)) # Background

            # Background icons
            if settings.showMenuIcons:
                for icon in bgIcons:
                    icon.move()
                    icon.draw()

            screen.blit(assets.planets[game.planetIndex],planet.rect)

            # Foreground icons
            if settings.showMenuIcons:
                for icon in fgIcons:
                    icon.move()
                    icon.draw()

            # Colliding icons
            if settings.showMenuIcons:
                for icon in cgIcons:
                    icon.draw()
                    icon.move()
                    if pygame.sprite.collide_mask(icon,planet):
                        game.explosions.append(Explosion(icon,None))
                        icon = icon.getNew()

            # DRAW EXPLOSIONS
            for debris in game.explosions:
                if debris.finished: game.explosions.remove(debris)
                else: debris.update()

            # PLAYER SKIN ANIMATION
            player.updateAnimation()

            screen.blit(assets.titleText,startRect) # Title Text
            if settings.showVersion: screen.blit(versionDisplay,versionRect) # Version info

            # Game controls
            self.drawLabels(startDisplays)
            self.drawLabels(controlDisplays)

            screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Draw current spaceship

            # Coin display
            screen.blit(coinDisplay,coinDisplayRect)
            screen.blit(assets.coinIcon,coinIconRect)

            # Ship stats display
            self.drawStats(shipAttributes)

            displayUpdate(game.clk)


    # PAUSE SCREEN
    def pause(self,game,player,obstacles,lasers,enemyLasers):
        pygame.mixer.music.pause()
        playerBlit = rotateImage(player.image,player.rect,player.lastAngle)
        paused = True

        pausedDisplay = assets.largeFont.render("Paused", True, settings.secondaryFontColor)
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
            game.showPlanet()
            game.showBackgroundCloud()
            if game.cave is not None:
                screen.blit(game.cave.background,game.cave.rect)
                screen.blit(game.cave.image,game.cave.rect) # Draw cave

            if settings.showHUD: game.showHUD(player)
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

            lasers.draw(screen)
            enemyLasers.draw(screen)
            screen.blit(pauseDisplay, pauseRect)
            screen.blit(pausedDisplay,pausedRect)
            displayUpdate(game.clk)

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
        assets.loadGameOverMusic()
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

        assets.storeRecords(game.records) # SAVE UPDATED RECORDS
        if settings.connectToLeaderboard and (newHighScore or newLongRun):
            newRecordDisplay = assets.mediumFont.render("NEW RECORD!",True,(0,0,0))
            newRecordRect = newRecordDisplay.get_rect(center = player.rect.center)
            screen.blit(newRecordDisplay,newRecordRect)
            pygame.display.update()
            assets.uploadRecords(game.records) # upload to database

        statsOffsetY = settings.screenSize[1]/10
        statsSpacingY = settings.screenSize[1]/20

        # "GAME OVER" text
        gameOverDisplay = assets.largeFont.render("GAME OVER", True, [255,0,0])
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
        scoreDisplay = assets.mediumFont.render(scoreLine, True, settings.primaryFontColor)
        highScoreDisplay = assets.mediumFont.render(highScoreLine, True, settings.primaryFontColor)
        newHighScoreDisplay = assets.mediumFont.render(newHighScoreLine, True, settings.primaryFontColor)
        longestRunDisplay = assets.mediumFont.render(overallLongestRunLine, True, settings.primaryFontColor)
        survivedDisplay = assets.mediumFont.render(survivedLine, True, settings.primaryFontColor)
        levelDisplay = assets.mediumFont.render(levelLine, True, settings.primaryFontColor)
        newLongestRunDisplay = assets.mediumFont.render(newLongestRunLine, True, settings.primaryFontColor)
        attemptDisplay = assets.mediumFont.render(attemptLine, True, settings.primaryFontColor)
        timeWastedDisplay = assets.mediumFont.render(timeWasted,True,settings.primaryFontColor)
        if not game.usingController or gamePad is None: exitDisplay = assets.mediumFont.render("TAB = Menu     SPACE = Restart    ESCAPE = Quit    C = Credits", True, settings.primaryFontColor)
        else: exitDisplay = assets.mediumFont.render("SELECT = Menu    A = Restart    START = Quit    Y = Credits", True, settings.primaryFontColor)

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
            screen.fill(screenColor)
            screen.blit(assets.bgList[game.currentStage - 1][0], (0,0) )
            game.showPlanet()
            game.showBackgroundCloud()
            if game.cave is not None:
                screen.blit(game.cave.background,game.cave.rect)
                screen.blit(game.cave.image,game.cave.rect) # Draw cave

            if type(player.finalImg) != str: screen.blit(player.finalImg,player.finalRect) # Explosion / skip if explosion not initialized yet

            pygame.draw.rect(screen, screenColor, [gameOverRect.x - 12,gameOverRect.y + 4,gameOverRect.width + 16, gameOverRect.height - 16],0,10)
            screen.blit(gameOverDisplay,gameOverRect)
            self.drawGameOverLabels(displayTextList,newHighScore,newLongRun)
            screen.blit(exitDisplay,exitRect)
            displayUpdate(game.clk)

            for event in pygame.event.get():

                # CREDITS
                if event.type == pygame.KEYDOWN and event.key in creditsInput or (gamePad is not None and gamePad.get_button(controllerCredits) == 1): menu.creditScreen()

                # EXIT
                if (event.type == pygame.KEYDOWN and event.key in escapeInput) or (gamePad is not None and gamePad.get_button(controllerExit) == 1) or event.type == pygame.QUIT: quitGame()

                # MUTE
                if (event.type == pygame.KEYDOWN) and (event.key in muteInput) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

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
                    elif (gamePad is not None and gamePad.get_button(controllerSelect) == 1): game.usingController,game.usingCursor = True,False
                    elif (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]==1): game.usingCursor, game.usingController = True, False
                    pygame.mouse.set_visible(game.usingCursor and not settings.rawCursorMode)
                    game.reset(player,obstacles)
                    player.updatePlayerConstants()
                    gameLoop()


    # GET LABEL
    def getLabel(self,text,pos,font):
        if type(font) == pygame.font.Font: labelDisplay = font.render(text,True,settings.primaryFontColor)
        else: labelDisplay = assets.labelFont.render(text,True,settings.primaryFontColor)
        labelRect = labelDisplay.get_rect(center = pos)
        return [labelDisplay,labelRect]


    # DRAW LABELS
    def drawLabels(self,textList):
        for text in textList: screen.blit(text[0],text[1])


    # Draw labels from formatted list of rects and displays, first 4 lines arranged based on truth value of two booleans / will be revisited
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
        elif conditionTwo and not conditionOne:
            for x in range(len(textList)):
                if x != 0 and x!= 1 and x!= 5: # Skip 1st, 2nd, and 6th items
                    textList[x][1].center = settings.screenSize[0]/2, settings.screenSize[1]/3+ statsOffsetY + statsSpacingY * (x+1 - skipped)
                    screen.blit(textList[x][0],textList[x][1])
                else: skipped+=1

        # newLongestRun
        elif conditionOne and not conditionTwo:
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


    # LEADERBOARD
    def leaderboard(self):
        if settings.connectToLeaderboard:
            self.loadingScreen()
            assets.leaderboard = assets.getLeaders()
            if assets.leaderboard is None: showLeaderboard = False
            else: showLeaderboard = True
            titleDisplay = assets.leaderboardTitleFont.render("LEADER BOARD", True, settings.primaryFontColor)
            titleRect = titleDisplay.get_rect(center=(settings.screenSize[0]/2, 70))
            cellW = settings.screenSize[0] * 0.6
            cellH = 40
            leaderboardX = (settings.screenSize[0] - cellW) / 2  # Center the table horizontally
            leaderboardY = 100
            headerText = "#       Name                              Time       Score"
            headerDisplay = assets.mediumFont.render(headerText, True, settings.primaryFontColor)
            headerRect = headerDisplay.get_rect(topleft=(settings.screenSize[0]*0.2, leaderboardY))
            leaderSpacing = 40
            cellBorder = 2
            maxUsernameLength = 15

            helpText = "ESCAPE or TAB = Back"
            label = self.getLabel(helpText,[settings.screenSize[0]/2,settings.screenSize[1]*0.9],None)

            while showLeaderboard:
                for event in pygame.event.get():
                    # QUIT GAME
                    if event.type == pygame.QUIT: quitGame()

                    # RETURN TO GAME
                    if ((event.type == pygame.KEYDOWN and (event.key in escapeInput or event.key in leadersInput or event.key in startInput or event.key in backInput)) or (gamePad is not None and gamePad.get_button(controllerBack) == 1)) or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]==1): showLeaderboard = False

                screen.fill(screenColor)
                screen.blit(assets.bgList[game.currentStage - 1][0], (0, 0))

                screen.blit(titleDisplay,titleRect) # 'Leaderboard' text
                screen.blit(headerDisplay, headerRect) # Leaderboard table header

                # DRAW LEADERBOARD
                for index, leader in enumerate(assets.leaderboard):

                    # Name coloring
                    if leader['id'] == game.records['id']:
                        if index == 0: thisColor = (255,0,0)
                        else: thisColor = (255,255,255)
                    else: thisColor = (0,0,0)

                    cellX = leaderboardX
                    cellY = leaderboardY + (index + 1) * leaderSpacing
                    pygame.draw.rect(screen, settings.primaryFontColor, (cellX, cellY, cellW, cellH))
                    pygame.draw.rect(screen, (0, 0, 0), (cellX, cellY, cellW, cellH), cellBorder)

                    rankText = f"{index + 1}."
                    rankDisplay = assets.mediumFont.render(rankText, True, thisColor)
                    rankRect = rankDisplay.get_rect(midleft=(cellX + 10, cellY + cellH // 2))
                    screen.blit(rankDisplay, rankRect)

                    nameText = leader['name'][:maxUsernameLength]
                    nameDisplay = assets.mediumFont.render(nameText, True, thisColor)
                    nameRect = nameDisplay.get_rect(midleft=(cellX + cellW //12, cellY + cellH // 2))
                    screen.blit(nameDisplay, nameRect)

                    timeText= str(leader['time']) + "s"
                    timeDisplay = assets.mediumFont.render(timeText, True, thisColor)
                    timeRect = timeDisplay.get_rect(center=(cellX + cellW * 0.7, cellY + cellH // 2))
                    screen.blit(timeDisplay, timeRect)

                    scoreText = str(leader['score'])
                    scoreDisplay = assets.mediumFont.render(scoreText, True, thisColor)
                    scoreRect = scoreDisplay.get_rect(center=(cellX + cellW * 0.88, cellY + cellH // 2))
                    screen.blit(scoreDisplay, scoreRect)

                for index in range(len(assets.leaderboard) + 1):pygame.draw.line(screen, (0, 0, 0), (leaderboardX, leaderboardY + (index + 1) * leaderSpacing),(leaderboardX + cellW, leaderboardY + (index + 1) * leaderSpacing), 1)
                screen.blit(label[0],label[1])
                displayUpdate(game.clk)


    # HANGER
    def hanger(self,player,unlocks):
        game.savedSkin = player.currentImageNum
        ships = []
        unlocked = game.records['unlocks']
        startPos,pos = [100,100],[100,100]
        spacingY = 80
        spacingX = 90
        scale = 2

        backLabel = self.getLabel("ESCAPE/TAB = Back",[120,settings.screenSize[1]*0.9 + 20],None)
        selectLabel = self.getLabel("SPACE = Select",[120,settings.screenSize[1]*0.9],None)
        viewLabel = self.getLabel("V = View",[120,settings.screenSize[1]*0.9 - 20],None)

        # Coin Display
        coinDisplay = assets.mediumFont.render(str(game.records['coins']), True, settings.secondaryFontColor)
        coinDisplayRect = coinDisplay.get_rect(center = (settings.screenSize[0] -25, 25))
        coinIconRect = assets.coinIcon.get_rect(center = (settings.screenSize[0] -60, 25))

        for shipIndex in range(len(assets.spaceShipList)):
            skins = []
            images = assets.spaceShipList[shipIndex]['skins']
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
                        oldScale = assets.spaceShipList[shipIndex]['skins'][0].get_rect().size
                        newScale = [oldScale[0]*scale,oldScale[1]*scale]
                        newImg = pygame.transform.scale(assets.spaceShipList[shipIndex]['skins'][0],newScale)
                        newImg.fill([0,0,0], special_flags=pygame.BLEND_RGBA_MIN)
                        skins.append([newImg,newImg.get_rect(center = (pos[0],pos[1]))])

                pos[1]+= spacingY
            pos[1] = startPos[1]
            pos[0] += spacingX
            ships.append(skins)

        # Selected
        selectedShip = game.savedShipLevel
        selectedSkin = game.savedSkin
        selectRect = assets.selectIcon.get_rect()
        textPos = [settings.screenSize[0]/2,settings.screenSize[1]/2 - 80]

        animationCount = 0
        surfSize = [settings.screenSize[0]*1.5,settings.screenSize[1]*1.5]
        iconSurf = pygame.surface.Surface(surfSize, pygame.SRCALPHA)
        iconsPos = [0,0]
        surfMovementSpeed = 4

        showHanger = True
        while showHanger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quitGame()

                # TOGGLE MUTE
                if ((event.type == pygame.KEYDOWN) and (event.key in muteInput)) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1): toggleScreen()

                # RETURN TO GAME
                elif (event.type == pygame.KEYDOWN and (event.key in escapeInput or event.key in backInput or event.key in hangerInput) ) or (gamePad is not None and (gamePad.get_button(controllerBack) == 1)): showHanger = False

                # SELECT SHIP + RETURN TO GAME
                elif event.type == pygame.KEYDOWN and event.key in startInput:
                    # switch to selected ship and return to menu
                    if unlocked[selectedShip][selectedSkin] or settings.devMode:
                        player.getShip(selectedShip)
                        player.getSkin(selectedSkin)
                        if not game.musicMuted: assets.pointNoise.play()
                        showHanger = False

                # SWITCH SHIPS
                elif (event.type == pygame.KEYDOWN and (event.key in leftInput)):
                    if selectedShip == 0: selectedShip = len(ships) - 1
                    else: selectedShip -= 1
                    selectedSkin = 0
                elif (event.type == pygame.KEYDOWN and (event.key in rightInput)):
                    if selectedShip + 1 >= len(ships): selectedShip = 0
                    else: selectedShip += 1
                    selectedSkin = 0

                # SWITCH SKINS
                elif (event.type == pygame.KEYDOWN and (event.key in upInput)):
                    if selectedSkin == 0: selectedSkin = len(ships[selectedShip]) - 1
                    else: selectedSkin -= 1
                elif (event.type == pygame.KEYDOWN and (event.key in downInput)):
                    if selectedSkin + 1 >= len(ships[selectedShip]): selectedSkin = 0
                    else: selectedSkin += 1

                # VIEW SELECTED SHIP
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                    if unlocked[selectedShip][selectedSkin] or settings.devMode: self.viewShip(assets.spaceShipList[selectedShip]['skins'][selectedSkin])

            iconSurf.fill((255,255,255,0))
            screen.blit(assets.bgList[game.currentStage - 1][0], (0, 0))

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
            iconSurf.blit(assets.selectIcon,selectRect)
            screen.blit(iconSurf,[settings.screenSize[0]/2 + iconsPos[0]-selectRect.center[0], settings.screenSize[1]/2 + iconsPos[1]-selectRect.center[1]]) # Draw icons surface on screen

            # Controls labels
            screen.blit(backLabel[0],backLabel[1])
            if unlocked[selectedShip][selectedSkin] or settings.devMode:
                screen.blit(viewLabel[0],viewLabel[1])
                screen.blit(selectLabel[0],selectLabel[1])

            # Coin count
            screen.blit(coinDisplay,coinDisplayRect)
            screen.blit(assets.coinIcon,coinIconRect)

            # Ship Name
            if unlocked[selectedShip][0]: shipName = unlocks.messages[selectedShip][1]
            else: shipName = " ? "
            nameDisplay = assets.mediumFont.render(" " + str(shipName) + " ",True,settings.primaryFontColor)
            nameRect = nameDisplay.get_rect(center = [textPos[0],textPos[1]])

            # Unlock Messages
            unlockMessage = unlocks.messages[selectedShip][0][selectedSkin][0]
            unlockMessageDisplay = assets.labelFont.render(" " + str(unlockMessage) + " ",True,settings.secondaryFontColor)
            unlockMessageRect = unlockMessageDisplay.get_rect(center = [textPos[0],textPos[1] + 25])

            # Variant name
            if unlocked[selectedShip][selectedSkin]: variantName = unlocks.messages[selectedShip][0][selectedSkin][1]
            else: variantName = " ? "
            variantNameDisplay = assets.mediumFont.render(" " + str(variantName) + " ", True, settings.secondaryFontColor)
            variantNameRect = variantNameDisplay.get_rect()
            variantNameRect.center = [nameRect.right + variantNameRect.width/2, textPos[1]]

            # Ship name display
            pygame.draw.rect(screen,screenColor,nameRect,0,5)
            screen.blit(nameDisplay,nameRect)

            # Variant name display
            if variantName is not None:
                pygame.draw.rect(screen,screenColor,variantNameRect,0,5)
                screen.blit(variantNameDisplay,variantNameRect)

            if not unlocked[selectedShip][selectedSkin] and not settings.devMode:
                pygame.draw.rect(screen,screenColor,unlockMessageRect,0,5)
                screen.blit(unlockMessageDisplay,unlockMessageRect) # unlock hint

            displayUpdate(game.clk)


    # VIEW SHIP
    def viewShip(self,image):
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
        backLabel = self.getLabel("ESCAPE/TAB/V = Back",[120,settings.screenSize[1]*0.9 + 20],None)

        viewing = True
        while viewing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quitGame()

                # TOGGLE MUTE
                if ((event.type == pygame.KEYDOWN) and (event.key in muteInput)) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1): toggleScreen()

                # RETURN TO HANGER
                elif (event.type == pygame.KEYDOWN and (event.key in escapeInput or event.key in backInput or event.key in hangerInput or event.key == pygame.K_v) ) or (gamePad is not None and (gamePad.get_button(controllerBack) == 1)): viewing = False

            key = pygame.key.get_pressed()
            if any(key[bind] for bind in upInput) or any(key[bind] for bind in downInput) or any(key[bind] for bind in leftInput) or any(key[bind] for bind in rightInput):
                prevAngle,prevScale = angle,scale
                if any(key[bind] for bind in upInput) and scale+zoomSpeed <= maxZoom: scale += zoomSpeed
                if any(key[bind] for bind in downInput) and scale - zoomSpeed > minZoom: scale -= zoomSpeed
                if any(key[bind] for bind in leftInput): angle += rotateSpeed
                if any(key[bind] for bind in rightInput): angle -= rotateSpeed

                # STATIC SKIN
                if angle != prevAngle or scale != prevScale: # ROTATE AND ZOOM
                    if angle <= -360 or angle >= 360: angle = 0
                    newScale = [oldScale[0]*scale,oldScale[1]*scale]
                    if type(image) != list:
                        newBlit = rotateImage(pygame.transform.scale(img,newScale),imgRect,angle)
                        newImg = newBlit[0]
                        imgRect = newBlit[1]

            # ANIMATED SKIN
            if type(image) == list:
                if animationCount < settings.skinAnimationDelay: animationCount += 1
                else:
                    animationCount = 0
                    if animationIndex + 1 >= len(image): animationIndex = 0
                    else: animationIndex += 1
                newBlit = rotateImage(pygame.transform.scale(image[animationIndex],newScale),imgRect,angle) # ROTATE AND ZOOM
                newImg = newBlit[0]
                imgRect = newBlit[1]

            screen.fill(screenColor)
            screen.blit(assets.bgList[game.currentStage - 1][0], (0,0) )
            screen.blit(newImg,imgRect)
            screen.blit(backLabel[0],backLabel[1])
            displayUpdate(game.clk)


    # CREDITS
    def creditScreen(self):
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

        createdByDisplay = assets.creatorFont.render(createdByLine, True, settings.secondaryFontColor)
        creditsDisplay = assets.mediumFont.render(creditsLine, True, settings.secondaryFontColor)
        musicCreditsDisplay = assets.mediumFont.render(musicCreditsLine, True, settings.secondaryFontColor)
        moreMusicCreditsDisplay = assets.mediumFont.render(moreMusicCreditsLine, True, settings.secondaryFontColor)

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

        if len(assets.donations) == 0: extrasCap = settings.maxExtras

        elif len(assets.donations) > 0:
            if len(assets.donations) < settings.maxExtras: extrasCap = len(assets.donations)
            else: extrasCap = settings.maxExtras

        while rollCredits:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: quitGame()

                # TOGGLE MUTE
                if ((event.type == pygame.KEYDOWN) and (event.key in muteInput)) or (gamePad is not None and gamePad.get_button(controllerMute) == 1): toggleMusic(game)

                # TOGGLE FULLSCREEN
                if (event.type == pygame.KEYDOWN and event.key in fullScreenInput) or (gamePad is not None and event.type == pygame.JOYBUTTONDOWN and gamePad.get_button(controllerFullScreen) == 1): toggleScreen()

                # SHIP SPAWN DELAY
                if event.type == backGroundShipSpawnEvent: waitToSpawn = False

                # RETURN TO GAME
                elif (event.type == pygame.KEYDOWN and (event.key in escapeInput or event.key in creditsInput or event.key in startInput or event.key in backInput) ) or (gamePad is not None and (gamePad.get_button(controllerBack) == 1 or gamePad.get_button(controllerCredits) == 1)): rollCredits = False

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

            screen.blit(createdByDisplay,createdByRect)
            screen.blit(creditsDisplay,creditsRect)
            screen.blit(musicCreditsDisplay,musicCreditsRect)
            screen.blit(moreMusicCreditsDisplay,moreMusicCreditsRect)
            displayUpdate(game.clk)


    # LOADING SCREEN
    def loadingScreen(self):
        loadingLine = "Loading..."
        loadingDisplay = assets.leaderboardTitleFont.render(loadingLine, True, settings.primaryFontColor)
        loadingRect = loadingDisplay.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
        screen.fill(screenColor)
        screen.blit(assets.bgList[game.currentStage - 1][0], (0,0) )
        if game.cave is not None: screen.blit(game.cave.background,game.cave.rect)
        game.showBackgroundCloud()
        screen.blit(loadingDisplay,loadingRect)
        displayUpdate(game.clk)


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
    def shipStatsDisplay(self):
        height = 5
        statsMultiplier = 10
        statsX = settings.screenSize[0]/2 -20
        statsY = settings.screenSize[1]/2 +125
        statsSpacingY = 10
        leftSpacing = -15
        topSpacing = 2

        shipStats = assets.spaceShipList[game.savedShipLevel]['stats']
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
        speedDisplay = assets.shipStatsFont.render("Speed", True, settings.secondaryFontColor)

        boostSpeedBar = pygame.Rect(statsX, statsY + statsSpacingY, boostSpeed, height)
        boostSpeedDisplay = assets.shipStatsFont.render("Boost", True, settings.secondaryFontColor)

        laserBar = pygame.Rect(statsX, statsY + (2*statsSpacingY), lasers, height)
        laserDisplay = assets.shipStatsFont.render("Laser", True, settings.secondaryFontColor)

        shieldBar = pygame.Rect(statsX,statsY + (3*statsSpacingY), shields, height)
        shieldDisplay =  assets.shipStatsFont.render("Shield", True, settings.secondaryFontColor)

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
    def drawStats(self,statsList):
        for i in statsList[0]: screen.blit(i[0],i[1])

        for i in statsList[1]:
            if i[0]: pygame.draw.rect(screen,i[1],i[2])


    # GET HELP LABELS
    def getHelpLabels(self,usingController):
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
                startDisplays.append(self.getLabel(label[0],label[1],assets.mediumFont))

            else:
                startDisplays.append(self.getLabel(label[0],label[1],None))
        return startDisplays


    def getControlLabels(self,player,usingController):
        controlsPos = [settings.screenSize[0]*0.75, settings.screenSize[1]*0.85]
        labels = []
        spacer = 25
        spacing = 0
        if not usingController:
            if len(assets.spaceShipList[game.savedShipLevel]['skins']) > 1 and (settings.devMode or game.unlocks.hasSkinUnlock(game.savedShipLevel)):
                labels.append(["A/LEFT = Last skin     D/RIGHT = Next skin",[controlsPos[0],controlsPos[1]]])
                spacing += spacer
            if len(assets.spaceShipList) > 1 and (settings.devMode or game.unlocks.hasShipUnlock()):
                labels.append(["S/DOWN = Last ship     W/UP = Next ship",[controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
            if player.hasGuns and player.boostSpeed > player.baseSpeed:
                labels.append(["SHIFT = Boost", [controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
                labels.append(["CTRL = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.hasGuns: labels.append(["CTRL = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.boostSpeed > player.baseSpeed: labels.append(["SHIFT = Boost", [controlsPos[0],controlsPos[1]+spacing]])
        else:
            if len(assets.spaceShipList[game.savedShipLevel]['skins']) > 1 and (settings.devMode or game.unlocks.hasSkinUnlock(game.savedShipLevel)):
                labels.append(["D-PAD LEFT = Last skin   D-PAD RIGHT = Next skin",[controlsPos[0],controlsPos[1]]])
                spacing += spacer
            if len(assets.spaceShipList) > 1 and (settings.devMode or game.unlocks.hasShipUnlock()):
                labels.append(["D-PAD DOWN = Last ship   D-PAD UP = Next ship",[controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
            if player.hasGuns and player.boostSpeed > player.baseSpeed:
                labels.append(["LT = Boost", [controlsPos[0],controlsPos[1]+spacing]])
                spacing += spacer
                labels.append(["RT = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.hasGuns: labels.append(["RT = Shoot", [controlsPos[0],controlsPos[1]+spacing]])
            elif player.boostSpeed > player.baseSpeed: labels.append(["LT = Boost", [controlsPos[0],controlsPos[1]+spacing]])

        controlLabels = []
        for label in labels: controlLabels.append(self.getLabel(label[0],label[1],None))
        return controlLabels



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
            if settings.cursorMode: self.lastCursor = pygame.Vector2(0,0)
            self.animated,self.skinAnimationCount,self.skinAnimationFrame,self.skinAnimationFrames = False, 0, 0, 0


        # VECTOR BASED MOVEMENT
        def movement(self):
            # KEYBOARD
            if not game.usingController and not game.usingCursor:
                key = pygame.key.get_pressed()
                direction = pygame.Vector2(0, 0) # Get new vector
                if any(key[bind] for bind in upInput): direction += pygame.Vector2(0, -1)
                if any(key[bind] for bind in downInput): direction += pygame.Vector2(0, 1)
                if any(key[bind] for bind in leftInput): direction += pygame.Vector2(-1, 0)
                if any(key[bind] for bind in rightInput): direction += pygame.Vector2(1, 0)
                if direction.length() > 0: direction.normalize_ip()
                if not any(key[bind] for bind in brakeInput): self.rect.move_ip((math.sqrt(2)*direction) * self.speed) # MOVE PLAYER
                if direction.x != 0 or direction.y != 0: self.angle = direction.angle_to(pygame.Vector2(0, -1)) # GET PLAYER ANGLE

            # CONTROLLER
            elif gamePad is not None and game.usingController:
                direction = pygame.Vector2(0, 0) # Get new vector
                xLeft,yLeft,xRight,yRight = gamePad.get_axis(controllerMoveX),gamePad.get_axis(controllerMoveY),gamePad.get_axis(controllerRotateX),gamePad.get_axis(controllerRotateY)
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
                resetCursor()
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
                    if settings.showCursorPath: pygame.draw.aaline(screen,(0,255,0),(cursorX,cursorY),self.rect.center)
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


        # SWITCH SHIP SKIN
        def toggleSkin(self, toggleDirection):
            if toggleDirection: # Next skin
                if not settings.devMode:
                    skin = game.unlocks.nextUnlockedSkin(game.savedShipLevel,self.currentImageNum)
                    if skin is not None: self.getSkin(skin)
                    elif skin != self.currentImageNum: self.getSkin(0) # Wrap to first skin
                else:
                    if self.currentImageNum +1 < len(assets.spaceShipList[game.savedShipLevel]['skins']): self.getSkin(self.currentImageNum+1)
                    elif len(assets.spaceShipList[game.savedShipLevel]['skins'])-1 != 0: self.getSkin(0)
            else: # Last skin
                if self.currentImageNum >= 1:
                    if not settings.devMode: skin = game.unlocks.lastUnlockedSkin(game.savedShipLevel,self.currentImageNum) # previous skin
                    else: skin = self.currentImageNum - 1
                else: # Wrap to last skin
                    if not settings.devMode: skin = game.unlocks.highestSkin(game.savedShipLevel)
                    else: skin = len(assets.spaceShipList[game.savedShipLevel]['skins'])-1
                if skin is not None: self.getSkin(skin)


        # SWITCH TO SPECIFIC SKIN
        def getSkin(self, skinNum):
            if assets.spaceShipList[game.savedShipLevel]['skins'][skinNum] or settings.devMode:
                self.currentImageNum = skinNum
                skinImage = assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]

                # Animated skin
                if type(skinImage) == list:
                    self.image = skinImage[0]
                    self.skinAnimationFrame, self.skinAnimationFrames = 0, len(assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum]) - 1
                    if not self.animated: self.animated = True # Set flag
                # Static skin
                else:
                    self.image = skinImage
                    if self.animated: self.animated = False
                self.rect = self.image.get_rect(center = (settings.screenSize[0]/2,settings.screenSize[1]/2))
                self.mask = pygame.mask.from_surface(self.image)


        # SWITCH SHIP TYPE
        def toggleSpaceShip(self,toggleDirection): # toggleDirection == True -> next ship / False -> last ship
            if toggleDirection:
                if not settings.devMode:
                    ship = game.unlocks.nextUnlockedShip(game.savedShipLevel)
                    if ship is not None: self.getShip(ship)
                    elif game.savedShipLevel != 0: self.getShip(0)
                else:
                    if game.savedShipLevel +1 < len(assets.spaceShipList): self.getShip(game.savedShipLevel+1) # get next ship
                    elif game.savedShipLevel != 0: self.getShip(0) # Wrap to first ship
            else:
                if not settings.devMode:
                    ship = game.unlocks.lastUnlockedShip(game.savedShipLevel)
                    if ship is not None: self.getShip(ship)
                    elif ship != game.savedShipLevel: self.getShip(game.unlocks.highestShip()) # Wrap to first ship
                else:
                    if game.savedShipLevel >= 1: self.getShip(game.savedShipLevel-1)
                    else: self.getShip(len(assets.spaceShipList)-1) # Wrap to last ship


        # SWITCH TO SPECIFIC SHIP TYPE
        def getShip(self,shipNum):
            if len(assets.spaceShipList) >= shipNum:
                if game.unlocks.hasShipUnlock() or settings.devMode:
                    if game.unlocks.ships[shipNum][0] or settings.devMode:
                        game.savedShipLevel = shipNum
                        self.updatePlayerConstants()
                        self.getSkin(0)


        # Update player attributes
        def updatePlayerConstants(self):
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


        # ROCKET EXHAUST ANIMATION
        def updateExhaust(self,game):
            if self.exhaustState+1 > len(assets.spaceShipList[game.savedShipLevel]['exhaust']): self.exhaustState = 0
            else: self.exhaustState += 1


        # SKIN ANIMATION
        def updateAnimation(self):
            if self.animated:
                if self.skinAnimationCount >= settings.skinAnimationDelay:
                    if self.skinAnimationFrame + 1 > self.skinAnimationFrames: self.skinAnimationFrame = 0
                    else: self.skinAnimationFrame += 1
                    self.image = assets.spaceShipList[game.savedShipLevel]['skins'][self.currentImageNum][self.skinAnimationFrame]
                    self.skinAnimationCount = 0
                self.skinAnimationCount += 1


        # PLAYER EXPLOSION ANIMATION
        def explode(self,game,obstacles):
            while self.explosionState < len(assets.explosionList):
                height = assets.explosionList[self.explosionState].get_height()
                width = assets.explosionList[self.explosionState].get_width()
                screen.fill(screenColor)
                screen.blit(assets.bgList[game.currentStage - 1][0], (0,0) )
                game.showPlanet()
                game.showBackgroundCloud()
                if game.cave is not None:
                    screen.blit(game.cave.background,game.cave.rect)
                    screen.blit(game.cave.image,game.cave.rect) # Draw cave

                # Draw obstacles during explosion
                for obs in obstacles:
                    obs.move(self,None)
                    obs.activate()
                    newBlit = rotateImage(obs.image,obs.rect,obs.angle)
                    screen.blit(newBlit[0],newBlit[1])

                img = pygame.transform.scale(assets.explosionList[self.explosionState], (height * self.explosionState, width * self.explosionState)) # Blow up explosion
                img, imgRect = rotateImage(img, self.rect, self.lastAngle) # Rotate
                screen.blit(img,imgRect) # Draw explosion
                screen.blit(assets.explosionList[self.explosionState],self.rect)
                self.explosionState += 1
                self.finalImg,self.finalRect = img,imgRect # Explosion effect on game over screen
                displayUpdate(game.clk)


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



# OBSTACLES
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,playerPos,**kwargs):
        super().__init__()
        # Accept kwargs or default to level settings
        self.attributeIndex = None
        self.spawnPattern = kwargs.get('spawn', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSpawn"]))
        self.target = kwargs.get('target', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleTarget"]))
        self.movement = getMovement(self.spawnPattern)
        self.speed = int(kwargs.get('speed', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSpeed"])))
        self.size = int(kwargs.get('size', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSize"])))
        self.spinSpeed = int(kwargs.get('spin', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleSpin"])))
        self.health = int(kwargs.get('health', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleHealth"])))
        self.bounds = kwargs.get('bounds', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleBounds"]))
        self.laserType = kwargs.get('lasers', self.getAttributes(assets.stageList[game.currentStage-1][game.currentLevel-1]["obstacleLaserType"]))

        try: self.image = kwargs.get('image', self.getAttributes(assets.obstacleImages[game.currentStage - 1][game.currentLevel-1]))
        except: self.image = assets.obstacleImages[0][random.randint(0,len(assets.obstacleImages[0])-1)] # Not enough assets for this level yet

        self.image = pygame.transform.scale(self.image, (self.size, self.size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.getDirection(playerPos)
        self.angle = random.randint(0,360) # Image rotation
        self.spinDirection = random.choice([-1,1])
        self.active = False
        self.slowerDiagonal = settings.slowerDiagonalObstacles
        self.laserDelay, self.lasersShot, self.maxLasers = 0, 0, settings.maxObsLasers


    # For levels with multiple obstacle types
    def getAttributes(self,attribute):
        if type(attribute) == list:
            if self.attributeIndex is None: self.attributeIndex = random.randint(0,len(attribute)-1)
            if self.attributeIndex > len(attribute): return attribute[random.randint(0,len(attribute)-1)]
            return attribute[self.attributeIndex] # Treat as parallel lists
        else: return attribute


    # Get correct type representation of angle
    def getDirection(self,playerPos):
        if self.target == "NONE": self.direction = self.movement[1] # Get a string representation of the direction
        else: self.direction = math.atan2(playerPos[1] - self.rect.centery, playerPos[0] - self.rect.centerx) # Get angle representation


    # Call corresponding movement function
    def move(self,player,enemyLasers):
        if self.target == "NONE": self.basicMove()
        elif self.target == "LOCK": self.targetMove()
        elif self.target == "HOME": self.homingMove(player)
        if self.laserType != "NONE": self.shoot(player,enemyLasers)


    # BASIC MOVEMENT (8-direction) -> direction is a string
    def basicMove(self):
        if self.slowerDiagonal: # Use sqrt(2) for correct diagonal movement
            if self.direction == "N": self.rect.centery -= self.speed
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


    # HEAT SEEKING -> direction is an angle, updated every frame
    def homingMove(self,player):
        dirX = (player.rect.centerx - self.rect.centerx + settings.screenSize[0]/2) % settings.screenSize[0]-settings.screenSize[0]/2 # Shortest horizontal path
        dirY = (player.rect.centery - self.rect.centery + settings.screenSize[1]/2) % settings.screenSize[1]-settings.screenSize[1]/2 # Shortest vetical path
        self.direction = math.atan2(dirY,dirX) # Angle to shortest path
        self.angle = -math.degrees(self.direction)-90
        self.targetMove()


    # BOUNDARY HANDLING
    def bound(self,obstacles):
        if self.bounds == "KILL": # Remove obstacle
            if self.rect.left > settings.screenSize[0] + settings.spawnDistance or self.rect.right < -settings.spawnDistance:
                obstacles.remove(self)
                self.kill()
            elif self.rect.top > settings.screenSize[1] + settings.spawnDistance or self.rect.bottom < 0 - settings.spawnDistance:
                obstacles.remove(self)
                self.kill()

        elif self.bounds == "BOUNCE": # Bounce off walls
            if self.rect.left < 0:
                if self.target == "NONE": self.movementReverse()
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.left = 1

            elif self.rect.right > settings.screenSize[0]:
                if self.target == "NONE": self.movementReverse()
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.right = settings.screenSize[0] - 1

            elif self.rect.top < 0:
                if self.target == "NONE": self.movementReverse()
                else: self.direction = math.atan2(math.sin(self.direction + math.pi), math.cos(self.direction + math.pi))
                self.rect.top = 1

            elif self.rect.bottom > settings.screenSize[1]:
                if self.target == "NONE": self.movementReverse()
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
            if self.rect.right > 0 and self.rect.left < settings.screenSize[0] and self.rect.bottom > 0 and self.rect.top < settings.screenSize[1]: self.active = True


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


    # Shoot lasers
    def shoot(self,player,enemyLasers):
        if enemyLasers is not None:
            if self.lasersShot < self.maxLasers and self.laserDelay >= settings.obsLaserDelay:
                enemyLasers.add(EnemyLaser(self,player))
                self.lasersShot += 1
                self.laserDelay = 0
            else: self.laserDelay += 1



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


    # True if cave is covering screen
    def inside(self):
        if self.rect.top < 0 and self.rect.bottom > settings.screenSize[1]: return True
        else: return False


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
        angle = math.radians( (self.angle-90))
        velX = 1.414 * self.speed * math.cos(angle)
        velY = 1.414 * self.speed * math.sin(angle)
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
                    game.explosions.append(Explosion(self,None))
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
    def __init__(self, obs, player):
        super().__init__()
        self.speed = obs.speed * 1.5
        self.angle = obs.angle
        if type(self.angle) == str: self.angle = getAngle(self.angle)  # Convert to degrees
        self.laserType = obs.laserType
        newBlit = rotateImage(assets.enemyLaserImage, assets.enemyLaserImage.get_rect(center=obs.rect.center), self.angle)
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
    def homingMove(self,player):
        if self.seekWaitTime < settings.heatSeekDelay:
            self.seekWaitTime += 1
            self.normalMove()
        elif self.seek == False: self.target, self.seek = player, True # Get target
        else:
            if self.target is None:
                if settings.heatSeekNeedsTarget:
                    game.explosions.append(Explosion(self,None))
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



# EXPLOSIONS
class Explosion(pygame.sprite.Sprite):
    def __init__(self,point,increment):
        super().__init__()
        self.state,self.finalState,self.finished = 0,len(assets.explosionList)-1,False
        self.image = assets.explosionList[self.state]
        self.rect = self.image.get_rect(center = point.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.updateFrame = 0
        self.delay = settings.explosionDelay
        self.size = self.rect.size[0]
        if increment is None: self.increment = settings.explosionIncrement
        else: self.increment = increment


    def update(self):
        self.updateFrame +=1
        if self.updateFrame >= self.delay:
            self.updateFrame = 0
            if self.state +1 >= len(assets.explosionList): self.finished = True
            else:
                self.state +=1
                self.image = assets.explosionList[self.state]
                self.enlarge()
                self.mask = pygame.mask.from_surface(self.image)

        screen.blit(self.image,self.rect)


    # ENLARGE EXPLOSION
    def enlarge(self):
        if self.increment > 0:
            self.size += self.increment
            self.image = pygame.transform.scale(assets.explosionList[self.state], (self.size,self.size))
            self.rect = self.image.get_rect(center = self.rect.center)



# POWER UP SPAWNS
class Point(pygame.sprite.Sprite):
    def __init__(self,player,lastPos):
        super().__init__()
        self.powerUp = ''
        pointChoices = settings.powerUpList.copy()
        if not player or (not player.hasShields and player.boostDrain == 0 and player.laserCost == 0  and player.baseSpeed == player.boostSpeed): self.powerUp = "Default"
        else:
            powerUps = pointChoices
            if not player.hasShields and "Shield" in powerUps: del pointChoices["Shield"]
            if not player.hasGuns and player.baseSpeed == player.boostSpeed and "Fuel" in powerUps: del pointChoices["Fuel"]
            self.powerUp = random.choices(list(pointChoices.keys()),weights = list(pointChoices.values()) )[0]

        self.image = pygame.transform.scale(assets.pointsList[self.powerUp], (settings.pointSize, settings.pointSize)) # GET SCALED IMAGE / not ideal

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



# MENU ICONS
class Icon(pygame.sprite.Sprite):
    def __init__(self, iconType):
        super().__init__()
        self.iconType = iconType
        self.getNew()
        self.active = False


    def move(self):
        if "N" in self.direction: self.rect.centery -= self.speed
        if "S" in self.direction: self.rect.centery += self.speed
        if "E" in self.direction: self.rect.centerx += self.speed
        if "W" in self.direction: self.rect.centerx -= self.speed
        self.activate()

        if self.angle >= 360 or self.angle <= -360: self.angle = 0

        self.angle += self.spinDirection * random.uniform(settings.minIconRotationSpeed, settings.maxIconRotationSpeed)

        randomTimerUX = random.randint(settings.screenSize[0] * 2,settings.screenSize[0] * 4)
        randomTimerUY = random.randint(settings.screenSize[1] * 2,settings.screenSize[1] * 4)
        randomTimerLX = -1 * random.randint(settings.screenSize[0], settings.screenSize[0] * 3)
        randomTimerLY = -1 * random.randint(settings.screenSize[0], settings.screenSize[1] * 3)

        if self.active and ( (self.rect.centery > randomTimerUY) or (self.rect.centery < randomTimerLY) or (self.rect.centerx> randomTimerUX) or (self.rect.centerx < randomTimerLX) ):
            self.getNew()
            self.active = False


    def activate(self):
        if not self.active:
            if ("W" in self.direction and self.rect.right >= 0) or ("E" in self.direction and self.rect.left <= settings.screenSize[0]) or ("N" in self.direction and self.rect.top <= settings.screenSize[1]) or ("S" in self.direction and self.rect.bottom >= 0): self.active = True


    def draw(self):
        if self.active:
            drawing, drawee = rotateImage(self.image,self.rect,self.angle)
            screen.blit(drawing,drawee)


    def getNew(self):
        if self.iconType is None or self.iconType == "FG": self.getNewFg()
        elif self.iconType == "BG": self.getNewBg()
        elif self.iconType == "CG" or self.iconType == "COLLIDE": self.getNewCg()
        else: self.getNewFg() # Default


    # Get new foreground icon
    def getNewFg(self):
        spins = [-1,1]
        self.speed = random.randint(settings.minIconSpeed,settings.maxIconSpeed)
        self.movement = getMovement("LEFT")
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        if random.randint(0,10) < 7: self.image = assets.menuList[0]
        else: self.image = assets.menuList[random.randint(1,len(assets.menuList)-1)]
        size = random.randint(settings.minIconSize,settings.maxIconSize)
        self.image = pygame.transform.scale(self.image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = random.randint(0,360)


    # Get new background icon
    def getNewBg(self):
        self.speed = random.randint(5,15)
        self.movement = getMovement("LEFT")
        self.direction = self.movement[1]
        self.spinDirection = 1
        if random.randint(0,10) < 7: self.image = assets.menuList[0]
        else: self.image = assets.menuList[random.randint(1,len(assets.menuList)-1)]
        size = random.randint(5,15)
        self.image = pygame.transform.scale(self.image, (size, size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0


    # Get new colliding icon
    def getNewCg(self):
        spins = [-1,1]
        self.speed = random.randint(settings.minIconSpeed,settings.maxIconSpeed)
        self.movement = getMovement("LEFT")
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        size = random.randint(10,20)
        self.image = pygame.transform.scale(assets.menuList[random.randint(0,len(assets.menuList)-1)], (size, size)).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.mask = pygame.mask.from_surface(self.image)
        self.angle = random.randint(0,360)



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
        self.movement = getMovement(None)
        self.direction = self.movement[1]
        self.angle = getAngle(self.direction)
        self.text = text
        self.image = pygame.transform.scale(assets.donationShips[random.randint(0, len(assets.donationShips) - 1)], (self.size, self.size) ).convert_alpha()
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.font = pygame.font.Font(assets.gameFont, int(self.size * 2/3))
        self.display = self.font.render(self.text, True, [0,0,0])
        self.displayRect = self.display.get_rect(center = self.rect.center)
        self.active = False


    def move(self):
        if "N" in self.direction: self.rect.centery -= self.speed
        if "S" in self.direction: self.rect.centery += self.speed
        if "E" in self.direction: self.rect.centerx += self.speed
        if "W" in self.direction: self.rect.centerx -= self.speed
        self.displayRect.center = self.rect.center
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


    # GET SCALED VALUE
    def valueScaler(self, amount, minimum, maximum, bottom, top):
        if bottom is None or top is None: return minimum
        elif top - bottom == 0: return (maximum + minimum) / 2
        else:
            scaled = (amount - bottom) / (top - bottom) * (maximum - minimum) + minimum
            return int(min(max(scaled, minimum), maximum))



# INITIALIZE GAME
game = Game() # Initialize game
menu = Menu() # Initialize menus
settings.debug("Game started") # Debug


# START GAME LOOP
def gameLoop():

    game.resetGameConstants() # Reset level settings
    player = Player(game) # Initialize player
    if game.mainMenu:
        assets.loadMenuMusic()
        pygame.mixer.music.play(-1)
        if game.musicMuted: pygame.mixer.music.set_volume(0)
        menu.home(game,player)

    else:
        assets.loadSoundtrack()
        player.getSkin(game.savedSkin)
        pygame.mixer.music.play()

    if game.musicMuted: pygame.mixer.music.set_volume(0)

    events = Event() # Initialize events
    events.set(player) # Events manipulate player cooldowns
    lasers = pygame.sprite.Group() # Laser group
    enemyLasers = pygame.sprite.Group() # Enemy laser group
    obstacles = pygame.sprite.Group() # Obstacle group

    # GAME LOOP
    while True: game.update(player,obstacles,menu,events,lasers,enemyLasers)


if __name__ == '__main__': gameLoop()