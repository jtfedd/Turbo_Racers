from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.0383548997343
        editor.bgg = 0.0809716284275
        editor.bgb = 0.144300118089
        editor.loadTerrain("championship/world/cw")
        editor.terrain.setScale(VBase3(3.8418, 3.8418, 3.8418))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.276560783386
        editor.dlightBrightness = 0.422544240952
        editor.ships.append(setupShip(-50.0, -286.0, 0, 0.0))
        editor.ships.append(setupShip(-39.0, -286.0, 1, 0.0))
        editor.ships.append(setupShip(-25.0, -286.0, 2, 0.0))
        editor.ships.append(setupShip(-16.0, -273.0, 3, 0.0))
        editor.ships.append(setupShip(-35.0, -273.0, 4, 0.0))
        editor.ships.append(setupShip(-50.0, -273.0, 5, 0.0))
        editor.barriers.append(setupBarrier(-116.0, -435.0, -45.0))
        editor.barriers.append(setupBarrier(-86.0, -461.0, -10.0))
        editor.barriers.append(setupBarrier(-83.0, -228.0, -38.0))
        editor.barriers.append(setupBarrier(-284.0, -246.0, -38.0))
        editor.barriers.append(setupBarrier(-260.0, -256.0, -2.0))
        editor.barriers.append(setupBarrier(-34.0, 145.0, -43.0))
        editor.checkpoints.append(setupCheckpoint(-113.0, -20.0, 42.0, 0, 3))
        editor.checkpoints.append(setupCheckpoint(-161.0, 146.0, -87.0, 1, 9))
        editor.checkpoints.append(setupCheckpoint(-226.0, -47.0, -204.0, 2, 14))
        editor.checkpoints.append(setupCheckpoint(-100.0, -339.0, -177.0, 3, 21))
        editor.startingline = setupStartingline(-30.0, -257.0, 0.0)
        editor.powerups.append(setupPowerup(-157.0, 62.0))
        editor.powerups.append(setupPowerup(-158.0, 44.0))
        editor.powerups.append(setupPowerup(-158.0, 28.0))
        editor.powerups.append(setupPowerup(-158.0, 9.0))
        editor.powerups.append(setupPowerup(-158.0, -6.0))
        editor.powerups.append(setupPowerup(-193.0, -241.0))
        editor.powerups.append(setupPowerup(-103.0, -314.0))
        editor.powerups.append(setupPowerup(-44.0, -314.0))
        editor.powerups.append(setupPowerup(-23.0, -314.0))
        editor.powerups.append(setupPowerup(-70.0, -439.0))
        editor.powerups.append(setupPowerup(-76.0, -79.0))
        editor.powerups.append(setupPowerup(-65.0, -72.0))
        editor.powerups.append(setupPowerup(-52.0, -66.0))
        editor.powerh.append(setupPowerh(-73.0, 76.0))
        editor.powerh.append(setupPowerh(-240.0, 90.0))
        editor.powerh.append(setupPowerh(-147.0, 148.0))
        editor.powerh.append(setupPowerh(-193.0, -226.0))
        editor.waypoints.append(setupWaypoint(-34.0, -209.0, 0))
        editor.waypoints.append(setupWaypoint(-40.0, -110.0, 1))
        editor.waypoints.append(setupWaypoint(-62.0, -68.0, 2))
        editor.waypoints.append(setupWaypoint(-151.0, 27.0, 4))
        editor.waypoints.append(setupWaypoint(-196.0, 57.0, 5))
        editor.waypoints.append(setupWaypoint(-232.0, 76.0, 6))
        editor.waypoints.append(setupWaypoint(-240.0, 123.0, 7))
        editor.waypoints.append(setupWaypoint(-190.0, 146.0, 8))
        editor.waypoints.append(setupWaypoint(-99.0, 145.0, 10))
        editor.waypoints.append(setupWaypoint(-62.0, 118.0, 11))
        editor.waypoints.append(setupWaypoint(-79.0, 68.0, 12))
        editor.waypoints.append(setupWaypoint(-187.0, -3.0, 13))
        editor.waypoints.append(setupWaypoint(-263.0, -96.0, 15))
        editor.waypoints.append(setupWaypoint(-278.0, -132.0, 16))
        editor.waypoints.append(setupWaypoint(-270.0, -209.0, 17))
        editor.waypoints.append(setupWaypoint(-252.0, -237.0, 18))
        editor.waypoints.append(setupWaypoint(-164.0, -245.0, 19))
        editor.waypoints.append(setupWaypoint(-116.0, -275.0, 20))
        editor.waypoints.append(setupWaypoint(-96.0, -412.0, 22))
        editor.waypoints.append(setupWaypoint(-67.0, -439.0, 23))
        editor.waypoints.append(setupWaypoint(-38.0, -413.0, 24))
        editor.laps = 3
        editor.winCredits = 850
        editor.minPlace = 1
        editor.setValues()