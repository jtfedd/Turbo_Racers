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
        environment.playerShip = Ship(player1ship, -194.0, -113.0, 5, -94.0, environment, 5, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -194.0, -99.0, 5, -94.0, environment, 5, 2)
        self.xpoints = [-124.0, -52.0, -38.0, -33.0, -38.0, -62.0, -167.0, -305.0, -345.0, -394.0, -396.0, -351.0, -187.0, -146.0, -100.0, -106.0, -178.0, -300.0, -355.0, -428.0, -443.0, -468.0, -448.0, -368.0, -247.0, -202.0]
        self.ypoints = [-121.0, -165.0, -204.0, -329.0, -418.0, -458.0, -457.0, -448.0, -397.0, -344.0, -303.0, -283.0, -324.0, -390.0, -389.0, -282.0, -240.0, -243.0, -228.0, -226.0, -227.0, -192.0, -142.0, -107.0, -90.0, -95.0]
        self.xplaces = [-194.0, -194.0, -194.0, -210.0, -210.0]
        self.yplaces = [-99.0, -85.0, -68.0, -87.0, -100.0]
        self.hs = [-94.0, -94.0, -94.0, -94.0, -94.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 3, 9, 15, 19, 0]
        self.pointsnum = 26
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
        environment.barriers.append(Barrier(-472.0, -232.0, 128.0))
        environment.barriers.append(Barrier(-273.0, -220.0, 198.0))
        environment.barriers.append(Barrier(-83.0, -229.0, 143.0))
        environment.barriers.append(Barrier(-93.0, -432.0, 212.0))
        environment.barriers.append(Barrier(-131.0, -438.0, 190.0))
        environment.barriers.append(Barrier(-154.0, -420.0, -34.0))
        environment.barriers.append(Barrier(-90.0, -416.0, 60.0))
        environment.barriers.append(Barrier(-121.0, -427.0, 8.0))
        environment.barriers.append(Barrier(-440.0, -457.0, 87.0))
        environment.checkpoints.append(Checkpoint(-33.0, -329.0, 0, -185.0))
        environment.checkpoints.append(Checkpoint(-394.0, -344.0, 0, 18.0))
        environment.checkpoints.append(Checkpoint(-106.0, -282.0, 0, 7.0))
        environment.checkpoints.append(Checkpoint(-428.0, -226.0, 0, 90.0))
        environment.checkpoints.append(Startingline(-177.0, -90.0, 0, -94.0))
        environment.powerups.append(Powerup(-124.0, -141.0, 5))
        environment.powerups.append(Powerup(-113.0, -134.0, 5))
        environment.powerups.append(Powerup(-101.0, -126.0, 5))
        environment.powerups.append(Powerup(-91.0, -118.0, 5))
        environment.powerups.append(Powerup(-31.0, -272.0, 5))
        environment.powerups.append(Powerup(-17.0, -272.0, 5))
        environment.powerups.append(Powerup(-90.0, -344.0, 5))
        environment.powerups.append(Powerup(-109.0, -344.0, 5))
        environment.powerups.append(Powerup(-232.0, -292.0, 5))
        environment.powerups.append(Powerup(-232.0, -308.0, 5))
        environment.powerups.append(Powerup(-232.0, -327.0, 5))
        environment.powerups.append(Powerup(-329.0, -422.0, 5))
        environment.powerups.append(Powerup(-410.0, -422.0, 5))
        environment.powerups.append(Powerup(-375.0, -228.0, 5))
        environment.powerups.append(Powerup(-210.0, -224.0, 5))
        environment.powerups.append(Powerup(-210.0, -238.0, 5))
        environment.powerups.append(Powerup(-210.0, -252.0, 5))
        environment.powerh.append(Powerh(-50.0, -272.0, 5))
        base.camera.setPos(Point3(-208.963, -111.954, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-208.963, -97.9537, 9))
        environment.laps = 3
        self.finishCredits = [600, 300, 150, 100, 75, 0]
        self.finishPlace = 1
