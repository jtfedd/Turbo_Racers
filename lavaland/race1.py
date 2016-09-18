from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.40000000596, 0.40000000596, 0.40000000596)
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
        environment.domenum = 1
        environment.playerShip = Ship(player1ship, -421.0, -276.0, 5, -361.0, environment, 5, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -402.0, -276.0, 5, -361.0, environment, 5, 2)
        self.xpoints = [-423.0, -413.0, -333.0, -206.0, -171.0, -162.0, -132.0, -22.0, 69.0, 128.0, 128.0, 115.0, 66.0, -193.0, -436.0, -516.0, -591.0, -623.0, -633.0, -643.0, -673.0, -679.0, -641.0, -596.0, -478.0, -440.0, -402.0]
        self.ypoints = [-69.0, 24.0, 106.0, 255.0, 354.0, 452.0, 545.0, 582.0, 582.0, 517.0, 439.0, 360.0, 325.0, 169.0, 104.0, 104.0, 84.0, 9.0, -300.0, -353.0, -429.0, -583.0, -677.0, -686.0, -686.0, -660.0, -323.0]
        self.xplaces = [-402.0, -383.0, -383.0, -403.0, -422.0]
        self.yplaces = [-276.0, -276.0, -293.0, -293.0, -293.0]
        self.hs = [-361.0, -361.0, -361.0, -361.0, -361.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 5, 10, 15, 23, 0]
        self.pointsnum = 27
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
        environment.checkpoints.append(Checkpoint(-162.0, 452.0, 0, 0.0))
        environment.checkpoints.append(Checkpoint(128.0, 439.0, 0, -181.0))
        environment.checkpoints.append(Checkpoint(-516.0, 104.0, 0, -275.0))
        environment.checkpoints.append(Checkpoint(-596.0, -686.0, 0, -446.0))
        environment.checkpoints.append(Startingline(-400.0, -255.0, 0, 0.0))
        environment.powerups.append(Powerup(-444.0, -65.0, 5))
        environment.powerups.append(Powerup(-435.0, -65.0, 5))
        environment.powerups.append(Powerup(-422.0, -65.0, 5))
        environment.powerups.append(Powerup(-411.0, -65.0, 5))
        environment.powerups.append(Powerup(-399.0, -65.0, 5))
        environment.powerups.append(Powerup(-278.0, 196.0, 5))
        environment.powerups.append(Powerup(-278.0, 177.0, 5))
        environment.powerups.append(Powerup(-278.0, 151.0, 5))
        environment.powerups.append(Powerup(-278.0, 131.0, 5))
        environment.powerups.append(Powerup(-278.0, 108.0, 5))
        environment.powerups.append(Powerup(-278.0, 91.0, 5))
        environment.powerups.append(Powerup(-278.0, 72.0, 5))
        environment.powerups.append(Powerup(-15.0, 559.0, 5))
        environment.powerups.append(Powerup(-15.0, 569.0, 5))
        environment.powerups.append(Powerup(-15.0, 612.0, 5))
        environment.powerups.append(Powerup(-15.0, 624.0, 5))
        environment.powerups.append(Powerup(64.0, 351.0, 5))
        environment.powerups.append(Powerup(64.0, 340.0, 5))
        environment.powerups.append(Powerup(64.0, 323.0, 5))
        environment.powerups.append(Powerup(64.0, 313.0, 5))
        environment.powerups.append(Powerup(64.0, 302.0, 5))
        environment.powerups.append(Powerup(-612.0, -214.0, 5))
        environment.powerups.append(Powerup(-624.0, -214.0, 5))
        environment.powerups.append(Powerup(-637.0, -214.0, 5))
        environment.powerups.append(Powerup(-651.0, -214.0, 5))
        environment.powerups.append(Powerup(-662.0, -508.0, 5))
        environment.powerups.append(Powerup(-678.0, -508.0, 5))
        environment.powerups.append(Powerup(-689.0, -508.0, 5))
        environment.powerups.append(Powerup(-425.0, -555.0, 5))
        environment.powerups.append(Powerup(-409.0, -555.0, 5))
        environment.powerups.append(Powerup(-396.0, -555.0, 5))
        environment.powerh.append(Powerh(-125.0, 358.0, 5))
        environment.powerh.append(Powerh(-146.0, 358.0, 5))
        environment.powerh.append(Powerh(-168.0, 358.0, 5))
        environment.powerh.append(Powerh(-192.0, 358.0, 5))
        environment.powerh.append(Powerh(-15.0, 584.0, 5))
        environment.powerh.append(Powerh(-15.0, 598.0, 5))
        environment.powerh.append(Powerh(-477.0, 59.0, 5))
        environment.powerh.append(Powerh(-477.0, 78.0, 5))
        environment.powerh.append(Powerh(-477.0, 99.0, 5))
        environment.powerh.append(Powerh(-477.0, 118.0, 5))
        environment.powerh.append(Powerh(-477.0, 134.0, 5))
        environment.powerh.append(Powerh(-475.0, -555.0, 5))
        environment.powerh.append(Powerh(-456.0, -555.0, 5))
        environment.powerh.append(Powerh(-441.0, -555.0, 5))
        base.camera.setPos(Point3(-421.262, -290.998, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-402.262, -290.998, 9))
        environment.laps = 3
        self.finishCredits = [700, 350, 175, 116, 87, 0]
        self.finishPlace = 2
