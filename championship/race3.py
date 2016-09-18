from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
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
        environment.playerShip = Ship(player1ship, -258.0, -2.0, 5, -83.0, environment, 6, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -256.0, -16.0, 5, -83.0, environment, 6, 2)
        self.xpoints = [-118.0, -65.0, -35.0, 10.0, 59.0, 82.0, 112.0, 121.0, 129.0, 141.0, 113.0, 194.0, 249.0, 267.0, 273.0, 213.0, 213.0, 220.0, 260.0, 265.0, 255.0, 232.0, 176.0, 124.0, 65.0, 1.0, -58.0, -132.0, -201.0, -264.0, -301.0, -322.0, -331.0, -330.0, -324.0, -299.0, -262.0, -230.0]
        self.ypoints = [32.0, 88.0, 142.0, 176.0, 180.0, 171.0, 142.0, 123.0, 78.0, 21.0, -32.0, -103.0, -78.0, -31.0, 18.0, 103.0, 135.0, 163.0, 259.0, 283.0, 308.0, 335.0, 347.0, 340.0, 317.0, 298.0, 304.0, 333.0, 347.0, 333.0, 308.0, 277.0, 231.0, 187.0, 139.0, 91.0, 37.0, 12.0]
        self.xplaces = [-256.0, -242.0, -241.0, -240.0, -239.0]
        self.yplaces = [-16.0, 11.0, -2.0, -16.0, -33.0]
        self.hs = [-83.0, -83.0, -83.0, -83.0, -83.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 8, 11, 14, 23, 34, 0]
        self.pointsnum = 38
        fact = 0
        if multiplayer:
            fact = 1
        for i in range(numCPUs):
            tempship = 0
            foundship = False
            while not foundship:
                tempship = random.randrange(6)
                if not shiptaken[tempship]:
                    shiptaken[tempship] = True
                    foundship = True
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 6, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-75.0, 144.0, 384.0))
        environment.barriers.append(Barrier(148.0, 107.0, 262.0))
        environment.barriers.append(Barrier(156.0, -9.0, 220.0))
        environment.barriers.append(Barrier(282.0, -108.0, 91.0))
        environment.barriers.append(Barrier(182.0, 101.0, 48.0))
        environment.barriers.append(Barrier(245.0, 101.0, 145.0))
        environment.barriers.append(Barrier(-321.0, -16.0, -22.0))
        environment.checkpoints.append(Checkpoint(129.0, 78.0, 0, -176.0))
        environment.checkpoints.append(Checkpoint(194.0, -103.0, 0, -98.0))
        environment.checkpoints.append(Checkpoint(273.0, 18.0, 0, 2.0))
        environment.checkpoints.append(Checkpoint(124.0, 340.0, 0, 104.0))
        environment.checkpoints.append(Checkpoint(-324.0, 139.0, 0, 189.0))
        environment.checkpoints.append(Startingline(-221.0, -9.0, 0, -83.0))
        environment.powerups.append(Powerup(-146.0, 46.0, 5))
        environment.powerups.append(Powerup(-146.0, 27.0, 5))
        environment.powerups.append(Powerup(-146.0, 7.0, 5))
        environment.powerups.append(Powerup(115.0, -30.0, 5))
        environment.powerups.append(Powerup(267.0, -30.0, 5))
        environment.powerups.append(Powerup(225.0, 57.0, 5))
        environment.powerups.append(Powerup(144.0, 55.0, 5))
        environment.powerups.append(Powerup(119.0, 55.0, 5))
        environment.powerups.append(Powerup(243.0, 324.0, 5))
        environment.powerups.append(Powerup(-94.0, 318.0, 5))
        environment.powerups.append(Powerup(-331.0, 255.0, 5))
        environment.powerups.append(Powerup(-300.0, 90.0, 5))
        environment.powerups.append(Powerup(-316.0, 90.0, 5))
        environment.powerups.append(Powerup(246.0, 56.0, 5))
        environment.powerups.append(Powerup(266.0, 56.0, 5))
        environment.powerh.append(Powerh(48.0, 180.0, 5))
        environment.powerh.append(Powerh(247.0, 227.0, 5))
        environment.powerh.append(Powerh(80.0, 324.0, 5))
        environment.powerh.append(Powerh(-225.0, 347.0, 5))
        base.camera.setPos(Point3(-272.888, -3.82804, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-270.888, -17.828, 9))
        environment.laps = 3
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
