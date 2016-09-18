from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Battledata import *
class Race(DirectObject):
    def __init__(self, environment, user, player1ship, player2ship):
        base.setBackgroundColor(0.700447559357, 0.924184978008, 1.0)
        environment.earth = loader.loadModel("mountain/world/mb")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.50387, 3.50387, 3.50387))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.playerShip = Ship(player1ship, 75.0, 229.0, 5, -166.0, environment, 1)
        environment.player2Ship = Ship(player2ship, -596.0, 23.0, 5, -84.0, environment, 2)
        environment.powerups.append(Powerup(-503.0, 177.0, 5))
        environment.powerups.append(Powerup(-622.0, 120.0, 5))
        environment.powerups.append(Powerup(-487.0, 35.0, 5))
        environment.powerups.append(Powerup(-367.0, -215.0, 5))
        environment.powerups.append(Powerup(-557.0, -254.0, 5))
        environment.powerups.append(Powerup(-39.0, -118.0, 5))
        environment.powerups.append(Powerup(246.0, -155.0, 5))
        environment.powerups.append(Powerup(32.0, -31.0, 5))
        environment.powerups.append(Powerup(-175.0, 140.0, 5))
        environment.powerups.append(Powerup(146.0, 22.0, 5))
        environment.powerups.append(Powerup(253.0, 22.0, 5))
        environment.powerups.append(Powerup(256.0, 262.0, 5))
        environment.powerups.append(Powerup(7.0, 268.0, 5))
        base.camera.setPos(Point3(71.3712, 243.554, 9))
        environment.cam2.setPos(Point3(-610.918, 21.4321, 9))
