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
        self.obsGroup = [] # Testing obstacle spawning
        self.spawningTowers = False
        self.risingLevel = False
        self.last = -1

    def timerFired(self, dt, screen): # Works much like graphics timerFired
        self.blips += 1

        if self.obsGroup == []: # If there's no obstacle, it means the character is on the floor
            obstacle = random.choice([spike, spikePit, steps2, steps3, tower1, blockPlat1]) # So make floor-level obstacles
            self.obsGroup.append(Obstacle(obstacle, screen))
            self.last += 1

        self.wallGroup.update(self.width, self.height)
        self.floorGroup.update(self.width, self.height)
        self.charGroup.update(self.isKeyPressed, self.width, self.height)

        for player in self.charGroup: # Manage collisions with obstacles and players
            for obs in self.obsGroup:
                for block in obs.obstacle:
                    if block.rect.colliderect(player.rect):
                        if player.x + (blockSize/2) == block.x - (blockSize/2) and (block.y - (blockSize/2)) <= player.y <= (block.y +(blockSize/2)):
                            self.charGroup.remove(player) # Kills player from any horizontal collision
                        if player.falling == True: # Allows vertical collisions bottom of player
                            player.falling = False
                        elif player.y - (blockSize/2) in (block.y - (blockSize/2),block.y + (blockSize/2)): # Not with top of player
                            self.charGroup.remove(player)

        for floor in self.floorGroup: # Managing collisions between player and floor
            for player in self.charGroup:
                 if floor.rect.colliderect(player.rect):
                     if player.falling == True:
                        player.falling = False
                        player.startY = floor.rect.y - (blockSize/2)
                        
        for obs in self.obsGroup:
            obs.update(self.width, self.height)

            if len(obs.obstacle) == 0: # If current sprite group (obstacle object) in list has no sprites left
                self.obsGroup.remove(obs) # Delete sprite group from obstacle list
                self.last -= 1
                
        if self.obsGroup[self.last].obType == "Tower" and self.spawningTowers == False and self.obsGroup[self.last].obLevel == "1": # Checks if latest obstacle is a tower
            self.spawningTowers = True
            self.risingLevel = True
            self.spawnDelay = self.towerDelay
        
        elif self.obsGroup[self.last].obType == "Blocks":
            self.spawnDelay = self.blockDelay

        elif self.obsGroup[self.last].obType == "Platform":
            self.spawnDelay = self.platformDelay

        elif self.obsGroup[self.last].obType == "Block":
            self.spawnDelay = self.towerDelay

        else:
            self.spawnDelay = self.levelDelay 
    
        if self.blips % self.spawnDelay == 0: # Add a new obstacle based on spawnDelay
            if self.spawningTowers == True: # Spawning towers

                if self.risingLevel == True:
                    if self.obsGroup[self.last].obLevel == "1":
                        self.obsGroup.append(Obstacle(tower2, screen))
                        self.last += 1

                    elif self.obsGroup[self.last].obLevel == "2":
                        self.obsGroup.append(Obstacle(tower3, screen))
                        self.last += 1

                    elif self.obsGroup[self.last].obLevel == "3":
                        self.obsGroup.append(Obstacle(tower4, screen))
                        self.risingLevel = False
                        self.last += 1


                elif self.risingLevel == False:
                    if self.obsGroup[self.last].obLevel == "4":
                        self.obsGroup.append(Obstacle(tower3, screen))
                        self.last += 1

                    elif self.obsGroup[self.last].obLevel == "3":
                        self.obsGroup.append(Obstacle(tower2, screen))
                        self.last += 1

                    elif self.obsGroup[self.last].obLevel == "2":
                        self.obsGroup.append(Obstacle(tower1, screen))
                        self.spawningTowers = False
                        self.spawnDelay = self.levelDelay # Reset spawn delay
                        self.last += 1

            elif self.spawningTowers == False:
                if self.obsGroup[self.last].obLevel == "1":
                    # if self.obsGroup[self.last].obType == "1":
                    obstacle = random.choice([spike, spikePit, steps2, steps3, blockPlat1, blockPlat2, block1, block2, tower1])

                elif self.obsGroup[self.last].obLevel == "2":
                    obstacle = random.choice([blockPlat1, blockPlat2, blockPlat3, block1, block2 ,block3, platform2, platform3])

                elif self.obsGroup[self.last].obLevel == "3":
                    obstacle = random.choice([blockPlat2, blockPlat3, blockPlat4, block2, block3, block4, platform2, platform3, platform4])

                elif self.obsGroup[self.last].obLevel == "4":
                    obstacle = random.choice([blockPlat3, blockPlat4, blockPlat5, block3, block4, platform3, platform4])

                elif self.obsGroup[self.last].obLevel == "5":
                    obstacle = random.choice([blockPlat3, blockPlat4, blockPlat5, block3, block4, platform3, platform4])

                self.obsGroup.append(Obstacle(obstacle, screen))
                self.last += 1
                

    def redrawAll(self, screen): # Works much like graphics redrawAll
        self.wallGroup.draw(screen)
        self.floorGroup.draw(screen)
        self.charGroup.draw(screen)
        for obs in self.obsGroup:
            obs.run()
        
Game(600, 600).run()