from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.700447559357
        editor.bgg = 0.924184978008
        editor.bgb = 1.0
        editor.loadTerrain("mountain/world/mb")
        editor.terrain.setScale(VBase3(3.50387, 3.50387, 3.50387))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(75.0, 229.0, 0, -166.0))
        editor.ships.append(setupShip(-596.0, 23.0, 1, -84.0))
        editor.powerups.append(setupPowerup(-503.0, 177.0))
        editor.powerups.append(setupPowerup(-622.0, 120.0))
        editor.powerups.append(setupPowerup(-487.0, 35.0))
        editor.powerups.append(setupPowerup(-367.0, -215.0))
        editor.powerups.append(setupPowerup(-557.0, -254.0))
        editor.powerups.append(setupPowerup(-39.0, -118.0))
        editor.powerups.append(setupPowerup(246.0, -155.0))
        editor.powerups.append(setupPowerup(32.0, -31.0))
        editor.powerups.append(setupPowerup(-175.0, 140.0))
        editor.powerups.append(setupPowerup(146.0, 22.0))
        editor.powerups.append(setupPowerup(253.0, 22.0))
        editor.powerups.append(setupPowerup(256.0, 262.0))
        editor.powerups.append(setupPowerup(7.0, 268.0))
        editor.laps = 0
        editor.winCredits = 0
        editor.minPlace = 0
        editor.setValues()