import pygame as pg
import player
from globalvars import score
from game import main


tick1 = 0
tick2 = 0
tick3 = 0
tick4 = 0
tick5 = 0
cherry_img = pg.image.load('Cherry.png')

if score >= 200 & tick1 == 0:
    main.screen.blit(cherry_img, (140, 120))
    tick1 = 1
