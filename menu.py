import time

import pygame

import globalvars
import player
from game import main
from globalclasses import Button
from globalclasses import GuiSettings
from input_name_menu import ask_name
from perfomance import img_load
from settings_menu import settings_menu
from store_score import store_score
from store_score_menu import store_score_menu

pygame.init()
pygame.mixer.init()

in_game: bool = False

background_file = f"./textures/bg/{globalvars.texture_modifier}pacman2.jpg"

def play():
    global in_game
    in_game = True
    main()
    time.sleep(0.3)  # Костыль
    in_game = False  # Но почему ?
    store_score(player.score, ask_name())
    options_menu()  # Но зачем ?


def exit_game():
    global in_game
    in_game = True

def sm():
    global background_file
    settings_menu()
    background_file = f"./textures/bg/{globalvars.texture_modifier}pacman2.jpg"

def options_menu():
    try:
        global background_file
        main_screen = pygame.display.set_mode((1066, 600))
        settings = GuiSettings()
        clock = pygame.time.Clock()
        buttons = [
            Button(220 * 0 + 80, 530, 200, 50, (0, 0, 0), settings, "Играть!", play),
            Button(220 * 1 + 80, 530, 200, 50, (0, 0, 0), settings, "Таблица Рекордов", store_score_menu),
            Button(220 * 2 + 80, 530, 200, 50, (0, 0, 0), settings, "Настройки", sm),
            Button(220 * 3 + 80, 530, 200, 50, (0, 0, 0), settings, "Выйти из игры", exit_game),
        ]
        timeout = 0
        while not in_game:
            timeout += 1
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit_game()
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_w] and pressed[pygame.K_t] and pressed[pygame.K_f] and timeout >= 100:
                        if background_file == "./textures/bg/pacman4.jpg":
                            background_file = f"./textures/bg/{globalvars.texture_modifier}pacman2.jpg"
                            globalvars.easter = 0
                            timeout = 0
                        elif timeout >= 100:
                            background_file = "./textures/bg/pacman4.jpg"
                            globalvars.easter = 1
                            timeout = 0

            for button in buttons:
                button.update(events)

            for button in buttons:
                button.draw(main_screen)

            pygame.display.flip()
            img = img_load(background_file)
            main_screen.blit(img, (0, 0))
            clock.tick(120)
        pygame.quit()
    except:
        print("Goodbye")
