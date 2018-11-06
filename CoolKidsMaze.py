####################################################################################
# Maze Game                                                                        #
# By: Manish Kadayat, Zachary Lyon, Brock Mordecai                                 #
# Date: 10/5/18                                                                    #
# Description: Top down maze game for final pi Project in CSC 132                  #
####################################################################################
import pygame
import sys
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()


    def load_data(self):
        pass


    def new(self):
        # initialize variables, setup game
        self.all_sprites = pygame.sprite.Group()

    def run(self):
        # Main loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # Update positions of all entities
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, colors[LIGHTGREY], (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, colors[LIGHTGREY], (0, y), (WIDTH, y))
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        # Anything outside of regular movement is calculated here
        pass
        
