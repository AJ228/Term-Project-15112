# This file runs the game using the pygamegame.py framework file
import pygame
from pygamegame import PygameGame
from Player import Player
from Wall import Wall
from Floor import Floor

class Game(PygameGame):
    def init(self):
        Wall.init(self.width, self.height)
        self.wallGroup = pygame.sprite.Group(Wall(0, self.height/2))
        self.wallGroup.add(Wall(self.width, self.height/2)) # Allows for wall to wrap around
        Floor.init(self.width, self.height)
        self.floorGroup = pygame.sprite.Group(Floor(0, 7*(self.height/8)))
        self.floorGroup.add(Floor(self.width, 7*(self.height/8)))
        # Allows floor to wrap around
        Player.init() 
        self.charGroup = pygame.sprite.Group(Player(self.width/4, 3*(self.height/4)-20))
        # Grouped character sprites together (demo only contains one sprite but still
        # useful for my project when making obstacles)

    def timerFired(self, dt): # Works much like graphics timerFired
        self.wallGroup.update(self.width, self.height)
        self.floorGroup.update(self.width, self.height)
        self.charGroup.update(self.isKeyPressed, self.width, self.height)

    def redrawAll(self, screen): # Works much like graphics redrawAll
        self.wallGroup.draw(screen)
        self.floorGroup.draw(screen)
        self.charGroup.draw(screen)
        
Game(600, 600).run()