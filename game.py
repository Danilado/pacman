from typing import List

import pygame

import globalvars

import player
from ghosts.blue_ghost import BlueGhostLogic
from ghosts.core import MainGhost
from ghosts.orange_ghost import OrangeGhostLogic
from ghosts.pink_ghost import PinkGhostLogic
from ghosts.red_ghost import RedGhostLogic
from layouts import simplified
from layouts import sprited
from perfomance import img_load

resolution = w, h = 224, 336


def render(window, matrix):  # Моя функция рендера карты и зёрен
    for i in range(len(matrix)):  # Y
        for j in range(len(matrix[i])):
            # X
            if matrix[i][j] == 5:
                pygame.draw.rect(window, (0, 0, 0), (8 * j, 8 * i + 50, 8, 8), 1)
                # Пустота окрашивается в чёрное   но зачем ?
            else:
                window.blit(img_load(f'./textures/walls/{globalvars.texture_modifier}{matrix[i][j]}.png'), (8 * j, 8 * i + 50))
                # Всё остальное отрисовывается


def pause(clock: pygame.time.Clock):
    paused = True
    print("paused")
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("un paused")
                    paused = False

        pygame.display.update()
        clock.tick(15)


def main():
    player.game_simplified_map = [i.copy() for i in sprited]
    player.game_map = [i.copy() for i in simplified]
    player.score = 0
    screen = pygame.display.set_mode(resolution)
    done = False
    pac = player.Pacman(w / 2 - 4, h / 2 + 6 * 8 + 8 - 40, screen)

    if not globalvars.ghostless:
        orange_ghost = MainGhost(OrangeGhostLogic, screen)
        red_ghost = MainGhost(RedGhostLogic, screen)
        pink_ghost = MainGhost(PinkGhostLogic, screen)
        blue_ghost = MainGhost(BlueGhostLogic, screen)
        ghosts: List[MainGhost] = [orange_ghost, red_ghost, pink_ghost, blue_ghost]

    audio_sound = pygame.mixer.Sound("./sounds/game_start.wav")
    audio_channel = pygame.mixer.Channel(0)
    audio_channel.play(audio_sound)

    clock = pygame.time.Clock()
    stage = 1
    while not done:
        trigger = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if not audio_channel.get_busy() and not pac.dead:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    pac.process_event(event)
                    if event.key == pygame.K_p:
                        pause(clock)
                    if event.key == pygame.K_r: 
                        trigger = 1
                    if event.key == pygame.K_e:
                        stage = 2
                    if event.key == pygame.K_q:
                        stage = 1
        screen.fill((0, 0, 0))
        render(screen, player.game_simplified_map)
        # MainGhost.draw_trigger_blocks(screen)

        if not globalvars.ghostless:
            for ghost in ghosts:
                ghost.draw(screen)

            if not audio_channel.get_busy() and not pac.dead:
                pac.upd(ghosts)
                for ghost in ghosts:
                    # TODO сделать тригеры и стадии игры (я чутка поправил код, чтобы до логики дошли тригер и стадия
                    ghost.update(pac, ghosts, stage, trigger)
        elif not audio_channel.get_busy() and not pac.dead: 
            pac.upd([])

        if pygame.time.get_ticks() % 16 <= 10 or not audio_channel.get_busy():
            pac.draw()
        done = done or (pac.dead and not pac.play_dead_sound())
        pygame.display.flip()
        clock.tick(120)
