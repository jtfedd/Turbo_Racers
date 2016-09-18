from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.845344007015, 0.845344185829, 0.845344185829)
        environment.earth = loader.loadModel("arctic/world/aw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.5, 3.5, 3.5))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.568484902382, 0.568484902382, 0.568484902382, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.432559132576, 0.432559132576, 0.432559132576, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.432559132576, 0.432559132576, 0.432559132576, 1))
        environment.domenum = 1
        environment.playerShip = Ship(player1ship, 421.0, 100.0, 5, -14.0, environment, 8, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 408.0, 104.0, 5, -14.0, environment, 8, 2)
        self.xpoints = [411.0, 390.0, 354.0, 302.0, 246.0, 187.0, 129.0, 54.0, 3.0, -41.0, -98.0, -140.0, -145.0, -143.0, -144.0, -142.0, -138.0, -126.0, -102.0, -72.0, -40.0, 21.0, 60.0, 39.0, 0.0, -30.0, -53.0, -65.0, -64.0, -43.0, 17.0, 90.0, 129.0, 147.0, 151.0, 174.0, 213.0, 250.0, 264.0, 226.0, 218.0, 240.0, 345.0, 386.0]
        self.ypoints = [175.0, 236.0, 256.0, 247.0, 211.0, 204.0, 226.0, 261.0, 292.0, 296.0, 267.0, 212.0, 152.0, 115.0, 84.0, 64.0, 49.0, 34.0, 22.0, 16.0, 21.0, 14.0, 44.0, 77.0, 73.0, 65.0, 75.0, 100.0, 131.0, 144.0, 140.0, 154.0, 167.0, 185.0, 199.0, 269.0, 339.0, 337.0, 271.0, 162.0, 123.0, 79.0, 86.0, 110.0]
        self.xplaces = [408.0, 393.0, 382.0, 397.0, 412.0]
        self.yplaces = [104.0, 108.0, 102.0, 98.0, 94.0]
        self.hs = [-14.0, -14.0, -14.0, -14.0, -14.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 5, 9, 14, 23, 30, 35, 40, 0]
        self.pointsnum = 44
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 8, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-50.0, 46.0, 359.0))
        environment.barriers.append(Barrier(-35.0, 46.0, 359.0))
        environment.barriers.append(Barrier(-18.0, 46.0, 359.0))
        environment.barriers.append(Barrier(-2.0, 46.0, 359.0))
        environment.barriers.append(Barrier(74.0, 9.0, 409.0))
        environment.barriers.append(Barrier(88.0, 63.0, 447.0))
        environment.barriers.append(Barrier(366.0, 157.0, 447.0))
        environment.barriers.append(Barrier(362.0, 211.0, 474.0))
        environment.barriers.append(Barrier(341.0, 291.0, 552.0))
        environment.barriers.append(Barrier(184.0, 180.0, 497.0))
        environment.barriers.append(Barrier(1.0, 221.0, 464.0))
        environment.barriers.append(Barrier(-3.0, 247.0, 464.0))
        environment.barriers.append(Barrier(-101.0, 213.0, 580.0))
        environment.barriers.append(Barrier(-170.0, 187.0, 655.0))
        environment.barriers.append(Barrier(199.0, 363.0, 746.0))
        environment.barriers.append(Barrier(296.0, 330.0, 647.0))
        environment.barriers.append(Barrier(230.0, 46.0, 675.0))
        environment.barriers.append(Barrier(291.0, 11.0, 711.0))
        environment.checkpoints.append(Checkpoint(187.0, 204.0, 0, 54.0))
        environment.checkpoints.append(Checkpoint(-41.0, 296.0, 0, 102.0))
        environment.checkpoints.append(Checkpoint(-144.0, 84.0, 0, 176.0))
        environment.checkpoints.append(Checkpoint(39.0, 77.0, 0, 420.0))
        environment.checkpoints.append(Checkpoint(17.0, 140.0, 0, 275.0))
        environment.checkpoints.append(Checkpoint(174.0, 269.0, 0, 340.0))
        environment.checkpoints.append(Checkpoint(218.0, 123.0, 0, 175.0))
        environment.checkpoints.append(Startingline(412.0, 119.0, 0, -14.0))
        environment.powerups.append(Powerup(247.0, 213.0, 5))
        environment.powerups.append(Powerup(269.0, 213.0, 5))
        environment.powerups.append(Powerup(247.0, 238.0, 5))
        environment.powerups.append(Powerup(221.0, 208.0, 5))
        environment.powerups.append(Powerup(244.0, 178.0, 5))
        environment.powerups.append(Powerup(404.0, 199.0, 5))
        environment.powerups.append(Powerup(91.0, 248.0, 5))
        environment.powerups.append(Powerup(91.0, 215.0, 5))
        environment.powerups.append(Powerup(46.0, 44.0, 5))
        environment.powerups.append(Powerup(60.0, 44.0, 5))
        environment.powerups.append(Powerup(187.0, 301.0, 5))
        environment.powerups.append(Powerup(306.0, 91.0, 5))
        environment.powerups.append(Powerup(306.0, 71.0, 5))
        environment.powerups.append(Powerup(306.0, 52.0, 5))
        environment.powerh.append(Powerh(91.0, 231.0, 5))
        environment.powerh.append(Powerh(-144.0, 151.0, 5))
        environment.powerh.append(Powerh(-143.0, 68.0, 5))
        environment.powerh.append(Powerh(74.0, 44.0, 5))
        environment.powerh.append(Powerh(35.0, 140.0, 5))
        base.camera.setPos(Point3(417.371, 85.4456, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(404.371, 89.4456, 9))
        environment.laps = 3
        self.finishCredits = [400, 200, 100, 66, 50, 0]
        self.finishPlace = 1
