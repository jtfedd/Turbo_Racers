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
        environment.domenum = 5
        environment.playerShip = Ship(player1ship, -145.0, 78.0, 5, 178.0, environment, 4, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -172.0, 78.0, 5, 178.0, environment, 4, 2)
        self.xpoints = [-175.0, -140.0, -92.0, -37.0, 61.0, 132.0, 194.0, 296.0, 339.0, 341.0, 359.0, 343.0, 228.0, 137.0, 40.0, -42.0, -112.0, -149.0]
        self.ypoints = [-81.0, -150.0, -209.0, -275.0, -378.0, -412.0, -413.0, -331.0, -216.0, -104.0, 98.0, 158.0, 212.0, 254.0, 236.0, 205.0, 187.0, 120.0]
        self.xplaces = [-172.0, -172.0, -144.0, -144.0, -173.0]
        self.yplaces = [78.0, 91.0, 91.0, 103.0, 103.0]
        self.hs = [178.0, 178.0, 178.0, 178.0, 178.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 3, 9, 13, 0]
        self.pointsnum = 18
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 4, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-176.0, 240.0, 253.0))
        environment.barriers.append(Barrier(-182.0, 213.0, 261.0))
        environment.barriers.append(Barrier(-182.0, 194.0, 261.0))
        environment.barriers.append(Barrier(-163.0, -256.0, 342.0))
        environment.barriers.append(Barrier(-132.0, -266.0, 342.0))
        environment.barriers.append(Barrier(-108.0, -272.0, 342.0))
        environment.barriers.append(Barrier(198.0, -469.0, 391.0))
        environment.barriers.append(Barrier(224.0, -454.0, 391.0))
        environment.barriers.append(Barrier(247.0, -435.0, 405.0))
        environment.barriers.append(Barrier(271.0, -416.0, 405.0))
        environment.barriers.append(Barrier(206.0, -369.0, 425.0))
        environment.checkpoints.append(Checkpoint(-37.0, -275.0, 0, 223.0))
        environment.checkpoints.append(Checkpoint(341.0, -104.0, 0, 354.0))
        environment.checkpoints.append(Checkpoint(137.0, 254.0, 0, 433.0))
        environment.checkpoints.append(Startingline(-161.0, 67.0, 0, 178.0))
        environment.powerups.append(Powerup(-155.0, -6.0, 5))
        environment.powerups.append(Powerup(-167.0, -6.0, 5))
        environment.powerups.append(Powerup(-181.0, -6.0, 5))
        environment.powerups.append(Powerup(-172.0, -184.0, 5))
        environment.powerups.append(Powerup(-158.0, -184.0, 5))
        environment.powerups.append(Powerup(-185.0, -184.0, 5))
        environment.powerups.append(Powerup(12.0, -329.0, 5))
        environment.powerups.append(Powerup(24.0, -321.0, 5))
        environment.powerups.append(Powerup(2.0, -339.0, 5))
        environment.powerups.append(Powerup(180.0, -412.0, 5))
        environment.powerups.append(Powerup(180.0, -428.0, 5))
        environment.powerups.append(Powerup(319.0, -242.0, 5))
        environment.powerups.append(Powerup(329.0, -242.0, 5))
        environment.powerups.append(Powerup(342.0, -242.0, 5))
        environment.powerups.append(Powerup(348.0, -11.0, 5))
        environment.powerups.append(Powerup(334.0, -11.0, 5))
        environment.powerups.append(Powerup(362.0, -11.0, 5))
        environment.powerups.append(Powerup(343.0, 158.0, 5))
        environment.powerups.append(Powerup(403.0, 177.0, 5))
        environment.powerups.append(Powerup(470.0, 179.0, 5))
        environment.powerups.append(Powerup(233.0, 228.0, 5))
        environment.powerups.append(Powerup(226.0, 213.0, 5))
        environment.powerups.append(Powerup(5.0, 222.0, 5))
        environment.powerups.append(Powerup(-145.0, 139.0, 5))
        environment.powerups.append(Powerup(-161.0, 139.0, 5))
        environment.powerh.append(Powerh(-131.0, -163.0, 5))
        environment.powerh.append(Powerh(-120.0, -148.0, 5))
        environment.powerh.append(Powerh(-121.0, -130.0, 5))
        environment.powerh.append(Powerh(180.0, -397.0, 5))
        environment.powerh.append(Powerh(274.0, -242.0, 5))
        environment.powerh.append(Powerh(258.0, -242.0, 5))
        environment.powerh.append(Powerh(223.0, 199.0, 5))
        base.camera.setPos(Point3(-144.477, 92.9909, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-171.477, 92.9909, 9))
        environment.laps = 3
        self.finishCredits = [600, 300, 150, 100, 75, 0]
        self.finishPlace = 1
