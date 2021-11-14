import pygame
from pygamegame import PygameGame
from Player import Player
from Floor import Floor

class Game(PygameGame):
    def init(self):
        Floor.init(self.width, self.height)
        self.floorGroup = pygame.sprite.Group(Floor(0, 7*(self.height/8)))
        Player.init() 
        self.charGroup = pygame.sprite.Group(Player(self.width/4, 3*(self.height/4)-20))
        # Grouped character sprites together (demo only contains one sprite but still
        # useful for my project when making obstacles)

    def timerFired(self, dt): # Works much like graphics timerFired
        self.floorGroup.update(self.width, self.height)
        self.charGroup.update(self.isKeyPressed, self.width, self.height)

    def redrawAll(self, screen): # Works much like graphics redrawAll
        self.floorGroup.draw(screen)
        self.charGroup.draw(screen)
        
Game(600, 600).run()