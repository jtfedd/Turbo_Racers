from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.600298464298, 0.864521503448, 1.0)
        environment.earth = loader.loadModel("arctic/world/aw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.5, 3.5, 3.5))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 3
        environment.playerShip = Ship(player1ship, -10.0, 294.0, 5, 113.0, environment, 8, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -13.0, 304.0, 5, 113.0, environment, 8, 2)
        self.xpoints = [-78.0, -106.0, -86.0, -26.0, 100.0, 184.0, 221.0, 269.0, 286.0, 277.0, 241.0, 144.0, 68.0, 41.0, 46.0, 51.0, 114.0, 270.0, 327.0, 352.0, 354.0, 301.0, 292.0, 302.0, 316.0, 312.0, 274.0, 256.0, 216.0, 158.0, 5.0]
        self.ypoints = [289.0, 257.0, 225.0, 229.0, 223.0, 204.0, 121.0, 67.0, 21.0, -61.0, -90.0, -110.0, -147.0, -183.0, -282.0, -316.0, -340.0, -320.0, -265.0, -193.0, -153.0, -94.0, -63.0, 18.0, 97.0, 195.0, 265.0, 328.0, 350.0, 348.0, 316.0]
        self.xplaces = [-13.0, -17.0, -22.0, -26.0, -30.0]
        self.yplaces = [304.0, 312.0, 323.0, 332.0, 341.0]
        self.hs = [113.0, 113.0, 113.0, 113.0, 113.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 3, 5, 10, 14, 19, 24, 29, 0]
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
        environment.barriers.append(Barrier(-162.0, 208.0, 659.0))
        environment.barriers.append(Barrier(-150.0, 194.0, 676.0))
        environment.barriers.append(Barrier(-134.0, 186.0, 702.0))
        environment.barriers.append(Barrier(147.0, 190.0, 704.0))
        environment.barriers.append(Barrier(228.0, 218.0, 687.0))
        environment.barriers.append(Barrier(251.0, 201.0, 678.0))
        environment.barriers.append(Barrier(265.0, 147.0, 600.0))
        environment.barriers.append(Barrier(265.0, 102.0, 661.0))
        environment.barriers.append(Barrier(279.0, -95.0, 561.0))
        environment.barriers.append(Barrier(303.0, -120.0, 495.0))
        environment.barriers.append(Barrier(284.0, -99.0, 481.0))
        environment.barriers.append(Barrier(23.0, -186.0, 628.0))
        environment.barriers.append(Barrier(23.0, -210.0, 628.0))
        environment.barriers.append(Barrier(23.0, -232.0, 628.0))
        environment.barriers.append(Barrier(273.0, 202.0, 470.0))
        environment.barriers.append(Barrier(260.0, 231.0, 473.0))
        environment.barriers.append(Barrier(246.0, 261.0, 468.0))
        environment.barriers.append(Barrier(223.0, -304.0, 7.0))
        environment.checkpoints.append(Checkpoint(-26.0, 229.0, 0, 279.0))
        environment.checkpoints.append(Checkpoint(184.0, 204.0, 0, 234.0))
        environment.checkpoints.append(Checkpoint(241.0, -90.0, 0, 110.0))
        environment.checkpoints.append(Checkpoint(46.0, -282.0, 0, 176.0))
        environment.checkpoints.append(Checkpoint(352.0, -193.0, 0, 348.0))
        environment.checkpoints.append(Checkpoint(316.0, 97.0, 0, 348.0))
        environment.checkpoints.append(Checkpoint(158.0, 348.0, 0, 458.0))
        environment.checkpoints.append(Startingline(-29.0, 316.0, 0, 113.0))
        environment.powerups.append(Powerup(-91.0, 272.0, 5))
        environment.powerups.append(Powerup(-86.0, 265.0, 5))
        environment.powerups.append(Powerup(-96.0, 279.0, 5))
        environment.powerups.append(Powerup(91.0, 225.0, 5))
        environment.powerups.append(Powerup(91.0, 240.0, 5))
        environment.powerups.append(Powerup(91.0, 254.0, 5))
        environment.powerups.append(Powerup(235.0, 123.0, 5))
        environment.powerups.append(Powerup(220.0, 123.0, 5))
        environment.powerups.append(Powerup(210.0, 123.0, 5))
        environment.powerups.append(Powerup(282.0, -9.0, 5))
        environment.powerups.append(Powerup(279.0, -29.0, 5))
        environment.powerups.append(Powerup(296.0, -29.0, 5))
        environment.powerups.append(Powerup(299.0, -12.0, 5))
        environment.powerups.append(Powerup(183.0, -104.0, 5))
        environment.powerups.append(Powerup(82.0, -129.0, 5))
        environment.powerups.append(Powerup(40.0, -232.0, 5))
        environment.powerups.append(Powerup(59.0, -232.0, 5))
        environment.powerups.append(Powerup(326.0, -265.0, 5))
        environment.powerups.append(Powerup(307.0, -103.0, 5))
        environment.powerups.append(Powerup(294.0, 159.0, 5))
        environment.powerups.append(Powerup(306.0, 159.0, 5))
        environment.powerups.append(Powerup(320.0, 159.0, 5))
        environment.powerups.append(Powerup(332.0, 159.0, 5))
        environment.powerups.append(Powerup(242.0, 345.0, 5))
        environment.powerups.append(Powerup(79.0, 330.0, 5))
        environment.powerups.append(Powerup(79.0, 345.0, 5))
        environment.powerups.append(Powerup(79.0, 313.0, 5))
        environment.powerh.append(Powerh(-72.0, 226.0, 5))
        environment.powerh.append(Powerh(-71.0, 212.0, 5))
        environment.powerh.append(Powerh(289.0, -20.0, 5))
        environment.powerh.append(Powerh(86.0, -140.0, 5))
        environment.powerh.append(Powerh(113.0, -342.0, 5))
        environment.powerh.append(Powerh(323.0, -91.0, 5))
        environment.powerh.append(Powerh(270.0, 275.0, 5))
        environment.powerh.append(Powerh(257.0, 275.0, 5))
        environment.powerh.append(Powerh(283.0, 275.0, 5))
        base.camera.setPos(Point3(3.80757, 299.861, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(0.807573, 309.861, 9))
        environment.laps = 4
        self.finishCredits = [550, 275, 137, 91, 68, 0]
        self.finishPlace = 1
