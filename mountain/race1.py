from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.700447559357, 0.924184978008, 1.0)
        environment.earth = loader.loadModel("mountain/world/mw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.50387, 3.50387, 3.50387))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 3
        environment.playerShip = Ship(player1ship, 148.0, 138.0, 5, 203.0, environment, 5, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 133.0, 131.0, 5, 203.0, environment, 5, 2)
        self.xpoints = [138.0, 130.0, 88.0, 14.0, -34.0, -101.0, -169.0, -218.0, -235.0, -209.0, -164.0, -80.0, -33.0, 45.0, 106.0, 231.0, 275.0, 274.0, 271.0, 259.0, 227.0, 185.0, 137.0, 126.0]
        self.ypoints = [70.0, 13.0, -29.0, -18.0, 35.0, 66.0, 68.0, 41.0, -15.0, -55.0, -87.0, -122.0, -176.0, -279.0, -301.0, -293.0, -254.0, -63.0, 69.0, 193.0, 256.0, 278.0, 244.0, 192.0]
        self.xplaces = [133.0, 116.0, 110.0, 127.0, 144.0]
        self.yplaces = [131.0, 124.0, 134.0, 142.0, 151.0]
        self.hs = [203.0, 203.0, 203.0, 203.0, 203.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 10, 14, 17, 0]
        self.pointsnum = 24
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 5, self.startPlaces, i+1))
        environment.barriers.append(Barrier(190.0, 53.0, 263.0))
        environment.barriers.append(Barrier(181.0, 14.0, 238.0))
        environment.barriers.append(Barrier(227.0, -3.0, 94.0))
        environment.barriers.append(Barrier(227.0, 48.0, 94.0))
        environment.barriers.append(Barrier(6.0, -68.0, 138.0))
        environment.barriers.append(Barrier(-11.0, -98.0, -38.0))
        environment.barriers.append(Barrier(52.0, -189.0, -90.0))
        environment.checkpoints.append(Checkpoint(-34.0, 35.0, 0, 408.0))
        environment.checkpoints.append(Checkpoint(-164.0, -87.0, 0, 245.0))
        environment.checkpoints.append(Checkpoint(106.0, -301.0, 0, 266.0))
        environment.checkpoints.append(Checkpoint(274.0, -63.0, 0, 358.0))
        environment.checkpoints.append(Startingline(140.0, 110.0, 0, 203.0))
        environment.powerups.append(Powerup(160.0, 39.0, 5))
        environment.powerups.append(Powerup(140.0, 39.0, 5))
        environment.powerups.append(Powerup(126.0, 39.0, 5))
        environment.powerups.append(Powerup(-143.0, 70.0, 5))
        environment.powerups.append(Powerup(18.0, -199.0, 5))
        environment.powerups.append(Powerup(-0.0, -199.0, 5))
        environment.powerups.append(Powerup(-16.0, -199.0, 5))
        environment.powerups.append(Powerup(271.0, -134.0, 5))
        environment.powerups.append(Powerup(256.0, -134.0, 5))
        environment.powerups.append(Powerup(120.0, 224.0, 5))
        environment.powerh.append(Powerh(-143.0, 82.0, 5))
        environment.powerh.append(Powerh(-143.0, 94.0, 5))
        environment.powerh.append(Powerh(282.0, -134.0, 5))
        environment.powerh.append(Powerh(132.0, 224.0, 5))
        base.camera.setPos(Point3(142.139, 151.808, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(127.139, 144.808, 9))
        environment.laps = 4
        self.finishCredits = [500, 250, 125, 83, 62, 0]
        self.finishPlace = 1
