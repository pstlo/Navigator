# Navigator
# Copyright (c) 2023 Mike Pistolesi
# All rights reserved

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import Settings
from Game import Game

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(Settings.numChannels)
pygame.display.set_caption('Navigator')

if Settings.fullScreen: screen = pygame.display.set_mode(Settings.screenSize,pygame.FULLSCREEN | pygame.SCALED, depth = 0)
else: screen = pygame.display.set_mode(Settings.screenSize, pygame.SCALED, depth = 0)

# LOADING SCREEN
loadingDisplay = pygame.font.SysFont("None", 30).render("Loading...", True, (0, 255, 0))
screen.blit(loadingDisplay, loadingDisplay.get_rect(midleft=(Settings.screenSize[0]/2 -30, Settings.screenSize[1]/2)))
pygame.display.update()

game = Game(screen) 

if __name__ == '__main__': game.start()