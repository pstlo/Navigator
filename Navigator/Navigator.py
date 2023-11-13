# Navigator
# Copyright (c) 2023 Mike Pistolesi
# All rights reserved

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

import Settings
from Game import Game
from Assets import Assets
from Menu import Menu
from Gamepad import Gamepad

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(Settings.numChannels)
pygame.display.set_caption('Navigator')

if Settings.fullScreen: screen = pygame.display.set_mode(Settings.screenSize,pygame.FULLSCREEN | pygame.SCALED, depth = 0)
else: screen = pygame.display.set_mode(Settings.screenSize, pygame.SCALED, depth = 0)

# LOADING SCREEN
loadingDisplay = pygame.font.SysFont("None", 30).render("Loading...", True, (0, 255, 0))
screen.blit(loadingDisplay, loadingDisplay.get_rect(midleft=(370, 400)))
pygame.display.update()

# CURSOR
curSurf = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.line(curSurf, (0, 255, 0), (10, 20), (30, 20), Settings.cursorThickness)
pygame.draw.line(curSurf, (0, 255, 0), (20, 10), (20, 30), Settings.cursorThickness)
cursor = pygame.cursors.Cursor((20, 20), curSurf)
pygame.mouse.set_cursor(cursor)
pygame.mouse.set_visible(Settings.cursorMode)
Settings.debug("Initialized cursor") # Debug

assets = Assets()
gamePad = Gamepad()
menu = Menu() 
game = Game(assets,screen,gamePad) 
Settings.debug("Game started") # Debug


if __name__ == '__main__': game.gameLoop()