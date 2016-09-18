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
        environment.playerShip = Ship(player1ship, -14.0, -304.0, 5, 176.0, environment, 5, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, -29.0, -304.0, 5, 176.0, environment, 5, 2)
        self.xpoints = [-44.0, -88.0, -143.0, -179.0, -297.0, -362.0, -402.0, -369.0, -330.0, -346.0, -452.0, -486.0, -482.0, -463.0, -465.0, -450.0, -367.0, -252.0, -149.0, -48.0, -35.0, -37.0]
        self.ypoints = [-421.0, -446.0, -395.0, -326.0, -297.0, -287.0, -314.0, -372.0, -420.0, -460.0, -451.0, -410.0, -349.0, -262.0, -183.0, -150.0, -109.0, -85.0, -93.0, -147.0, -215.0, -299.0]
        self.xplaces = [-29.0, -49.0, -49.0, -30.0, -15.0]
        self.yplaces = [-304.0, -304.0, -290.0, -290.0, -290.0]
        self.hs = [176.0, 176.0, 176.0, 176.0, 176.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 8, 13, 17, 0]
        self.pointsnum = 22
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
        environment.barriers.append(Barrier(-106.0, -404.0, 143.0))
        environment.barriers.append(Barrier(-162.0, -455.0, 95.0))
        environment.barriers.append(Barrier(-425.0, -384.0, -20.0))
        environment.barriers.append(Barrier(-398.0, -398.0, -22.0))
        environment.barriers.append(Barrier(-302.0, -456.0, -123.0))
        environment.barriers.append(Barrier(-407.0, -432.0, -175.0))
        environment.barriers.append(Barrier(-19.0, -158.0, -94.0))
        environment.checkpoints.append(Checkpoint(-297.0, -297.0, 0, 81.0))
        environment.checkpoints.append(Checkpoint(-330.0, -420.0, 0, 181.0))
        environment.checkpoints.append(Checkpoint(-463.0, -262.0, 0, 3.0))
        environment.checkpoints.append(Checkpoint(-252.0, -85.0, 0, -83.0))
        environment.checkpoints.append(Startingline(-26.0, -318.0, 0, 176.0))
        environment.powerups.append(Powerup(-49.0, -377.0, 5))
        environment.powerups.append(Powerup(-35.0, -377.0, 5))
        environment.powerups.append(Powerup(-22.0, -377.0, 5))
        environment.powerups.append(Powerup(-156.0, -362.0, 5))
        environment.powerups.append(Powerup(-236.0, -327.0, 5))
        environment.powerups.append(Powerup(-236.0, -311.0, 5))
        environment.powerups.append(Powerup(-236.0, -296.0, 5))
        environment.powerups.append(Powerup(-384.0, -366.0, 5))
        environment.powerups.append(Powerup(-410.0, -456.0, 5))
        environment.powerups.append(Powerup(-189.0, -105.0, 5))
        environment.powerups.append(Powerup(-189.0, -85.0, 5))
        environment.powerups.append(Powerup(-189.0, -60.0, 5))
        environment.powerh.append(Powerh(-167.0, -370.0, 5))
        environment.powerh.append(Powerh(-144.0, -357.0, 5))
        environment.powerh.append(Powerh(-471.0, -299.0, 5))
        environment.powerh.append(Powerh(-459.0, -299.0, 5))
        base.camera.setPos(Point3(-13.1624, -289.504, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(-27.5346, -289.504, 9))
        environment.laps = 4
        self.finishCredits = [800, 400, 200, 133, 100, 0]
        self.finishPlace = 1
