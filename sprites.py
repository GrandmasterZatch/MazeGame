import pygame as pg
import RPi.GPIO as GPIO
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.oldX=x
        self.oldY=y
        self.canRewind = False

    def move(self, dx = 0, dy = 0):
        if not self.collide_with_walls(dx, dy):
            self.oldX = self.x
            self.oldY = self.y
            self.canRewind = True
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx = 0, dy = 0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def rewind(self):
        self.x = self.oldX
        self.y = self.oldY
        self.canRewind = False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Monster(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.oldX = x
        self.oldY = y

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            # If player is caught, end game
            if self.game.player.x == self.x and self.game.player.y == self.y:
                self.game.show_lose_screen()

    def collide_with_walls(self, dx = 0, dy = 0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def calc(self, num):
        self.oldX = self.x
        self.oldY = self.y
        for i in range(num):

            # Figure out movement direction, x before y
            if self.game.player.x < self.x:
                self.move(dx = -1)

            elif self.game.player.x > self.x:
                self.move(dx = 1)

            elif self.game.player.y < self.y:
                self.move(dy = -1)

            elif self.game.player.y > self.y:
                self.move(dy = 1)
                
    def rewind(self):
        self.x = self.oldX
        self.y = self.oldY

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Treasure(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((1, 1))
        self.image.fill(TAN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.direction()

    def all_off(self):
        for i in leds:
            GPIO.output(leds, False)
            
    def all_on(self):
        for i in range(0, 3):
            GPIO.output(leds, True)

    def direction(self):
        self.all_off()
        # 16:SOUTH, 17:NORTH, 18:EAST, 19:WEST
        if self.game.player.x > self.x:
            GPIO.output(leds[3], True)
            
        if self.game.player.x < self.x:
            GPIO.output(leds[2], True)

        if self.game.player.y > self.y:
            GPIO.output(leds[1], True)

        if self.game.player.y < self.y:
            GPIO.output(leds[0], True)

        if self.game.player.y == self.y and self.game.player.x == self.x:
            self.all_on()

    


# initialize joysticks
pg.joystick.init()
# get count of joysticks
joystick_count = pg.joystick.get_count()

# for each joystick
for i in range(joystick_count):
    joystick = pg.joystick.Joystick(i)
    joystick.init()

    # get name from OS for the joystick
    name = joystick.get_name()
    axes = joystick.get_numaxes()

    for i in range(axes):
        axis = joystick.get_axis(i)

    buttons = joystick.get_numbuttons()

    for i in range(buttons):
        button = joystick.get_button(i)
