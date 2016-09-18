from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.742857158184
        editor.bgg = 0.917293250561
        editor.bgb = 1.0
        editor.loadTerrain("arctic/world/aw")
        editor.terrain.setScale(VBase3(3.5, 3.5, 3.5))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(-145.0, -284.0, 1, -85.0))
        editor.ships.append(setupShip(-147.0, -273.0, 2, -85.0))
        editor.ships.append(setupShip(-149.0, -262.0, 3, -85.0))
        editor.ships.append(setupShip(-152.0, -249.0, 4, -85.0))
        editor.ships.append(setupShip(-156.0, -263.0, 5, -85.0))
        editor.ships.append(setupShip(-154.0, -273.0, 6, -85.0))
        editor.barriers.append(setupBarrier(39.0, -180.0, -23.0))
        editor.barriers.append(setupBarrier(210.0, -252.0, 17.0))
        editor.barriers.append(setupBarrier(236.0, -239.0, 38.0))
        editor.barriers.append(setupBarrier(323.0, -121.0, 85.0))
        editor.checkpoints.append(setupCheckpoint(268.0, -159.0, -41.0, 1, 4))
        editor.checkpoints.append(setupCheckpoint(272.0, 252.0, 48.0, 2, 8))
        editor.checkpoints.append(setupCheckpoint(-28.0, 298.0, 105.0, 3, 11))
        editor.checkpoints.append(setupCheckpoint(-167.0, 187.0, 105.0, 4, 15))
        editor.checkpoints.append(setupCheckpoint(-277.0, -8.0, 163.0, 5, 18))
        editor.startingline = setupStartingline(-132.0, -259.0, -76.0)
        editor.powerups.append(setupPowerup(-2.0, -198.0))
        editor.powerups.append(setupPowerup(-2.0, -214.0))
        editor.powerups.append(setupPowerup(-2.0, -229.0))
        editor.powerups.append(setupPowerup(288.0, -27.0))
        editor.powerups.append(setupPowerup(309.0, 94.0))
        editor.powerups.append(setupPowerup(325.0, 94.0))
        editor.powerups.append(setupPowerup(232.0, 351.0))
        editor.powerups.append(setupPowerup(192.0, 211.0))
        editor.powerups.append(setupPowerup(27.0, 280.0))
        editor.powerups.append(setupPowerup(-94.0, 274.0))
        editor.powerups.append(setupPowerup(-287.0, 23.0))
        editor.powerups.append(setupPowerup(-271.0, 23.0))
        editor.powerups.append(setupPowerup(-321.0, -126.0))
        editor.powerups.append(setupPowerup(-283.0, -210.0))
        editor.powerups.append(setupPowerup(-267.0, -202.0))
        editor.powerups.append(setupPowerup(-253.0, -197.0))
        editor.powerh.append(setupPowerh(227.0, -192.0))
        editor.powerh.append(setupPowerh(293.0, 94.0))
        editor.powerh.append(setupPowerh(167.0, 269.0))
        editor.powerh.append(setupPowerh(47.0, 280.0))
        editor.powerh.append(setupPowerh(-257.0, 23.0))
        editor.powerh.append(setupPowerh(-275.0, -94.0))
        editor.waypoints.append(setupWaypoint(-3.0, -213.0, 1))
        editor.waypoints.append(setupWaypoint(92.0, -228.0, 2))
        editor.waypoints.append(setupWaypoint(210.0, -200.0, 3))
        editor.waypoints.append(setupWaypoint(286.0, -56.0, 5))
        editor.waypoints.append(setupWaypoint(300.0, 47.0, 6))
        editor.waypoints.append(setupWaypoint(310.0, 197.0, 7))
        editor.waypoints.append(setupWaypoint(259.0, 324.0, 9))
        editor.waypoints.append(setupWaypoint(234.0, 352.0, 10))
        editor.waypoints.append(setupWaypoint(-92.0, 275.0, 12))
        editor.waypoints.append(setupWaypoint(-129.0, 214.0, 13))
        editor.waypoints.append(setupWaypoint(-197.0, 164.0, 16))
        editor.waypoints.append(setupWaypoint(-232.0, 119.0, 17))
        editor.waypoints.append(setupWaypoint(-300.0, -73.0, 19))
        editor.waypoints.append(setupWaypoint(-322.0, -126.0, 20))
        editor.waypoints.append(setupWaypoint(-282.0, -209.0, 21))
        editor.waypoints.append(setupWaypoint(-166.0, -270.0, 22))
        editor.laps = 3
        editor.winCredits = 500
        editor.minPlace = 2
        editor.setValues()