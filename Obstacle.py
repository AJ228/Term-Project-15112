# This file will store the level as it is being run
# This approach was inspired by: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s
import pygame
from Obstacles import *
from Block import Block

class Obstacle():
    def __init__(self, obsData, dispSurface):
        self.obType = obsData[0][0:-1] # Identifies the type of obstacle to determine loading next obstacle
        self.obLevel = obsData[0][-1] # Gets the height level of the obstacle being made
        self.displaySurface = dispSurface
        self.createObstacle(obsData[1]) # Makes the obstacle based on the data list it is given

    def createObstacle(self, obstacle):
        self.obstacle = pygame.sprite.Group()
        for rowIndex, row in enumerate(obstacle): # Returns the index and sprite image letter stored at that index
            for colIndex, col in enumerate(row): # Enumerate helps me see the exact position of each block in the data list
                #print(f"{rowIndex},{colIndex}:{col}") # Identifies exact position of string being read
                if col != " ": #Ensures no block object is made for a blank space
                    if col == "P": # Make a platform
                        if colIndex == 0 or "P" not in obstacle[rowIndex][0:colIndex]: # Choose which platform image to use
                            image = "LeftPlatform.png"
                        elif colIndex == len(row)-1 or "P" not in obstacle[rowIndex][colIndex:]:
                            image = "RightPlatform.png"
                        else:
                            image = "MidPlatform.png"
                        image =  pygame.transform.scale(pygame.image.load(image).convert_alpha(),(blockSize,blockSize/2))

                    elif col == "B": # Choose which block image to use
                        if colIndex == 0 or "B" not in obstacle[rowIndex][0:colIndex]: 
                            image = "TopLeftPlatBlock.png"
                        elif rowIndex == 0:
                            if colIndex == len(row)-1 or "B" not in obstacle[rowIndex][colIndex:]:
                                image = "TopRightPlatBlock.png"
                            else:
                                image = "TopMidPlatBlock.png"
                        else:
                            image = "MidPlatBlock.png"
                        image =  pygame.transform.scale(pygame.image.load(image).convert_alpha(),(blockSize,blockSize))
                    
                    elif col == "O": # Making towers and choosing correct tower image
                        if rowIndex == 0: # Top of tower
                            image = "TowerTop.png"
                        else: # Base of tower
                            image = "TowerBase.png"
                        image =  pygame.transform.scale(pygame.image.load(image).convert_alpha(),(blockSize,blockSize))

                    elif col == "4": # Making square-type platforms:
                        image = "Four_Borders.png"
                        image =  pygame.transform.scale(pygame.image.load(image).convert_alpha(),(blockSize,blockSize))
                    
                    elif col == "S": # Making spikes
                        image = "Spike.png"
                        image =  pygame.transform.scale(pygame.image.load(image).convert_alpha(),(blockSize,blockSize))
                    
                    elif col == "T": # Making thorn pits
                        image = "FlatTPit.png" # Thorn pit has same dimensions as platforms
                        image =  pygame.transform.scale(pygame.image.load(image).convert_alpha(),(blockSize,blockSize/2))

                    x = screen_width + (colIndex * blockSize) # Getting x,y coordinates using obstacle list sizes
                    y = (5*(screen_height/6)) - ((len(obstacle)-rowIndex)*(blockSize)) 
                    obs = Block(x, y, image)
                    self.obstacle.add(obs)
    
    def update(self, screenWidth, screenHeight):
        for block in self.obstacle:
            if block.rect.right == 0: # Delete sprite once off screen
                self.obstacle.remove(block)
        self.obstacle.update(screenWidth, screenHeight)
    
    def run(self):
        self.obstacle.draw(self.displaySurface)

# All obstacle images cited from:
# https://geometry-dash.fandom.com/wiki/Level_Components