import pygame
from GameObject import  GameObject

class Player(GameObject): # The player sprite(s)
    @staticmethod
    def init(): # Loading the player sprite image
        Player.charImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('GeodashChar.png').convert_alpha(),
            (40, 40)), 0)

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, Player.charImage)
        self.angle = 0
        self.startY = self.y # Stores height the character is at before jumping
        self.turnAngle = 5
        self.jumpHeight = 0
        self.jumped = False

    def update(self, keysDown, screenWidth, screenHeight):
        self.image = pygame.transform.rotate(self.baseImage, self.angle)
        self.x += self.vX

        if keysDown(pygame.K_SPACE) and self.y == self.startY:
            self.jump()

        if self.jumped == True:
            self.jumpHeight += self.vY

            if self.jumpHeight == 70:
                self.jumped = False

        elif self.jumped == False and self.y != self.startY:
            self.jumpHeight -= self.vY    

        if self.y != self.startY:
            self.angle -= self.turnAngle

        elif self.y == self.startY and self.angle % 90 != 0:
            self.angle -= (self.angle % 90)

        self.y = self.startY - self.jumpHeight

        super(Player, self).update(screenWidth, screenHeight)
    
    def jump(self):
        self.jumped = True
            


