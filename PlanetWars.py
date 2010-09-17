#!/usr/bin/env python
#

from math import ceil, sqrt
from sys import stdout
import logging


logger = logging.getLogger("BotLogger")

class Fleet:
    def __init__(self, owner, num_ships, source_planet, destination_planet, \
            total_trip_length, turns_remaining):
        self.owner = owner
        self.num_ships = num_ships
        self.source_planet = source_planet
        self.destination_planet = destination_planet
        self.total_trip_length = total_trip_length
        self.turns_remaining = turns_remaining

    def __str__(self):
        return "F %d %d %d %d %d %d\n" % \
            (self.owner, self.num_ships, self.source_planet, self.destination_planet, \
            self.total_trip_length, self.turns_remaining)





class Planet:
    def __init__(self, planet_id, owner, num_ships, growth_rate, x, y):
        self.planet_id = planet_id
        self.owner = owner
        self.num_ships = num_ships
        self.growth_rate = growth_rate
        self.x = x
        self.y = y

    def __str__(self):
        return "P %f %f %d %d %d\n" % (self.x, self.y, self.owner, self.num_ships, self.growth_rate)

    def __repr__(self):
        return str(self)

    def AddShips(self, amount):
        self.num_ships += amount

    def RemoveShips(self, amount):
        self.num_ships -= amount

    def findBestTarget(self, pw):
        # Find the largest 5 producers and then find the closest
        other_planets = pw.NotMyPlanets()
        #other_planets.sort(key=Planet.growth_rate)
        top_planets = [p for p in other_planets if self.num_ships > p.num_ships][:5]
        logger.debug("Top planets: %s" % top_planets)

        closest = None
        distance = 0
        for planet in top_planets:
            new_distance = self.distanceFrom(planet)
            if closest is None or new_distance < distance:
                closest = planet
                distance = new_distance
        logger.debug("Closets: %s" % closest)
        return closest

    def distanceFrom(self, otherPlanet):
        dx = self.x - otherPlanet.x
        dy = self.y - otherPlanet.y
        return int(ceil(sqrt(dx * dx + dy * dy)))

class PlanetWars:
    def __init__(self, gameState):
        self.planets = []
        self.fleets = []
        logger.debug("Parsing game state")
        self.ParseGameState(gameState)
        logger.debug("Game state parsed")

    def NumPlanets(self):
        return len(self.planets)

    def GetPlanet(self, planet_id):
        return self.planets[planet_id]

    def NumFleets(self):
        return len(self.fleets)

    def MyPlanets(self):
        logger.debug("Getting my planets")
        return [p for p in self.planets if p.owner == 1]

    def NeutralPlanets(self):
        r = []
        logger.debug(self.planets)
        for p in self.planets:
            if p.owner != 0:
                continue
            r.append(p)
        return r

    def EnemyPlanets(self):
        r = []
        for p in self.planets:
            if p.owner <= 1:
                continue
            r.append(p)
        return r

    def NotMyPlanets(self):
        r = []
        for p in self.planets:
            if p.owner == 1:
                continue
            r.append(p)
        return r

    def Fleets(self):
        return self.fleets

    def MyFleets(self):
        r = []
        for f in self.fleets:
            if f.owner != 1:
                continue
            r.append(f)
        return r

    def EnemyFleets(self):
        r = []
        for f in self.fleets:
            if f.owner <= 1:
                continue
            r.append(f)
        return r

    def __str__(self):
        s = ''
        for p in self.planets:
            s += str(p)
        for f in self.fleets:
            s += str(f)
        return s

    def IssueOrder(self, source_planet, destination_planet, num_ships):
        stdout.write("%d %d %d\n" % \
     (source_planet, destination_planet, num_ships))
        stdout.flush()

    def IsAlive(self, player_id):
        for p in self.planets:
            if p.owner == player_id:
                return True
        for f in self.fleets:
            if f.owner == player_id:
                return True
        return False

    def ParseGameState(self, s):
        self.planets = []
        self.fleets = []
        lines = s.split("\n")
        planet_id = 0

        for line in lines:
            line = line.split("#")[0] # remove comments
            tokens = line.split(" ")
            if len(tokens) == 1:
                continue
            if tokens[0] == "P":
                if len(tokens) != 6:
                    return 0
                p = Planet(planet_id, # The ID of this planet
                           int(tokens[3]), # Owner
                           int(tokens[4]), # Num ships
                           int(tokens[5]), # Growth rate
                           float(tokens[1]), # X
                           float(tokens[2])) # Y
                planet_id += 1
                self.planets.append(p)
            elif tokens[0] == "F":
                if len(tokens) != 7:
                    return 0
                f = Fleet(int(tokens[1]), # Owner
                          int(tokens[2]), # Num ships
                          int(tokens[3]), # Source
                          int(tokens[4]), # Destination
                          int(tokens[5]), # Total trip length
                          int(tokens[6])) # Turns remaining
                self.fleets.append(f)
            else:
                return 0
        return 1

    def FinishTurn(self):
        stdout.write("go\n")
        stdout.flush()
