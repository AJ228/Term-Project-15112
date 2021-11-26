import pygame
from Button import Button

# Using the framework provided in the Pygame manual with my own extra attributes
# https://qwewy.gitbooks.io/pygame-module-manual/content/chapter1/framework.html
# Created by Lukas Peraza

# Single player level music source:
# https://downloads.khinsider.com/game-soundtracks/album/geometry-dash/05.DJVI%2520-%2520Base%2520After%2520Base.mp3

# Multiplayer level music source:
# https://downloads.khinsider.com/game-soundtracks/album/geometry-dash/13.Waterflame%2520-%2520Electroman%2520Adventures%2520%2528HD%2529.mp3

class PygameGame(object):

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=820, height=600, fps=60, title="112 Dash"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (0, 0, 0)
        self.blips = 0 # Used to track time-based events
        self.obsGroup = [] # For obstacle spawning
        self.last = 0
        self.towerDelay = 21 # Spawning timers depending on obstacle generated
        self.blocksDelay = 61
        self.blockDelay = 21
        self.hazardDelay = 21
        self.stepDelay = 41
        self.platformDelay = 51
        self.killCount = 0 # Used to decide when the game over screen should appear
        self.gameOver = False
        self.levelDelay = 61 # All incremented by 1 to allow blip adjustment in Game.py
        self.spawnDelay = self.levelDelay # Setting delays between obstacles spawning, starts at 1 second
        self.multiplayer = False
        self.scores = [0] # Stores scores of players to be displayed once game ends


        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Setting text font for displaying text
        self.font = pygame.font.Font("freesansbold.ttf",15)
        self.titleFont = pygame.font.Font("freesansbold.ttf",30)

        wallImage = pygame.image.load('Game_BG.png').convert_alpha() # For screen background
        self.background = pygame.transform.scale(wallImage,(self.width,self.height))

    # startScreen - method used to run the start screen 
    # Method to do this inspired from https://www.youtube.com/watch?v=vz8YnvnAPp4

    def startScreen(self):
        
        start = True # Starts the game loop for the start screen

        title = self.titleFont.render("112 Dash", True, (255, 255, 255)) # Creating title screen text
        title_rect = title.get_rect(x=self.width/2 - 50, y=200)

        play1_button = Button(self.width/3 - 50, self.height/2, 200, 80, (255,255,255), (0, 0, 0), "Single Player", 30)
        play2_button = Button(2*(self.width/3) - 50, self.height/2, 200, 80, (255,255,255), (0, 0, 0), "Multiplayer", 30)
        # Making a button that the user can interact with

        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Allows user to quit from the title screen
                    start = False
                    self.playing = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play1_button.isPressed(mouse_pos, mouse_pressed): # Starts the game if play is clicked
                start = False

                self.playing = True

            elif play2_button.isPressed(mouse_pos, mouse_pressed): # Same thing but for multiplayer
                start = False
                self.multiplayer = True
                self.playing = True

            self.screen.blit(self.background, (0, 0)) # Draw all elements onto the screen
            self.screen.blit(title, title_rect)
            self.screen.blit(play1_button.image, play1_button.rect)
            self.screen.blit(play2_button.image, play2_button.rect)
            
            self.clock.tick(self.fps)
            pygame.display.update()

    # gameEndScreen - method used to run the game over screen

    def gameEndScreen(self):
        
        start = True # Starts the game loop for the game end screen

        title = self.titleFont.render("Game Over", True, (255, 255, 255)) # Creating screen text
        title_rect = title.get_rect(x=self.width/2 - 50, y=200)

        score1 = self.titleFont.render(f"Player 1: {self.scores[0]}", True, (255, 255, 255)) # Showing player 1 score
        score1_rect = score1.get_rect(x=self.width/2 - 50, y=300)

        if self.multiplayer == True:
            score2 = self.titleFont.render(f"Player 2: {self.scores[1]}", True, (255, 255, 255)) # Showing player 2 score
            score2_rect = score1.get_rect(x=self.width/2 - 50, y=400)

        quit_button = Button(self.width/2 - 50, 500, 100, 80, (255,255,255), (0, 0, 0), "Quit", 30)

        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                    self.playing = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if quit_button.isPressed(mouse_pos, mouse_pressed):
                start = False
                self.playing = False # Close program after game ends

            self.screen.blit(self.background, (0, 0)) # Draw all elements onto the screen
            self.screen.blit(title, title_rect)
            self.screen.blit(score1, score1_rect)
            self.screen.blit(quit_button.image, quit_button.rect)

            if self.multiplayer == True:
               self.screen.blit(score2, score2_rect) 
            
            self.clock.tick(self.fps)
            pygame.display.update()


    def run(self):

        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init(self.screen)

        while self.playing:
            time = self.clock.tick(self.fps)
            self.timerFired(time, self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))

                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                    
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))

                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)

                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)

                elif event.type == pygame.QUIT:
                    self.playing = False
            
            if self.gameOver == True:
                self.gameEndScreen()

            self.screen.fill(self.bgColor)
            self.redrawAll(self.screen)

            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.startScreen()
    game.run()

if __name__ == '__main__':
    main()