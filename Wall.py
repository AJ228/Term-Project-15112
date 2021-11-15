# This file manages the movement of the wall as a sprite
import pygame
from GameObject import  GameObject

class Wall(GameObject): # The moving wall sprite(s)
    @staticmethod
    def init(screenWidth, screenHeight): # Loading the player sprite image
        wallImage = pygame.image.load('Game_BG.png') # For moving background
        background = pygame.transform.scale(wallImage,(screenWidth,screenHeight))
        Wall.wallImage = background

    def __init__(self, x, y):
        super(Wall, self).__init__(x, y, Wall.wallImage)

    def update(self, screenWidth, screenHeight):
        self.x -= self.vX
        
        super(Wall, self).update(screenWidth, screenHeight)
#screen.blit(background, (i, 0))
#screen.blit(background, (self.width + i, 0))
#i -= 10
#if i == -self.width:
#    screen.blit(background, (self.width + i, 0)) 
#    i = 0