# This file runs the game using the pygamegame.py framework file
import pygame
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
        self.charGroup = pygame.sprite.Group(Player(self.width/4, 5*(self.height/6)-20))
        # Grouped character sprites together (demo only contains one sprite but still
        # useful for my project when making obstacles)
        self.obsGroup = [Obstacle(steps3, screen)]
        self.obsGroupSize = len(self.obsGroup)

    def timerFired(self, dt, screen): # Works much like graphics timerFired
        self.wallGroup.update(self.width, self.height)
        self.floorGroup.update(self.width, self.height)
        self.charGroup.update(self.isKeyPressed, self.width, self.height)
        for obs in self.obsGroup:
            obs.update(self.width, self.height)
            if obs.halfWay == True and self.obsGroupSize == 1:
                self.obsGroup.append(Obstacle(level3Platform, screen))
                obs.halfWay = False
                self.obsGroupSize += 1
            elif len(obs.obstacle) == 0:
                del obs
                self.obsGroupSize -= 1

    def redrawAll(self, screen): # Works much like graphics redrawAll
        self.wallGroup.draw(screen)
        self.floorGroup.draw(screen)
        self.charGroup.draw(screen)
        for obs in self.obsGroup:
            obs.run()
        
Game(600, 600).run()