from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.539348363876
        editor.bgg = 0.839599013329
        editor.bgb = 1.0
        editor.loadTerrain("lavaland/world/lw")
        editor.terrain.setScale(VBase3(8, 8, 8))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(389.0, 319.0, 6, -89.0))
        editor.ships.append(setupShip(389.0, 300.0, 7, -89.0))
        editor.ships.append(setupShip(389.0, 280.0, 8, -89.0))
        editor.ships.append(setupShip(368.0, 280.0, 9, -89.0))
        editor.ships.append(setupShip(368.0, 299.0, 10, -89.0))
        editor.ships.append(setupShip(368.0, 319.0, 11, -89.0))
        editor.checkpoints.append(setupCheckpoint(521.0, -119.0, -183.0, 0, 3))
        editor.checkpoints.append(setupCheckpoint(-172.0, -640.0, -271.0, 1, 10))
        editor.checkpoints.append(setupCheckpoint(-94.0, -152.0, -409.0, 2, 15))
        editor.startingline = setupStartingline(415.0, 299.0, -89.0)
        editor.powerups.append(setupPowerup(498.0, 72.0))
        editor.powerups.append(setupPowerup(520.0, 72.0))
        editor.powerups.append(setupPowerup(545.0, 72.0))
        editor.powerups.append(setupPowerup(565.0, 72.0))
        editor.powerups.append(setupPowerup(378.0, -353.0))
        editor.powerups.append(setupPowerup(368.0, -346.0))
        editor.powerups.append(setupPowerup(358.0, -339.0))
        editor.powerups.append(setupPowerup(349.0, -330.0))
        editor.powerups.append(setupPowerup(343.0, -325.0))
        editor.powerups.append(setupPowerup(-362.0, -530.0))
        editor.powerups.append(setupPowerup(-382.0, -530.0))
        editor.powerups.append(setupPowerup(-407.0, -530.0))
        editor.powerups.append(setupPowerup(-432.0, -530.0))
        editor.powerups.append(setupPowerup(136.0, -200.0))
        editor.powerups.append(setupPowerup(230.0, 111.0))
        editor.powerups.append(setupPowerup(248.0, 133.0))
        editor.powerups.append(setupPowerup(191.0, 139.0))
        editor.powerups.append(setupPowerup(212.0, 123.0))
        editor.powerups.append(setupPowerup(173.0, 160.0))
        editor.powerups.append(setupPowerup(192.0, 179.0))
        editor.powerups.append(setupPowerup(209.0, 160.0))
        editor.powerups.append(setupPowerup(228.0, 143.0))
        editor.powerh.append(setupPowerh(166.0, -561.0))
        editor.powerh.append(setupPowerh(181.0, -576.0))
        editor.powerh.append(setupPowerh(191.0, -591.0))
        editor.powerh.append(setupPowerh(203.0, -607.0))
        editor.powerh.append(setupPowerh(-268.0, -367.0))
        editor.powerh.append(setupPowerh(-276.0, -361.0))
        editor.powerh.append(setupPowerh(-284.0, -354.0))
        editor.powerh.append(setupPowerh(-296.0, -342.0))
        editor.powerh.append(setupPowerh(-305.0, -331.0))
        editor.waypoints.append(setupWaypoint(470.0, 293.0, 0))
        editor.waypoints.append(setupWaypoint(518.0, 247.0, 1))
        editor.waypoints.append(setupWaypoint(535.0, 169.0, 2))
        editor.waypoints.append(setupWaypoint(511.0, -181.0, 4))
        editor.waypoints.append(setupWaypoint(402.0, -291.0, 5))
        editor.waypoints.append(setupWaypoint(368.0, -346.0, 6))
        editor.waypoints.append(setupWaypoint(224.0, -494.0, 7))
        editor.waypoints.append(setupWaypoint(150.0, -620.0, 8))
        editor.waypoints.append(setupWaypoint(-3.0, -635.0, 9))
        editor.waypoints.append(setupWaypoint(-335.0, -623.0, 11))
        editor.waypoints.append(setupWaypoint(-384.0, -586.0, 12))
        editor.waypoints.append(setupWaypoint(-384.0, -451.0, 13))
        editor.waypoints.append(setupWaypoint(-290.0, -351.0, 14))
        editor.waypoints.append(setupWaypoint(192.0, 139.0, 16))
        editor.waypoints.append(setupWaypoint(359.0, 298.0, 17))
        editor.laps = 2
        editor.winCredits = 500
        editor.minPlace = 1
        editor.setValues()