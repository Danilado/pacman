from typing import Tuple
from globalclasses import Button
from globalclasses import GuiSettingsForOptions
import globalvars

import pygame

def settings_menu():
    main_screen = pygame.display.set_mode((1066, 600))
    running = True
    settings = GuiSettingsForOptions()
    clock = pygame.time.Clock()
    buttons = [
        Button(340, 80, 200, 50, (0, 0, 0), settings, "Лёгкая", ),
        Button(560, 80, 200, 50, (0, 0, 0), settings, "Нормальная", ),
        Button(780, 80, 200, 50, (0, 0, 0), settings, "Сложная", ),


        Button(340, 180, 200, 50, (0, 0, 0), settings, "Обычные", ),
        Button(780, 180, 200, 50, (0, 0, 0), settings, "Альтернативные", ),
    ]
    text_font = pygame.font.SysFont("segoeuisemibold", 32)
    back_color = "black"
    # noinspection PyTypeChecker
    text_color: Tuple[int, int, int] = "white"
    while running:
        events = pygame.event.get()
        if pygame.event.peek(pump=True):
            main_screen.fill(back_color)
            main_screen.blit(
                text_font.render("Настройки", False, text_color),
                (
                    main_screen.get_width() // 2 - text_font.size("Настройки")[0] // 2,
                    20
                )
            )

            main_screen.blit(text_font.render("Сложность", False, text_color), (20, 90))
            main_screen.blit(text_font.render("Текстуры", False, text_color), (20, 190))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            for button in buttons:
                button.update(events)

            for button in buttons:
                button.draw(main_screen)

            pygame.display.flip()
