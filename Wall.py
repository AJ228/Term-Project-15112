# This file manages the movement of the wall (background) as a sprite
import pygame
from GameObject import  GameObject

class Wall(GameObject): # The moving wall sprite(s)
    @staticmethod
    def init(screenWidth, screenHeight): # Loading the wall sprite image
        wallImage = pygame.image.load('Game_BG.png').convert_alpha() # For moving background
        background = pygame.transform.scale(wallImage,(screenWidth,screenHeight))
        Wall.wallImage = background

    def __init__(self, x, y):
        super(Wall, self).__init__(x, y, Wall.wallImage)

    def update(self, screenWidth, screenHeight): # Moves the background image
        self.x -= self.vX
        
        super(Wall, self).update(screenWidth, screenHeight)
