from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.80183249712, 0.926734805107, 1.0)
        environment.earth = loader.loadModel("city/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(5.35364, 5.35364, 5.35364))
        environment.earth.setBin("background", 1)
        environment.earth.find("**/trees").setBin("transparent", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 3
        environment.playerShip = Ship(player1ship, 212.0, 476.0, 5, -89.0, environment, 11, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 212.0, 492.0, 5, -89.0, environment, 11, 2)
        self.xpoints = [346.0, 383.0, 384.0, 376.0, 236.0, 163.0, 119.0, 117.0, 79.0, -135.0, -314.0, -351.0, -351.0, -312.0, -248.0, -214.0, -190.0, -108.0, 94.0, 445.0, 485.0, 484.0, 454.0, 439.0, 231.0, 218.0, 219.0, 182.0, -135.0, -219.0, -302.0, -449.0, -484.0, -485.0, -484.0, -447.0, -299.0, 185.0]
        self.ypoints = [479.0, 446.0, 233.0, 6.0, -289.0, -318.0, -288.0, -88.0, -55.0, -50.0, -50.0, -83.0, -307.0, -352.0, -352.0, -390.0, -447.0, -478.0, -485.0, -485.0, -452.0, -320.0, -286.0, -283.0, -6.0, 153.0, 287.0, 316.0, 318.0, 324.0, 345.0, 352.0, 385.0, 423.0, 446.0, 483.0, 484.0, 482.0]
        self.xplaces = [212.0, 212.0, 203.0, 203.0, 203.0]
        self.yplaces = [492.0, 508.0, 501.0, 491.0, 480.0]
        self.hs = [-89.0, -89.0, -89.0, -89.0, -89.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 2, 5, 9, 12, 18, 23, 25, 28, 33, 36, 0]
        self.pointsnum = 38
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 11, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-351.0, -373.0, -0.0))
        environment.barriers.append(Barrier(-48.0, -335.0, -51.0))
        environment.barriers.append(Barrier(-366.0, -49.0, -101.0))
        environment.barriers.append(Barrier(-217.0, 293.0, -195.0))
        environment.barriers.append(Barrier(-217.0, 358.0, -195.0))
        environment.barriers.append(Barrier(220.0, 334.0, -195.0))
        environment.barriers.append(Barrier(84.0, -219.0, -296.0))
        environment.barriers.append(Barrier(200.0, -10.0, -296.0))
        environment.barriers.append(Barrier(251.0, 1.0, -212.0))
        environment.barriers.append(Barrier(-510.0, 356.0, -277.0))
        environment.checkpoints.append(Checkpoint(384.0, 233.0, 0, -180.0))
        environment.checkpoints.append(Checkpoint(163.0, -318.0, 0, -268.0))
        environment.checkpoints.append(Checkpoint(-135.0, -50.0, 0, -268.0))
        environment.checkpoints.append(Checkpoint(-351.0, -307.0, 0, -188.0))
        environment.checkpoints.append(Checkpoint(94.0, -485.0, 0, -98.0))
        environment.checkpoints.append(Checkpoint(439.0, -283.0, 0, 80.0))
        environment.checkpoints.append(Checkpoint(218.0, 153.0, 0, 2.0))
        environment.checkpoints.append(Checkpoint(-135.0, 318.0, 0, 92.0))
        environment.checkpoints.append(Checkpoint(-485.0, 423.0, 0, -1.0))
        environment.checkpoints.append(Checkpoint(-299.0, 484.0, 0, -90.0))
        environment.checkpoints.append(Startingline(223.0, 482.0, 0, -89.0))
        environment.powerups.append(Powerup(373.0, 385.0, 5))
        environment.powerups.append(Powerup(385.0, 385.0, 5))
        environment.powerups.append(Powerup(397.0, 385.0, 5))
        environment.powerups.append(Powerup(227.0, -170.0, 5))
        environment.powerups.append(Powerup(290.0, -170.0, 5))
        environment.powerups.append(Powerup(366.0, -170.0, 5))
        environment.powerups.append(Powerup(428.0, -170.0, 5))
        environment.powerups.append(Powerup(131.0, -128.0, 5))
        environment.powerups.append(Powerup(117.0, -128.0, 5))
        environment.powerups.append(Powerup(103.0, -128.0, 5))
        environment.powerups.append(Powerup(-339.0, -219.0, 5))
        environment.powerups.append(Powerup(-366.0, -219.0, 5))
        environment.powerups.append(Powerup(-350.0, -219.0, 5))
        environment.powerups.append(Powerup(-97.0, -478.0, 5))
        environment.powerups.append(Powerup(-97.0, -494.0, 5))
        environment.powerups.append(Powerup(96.0, 328.0, 5))
        environment.powerups.append(Powerup(96.0, 317.0, 5))
        environment.powerups.append(Powerup(96.0, 307.0, 5))
        environment.powerups.append(Powerup(-374.0, 496.0, 5))
        environment.powerups.append(Powerup(-374.0, 484.0, 5))
        environment.powerups.append(Powerup(-374.0, 472.0, 5))
        environment.powerups.append(Powerup(-149.0, 485.0, 5))
        environment.powerups.append(Powerup(-86.0, 485.0, 5))
        environment.powerups.append(Powerup(4.0, 485.0, 5))
        environment.powerups.append(Powerup(102.0, 485.0, 5))
        environment.powerups.append(Powerup(143.0, 470.0, 5))
        environment.powerups.append(Powerup(52.0, 470.0, 5))
        environment.powerups.append(Powerup(-43.0, 470.0, 5))
        environment.powerups.append(Powerup(-118.0, 470.0, 5))
        environment.powerups.append(Powerup(-119.0, 498.0, 5))
        environment.powerups.append(Powerup(-40.0, 498.0, 5))
        environment.powerups.append(Powerup(50.0, 498.0, 5))
        environment.powerups.append(Powerup(142.0, 498.0, 5))
        environment.powerh.append(Powerh(379.0, 86.0, 5))
        environment.powerh.append(Powerh(392.0, 86.0, 5))
        environment.powerh.append(Powerh(263.0, -170.0, 5))
        environment.powerh.append(Powerh(330.0, -170.0, 5))
        environment.powerh.append(Powerh(398.0, -170.0, 5))
        environment.powerh.append(Powerh(305.0, -477.0, 5))
        environment.powerh.append(Powerh(305.0, -493.0, 5))
        base.camera.setPos(Point3(197.455, 475.384, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(197.455, 491.896, 9))
        environment.laps = 2
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
