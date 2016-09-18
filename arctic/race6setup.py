from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from level_editor_data import *
class RaceSetup(DirectObject):
    def __init__(self, editor):
        editor.bgr = 0.779288351536
        editor.bgg = 0.964670836926
        editor.bgb = 1.0
        editor.loadTerrain("arctic/world/ab")
        editor.terrain.setScale(VBase3(3.5, 3.5, 3.5))
        editor.terrain.setZ(0.0)
        editor.alightBrightness = 0.300000011921
        editor.dlightBrightness = 1.0
        editor.ships.append(setupShip(-101.0, -254.0, 0, 74.0))
        editor.ships.append(setupShip(313.0, 94.0, 1, 4.0))
        editor.powerups.append(setupPowerup(-210.0, -244.0))
        editor.powerups.append(setupPowerup(-258.0, -312.0))
        editor.powerups.append(setupPowerup(-284.0, -59.0))
        editor.powerups.append(setupPowerup(50.0, -230.0))
        editor.powerups.append(setupPowerup(221.0, -312.0))
        editor.powerups.append(setupPowerup(292.0, -109.0))
        editor.powerups.append(setupPowerup(265.0, 250.0))
        editor.powerups.append(setupPowerup(110.0, 332.0))
        editor.powerups.append(setupPowerup(92.0, 238.0))
        editor.powerups.append(setupPowerup(-143.0, 192.0))
        editor.powerups.append(setupPowerup(-218.0, 149.0))
        editor.powerups.append(setupPowerup(-311.0, 150.0))
        editor.powerups.append(setupPowerup(-207.0, 226.0))
        editor.powerups.append(setupPowerup(-301.0, 56.0))
        editor.powerups.append(setupPowerup(-256.0, 128.0))
        editor.powerups.append(setupPowerup(-197.0, 84.0))
        editor.powerups.append(setupPowerup(-62.0, -138.0))
        editor.powerups.append(setupPowerup(-20.0, 48.0))
        editor.powerups.append(setupPowerup(20.0, 17.0))
        editor.powerups.append(setupPowerup(20.0, 84.0))
        editor.powerups.append(setupPowerup(58.0, 50.0))
        editor.laps = 0
        editor.winCredits = 0
        editor.minPlace = 0
        editor.setValues()