#!/usr/bin/env python
#

"""
// The DoTurn function is where your code goes. The PlanetWars object contains
// the state of the game, including information about all planets and fleets
// that currently exist. Inside this function, you issue orders using the
// pw.IssueOrder() function. For example, to send 10 ships from planet 3 to
// planet 8, you would say pw.IssueOrder(3, 8, 10).
//
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own. Check out the tutorials and articles on the contest website at
// http://www.ai-contest.com/resources.
"""

import logging
from PlanetWars import PlanetWars

logger = logging.getLogger("BotLogger")

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

def DoTurn(pw):
    logger.debug("Doing turn")
    for planet in pw.MyPlanets():
        logger.debug("Working with planet %s" % planet)
        target =  planet.findBestTarget(pw)
        if target is not None and planet.num_ships > target.num_ships:
            num_ships = target.num_ships + 1
            pw.IssueOrder(planet.planet_id, target.planet_id, num_ships)
    logger.debug("Turn complete")


def main():
    map_data = ''
    turn = 1
    while(True):
        current_line = raw_input()
        if len(current_line) >= 2 and current_line.startswith("go"):
            logger.debug("Turn %d: %s" % (turn, current_line))
            turn += 1
            pw = PlanetWars(map_data)
            DoTurn(pw)
            pw.FinishTurn()
            map_data = ''
        else:
            map_data += current_line + '\n'


def configureLogger():
    logger.setLevel("logging.DEBUG")
    logger.addHandler(NullHandler())
    logger.debug("Starting")

if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    try:
        configureLogger()
        main()
    except KeyboardInterrupt:
        print 'ctrl-c, leaving ...'
