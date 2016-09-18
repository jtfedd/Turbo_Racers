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
        editor.ships.append(setupShip(-271.0, -242.0, 0, 0.0))
        editor.ships.append(setupShip(146.0, -140.0, 1, 0.0))
        editor.powerups.append(setupPowerup(209.0, -199.0))
        editor.powerups.append(setupPowerup(245.0, -106.0))
        editor.powerups.append(setupPowerup(188.0, -5.0))
        editor.powerups.append(setupPowerup(175.0, 99.0))
        editor.powerups.append(setupPowerup(-154.0, 20.0))
        editor.powerups.append(setupPowerup(-229.0, 142.0))
        editor.powerups.append(setupPowerup(-321.0, 78.0))
        editor.powerups.append(setupPowerup(-367.0, -59.0))
        editor.powerups.append(setupPowerup(-412.0, -141.0))
        editor.powerups.append(setupPowerup(-190.0, -100.0))
        editor.powerups.append(setupPowerup(-38.0, -237.0))
        editor.powerups.append(setupPowerup(-124.0, -439.0))
        editor.powerups.append(setupPowerup(-289.0, -301.0))
        editor.powerups.append(setupPowerup(-402.0, -369.0))
        editor.powerups.append(setupPowerup(-464.0, -232.0))
        editor.powerups.append(setupPowerup(-235.0, -380.0))
        editor.laps = 0
        editor.winCredits = 0
        editor.minPlace = 0
        editor.setValues()