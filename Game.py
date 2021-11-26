# This file runs the game using the pygamegame.py framework file
import pygame
import random
from pygame import mixer
from pygamegame import PygameGame
from GameObject import GameObject
from Button import Button
from Player import Player
from Wall import Wall
from Floor import Floor
from Obstacle import Obstacle
from Obstacles import *

class Game(PygameGame):

    def init(self, screen):

        Player.init() 
        self.charGroup = pygame.sprite.Group(Player(self.width/12, 3*(self.height/4), False))
        # Grouped character sprites together (grouped because there can be multiple players)

        Wall.init(self.width, self.height)
        self.wallGroup = pygame.sprite.Group(Wall(0, self.height/2))
        self.wallGroup.add(Wall(self.width, self.height/2)) # Allows for wall to wrap around

        Floor.init(self.width, self.height)
        self.floorGroup = pygame.sprite.Group(Floor(0, 11*(self.height/12)))
        self.floorGroup.add(Floor(self.width, 11*(self.height/12)))
        # Allows floor to wrap around
        
        self.obsGroup = [] # For obstacle spawning
        self.last = 0

        obstacle = random.choice([steps2, steps3, tower1, blockPlat1]) # Start round with an obstacle

        # Make according changes to game on start-up based on mode (single player or multiplayer)

        if self.multiplayer == True:
            self.charGroup.add(Player(7*(self.width/12),3*(self.height/4), True)) # Makes a second player
            self.obsGroup2 = [] # Makes a second set of obstacles (will be identical to player 1's) for player 2
            # Add obstacles to both groups if in multiplayer mode
            self.obsGroup.append(Obstacle(obstacle, screen, 1))
            self.obsGroup2.append(Obstacle(obstacle, screen, 2))
            self.scores = [0, 0] # Have self.scores change for multiplayer
            mixer.music.load("Multiplayer_level.mp3")
            mixer.music.play(-1)

        else:
            self.obsGroup.append(Obstacle(obstacle, screen, 3))
            mixer.music.load("Singleplayer_level.mp3")
            mixer.music.play(-1) # Ensures music runs infinitely

        self.last += 0 # Does not increase since this would create an index error
    

    def manageCollisions(self, player, obsGroup, mode): # Manage player collisions with a specific obstacle group
        for obs in obsGroup: # Checks obstacle objects in relevant obstacle group
            for block in obs.obstacle: # Checks each block sprite for every obstacle object
                if block.rect.colliderect(player.rect):
                    if player.x + (blockSize/2) == block.x - 10:
                        if player.y + (blockSize/2) > block.y - 15: # Makes sure player is below top edge
                            player.killed = True # Kills player from any horizontal collision and ends game
                            self.killCount += 1 # Add 1 to the kill count if character is killed
                    
                    elif player.startY + (blockSize/2) >= block.rect.y - (blockSize/2): 
                        # Allows vertical collisions with bottom of player
                        if obs.obType == "Hazard": # Kill if player lands on a hazard 
                            player.killed = True
                            self.killCount += 1 # Add 1 to the kill count if character is killed
                        else:
                            player.obCollision = True
                            player.floorCollision = False
                            player.jumpHeight = 0
                            player.startY = block.rect.y - (blockSize/2)
                    
                    if player.y - (blockSize/2) >= block.rect.top:
                        # Not with top of player for overhead obstacles 
                        player.killed = True
                        self.killCount += 1 # Add 1 to the kill count if character is killed
                    

                elif block == obs.lastBlock: # If the block is the last one in the obstacle
                    if player.x - (blockSize/2) >= block.rect.right: # Allows player to fall off obstacle
                        if player.x - (blockSize/2) <= block.rect.right + 5:
                            player.obCollision = False

            obs.update(self.width, self.height, mode)

            if len(obs.obstacle) == 0 and (obs.drawCheck == None or obs.drawCheck == True): # If current sprite group (obstacle object) in list has no sprites left
                obsGroup.remove(obs) # Delete sprite group from obstacle list
            
            if len(obsGroup) > 1:
                self.last = -1 # Makes sure there will be no indexing issues and group sizes remain consistent

    def timerFired(self, dt, screen): # Works much like graphics timerFired
        self.blips += 1
        
        if self.gameOver != True: # Only update the screen if the game is not over

            self.wallGroup.update(self.width, self.height)
            self.floorGroup.update(self.width, self.height)
            self.charGroup.update(self.isKeyPressed, self.width, self.height)

            if self.killCount == len(self.charGroup):
                self.gameOver = True

            for player in self.charGroup: # Manage collisions with obstacles and players

                # Decide which obstacle group to check for collisions depending on player and game modes

                if self.multiplayer == True:
                    if player.player2 == False: 
                        obsGroup = self.obsGroup
                        mode = 1 # Setting modes for updating obstacles

                    elif player.player2 == True:
                        obsGroup = self.obsGroup2
                        mode = 2

                else:
                    obsGroup = self.obsGroup
                    mode = 3

                self.manageCollisions(player,obsGroup,mode)

                if self.blips % 30 == 0 and player.killed == False: # Increase player score every half second they survive
                    player.score += 5
                    if player.player2 == False: # Update self.scores array
                        self.scores[0] = player.score

                    elif player.player2 == True:
                        self.scores[1] = player.score

                for floor in self.floorGroup: # Managing collisions between player and floor
                    if floor.rect.colliderect(player.rect):
                        player.obCollision = False
                        player.floorCollision = True
                        player.jumpHeight = 0
                        player.startY = floor.rect.y - (blockSize/2)

            if self.obsGroup[self.last].obType == "Tower": # Changes spawning timer based on obstacle type
                self.spawnDelay = self.towerDelay
                            
            elif self.obsGroup[self.last].obType == "Blocks":
                self.spawnDelay = self.blocksDelay
                
            elif self.obsGroup[self.last].obType == "Hazard":
                self.spawnDelay = self.hazardDelay   

            elif self.obsGroup[self.last].obType == "Steps":
                self.spawnDelay = self.stepDelay
                
            elif self.obsGroup[self.last].obType == "Platform":
                self.spawnDelay = self.platformDelay
            
            elif self.obsGroup[self.last].obType == "Block":
                self.spawnDelay = self.blockDelay
            
            else:
                self.spawnDelay = self.levelDelay

            if self.blips % self.spawnDelay == 0:
                # Add a new obstacle based on spawnDelay
                
                # Choose obstacles from specific sets based on latest obstacle level and type

                if self.obsGroup[self.last].obLevel == "1": 
                    if self.obsGroup[self.last].obType == "Block":
                        obstacle = random.choice([blockPlat1, blockPlat2, block1, block2, tower1, tower2, platform2])

                    elif self.obsGroup[self.last].obType == "Hazard":
                        obstacle = random.choice([spike, blockPlat1, block1, tower1])

                    elif self.obsGroup[self.last].obType == "Blocks":
                        obstacle = random.choice([block1, block2, platform2])

                    elif self.obsGroup[self.last].obType == "Tower":
                        obstacle = random.choice([tower1, tower2, blockPlat2, platform2])

                    elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                        obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle
                        
                elif self.obsGroup[self.last].obLevel == "2":
                    if self.obsGroup[self.last].obType == "Block":
                        obstacle = random.choice([blockPlat1, blockPlat2, blockPlat3, tower2, tower3, platform2, platform3])

                    elif self.obsGroup[self.last].obType == "Blocks":
                        obstacle = random.choice([platform2, platform3, block1, block2, block3])

                    elif self.obsGroup[self.last].obType == "Platform":
                        obstacle = random.choice([platform2, platform3, blockPlat2, blockPlat3, block1, block2, block3])

                    elif self.obsGroup[self.last].obType == "Tower":
                        obstacle = random.choice([tower1, tower2, tower3, blockPlat2, blockPlat3]) 

                    elif self.obsGroup[self.last].obType == "Steps":
                        obstacle = random.choice([platform2, platform3, blockPlat2, blockPlat3, block2, block3])

                    elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                        obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle 

                elif self.obsGroup[self.last].obLevel == "3":
                    if self.obsGroup[self.last].obType == "Block":
                        obstacle = random.choice([blockPlat2, blockPlat3, blockPlat4, tower3, tower4, platform3, platform4])

                    elif self.obsGroup[self.last].obType == "Blocks":
                        obstacle = random.choice([platform2, platform3, platform4, block2, block3, block4])

                    elif self.obsGroup[self.last].obType == "Platform":
                        obstacle = random.choice([platform2, platform3, platform4, blockPlat3, blockPlat4, block2,\
                            block3, block4])

                    elif self.obsGroup[self.last].obType == "Tower":
                        obstacle = random.choice([tower2, tower3, tower4, blockPlat2, blockPlat3, blockPlat4]) 

                    elif self.obsGroup[self.last].obType == "Steps":
                        obstacle = random.choice([platform3, platform4, blockPlat3, blockPlat4, block2, block3, block4])

                    elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                        obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle

                elif self.obsGroup[self.last].obLevel == "4":
                    if self.obsGroup[self.last].obType == "Block":
                        obstacle = random.choice([blockPlat3, blockPlat4, blockPlat5, tower3, tower4, platform4])

                    elif self.obsGroup[self.last].obType == "Blocks":
                        obstacle = random.choice([platform2 ,platform3, platform4, block3, block4])

                    elif self.obsGroup[self.last].obType == "Platform":
                        obstacle = random.choice([platform3, platform4, blockPlat3, blockPlat4, blockPlat5, block2,\
                            block3, block4])

                    elif self.obsGroup[self.last].obType == "Tower":
                        obstacle = random.choice([tower3, tower4, blockPlat3, blockPlat4, blockPlat5]) 

                    elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                        obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle

                elif self.obsGroup[self.last].obLevel == "5": # Only one type of level 5 obstacle so no need to split
                    obstacle = random.choice([tower4, blockPlat3, blockPlat4, blockPlat5, block3, block4, platform3,\
                        platform4])

                else: # For level 0 (floor-level) obstacles
                    obstacle = random.choice([steps2, steps3, blockPlat1, block1, tower1]) 

                if self.multiplayer == True: # Add obstacles based on game mode and player
                    self.obsGroup.append(Obstacle(obstacle, screen, 1))
                    self.obsGroup2.append(Obstacle(obstacle, screen, 2))

                else:
                    self.obsGroup.append(Obstacle(obstacle, screen, 3))

                self.last += 1
                self.blips = 1 # Resets timer so that obstacle spawning times are consistent with their delays
        else:
            pygame.mixer.music.stop() # Stop music once game ends

    def redrawAll(self, screen): # Works much like graphics redrawAll
        self.wallGroup.draw(screen)
        self.floorGroup.draw(screen)
        self.charGroup.draw(screen)
        for obs in self.obsGroup: # Draw obstacles for player 1
            # No need to worry about mode-specific drawing since the update function handles that for player 1
                obs.run()

        # It is still needed for player 2 though

        for player in self.charGroup: 
            if self.multiplayer == True:
                if player.player2 == False:
                    score1 = self.font.render(f"Player 1: {player.score}",True,(255,255,255)) # Make the score text
                    screen.blit(score1, (self.width/20,40)) # Display score on screen

                elif player.player2 == True:
                    score2 = self.font.render(f"Player 2: {player.score}",True,(255,255,255))
                    screen.blit(score2, (16*(self.width/20),40))

                for obs in self.obsGroup2: # Draw obstacles for player 2
                    obs.run()

                # Draw the line for split screen in multiplayer mode
                pygame.draw.line(screen,(255,255,255),(self.width/2 - (blockSize/2), 0),\
                    (self.width/2 - (blockSize/2), 5*(self.height/6)), width=5)

            else:
                score1 = self.font.render(f"Player 1: {player.score}",True,(255,255,255))
                screen.blit(score1, (10*(self.width/12),40))
            

game = Game(820,600)

game.startScreen()        
game.run()
