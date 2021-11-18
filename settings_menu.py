import pygame
from globalclasses import Button, GuiSettings
import globalvars

def setTextures():
    if globalvars.texture_modifier != "":
        globalvars.texture_modifier = ""
    else:
        globalvars.texture_modifier = "r_"


def settings_menu():
    main_screen = pygame.display.set_mode((1066, 600))
    text_color = (255,) * 3
    settings = GuiSettings(button_color=text_color, button_color_hover=(120,) * 3)
    buttons = [
        Button(220 * 0 + main_screen.get_width() // 4 + 80, 80, 200, 50, (0, 0, 0), settings, "Лёгкая"),
        Button(220 * 1 + main_screen.get_width() // 4 + 80, 80, 200, 50, (0, 0, 0), settings, "Нормальная"),
        Button(220 * 2 + main_screen.get_width() // 4 + 80, 80, 200, 50, (0, 0, 0), settings, "Сложная"),
        Button(220 * 0 + main_screen.get_width() // 4 + 80, 180, 200, 50, (0, 0, 0), settings, "Обычные", setTextures),
        Button(220 * 2 + main_screen.get_width() // 4 + 80, 180, 200, 50, (0, 0, 0), settings, "Альтернативные", setTextures),
    ]
    text_font = pygame.font.SysFont("segoeuisemibold", 32)
    running = True
    back_color = "black"
    while running:
        if pygame.event.peek(pump=True):
            events = pygame.event.get()
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

            for event in events:
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
