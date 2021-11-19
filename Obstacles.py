# File stores all possible obstacles that can be created in a level as a sprite
# This approach was inspired by: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s
import pygame

blockSize = 40
screen_width = 600
screen_height = 600

# Following obstacles are designed to be hazardous to the player while still traversable
# Floor-level hazards
spike = ["S"]

spikePit = [" PP ",
            "STTS"]
# The following obstacles are for traversal purposes only

# Stepping platforms
steps2 = ["  B",
          " BB"]

steps3 = ["  B",
          " BB",
          "BBB"]

# Mid-air platforms

platform3 = ["PPPP",
             "",
             ""]

platform4 = ["PPPP",
             "",
             "",
             ""]

# Block-type platforms - will be square-type platforms (used with tower and step obstacles)

blockPlat3 = ["4",
              "",
              ""]

blockPlat4 = ["4",
              "",
              "",
              ""]

blockPlat5 = ["4",
              "",
              "",
              "",
              ""]

# Elevated floor blocks

block2 = ["BBBBBB",
          "BBBBBB"]

block4 = ["BBBBBB",
          "BBBBBB",
          "BBBBBB"]

# Tower blocks, similar function to steps

tower1 = ["O"]

tower2 = ["O",
          "O"]

tower3 = ["O",
          "O",
          "O"]
          
tower4 = ["O",
          "O",
          "O",
          "O"]
