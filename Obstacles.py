# File stores all possible obstacles that can be created in a level as a sprite
# This approach was inspired by: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s
import pygame

blockSize = 40
screen_width = 600
screen_height = 600

# Following obstacles are designed to be hazardous to the player while still traversable
# Floor-level hazards
spike = ("Hazard",["S"])

spikePit = ("Hazard",[" PP ",
            "STTS"])
# The following obstacles are for traversal purposes only

# Stepping platforms
steps2 = ("Steps",["  B",
          " BB"])

steps3 = ("Steps",["  B",
          " BB",
          "BBB"])

# Mid-air platforms

platform3 = ("Platform",
            ["PPPP",
             "",
             ""])

platform4 = ("Platform",
            ["PPPP",
             "",
             "",
             ""])

# Block-type platforms - will be square-type platforms (used with tower and step obstacles)

blockPlat3 = ("Block",
             ["4",
              "",
              ""])

blockPlat4 = ("Block",
             ["4",
              "",
              "",
              ""])

blockPlat5 = ("Block",
             ["4",
              "",
              "",
              "",
              ""])

# Elevated floor blocks

block2 = ("Blocks",
         ["BBBBBB",
          "BBBBBB"])

block4 = ("Blocks",
         ["BBBBBB",
          "BBBBBB",
          "BBBBBB"])

# Tower blocks, similar function to steps

tower1 = ("Tower",
         ["O"])

tower2 = ("Tower",
         ["O",
          "O"])

tower3 = ("Tower",
         ["O",
          "O",
          "O"])

tower4 = ("Tower",
         ["O",
          "O",
          "O",
          "O"])
