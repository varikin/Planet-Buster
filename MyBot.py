#!/usr/bin/env python
#

from logger import logger, configure_logger
from PlanetWars import Turn

def main():
    map_data = ''
    while(True):
        current_line = raw_input()
        if len(current_line) >= 2 and current_line.startswith("go"):
            turn = Turn(map_data)
            turn.go()
            turn.finish()
            map_data = ''
        else:
            map_data += current_line + '\n'



if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    try:
        configure_logger()
        main()
    except KeyboardInterrupt:
        print 'ctrl-c, leaving ...'
