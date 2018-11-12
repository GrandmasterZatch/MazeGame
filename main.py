####################################################################################
# Maze Game                                                                        #
# By: Manish Kadayat, Zachary Lyon, Brock Mordecai                                 #
# Date: 10/5/18                                                                    #
# Description: Top down maze game for final pi Project in CSC 132                  #
####################################################################################

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
import RPi.GPIO as GPIO


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map3.txt'))

    def new(self):
        # initialize variables
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                    
                if tile == 'P':
                    self.player = Player(self, col, row)

                if tile == 'M':
                    self.monster = Monster(self, col, row)

                if tile == 'T':
                    self.treasure = Treasure(self, col, row)
                    
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = (self.clock.tick(FPS) / 1000)
            self.CheckJoystick()
            self.checkButton()
            self.events()
            self.update()
            self.draw()

    def quit(self):
        GPIO.cleanup()
        pg.quit()
        sys.exit()

    def update(self):
        # update game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
            
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def CheckJoystick(self):
        if round(joystick.get_axis(0)) == 1:
            self.player.move(dy = -1)
            self.monster.calc(2)
            pg.time.delay(225)

        if round(joystick.get_axis(0)) == -1:
            self.player.move(dy = 1)
            self.monster.calc(2)
            pg.time.delay(225)

        if round(joystick.get_axis(1)) == 1:
            self.player.move(dx = 1)
            self.monster.calc(2)
            pg.time.delay(225)

        if round(joystick.get_axis(1)) == -1:
            self.player.move(dx = -1)
            self.monster.calc(2)
            pg.time.delay(225)

    def checkButton(self):
        if(self.player.canRewind == True):
            GPIO.output(leds[4], GPIO.HIGH)
        else:
            GPIO.output(leds[4], GPIO.LOW)
        if (GPIO.input(button) == GPIO.HIGH):
            if(self.player.canRewind == True):
                self.player.rewind()
                self.monster.rewind()

    def events(self):
        # catch events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.treasure.all_off()
                GPIO.cleanup()
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                    
                if event.key == pg.K_LEFT:
                    self.player.move(dx = -1)
                    self.monster.calc(2)
                    
                if event.key == pg.K_RIGHT:
                    self.player.move(dx = 1)
                    self.monster.calc(2)

                if event.key == pg.K_UP:
                    self.player.move(dy = -1)
                    self.monster.calc(2)

                if event.key == pg.K_DOWN:
                    self.player.move(dy = 1)
                    self.monster.calc(2)

                if event.key == pg.K_SPACE:
                    if self.player.x == self.treasure.x and self.player.y == self.player.y:
                        self.show_win_screen()
        
            if event.type == pg.JOYBUTTONDOWN:
                if self.player.x == self.treasure.x and self.player.y == self.player.y:
                    self.show_win_screen()

    def show_win_screen(self):
        print "YOU WIN!!!"
        print "YOU WIN!!!"
        print "YOU WIN!!!"
        self.quit()

    def show_lose_screen(self):
        print "YOU LOSE!!!"
        print "YOU LOSE!!!"
        print "YOU LOSE!!!"
        self.quit()


# Use broadcom pin mode and disable warnings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Button setup
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup input and output pins
GPIO.setup(leds, GPIO.OUT)

# Create game object
g = Game()
while True:
    g.new()
    g.run()
    g.show_win_screen()
