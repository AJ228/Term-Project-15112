import pygame

# GameObject will be used for character and obstacle sprites that will appear in the game
# They operate similarly
# Class structure inspired from:
# https://qwewy.gitbooks.io/pygame-module-manual/content/tutorials/using-sprites/making-a-game-with-sprites.html

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image): # x, y represent center coordinates of sprites
        super(GameObject, self).__init__()
        self.x, self.y, self.image = x, y, image
        self.baseImage = image.copy() # Character sprite will be rotated in jumps so this is needed
        w, h = image.get_size()
        self.updateRect()
        self.vX = 5
        self.vY = 10

    def updateRect(self): # Updating the sprite's rectangle object
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)    

    def update(self, screenWidth, screenHeight):
        if self.rect.left > screenWidth: # Updates rectangle position if it crosses screen boundaries
            self.x -= screenWidth + self.width
            
        elif self.rect.right < 0: # Wrap around in the horizontal direction
            self.x += screenWidth + self.width
            
        if self.rect.top > screenHeight: # Wrap around in the vertical direction
            self.y -= screenHeight + self.height
            
        elif self.rect.bottom < 0: # When it crosses the top
            self.y += screenHeight + self.height # Start from the bottom and keep going up (wrap around)
            
        self.updateRect() # Always update the rectangle after any movement is made