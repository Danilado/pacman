import argparse

import global_vars
import store_settings
from menu import options_menu


def load_settings():
    my_settings = store_settings.get_settings()
    if my_settings is not None:
        global_vars.texture_modifier = my_settings.texture_modifier
        global_vars.difficulty = my_settings.difficulty


def main():
    parser = argparse.ArgumentParser(description='Pacman')
    parser.add_argument("-b", "--ghostbusters", help='Disables ghosts on the map',      action="store_true")
    parser.add_argument("-i", "--instawin",     help='Makes pacman win instantly',      action="store_true")
    parser.add_argument("-g", "--god",          help='Makes pacman immortal',           action="store_true")
    parser.add_argument("-d", "--debug",        help='Shows ghosts target position',    action="store_true")
    args = parser.parse_args()
    if args.ghostbusters:
        global_vars.ghost_less = 1
        print("Ghosts off")
    if args.instawin:
        global_vars.instant_win = 1
        print("Instant win on")
    if args.god:
        global_vars.god = 1
        print("Godmode on")
    if args.debug:
        global_vars.debug = 1
        print("Debug mode on")


if __name__ == '__main__':
    main()
    load_settings()
    options_menu()
