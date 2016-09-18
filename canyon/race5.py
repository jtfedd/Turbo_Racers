from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.0, 0.0431076809764, 0.0616540722549)
        environment.earth = loader.loadModel("canyon/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(5, 5, 5))
        environment.earth.setBin("background", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.121553950012, 0.121553950012, 0.121553950012, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.0556390546262, 0.0556390546262, 0.0556390546262, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.0556390546262, 0.0556390546262, 0.0556390546262, 1))
        environment.domenum = 2
        environment.playerShip = Ship(player1ship, -134.0, -425.0, 5, -49.0, environment, 10, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -140.0, -416.0, 5, -49.0, environment, 10, 2)
        self.xpoints = [-126.0, -108.0, -36.0, -5.0, 23.0, 91.0, 161.0, 261.0, 261.0, 145.0, 119.0, 144.0, 206.0, 282.0, 334.0, 361.0, 389.0, 440.0, 444.0, 439.0, 392.0, 200.0, 106.0, 50.0, -19.0, -53.0, -54.0, -26.0, 40.0, 121.0, 156.0, 154.0, -19.0, -82.0, -188.0, -240.0, -338.0, -382.0, -424.0, -445.0, -444.0, -443.0, -399.0, -355.0, -324.0, -298.0, -183.0]
        self.ypoints = [-347.0, -250.0, -165.0, -80.0, 11.0, 74.0, 101.0, 43.0, -15.0, -141.0, -196.0, -277.0, -357.0, -328.0, -222.0, 25.0, 62.0, 32.0, -112.0, -380.0, -447.0, -448.0, -400.0, -367.0, -266.0, -102.0, -54.0, 45.0, 117.0, 165.0, 196.0, 253.0, 316.0, 396.0, 418.0, 444.0, 463.0, 433.0, 380.0, 279.0, -8.0, -197.0, -250.0, -285.0, -362.0, -412.0, -403.0]
        self.xplaces = [-140.0, -145.0, -152.0, -159.0, -166.0]
        self.yplaces = [-416.0, -408.0, -399.0, -390.0, -381.0]
        self.hs = [-49.0, -49.0, -49.0, -49.0, -49.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 3, 9, 14, 18, 22, 26, 29, 36, 40, 0]
        self.pointsnum = 47
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 10, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-99.0, -397.0, 66.0))
        environment.barriers.append(Barrier(-91.0, -374.0, 66.0))
        environment.barriers.append(Barrier(-180.0, -144.0, 32.0))
        environment.barriers.append(Barrier(-159.0, -133.0, 32.0))
        environment.barriers.append(Barrier(-29.0, -78.0, 32.0))
        environment.barriers.append(Barrier(-34.0, -76.0, 119.0))
        environment.barriers.append(Barrier(57.0, -429.0, 139.0))
        environment.barriers.append(Barrier(35.0, -413.0, 139.0))
        environment.barriers.append(Barrier(220.0, -393.0, -2.0))
        environment.barriers.append(Barrier(258.0, -393.0, -2.0))
        environment.barriers.append(Barrier(236.0, -320.0, 34.0))
        environment.barriers.append(Barrier(347.0, 156.0, 34.0))
        environment.barriers.append(Barrier(403.0, 174.0, 7.0))
        environment.barriers.append(Barrier(457.0, 162.0, -44.0))
        environment.barriers.append(Barrier(294.0, -427.0, -200.0))
        environment.barriers.append(Barrier(262.0, -414.0, -200.0))
        environment.barriers.append(Barrier(231.0, -406.0, -200.0))
        environment.barriers.append(Barrier(238.0, 210.0, -268.0))
        environment.barriers.append(Barrier(211.0, 267.0, -226.0))
        environment.barriers.append(Barrier(142.0, 304.0, -190.0))
        environment.barriers.append(Barrier(3.0, 220.0, -258.0))
        environment.barriers.append(Barrier(-26.0, 274.0, -216.0))
        environment.barriers.append(Barrier(-64.0, 306.0, -234.0))
        environment.barriers.append(Barrier(-18.0, 445.0, -205.0))
        environment.barriers.append(Barrier(-395.0, 213.0, -99.0))
        environment.barriers.append(Barrier(-228.0, -371.0, -1.0))
        environment.checkpoints.append(Checkpoint(-5.0, -80.0, 0, -19.0))
        environment.checkpoints.append(Checkpoint(145.0, -141.0, 0, 134.0))
        environment.checkpoints.append(Checkpoint(334.0, -222.0, 0, 346.0))
        environment.checkpoints.append(Checkpoint(444.0, -112.0, 0, 181.0))
        environment.checkpoints.append(Checkpoint(106.0, -400.0, 0, 51.0))
        environment.checkpoints.append(Checkpoint(-54.0, -54.0, 0, -12.0))
        environment.checkpoints.append(Checkpoint(121.0, 165.0, 0, -65.0))
        environment.checkpoints.append(Checkpoint(-338.0, 463.0, 0, 95.0))
        environment.checkpoints.append(Checkpoint(-444.0, -8.0, 0, 181.0))
        environment.checkpoints.append(Startingline(-136.0, -392.0, 0, -49.0))
        environment.powerups.append(Powerup(-96.0, -275.0, 5))
        environment.powerups.append(Powerup(-108.0, -275.0, 5))
        environment.powerups.append(Powerup(-122.0, -275.0, 5))
        environment.powerups.append(Powerup(-132.0, -275.0, 5))
        environment.powerups.append(Powerup(-58.0, -272.0, 5))
        environment.powerups.append(Powerup(-43.0, -272.0, 5))
        environment.powerups.append(Powerup(-31.0, -272.0, 5))
        environment.powerups.append(Powerup(-17.0, -272.0, 5))
        environment.powerups.append(Powerup(-3.0, -272.0, 5))
        environment.powerups.append(Powerup(-67.0, -72.0, 5))
        environment.powerups.append(Powerup(0.0, -95.0, 5))
        environment.powerups.append(Powerup(210.0, 72.0, 5))
        environment.powerups.append(Powerup(215.0, 88.0, 5))
        environment.powerups.append(Powerup(225.0, 102.0, 5))
        environment.powerups.append(Powerup(206.0, -84.0, 5))
        environment.powerups.append(Powerup(275.0, -335.0, 5))
        environment.powerups.append(Powerup(275.0, -348.0, 5))
        environment.powerups.append(Powerup(366.0, -462.0, 5))
        environment.powerups.append(Powerup(366.0, -474.0, 5))
        environment.powerups.append(Powerup(366.0, -448.0, 5))
        environment.powerups.append(Powerup(442.0, -158.0, 5))
        environment.powerups.append(Powerup(358.0, -83.0, 5))
        environment.powerups.append(Powerup(345.0, -83.0, 5))
        environment.powerups.append(Powerup(144.0, -276.0, 5))
        environment.powerups.append(Powerup(168.0, -310.0, 5))
        environment.powerups.append(Powerup(197.0, -348.0, 5))
        environment.powerups.append(Powerup(51.0, -366.0, 5))
        environment.powerups.append(Powerup(39.0, -382.0, 5))
        environment.powerups.append(Powerup(29.0, -399.0, 5))
        environment.powerups.append(Powerup(-10.0, 277.0, 5))
        environment.powerups.append(Powerup(-10.0, 294.0, 5))
        environment.powerups.append(Powerup(-10.0, 314.0, 5))
        environment.powerups.append(Powerup(-10.0, 330.0, 5))
        environment.powerups.append(Powerup(-139.0, 394.0, 5))
        environment.powerups.append(Powerup(-139.0, 410.0, 5))
        environment.powerups.append(Powerup(-408.0, 405.0, 5))
        environment.powerups.append(Powerup(-427.0, 283.0, 5))
        environment.powerups.append(Powerup(-446.0, 283.0, 5))
        environment.powerups.append(Powerup(-429.0, -127.0, 5))
        environment.powerups.append(Powerup(-443.0, -127.0, 5))
        environment.powerups.append(Powerup(-458.0, -127.0, 5))
        environment.powerups.append(Powerup(-320.0, -335.0, 5))
        environment.powerups.append(Powerup(-334.0, -335.0, 5))
        environment.powerups.append(Powerup(-248.0, -413.0, 5))
        environment.powerups.append(Powerup(-231.0, -429.0, 5))
        environment.powerups.append(Powerup(-231.0, -400.0, 5))
        environment.powerups.append(Powerup(-215.0, -417.0, 5))
        environment.powerh.append(Powerh(-53.0, -74.0, 5))
        environment.powerh.append(Powerh(-18.0, -87.0, 5))
        environment.powerh.append(Powerh(92.0, 75.0, 5))
        environment.powerh.append(Powerh(92.0, 87.0, 5))
        environment.powerh.append(Powerh(91.0, 65.0, 5))
        environment.powerh.append(Powerh(73.0, 129.0, 5))
        environment.powerh.append(Powerh(70.0, 138.0, 5))
        environment.powerh.append(Powerh(70.0, 150.0, 5))
        environment.powerh.append(Powerh(185.0, -104.0, 5))
        environment.powerh.append(Powerh(275.0, -319.0, 5))
        environment.powerh.append(Powerh(428.0, -158.0, 5))
        environment.powerh.append(Powerh(455.0, -158.0, 5))
        environment.powerh.append(Powerh(329.0, -83.0, 5))
        environment.powerh.append(Powerh(-139.0, 428.0, 5))
        environment.powerh.append(Powerh(-381.0, 370.0, 5))
        environment.powerh.append(Powerh(-429.0, 51.0, 5))
        environment.powerh.append(Powerh(-442.0, 51.0, 5))
        environment.powerh.append(Powerh(-458.0, 51.0, 5))
        environment.powerh.append(Powerh(-347.0, -335.0, 5))
        environment.powerh.append(Powerh(-231.0, -413.0, 5))
        base.camera.setPos(Point3(-145.321, -434.841, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-151.321, -425.841, 9))
        environment.laps = 2
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
