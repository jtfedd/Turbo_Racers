from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.666354238987
        editor.bgg = 0.960409045219
        editor.bgb = 1.0
        editor.loadTerrain("canyon/world/cb")
        editor.terrain.setScale(VBase3(5, 5, 5))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(-113.0, -348.0, 0, 0.0))
        editor.ships.append(setupShip(326.0, 330.0, 1, 86.0))
        editor.powerups.append(setupPowerup(145.0, 304.0))
        editor.powerups.append(setupPowerup(76.0, 429.0))
        editor.powerups.append(setupPowerup(-82.0, 247.0))
        editor.powerups.append(setupPowerup(-306.0, 206.0))
        editor.powerups.append(setupPowerup(-445.0, 226.0))
        editor.powerups.append(setupPowerup(-341.0, 395.0))
        editor.powerups.append(setupPowerup(-441.0, 30.0))
        editor.powerups.append(setupPowerup(-323.0, -365.0))
        editor.powerups.append(setupPowerup(-215.0, -417.0))
        editor.powerups.append(setupPowerup(-45.0, -237.0))
        editor.powerups.append(setupPowerup(-56.0, -104.0))
        editor.powerups.append(setupPowerup(202.0, -85.0))
        editor.powerups.append(setupPowerup(337.0, -126.0))
        editor.powerups.append(setupPowerup(256.0, -394.0))
        editor.powerups.append(setupPowerup(452.0, -159.0))
        editor.powerups.append(setupPowerup(412.0, 106.0))
        editor.laps = 0
        editor.winCredits = 0
        editor.minPlace = 0
        editor.setValues()