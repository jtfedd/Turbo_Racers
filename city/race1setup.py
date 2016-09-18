from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.638653337955
        editor.bgg = 0.864521503448
        editor.bgb = 1.0
        editor.loadTerrain("city/world/cw")
        editor.terrain.setScale(VBase3(5.35364, 5.35364, 5.35364))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(-343.0, -162.0, 0, 0.0))
        editor.ships.append(setupShip(-359.0, -162.0, 1, 0.0))
        editor.ships.append(setupShip(-378.0, -162.0, 2, 0.0))
        editor.ships.append(setupShip(-378.0, -178.0, 3, 0.0))
        editor.ships.append(setupShip(-361.0, -178.0, 4, 0.0))
        editor.ships.append(setupShip(-343.0, -178.0, 5, 0.0))
        editor.barriers.append(setupBarrier(-326.0, -214.0, 482.0))
        editor.barriers.append(setupBarrier(-326.0, -53.0, 482.0))
        editor.barriers.append(setupBarrier(-351.0, 68.0, 540.0))
        editor.barriers.append(setupBarrier(-510.0, 46.0, 623.0))
        editor.barriers.append(setupBarrier(-486.0, -506.0, 720.0))
        editor.barriers.append(setupBarrier(-332.0, -493.0, 809.0))
        editor.barriers.append(setupBarrier(-324.0, -353.0, 848.0))
        editor.checkpoints.append(setupCheckpoint(-417.0, 47.0, 93.0, 0, 2))
        editor.checkpoints.append(setupCheckpoint(-486.0, -149.0, 182.0, 1, 5))
        editor.checkpoints.append(setupCheckpoint(-486.0, -441.0, 182.0, 2, 6))
        editor.checkpoints.append(setupCheckpoint(-352.0, -380.0, 359.0, 3, 9))
        editor.startingline = setupStartingline(-369.0, -149.0, 0.0)
        editor.powerups.append(setupPowerup(-340.0, -56.0))
        editor.powerups.append(setupPowerup(-351.0, -56.0))
        editor.powerups.append(setupPowerup(-364.0, -56.0))
        editor.powerups.append(setupPowerup(-472.0, -51.0))
        editor.powerups.append(setupPowerup(-484.0, -51.0))
        editor.powerups.append(setupPowerup(-471.0, -319.0))
        editor.powerups.append(setupPowerup(-485.0, -319.0))
        editor.powerups.append(setupPowerup(-496.0, -319.0))
        editor.powerups.append(setupPowerup(-364.0, -305.0))
        editor.powerups.append(setupPowerup(-351.0, -305.0))
        editor.powerups.append(setupPowerup(-338.0, -305.0))
        editor.powerh.append(setupPowerh(-496.0, -51.0))
        editor.powerh.append(setupPowerh(-410.0, -472.0))
        editor.powerh.append(setupPowerh(-410.0, -487.0))
        editor.powerh.append(setupPowerh(-409.0, -500.0))
        editor.waypoints.append(setupWaypoint(-351.0, -56.0, 0))
        editor.waypoints.append(setupWaypoint(-353.0, 11.0, 1))
        editor.waypoints.append(setupWaypoint(-454.0, 32.0, 3))
        editor.waypoints.append(setupWaypoint(-481.0, -28.0, 4))
        editor.waypoints.append(setupWaypoint(-409.0, -485.0, 7))
        editor.waypoints.append(setupWaypoint(-359.0, -436.0, 8))
        editor.waypoints.append(setupWaypoint(-352.0, -197.0, 10))
        editor.laps = 3
        editor.winCredits = 500
        editor.minPlace = 1
        editor.setValues()