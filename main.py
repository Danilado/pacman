from menu import options_menu
import argparse
import globalvars

def main():
    parser = argparse.ArgumentParser(description='Pacman')
    parser.add_argument("-g", "--ghostless", help='Disables ghosts on the map', action="store_true")
    args = parser.parse_args()
    if args.ghostless:
        globalvars.ghostless = 1

if __name__ == '__main__':
    main()
    options_menu()
