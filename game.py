from typing import List

import pygame

import globalvars
import player
from ghosts.blue_ghost import BlueGhostLogic
from ghosts.core import MainGhost
from ghosts.orange_ghost import OrangeGhostLogic
from ghosts.pink_ghost import PinkGhostLogic
from ghosts.red_ghost import RedGhostLogic
from layouts import map_with_sprites
from layouts import simplified
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
                window.blit(img_load(f'./textures/walls/{globalvars.texture_modifier}{matrix[i][j]}.png'),
                            (8 * j, 8 * i + 50))
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
    player.game_simplified_map = [i.copy() for i in map_with_sprites]
    player.game_map = [i.copy() for i in simplified]
    player.score = 0
    screen = pygame.display.set_mode(resolution)
    done = False
    pac = player.Pacman(w / 2 - 4, h / 2 + 6 * 8 + 8 - 40, screen)
    last_time = 0
    local_stage = 1
    flag = 0

    ghosts: List[MainGhost] = []
    if not globalvars.ghost_less:
        orange_ghost = MainGhost(OrangeGhostLogic, screen)
        red_ghost = MainGhost(RedGhostLogic, screen)
        pink_ghost = MainGhost(PinkGhostLogic, screen)
        blue_ghost = MainGhost(BlueGhostLogic, screen)
        ghosts = [orange_ghost, red_ghost, pink_ghost, blue_ghost]

    audio_sound = pygame.mixer.Sound("./sounds/game_start.wav")
    audio_channel = pygame.mixer.Channel(0)
    audio_channel.play(audio_sound)

    clock = pygame.time.Clock()
    stage = 1

    if not globalvars.ghost_less:
        for ghost in ghosts:
            globalvars.blue_trigger = 0
            globalvars.orange_trigger = 0
            ghost.reset_position()

    while not done:
        trigger = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                pac.process_event(event)
                if event.key == pygame.K_p:
                    pause(clock)
        screen.fill((0, 0, 0))
        render(screen, player.game_simplified_map)
        # MainGhost.draw_trigger_blocks(screen)
        if not globalvars.ghost_less:
            for ghost in ghosts:
                ghost.draw(screen)

            if ghosts[0].scared and not flag:
                print("Scare detected")
                last_time += 7000
                flag = 1
            if local_stage == 1:
                if pygame.time.get_ticks() - last_time >= 20000:
                    local_stage = 2
                    flag = 0
                    print("Set AI mode runaway")
                    for ghost in ghosts:
                        if ghost.ghost_logic.stay == 0:
                            ghost.ghost_logic.stage = 2
                            stage = 2
                    last_time = pygame.time.get_ticks()
            if local_stage == 2:
                if pygame.time.get_ticks() - last_time >= 7000:
                    local_stage = 1
                    flag = 0
                    print("Set AI mode chase")
                    for ghost in ghosts:
                        if ghost.ghost_logic.stay == 0:
                            ghost.ghost_logic.stage = 1
                            stage = 1
                    last_time = pygame.time.get_ticks()

        elif not audio_channel.get_busy() and not pac.dead and not pac.win:
            pac.upd([])

        if pygame.time.get_ticks() % 500 < 250 or not audio_channel.get_busy() and not pac.paused:
            pac.draw()
        if not audio_channel.get_busy() and not pac.dead and not pac.win and not globalvars.ghost_less and not pac.paused:
            pac.upd(ghosts)
            for ghost in ghosts:
                ghost.update(pac, ghosts, stage, trigger)
            
        if pac.paused:
            if pygame.time.get_ticks() - pac.paused_time >= 2500:
                pac.paused = 0
                pac.paused_frame = 0
                pac.status = 'unhit'
                pac.vec = 0
            if pygame.time.get_ticks() % 500 < 250:
                pac.status_eat = 0
                pac.draw()


        done = done or (pac.dead and not pac.play_dead_sound()) or (pac.win and not pac.play_win_sound())
        pygame.display.flip()
        clock.tick(120)
