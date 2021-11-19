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
        self.angle = 0
        self.startY = self.y # Stores height the character is at before jumping (currently static y value)
        self.turnAngle = 5 # Following attributes help with airborne movement
        self.jumpHeight = 0
        self.jumped = False

    def applyGravity(self): # Used when player sprite is falling
        self.y += self.vY
        self.rect.y += self.vY


    def update(self, keysDown, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)

        if keysDown(pygame.K_SPACE) and self.y == self.startY: # Allows jumping only when not in mid-air
            self.jump()

        if self.jumped == True:
            self.jumpHeight += self.vY

            if self.jumpHeight == 70: # There is only one type of jump so change height that way
                self.jumped = False

        elif self.jumped == False and self.y != self.startY:
            self.applyGravity()  # Descending while midair
            self.jumpHeight -= self.vY  

        if self.y != self.startY:
            self.angle -= self.turnAngle # Makes the player sprite rotate when mid-air

        elif self.y == self.startY and self.angle % 90 != 0:
            self.angle -= (self.angle % 90) # Makes sure player always lands on a flat surface

        self.y = self.startY - self.jumpHeight # This is temporary until I implement collision detection
                                               # between player and floor sprites

        super(Player, self).update(screenWidth, screenHeight)
    
    def jump(self):
        self.jumped = True