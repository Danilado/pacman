import argparse

import global_variables
import store_settings
from game import set_block_size
from menu import options_menu


def load_settings():
    my_settings = store_settings.get_settings()
    if my_settings is not None:
        set_block_size(my_settings.cell_size)
        global_variables.theme_api.textures_mode = my_settings.texture_setting
        global_variables.difficulty = my_settings.difficulty


def main():
    parser = argparse.ArgumentParser(description='Pacman')
    parser.add_argument("-c", "--coop",         help='Disables ghosts on the map', action="store_true")
    parser.add_argument("-i", "--instawin",     help='Makes pacman win instantly', action="store_true")
    parser.add_argument("-g", "--god",          help='Makes pacman immortal',           action="store_true")
    parser.add_argument("-d", "--debug",        help='Shows ghosts target position',    action="store_true")
    args = parser.parse_args()
    if args.coop:
        global_variables.coop = 1
        print("Coop on")
    if args.instawin:
        global_variables.instant_win = 1
        print("Instant win on")
    if args.god:
        global_variables.god = 1
        print("Godmode on")
    if args.debug:
        global_variables.debug = 1
        print("Debug mode on")


if __name__ == '__main__':
    main()
    load_settings()
    options_menu()
