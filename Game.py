import pygame
from pygamegame import PygameGame
from Player import Player

class Game(PygameGame):
    def init(self):
        Player.init() 
        self.charGroup = pygame.sprite.Group(Player(self.width/2, self.height/2))
        # Grouped character sprites together (demo only contains one sprite but still
        # useful for my project when making obstacles)

    def timerFired(self, dt): # Works much like graphics timerFired
        self.charGroup.update(self.isKeyPressed, self.width, self.height)

    def redrawAll(self, screen): # Works much like graphics redrawAll
        self.charGroup.draw(screen)
        
Game(600, 600).run()