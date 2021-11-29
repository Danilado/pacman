import argparse

import globalvars
import store_settings
from menu import options_menu


def load_settings():
    my_settings = store_settings.get_settings()
    if my_settings is not None:
        globalvars.texture_modifier = my_settings.texture_modifier
        globalvars.difficulty = my_settings.difficulty


def main():
    parser = argparse.ArgumentParser(description='Pacman')
    parser.add_argument("-c", "--coop", help='Disables ghosts on the map',      action="store_true")
    parser.add_argument("-i", "--instawin",     help='Makes pacman win instantly',      action="store_true")
    parser.add_argument("-g", "--god",          help='Makes pacman immortal',           action="store_true")
    parser.add_argument("-d", "--debug",        help='Shows ghosts target position',    action="store_true")
    args = parser.parse_args()
    if args.coop:
        globalvars.ghost_less = 1
        print("Coop on")
    if args.instawin:
        globalvars.instant_win = 1
        print("Instant win on")
    if args.god:
        globalvars.god = 1
        print("Godmode on")
    if args.debug:
        globalvars.debug = 1
        print("Debug mode on")


if __name__ == '__main__':
    main()
    load_settings()
    options_menu()
