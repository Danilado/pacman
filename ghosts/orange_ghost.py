from math import sqrt
from typing import List

import pygame

from ghosts.core import AbstractGhostLogic, MainGhost, Direction
from player import Pacman
from layouts import sprited


class OrangeGhostLogic(AbstractGhostLogic):
    # default_position = pygame.Vector2(15 * 8, 13 * 8 + 4)
    default_position = pygame.Vector2(13 * 8 + 4, 10 * 8 + 8)
    default_direction = "left"
    back_animations = ["./textures/ghosts/orange/b1.png", "./textures/ghosts/orange/b2.png"]
    left_animations = ["./textures/ghosts/orange/l1.png", "./textures/ghosts/orange/l2.png"]
    right_animations = ["./textures/ghosts/orange/r1.png", "./textures/ghosts/orange/r2.png"]
    up_animations = ["./textures/ghosts/orange/u1.png", "./textures/ghosts/orange/u2.png"]
    speed = 0.5
    list_normal_tile = ['seed', 5, 'nrg']

    def __init__(self, main_ghost: "MainGhost"):
        super().__init__(main_ghost)
        self.main_ghost = main_ghost

    def find_ways(self):  # 0 - ищем выход из начальной комнаты
        # TODO призрак может телепортироваться на экваторе карты, проверить и везде ли есть границы
        tmp_list_vec = []
        if (self.main_ghost.position[0] + 4) % 8 == 0 and (self.main_ghost.position[1]+4) % 8 == 0:
            if sprited[self.main_ghost.position_in_blocks[1] + 1][(self.main_ghost.position_in_blocks[0])] in \
                    self.list_normal_tile:
                tmp_list_vec.append('back')
            if sprited[self.main_ghost.position_in_blocks[1] - 1][(self.main_ghost.position_in_blocks[0])] in \
                    self.list_normal_tile:
                tmp_list_vec.append('up')
            if sprited[(self.main_ghost.position_in_blocks[1])][self.main_ghost.position_in_blocks[0] + 1] in \
                    self.list_normal_tile:
                tmp_list_vec.append('right')
            if sprited[(self.main_ghost.position_in_blocks[1])][self.main_ghost.position_in_blocks[0] - 1] in \
                    self.list_normal_tile:
                tmp_list_vec.append('left')
        return tmp_list_vec

    def where_am_i_should_move(self, pacman: Pacman, all_ghosts: List[MainGhost]) -> Direction:
        target_pos = [0, 256]
        if sqrt((pacman.x - all_ghosts[0].position[0]) ** 2 + (pacman.y - all_ghosts[0].position[1]) ** 2) > 8:
            target_pos = [pacman.x, pacman.y]
        direction = self.main_ghost.direction
        tmp_list_ways = self.find_ways()
        back_direction = True
        if direction == 'right':
            back_direction = 'left'
        elif direction == 'left':
            back_direction = 'right'
        elif direction == 'up':
            back_direction = 'back'
        elif direction == 'back':
            back_direction = 'up'
        if len(tmp_list_ways) > 2:
            min_range = 100000
            min_vel = 'left'
            for tmp_vel in tmp_list_ways:
                if tmp_vel != back_direction:
                    if tmp_vel == 'right':
                        tmp_range = sqrt((self.main_ghost.position[0] + 8 - target_pos[0]) ** 2 + (
                                self.main_ghost.position[1] - target_pos[1]) ** 2)
                    elif tmp_vel == 'left':
                        tmp_range = sqrt((self.main_ghost.position[0] - 8 - target_pos[0]) ** 2 + (
                                self.main_ghost.position[1] - target_pos[1]) ** 2)
                    elif tmp_vel == 'up':
                        tmp_range = sqrt((self.main_ghost.position[0] - target_pos[0]) ** 2 + (
                                self.main_ghost.position[1] - 8 - target_pos[1]) ** 2)
                    else:
                        tmp_range = sqrt((self.main_ghost.position[0] - target_pos[0]) ** 2 + (
                                self.main_ghost.position[1] + 8 - target_pos[1]) ** 2)

                    if tmp_range < min_range:
                        min_range = tmp_range
                        min_vel = tmp_vel
            direction = min_vel
        elif len(tmp_list_ways) == 2:
            for tmp_vel in tmp_list_ways:
                if tmp_vel != back_direction:
                    direction = tmp_vel
        return direction
