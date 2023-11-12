import pygame
import Settings as settings

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
    def muteEvent(self,game,event):
        # TOGGLE MUTE
        if ((event.type == pygame.KEYDOWN) and (event.key in settings.muteInput)) or (game.gamePad is not None and game.gamePad.get_button(game.controller.controllerMute) == 1): game.toggleMusic()