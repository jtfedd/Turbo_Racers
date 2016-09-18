from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.717794537544, 1.0, 1.0)
        environment.earth = loader.loadModel("lavaland/world/lw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(8, 8, 8))
        environment.earth.setBin("background", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.300000011921, 0.300000011921, 0.300000011921, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.directionalLight.setSpecularColor(Vec4(1.0, 1.0, 1.0, 1))
        environment.domenum = 3
        environment.playerShip = Ship(player1ship, 575.0, 393.0, 5, 167.0, environment, 8, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 556.0, 396.0, 5, 167.0, environment, 8, 2)
        self.xpoints = [543.0, 554.0, 618.0, 706.0, 787.0, 842.0, 1050.0, 1203.0, 1279.0, 1288.0, 1281.0, 1206.0, 1108.0, 1014.0, 927.0, 842.0, 842.0, 876.0, 959.0, 959.0, 988.0, 1124.0, 1231.0, 1286.0, 1401.0, 1418.0, 1388.0, 1318.0, 1271.0, 1047.0, 751.0, 571.0]
        self.ypoints = [185.0, -123.0, -365.0, -437.0, -594.0, -635.0, -674.0, -674.0, -629.0, -589.0, -466.0, -425.0, -425.0, -425.0, -369.0, -287.0, -137.0, -78.0, 29.0, 175.0, 228.0, 228.0, 228.0, 251.0, 365.0, 431.0, 526.0, 609.0, 618.0, 622.0, 575.0, 438.0]
        self.xplaces = [556.0, 538.0, 542.0, 559.0, 578.0]
        self.yplaces = [396.0, 400.0, 415.0, 409.0, 404.0]
        self.hs = [167.0, 167.0, 167.0, 167.0, 167.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 1, 4, 9, 12, 17, 21, 27, 0]
        self.pointsnum = 32
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
        environment.checkpoints.append(Checkpoint(554.0, -123.0, 0, -182.0))
        environment.checkpoints.append(Checkpoint(787.0, -594.0, 0, -150.0))
        environment.checkpoints.append(Checkpoint(1288.0, -589.0, 0, -2.0))
        environment.checkpoints.append(Checkpoint(1108.0, -425.0, 0, 89.0))
        environment.checkpoints.append(Checkpoint(876.0, -78.0, 0, -46.0))
        environment.checkpoints.append(Checkpoint(1124.0, 228.0, 0, -90.0))
        environment.checkpoints.append(Checkpoint(1318.0, 609.0, 0, 46.0))
        environment.checkpoints.append(Startingline(549.0, 375.0, 0, -195.0))
        environment.powerups.append(Powerup(575.0, 175.0, 5))
        environment.powerups.append(Powerup(562.0, 175.0, 5))
        environment.powerups.append(Powerup(544.0, 175.0, 5))
        environment.powerups.append(Powerup(528.0, 175.0, 5))
        environment.powerups.append(Powerup(514.0, 175.0, 5))
        environment.powerups.append(Powerup(625.0, -340.0, 5))
        environment.powerups.append(Powerup(613.0, -358.0, 5))
        environment.powerups.append(Powerup(603.0, -374.0, 5))
        environment.powerups.append(Powerup(853.0, -619.0, 5))
        environment.powerups.append(Powerup(853.0, -633.0, 5))
        environment.powerups.append(Powerup(853.0, -648.0, 5))
        environment.powerups.append(Powerup(1119.0, -658.0, 5))
        environment.powerups.append(Powerup(1119.0, -672.0, 5))
        environment.powerups.append(Powerup(1119.0, -686.0, 5))
        environment.powerups.append(Powerup(1205.0, -444.0, 5))
        environment.powerups.append(Powerup(1205.0, -425.0, 5))
        environment.powerups.append(Powerup(1205.0, -408.0, 5))
        environment.powerups.append(Powerup(926.0, -369.0, 5))
        environment.powerups.append(Powerup(918.0, -384.0, 5))
        environment.powerups.append(Powerup(843.0, -226.0, 5))
        environment.powerups.append(Powerup(843.0, -208.0, 5))
        environment.powerups.append(Powerup(956.0, 103.0, 5))
        environment.powerups.append(Powerup(972.0, 103.0, 5))
        environment.powerups.append(Powerup(1188.0, 227.0, 5))
        environment.powerups.append(Powerup(1188.0, 216.0, 5))
        environment.powerups.append(Powerup(1188.0, 240.0, 5))
        environment.powerups.append(Powerup(1402.0, 432.0, 5))
        environment.powerups.append(Powerup(1418.0, 432.0, 5))
        environment.powerups.append(Powerup(1433.0, 432.0, 5))
        environment.powerups.append(Powerup(1116.0, 605.0, 5))
        environment.powerups.append(Powerup(1116.0, 621.0, 5))
        environment.powerups.append(Powerup(638.0, 517.0, 5))
        environment.powerups.append(Powerup(654.0, 510.0, 5))
        environment.powerups.append(Powerup(671.0, 504.0, 5))
        environment.powerh.append(Powerh(633.0, -320.0, 5))
        environment.powerh.append(Powerh(591.0, -389.0, 5))
        environment.powerh.append(Powerh(1256.0, -540.0, 5))
        environment.powerh.append(Powerh(1278.0, -542.0, 5))
        environment.powerh.append(Powerh(1295.0, -543.0, 5))
        environment.powerh.append(Powerh(938.0, -354.0, 5))
        environment.powerh.append(Powerh(907.0, -399.0, 5))
        environment.powerh.append(Powerh(940.0, 103.0, 5))
        environment.powerh.append(Powerh(1071.0, 228.0, 5))
        environment.powerh.append(Powerh(1071.0, 237.0, 5))
        environment.powerh.append(Powerh(1071.0, 217.0, 5))
        environment.powerh.append(Powerh(1450.0, 432.0, 5))
        environment.powerh.append(Powerh(1116.0, 637.0, 5))
        environment.powerh.append(Powerh(627.0, 523.0, 5))
        environment.powerh.append(Powerh(685.0, 498.0, 5))
        base.camera.setPos(Point3(578.374, 407.616, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(559.374, 410.616, 9))
        environment.laps = 3
        self.finishCredits = [750, 375, 187, 125, 93, 0]
        self.finishPlace = 1
