import sys,math,pygame

debugging = False # Default = False / show status messages

# DEBUGGING MESSAGES
def debug(text):
    if debugging:print(text)

screenSize = [800,800] # Default = [800,800]
screenColor = [0,0,0] # Screen fill color
fps = 60 # Default = 60
fullScreen = False # Default = False / start game in fullscreen
showFPS = False # Default = False / shows fps counter in window caption

# INPUT
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
debug("Loaded keybinds") # Debug

useController = True # Default = True / Allow controller input
cursorMode = True # Default = True / Allow cursor input
cursorFollowDistance = 15 # Default = 15 / Cursor follow deadzone
cursorRotateDistance = 5 # Default = 5 / Cursor rotate deadzone
cursorThickness = 2 # Default = 2

# HUD
showHUD = True
shieldColor = [0,0,255] # Default = [0,0,255] / Color of shield gauge / Blue
fullShieldColor = [0,255,255] # Default = [0,255,255] / Color of active shield gauge / Cyan
fuelColor = [255,0,0] # Default = [255,0,0] / Color of fuel gauge /  Red
timerDelay = 1000 # Default = 1000
pauseMax = 5 # Default = 5 / max pauses per game
nearMissIndicatorDuration = 1500 # Default = 1500 / visual duration of near miss indicator

# POWER UPS
spawnRange = [0.15, 0.85]
spawnVertices = 8 # Default = 8 / Vertices in shape of point spawn area (Octagon)
pointSize = 25  # Default = 25
shieldChunkSize = screenSize[0]/40 # Default = screen width / 40
nukeSize = 75 # Default = 75 / Nuke expansion rate
boostCooldownTime = 2000 # Default = 2000 / Activates when fuel runs out to allow regen
powerUpList = {"Default":55,"Shield":25, "Fuel":15, "Coin":1, "Nuke":4} # Default = {"Default":55,"Shield":20, "Fuel":15, "Coin":5, "Nuke":5} / power up odds
playerShieldSize = 48 # Default = 48 / Shield visual size
shieldVisualDuration = 250 # Default = 250 / Shield visual duration
minDistanceToPoint = (screenSize[0] + screenSize[1]) / 16 # Default = 100
maxRandomAttempts = 100 # Default = 100 / For random generator distances / max random attempts at finding a valid point

# BACKGROUND CLOUD
showBackgroundCloud = True # Default = True
cloudSpeed = 1 # Default = 1
cloudStart = -1000 # Default = -1000
cloudSpeedAdder = 0.5 # Default = 0.5 / cloud speed increment per level

# FONT COLORS
primaryFontColor = [0,255,0] # Default = [0,255,0] / Green
secondaryFontColor = [255,255,255] # Default = [255,255,255] / White

# START MENU
maxFgIcons = 1 # Default = 1 / foreground icons
maxBgIcons = 5 # Default = 5 / background icons
maxCgIcons = 1 # Default = 1 / colliding icons
minIconSpeed = 6 # Default = 6
maxIconSpeed = 12 # Default = 12
minIconRotationSpeed = 3 # Default = 3
maxIconRotationSpeed = 6 # Default = 6
minIconSize = 30 # Default = 30
maxIconSize = 100  # Default = 100
showVersion = True # show version info
showMenuIcons = True # show menu icons

# STAGE UP
stageUpCloudStartPos = -900 # Default = -900
stageUpCloudSpeed = 8  # Default = 8

# CREDITS
mainCreditsSpeed = 2 # Default = 2
extraCreditsSize = 30  # Default = 30 / background ships text size
maxExtras = 3 # Default = 3 / # max background ships
minBackgroundShipSpeed = 2 # Default = 2
maxBackgroundShipSpeed = 3 # Default = 3
minBackgroundShipSize = 50 # Default = 50
maxBackgroundShipSize = 100 # Default = 100
minBackgroundShipSpawnDelay = 500 # / Min delay (ms) before a ship spawns
maxBackgroundShipSpawnDelay = 3000 # / Max delay (ms) before a ship spawns
showBackgroundShips = True # Default = True
showSupporterNames = True # Default = True

# SOUNDS
musicVolume = 10 # Default = 10 / Music volume / 100
sfxVolume = 5 # Default = 5 / SFX volume / 100
numChannels = 16 # Default = 16
musicMuted = False # Default = False

# PLAYER
resetPlayerOrientation = True # Default = True / reset orientation if player is not moving
drawExhaust = True # Default = True / draw exhaust animation
exhaustUpdateDelay = 50 # Default = 50 / Delay (ms) between exhaust animation frames
defaultToHighSkin = True # Default = True / Default to highest skin unlocked on game launch
defaultToHighShip = False # Default = False / Default to highest ship unlocked on game launch
heatSeekDelay = 15 # Default = 15 / time before projectile starts homing
heatSeekNeedsTarget = False # Default = False / projectile will explode if target not found
skinAnimationDelay = 5 # Default = 5 / Delay between skin animation frame updates

# LEVELS
levelUpCloudSpeed = 25 # Default = 25 / Only affects levels preceded by wipe

# PLANETS
planetMoveDelay = 2 # Default = 2
unlimitedPlanets = True # Temporary until more planets added

# OBSTACLES
slowerDiagonalObstacles = True # Default = True / use the hypotenuse or whatever
spawnDistance = 0 # Default = 0 / Distance past screen border required before new obstacle spawned
obsLaserDelay = 10 # Default = 10 / delay before obstacle fires another laser
obsLaserDamage = 1 # Default = 1
maxObsLasers = 3 # Default = 3 / lasers per obstacle

# EXPLOSIONS
explosionIncrement = 0 # Default = 0 / explosion expansion rate
explosionDelay = 2 # Default = 2 / delay between explosion frame updates

# NEAR MISSES
nearMisses = True # Default = True / register near misses
nearMissDist = 40 # Default = 40 / distance for near miss start
nearMissSafeDist = 60 # Default = 60 distance for near miss end
nearMissValue = 0 # Default = 0 / point value for near misses

# CAVES
caveStartPos = screenSize[1]*-2 # Default = -1600 / Cave start Y coordinate
caveSpeed = 20 # Default = 20 / Cave flyby speed

# SAVING
encryptGameRecords = True # Default = True / Hide game records from user to prevent manual unlocks
invalidKeyMessage = "Invalid key, could not save records." # Saved to game records file if settings.encryptGameRecords == True and key is invalid

# LEADERBOARD
connectToLeaderboard = True # Default = True
leaderboardSize = 10 # Number of players shown on leaderboard

# EXPERIMENTAL
rawCursorMode = False # Default = False / sets player position to cursor position
cythonMode = False # Default = False / -> use ../../Navigator instead of . for path

# DISCORD
showPresence = True # Default = True / Discord presence using pypresence

# TESTING
useArgs = True # Default = False / accept command line args
devMode = False # Default = False
showSpawnArea = False # Default = False / show powerup spawn area
showCursorPath = False # Default = False / Draw line from cursor to ship


# ARGS
if useArgs:
    arguments = sys.argv[1:]
    for arg in arguments: arg = arg.lower()
else: arguments = None

# APPLY ARGS
if arguments is not None:
    if "debug" in arguments: debugging = True
    if "devmode" in arguments: devMode = True

# CONTROLLER BINDS
controllerBinds = {
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


runningFromExe = hasattr(sys,'_MEIPASS') # Specify if running from EXE/app or Python script
if runningFromExe: debug("Running from executable") # Debug
else: debug("Running from Python script") # Debug
debug("Loaded settings") # Debug


