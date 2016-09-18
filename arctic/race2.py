from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.40000000596, 0.40000000596, 0.40000000596)
        environment.earth = loader.loadModel("arctic/world/aw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.5, 3.5, 3.5))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.386215537786, 0.386215537786, 0.386215537786, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.38446110487, 0.38446110487, 0.38446110487, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.38446110487, 0.38446110487, 0.38446110487, 1))
        environment.domenum = 1
        environment.playerShip = Ship(player1ship, -197.0, -189.0, 5, -23.0, environment, 6, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -197.0, -203.0, 5, -23.0, environment, 6, 2)
        self.xpoints = [-135.0, -122.0, -95.0, -55.0, 56.0, 78.0, 95.0, 93.0, 71.0, 38.0, -47.0, -78.0, -121.0, -142.0, -144.0, -128.0, -65.0, 113.0, 173.0, 221.0, 243.0, 272.0, 291.0, 284.0, 268.0, 205.0, 91.0, 7.0, -65.0, -114.0, -146.0, -147.0]
        self.ypoints = [-116.0, -88.0, -68.0, -68.0, -73.0, -68.0, -44.0, -24.0, 9.0, 26.0, 17.0, 16.0, 29.0, 76.0, 137.0, 185.0, 217.0, 220.0, 203.0, 135.0, 89.0, 49.0, -1.0, -65.0, -155.0, -214.0, -227.0, -213.0, -222.0, -237.0, -219.0, -162.0]
        self.xplaces = [-197.0, -183.0, -177.0, -163.0, -159.0]
        self.yplaces = [-203.0, -196.0, -213.0, -205.0, -223.0]
        self.hs = [-23.0, -23.0, -23.0, -23.0, -23.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 9, 15, 18, 23, 27, 0]
        self.pointsnum = 32
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
        environment.barriers.append(Barrier(-196.0, -263.0, 90.0))
        environment.barriers.append(Barrier(-196.0, -232.0, 90.0))
        environment.barriers.append(Barrier(257.0, -98.0, 255.0))
        environment.barriers.append(Barrier(228.0, -237.0, 204.0))
        environment.barriers.append(Barrier(-155.0, 172.0, 59.0))
        environment.barriers.append(Barrier(-128.0, 215.0, 43.0))
        environment.barriers.append(Barrier(-110.0, 232.0, 43.0))
        environment.barriers.append(Barrier(225.0, 219.0, -35.0))
        environment.barriers.append(Barrier(252.0, 200.0, -45.0))
        environment.barriers.append(Barrier(348.0, 105.0, -113.0))
        environment.barriers.append(Barrier(333.0, 74.0, -113.0))
        environment.barriers.append(Barrier(322.0, 48.0, -105.0))
        environment.barriers.append(Barrier(305.0, -104.0, -88.0))
        environment.checkpoints.append(Checkpoint(38.0, 26.0, 0, 95.0))
        environment.checkpoints.append(Checkpoint(-128.0, 185.0, 0, -29.0))
        environment.checkpoints.append(Checkpoint(173.0, 203.0, 0, -119.0))
        environment.checkpoints.append(Checkpoint(284.0, -65.0, 0, -185.0))
        environment.checkpoints.append(Checkpoint(7.0, -213.0, 0, -272.0))
        environment.checkpoints.append(Startingline(-166.0, -184.0, 0, -23.0))
        environment.powerups.append(Powerup(-162.0, -134.0, 5))
        environment.powerups.append(Powerup(-148.0, -141.0, 5))
        environment.powerups.append(Powerup(-136.0, -150.0, 5))
        environment.powerups.append(Powerup(11.0, 11.0, 5))
        environment.powerups.append(Powerup(11.0, 23.0, 5))
        environment.powerups.append(Powerup(11.0, 33.0, 5))
        environment.powerups.append(Powerup(-59.0, 218.0, 5))
        environment.powerups.append(Powerup(-59.0, 231.0, 5))
        environment.powerups.append(Powerup(314.0, 182.0, 5))
        environment.powerups.append(Powerup(332.0, 182.0, 5))
        environment.powerups.append(Powerup(231.0, 110.0, 5))
        environment.powerups.append(Powerup(216.0, 110.0, 5))
        environment.powerups.append(Powerup(266.0, -158.0, 5))
        environment.powerups.append(Powerup(149.0, -107.0, 5))
        environment.powerups.append(Powerup(-54.0, -224.0, 5))
        environment.powerups.append(Powerup(-54.0, -255.0, 5))
        environment.powerh.append(Powerh(11.0, -74.0, 5))
        environment.powerh.append(Powerh(-59.0, 204.0, 5))
        environment.powerh.append(Powerh(-54.0, -237.0, 5))
        base.camera.setPos(Point3(-202.861, -202.808, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-202.861, -216.808, 9))
        environment.laps = 3
        self.finishCredits = [750, 375, 187, 125, 93, 0]
        self.finishPlace = 1
