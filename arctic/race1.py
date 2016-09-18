from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.742857158184, 0.917293250561, 1.0)
        environment.earth = loader.loadModel("arctic/world/aw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.5, 3.5, 3.5))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.playerShip = Ship(player1ship, -145.0, -284.0, 5, -85.0, environment, 6, 1)
        environment.domenum = 3
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -147.0, -273.0, 5, -85.0, environment, 6, 2)
        self.xpoints = [-3.0, 92.0, 210.0, 268.0, 286.0, 300.0, 310.0, 272.0, 259.0, 234.0, -28.0, -92.0, -129.0, -167.0, -197.0, -232.0, -277.0, -300.0, -322.0, -282.0, -166.0]
        self.ypoints = [-213.0, -228.0, -200.0, -159.0, -56.0, 47.0, 197.0, 252.0, 324.0, 352.0, 298.0, 275.0, 214.0, 187.0, 164.0, 119.0, -8.0, -73.0, -126.0, -209.0, -270.0]
        self.xplaces = [-147.0, -149.0, -152.0, -156.0, -154.0]
        self.yplaces = [-273.0, -262.0, -249.0, -263.0, -273.0]
        self.hs = [-85.0, -85.0, -85.0, -85.0, -85.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 8, 11, 15, 18, 0]
        self.pointsnum = 21
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
        environment.barriers.append(Barrier(39.0, -180.0, -23.0))
        environment.barriers.append(Barrier(210.0, -252.0, 17.0))
        environment.barriers.append(Barrier(236.0, -239.0, 38.0))
        environment.barriers.append(Barrier(323.0, -121.0, 85.0))
        environment.checkpoints.append(Checkpoint(268.0, -159.0, 0, -41.0))
        environment.checkpoints.append(Checkpoint(272.0, 252.0, 0, 48.0))
        environment.checkpoints.append(Checkpoint(-28.0, 298.0, 0, 105.0))
        environment.checkpoints.append(Checkpoint(-167.0, 187.0, 0, 105.0))
        environment.checkpoints.append(Checkpoint(-277.0, -8.0, 0, 163.0))
        environment.checkpoints.append(Startingline(-132.0, -259.0, 0, -76.0))
        environment.powerups.append(Powerup(-2.0, -198.0, 5))
        environment.powerups.append(Powerup(-2.0, -214.0, 5))
        environment.powerups.append(Powerup(-2.0, -229.0, 5))
        environment.powerups.append(Powerup(288.0, -27.0, 5))
        environment.powerups.append(Powerup(309.0, 94.0, 5))
        environment.powerups.append(Powerup(325.0, 94.0, 5))
        environment.powerups.append(Powerup(232.0, 351.0, 5))
        environment.powerups.append(Powerup(192.0, 211.0, 5))
        environment.powerups.append(Powerup(27.0, 280.0, 5))
        environment.powerups.append(Powerup(-94.0, 274.0, 5))
        environment.powerups.append(Powerup(-287.0, 23.0, 5))
        environment.powerups.append(Powerup(-271.0, 23.0, 5))
        environment.powerups.append(Powerup(-321.0, -126.0, 5))
        environment.powerups.append(Powerup(-283.0, -210.0, 5))
        environment.powerups.append(Powerup(-267.0, -202.0, 5))
        environment.powerups.append(Powerup(-253.0, -197.0, 5))
        environment.powerh.append(Powerh(227.0, -192.0, 5))
        environment.powerh.append(Powerh(293.0, 94.0, 5))
        environment.powerh.append(Powerh(167.0, 269.0, 5))
        environment.powerh.append(Powerh(47.0, 280.0, 5))
        environment.powerh.append(Powerh(-257.0, 23.0, 5))
        environment.powerh.append(Powerh(-275.0, -94.0, 5))
        base.camera.setPos(Point3(-159.943, -285.307, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-161.943, -274.307, 9))
        environment.laps = 3
        self.finishCredits = [500, 250, 125, 83, 62, 0]
        self.finishPlace = 2
