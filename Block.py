# Stores all block objects, used to generate obstacles and platforms.
# Idea inspired from: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s

import pygame
from GameObject import GameObject # Obstacle movement on the path will be similar to the floor

class Block(GameObject):
    def __init__(self, x, y, image):
        super(Block, self).__init__(x, y, image)
        self.vY = 20 # Obstacles will either fall from the sky or rise from the ground
        self.placed = False # Flag to tell obstacle block when to stop rising/falling

    def update(self, screenWidth, screenHeight):
        if self.rect.right != 0:
            self.x -= self.vX
        
        super(Block, self).updateRect() # No wrap around required for these objects
# Using update messed up how the obstacles were spawning because some blocks wrapped around when they should not
