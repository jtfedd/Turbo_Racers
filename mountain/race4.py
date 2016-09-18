from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.787811636925, 0.926316022873, 1.0)
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
        environment.playerShip = Ship(player1ship, -156.0, 72.0, 5, -82.0, environment, 5, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -158.0, 88.0, 5, -82.0, environment, 5, 2)
        self.xpoints = [-101.0, -39.0, 39.0, 91.0, 137.0, 124.0, -4.0, -24.0, -69.0, -176.0, -243.0, -345.0, -399.0, -465.0, -595.0, -620.0, -625.0, -628.0, -611.0, -589.0, -541.0, -481.0, -429.0, -383.0, -325.0, -302.0, -234.0, -125.0, -88.0, -46.0, -48.0, -98.0, -176.0, -217.0, -228.0, -207.0, -157.0]
        self.ypoints = [73.0, 37.0, -7.0, -17.0, 43.0, 113.0, 254.0, 271.0, 289.0, 303.0, 308.0, 308.0, 308.0, 316.0, 295.0, 263.0, 212.0, 143.0, 68.0, 40.0, 22.0, 12.0, -13.0, -76.0, -200.0, -233.0, -248.0, -252.0, -233.0, -190.0, -147.0, -111.0, -77.0, -29.0, 4.0, 45.0, 76.0]
        self.xplaces = [-158.0, -161.0, -163.0, -167.0, -170.0]
        self.yplaces = [88.0, 106.0, 123.0, 78.0, 98.0]
        self.hs = [-82.0, -82.0, -82.0, -82.0, -82.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 6, 11, 17, 26, 0]
        self.pointsnum = 37
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
        environment.barriers.append(Barrier(18.0, -43.0, 352.0))
        environment.barriers.append(Barrier(217.0, 22.0, 450.0))
        environment.barriers.append(Barrier(82.0, 247.0, 537.0))
        environment.barriers.append(Barrier(-412.0, 287.0, 523.0))
        environment.barriers.append(Barrier(-535.0, 279.0, 523.0))
        environment.barriers.append(Barrier(-604.0, 15.0, 323.0))
        environment.barriers.append(Barrier(-367.0, -230.0, 323.0))
        environment.barriers.append(Barrier(-204.0, 96.0, 405.0))
        environment.barriers.append(Barrier(-113.0, 141.0, 340.0))
        environment.barriers.append(Barrier(10.0, -271.0, 394.0))
        environment.barriers.append(Barrier(48.0, -187.0, 457.0))
        environment.barriers.append(Barrier(-20.0, -90.0, 511.0))
        environment.barriers.append(Barrier(-59.0, 101.0, -53.0))
        environment.checkpoints.append(Checkpoint(-4.0, 254.0, 0, 51.0))
        environment.checkpoints.append(Checkpoint(-345.0, 308.0, 0, 85.0))
        environment.checkpoints.append(Checkpoint(-628.0, 143.0, 0, 180.0))
        environment.checkpoints.append(Checkpoint(-234.0, -248.0, 0, 262.0))
        environment.checkpoints.append(Startingline(-146.0, 100.0, 0, -82.0))
        environment.powerups.append(Powerup(-30.0, 50.0, 5))
        environment.powerups.append(Powerup(-37.0, 39.0, 5))
        environment.powerups.append(Powerup(-43.0, 30.0, 5))
        environment.powerups.append(Powerup(62.0, -11.0, 5))
        environment.powerups.append(Powerup(62.0, -24.0, 5))
        environment.powerups.append(Powerup(79.0, 202.0, 5))
        environment.powerups.append(Powerup(-464.0, 316.0, 5))
        environment.powerups.append(Powerup(-633.0, 262.0, 5))
        environment.powerups.append(Powerup(-519.0, 19.0, 5))
        environment.powerups.append(Powerup(-100.0, -126.0, 5))
        environment.powerups.append(Powerup(-98.0, -112.0, 5))
        environment.powerh.append(Powerh(67.0, 192.0, 5))
        environment.powerh.append(Powerh(-464.0, 305.0, 5))
        environment.powerh.append(Powerh(-464.0, 327.0, 5))
        environment.powerh.append(Powerh(-620.0, 262.0, 5))
        environment.powerh.append(Powerh(-519.0, 40.0, 5))
        environment.powerh.append(Powerh(-97.0, -97.0, 5))
        base.camera.setPos(Point3(-170.854, 69.9124, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-172.854, 85.9124, 9))
        environment.laps = 3
        self.finishCredits = [750, 375, 187, 125, 93, 0]
        self.finishPlace = 1
