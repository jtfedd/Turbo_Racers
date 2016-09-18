from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.700447559357
        editor.bgg = 0.924184978008
        editor.bgb = 1.0
        editor.loadTerrain("mountain/world/mw")
        editor.terrain.setScale(VBase3(3.50387, 3.50387, 3.50387))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(148.0, 138.0, 0, 203.0))
        editor.ships.append(setupShip(133.0, 131.0, 1, 203.0))
        editor.ships.append(setupShip(116.0, 124.0, 2, 203.0))
        editor.ships.append(setupShip(110.0, 134.0, 3, 203.0))
        editor.ships.append(setupShip(127.0, 142.0, 4, 203.0))
        editor.ships.append(setupShip(144.0, 151.0, 5, 203.0))
        editor.barriers.append(setupBarrier(190.0, 53.0, 263.0))
        editor.barriers.append(setupBarrier(181.0, 14.0, 238.0))
        editor.barriers.append(setupBarrier(227.0, -3.0, 94.0))
        editor.barriers.append(setupBarrier(227.0, 48.0, 94.0))
        editor.barriers.append(setupBarrier(6.0, -68.0, 138.0))
        editor.barriers.append(setupBarrier(-11.0, -98.0, -38.0))
        editor.barriers.append(setupBarrier(52.0, -189.0, -90.0))
        editor.checkpoints.append(setupCheckpoint(-34.0, 35.0, 408.0, 0, 4))
        editor.checkpoints.append(setupCheckpoint(-164.0, -87.0, 245.0, 1, 10))
        editor.checkpoints.append(setupCheckpoint(106.0, -301.0, 266.0, 2, 14))
        editor.checkpoints.append(setupCheckpoint(274.0, -63.0, 358.0, 3, 17))
        editor.startingline = setupStartingline(140.0, 110.0, 203.0)
        editor.powerups.append(setupPowerup(160.0, 39.0))
        editor.powerups.append(setupPowerup(140.0, 39.0))
        editor.powerups.append(setupPowerup(126.0, 39.0))
        editor.powerups.append(setupPowerup(-143.0, 70.0))
        editor.powerups.append(setupPowerup(18.0, -199.0))
        editor.powerups.append(setupPowerup(0.0, -199.0))
        editor.powerups.append(setupPowerup(-16.0, -199.0))
        editor.powerups.append(setupPowerup(271.0, -134.0))
        editor.powerups.append(setupPowerup(256.0, -134.0))
        editor.powerups.append(setupPowerup(120.0, 224.0))
        editor.powerh.append(setupPowerh(-143.0, 82.0))
        editor.powerh.append(setupPowerh(-143.0, 94.0))
        editor.powerh.append(setupPowerh(282.0, -134.0))
        editor.powerh.append(setupPowerh(132.0, 224.0))
        editor.waypoints.append(setupWaypoint(138.0, 70.0, 0))
        editor.waypoints.append(setupWaypoint(130.0, 13.0, 1))
        editor.waypoints.append(setupWaypoint(88.0, -29.0, 2))
        editor.waypoints.append(setupWaypoint(14.0, -18.0, 3))
        editor.waypoints.append(setupWaypoint(-101.0, 66.0, 5))
        editor.waypoints.append(setupWaypoint(-169.0, 68.0, 6))
        editor.waypoints.append(setupWaypoint(-218.0, 41.0, 7))
        editor.waypoints.append(setupWaypoint(-235.0, -15.0, 8))
        editor.waypoints.append(setupWaypoint(-209.0, -55.0, 9))
        editor.waypoints.append(setupWaypoint(-80.0, -122.0, 11))
        editor.waypoints.append(setupWaypoint(-33.0, -176.0, 12))
        editor.waypoints.append(setupWaypoint(45.0, -279.0, 13))
        editor.waypoints.append(setupWaypoint(231.0, -293.0, 15))
        editor.waypoints.append(setupWaypoint(275.0, -254.0, 16))
        editor.waypoints.append(setupWaypoint(271.0, 69.0, 18))
        editor.waypoints.append(setupWaypoint(259.0, 193.0, 19))
        editor.waypoints.append(setupWaypoint(227.0, 256.0, 20))
        editor.waypoints.append(setupWaypoint(185.0, 278.0, 21))
        editor.waypoints.append(setupWaypoint(137.0, 244.0, 22))
        editor.waypoints.append(setupWaypoint(126.0, 192.0, 23))
        editor.laps = 4
        editor.winCredits = 500
        editor.minPlace = 1
        editor.setValues()