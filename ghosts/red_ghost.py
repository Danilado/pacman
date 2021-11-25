from math import sqrt
from random import randint

import pygame

from ghosts.core import AbstractGhostLogic, MainGhost, Direction
from player import Pacman
from layouts import simplified
from layouts import sprited


class RedGhostLogic(AbstractGhostLogic):
    """Пример логики призрака"""

    default_position = pygame.Vector2(13*8+ 4,11*8)
    default_direction = "left"
    back_animations = ["./textures/ghosts/red/b1.png", "./textures/ghosts/red/b2.png"]
    left_animations = ["./textures/ghosts/red/l1.png", "./textures/ghosts/red/l2.png"]
    right_animations = ["./textures/ghosts/red/r1.png", "./textures/ghosts/red/r2.png"]
    up_animations = ["./textures/ghosts/red/u1.png", "./textures/ghosts/red/u2.png"]
    scared_animations_blue = []
    speed = 0.3333
    flag = 1
    list_normal_tile = ['seed', 5, 'nrg']

    def __init__(self, main_ghost: "MainGhost"):
        super().__init__(main_ghost)
        self.prev_block = (0, 0)
        self.main_ghost = main_ghost
        self.stay = 0
        self.eaten = 0
        self.trigger = 0

    def my_position_in_blocks(self):
        return int((self.main_ghost.position.x + 4) // 8), int((self.main_ghost.position.y + 4) // 8)

    def find_ways(self):  # 0 - ищем выход из начальной комнаты
        tmp_list_vec = []
        if (self.main_ghost.position[0]) % 8 == 0 and (self.main_ghost.position[1]) % 8 == 0 and self.prev_block != (
                self.main_ghost.position[0], self.main_ghost.position[1]):
            self.prev_block = (self.main_ghost.position[0], self.main_ghost.position[1])
            if len(sprited[0]) <= self.my_position_in_blocks()[0] + 1 or self.my_position_in_blocks()[0] - 1 < 0:
                tmp_list_vec.append('ll')
                return tmp_list_vec
            if sprited[self.my_position_in_blocks()[1] + 1][
                (self.my_position_in_blocks()[0])] in self.list_normal_tile:
                tmp_list_vec.append('back')
            if sprited[self.my_position_in_blocks()[1] - 1][
                (self.my_position_in_blocks()[0])] in self.list_normal_tile:
                tmp_list_vec.append('up')
            if sprited[(self.my_position_in_blocks()[1])][
                self.my_position_in_blocks()[0] + 1] in self.list_normal_tile:
                tmp_list_vec.append('right')
            if sprited[(self.my_position_in_blocks()[1])][
                self.my_position_in_blocks()[0] - 1] in self.list_normal_tile:
                tmp_list_vec.append('left')
        return tmp_list_vec

    def select_tile(self, target_pos):
        direction = self.main_ghost.direction
        tmp_list_ways = self.find_ways()
        if direction == 'right':
            back_direction = 'left'
        elif direction == 'left':
            back_direction = 'right'
        elif direction == 'up':
            back_direction = 'back'
        elif direction == 'back':
            back_direction = 'up'
        else:
            back_direction = ''
        if len(tmp_list_ways) == 1 and tmp_list_ways[0] == 'll':
            return back_direction
        elif len(tmp_list_ways) > 2:
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

    def acceleration_stage(self):
        target_pos = [224, 0]
        return self.select_tile(target_pos)

    def chase_stage(self, pacman):
        target_pos = [pacman.x, pacman.y]
        return self.select_tile(target_pos)

    def scared_stage(self):
        target_pos = [self.main_ghost.position.x + randint(-1, 1)*8, self.main_ghost.position.y + randint(-1, 1)*8]
        return self.select_tile(target_pos)

    def gohome(self):
        self.main_ghost.reset_position()
        self.main_ghost.direction = "right"
        self.stage = 1

    def stay_stage(self, trigger):
        self.default_direction = "right"
        if (self.main_ghost.position[1]) % 8 == 0:
            if sprited[self.my_position_in_blocks()[1] + 1][
                (self.main_ghost.position_in_blocks[0])] == 'gate':
                self.stay = 0
                self.prev_block = (self.main_ghost.position[0], self.main_ghost.position[1])
                return 'right'
            else:
                return "up"
        else:
            return 'up'

    def eaten_stage(self):
        target_pos = [13*8+ 4,11*8]
        print(self.eaten, self.main_ghost.position)
        if self.eaten == 1:
            self.speed = 1
            if self.main_ghost.position.x != target_pos[0] or self.main_ghost.position.y != target_pos[1]:
                return self.select_tile(target_pos)
            else:
                self.eaten = 2
                return 'back'
        elif self.eaten == 2:
            if self.main_ghost.position.y != 14 * 8:
                return 'back'
            else:
                self.eaten = 0
                self.speed = 0.3
                self.stay = 1
                return 'up'

    def where_am_i_should_move(self, pacman: Pacman, all_ghosts, stage=1,
                               trigger=0) -> Direction:  ## 1 - стадия разгона, 2 - стадия преследования, 3 - страх

        if self.stay:
            return self.stay_stage(1)
        elif self.eaten:
            return self.eaten_stage()
        elif self.main_ghost.scared:
            return self.scared_stage()
        elif stage == 1:
            return self.chase_stage(pacman)
        elif stage == 2:
            return self.acceleration_stage()
        return 'back'
