# MenuComp.py - Stores all necessary components for user interaction elements like buttons for screens

import pygame

class Button:
    def __init__(self, x, y, width, height, foreground, background, content, fontSize):
        self.titleFont = pygame.font.Font("freesansbold.ttf", fontSize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.foreground = foreground
        self.background = background

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.background)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.titleFont.render(self.content, True, self.foreground)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))

        self.image.blit(self.text, self.text_rect)

    def isPressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


