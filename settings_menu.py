import pygame

import globalvars
from globalclasses import Button, GuiSettings


def set_common_textures():
    globalvars.texture_modifier = ""


def set_alt_textures():
    globalvars.texture_modifier = "r_"


def set_easy_difficulty():
    globalvars.difficulty = 0.5


def set_normal_difficulty():
    globalvars.difficulty = 1


def set_hard_difficulty():
    globalvars.difficulty = 1.5


def settings_menu():
    main_screen = pygame.display.set_mode((1066, 600))
    text_color = (255,) * 3
    settings = GuiSettings(button_color=text_color, button_color_hover=(127,) * 3)
    btn_easy = Button(220 * 0 + main_screen.get_width() // 4 + 80, 80, 200, 50, (0, 0, 0),
                      settings, "Лёгкая", set_easy_difficulty)
    btn_norm = Button(220 * 1 + main_screen.get_width() // 4 + 80, 80, 200, 50, (0, 0, 0),
                      settings, "Нормальная", set_normal_difficulty)
    btn_hard = Button(220 * 2 + main_screen.get_width() // 4 + 80, 80, 200, 50, (0, 0, 0),
                      settings, "Сложная", set_hard_difficulty)
    btn_common_textures = Button(220 * 0 + main_screen.get_width() // 4 + 80, 180, 200, 50, (0, 0, 0),
                                 settings, "Классические", set_common_textures)
    btn_alt_textures = Button(220 * 2 + main_screen.get_width() // 4 + 80, 180, 200, 50, (0, 0, 0),
                              settings, "Альтернативные", set_alt_textures)
    buttons = [btn_easy, btn_norm, btn_hard, btn_common_textures, btn_alt_textures]
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

            dif_str = ""
            txt_str = ""
            if globalvars.difficulty == 0.5:
                dif_str = "Легкая"
            elif globalvars.difficulty == 1.5:
                dif_str = "Сложная"
            else:
                dif_str = "Нормальная"
            if globalvars.texture_modifier == "":
                txt_str = "Классические"
            else:
                txt_str = "Альтернативные"
            main_screen.blit(text_font.render("Сложность", False, text_color), (20, 90))
            main_screen.blit(text_font.render("Текстуры", False, text_color), (20, 190))
            main_screen.blit(text_font.render(f"Текущая сложность:  {dif_str}", False, text_color), (20, 290))
            main_screen.blit(text_font.render(f"Текущие текстуры:  {txt_str}", False, text_color), (20, 390))

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
