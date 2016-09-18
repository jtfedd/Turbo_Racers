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
        editor.ships.append(setupShip(-14.0, -304.0, 0, 176.0))
        editor.ships.append(setupShip(-29.0, -304.0, 1, 176.0))
        editor.ships.append(setupShip(-49.0, -304.0, 2, 176.0))
        editor.ships.append(setupShip(-49.0, -290.0, 3, 176.0))
        editor.ships.append(setupShip(-30.0, -290.0, 4, 176.0))
        editor.ships.append(setupShip(-15.0, -290.0, 5, 176.0))
        editor.barriers.append(setupBarrier(-106.0, -404.0, 143.0))
        editor.barriers.append(setupBarrier(-162.0, -455.0, 95.0))
        editor.barriers.append(setupBarrier(-425.0, -384.0, -20.0))
        editor.barriers.append(setupBarrier(-398.0, -398.0, -22.0))
        editor.barriers.append(setupBarrier(-302.0, -456.0, -123.0))
        editor.barriers.append(setupBarrier(-407.0, -432.0, -175.0))
        editor.barriers.append(setupBarrier(-19.0, -158.0, -94.0))
        editor.checkpoints.append(setupCheckpoint(-297.0, -297.0, 81.0, 0, 4))
        editor.checkpoints.append(setupCheckpoint(-330.0, -420.0, 181.0, 1, 8))
        editor.checkpoints.append(setupCheckpoint(-463.0, -262.0, 3.0, 2, 13))
        editor.checkpoints.append(setupCheckpoint(-252.0, -85.0, -83.0, 3, 17))
        editor.startingline = setupStartingline(-26.0, -318.0, 176.0)
        editor.powerups.append(setupPowerup(-49.0, -377.0))
        editor.powerups.append(setupPowerup(-35.0, -377.0))
        editor.powerups.append(setupPowerup(-22.0, -377.0))
        editor.powerups.append(setupPowerup(-156.0, -362.0))
        editor.powerups.append(setupPowerup(-236.0, -327.0))
        editor.powerups.append(setupPowerup(-236.0, -311.0))
        editor.powerups.append(setupPowerup(-236.0, -296.0))
        editor.powerups.append(setupPowerup(-384.0, -366.0))
        editor.powerups.append(setupPowerup(-410.0, -456.0))
        editor.powerups.append(setupPowerup(-189.0, -105.0))
        editor.powerups.append(setupPowerup(-189.0, -85.0))
        editor.powerups.append(setupPowerup(-189.0, -60.0))
        editor.powerh.append(setupPowerh(-167.0, -370.0))
        editor.powerh.append(setupPowerh(-144.0, -357.0))
        editor.powerh.append(setupPowerh(-471.0, -299.0))
        editor.powerh.append(setupPowerh(-459.0, -299.0))
        editor.waypoints.append(setupWaypoint(-44.0, -421.0, 0))
        editor.waypoints.append(setupWaypoint(-88.0, -446.0, 1))
        editor.waypoints.append(setupWaypoint(-143.0, -395.0, 2))
        editor.waypoints.append(setupWaypoint(-179.0, -326.0, 3))
        editor.waypoints.append(setupWaypoint(-362.0, -287.0, 5))
        editor.waypoints.append(setupWaypoint(-402.0, -314.0, 6))
        editor.waypoints.append(setupWaypoint(-369.0, -372.0, 7))
        editor.waypoints.append(setupWaypoint(-346.0, -460.0, 9))
        editor.waypoints.append(setupWaypoint(-452.0, -451.0, 10))
        editor.waypoints.append(setupWaypoint(-486.0, -410.0, 11))
        editor.waypoints.append(setupWaypoint(-482.0, -349.0, 12))
        editor.waypoints.append(setupWaypoint(-465.0, -183.0, 14))
        editor.waypoints.append(setupWaypoint(-450.0, -150.0, 15))
        editor.waypoints.append(setupWaypoint(-367.0, -109.0, 16))
        editor.waypoints.append(setupWaypoint(-149.0, -93.0, 18))
        editor.waypoints.append(setupWaypoint(-48.0, -147.0, 19))
        editor.waypoints.append(setupWaypoint(-37.0, -299.0, 21))
        editor.waypoints.append(setupWaypoint(-35.0, -215.0, 20))
        editor.laps = 4
        editor.winCredits = 800
        editor.minPlace = 1
        editor.setValues()