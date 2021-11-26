# This file will store the level as it is being run
# This approach was inspired by: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s
import pygame
from Obstacles import *
from Block import Block

class Obstacle():
    def __init__(self, obsData, dispSurface, player):
        self.obType = obsData[0][0:-1] # Identifies the type of obstacle to determine loading next obstacle
        self.obLevel = obsData[0][-1] # Gets the height level of the obstacle being made
        self.displaySurface = dispSurface
        self.player = player # Used to decide where to spawn the blocks depending on the player if in multiplayer mode
        self.lastBlock = None # Will hold the last sprite of the top row of every obstacle for collision management
        self.drawCheck = None # For drawing player 1 obstacles in multiplayer mode
        self.mpObstacle = pygame.sprite.Group() # Used to store player 1 obstacle blocks that have not crossed the \
        # halfway mark in multiplayer mode
        self.obstacle = pygame.sprite.Group()
        self.createObstacle(obsData[1], player) # Makes the obstacle based on the data list it is given

    def createObstacle(self, obstacle, player):
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

                    # Getting x,y coordinates using obstacle list sizes

                    if player == 1: # Player 1 in multiplayer mode
                        self.drawCheck = False # Don't draw the block as soon as it's made
                        x = screen_width/2 + (colIndex * blockSize) # Make at the middle of the screen

                    elif player == 2 or player == 3: # Player 2 in multiplayer mode or Player 1 in single player mode
                        x = screen_width + (colIndex * blockSize) # Make at the end of the screen

                    y = (5*(screen_height/6)) - ((len(obstacle)-rowIndex)*(blockSize)) + (blockSize/2)
                    # Y position not affected by player designation or game mode 

                    obs = Block(x, y, image)

                    # Remember the last (top-right) block in an obstacle
                    if rowIndex == 0 and (colIndex == len(row)-1 or " " in obstacle[rowIndex][colIndex:]):
                        self.lastBlock = obs
                    if player == 1:
                        self.mpObstacle.add(obs) # Store blocks here for player 1 in multiplayer mode
                    else:
                        self.obstacle.add(obs) # Makes each component of an obsacle into a sprite and stores that in a group
    
    def update(self, screenWidth, screenHeight, player):
        if self.drawCheck == False:
            for block in self.mpObstacle:

                if block.x + (blockSize/2) < screen_width/2 - (blockSize/2): # When the block is beyond the halfway line
                    self.obstacle.add(block) # Put the block in self.obstacle
                    self.mpObstacle.remove(block) # Remove from the other group

            if len(self.mpObstacle) == 0: # If this group is empty
                self.drawCheck = True # No need to check this group anymore when updating
            
            self.mpObstacle.update(screenWidth, screenHeight)

        for block in self.obstacle:

            if player == 1 or player == 3: 
                # Always removes obstacle once it reaches the end of the screen for player 1
                if block.rect.left == 0: # Delete sprite once off screen
                    self.obstacle.remove(block)

            elif player == 2:
                if block.x - (blockSize/2) == screenWidth/2 - (blockSize/2): # Once the left of the block hits the middle of the screen
                    # Remove the block to keep obstacles from overlapping to player 1's side
                    self.obstacle.remove(block) 
                    
        self.obstacle.update(screenWidth, screenHeight)
    
    def run(self):
        self.obstacle.draw(self.displaySurface)

# All obstacle images cited from:
# https://geometry-dash.fandom.com/wiki/Level_Components