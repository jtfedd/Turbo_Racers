from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.0, 0.072448477149, 0.135776743293)
        environment.earth = loader.loadModel("mountain/world/mw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.50387, 3.50387, 3.50387))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.164912283421, 0.164912283421, 0.164912283421, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.105263121426, 0.105263121426, 0.105263121426, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.105263121426, 0.105263121426, 0.105263121426, 1))
        environment.domenum = 3
        environment.playerShip = Ship(player1ship, 121.0, -201.0, 5, 105.0, environment, 7, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 119.0, -193.0, 5, 105.0, environment, 7, 2)
        self.xpoints = [-50.0, -100.0, -167.0, -209.0, -295.0, -532.0, -570.0, -618.0, -643.0, -630.0, -583.0, -518.0, -470.0, -414.0, -292.0, -228.0, -126.0, -97.0, -64.0, -5.0, 100.0, 190.0, 236.0, 259.0, 268.0, 268.0, 242.0, 177.0]
        self.ypoints = [-231.0, -247.0, -252.0, -252.0, -244.0, -244.0, -238.0, -186.0, -96.0, -53.0, -3.0, 47.0, 82.0, 107.0, 139.0, 156.0, 230.0, 274.0, 291.0, 284.0, 282.0, 280.0, 254.0, 198.0, 51.0, -68.0, -108.0, -151.0]
        self.xplaces = [119.0, 116.0, 114.0, 111.0, 109.0]
        self.yplaces = [-193.0, -185.0, -176.0, -167.0, -157.0]
        self.hs = [105.0, 105.0, 105.0, 105.0, 105.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 2, 5, 11, 16, 21, 24, 0]
        self.pointsnum = 28
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
        environment.barriers.append(Barrier(-365.0, -193.0, -162.0))
        environment.barriers.append(Barrier(-617.0, 50.0, 20.0))
        environment.barriers.append(Barrier(-494.0, 103.0, -5.0))
        environment.barriers.append(Barrier(-463.0, 49.0, 77.0))
        environment.barriers.append(Barrier(-188.0, 120.0, 34.0))
        environment.barriers.append(Barrier(-142.0, 153.0, 56.0))
        environment.barriers.append(Barrier(-96.0, 294.0, 21.0))
        environment.barriers.append(Barrier(240.0, -3.0, -77.0))
        environment.barriers.append(Barrier(289.0, -209.0, -147.0))
        environment.barriers.append(Barrier(266.0, -223.0, -158.0))
        environment.checkpoints.append(Checkpoint(-167.0, -252.0, 0, 88.0))
        environment.checkpoints.append(Checkpoint(-532.0, -244.0, 0, 88.0))
        environment.checkpoints.append(Checkpoint(-518.0, 47.0, 0, -51.0))
        environment.checkpoints.append(Checkpoint(-126.0, 230.0, 0, -51.0))
        environment.checkpoints.append(Checkpoint(190.0, 280.0, 0, -94.0))
        environment.checkpoints.append(Checkpoint(268.0, 51.0, 0, -181.0))
        environment.checkpoints.append(Startingline(100.0, -179.0, 0, 105.0))
        environment.powerups.append(Powerup(6.0, -233.0, 5))
        environment.powerups.append(Powerup(-1.0, -198.0, 5))
        environment.powerups.append(Powerup(-367.0, -218.0, 5))
        environment.powerups.append(Powerup(-366.0, -233.0, 5))
        environment.powerups.append(Powerup(-368.0, -248.0, 5))
        environment.powerups.append(Powerup(-645.0, -117.0, 5))
        environment.powerups.append(Powerup(-547.0, 28.0, 5))
        environment.powerups.append(Powerup(-555.0, 35.0, 5))
        environment.powerups.append(Powerup(-536.0, 20.0, 5))
        environment.powerups.append(Powerup(-186.0, 189.0, 5))
        environment.powerups.append(Powerup(-172.0, 178.0, 5))
        environment.powerups.append(Powerup(263.0, 149.0, 5))
        environment.powerups.append(Powerup(216.0, -129.0, 5))
        environment.powerups.append(Powerup(226.0, -143.0, 5))
        environment.powerups.append(Powerup(235.0, -155.0, 5))
        environment.powerh.append(Powerh(2.0, -215.0, 5))
        environment.powerh.append(Powerh(-5.0, -183.0, 5))
        environment.powerh.append(Powerh(-657.0, -115.0, 5))
        environment.powerh.append(Powerh(-157.0, 167.0, 5))
        environment.powerh.append(Powerh(102.0, 271.0, 5))
        environment.powerh.append(Powerh(102.0, 282.0, 5))
        environment.powerh.append(Powerh(275.0, 149.0, 5))
        base.camera.setPos(Point3(135.489, -197.118, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(133.489, -189.118, 9))
        environment.laps = 3
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
