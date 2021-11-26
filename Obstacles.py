# File stores all possible obstacles that can be created in a level as a sprite
# This approach was inspired by: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=3184s
import pygame

blockSize = 40
screen_width = 800
screen_height = 600

# Following obstacles are designed to be hazardous to the player while still traversable
# Floor-level hazards

spike = ("Hazard1",
        ["S"]) # Obstacle type identifiers needed to decide which obstacle to spawn

spikePit = ("Hazard2",
           ["STTS"])

# The following obstacles are for traversal purposes only

# Stepping platforms

steps2 = ("Steps2",
         ["  B",
          " BB"])

steps3 = ("Steps3",
         ["  B",
          " BB",
          "BBB"])

# Mid-air platforms

platform2 = ("Platform2",
            ["PPPPP",
             ""])

platform3 = ("Platform3",
            ["PPPPP",
             "",
             ""])

platform4 = ("Platform4",
            ["PPPPP",
             "",
             "",
             ""])

# Block-type platforms - will be square-type platforms (used with tower and step obstacles)

blockPlat1 = ("Block1",
             ["4"])

blockPlat2 = ("Block2",
             ["4",
              ""])

blockPlat3 = ("Block3",
             ["4",
              "",
              ""])

blockPlat4 = ("Block4",
             ["4",
              "",
              "",
              ""])

blockPlat5 = ("Block5",
             ["4",
              "",
              "",
              "",
              ""])

# Elevated floor blocks

block1 = ("Blocks1",
         ["BBBBBB"])

block2 = ("Blocks2",
         ["BBBBBB",
          "BBBBBB"])

block3 = ("Blocks3",
         ["BBBBBB",
          "BBBBBB",
          "BBBBBB"])

block4 = ("Blocks4",
         ["BBBBBB",
          "BBBBBB",
          "BBBBBB",
          "BBBBBB"])

# Tower blocks, similar function to steps

tower1 = ("Tower1",
         ["O"])

tower2 = ("Tower2",
         ["O",
          "O"])

tower3 = ("Tower3",
         ["O",
          "O",
          "O"])

tower4 = ("Tower4",
         ["O",
          "O",
          "O",
          "O"])
