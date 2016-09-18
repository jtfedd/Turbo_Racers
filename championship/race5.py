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
        environment.playerShip = Ship(player1ship, -264.0, -282.0, 5, 91.0, environment, 9, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -264.0, -292.0, 5, 91.0, environment, 9, 2)
        self.xpoints = [-359.0, -404.0, -411.0, -448.0, -476.0, -465.0, -467.0, -425.0, -358.0, -331.0, -327.0, -333.0, -324.0, -294.0, -242.0, -200.0, -137.0, -66.0, -7.0, 49.0, 108.0, 171.0, 224.0, 261.0, 263.0, 226.0, 207.0, 228.0, 263.0, 267.0, 250.0, 203.0, 153.0, 126.0, 117.0, 104.0, 129.0, 129.0, 103.0, 81.0, 48.0, 18.0, -16.0, -24.0, -85.0, -152.0, -206.0, -243.0, -209.0, -134.0, -91.0, -79.0, -49.0, -35.0, -35.0, -42.0, -83.0, -177.0, -199.0, -189.0, -239.0]
        self.ypoints = [-285.0, -321.0, -428.0, -454.0, -412.0, -306.0, -177.0, -78.0, -8.0, 71.0, 140.0, 231.0, 272.0, 313.0, 338.0, 344.0, 333.0, 304.0, 296.0, 310.0, 338.0, 349.0, 340.0, 301.0, 271.0, 184.0, 120.0, 75.0, 27.0, -31.0, -157.0, -191.0, -175.0, -91.0, -32.0, 13.0, 65.0, 115.0, 156.0, 174.0, 180.0, 176.0, 159.0, 152.0, 139.0, 145.0, 143.0, 98.0, 63.0, 4.0, -54.0, -119.0, -161.0, -203.0, -320.0, -418.0, -458.0, -457.0, -417.0, -352.0, -312.0]
        self.xplaces = [-264.0, -264.0, -264.0, -264.0, -264.0]
        self.yplaces = [-292.0, -302.0, -315.0, -326.0, -338.0]
        self.hs = [91.0, 91.0, 91.0, 91.0, 91.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 5, 10, 18, 26, 31, 37, 45, 54, 0]
        self.pointsnum = 61
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 9, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-57.0, 108.0, 138.0))
        environment.barriers.append(Barrier(-118.0, 44.0, 299.0))
        environment.barriers.append(Barrier(-123.0, -426.0, 210.0))
        environment.barriers.append(Barrier(-224.0, -452.0, 442.0))
        environment.barriers.append(Barrier(-183.0, -305.0, 533.0))
        environment.barriers.append(Barrier(-400.0, -459.0, 591.0))
        environment.barriers.append(Barrier(-264.0, 36.0, 484.0))
        environment.checkpoints.append(Checkpoint(-465.0, -306.0, 0, 1.0))
        environment.checkpoints.append(Checkpoint(-327.0, 140.0, 0, 5.0))
        environment.checkpoints.append(Checkpoint(-7.0, 296.0, 0, -91.0))
        environment.checkpoints.append(Checkpoint(207.0, 120.0, 0, -183.0))
        environment.checkpoints.append(Checkpoint(203.0, -191.0, 0, -261.0))
        environment.checkpoints.append(Checkpoint(129.0, 115.0, 0, -330.0))
        environment.checkpoints.append(Checkpoint(-152.0, 145.0, 0, -272.0))
        environment.checkpoints.append(Checkpoint(-35.0, -320.0, 0, -187.0))
        environment.checkpoints.append(Startingline(-275.0, -308.0, 0, 91.0))
        environment.powerups.append(Powerup(-359.0, -299.0, 5))
        environment.powerups.append(Powerup(-359.0, -286.0, 5))
        environment.powerups.append(Powerup(-359.0, -272.0, 5))
        environment.powerups.append(Powerup(-419.0, -375.0, 5))
        environment.powerups.append(Powerup(-405.0, -375.0, 5))
        environment.powerups.append(Powerup(-390.0, -375.0, 5))
        environment.powerups.append(Powerup(-462.0, -258.0, 5))
        environment.powerups.append(Powerup(-307.0, 89.0, 5))
        environment.powerups.append(Powerup(-324.0, 89.0, 5))
        environment.powerups.append(Powerup(262.0, 303.0, 5))
        environment.powerups.append(Powerup(267.0, -33.0, 5))
        environment.powerups.append(Powerup(117.0, -33.0, 5))
        environment.powerups.append(Powerup(140.0, 81.0, 5))
        environment.powerups.append(Powerup(165.0, 81.0, 5))
        environment.powerups.append(Powerup(194.0, 81.0, 5))
        environment.powerups.append(Powerup(221.0, 81.0, 5))
        environment.powerups.append(Powerup(-129.0, 5.0, 5))
        environment.powerups.append(Powerup(-155.0, 5.0, 5))
        environment.powerups.append(Powerup(-141.0, -445.0, 5))
        environment.powerups.append(Powerup(115.0, 80.0, 5))
        environment.powerh.append(Powerh(-395.0, -39.0, 5))
        environment.powerh.append(Powerh(-384.0, -50.0, 5))
        environment.powerh.append(Powerh(-342.0, 89.0, 5))
        environment.powerh.append(Powerh(-215.0, 345.0, 5))
        environment.powerh.append(Powerh(-11.0, 297.0, 5))
        environment.powerh.append(Powerh(-49.0, -272.0, 5))
        environment.powerh.append(Powerh(-35.0, -272.0, 5))
        environment.powerh.append(Powerh(-20.0, -272.0, 5))
        environment.powerh.append(Powerh(-141.0, -471.0, 5))
        environment.powerh.append(Powerh(-141.0, -460.0, 5))
        base.camera.setPos(Point3(-249.002, -281.738, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-249.002, -291.738, 9))
        environment.laps = 2
        self.finishCredits = [2000, 1000, 500, 333, 250, 0]
        self.finishPlace = 1
