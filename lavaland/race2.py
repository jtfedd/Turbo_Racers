from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.539348363876, 1.0, 1.0)
        environment.earth = loader.loadModel("lavaland/world/lw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(8, 8, 8))
        environment.earth.setBin("background", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 5
        environment.playerShip = Ship(player1ship, 389.0, 319.0, 5, -89.0, environment, 4, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 389.0, 300.0, 5, -89.0, environment, 4, 2)
        self.xpoints = [470.0, 518.0, 535.0, 521.0, 511.0, 402.0, 368.0, 224.0, 150.0, -3.0, -172.0, -335.0, -384.0, -384.0, -290.0, -94.0, 192.0, 359.0]
        self.ypoints = [293.0, 247.0, 169.0, -119.0, -181.0, -291.0, -346.0, -494.0, -620.0, -635.0, -640.0, -623.0, -586.0, -451.0, -351.0, -152.0, 139.0, 298.0]
        self.xplaces = [389.0, 389.0, 368.0, 368.0, 368.0]
        self.yplaces = [300.0, 280.0, 280.0, 299.0, 319.0]
        self.hs = [-89.0, -89.0, -89.0, -89.0, -89.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 3, 10, 15, 0]
        self.pointsnum = 18
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 4, self.startPlaces, i+1))
        environment.checkpoints.append(Checkpoint(521.0, -119.0, 0, -183.0))
        environment.checkpoints.append(Checkpoint(-172.0, -640.0, 0, -271.0))
        environment.checkpoints.append(Checkpoint(-94.0, -152.0, 0, -409.0))
        environment.checkpoints.append(Startingline(415.0, 299.0, 0, -89.0))
        environment.powerups.append(Powerup(498.0, 72.0, 5))
        environment.powerups.append(Powerup(520.0, 72.0, 5))
        environment.powerups.append(Powerup(545.0, 72.0, 5))
        environment.powerups.append(Powerup(565.0, 72.0, 5))
        environment.powerups.append(Powerup(378.0, -353.0, 5))
        environment.powerups.append(Powerup(368.0, -346.0, 5))
        environment.powerups.append(Powerup(358.0, -339.0, 5))
        environment.powerups.append(Powerup(349.0, -330.0, 5))
        environment.powerups.append(Powerup(343.0, -325.0, 5))
        environment.powerups.append(Powerup(-362.0, -530.0, 5))
        environment.powerups.append(Powerup(-382.0, -530.0, 5))
        environment.powerups.append(Powerup(-407.0, -530.0, 5))
        environment.powerups.append(Powerup(-432.0, -530.0, 5))
        environment.powerups.append(Powerup(136.0, -200.0, 5))
        environment.powerups.append(Powerup(230.0, 111.0, 5))
        environment.powerups.append(Powerup(248.0, 133.0, 5))
        environment.powerups.append(Powerup(191.0, 139.0, 5))
        environment.powerups.append(Powerup(212.0, 123.0, 5))
        environment.powerups.append(Powerup(173.0, 160.0, 5))
        environment.powerups.append(Powerup(192.0, 179.0, 5))
        environment.powerups.append(Powerup(209.0, 160.0, 5))
        environment.powerups.append(Powerup(228.0, 143.0, 5))
        environment.powerh.append(Powerh(166.0, -561.0, 5))
        environment.powerh.append(Powerh(181.0, -576.0, 5))
        environment.powerh.append(Powerh(191.0, -591.0, 5))
        environment.powerh.append(Powerh(203.0, -607.0, 5))
        environment.powerh.append(Powerh(-268.0, -367.0, 5))
        environment.powerh.append(Powerh(-276.0, -361.0, 5))
        environment.powerh.append(Powerh(-284.0, -354.0, 5))
        environment.powerh.append(Powerh(-296.0, -342.0, 5))
        environment.powerh.append(Powerh(-305.0, -331.0, 5))
        base.camera.setPos(Point3(374.002, 318.738, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(374.002, 299.738, 9))
        environment.laps = 2
        self.finishCredits = [500, 250, 125, 83, 62, 0]
        self.finishPlace = 1
