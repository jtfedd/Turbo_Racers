from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.704761922359, 0.907268106937, 1.0)
        environment.earth = loader.loadModel("canyon/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(5, 5, 5))
        environment.earth.setBin("background", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 4
        environment.playerShip = Ship(player1ship, -173.0, -455.0, 5, 86.0, environment, 8, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -173.0, -430.0, 5, 86.0, environment, 8, 2)
        self.xpoints = [-279.0, -325.0, -336.0, -412.0, -439.0, -439.0, -424.0, -374.0, -314.0, -274.0, -287.0, -286.0, -252.0, -233.0, -218.0, -183.0, -139.0, -113.0, -109.0, -59.0, -30.0, 24.0, 174.0, 238.0, 318.0, 363.0, 353.0, 337.0, 286.0, 243.0, 222.0, 178.0, 72.0, -124.0]
        self.ypoints = [-407.0, -364.0, -323.0, -236.0, -161.0, 142.0, 181.0, 204.0, 167.0, -45.0, -107.0, -162.0, -238.0, -337.0, -384.0, -415.0, -374.0, -277.0, -183.0, -63.0, 32.0, 112.0, 198.0, 212.0, 192.0, 137.0, 41.0, -111.0, -186.0, -306.0, -401.0, -435.0, -463.0, -463.0]
        self.xplaces = [-173.0, -173.0, -160.0, -160.0, -160.0]
        self.yplaces = [-430.0, -408.0, -408.0, -431.0, -456.0]
        self.hs = [86.0, 86.0, 86.0, 86.0, 86.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 5, 13, 17, 23, 26, 30, 0]
        self.pointsnum = 34
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
        environment.barriers.append(Barrier(-9.0, -87.0, 129.0))
        environment.barriers.append(Barrier(-173.0, -192.0, 15.0))
        environment.barriers.append(Barrier(-134.0, -152.0, 72.0))
        environment.barriers.append(Barrier(-463.0, 236.0, 27.0))
        environment.barriers.append(Barrier(-433.0, 247.0, 12.0))
        environment.barriers.append(Barrier(-406.0, 247.0, -9.0))
        environment.barriers.append(Barrier(-277.0, 232.0, -90.0))
        environment.barriers.append(Barrier(-277.0, 213.0, -90.0))
        environment.barriers.append(Barrier(-277.0, 193.0, -90.0))
        environment.barriers.append(Barrier(359.0, 218.0, -75.0))
        environment.barriers.append(Barrier(203.0, -364.0, -117.0))
        environment.barriers.append(Barrier(186.0, -470.0, -204.0))
        environment.checkpoints.append(Checkpoint(-439.0, -161.0, 0, -2.0))
        environment.checkpoints.append(Checkpoint(-439.0, 142.0, 0, -2.0))
        environment.checkpoints.append(Checkpoint(-233.0, -337.0, 0, -176.0))
        environment.checkpoints.append(Checkpoint(-113.0, -277.0, 0, -15.0))
        environment.checkpoints.append(Checkpoint(238.0, 212.0, 0, -80.0))
        environment.checkpoints.append(Checkpoint(353.0, 41.0, 0, -189.0))
        environment.checkpoints.append(Checkpoint(222.0, -401.0, 0, -199.0))
        environment.checkpoints.append(Startingline(-188.0, -430.0, 0, 86.0))
        environment.powerups.append(Powerup(-336.0, -324.0, 5))
        environment.powerups.append(Powerup(-323.0, -324.0, 5))
        environment.powerups.append(Powerup(-349.0, -324.0, 5))
        environment.powerups.append(Powerup(-441.0, -98.0, 5))
        environment.powerups.append(Powerup(-455.0, -98.0, 5))
        environment.powerups.append(Powerup(-374.0, 203.0, 5))
        environment.powerups.append(Powerup(-374.0, 219.0, 5))
        environment.powerups.append(Powerup(-315.0, 112.0, 5))
        environment.powerups.append(Powerup(-290.0, 112.0, 5))
        environment.powerups.append(Powerup(-273.0, -47.0, 5))
        environment.powerups.append(Powerup(-265.0, -237.0, 5))
        environment.powerups.append(Powerup(-252.0, -237.0, 5))
        environment.powerups.append(Powerup(-236.0, -237.0, 5))
        environment.powerups.append(Powerup(-127.0, -332.0, 5))
        environment.powerups.append(Powerup(90.0, 155.0, 5))
        environment.powerups.append(Powerup(89.0, 168.0, 5))
        environment.powerups.append(Powerup(107.0, 155.0, 5))
        environment.powerups.append(Powerup(344.0, 160.0, 5))
        environment.powerups.append(Powerup(313.0, -253.0, 5))
        environment.powerups.append(Powerup(328.0, -253.0, 5))
        environment.powerups.append(Powerup(342.0, -253.0, 5))
        environment.powerups.append(Powerup(80.0, -423.0, 5))
        environment.powerups.append(Powerup(57.0, -439.0, 5))
        environment.powerups.append(Powerup(45.0, -439.0, 5))
        environment.powerups.append(Powerup(-103.0, -444.0, 5))
        environment.powerups.append(Powerup(-103.0, -459.0, 5))
        environment.powerups.append(Powerup(-103.0, -471.0, 5))
        environment.powerups.append(Powerup(-119.0, -425.0, 5))
        environment.powerups.append(Powerup(-129.0, -425.0, 5))
        environment.powerh.append(Powerh(-427.0, -98.0, 5))
        environment.powerh.append(Powerh(-301.0, 112.0, 5))
        environment.powerh.append(Powerh(-280.0, 112.0, 5))
        environment.powerh.append(Powerh(-114.0, -332.0, 5))
        environment.powerh.append(Powerh(-140.0, -332.0, 5))
        environment.powerh.append(Powerh(-60.0, -49.0, 5))
        environment.powerh.append(Powerh(-45.0, -55.0, 5))
        environment.powerh.append(Powerh(69.0, 155.0, 5))
        environment.powerh.append(Powerh(90.0, 141.0, 5))
        environment.powerh.append(Powerh(347.0, -40.0, 5))
        environment.powerh.append(Powerh(332.0, -40.0, 5))
        environment.powerh.append(Powerh(362.0, -40.0, 5))
        environment.powerh.append(Powerh(270.0, -226.0, 5))
        environment.powerh.append(Powerh(260.0, -226.0, 5))
        environment.powerh.append(Powerh(282.0, -226.0, 5))
        environment.powerh.append(Powerh(87.0, -456.0, 5))
        environment.powerh.append(Powerh(87.0, -472.0, 5))
        environment.powerh.append(Powerh(-103.0, -408.0, 5))
        base.camera.setPos(Point3(-158.037, -456.046, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-158.037, -431.046, 9))
        environment.laps = 3
        self.finishCredits = [800, 400, 200, 133, 100, 0]
        self.finishPlace = 1
