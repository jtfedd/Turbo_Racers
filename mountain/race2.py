from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.647773385048, 0.94395917654, 1.0)
        environment.earth = loader.loadModel("mountain/world/mw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.50387, 3.50387, 3.50387))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.408672422171, 0.408672422171, 0.408672422171, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.607926607132, 0.607926607132, 0.607926607132, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.607926607132, 0.607926607132, 0.607926607132, 1))
        environment.domenum = 5
        environment.playerShip = Ship(player1ship, -478.0, -233.0, 5, -92.0, environment, 8, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -478.0, -243.0, 5, -92.0, environment, 8, 2)
        self.xpoints = [-418.0, -388.0, -382.0, -396.0, -462.0, -497.0, -491.0, -444.0, -383.0, -336.0, -218.0, -116.0, -21.0, 74.0, 128.0, 142.0, 121.0, 87.0, 15.0, -84.0, -166.0, -241.0, -302.0, -379.0, -445.0, -532.0, -608.0, -644.0, -648.0, -616.0, -554.0]
        self.ypoints = [-231.0, -172.0, -105.0, -58.0, 27.0, 89.0, 135.0, 212.0, 290.0, 309.0, 309.0, 296.0, 269.0, 173.0, 108.0, 49.0, 1.0, -21.0, -3.0, 83.0, 117.0, 139.0, 132.0, 115.0, 89.0, 43.0, -16.0, -74.0, -133.0, -191.0, -237.0]
        self.xplaces = [-478.0, -478.0, -478.0, -478.0, -478.0]
        self.yplaces = [-243.0, -255.0, -267.0, -278.0, -289.0]
        self.hs = [-92.0, -92.0, -92.0, -92.0, -92.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 7, 11, 14, 19, 23, 26, 0]
        self.pointsnum = 31
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 8, self.startPlaces, i+1))
        environment.barriers.append(Barrier(21.0, -53.0, 158.0))
        environment.barriers.append(Barrier(182.0, 6.0, 232.0))
        environment.barriers.append(Barrier(121.0, 268.0, 293.0))
        environment.barriers.append(Barrier(-212.0, 86.0, 475.0))
        environment.barriers.append(Barrier(-194.0, 176.0, 595.0))
        environment.barriers.append(Barrier(-524.0, 143.0, 786.0))
        environment.barriers.append(Barrier(-500.0, 185.0, 763.0))
        environment.barriers.append(Barrier(-422.0, 314.0, 740.0))
        environment.checkpoints.append(Checkpoint(-462.0, 27.0, 0, 37.0))
        environment.checkpoints.append(Checkpoint(-444.0, 212.0, 0, -36.0))
        environment.checkpoints.append(Checkpoint(-116.0, 296.0, 0, -105.0))
        environment.checkpoints.append(Checkpoint(128.0, 108.0, 0, -150.0))
        environment.checkpoints.append(Checkpoint(-84.0, 83.0, 0, -308.0))
        environment.checkpoints.append(Checkpoint(-379.0, 115.0, 0, -248.0))
        environment.checkpoints.append(Checkpoint(-608.0, -16.0, 0, -226.0))
        environment.checkpoints.append(Startingline(-464.0, -261.0, 0, -92.0))
        environment.powerups.append(Powerup(-381.0, -129.0, 5))
        environment.powerups.append(Powerup(-365.0, -129.0, 5))
        environment.powerups.append(Powerup(-341.0, -129.0, 5))
        environment.powerups.append(Powerup(-489.0, 70.0, 5))
        environment.powerups.append(Powerup(-463.0, 163.0, 5))
        environment.powerups.append(Powerup(-485.0, 173.0, 5))
        environment.powerups.append(Powerup(45.0, 200.0, 5))
        environment.powerups.append(Powerup(-35.0, 43.0, 5))
        environment.powerups.append(Powerup(-27.0, 51.0, 5))
        environment.powerups.append(Powerup(-45.0, 33.0, 5))
        environment.powerups.append(Powerup(-646.0, -131.0, 5))
        environment.powerups.append(Powerup(-658.0, -131.0, 5))
        environment.powerh.append(Powerh(-472.0, 169.0, 5))
        environment.powerh.append(Powerh(58.0, 210.0, 5))
        environment.powerh.append(Powerh(32.0, 191.0, 5))
        environment.powerh.append(Powerh(-633.0, -131.0, 5))
        base.camera.setPos(Point3(-492.991, -232.477, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-492.991, -242.477, 9))
        environment.laps = 2
        self.finishCredits = [750, 375, 187, 125, 93, 0]
        self.finishPlace = 1
