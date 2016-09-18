from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Battledata import *
class Race(DirectObject):
    def __init__(self, environment, user, player1ship, player2ship):
        base.setBackgroundColor(0.0383548997343, 0.0809716284275, 0.144300118089)
        environment.earth = loader.loadModel("championship/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.8418, 3.8418, 3.8418))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.276560783386, 0.276560783386, 0.276560783386, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.422544240952, 0.422544240952, 0.422544240952, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.422544240952, 0.422544240952, 0.422544240952, 1))
        environment.domenum = 7
        environment.playerShip = Ship(player1ship, -271.0, -242.0, 5, 0.0, environment, 1)
        environment.player2Ship = Ship(player2ship, 146.0, -140.0, 5, 0.0, environment, 2)
        environment.powerups.append(Powerup(209.0, -199.0, 5))
        environment.powerups.append(Powerup(245.0, -106.0, 5))
        environment.powerups.append(Powerup(188.0, -5.0, 5))
        environment.powerups.append(Powerup(175.0, 99.0, 5))
        environment.powerups.append(Powerup(-154.0, 20.0, 5))
        environment.powerups.append(Powerup(-229.0, 142.0, 5))
        environment.powerups.append(Powerup(-321.0, 78.0, 5))
        environment.powerups.append(Powerup(-367.0, -59.0, 5))
        environment.powerups.append(Powerup(-412.0, -141.0, 5))
        environment.powerups.append(Powerup(-190.0, -100.0, 5))
        environment.powerups.append(Powerup(-38.0, -237.0, 5))
        environment.powerups.append(Powerup(-124.0, -439.0, 5))
        environment.powerups.append(Powerup(-289.0, -301.0, 5))
        environment.powerups.append(Powerup(-402.0, -369.0, 5))
        environment.powerups.append(Powerup(-464.0, -232.0, 5))
        environment.powerups.append(Powerup(-235.0, -380.0, 5))
        base.camera.setPos(Point3(-271, -257, 9))
        environment.cam2.setPos(Point3(146, -155, 9))
