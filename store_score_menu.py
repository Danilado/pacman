from random import randint
from typing import Tuple

import pygame

from store_score import get_scores


# Sum of the min & max of (a, b, c)
def hilo(a, b, c):
    if c < b:
        b, c = c, b
    if b < a:
        a, b = b, a
    if c < b:
        b, c = c, b
    return a + c


def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))


def render_scores(main_screen, text_font: pygame.font.Font, color):
    for index, result in enumerate(get_scores()):
        text = f"{index + 1}) {result}"
        pos = (1066//2 - (text_font.size(text)[0])//2 - 15, 100 + 100 * (index + 1))
        print(text, pos)
        main_screen.blit(
            text_font.render(text, False, color),
            pos
        )


def store_score_menu():
    main_screen = pygame.display.set_mode((1066, 600))
    clock = pygame.time.Clock()
    running = True

    text_font = pygame.font.SysFont("Arial", 32)

    while running:
        back_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        # noinspection PyTypeChecker
        text_color: Tuple[int, int, int] = complement(back_color[0], back_color[1], back_color[2])

        clock.tick(120)
        pygame.display.flip()
        main_screen.fill(back_color)

        main_screen.blit(text_font.render("Таблица рекордов", False, text_color), (380, 100))
        render_scores(main_screen, text_font, text_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
