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
        environment.playerShip = Ship(player1ship, 289.0, -369.0, 5, 176.0, environment, 8, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 263.0, -355.0, 5, 176.0, environment, 8, 2)
        self.xpoints = [283.0, 347.0, 425.0, 444.0, 443.0, 443.0, 414.0, 392.0, 371.0, 299.0, 205.0, 147.0, 102.0, 6.0, -136.0, -237.0, -285.0, -371.0, -420.0, -429.0, -398.0, -347.0, -317.0, -295.0, -272.0, -295.0, -259.0, -231.0, -217.0, -160.0, -129.0, -65.0, -12.0, 21.0, 69.0, 165.0, 267.0, 266.0, 222.0, 141.0, 124.0, 165.0, 195.0, 233.0]
        self.ypoints = [-416.0, -457.0, -410.0, -326.0, -18.0, 66.0, 143.0, 215.0, 272.0, 340.0, 384.0, 392.0, 414.0, 393.0, 406.0, 402.0, 407.0, 370.0, 340.0, 292.0, 231.0, 214.0, 183.0, 42.0, -51.0, -127.0, -215.0, -329.0, -381.0, -410.0, -280.0, -205.0, -88.0, 8.0, 61.0, 106.0, 41.0, -15.0, -67.0, -141.0, -232.0, -311.0, -349.0, -364.0]
        self.xplaces = [263.0, 238.0, 241.0, 291.0, 268.0]
        self.yplaces = [-355.0, -365.0, -344.0, -348.0, -337.0]
        self.hs = [176.0, 176.0, 176.0, 176.0, 176.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 9, 14, 20, 27, 32, 38, 0]
        self.pointsnum = 44
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
        environment.barriers.append(Barrier(210.0, -385.0, 13.0))
        environment.barriers.append(Barrier(207.0, -412.0, -63.0))
        environment.barriers.append(Barrier(225.0, -438.0, -46.0))
        environment.barriers.append(Barrier(249.0, -457.0, -46.0))
        environment.barriers.append(Barrier(271.0, -472.0, -23.0))
        environment.barriers.append(Barrier(-469.0, 241.0, -23.0))
        environment.barriers.append(Barrier(-442.0, 229.0, -23.0))
        environment.barriers.append(Barrier(-281.0, 223.0, -61.0))
        environment.barriers.append(Barrier(-274.0, 194.0, -94.0))
        environment.barriers.append(Barrier(-249.0, -395.0, -60.0))
        environment.barriers.append(Barrier(-232.0, -413.0, -41.0))
        environment.barriers.append(Barrier(-211.0, -425.0, -27.0))
        environment.barriers.append(Barrier(-94.0, -401.0, 75.0))
        environment.barriers.append(Barrier(-175.0, -111.0, 2.0))
        environment.barriers.append(Barrier(-56.0, -60.0, -22.0))
        environment.barriers.append(Barrier(226.0, -325.0, 52.0))
        environment.barriers.append(Barrier(242.0, -313.0, 22.0))
        environment.barriers.append(Barrier(287.0, -313.0, -25.0))
        environment.barriers.append(Barrier(304.0, -328.0, -63.0))
        environment.checkpoints.append(Checkpoint(443.0, -18.0, 0, 0.0))
        environment.checkpoints.append(Checkpoint(299.0, 340.0, 0, 45.0))
        environment.checkpoints.append(Checkpoint(-136.0, 406.0, 0, 85.0))
        environment.checkpoints.append(Checkpoint(-398.0, 231.0, 0, 231.0))
        environment.checkpoints.append(Checkpoint(-231.0, -329.0, 0, 183.0))
        environment.checkpoints.append(Checkpoint(-12.0, -88.0, 0, 334.0))
        environment.checkpoints.append(Checkpoint(222.0, -67.0, 0, 482.0))
        environment.checkpoints.append(Startingline(262.0, -384.0, 0, 176.0))
        environment.powerups.append(Powerup(347.0, -458.0, 5))
        environment.powerups.append(Powerup(347.0, -442.0, 5))
        environment.powerups.append(Powerup(347.0, -471.0, 5))
        environment.powerups.append(Powerup(455.0, -157.0, 5))
        environment.powerups.append(Powerup(430.0, -157.0, 5))
        environment.powerups.append(Powerup(467.0, 185.0, 5))
        environment.powerups.append(Powerup(405.0, 178.0, 5))
        environment.powerups.append(Powerup(346.0, 167.0, 5))
        environment.powerups.append(Powerup(371.0, 272.0, 5))
        environment.powerups.append(Powerup(188.0, 327.0, 5))
        environment.powerups.append(Powerup(188.0, 383.0, 5))
        environment.powerups.append(Powerup(89.0, 347.0, 5))
        environment.powerups.append(Powerup(89.0, 415.0, 5))
        environment.powerups.append(Powerup(89.0, 430.0, 5))
        environment.powerups.append(Powerup(-289.0, 130.0, 5))
        environment.powerups.append(Powerup(-304.0, 130.0, 5))
        environment.powerups.append(Powerup(-318.0, 130.0, 5))
        environment.powerups.append(Powerup(-237.0, -291.0, 5))
        environment.powerups.append(Powerup(-224.0, -291.0, 5))
        environment.powerups.append(Powerup(-150.0, -308.0, 5))
        environment.powerups.append(Powerup(-131.0, -308.0, 5))
        environment.powerups.append(Powerup(90.0, 70.0, 5))
        environment.powerups.append(Powerup(85.0, 82.0, 5))
        environment.powerups.append(Powerup(173.0, -111.0, 5))
        environment.powerups.append(Powerup(167.0, -98.0, 5))
        environment.powerups.append(Powerup(182.0, -121.0, 5))
        environment.powerups.append(Powerup(163.0, -309.0, 5))
        environment.powerh.append(Powerh(469.0, -157.0, 5))
        environment.powerh.append(Powerh(441.0, -157.0, 5))
        environment.powerh.append(Powerh(188.0, 398.0, 5))
        environment.powerh.append(Powerh(89.0, 444.0, 5))
        environment.powerh.append(Powerh(-79.0, 385.0, 5))
        environment.powerh.append(Powerh(-79.0, 401.0, 5))
        environment.powerh.append(Powerh(-79.0, 415.0, 5))
        environment.powerh.append(Powerh(-281.0, -9.0, 5))
        environment.powerh.append(Powerh(-292.0, -9.0, 5))
        environment.powerh.append(Powerh(-269.0, -9.0, 5))
        environment.powerh.append(Powerh(-249.0, -291.0, 5))
        environment.powerh.append(Powerh(-111.0, -308.0, 5))
        environment.powerh.append(Powerh(210.0, 65.0, 5))
        environment.powerh.append(Powerh(217.0, 76.0, 5))
        environment.powerh.append(Powerh(225.0, 90.0, 5))
        environment.powerh.append(Powerh(233.0, 104.0, 5))
        environment.powerh.append(Powerh(174.0, -301.0, 5))
        environment.powerh.append(Powerh(154.0, -316.0, 5))
        base.camera.setPos(Point3(290.046, -354.037, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(264.046, -340.037, 9))
        environment.laps = 2
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
