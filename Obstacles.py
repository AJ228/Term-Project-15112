# File stores all possible obstacles that can be created as a sprite
# This approach was inspired by: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s
import pygame

blockSize = 40
screen_width = 600
screen_height = 600

spike = ["S"]
steps3 = ["  B",
         " BB",
         "BBB"]
level4Platform = ["PPPP",
                  "",
                  "",
                  ""]
level3Block = ["BBBBBB",
               "BBBBBB",
               "BBBBBB"]
