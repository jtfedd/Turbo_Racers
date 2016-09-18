from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.441082626581, 0.620711505413, 0.855103313923)
        environment.earth = loader.loadModel("city/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(5.35364, 5.35364, 5.35364))
        environment.earth.setBin("background", 1)
        environment.earth.find("**/trees").setBin("transparent", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.765608370304, 0.765608370304, 0.765608370304, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.765608370304, 0.765608370304, 0.765608370304, 1))
        environment.domenum = 4
        environment.playerShip = Ship(player1ship, -40.0, 117.0, 5, -178.0, environment, 6, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -59.0, 117.0, 5, -178.0, environment, 6, 2)
        self.xpoints = [-50.0, -47.0, -26.0, 91.0, 117.0, 117.0, 115.0, 80.0, -119.0, -173.0, -216.0, -216.0, -210.0, -182.0, -15.0, 61.0, 88.0, 83.0, 52.0, -23.0, -50.0, -50.0]
        self.ypoints = [-145.0, -196.0, -219.0, -222.0, -181.0, -128.0, -83.0, -56.0, -49.0, -49.0, 1.0, 392.0, 454.0, 479.0, 486.0, 476.0, 427.0, 351.0, 317.0, 299.0, 261.0, 126.0]
        self.xplaces = [-59.0, -59.0, -40.0, -40.0, -58.0]
        self.yplaces = [117.0, 131.0, 131.0, 146.0, 145.0]
        self.hs = [-178.0, -178.0, -178.0, -178.0, -178.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 0, 5, 8, 11, 14, 0]
        self.pointsnum = 22
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
        environment.barriers.append(Barrier(-50.0, -246.0, -10.0))
        environment.barriers.append(Barrier(122.0, -235.0, 50.0))
        environment.barriers.append(Barrier(-229.0, -61.0, 126.0))
        environment.barriers.append(Barrier(-226.0, 496.0, 37.0))
        environment.barriers.append(Barrier(239.0, 486.0, -43.0))
        environment.barriers.append(Barrier(223.0, 308.0, -147.0))
        environment.barriers.append(Barrier(-74.0, 320.0, -135.0))
        environment.checkpoints.append(Checkpoint(-50.0, -145.0, 0, -178.0))
        environment.checkpoints.append(Checkpoint(117.0, -128.0, 0, 3.0))
        environment.checkpoints.append(Checkpoint(-119.0, -49.0, 0, 89.0))
        environment.checkpoints.append(Checkpoint(-216.0, 392.0, 0, 4.0))
        environment.checkpoints.append(Checkpoint(-15.0, 486.0, 0, -86.0))
        environment.checkpoints.append(Startingline(-49.0, 105.0, 0, 0.0))
        environment.powerups.append(Powerup(-38.0, 29.0, 5))
        environment.powerups.append(Powerup(-50.0, 29.0, 5))
        environment.powerups.append(Powerup(-64.0, 29.0, 5))
        environment.powerups.append(Powerup(26.0, -210.0, 5))
        environment.powerups.append(Powerup(26.0, -219.0, 5))
        environment.powerups.append(Powerup(26.0, -231.0, 5))
        environment.powerups.append(Powerup(-50.0, -52.0, 5))
        environment.powerups.append(Powerup(-203.0, 317.0, 5))
        environment.powerups.append(Powerup(-217.0, 317.0, 5))
        environment.powerups.append(Powerup(-231.0, 317.0, 5))
        environment.powerups.append(Powerup(-58.0, 478.0, 5))
        environment.powerups.append(Powerup(218.0, 410.0, 5))
        environment.powerups.append(Powerup(-64.0, 198.0, 5))
        environment.powerups.append(Powerup(-50.0, 198.0, 5))
        environment.powerups.append(Powerup(-36.0, 198.0, 5))
        environment.powerh.append(Powerh(-35.0, -67.0, 5))
        environment.powerh.append(Powerh(-35.0, -36.0, 5))
        environment.powerh.append(Powerh(-67.0, -36.0, 5))
        environment.powerh.append(Powerh(-67.0, -67.0, 5))
        environment.powerh.append(Powerh(-208.0, 51.0, 5))
        environment.powerh.append(Powerh(-217.0, 51.0, 5))
        environment.powerh.append(Powerh(-228.0, 51.0, 5))
        environment.powerh.append(Powerh(-58.0, 492.0, 5))
        base.camera.setPos(Point3(-40.5235, 131.991, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-59.5235, 131.991, 9))
        environment.laps = 3
        self.finishCredits = [400, 200, 100, 66, 50, 0]
        self.finishPlace = 1
