from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.0334966816008, 0.0, 0.149158328772)
        environment.earth = loader.loadModel("arctic/world/aw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.5, 3.5, 3.5))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.114617533982, 0.114617533982, 0.114617533982, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.0794800668955, 0.0794800668955, 0.0794800668955, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.0794800668955, 0.0794800668955, 0.0794800668955, 1))
        environment.domenum = 2
        environment.playerShip = Ship(player1ship, -258.0, -4.0, 5, 0.0, environment, 14, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -270.0, -4.0, 5, 0.0, environment, 14, 2)
        self.xpoints = [-254.0, -236.0, -226.0, -199.0, -166.0, -106.0, -42.0, 66.0, 156.0, 173.0, 151.0, 124.0, 89.0, 25.0, -42.0, -59.0, -66.0, -61.0, -46.0, 14.0, 69.0, 86.0, 95.0, 95.0, 88.0, 67.0, 41.0, -53.0, -79.0, -103.0, -119.0, -132.0, -135.0, -96.0, -33.0, 65.0, 181.0, 241.0, 269.0, 281.0, 298.0, 318.0, 290.0, 228.0, 191.0, 127.0, 23.0, -80.0, -126.0, -144.0, -145.0, -141.0, -132.0, -112.0, -77.0, -47.0, 34.0, 82.0, 108.0, 126.0, 137.0, 137.0, 138.0, 105.0, 50.0, 32.0, -24.0, -98.0, -198.0, -255.0, -276.0, -268.0, -280.0, -272.0]
        self.ypoints = [55.0, 104.0, 135.0, 161.0, 191.0, 264.0, 300.0, 314.0, 300.0, 268.0, 193.0, 166.0, 156.0, 142.0, 144.0, 136.0, 111.0, 88.0, 69.0, 30.0, 15.0, -5.0, -25.0, -46.0, -63.0, -72.0, -73.0, -68.0, -67.0, -72.0, -84.0, -108.0, -136.0, -163.0, -207.0, -225.0, -214.0, -195.0, -154.0, -85.0, 37.0, 159.0, 215.0, 212.0, 206.0, 226.0, 233.0, 220.0, 196.0, 156.0, 96.0, 60.0, 41.0, 27.0, 14.0, 16.0, 30.0, 65.0, 60.0, 46.0, 20.0, -80.0, -95.0, -124.0, -161.0, -195.0, -216.0, -249.0, -248.0, -218.0, -184.0, -120.0, -63.0, 1.0]
        self.xplaces = [-270.0, -282.0, -296.0, -283.0, -270.0]
        self.yplaces = [-4.0, -4.0, -4.0, -21.0, -21.0]
        self.hs = [0.0, 0.0, 0.0, 0.0, 0.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 5, 9, 18, 20, 33, 38, 43, 50, 55, 58, 64, 68, 70, 0]
        self.pointsnum = 74
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 14, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-153.0, -120.0, 244.0))
        environment.barriers.append(Barrier(-154.0, -139.0, 293.0))
        environment.barriers.append(Barrier(-144.0, -152.0, 319.0))
        environment.barriers.append(Barrier(-133.0, -161.0, 319.0))
        environment.barriers.append(Barrier(-151.0, 186.0, 420.0))
        environment.barriers.append(Barrier(-144.0, 198.0, 420.0))
        environment.barriers.append(Barrier(-142.0, 197.0, 236.0))
        environment.barriers.append(Barrier(-148.0, 186.0, 236.0))
        environment.barriers.append(Barrier(191.0, 309.0, 287.0))
        environment.barriers.append(Barrier(153.0, -112.0, 226.0))
        environment.barriers.append(Barrier(-24.0, -182.0, -25.0))
        environment.barriers.append(Barrier(69.0, -205.0, -25.0))
        environment.barriers.append(Barrier(191.0, 239.0, 250.0))
        environment.barriers.append(Barrier(161.0, 185.0, 250.0))
        environment.checkpoints.append(Checkpoint(-106.0, 264.0, 0, -52.0))
        environment.checkpoints.append(Checkpoint(173.0, 268.0, 0, -184.0))
        environment.checkpoints.append(Checkpoint(-46.0, 69.0, 0, 225.0))
        environment.checkpoints.append(Checkpoint(69.0, 15.0, 0, -139.0))
        environment.checkpoints.append(Checkpoint(-96.0, -163.0, 0, -127.0))
        environment.checkpoints.append(Checkpoint(269.0, -154.0, 0, -33.0))
        environment.checkpoints.append(Checkpoint(228.0, 212.0, 0, 114.0))
        environment.checkpoints.append(Checkpoint(-145.0, 96.0, 0, 181.0))
        environment.checkpoints.append(Checkpoint(-47.0, 16.0, 0, 292.0))
        environment.checkpoints.append(Checkpoint(82.0, 65.0, 0, 274.0))
        environment.checkpoints.append(Checkpoint(105.0, -124.0, 0, 124.0))
        environment.checkpoints.append(Checkpoint(-98.0, -249.0, 0, 105.0))
        environment.checkpoints.append(Checkpoint(-255.0, -218.0, 0, 63.0))
        environment.checkpoints.append(Startingline(-271.0, 15.0, 0, 0.0))
        environment.powerups.append(Powerup(-234.0, 105.0, 5))
        environment.powerups.append(Powerup(-199.0, 162.0, 5))
        environment.powerups.append(Powerup(-195.0, 129.0, 5))
        environment.powerups.append(Powerup(-195.0, 93.0, 5))
        environment.powerups.append(Powerup(-125.0, 182.0, 5))
        environment.powerups.append(Powerup(-131.0, 192.0, 5))
        environment.powerups.append(Powerup(-139.0, 198.0, 5))
        environment.powerups.append(Powerup(-149.0, 202.0, 5))
        environment.powerups.append(Powerup(-161.0, 203.0, 5))
        environment.powerups.append(Powerup(296.0, 159.0, 5))
        environment.powerups.append(Powerup(315.0, 159.0, 5))
        environment.powerups.append(Powerup(334.0, 159.0, 5))
        environment.powerups.append(Powerup(253.0, -175.0, 5))
        environment.powerups.append(Powerup(212.0, -206.0, 5))
        environment.powerups.append(Powerup(4.0, -212.0, 5))
        environment.powerups.append(Powerup(4.0, -196.0, 5))
        environment.powerups.append(Powerup(4.0, -232.0, 5))
        environment.powerups.append(Powerup(-198.0, -248.0, 5))
        environment.powerups.append(Powerup(-200.0, -266.0, 5))
        environment.powerups.append(Powerup(-284.0, -95.0, 5))
        environment.powerups.append(Powerup(-277.0, -87.0, 5))
        environment.powerups.append(Powerup(-266.0, -76.0, 5))
        environment.powerups.append(Powerup(-113.0, 26.0, 5))
        environment.powerups.append(Powerup(138.0, 20.0, 5))
        environment.powerups.append(Powerup(30.0, 6.0, 5))
        environment.powerups.append(Powerup(30.0, 19.0, 5))
        environment.powerups.append(Powerup(30.0, 30.0, 5))
        environment.powerups.append(Powerup(30.0, 68.0, 5))
        environment.powerups.append(Powerup(30.0, 84.0, 5))
        environment.powerups.append(Powerup(30.0, 100.0, 5))
        environment.powerups.append(Powerup(44.0, 46.0, 5))
        environment.powerups.append(Powerup(59.0, 46.0, 5))
        environment.powerups.append(Powerup(73.0, 46.0, 5))
        environment.powerups.append(Powerup(8.0, 48.0, 5))
        environment.powerups.append(Powerup(-4.0, 48.0, 5))
        environment.powerups.append(Powerup(-15.0, 48.0, 5))
        environment.powerh.append(Powerh(-294.0, 81.0, 5))
        environment.powerh.append(Powerh(84.0, 220.0, 5))
        environment.powerh.append(Powerh(84.0, 232.0, 5))
        environment.powerh.append(Powerh(84.0, 246.0, 5))
        environment.powerh.append(Powerh(84.0, 300.0, 5))
        environment.powerh.append(Powerh(84.0, 314.0, 5))
        environment.powerh.append(Powerh(84.0, 323.0, 5))
        environment.powerh.append(Powerh(256.0, -198.0, 5))
        environment.powerh.append(Powerh(212.0, -190.0, 5))
        environment.powerh.append(Powerh(-197.0, -234.0, 5))
        environment.powerh.append(Powerh(-54.0, -67.0, 5))
        environment.powerh.append(Powerh(-59.0, 137.0, 5))
        base.camera.setPos(Point3(-258, -19, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-270, -19, 9))
        environment.laps = 2
        self.finishCredits = [850, 425, 212, 141, 106, 0]
        self.finishPlace = 1
