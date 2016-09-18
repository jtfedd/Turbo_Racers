from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.40000000596, 0.40000000596, 0.40000000596)
        environment.earth = loader.loadModel("city/world/cw")
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
        environment.domenum = 5
        environment.playerShip = Ship(player1ship, -228.0, 493.0, 5, 89.0, environment, 7, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -228.0, 476.0, 5, 89.0, environment, 7, 2)
        self.xpoints = [-448.0, -477.0, -479.0, -452.0, -418.0, -418.0, -376.0, -352.0, -342.0, -265.0, -7.0, 80.0, 117.0, 123.0, 155.0, 205.0, 385.0, 385.0, 350.0, 256.0, -216.0]
        self.ypoints = [480.0, 456.0, 391.0, 349.0, 295.0, 88.0, 43.0, -1.0, -36.0, -48.0, -50.0, -56.0, -91.0, -281.0, -316.0, -310.0, 11.0, 455.0, 481.0, 485.0, 478.0]
        self.xplaces = [-228.0, -222.0, -228.0, -222.0, -215.0]
        self.yplaces = [476.0, 485.0, 508.0, 501.0, 493.0]
        self.hs = [89.0, 89.0, 89.0, 89.0, 89.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 7, 10, 15, 16, 19, 0]
        self.pointsnum = 21
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 7, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-352.0, -71.0, 324.0))
        environment.barriers.append(Barrier(-420.0, 41.0, 324.0))
        environment.barriers.append(Barrier(384.0, 502.0, 180.0))
        environment.barriers.append(Barrier(-395.0, 350.0, 269.0))
        environment.checkpoints.append(Checkpoint(-418.0, 295.0, 0, 173.0))
        environment.checkpoints.append(Checkpoint(-352.0, -1.0, 0, 176.0))
        environment.checkpoints.append(Checkpoint(-7.0, -50.0, 0, 267.0))
        environment.checkpoints.append(Checkpoint(205.0, -310.0, 0, 300.0))
        environment.checkpoints.append(Checkpoint(385.0, 11.0, 0, 362.0))
        environment.checkpoints.append(Checkpoint(256.0, 485.0, 0, 454.0))
        environment.checkpoints.append(Startingline(-238.0, 484.0, 0, 89.0))
        environment.powerups.append(Powerup(-377.0, 473.0, 5))
        environment.powerups.append(Powerup(-377.0, 485.0, 5))
        environment.powerups.append(Powerup(-377.0, 498.0, 5))
        environment.powerups.append(Powerup(-473.0, 421.0, 5))
        environment.powerups.append(Powerup(-485.0, 421.0, 5))
        environment.powerups.append(Powerup(-496.0, 421.0, 5))
        environment.powerups.append(Powerup(-284.0, -51.0, 5))
        environment.powerups.append(Powerup(104.0, -135.0, 5))
        environment.powerups.append(Powerup(117.0, -135.0, 5))
        environment.powerups.append(Powerup(130.0, -135.0, 5))
        environment.powerups.append(Powerup(211.0, -147.0, 5))
        environment.powerups.append(Powerup(283.0, -147.0, 5))
        environment.powerups.append(Powerup(350.0, -147.0, 5))
        environment.powerups.append(Powerup(411.0, -147.0, 5))
        environment.powerups.append(Powerup(372.0, 234.0, 5))
        environment.powerups.append(Powerup(384.0, 234.0, 5))
        environment.powerups.append(Powerup(159.0, 472.0, 5))
        environment.powerups.append(Powerup(159.0, 485.0, 5))
        environment.powerh.append(Powerh(-407.0, 187.0, 5))
        environment.powerh.append(Powerh(-418.0, 187.0, 5))
        environment.powerh.append(Powerh(-430.0, 187.0, 5))
        environment.powerh.append(Powerh(-284.0, -39.0, 5))
        environment.powerh.append(Powerh(-284.0, -63.0, 5))
        environment.powerh.append(Powerh(245.0, -147.0, 5))
        environment.powerh.append(Powerh(319.0, -147.0, 5))
        environment.powerh.append(Powerh(379.0, -147.0, 5))
        environment.powerh.append(Powerh(398.0, 234.0, 5))
        environment.powerh.append(Powerh(159.0, 499.0, 5))
        base.camera.setPos(Point3(-212.693, 492.953, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-212.686, 476.273, 9))
        environment.laps = 3
        self.finishCredits = [600, 300, 150, 100, 75, 0]
        self.finishPlace = 1
