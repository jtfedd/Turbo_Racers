from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Battledata import *
class Race(DirectObject):
    def __init__(self, environment, user, player1ship, player2ship):
        base.setBackgroundColor(0.40000000596, 0.40000000596, 0.40000000596)
        environment.earth = loader.loadModel("city/world/cb")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(5.35364, 5.35364, 5.35364))
        environment.earth.setBin("background", 1)
        environment.earth.find("**/trees").setBin("transparent", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 7
        environment.playerShip = Ship(player1ship, -484.0, -223.0, 5, -100.0, environment, 1)
        environment.player2Ship = Ship(player2ship, 303.0, -194.0, 5, 21.0, environment, 2)
        environment.powerups.append(Powerup(419.0, -288.0, 5))
        environment.powerups.append(Powerup(117.0, -271.0, 5))
        environment.powerups.append(Powerup(-50.0, -133.0, 5))
        environment.powerups.append(Powerup(-186.0, -210.0, 5))
        environment.powerups.append(Powerup(-216.0, 62.0, 5))
        environment.powerups.append(Powerup(-328.0, 354.0, 5))
        environment.powerups.append(Powerup(-421.0, 140.0, 5))
        environment.powerups.append(Powerup(-429.0, -387.0, 5))
        environment.powerups.append(Powerup(-158.0, -474.0, 5))
        environment.powerups.append(Powerup(232.0, -489.0, 5))
        environment.powerups.append(Powerup(298.0, 236.0, 5))
        environment.powerups.append(Powerup(215.0, 490.0, 5))
        environment.powerups.append(Powerup(-43.0, 275.0, 5))
        environment.powerups.append(Powerup(-211.0, 486.0, 5))
        environment.powerups.append(Powerup(-482.0, 458.0, 5))
        base.camera.setPos(Point3(-498.772, -220.395, 9))
        environment.cam2.setPos(Point3(308.376, -208.004, 9))
