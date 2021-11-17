# Stores all block objects, used to generate obstacles and platforms.
# Idea inspired from: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s

import pygame
from GameObject import GameObject # Obstacle movement on the path will be similar to the floor

class Block(GameObject):
    def __init__(self, x, y, image):
        super(Block, self).__init__(x, y, image)

    def update(self, screenWidth, screenHeight):
        self.x -= self.vX
        
        super(Block, self).update(screenWidth, screenHeight)
