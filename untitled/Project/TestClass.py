import sys
import pygame as pg

def run_game():
    pg.init()
    screen= pg.display.set_mode((1200,800))
    pg.display.set_caption("Alien Invasion")
    while True:
        for event in pg.event.get():
            if event.type == pq.QUIT:
                sys.exit()

        pg.display.flip()

run_game()