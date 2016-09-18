from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.40000000596
        editor.bgg = 0.40000000596
        editor.bgb = 0.40000000596
        editor.loadTerrain("city/world/cw")
        editor.terrain.setScale(VBase3(5.35364, 5.35364, 5.35364))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(-484.0, -223.0, 0, -100.0))
        editor.ships.append(setupShip(303.0, -194.0, 1, 21.0))
        editor.powerups.append(setupPowerup(419.0, -288.0))
        editor.powerups.append(setupPowerup(117.0, -271.0))
        editor.powerups.append(setupPowerup(-50.0, -133.0))
        editor.powerups.append(setupPowerup(-186.0, -210.0))
        editor.powerups.append(setupPowerup(-216.0, 62.0))
        editor.powerups.append(setupPowerup(-328.0, 354.0))
        editor.powerups.append(setupPowerup(-421.0, 140.0))
        editor.powerups.append(setupPowerup(-429.0, -387.0))
        editor.powerups.append(setupPowerup(-158.0, -474.0))
        editor.powerups.append(setupPowerup(232.0, -489.0))
        editor.powerups.append(setupPowerup(298.0, 236.0))
        editor.powerups.append(setupPowerup(215.0, 490.0))
        editor.powerups.append(setupPowerup(-43.0, 275.0))
        editor.powerups.append(setupPowerup(-211.0, 486.0))
        editor.powerups.append(setupPowerup(-482.0, 458.0))
        editor.laps = 0
        editor.winCredits = 0
        editor.minPlace = 0
        editor.setValues()