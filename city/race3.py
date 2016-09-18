from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.0, 0.0, 0.0675899758935)
        environment.earth = loader.loadModel("city/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(5.35364, 5.35364, 5.35364))
        environment.earth.setBin("background", 1)
        environment.earth.find("**/trees").setBin("transparent", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.140187487006, 0.140187487006, 0.140187487006, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.162582710385, 0.162582710385, 0.162582710385, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.162582710385, 0.162582710385, 0.162582710385, 1))
        environment.domenum = 7
        environment.playerShip = Ship(player1ship, 312.0, -200.0, 5, -153.0, environment, 7, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 321.0, -196.0, 5, -153.0, environment, 7, 2)
        self.xpoints = [418.0, 467.0, 485.0, 483.0, 452.0, 33.0, -154.0, -203.0, -220.0, -252.0, -313.0, -344.0, -344.0, -308.0, -262.0, -212.0, -186.0, -186.0, -210.0, -217.0, -212.0, -179.0, 19.0, 183.0, 208.0, 218.0, 225.0, 346.0]
        self.ypoints = [-263.0, -297.0, -397.0, -448.0, -478.0, -486.0, -479.0, -432.0, -385.0, -357.0, -346.0, -320.0, -246.0, -220.0, -220.0, -215.0, -192.0, -82.0, -20.0, 108.0, 275.0, 309.0, 317.0, 313.0, 296.0, 163.0, 1.0, -173.0]
        self.xplaces = [321.0, 330.0, 330.0, 339.0, 349.0]
        self.yplaces = [-196.0, -192.0, -192.0, -188.0, -182.0]
        self.hs = [-153.0, -153.0, -153.0, -153.0, -153.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 2, 5, 14, 19, 22, 25, 0]
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
        environment.barriers.append(Barrier(412.0, -303.0, -388.0))
        environment.barriers.append(Barrier(-50.0, -330.0, -546.0))
        environment.barriers.append(Barrier(-363.0, -351.0, -608.0))
        environment.barriers.append(Barrier(-352.0, -190.0, -723.0))
        environment.barriers.append(Barrier(-170.0, -45.0, -596.0))
        environment.barriers.append(Barrier(-235.0, -51.0, -634.0))
        environment.barriers.append(Barrier(-219.0, 340.0, -699.0))
        environment.barriers.append(Barrier(247.0, 318.0, -815.0))
        environment.barriers.append(Barrier(198.0, -63.0, -777.0))
        environment.checkpoints.append(Checkpoint(485.0, -397.0, 0, -179.0))
        environment.checkpoints.append(Checkpoint(33.0, -486.0, 0, -269.0))
        environment.checkpoints.append(Checkpoint(-262.0, -220.0, 0, -454.0))
        environment.checkpoints.append(Checkpoint(-217.0, 108.0, 0, -359.0))
        environment.checkpoints.append(Checkpoint(19.0, 317.0, 0, -448.0))
        environment.checkpoints.append(Checkpoint(218.0, 163.0, 0, -542.0))
        environment.checkpoints.append(Startingline(342.0, -199.0, 0, -153.0))
        environment.powerups.append(Powerup(205.0, 34.0, 5))
        environment.powerups.append(Powerup(218.0, 34.0, 5))
        environment.powerups.append(Powerup(230.0, 34.0, 5))
        environment.powerups.append(Powerup(451.0, -275.0, 5))
        environment.powerups.append(Powerup(450.0, -286.0, 5))
        environment.powerups.append(Powerup(450.0, -299.0, 5))
        environment.powerups.append(Powerup(402.0, -474.0, 5))
        environment.powerups.append(Powerup(402.0, -485.0, 5))
        environment.powerups.append(Powerup(402.0, -498.0, 5))
        environment.powerups.append(Powerup(140.0, -474.0, 5))
        environment.powerups.append(Powerup(140.0, -486.0, 5))
        environment.powerups.append(Powerup(140.0, -499.0, 5))
        environment.powerups.append(Powerup(-351.0, -289.0, 5))
        environment.powerups.append(Powerup(-361.0, -289.0, 5))
        environment.powerups.append(Powerup(-186.0, -132.0, 5))
        environment.powerups.append(Powerup(-197.0, -132.0, 5))
        environment.powerups.append(Powerup(-174.0, -132.0, 5))
        environment.powerups.append(Powerup(-209.0, 230.0, 5))
        environment.powerups.append(Powerup(-218.0, 230.0, 5))
        environment.powerups.append(Powerup(-227.0, 230.0, 5))
        environment.powerups.append(Powerup(111.0, 330.0, 5))
        environment.powerups.append(Powerup(111.0, 317.0, 5))
        environment.powerups.append(Powerup(111.0, 305.0, 5))
        environment.powerh.append(Powerh(-145.0, -477.0, 5))
        environment.powerh.append(Powerh(-145.0, -486.0, 5))
        environment.powerh.append(Powerh(-145.0, -498.0, 5))
        environment.powerh.append(Powerh(-343.0, -289.0, 5))
        base.camera.setPos(Point3(305.375, -186.302, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(314.384, -182.314, 9))
        environment.laps = 3
        self.finishCredits = [600, 300, 150, 100, 75, 0]
        self.finishPlace = 1
