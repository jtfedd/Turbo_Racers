from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.0383548997343, 0.0809716284275, 0.144300118089)
        environment.earth = loader.loadModel("championship/world/cw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.8418, 3.8418, 3.8418))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.276560783386, 0.276560783386, 0.276560783386, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.422544240952, 0.422544240952, 0.422544240952, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.422544240952, 0.422544240952, 0.422544240952, 1))
        environment.domenum = 7
        environment.playerShip = Ship(player1ship, -50.0, -286.0, 5, 0.0, environment, 5, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -39.0, -286.0, 5, 0.0, environment, 5, 2)
        self.xpoints = [-34.0, -40.0, -62.0, -113.0, -151.0, -196.0, -232.0, -240.0, -190.0, -161.0, -99.0, -62.0, -79.0, -187.0, -226.0, -263.0, -278.0, -270.0, -252.0, -164.0, -116.0, -100.0, -96.0, -67.0, -38.0]
        self.ypoints = [-209.0, -110.0, -68.0, -20.0, 27.0, 57.0, 76.0, 123.0, 146.0, 146.0, 145.0, 118.0, 68.0, -3.0, -47.0, -96.0, -132.0, -209.0, -237.0, -245.0, -275.0, -339.0, -412.0, -439.0, -413.0]
        self.xplaces = [-39.0, -25.0, -16.0, -35.0, -50.0]
        self.yplaces = [-286.0, -286.0, -273.0, -273.0, -273.0]
        self.hs = [0.0, 0.0, 0.0, 0.0, 0.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 3, 9, 14, 21, 0]
        self.pointsnum = 25
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
        environment.barriers.append(Barrier(-116.0, -435.0, -45.0))
        environment.barriers.append(Barrier(-86.0, -461.0, -10.0))
        environment.barriers.append(Barrier(-83.0, -228.0, -38.0))
        environment.barriers.append(Barrier(-284.0, -246.0, -38.0))
        environment.barriers.append(Barrier(-260.0, -256.0, -2.0))
        environment.barriers.append(Barrier(-34.0, 145.0, -43.0))
        environment.checkpoints.append(Checkpoint(-113.0, -20.0, 0, 42.0))
        environment.checkpoints.append(Checkpoint(-161.0, 146.0, 0, -87.0))
        environment.checkpoints.append(Checkpoint(-226.0, -47.0, 0, -204.0))
        environment.checkpoints.append(Checkpoint(-100.0, -339.0, 0, -177.0))
        environment.checkpoints.append(Startingline(-30.0, -257.0, 0, 0.0))
        environment.powerups.append(Powerup(-157.0, 62.0, 5))
        environment.powerups.append(Powerup(-158.0, 44.0, 5))
        environment.powerups.append(Powerup(-158.0, 28.0, 5))
        environment.powerups.append(Powerup(-158.0, 9.0, 5))
        environment.powerups.append(Powerup(-158.0, -6.0, 5))
        environment.powerups.append(Powerup(-193.0, -241.0, 5))
        environment.powerups.append(Powerup(-103.0, -314.0, 5))
        environment.powerups.append(Powerup(-44.0, -314.0, 5))
        environment.powerups.append(Powerup(-23.0, -314.0, 5))
        environment.powerups.append(Powerup(-70.0, -439.0, 5))
        environment.powerups.append(Powerup(-76.0, -79.0, 5))
        environment.powerups.append(Powerup(-65.0, -72.0, 5))
        environment.powerups.append(Powerup(-52.0, -66.0, 5))
        environment.powerh.append(Powerh(-73.0, 76.0, 5))
        environment.powerh.append(Powerh(-240.0, 90.0, 5))
        environment.powerh.append(Powerh(-147.0, 148.0, 5))
        environment.powerh.append(Powerh(-193.0, -226.0, 5))
        base.camera.setPos(Point3(-50.4087, -300.622, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-38.7552, -300.622, 9))
        environment.laps = 3
        self.finishCredits = [850, 425, 212, 141, 106, 0]
        self.finishPlace = 1
