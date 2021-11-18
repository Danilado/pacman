from typing import List

import pygame

from ghosts.core import AbstractGhostLogic, MainGhost, Direction
from player import Pacman
import globalvars
from layouts import simplified as game_map


class RedGhostLogic(AbstractGhostLogic):
    """Пример логики призрака"""

    default_position = pygame.Vector2(13 * 8 + 4, 10 * 8 + 8)
    default_direction = "left"
    back_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}b1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}b2.png"]
    left_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}l1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}l2.png"]
    right_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}r1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}r2.png"]
    up_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}u1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}u2.png"]
    speed = 0.3

    def __init__(self, main_ghost: "MainGhost"):
        super().__init__(main_ghost)
        self.main_ghost = main_ghost
        self.timeout = 0
        self.timer = 0
        global back_animations
        global left_animations
        global right_animations
        global up_animations
        back_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}b1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}b2.png"]
        left_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}l1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}l2.png"]
        right_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}r1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}r2.png"]
        up_animations = [f"./textures/ghosts/red/{globalvars.texture_modifier}u1.png", f"./textures/ghosts/red/{globalvars.texture_modifier}u2.png"]

    def where_am_i_should_move(self, pacman: Pacman, all_ghosts: List["MainGhost"], stage, trigger) -> Direction:

        # pygame.draw.rect(self.main_ghost.screen, (255, 0, 0), (pacman.x, pacman.y, 8, 8), 1)

        if self.timeout == 0:
            if list(self.main_ghost.position_in_blocks) in self.main_ghost.trigger_blocks:  # я где
                dirs = {}
                direction = ''
                if game_map[self.main_ghost.position_in_blocks[1] - 1][self.main_ghost.position_in_blocks[0]] != 0:
                    dirs['up'] = ((pacman.x - self.main_ghost.position.x) ** 2
                                  + (pacman.y - (self.main_ghost.position.y - 8)) ** 2) ** 0.5
                    direction = 'up'
                if game_map[self.main_ghost.position_in_blocks[1] + 1][self.main_ghost.position_in_blocks[0]] != 0:
                    dirs['back'] = ((pacman.x - self.main_ghost.position.x) ** 2
                                    + (pacman.y - (self.main_ghost.position.y + 8)) ** 2) ** 0.5
                    if not direction:
                        direction = 'back'
                    elif dirs[direction] > dirs['back']:
                        direction = 'back'
                if game_map[self.main_ghost.position_in_blocks[1]][self.main_ghost.position_in_blocks[0] - 1] != 0:
                    dirs['left'] = ((pacman.x - (self.main_ghost.position.x - 8)) ** 2
                                    + (pacman.y - self.main_ghost.position.y) ** 2) ** 0.5
                    if not direction:
                        direction = 'left'
                    elif dirs[direction] > dirs['left']:
                        direction = 'left'
                if game_map[self.main_ghost.position_in_blocks[1]][self.main_ghost.position_in_blocks[0] + 1] != 0:
                    dirs['right'] = ((pacman.x - (self.main_ghost.position.x + 8)) ** 2
                                     + (pacman.y - self.main_ghost.position.y) ** 2) ** 0.5
                    if not direction:
                        direction = 'right'
                    elif dirs[direction] > dirs['right']:
                        direction = 'right'
                self.timeout = 1
                self.timer = 27

                if direction == "up" or direction == "back":
                    self.main_ghost._position.x = self.main_ghost.position_in_blocks[0]*8
                else:
                    self.main_ghost._position.y = self.main_ghost.position_in_blocks[1]*8
                return direction
        else:
            self.timer -= 1
            if self.timer == 0:
                self.timeout = 0
        return self.main_ghost.direction
