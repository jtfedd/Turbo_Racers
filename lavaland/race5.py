from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.0561403296888, 0.0561403296888, 0.0561403296888)
        environment.earth = loader.loadModel("lavaland/world/lw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(8, 8, 8))
        environment.earth.setBin("background", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.205263122916, 0.205263122916, 0.205263122916, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.137092724442, 0.137092724442, 0.137092724442, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.137092724442, 0.137092724442, 0.137092724442, 1))
        environment.domenum = 7
        environment.playerShip = Ship(player1ship, 155.0, 385.0, 5, -502.0, environment, 9, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 165.0, 392.0, 5, -502.0, environment, 9, 2)
        self.xpoints = [224.0, 335.0, 448.0, 524.0, 590.0, 663.0, 742.0, 853.0, 894.0, 895.0, 901.0, 947.0, 956.0, 940.0, 853.0, 844.0, 839.0, 793.0, 662.0, 577.0, 489.0, 427.0, 366.0, 262.0, 187.0, 157.0, 82.0, -283.0, -335.0, -383.0, -396.0, -423.0, -403.0, -359.0, -219.0, -172.0, -145.0, -100.0, -18.0, 81.0, 116.0, 158.0]
        self.ypoints = [329.0, 298.0, 298.0, 328.0, 418.0, 537.0, 583.0, 583.0, 532.0, 401.0, 343.0, 222.0, 77.0, 7.0, -129.0, -179.0, -303.0, -380.0, -388.0, -348.0, -321.0, -319.0, -351.0, -450.0, -561.0, -598.0, -617.0, -617.0, -614.0, -529.0, -414.0, -74.0, 35.0, 89.0, 269.0, 385.0, 493.0, 557.0, 564.0, 560.0, 523.0, 435.0]
        self.xplaces = [165.0, 175.0, 183.0, 192.0, 201.0]
        self.yplaces = [392.0, 398.0, 403.0, 409.0, 417.0]
        self.hs = [-502.0, -502.0, -502.0, -502.0, -502.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 9, 15, 19, 24, 29, 33, 38, 0]
        self.pointsnum = 42
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 9, self.startPlaces, i+1))
        environment.checkpoints.append(Checkpoint(590.0, 418.0, 0, -34.0))
        environment.checkpoints.append(Checkpoint(895.0, 401.0, 0, -182.0))
        environment.checkpoints.append(Checkpoint(844.0, -179.0, 0, -182.0))
        environment.checkpoints.append(Checkpoint(577.0, -348.0, 0, -298.0))
        environment.checkpoints.append(Checkpoint(187.0, -561.0, 0, -214.0))
        environment.checkpoints.append(Checkpoint(-383.0, -529.0, 0, -332.0))
        environment.checkpoints.append(Checkpoint(-359.0, 89.0, 0, -400.0))
        environment.checkpoints.append(Checkpoint(-18.0, 564.0, 0, -450.0))
        environment.checkpoints.append(Startingline(184.0, 391.0, 0, -143.0))
        environment.powerups.append(Powerup(386.0, 297.0, 5))
        environment.powerups.append(Powerup(386.0, 314.0, 5))
        environment.powerups.append(Powerup(386.0, 330.0, 5))
        environment.powerups.append(Powerup(386.0, 282.0, 5))
        environment.powerups.append(Powerup(386.0, 265.0, 5))
        environment.powerups.append(Powerup(678.0, 530.0, 5))
        environment.powerups.append(Powerup(646.0, 549.0, 5))
        environment.powerups.append(Powerup(790.0, 582.0, 5))
        environment.powerups.append(Powerup(790.0, 600.0, 5))
        environment.powerups.append(Powerup(891.0, 468.0, 5))
        environment.powerups.append(Powerup(912.0, 323.0, 5))
        environment.powerups.append(Powerup(893.0, 307.0, 5))
        environment.powerups.append(Powerup(928.0, 136.0, 5))
        environment.powerups.append(Powerup(967.0, 113.0, 5))
        environment.powerups.append(Powerup(967.0, 133.0, 5))
        environment.powerups.append(Powerup(843.0, -259.0, 5))
        environment.powerups.append(Powerup(815.0, -343.0, 5))
        environment.powerups.append(Powerup(663.0, -399.0, 5))
        environment.powerups.append(Powerup(663.0, -374.0, 5))
        environment.powerups.append(Powerup(456.0, -327.0, 5))
        environment.powerups.append(Powerup(456.0, -317.0, 5))
        environment.powerups.append(Powerup(456.0, -304.0, 5))
        environment.powerups.append(Powerup(67.0, -600.0, 5))
        environment.powerups.append(Powerup(67.0, -615.0, 5))
        environment.powerups.append(Powerup(67.0, -630.0, 5))
        environment.powerups.append(Powerup(67.0, -644.0, 5))
        environment.powerups.append(Powerup(67.0, -660.0, 5))
        environment.powerups.append(Powerup(-279.0, -617.0, 5))
        environment.powerups.append(Powerup(-279.0, -633.0, 5))
        environment.powerups.append(Powerup(-422.0, -73.0, 5))
        environment.powerups.append(Powerup(-422.0, -57.0, 5))
        environment.powerups.append(Powerup(-204.0, 253.0, 5))
        environment.powerups.append(Powerup(-218.0, 267.0, 5))
        environment.powerups.append(Powerup(-233.0, 279.0, 5))
        environment.powerups.append(Powerup(-145.0, 449.0, 5))
        environment.powerups.append(Powerup(-162.0, 449.0, 5))
        environment.powerups.append(Powerup(-177.0, 449.0, 5))
        environment.powerh.append(Powerh(663.0, 540.0, 5))
        environment.powerh.append(Powerh(790.0, 567.0, 5))
        environment.powerh.append(Powerh(922.0, 334.0, 5))
        environment.powerh.append(Powerh(903.0, 317.0, 5))
        environment.powerh.append(Powerh(928.0, 113.0, 5))
        environment.powerh.append(Powerh(940.0, 113.0, 5))
        environment.powerh.append(Powerh(952.0, 113.0, 5))
        environment.powerh.append(Powerh(663.0, -387.0, 5))
        environment.powerh.append(Powerh(456.0, -342.0, 5))
        environment.powerh.append(Powerh(298.0, -420.0, 5))
        environment.powerh.append(Powerh(-279.0, -602.0, 5))
        environment.powerh.append(Powerh(-373.0, -277.0, 5))
        environment.powerh.append(Powerh(-395.0, -277.0, 5))
        environment.powerh.append(Powerh(-413.0, -277.0, 5))
        environment.powerh.append(Powerh(-436.0, -277.0, 5))
        environment.powerh.append(Powerh(100.0, 506.0, 5))
        environment.powerh.append(Powerh(113.0, 522.0, 5))
        environment.powerh.append(Powerh(129.0, 542.0, 5))
        base.camera.setPos(Point3(145.765, 396.82, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(155.765, 403.82, 9))
        environment.laps = 3
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
