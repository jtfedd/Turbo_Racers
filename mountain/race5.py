from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.0313658155501, 0.0, 0.0995523706079)
        environment.earth = loader.loadModel("mountain/world/mw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(3.50387, 3.50387, 3.50387))
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.0916258618236, 0.0916258618236, 0.0916258618236, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.164713516831, 0.164713516831, 0.164713516831, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.164713516831, 0.164713516831, 0.164713516831, 1))
        environment.domenum = 2
        environment.playerShip = Ship(player1ship, 254.0, 179.0, 5, 0.0, environment, 7, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 265.0, 179.0, 5, 0.0, environment, 7, 2)
        self.xpoints = [242.0, 205.0, -12.0, -64.0, -90.0, -125.0, -132.0, -123.0, -20.0, -2.0, -7.0, -46.0, -108.0, -148.0, -226.0, -308.0, -357.0, -392.0, -437.0, -484.0, -492.0, -471.0, -406.0, -309.0, -242.0, -227.0, -234.0, -203.0, -135.0, -72.0, 104.0, 235.0, 264.0, 267.0]
        self.ypoints = [255.0, 280.0, 281.0, 291.0, 285.0, 239.0, 196.0, 153.0, 28.0, -7.0, -106.0, -190.0, -241.0, -251.0, -251.0, -241.0, -142.0, -56.0, 4.0, 26.0, 58.0, 81.0, 109.0, 135.0, 127.0, 42.0, -7.0, -63.0, -92.0, -98.0, -20.0, 50.0, 78.0, 174.0]
        self.xplaces = [265.0, 278.0, 292.0, 304.0, 279.0]
        self.yplaces = [179.0, 179.0, 179.0, 179.0, 168.0]
        self.hs = [0.0, 0.0, 0.0, 0.0, 0.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 5, 8, 15, 17, 29, 32, 0]
        self.pointsnum = 34
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 7, self.startPlaces, i+1))
        environment.barriers.append(Barrier(-103.0, 298.0, 252.0))
        environment.barriers.append(Barrier(-182.0, 212.0, 270.0))
        environment.barriers.append(Barrier(-178.0, 175.0, 270.0))
        environment.barriers.append(Barrier(-173.0, 137.0, 270.0))
        environment.barriers.append(Barrier(-164.0, 100.0, 270.0))
        environment.barriers.append(Barrier(-159.0, 69.0, 270.0))
        environment.barriers.append(Barrier(47.0, 0.0, 270.0))
        environment.barriers.append(Barrier(-84.0, -144.0, 388.0))
        environment.barriers.append(Barrier(48.0, -194.0, 288.0))
        environment.barriers.append(Barrier(9.0, -274.0, 199.0))
        environment.barriers.append(Barrier(-458.0, -289.0, 109.0))
        environment.barriers.append(Barrier(-458.0, -248.0, 73.0))
        environment.barriers.append(Barrier(-526.0, 13.0, 104.0))
        environment.barriers.append(Barrier(-530.0, 46.0, 98.0))
        environment.barriers.append(Barrier(-496.0, 105.0, 9.0))
        environment.barriers.append(Barrier(148.0, 76.0, 9.0))
        environment.checkpoints.append(Checkpoint(-125.0, 239.0, 0, 143.0))
        environment.checkpoints.append(Checkpoint(-20.0, 28.0, 0, -138.0))
        environment.checkpoints.append(Checkpoint(-308.0, -241.0, 0, -269.0))
        environment.checkpoints.append(Checkpoint(-392.0, -56.0, 0, 14.0))
        environment.checkpoints.append(Checkpoint(-203.0, -63.0, 0, -493.0))
        environment.checkpoints.append(Checkpoint(104.0, -20.0, 0, -418.0))
        environment.checkpoints.append(Startingline(280.0, 194.0, 0, 0.0))
        environment.powerups.append(Powerup(213.0, 43.0, 5))
        environment.powerups.append(Powerup(213.0, 20.0, 5))
        environment.powerups.append(Powerup(213.0, -3.0, 5))
        environment.powerups.append(Powerup(83.0, 278.0, 5))
        environment.powerups.append(Powerup(83.0, 262.0, 5))
        environment.powerups.append(Powerup(83.0, 246.0, 5))
        environment.powerups.append(Powerup(-88.0, 101.0, 5))
        environment.powerups.append(Powerup(-208.0, 87.0, 5))
        environment.powerups.append(Powerup(-10.0, -81.0, 5))
        environment.powerups.append(Powerup(22.0, -65.0, 5))
        environment.powerups.append(Powerup(-3.0, -34.0, 5))
        environment.powerups.append(Powerup(-386.0, -108.0, 5))
        environment.powerups.append(Powerup(-357.0, -108.0, 5))
        environment.powerh.append(Powerh(-99.0, 87.0, 5))
        environment.powerh.append(Powerh(-227.0, 87.0, 5))
        environment.powerh.append(Powerh(-28.0, -167.0, 5))
        environment.powerh.append(Powerh(-8.0, -178.0, 5))
        environment.powerh.append(Powerh(-372.0, -108.0, 5))
        base.camera.setPos(Point3(254, 164, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(265, 164, 9))
        environment.laps = 3
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
