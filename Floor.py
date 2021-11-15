# This file manages the movement of the floor as a sprite
import pygame
from GameObject import  GameObject

class Floor(GameObject): # The player sprite(s)
    @staticmethod
    def init(screenWidth, screenHeight): # Loading the floor sprite image
        Floor.floorImage = pygame.transform.scale(pygame.image.load('Game_Floor.png').convert_alpha(),
            (screenWidth, screenHeight/4))

    def __init__(self, x, y):
        super(Floor, self).__init__(x, y, Floor.floorImage)

    def update(self, screenWidth, screenHeight):
        self.x -= self.vX
        
        super(Floor, self).update(screenWidth, screenHeight)
