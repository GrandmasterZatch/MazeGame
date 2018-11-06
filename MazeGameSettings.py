# Storage center for colors, tile size, EVERYTHING
colors = {
    "WHITE" : [255,255, 255],
    "BLACK" : [0, 0, 0],
    "DARKGREY" : [40, 40, 40],
    "LIGHTGREY" : [100,100,100],
    "GREEN" : [0, 255, 0],
    "RED" : [255, 0, 0],
    "YELLOW" : [255, 255, 0]
        }

WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Maze game demo"
BGCOLOR = colors["DARKGREY"]

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
