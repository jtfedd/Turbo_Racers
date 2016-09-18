from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.638653337955, 0.864521503448, 1.0)
        environment.earth = loader.loadModel("city/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(5.35364, 5.35364, 5.35364))
        environment.earth.setBin("background", 1)
        environment.earth.find('**/trees').setBin('transparent', 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 3
        environment.playerShip = Ship(player1ship, -343.0, -162.0, 5, 0.0, environment, 5, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -359.0, -162.0, 5, 0.0, environment, 5, 2)
        self.xpoints = [-351.0, -353.0, -417.0, -454.0, -481.0, -486.0, -486.0, -409.0, -359.0, -352.0, -352.0]
        self.ypoints = [-56.0, 11.0, 47.0, 32.0, -28.0, -149.0, -441.0, -485.0, -436.0, -380.0, -197.0]
        self.xplaces = [-359.0, -378.0, -378.0, -361.0, -343.0]
        self.yplaces = [-162.0, -162.0, -178.0, -178.0, -178.0]
        self.hs = [0.0, 0.0, 0.0, 0.0, 0.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 2, 5, 6, 9, 0]
        self.pointsnum = 11
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
        environment.barriers.append(Barrier(-326.0, -214.0, 482.0))
        environment.barriers.append(Barrier(-326.0, -53.0, 482.0))
        environment.barriers.append(Barrier(-351.0, 68.0, 540.0))
        environment.barriers.append(Barrier(-510.0, 46.0, 623.0))
        environment.barriers.append(Barrier(-486.0, -506.0, 720.0))
        environment.barriers.append(Barrier(-332.0, -493.0, 809.0))
        environment.barriers.append(Barrier(-324.0, -353.0, 848.0))
        environment.checkpoints.append(Checkpoint(-417.0, 47.0, 0, 93.0))
        environment.checkpoints.append(Checkpoint(-486.0, -149.0, 0, 182.0))
        environment.checkpoints.append(Checkpoint(-486.0, -441.0, 0, 182.0))
        environment.checkpoints.append(Checkpoint(-352.0, -380.0, 0, 359.0))
        environment.checkpoints.append(Startingline(-369.0, -149.0, 0, 0.0))
        environment.powerups.append(Powerup(-340.0, -56.0, 5))
        environment.powerups.append(Powerup(-351.0, -56.0, 5))
        environment.powerups.append(Powerup(-364.0, -56.0, 5))
        environment.powerups.append(Powerup(-472.0, -51.0, 5))
        environment.powerups.append(Powerup(-484.0, -51.0, 5))
        environment.powerups.append(Powerup(-471.0, -319.0, 5))
        environment.powerups.append(Powerup(-485.0, -319.0, 5))
        environment.powerups.append(Powerup(-496.0, -319.0, 5))
        environment.powerups.append(Powerup(-364.0, -305.0, 5))
        environment.powerups.append(Powerup(-351.0, -305.0, 5))
        environment.powerups.append(Powerup(-338.0, -305.0, 5))
        environment.powerh.append(Powerh(-496.0, -51.0, 5))
        environment.powerh.append(Powerh(-410.0, -472.0, 5))
        environment.powerh.append(Powerh(-410.0, -487.0, 5))
        environment.powerh.append(Powerh(-409.0, -500.0, 5))
        base.camera.setPos(Point3(-342.604, -176.608, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-359.31, -176.608, 9))
        environment.laps = 3
        self.finishCredits = [500, 250, 125, 83, 62, 0]
        self.finishPlace = 1
