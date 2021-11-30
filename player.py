from typing import List, TYPE_CHECKING

import pygame

import global_variables
from perfomance import img_load
from store_score import get_scores

if TYPE_CHECKING:
    from ghosts.core import MainGhost

black = 0, 0, 0
game_map = []
game_simplified_map = []
score = 0


class Pacman:
    def __init__(self, x, y, window):
        scores = tuple(get_scores())
        self.cherry_img = img_load('textures/Cherry.png', 2 * global_variables.cell_size,
                                   1.875 * global_variables.cell_size)
        self.best = max(scores, key=lambda item: item.score).score if scores != () else 0
        self.x = x
        self.y = y
        self.vec = 0  # 0 - вправо. 1 - вверх. 2 - влево. 3 - вниз.
        self.vel = 1
        self.speed = 0.5
        self.status = 'unhit'
        self.screen = window
        self.dead = False
        self.dead_sound = pygame.mixer.Sound("./sounds/death_1.wav")
        self.dead_channel = pygame.mixer.Channel(1)
        self.dead_sound_playing = False
        self.invincible = 0
        self.eaten = 0
        self.lives = 3
        self.last = pygame.time.get_ticks()
        self.in_energizer = False
        self.eat_ghost_sound = pygame.mixer.Sound("./sounds/eat_ghost.wav")
        self.eat_channel = pygame.mixer.Channel(2)
        self.eat_sound1 = pygame.mixer.Sound("./sounds/munch_1.wav")
        self.eat_sound2 = pygame.mixer.Sound("./sounds/munch_2.wav")
        self.win = False
        self.victory_sound_playing = False
        self.victory_sound_1 = pygame.mixer.Sound("./sounds/victory_1.wav")
        self.victory_sound_2 = pygame.mixer.Sound("./sounds/victory_2.wav")
        self.win_channel = pygame.mixer.Channel(3)
        self.current_eat_sound_index = 1
        self.remember_vec = -1
        self.dots = 0
        if global_variables.instant_win:
            self.dots = 244
        self.number_image = -1
        self.god = global_variables.god
        self.cherry_call = 0xAB0BA
        self.cherry_on_screen = 0
        self.cherry_multiplier = 100
        self.total_way = 0
        self.status_eat = 0
        self.paused = 0
        self.paused_time = 0
        self.cherry_position = pygame.rect.Rect(
            self.screen.get_width() // 2 - global_variables.cell_size, 23 * global_variables.cell_size - 50,
            self.cherry_img.get_width(), self.cherry_img.get_height()
        )

    def draw(self):
        img = img_load(f'./textures/pacsprites/pacman0.png', global_variables.cell_size * 2,
                       global_variables.cell_size * 2)
        if self.status_eat == 90:
            img = img_load(f'./textures/pacsprites/pacman{self.vec + 5}.png',
                           global_variables.cell_size * 2, global_variables.cell_size * 2)
        elif self.status_eat == 0:
            img = img_load(f'./textures/pacsprites/pacman9.png', global_variables.cell_size * 2,
                           global_variables.cell_size * 2)
        elif self.status_eat == 45:
            img = img_load(f'./textures/pacsprites/pacman{self.vec}.png',
                           global_variables.cell_size * 2, global_variables.cell_size * 2)
        img2 = img_load(f'./textures/pacsprites/pacman0.png', global_variables.cell_size * 2,
                        global_variables.cell_size * 2)
        for i in range(self.lives):
            self.screen.blit(
                img2,
                (
                    20 * i * (global_variables.cell_size / 8),
                    self.screen.get_height() - 20 * (global_variables.cell_size / 8)
                )
            )
        # pygame.draw.rect(self.screen, (255, 255, 0), (self.x, self.y, 8, 8), 1)
        self.screen.blit(
            img, (self.x - (global_variables.cell_size / 2), self.y - (global_variables.cell_size / 2) + 50)
        )

    def play_dead_sound(self):
        if not self.dead_sound_playing:
            self.dead_channel.play(self.dead_sound)
            if self.lives == 0:
                self.dead_sound_playing = True
        return self.dead_channel.get_busy()

    def play_win_sound(self):
        if not self.victory_sound_playing:
            if not global_variables.easter:
                self.win_channel.play(self.victory_sound_1)
            else:
                self.win_channel.play(self.victory_sound_2)
            self.victory_sound_playing = True
        return self.win_channel.get_busy()

    def play_eat_ghost_sound(self):
        is_audio_running = self.eat_channel.get_busy()
        if not is_audio_running:
            self.eat_channel.play(self.eat_ghost_sound)
        is_audio_running = self.eat_channel.get_busy()
        return is_audio_running

    def play_munch_sound(self):
        if not self.eat_channel.get_busy():
            if self.current_eat_sound_index == 1:
                self.eat_channel.play(self.eat_sound1)
                self.current_eat_sound_index += 1
            elif self.current_eat_sound_index == 2:
                self.eat_channel.play(self.eat_sound2)
                self.current_eat_sound_index = 1

    def _update_energizer_effect(self, ghosts: List["MainGhost"]):
        global score
        now = pygame.time.get_ticks()
        if self.in_energizer and now - self.last <= 7000:
            for ghost in ghosts:
                if ((self.x - ghost.position.x) ** 2 + (
                        self.y - ghost.position.y) ** 2) ** 0.5 <= global_variables.cell_size:
                    if ghost.scared:
                        if not ghost.ghost_logic.eaten:
                            score += 200 * (2 ** self.eaten)
                            self.eaten += 1
                            # print(f'{self.eaten} {score}')
                            self.play_eat_ghost_sound()
                            ghost.trigger_eaten()
                    elif not self.god and not ghost.ghost_logic.eaten:
                        self.hit(ghosts)
        if now - self.last >= 7000:
            self.invincible = 0
            self.in_energizer = False

    def hit(self, ghosts: List["MainGhost"]):
        for ghost in ghosts:
            ghost.ghost_logic.go_home()
            ghost.trigger = 0
            ghost.stay = 1
        self.lives -= 1
        self.x = 108 * (global_variables.cell_size / 8)
        self.y = 184 * (global_variables.cell_size / 8)
        self.vec = 1
        self.remember_vec = -1
        self.status = "hit-1"
        self.play_dead_sound()
        if self.lives == 0:
            self.dead = True
        else:
            self.paused_time = pygame.time.get_ticks()
            self.paused = 1

    def upd(self, ghosts: List["MainGhost"]):
        global score
        global game_map
        global game_simplified_map

        if self.cherry_on_screen:
            self.update_cherry()

        if self.dots >= 30:
            global_variables.blue_trigger = 1
        if self.dots == 244 * 0.25:
            self.cherry_multiplier = 100
            self.cherry_spawn()
        if self.dots == 244 * 0.50:
            self.cherry_multiplier = 300
            self.cherry_spawn()
        if self.dots == 244 * 0.75:
            self.cherry_multiplier = 500
            self.cherry_spawn()
        if self.dots >= 244 // 3:
            global_variables.orange_trigger = 1
        if self.dots >= 244:
            self.win = True
            img = img_load(f'./textures/pacsprites/pacman9.png', 2 * global_variables.cell_size,
                           2 * global_variables.cell_size)
            self.status_eat = 0
            self.screen.blit(
                img,
                (self.x - (global_variables.cell_size / 2), self.y - (global_variables.cell_size / 2) + 50)
            )

        text_font = pygame.font.SysFont("segoeuisemibold", 16)
        self.screen.blit(text_font.render("Счёт", False, (255, 255, 255)), (0, 0))
        self.screen.blit(text_font.render("Рекорд", False, (255, 255, 255)), (self.screen.get_width() / 2, 0))

        self.screen.blit(text_font.render(f"{score}", False, (255, 255, 255)), (0, 18))
        self.screen.blit(text_font.render(f"{self.best}", False, (255, 255, 255)), (self.screen.get_width() / 2, 18))

        if self.status != 'hit-0' and self.status != 'hit-1' and self.status != 'hit-2' and self.status != 'hit-3':
            self.total_way += 1
            if self.total_way == 20:
                if self.status_eat == 90:
                    self.status_eat = 0
                    self.total_way = 0
                elif self.status_eat == 45:
                    self.status_eat = 90
                    self.total_way = 0
                elif self.status_eat == 0:
                    self.status_eat = 45
                    self.total_way = 0
            self.vel = self.speed
            if self.vec == 0 or self.vec == 3:
                self.x += self.vel * (global_variables.cell_size / 8)
            if self.vec == 1:
                self.y -= self.vel * (global_variables.cell_size / 8)
            if self.vec == 2:
                self.x -= self.vel * (global_variables.cell_size / 8)
            if self.vec == 3:
                self.y += self.vel * (global_variables.cell_size / 8)

        # 1 /\
        # 3 \/
        # 2 <
        # 0 >

        # print(f'{self.x} {self.y} {self.vec} {int(self.x // 8)} {int(self.y // 8)} {self.status} {self.vec}')
        # БЛОК ПРОВЕРКИ НА ЗАПОМИНАНИЯ
        if int(self.x // global_variables.cell_size) + 1 <= 27 and int(self.x // global_variables.cell_size) - 1 >= 0:
            if (game_map[int(self.y // global_variables.cell_size)][
                    int(self.x // global_variables.cell_size) + 1] == 3 or
                game_map[int(self.y // global_variables.cell_size)][
                    int(self.x // global_variables.cell_size) + 1] == 4 or
                game_map[int(self.y // global_variables.cell_size)][
                    int(self.x // global_variables.cell_size) + 1] == 5) and \
                    self.remember_vec == 0 and self.vec != 0:
                self.x = (self.x // global_variables.cell_size) * global_variables.cell_size
                self.y = (self.y // global_variables.cell_size) * global_variables.cell_size
                self.vec = self.remember_vec
                self.status = 'unhit'
                self.remember_vec = -1
            elif (game_map[int(self.y // global_variables.cell_size)][
                      int(self.x // global_variables.cell_size) - 1] == 3 or
                  game_map[int(self.y // global_variables.cell_size)][
                      int(self.x // global_variables.cell_size) - 1] == 4 or
                  game_map[int(self.y // global_variables.cell_size)][
                      int(self.x // global_variables.cell_size) - 1] == 5) and \
                    self.remember_vec == 2 and \
                    self.vec != 2:
                self.x = (self.x // global_variables.cell_size) * global_variables.cell_size
                self.y = (self.y // global_variables.cell_size) * global_variables.cell_size
                self.vec = self.remember_vec
                self.status = 'unhit'
                self.remember_vec = -1
            elif (game_map[int(self.y // global_variables.cell_size) + 1][
                      int(self.x // global_variables.cell_size)] == 3 or
                  game_map[int(self.y // global_variables.cell_size) + 1][
                      int(self.x // global_variables.cell_size)] == 4 or
                  game_map[int(self.y // global_variables.cell_size) + 1][
                      int(self.x // global_variables.cell_size)] == 5) and \
                    self.remember_vec == 3 and \
                    self.vec != 3:
                self.x = (self.x // global_variables.cell_size) * global_variables.cell_size
                self.y = (self.y // global_variables.cell_size) * global_variables.cell_size
                self.vec = self.remember_vec
                self.status = 'unhit'
                self.remember_vec = -1
            elif (game_map[int(self.y // global_variables.cell_size) - 1][
                      int(self.x // global_variables.cell_size)] == 3 or
                  game_map[int(self.y // global_variables.cell_size) - 1][
                      int(self.x // global_variables.cell_size)] == 4 or
                  game_map[int(self.y // global_variables.cell_size) - 1][
                      int(self.x // global_variables.cell_size)] == 5) and \
                    self.remember_vec == 1 and \
                    self.vec != 1:
                self.x = (self.x // global_variables.cell_size) * global_variables.cell_size
                self.y = (self.y // global_variables.cell_size) * global_variables.cell_size
                self.vec = self.remember_vec
                self.status = 'unhit'
                self.remember_vec = -1
        # Дебаг
        # print(f'{self.x} {self.y} {self.vec} '
        #       f'{game_map[int(self.y//global_variables.cell_size)][int(self.x//global_variables.cell_size)]} '
        #       f'{self.status}')
        if self.vec == 1 or self.vec == 3:
            self.x = round(self.x / global_variables.cell_size) * global_variables.cell_size
        if self.vec == 0 or self.vec == 2:
            self.y = round(self.y / global_variables.cell_size) * global_variables.cell_size
        if 0 <= self.x < self.screen.get_width() - global_variables.cell_size:
            # коллизия с зерном
            if game_map[int(self.y // global_variables.cell_size)][int(self.x // global_variables.cell_size)] == 3:
                score += 10
                self.dots += 1
                game_map[int(self.y // global_variables.cell_size)][int(self.x // global_variables.cell_size)] = 5
                game_simplified_map[int(self.y // global_variables.cell_size)][
                    int(self.x // global_variables.cell_size)] = 5
                self.play_munch_sound()
            # коллизия с батарейкой
            if game_map[int(self.y // global_variables.cell_size)][int(self.x // global_variables.cell_size)] == 4:
                self.invincible = 1
                self.eaten = 0
                score += 50
                self.dots += 1
                game_map[int(self.y // global_variables.cell_size)][int(self.x // global_variables.cell_size)] = 5
                game_simplified_map[int(self.y // global_variables.cell_size)][
                    int(self.x // global_variables.cell_size)] = 5
                self.last = pygame.time.get_ticks()
                self.in_energizer = True
                for ghost in ghosts:
                    ghost.scare()

            self._update_energizer_effect(ghosts)

            # коллизия вверх
            if self.vec == 1 and \
                    game_map[int(self.y // global_variables.cell_size)][int(self.x // global_variables.cell_size)] == 0:
                self.vel = 0
                self.y += 1
                self.status = 'hit-1'
                if self.status_eat == 0:
                    self.status_eat = 45
            # коллизия влево
            if self.vec == 2 and \
                    game_map[int(self.y // global_variables.cell_size)][int(self.x // global_variables.cell_size)] == 0:
                self.vel = 0
                self.x += 1
                self.status = 'hit-2'
                if self.status_eat == 0:
                    self.status_eat = 45
            # коллизия вниз
            if self.vec == 3 and \
                    game_map[int((self.y + global_variables.cell_size) // global_variables.cell_size)][
                        int(self.x // global_variables.cell_size)] == 0:
                self.vel = 0
                # self.y-=1
                self.status = 'hit-3'
                if self.status_eat == 0:
                    self.status_eat = 45
            # коллизия вправо
            if self.vec == 0 and \
                    game_map[int(self.y // global_variables.cell_size)][
                        int((self.x + global_variables.cell_size) // global_variables.cell_size)] == 0:
                self.vel = 0
                # self.x-=1
                self.status = 'hit-0'
                if self.status_eat == 0:
                    self.status_eat = 45

        if (self.x - 9) >= self.screen.get_width():
            self.x = -7
            self.y = self.y // global_variables.cell_size * global_variables.cell_size
        if self.x <= -9:
            self.x = self.screen.get_width() - 1
            self.y = self.y // global_variables.cell_size * global_variables.cell_size

        # проверка на призрака
        if not self.invincible and not self.god:
            for ghost in ghosts:
                if ((self.x - ghost.position.x) ** 2 + (
                        self.y - ghost.position.y) ** 2) ** 0.5 <= global_variables.cell_size and \
                        not ghost.ghost_logic.eaten:
                    self.hit(ghosts)

    def process_event(self, event: pygame.event.Event):
        # ПРОВЕРКА НА ПОВОРОТ И ЗАПОМИНАНИЕ В СЛУЧИИ ЕГО ОТСУТСВИЯ
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            if game_map[int(self.y // global_variables.cell_size)][
                int(self.x // global_variables.cell_size) - 1] == 3 or \
                    game_map[int(self.y // global_variables.cell_size)][
                        int(self.x // global_variables.cell_size) - 1] == 5 or \
                    game_map[int(self.y // global_variables.cell_size)][
                        int(self.x // global_variables.cell_size) - 1] == 4 and \
                    self.vec != 2:
                if self.vec == 0 and self.y % 1 >= 0:
                    self.y = int(self.y) + 1
                elif self.vec == 2 and self.y % 1 >= 0:
                    self.y = int(self.y) - 1
                if self.status != 'hit-2':
                    if self.status == 'hit-1' or self.status == 'hit-3' or self.status == 'hit-0' or self.vec == 0:
                        self.status = 'unhit'
                        self.vec = 2
                        self.number_image = 2
                        self.remember_vec = -1
                    else:
                        self.remember_vec = 2
            elif game_map[
                int(self.y // global_variables.cell_size)
            ][
                int(self.x // global_variables.cell_size) - 1
            ] == 0:
                self.remember_vec = 2

        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            if game_map[int(self.y // global_variables.cell_size)][
                int(self.x // global_variables.cell_size) + 1] == 3 or \
                    game_map[int(self.y // global_variables.cell_size)][
                        int(self.x // global_variables.cell_size) + 1] == 5 or \
                    game_map[int(self.y // global_variables.cell_size)][
                        int(self.x // global_variables.cell_size) + 1] == 4 and \
                    self.vec != 0:
                if self.vec == 0 and self.y % 1 >= 0:
                    self.y = int(self.y) + 1
                elif self.vec == 2 and self.y % 1 >= 0:
                    self.y = int(self.y) - 1
                if self.status != 'hit-0':
                    if self.status == 'hit-1' or self.status == 'hit-2' or self.status == 'hit-3' or self.vec == 2:
                        self.status = 'unhit'
                        self.vec = 0
                        self.number_image = 0
                        self.remember_vec = -1
                    else:
                        self.remember_vec = 0
            elif game_map[
                int(self.y // global_variables.cell_size)
            ][
                int(self.x // global_variables.cell_size) + 1
            ] == 0:
                self.remember_vec = 0

        if event.key == pygame.K_w or event.key == pygame.K_UP:
            if game_map[int(self.y // global_variables.cell_size) - 1][
                int(self.x // global_variables.cell_size)] == 3 or \
                    game_map[int(self.y // global_variables.cell_size) - 1][
                        int(self.x // global_variables.cell_size)] == 5 or \
                    game_map[int(self.y // global_variables.cell_size) - 1][
                        int(self.x // global_variables.cell_size)] == 4 and \
                    self.vec != 1:
                if self.vec == 0 and self.x % 1 >= 0:
                    self.x = int(self.x) + 1
                elif self.vec == 2 and self.x % 1 >= 0:
                    self.x = int(self.x) - 1
                if self.status != 'hit-1':
                    if self.status == 'hit-3' or self.status == 'hit-2' or self.status == 'hit-0' or self.vec == 3:
                        self.status = 'unhit'
                        self.vec = 1
                        self.number_image = 1
                        self.remember_vec = -1
                    else:
                        self.remember_vec = 1
            elif game_map[
                int(self.y // global_variables.cell_size) - 1
            ][
                int(self.x // global_variables.cell_size)
            ] == 0:
                self.remember_vec = 1

        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            if game_map[int(self.y // global_variables.cell_size) + 1][
                int(self.x // global_variables.cell_size)] == 3 or \
                    game_map[int(self.y // global_variables.cell_size) + 1][
                        int(self.x // global_variables.cell_size)] == 5 or \
                    game_map[int(self.y // global_variables.cell_size) + 1][
                        int(self.x // global_variables.cell_size)] == 4 and \
                    self.vec != 3:
                if self.vec == 0 and self.x % 1 >= 0:
                    self.x = int(self.x) + 1
                elif self.vec == 2 and self.x % 1 >= 0:
                    self.x = int(self.x) - 1
                if self.status != 'hit-3':
                    if self.status == 'hit-1' or self.status == 'hit-2' or self.status == 'hit-0' or self.vec == 1:
                        self.status = 'unhit'
                        self.vec = 3
                        self.number_image = 3
                        self.remember_vec = -1
                    else:
                        self.remember_vec = 3
            elif game_map[
                int(self.y // global_variables.cell_size) + 1
            ][
                int(self.x // global_variables.cell_size)
            ] == 0:
                self.remember_vec = 3

    def cherry_spawn(self):
        self.cherry_call = pygame.time.get_ticks()
        self.cherry_on_screen = 1

    def update_cherry(self):
        global score
        now = pygame.time.get_ticks()
        if (int(self.cherry_position[0] - self.x) ** 2 +
            int(self.cherry_position[1] + global_variables.cell_size // 2 - self.y) ** 2) ** 0.5 <= \
                global_variables.cell_size:
            self.cherry_on_screen = 0
            score += self.cherry_multiplier
            self.cherry_call = 0xAB0BA
            self.play_eat_ghost_sound()
            return
        if now - self.cherry_call >= 10000:
            self.cherry_on_screen = 0
            self.cherry_call = 0xAB0BA
            return
        elif now - self.cherry_call >= 7000:
            if (now - self.cherry_call) % 1000 >= 500:
                self.screen.blit(
                    self.cherry_img,
                    (self.cherry_position[0], self.cherry_position[1] + 50)
                )
        else:
            self.cherry_position = (100 * (global_variables.cell_size / 8) + global_variables.cell_size / 2, 128 *
                                    (global_variables.cell_size / 8) + global_variables.cell_size / 2)
            self.screen.blit(
                self.cherry_img,
                (self.cherry_position[0], self.cherry_position[1] + 50)
            )
