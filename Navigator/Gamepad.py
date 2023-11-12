import Settings as settings
import pygame

class Gamepad:
    def __init__(self):

        # CONTROLLER INPUT
        self.gamePad = None
        compatibleController = False
        if settings.useController:
            pygame.joystick.init()
            settings.debug("Initialized controller module") # Debug
            if pygame.joystick.get_count() > 0:
                gamePad = pygame.joystick.Joystick(0)
                gamePad.init()        
                settings.debug(str(gamePad.get_name()) + " detected, checking for compatibility") # Debug
                for controllerType in settings.controllerBinds:
                    if gamePad.get_name() in settings.controllerBinds[controllerType]['name']:
                        self.controllerMoveX = settings.controllerBinds[controllerType]['moveX']
                        self.controllerMoveY = settings.controllerBinds[controllerType]['moveY']
                        self.controllerRotateX = settings.controllerBinds[controllerType]['rotX']
                        self.controllerRotateY = settings.controllerBinds[controllerType]['rotY']
                        self.controllerBoost = settings.controllerBinds[controllerType]['boost']
                        self.controllerShoot = settings.controllerBinds[controllerType]['shoot']
                        self.controllerNextShip = settings.controllerBinds[controllerType]['nextShip']
                        self.controllerLastShip = settings.controllerBinds[controllerType]['lastShip']
                        self.controllerNextSkin = settings.controllerBinds[controllerType]['nextSkin']
                        self.controllerLastSkin = settings.controllerBinds[controllerType]['lastSkin']
                        self.controllerSelect = settings.controllerBinds[controllerType]['select']
                        self.controllerBack = settings.controllerBinds[controllerType]['back']
                        self.controllerMute = settings.controllerBinds[controllerType]['mute']
                        self.controllerExit = settings.controllerBinds[controllerType]['exit']
                        self.controllerPause = settings.controllerBinds[controllerType]['pause']
                        self.controllerMenu = settings.controllerBinds[controllerType]['menu']
                        self.controllerFullScreen = settings.controllerBinds[controllerType]['settings.fullScreen']
                        self.controllerCredits = settings.controllerBinds[controllerType]['credits']
                        compatibleController = True
                        settings.debug("Compatible controller found, loaded corresponding binds") # Debug
                        break

                # Incompatible controller
                if not compatibleController:
                    settings.debug("Incompatible controller") # Debug
                    pygame.joystick.quit()
                    settings.debug("Uninitialized controller module") # Debug
                    if settings.useController: settings.useController = False
                    self.gamePad = None

            else:
                settings.debug("Controller not found") # Debug
                pygame.joystick.quit()
                settings.debug("Uninitialized controller module") # Debug
                if settings.useController: settings.useController = False
                self.gamePad = None
