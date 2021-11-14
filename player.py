from typing import List, TYPE_CHECKING

import pygame

from perfomance import img_load

if TYPE_CHECKING:
    from ghosts.core import MainGhost

black = 0, 0, 0
score = 0
game_map = []
game_simplified_map = []


class Pacman:
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.vec = 0  # 0 - вправо. 1 - вверх. 2 - влево. 3 - вниз.
        self.vel = 1
        self.speed = 0.4
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
        self.current_eat_sound_index = 1

    def draw(self):
        img = img_load(f'./textures/pacsprites/pacman{self.vec}.png')
        img = pygame.transform.scale(img, (16, 16))
        # pygame.draw.rect(self.screen, (255, 255, 0), (self.x, self.y, 8, 8), 1)
        self.screen.blit(img, (self.x - 4, self.y - 4))

    def play_dead_sound(self):
        if not self.dead_sound_playing:
            self.dead_channel.play(self.dead_sound)
            self.dead_sound_playing = True
        return self.dead_channel.get_busy()

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
            rect = pygame.rect.Rect(self.x - 4, self.y - 4, 8, 8)
            for ghost in ghosts:
                if rect.colliderect(ghost.position):
                    score += 200 * (2 ** self.eaten)
                    self.eaten += 1
                    print(f'{self.eaten} {score}')
                    ghost.reset_position()
                    self.play_eat_ghost_sound()
        if now - self.last >= 7000:
            self.invincible = 0
            self.in_energizer = False

    def upd(self, ghosts: List["MainGhost"]):
        global score
        global game_map
        global game_simplified_map

        if self.status != 'hit-0' and self.status != 'hit-1' and self.status != 'hit-2' and self.status != 'hit-3':
            self.vel = self.speed
            if self.vec == 0 or self.vec == 3:
                self.x += self.vel
            if self.vec == 1:
                self.y -= self.vel
            if self.vec == 2:
                self.x -= self.vel
            if self.vec == 3:
                self.y += self.vel

        # Дебаг
        # print(f'{self.x} {self.y} {self.vec} {map[int(self.y//8)][int(self.x//8)]} {self.status}')
        if self.vec == 1 or self.vec == 3:
            self.x = round(self.x / 8) * 8
        if self.vec == 0 or self.vec == 2:
            self.y = round(self.y / 8) * 8
        if 0 <= self.x < self.screen.get_width() - 8:
            # коллизия с зерном
            if game_map[int(self.y // 8)][int(self.x // 8)] == 3:
                score += 10
                game_map[int(self.y // 8)][int(self.x // 8)] = 5
                game_simplified_map[int(self.y // 8)][int(self.x // 8)] = 5
                self.play_munch_sound()
            # коллизия с батарейкой
            if game_map[int(self.y // 8)][int(self.x // 8)] == 4:
                self.invincible = 1
                self.eaten = 0
                score += 50
                game_map[int(self.y // 8)][int(self.x // 8)] = 5
                game_simplified_map[int(self.y // 8)][int(self.x // 8)] = 5
                self.last = pygame.time.get_ticks()
                self.in_energizer = True

            self._update_energizer_effect(ghosts)

            # коллизия вверх
            if self.vec == 1 and game_map[int(self.y // 8)][int(self.x // 8)] == 0:
                self.vel = 0
                self.y += 1
                self.status = 'hit-1'
            # коллизия влево
            if self.vec == 2 and game_map[int(self.y // 8)][int(self.x // 8)] == 0:
                self.vel = 0
                self.x += 1
                self.status = 'hit-2'
            # коллизия вниз
            if self.vec == 3 and game_map[int((self.y + 8) // 8)][int(self.x // 8)] == 0:
                self.vel = 0
                # self.y-=1
                self.status = 'hit-3'
            # коллизия вправо
            if self.vec == 0 and game_map[int(self.y // 8)][int((self.x + 8) // 8)] == 0:
                self.vel = 0
                # self.x-=1
                self.status = 'hit-0'

        if (self.x - 9) >= self.screen.get_width():
            self.x = -7
            self.y = self.y // 8 * 8
        if self.x <= -9:
            self.x = self.screen.get_width() - 1
            self.y = self.y // 8 * 8

        # проверка на призрака
        if not self.invincible:
            rect = pygame.rect.Rect(self.x + 4, self.y + 4, 8, 8)
            for ghost in ghosts:
                if rect.colliderect(ghost.position):
                    self.lives -= 1
                    if self.lives == 0:
                        self.dead = True
                        break

    def process_event(self, event: pygame.event.Event):
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            if self.status != 'hit-2':
                self.status = 'unhit'
                self.vec = 2
                self.number_image = 2

        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            if self.status != 'hit-0':
                self.status = 'unhit'
                self.vec = 0
                self.number_image = 0

        if event.key == pygame.K_w or event.key == pygame.K_UP:
            if self.status != 'hit-1':
                self.status = 'unhit'
                self.vec = 1
                self.number_image = 1

        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
            if self.status != 'hit-3':
                self.status = 'unhit'
                self.vec = 3
                self.number_image = 3
