import pygame

import Settings as settings

# EXPLOSIONS
class Explosion(pygame.sprite.Sprite):
    def __init__(self,game,point,increment):
        super().__init__()
        self.state,self.finalState,self.finished = 0,len(game.assets.explosionList)-1,False
        self.image = game.assets.explosionList[self.state]
        self.rect = self.image.get_rect(center = point.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.updateFrame = 0
        self.delay = settings.explosionDelay
        self.size = self.rect.size[0]
        if increment is None: self.increment = settings.explosionIncrement
        else: self.increment = increment


    def update(self,game):
        self.updateFrame +=1
        if self.updateFrame >= self.delay:
            self.updateFrame = 0
            if self.state +1 >= len(game.assets.explosionList): self.finished = True
            else:
                self.state +=1
                self.image = game.assets.explosionList[self.state]
                self.enlarge(game)
                self.mask = pygame.mask.from_surface(self.image)

        game.screen.blit(self.image,self.rect)


    # ENLARGE EXPLOSION
    def enlarge(self,game):
        if self.increment > 0:
            self.size += self.increment
            self.image = pygame.transform.scale(game.assets.explosionList[self.state], (self.size,self.size))
            self.rect = self.image.get_rect(center = self.rect.center)
