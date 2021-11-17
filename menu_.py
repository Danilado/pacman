import time

import pygame

import player
from game import main
from input_name_menu import ask_name
from perfomance import img_load
from store_score import store_score
from store_score_menu import store_score_menu

pygame.init()
pygame.mixer.init()


class GuiSettings:
    def __init__(self):
        self.text_size = 20
        self.button_color = (93, 0, 255)
        self.button_color_hover = (174, 127, 255)


class Button:
    def __init__(self, x, y, width, height, outline, settings, text="", action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.settings = settings
        self.action = action
        self.outline = outline

    def draw(self, screen):
        if self.outline:
            pygame.draw.rect(screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        color = self.settings.button_color if not self.is_over(
            pygame.mouse.get_pos()) else self.settings.button_color_hover
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            pygame.font.init()
            font = pygame.font.SysFont('segoeuisemibold', self.settings.text_size)
            text = font.render(self.text, True, (0, 0, 0))
            screen.blit(
                text,
                (
                    self.x + (self.width / 2 - text.get_width() / 2),
                    self.y + (self.height / 2 - text.get_height() / 2)
                )
            )

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN \
                    and self.is_over(pygame.mouse.get_pos()) \
                    and self.action:
                self.action()
                return True
        return False

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


in_game: bool = False


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


def options_menu():
    main_screen = pygame.display.set_mode((1066, 600))
    settings = GuiSettings()
    clock = pygame.time.Clock()
    buttons = [
        Button(80, 530, 200, 50, (0, 0, 0), settings, "Играть!", play),
        Button(300, 530, 200, 50, (0, 0, 0), settings, "Таблица Рекордов", store_score_menu),
        Button(520, 530, 200, 50, (0, 0, 0), settings, "Выйти из игры", exit_game),
        Button(740, 530, 200, 50, (0, 0, 0), settings, "Настройки",            ),
    ]
    background_file = "./textures/bg/pacman2.jpg"

    while not in_game:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w] and pressed[pygame.K_t] and pressed[pygame.K_f]:
                    if background_file == "./textures/bg/pacman4.jpg":
                        background_file = "./textures/bg/pacman2.jpg"
                    else:
                        background_file = "./textures/bg/pacman4.jpg"

        for button in buttons:
            button.update(events)

        for button in buttons:
            button.draw(main_screen)

        pygame.display.flip()
        img = img_load(background_file)
        main_screen.blit(img, (0, 0))
        clock.tick(120)
    pygame.quit()
