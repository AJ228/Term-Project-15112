# This file manages the movement of the player character 
import pygame
from GameObject import  GameObject

class Player(GameObject): # The player sprite(s) class is a subclass of GameObject
    @staticmethod # Method considered as a member of the object but is accessible directly from the constructor
    def init(): # Loading the player sprite image
        Player.charImage = pygame.transform.scale(pygame.image.load('GeodashChar2.png').convert_alpha(),
            (40, 40))

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, Player.charImage)
        self.vY = 9
        self.angle = 0
        self.startY = self.y # Stores height the character is at before jumping (currently static y value)
        self.falling = False
        self.turnAngle = 7 # Following attributes help with airborne movement
        self.jumpHeight = 0
        self.jumped = False
        self.floorCollision = False # Flags to check collisions
        self.obCollision = False

    def applyGravity(self): # Used when player sprite is falling
        self.startY += self.vY
        self.rect.y += self.vY


    def update(self, keysDown, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)

        if keysDown(pygame.K_SPACE) and self.y == self.startY and self.falling == False: # Allows jumping only when not in mid-air
            self.jumped = True
            self.falling = False
            self.floorCollision = False
            self.obCollision = False

        if self.jumped == True or self.falling == True:
            self.angle -= self.turnAngle # Makes the player sprite rotate when mid-air

        if self.jumped == True:
            self.jumpHeight += self.vY

            if self.jumpHeight == 90: # There is only one type of jump so change height that way
                self.jumped = False  

        if self.jumpHeight != 0 and self.jumped == False:
            self.jumpHeight -= self.vY 

        if (self.floorCollision == False and self.obCollision == False) and self.jumped == False:
            # Makes sure the player falls when not touching the floor or an obstacle
            self.falling = True
        else:
            self.falling = False

        if self.falling == True:
            self.applyGravity()  # Descending while midair


        if self.y == self.startY and self.angle % 90 != 0:
            self.angle -= (self.angle % 90) # Makes sure player always lands with a flat surface

        self.y = self.startY - self.jumpHeight 

        super(Player, self).update(screenWidth, screenHeight)
    