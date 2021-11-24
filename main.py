import argparse

import globalvars
from menu import options_menu


def main():
    parser = argparse.ArgumentParser(description='Pacman')
    parser.add_argument("-b", "--ghostbusters", help='Disables ghosts on the map',      action="store_true")
    parser.add_argument("-i", "--instawin",     help='Makes pacman win instantly',      action="store_true")
    parser.add_argument("-g", "--god",          help='Makes pacman immortal',           action="store_true")
    parser.add_argument("-d", "--debug",        help='Shows ghosts target position',    action="store_true")
    args = parser.parse_args()
    if args.ghostbusters:
        globalvars.ghost_less = 1
        print("Ghosts off")
    if args.instawin:
        globalvars.iwin = 1
        print("Instant win on")
    if args.god:
        globalvars.god = 1
        print("Godmode on")
    if args.debug:
        globalvars.debug = 1
        print("Debug mode on")


if __name__ == '__main__':
    main()
    options_menu()
