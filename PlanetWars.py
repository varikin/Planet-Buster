#!/usr/bin/env python
#

from math import ceil, sqrt
from sys import stdout
from operator import attrgetter
from logger import logger


NEUTRAL = 0
MINE = 1
ENEMY = 2

class Turn:
    def __init__(self, turn_data):
        game_state = GameState(turn_data)
        self.planets = game_state.planets
        self.fleets = game_state.fleets
        
    def go(self):
        logger.debug("Go time")
        for planet in self.planets[MINE]:
            target = self.findBestTarget(planet)
            if target is not None:
                incoming = self.getIncomingAttacks(planet)
                enroute = self.getEnrouteAttacks(planet)
                needed_ships = target.num_ships - enroute + 1
                if needed_ships < incoming:
                    planet.attack(target, needed_ships)
            else:
                target = self.findBestNeutralTarget(planet)
                if target is not None:
                    planet.attack(target, target.num_ships + 1)
                
    
    def findBestNeutralTarget(self, planet):
        logger.debug("Finding the best neutral target")
        other_planets = self.planets[NEUTRAL]
        other_planets.sort(key=attrgetter('growth_rate'))
        top_planets = [p for p in other_planets if planet.num_ships > p.num_ships][:5]
        logger.debug("Best neutral targets: %s" % top_planets)
        
        closest = None
        distance = 0
        for top_planet in top_planets:
            new_distance = planet.distanceFrom(top_planet)
            if closest is None or new_distance < distance:
                closest = top_planet
                distance = new_distance
        
        logger.debug("Closest neutral: %s" % closest)
        return closest
    
    def findBestTarget(self, planet):
        # Find the largest 5 producers and then find the closest
        logger.debug("Finding best target")
        other_planets = self.planets[ENEMY]
        other_planets.sort(key=attrgetter('growth_rate'))
        top_planets = [p for p in other_planets if planet.num_ships > p.num_ships][:5]
        logger.debug("Best planets: %s" % top_planets)

        closest = None
        distance = 0
        for top_planet in top_planets:
            new_distance = planet.distanceFrom(top_planet)
            if closest is None or new_distance < distance:
                closest = top_planet
                distance = new_distance

        logger.debug("Closest target: %s" % closest)
        return closest
    
    def getEnrouteAttacks(self, planet):
        logger.debug("Getting enroute attacks")
        enroute = 0
        for fleet in self.fleets[MINE]:
            if fleet.target == planet.id:
                enroute += fleet.num_ships
        logger.debug("Planet %d has %d enroute ships" % (planet.id, enroute))
        return enroute
    
    def getIncomingAttacks(self, planet):
        logger.debug("Getting incoming attacks")
        incoming = 0
        for fleet in self.fleets[ENEMY]:
            if fleet.target == planet.id:
                incoming += fleet.num_ships
        logger.debug("Planet %d has %d incoming ships" % (planet.id, incoming))
        return incoming


    def finish(self):
        stdout.write("go\n")
        stdout.flush()

class Fleet:
    def __init__(self, owner, num_ships, source, target, \
            total_trip_length, turns_remaining):
        self.owner = owner
        self.num_ships = num_ships
        self.source = source
        self.target = target
        self.total_trip_length = total_trip_length
        self.turns_remaining = turns_remaining

    def __str__(self):
        return "F %d %d %d %d %d %d\n" % \
            (self.owner, self.num_ships, self.source, self.target, \
            self.total_trip_length, self.turns_remaining)


class Planet:
    def __init__(self, id, owner, num_ships, growth_rate, x, y):
        self.id = id
        self.owner = owner
        self.num_ships = num_ships
        self.growth_rate = growth_rate
        self.x = x
        self.y = y

    def __str__(self):
        return "P %f %f %d %d %d\n" % (self.x, self.y, self.owner, self.num_ships, self.growth_rate)

    def __repr__(self):
        return str(self)
    
    def attack(self, target, num_ships):
        logger.debug("Attacking %s" % target)
        self.num_ships -= num_ships
        attack = "%d %d %d\n" % (self.id, target.id, num_ships)
        stdout.write(attack)
        stdout.flush()
        logger.debug("Attack message: %s" % attack)
        

    def distanceFrom(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        return int(ceil(sqrt(dx * dx + dy * dy)))

class GameState:
    def __init__(self, gameState):
        logger.debug("Parsing the game state")
        self.planets = {NEUTRAL: [], MINE:[], ENEMY:[]}
        self.fleets = {MINE:[],ENEMY:[]}
        self.num_planets = 0

        lines = gameState.split("\n")
        for line in lines:
            line = line.split("#")[0] # remove comments
            tokens = line.split(" ")
            if len(tokens) == 1:
                continue
            if tokens[0] == "P":
                self.parsePlanet(tokens)
            elif tokens[0] == "F":
                self.parseFleet(tokens)
            else:
                msg = "Error parseing the game state"
                logger.debug(msg)
                raise ValueError(msg)
    
    def parseFleet(self, tokens):
        if len(tokens) != 7:
            msg = "Incorrect number of fleet tokens"
            logger.debug("Incorrect number of fleet tokens")
            raise ValueError(msg)
        f = Fleet(int(tokens[1]), # Owner
                  int(tokens[2]), # Num ships
                  int(tokens[3]), # Source
                  int(tokens[4]), # Destination
                  int(tokens[5]), # Total trip length
                  int(tokens[6])) # Turns remaining
        self.fleets[f.owner].append(f)
    
    def parsePlanet(self, tokens):
        if len(tokens) != 6:
            msg = "Incorrect number of planet tokens"
            logger.debug(msg)
            raise ValueError(msg)
        p = Planet(self.num_planets, # The ID of this planet
                   int(tokens[3]), # Owner
                   int(tokens[4]), # Num ships
                   int(tokens[5]), # Growth rate
                   float(tokens[1]), # X
                   float(tokens[2])) # Y
        self.num_planets += 1
        self.planets[p.owner].append(p)

