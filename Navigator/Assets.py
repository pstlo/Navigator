import Settings as settings
import os,sys,platform,json,base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import pygame
import Presence

# ASSETS
class Assets:
    def __init__(self):
        self.version = "v0.5.0"
        assetDirectory = self.resources('Assets') # ASSET DIRECTORY
        envPath = os.path.join(assetDirectory,'.env')

        # RECORD AND PREFERENCE PATHS
        if platform.system().lower() == 'windows':
            settings.debug("OS: Windows") # DEBUG

            # SAVE TO APPDATA
            navPath = os.path.join(os.getenv('LOCALAPPDATA'),'Navigator')

            if not os.path.exists(navPath):
                settings.debug("Directory not found. Attempting to create " + navPath)
                os.mkdir(navPath)

                if os.path.exists(envPath): os.rename(envPath,os.path.join(navPath,'.env'))
                settings.debug("Successfully created directory") # DEBUG

            # MOVE ENV TO APPDATA
            newEnvPath = os.path.join(navPath,'.env')
            if os.path.exists(envPath) and not os.path.exists(newEnvPath):
                os.rename(envPath,newEnvPath)
                settings.debug("Moved ENV to APPDATA") # DEBUG

            envPath = newEnvPath
            self.recordsPath, self.preferencesPath = os.path.join(navPath,'Records'), os.path.join(navPath,'Preferences')

        elif platform.system().lower() == 'linux':
            settings.debug("OS: Linux") # DEBUG
            self.recordsPath,self.preferencesPath = './gameRecords.txt','./gamePreferences.txt'  # For windows and linux
        else:
            settings.debug("OS: Mac") # DEBUG
            self.recordsPath,self.preferencesPath = self.resources('gameRecords.txt'), self.resources('gamePreferences.txt') # For MacOS

        # ASSET PATHS
        load_dotenv(envPath) # LOAD ENV VARS
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
        self.soundDirectory = os.path.join(assetDirectory, 'Sounds') # Sound assets directory / will be referenced again for music loading

        self.windowIcon = pygame.image.load(self.resources(os.path.join(assetDirectory,'Icon.png'))).convert_alpha()
        self.stageCloudImg = pygame.image.load(self.resources(os.path.join(assetDirectory,'StageCloud.png') ) ).convert_alpha() # STAGE WIPE CLOUD

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
        self.planetSizes = [400,500] # Planet sizes for corresponding index
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
        self.presence = Presence.start()


    # EXE/APP RESOURCES
    def resources(self,relative):
        try: base = sys._MEIPASS # Running from EXE/APP
        except: base = os.path.abspath(".") # Running fron script
        settings.debug("Joining " + base + " with " + relative)
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