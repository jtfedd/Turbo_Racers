from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.631578862667
        editor.bgg = 0.631578862667
        editor.bgb = 0.631578862667
        editor.loadTerrain("lavaland/world/lb")
        editor.terrain.setScale(VBase3(8, 8, 8))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(-124.0, 293.0, 0, -87.0))
        editor.ships.append(setupShip(976.0, 1.0, 1, 8.0))
        editor.powerups.append(setupPowerup(871.0, -115.0))
        editor.powerups.append(setupPowerup(883.0, -386.0))
        editor.powerups.append(setupPowerup(1278.0, -471.0))
        editor.powerups.append(setupPowerup(1292.0, -695.0))
        editor.powerups.append(setupPowerup(674.0, -493.0))
        editor.powerups.append(setupPowerup(536.0, -274.0))
        editor.powerups.append(setupPowerup(272.0, -597.0))
        editor.powerups.append(setupPowerup(-104.0, -656.0))
        editor.powerups.append(setupPowerup(-401.0, -662.0))
        editor.powerups.append(setupPowerup(-631.0, -386.0))
        editor.powerups.append(setupPowerup(-319.0, -311.0))
        editor.powerups.append(setupPowerup(101.0, -51.0))
        editor.powerups.append(setupPowerup(205.0, 151.0))
        editor.powerups.append(setupPowerup(144.0, 436.0))
        editor.powerups.append(setupPowerup(390.0, 307.0))
        editor.powerups.append(setupPowerup(539.0, 95.0))
        editor.powerups.append(setupPowerup(586.0, 519.0))
        editor.powerups.append(setupPowerup(908.0, 560.0))
        editor.powerups.append(setupPowerup(953.0, 219.0))
        editor.powerups.append(setupPowerup(1479.0, 254.0))
        editor.powerups.append(setupPowerup(1384.0, 571.0))
        editor.powerups.append(setupPowerup(1481.0, -273.0))
        editor.powerups.append(setupPowerup(-320.0, 103.0))
        editor.powerups.append(setupPowerup(-623.0, 136.0))
        editor.powerups.append(setupPowerup(-670.0, 430.0))
        editor.powerups.append(setupPowerup(-454.0, 657.0))
        editor.powerups.append(setupPowerup(-138.0, 623.0))
        editor.laps = 0
        editor.winCredits = 0
        editor.minPlace = 0
        editor.setValues()