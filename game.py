from typing import List

import pygame

import globalvars
import player
from ghosts.blue_ghost import BlueGhostLogic
from ghosts.core import MainGhost
from ghosts.orange_ghost import OrangeGhostLogic
from ghosts.pink_ghost import PinkGhostLogic
from ghosts.red_ghost import RedGhostLogic
from ghosts.sounds import Sound
from layouts import map_with_sprites
from layouts import simplified
from perfomance import img_load

resolution = w, h = 224, 336
last_time = 0
local_stage = 1


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


def pause(clock: pygame.time.Clock, screen):
    global last_time
    global local_stage
    save = pygame.time.get_ticks()
    paused = True
    pygame.mixer.pause()
    pause_icon = img_load(f'./textures/pause.png')
    print("Game paused...")
    while paused:
        if pygame.time.get_ticks() % 1000 < 500:
            screen.blit(pause_icon, (screen.get_width() - 32, 0))
        else:
            screen.fill((0, 0, 0), (screen.get_width() - 32, 0, 32, 32))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("Resuming...")
                    paused = False
                    pygame.mixer.unpause()
                    last_time += pygame.time.get_ticks() - save
        pygame.display.update()
        clock.tick(120)


def main():
    player.game_simplified_map = [i.copy() for i in map_with_sprites]
    player.game_map = [i.copy() for i in simplified]
    player.score = 0
    globalvars.dots = 0
    screen = pygame.display.set_mode(resolution)
    done = False
    pac1 = player.Pacman(w / 2 - 4, h / 2 + 6 * 8 + 8 - 40, screen, 1)
    globalvars.pacs = [pac1]
    if globalvars.coop:
        pac2 = player.Pacman(w / 2 - 4, h / 2 + 6 * 8 + 8 - 136, screen, 2)
        globalvars.pacs.append(pac2)
    flag = 0

    global last_time
    global local_stage

    ghosts: List[MainGhost] = []
    if not globalvars.coop:
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

    if not globalvars.coop:
        for ghost in ghosts:
            globalvars.blue_trigger = 0
            globalvars.orange_trigger = 0
            ghost.reset_position()

    Sound().current_sound_index = 1

    while not done:
        trigger = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    pygame.mixer.pause()
                for pac in globalvars.pacs:
                    if not audio_channel.get_busy() and not pac.dead_channel.get_busy() and \
                            not pac.win_channel.get_busy():
                        pac.process_event(event)
                if event.key == pygame.K_p:
                    pause(clock, screen)
        screen.fill((0, 0, 0))
        render(screen, player.game_simplified_map)
        # MainGhost.draw_trigger_blocks(screen)
        if not globalvars.coop:
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
                    if globalvars.debug:
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
                    if globalvars.debug:
                        print("Set AI mode chase")
                    for ghost in ghosts:
                        if ghost.ghost_logic.stay == 0:
                            ghost.ghost_logic.stage = 1
                            stage = 1
                    last_time = pygame.time.get_ticks()

        elif not audio_channel.get_busy() and not pac1.dead and not pac1.win:
            for pac in globalvars.pacs:
                pac.upd([])

        for pac in globalvars.pacs:
            if pygame.time.get_ticks() % 500 < 250 or not audio_channel.get_busy() and not pac.paused:
                pac.draw()
            if not audio_channel.get_busy() and not pac.dead and not pac.win and \
                    not globalvars.coop and not pac.paused:
                if pac.in_energizer:
                    Sound().play_energizer_sound()
                else:
                    Sound().play_siren()
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
