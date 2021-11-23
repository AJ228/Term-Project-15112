# This file runs the game using the pygamegame.py framework file
import pygame
import random
from pygamegame import PygameGame
from Player import Player
from Wall import Wall
from Floor import Floor
from Obstacle import Obstacle
from Obstacles import *

class Game(PygameGame):
    def init(self, screen):
        Wall.init(self.width, self.height)
        self.wallGroup = pygame.sprite.Group(Wall(0, self.height/2))
        self.wallGroup.add(Wall(self.width, self.height/2)) # Allows for wall to wrap around
        Floor.init(self.width, self.height)
        self.floorGroup = pygame.sprite.Group(Floor(0, 11*(self.height/12)))
        self.floorGroup.add(Floor(self.width, 11*(self.height/12)))
        # Allows floor to wrap around
        Player.init() 
        self.charGroup = pygame.sprite.Group(Player(self.width/4, self.height/2))
        # Grouped character sprites together (grouped because there can be multiple players)
        self.obsGroup = [] # For obstacle spawning
        self.last = -1

    def timerFired(self, dt, screen): # Works much like graphics timerFired
        self.blips += 1

        if self.obsGroup == []: # If there's no obstacle, it means the character is on the floor
            obstacle = random.choice([spike, steps2, steps3, tower1, blockPlat1]) # So make floor-level obstacles
            self.obsGroup.append(Obstacle(obstacle, screen))
            self.last += 1

        self.wallGroup.update(self.width, self.height)
        self.floorGroup.update(self.width, self.height)
        self.charGroup.update(self.isKeyPressed, self.width, self.height)

        for player in self.charGroup: # Manage collisions with obstacles and players
            for obs in self.obsGroup: # Checks obstacle objects
                for block in obs.obstacle: # Checks each block sprite for every obstacle object
                    if block.rect.colliderect(player.rect):
                        if player.x + (blockSize/2) == block.x - (blockSize/2):
                            if player.y + (blockSize/2) > block.y - (blockSize/3): # Makes sure player is below top edge
                                self.gameOver = True # Kills player from any horizontal collision and ends game
                        
                        elif player.startY + (blockSize/2) >= block.rect.top: # Allows vertical collisions with bottom of player
                            if obs.obType == "Hazard": # Kill if player lands on a hazard 
                                self.gameOver = True
                            else:
                                player.obCollision = True
                                player.floorCollision = False
                                player.jumpHeight = 0
                                player.startY = block.rect.y - (blockSize/2)
                        
                        if player.y - (blockSize/2) == block.y + (blockSize/2): # Not with top of player for overhead obstacles
                            self.gameOver = True

                    elif player.x - (blockSize/2) == block.x + (blockSize/2): # Allows player to fall off obstacle
                        player.obCollision = False

            for floor in self.floorGroup: # Managing collisions between player and floor
                if floor.rect.colliderect(player.rect):
                    player.obCollision = False
                    player.floorCollision = True
                    player.jumpHeight = 0
                    player.startY = floor.rect.y - (blockSize/2)
                
        for obs in self.obsGroup:
            obs.update(self.width, self.height)

            if len(obs.obstacle) == 0: # If current sprite group (obstacle object) in list has no sprites left
                self.obsGroup.remove(obs) # Delete sprite group from obstacle list
                self.last -= 1

        if self.obsGroup[self.last].obType == "Tower": # Checks if latest obstacle is a tower
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

        if self.blips % self.spawnDelay == 0 and len(self.obsGroup) <= self.spawnLimit: # Add a new obstacle based on spawnDelay
            
            # Choose obstacles from specific sets based on latest obstacle level and type

            if self.obsGroup[self.last].obLevel == "1": 
                if self.spawnDelay == self.blockDelay:
                    obstacle = random.choice([blockPlat1, blockPlat2, block1, block2, tower1, tower2])
                elif self.spawnDelay == self.hazardDelay:
                    obstacle = random.choice([spike, blockPlat1, block1, tower1])
                elif self.spawnDelay == self.blocksDelay:
                    obstacle = random.choice([block1, block2, platform2])
                elif self.spawnDelay == self.towerDelay:
                    obstacle = random.choice([tower1, tower2, blockPlat2, block2, platform2])
                elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                    obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle
                    
            elif self.obsGroup[self.last].obLevel == "2":
                if self.spawnDelay == self.blockDelay:
                    obstacle = random.choice([platform2, platform3, blockPlat1, blockPlat2, blockPlat3, block1,\
                         block2, block3, tower2, tower3])
                elif self.spawnDelay == self.blocksDelay:
                    obstacle = random.choice([platform2, platform3, block1, block2, block3])
                elif self.spawnDelay == self.platformDelay:
                    obstacle = random.choice([platform2, platform3, blockPlat2, blockPlat3, block1, block2, block3])
                elif self.spawnDelay == self.towerDelay:
                    obstacle = random.choice([tower1, tower2, tower3, blockPlat2, blockPlat3, block2, block3]) 
                elif self.spawnDelay == self.stepDelay:
                    obstacle = random.choice([platform2, platform3, blockPlat2, blockPlat3, block2, block3])
                elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                    obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle 

            elif self.obsGroup[self.last].obLevel == "3":
                if self.spawnDelay == self.blockDelay:
                    obstacle = random.choice([platform2, platform3, platform4, blockPlat2, blockPlat3, blockPlat4,\
                         block2, block3, block4, tower3, tower4])
                elif self.spawnDelay == self.blocksDelay:
                    obstacle = random.choice([platform2, platform3, platform4, block2, block3, block4])
                elif self.spawnDelay == self.platformDelay:
                    obstacle = random.choice([platform2, platform3, platform4, blockPlat3, blockPlat4, block2,\
                         block3, block4])
                elif self.spawnDelay == self.towerDelay:
                    obstacle = random.choice([tower2, tower3, tower4, blockPlat2, blockPlat3, blockPlat4, block2, \
                        block3, block4]) 
                elif self.spawnDelay == self.stepDelay:
                    obstacle = random.choice([platform3, platform4, blockPlat3, blockPlat4, block2, block3, block4])
                elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                    obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle

            elif self.obsGroup[self.last].obLevel == "4":
                if self.spawnDelay == self.blockDelay:
                    obstacle = random.choice([platform3, platform4, blockPlat3, blockPlat4, blockPlat5, block3,\
                         block4, tower3, tower4])
                elif self.spawnDelay == self.blocksDelay:
                    obstacle = random.choice([platform2 ,platform3, platform4, block3, block4])
                elif self.spawnDelay == self.platformDelay:
                    obstacle = random.choice([platform3, platform4, blockPlat3, blockPlat4, blockPlat5, block2,\
                         block3, block4])
                elif self.spawnDelay == self.towerDelay:
                    obstacle = random.choice([tower3, tower4, blockPlat3, blockPlat4, blockPlat5, block2, block3, \
                        block4]) 
                elif self.spawnDelay == self.levelDelay: # The obstacle would have been long gone in this case so...
                    obstacle = random.choice([tower1, blockPlat1, block1, spike]) # Spawn a floor-level obstacle

            elif self.obsGroup[self.last].obLevel == "5": # Only one type of level 5 obstacle so no need to split
                obstacle = random.choice([tower4, blockPlat3, blockPlat4, blockPlat5, block3, block4, platform3,\
                     platform4])

            else: # For level 0 (floor-level) obstacles
                obstacle = random.choice([spike, steps2, steps3, blockPlat1, block1, tower1]) 

            self.obsGroup.append(Obstacle(obstacle, screen))
            self.last += 1
                
    def redrawAll(self, screen): # Works much like graphics redrawAll
        self.wallGroup.draw(screen)
        self.floorGroup.draw(screen)
        self.charGroup.draw(screen)
        for obs in self.obsGroup:
            obs.run()
        
Game(600, 600).run()