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
        environment.domenum = 3
        environment.playerShip = Ship(player1ship, -112.0, 258.0, 5, 306.0, environment, 6, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -95.0, 233.0, 5, 306.0, environment, 6, 2)
        self.xpoints = [-61.0, -93.0, -135.0, -222.0, -287.0, -378.0, -427.0, -444.0, -441.0, -441.0, -411.0, -338.0, -316.0, -285.0, -246.0, -237.0, -272.0, -302.0, -267.0, -281.0, -293.0, -266.0, -156.0, -106.0]
        self.ypoints = [302.0, 385.0, 404.0, 400.0, 408.0, 370.0, 337.0, 279.0, -16.0, -181.0, -239.0, -297.0, -385.0, -410.0, -395.0, -277.0, -203.0, -150.0, -79.0, 9.0, 159.0, 207.0, 226.0, 263.0]
        self.xplaces = [-95.0, -110.0, -104.0, -119.0, -127.0]
        self.yplaces = [233.0, 223.0, 228.0, 253.0, 248.0]
        self.hs = [306.0, 306.0, 306.0, 306.0, 306.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 3, 7, 8, 12, 19, 0]
        self.pointsnum = 24
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
        environment.barriers.append(Barrier(-5.0, 270.0, 90.0))
        environment.barriers.append(Barrier(-2.0, 312.0, 90.0))
        environment.barriers.append(Barrier(-51.0, 432.0, 167.0))
        environment.barriers.append(Barrier(-396.0, 214.0, 264.0))
        environment.barriers.append(Barrier(-336.0, 207.0, 445.0))
        environment.barriers.append(Barrier(-283.0, -444.0, 368.0))
        environment.barriers.append(Barrier(-250.0, -431.0, 388.0))
        environment.barriers.append(Barrier(-226.0, -412.0, 419.0))
        environment.barriers.append(Barrier(-211.0, -384.0, 433.0))
        environment.checkpoints.append(Checkpoint(-222.0, 400.0, 0, 90.0))
        environment.checkpoints.append(Checkpoint(-444.0, 279.0, 0, 178.0))
        environment.checkpoints.append(Checkpoint(-441.0, -16.0, 0, 178.0))
        environment.checkpoints.append(Checkpoint(-316.0, -385.0, 0, 202.0))
        environment.checkpoints.append(Checkpoint(-281.0, 9.0, 0, 365.0))
        environment.checkpoints.append(Startingline(-87.0, 254.0, 0, -57.0))
        environment.powerups.append(Powerup(-75.0, 331.0, 5))
        environment.powerups.append(Powerup(-62.0, 331.0, 5))
        environment.powerups.append(Powerup(-49.0, 331.0, 5))
        environment.powerups.append(Powerup(-165.0, 403.0, 5))
        environment.powerups.append(Powerup(-165.0, 393.0, 5))
        environment.powerups.append(Powerup(-165.0, 416.0, 5))
        environment.powerups.append(Powerup(-338.0, 387.0, 5))
        environment.powerups.append(Powerup(-438.0, 74.0, 5))
        environment.powerups.append(Powerup(-426.0, 74.0, 5))
        environment.powerups.append(Powerup(-450.0, 74.0, 5))
        environment.powerups.append(Powerup(-441.0, -148.0, 5))
        environment.powerups.append(Powerup(-454.0, -148.0, 5))
        environment.powerups.append(Powerup(-231.0, -319.0, 5))
        environment.powerups.append(Powerup(-276.0, -96.0, 5))
        environment.powerups.append(Powerup(-264.0, -96.0, 5))
        environment.powerups.append(Powerup(-291.0, -96.0, 5))
        environment.powerups.append(Powerup(-262.0, 208.0, 5))
        environment.powerups.append(Powerup(-262.0, 195.0, 5))
        environment.powerh.append(Powerh(-335.0, 371.0, 5))
        environment.powerh.append(Powerh(-343.0, 401.0, 5))
        environment.powerh.append(Powerh(-430.0, 198.0, 5))
        environment.powerh.append(Powerh(-448.0, 198.0, 5))
        environment.powerh.append(Powerh(-426.0, -148.0, 5))
        environment.powerh.append(Powerh(-330.0, -345.0, 5))
        environment.powerh.append(Powerh(-315.0, -340.0, 5))
        environment.powerh.append(Powerh(-344.0, -350.0, 5))
        environment.powerh.append(Powerh(-295.0, 53.0, 5))
        environment.powerh.append(Powerh(-280.0, 53.0, 5))
        environment.powerh.append(Powerh(-305.0, 53.0, 5))
        environment.powerh.append(Powerh(-262.0, 224.0, 5))
        base.camera.setPos(Point3(-124.135, 249.183, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-107.135, 224.183, 9))
        environment.laps = 3
        self.finishCredits = [400, 200, 100, 66, 50, 0]
        self.finishPlace = 2
