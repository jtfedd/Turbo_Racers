from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from Environment import *
class Race(DirectObject):
    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):
        base.setBackgroundColor(0.113283209503, 0.0591478534043, 0.0591478534043)
        environment.earth = loader.loadModel("lavaland/world/lw")
        environment.earth.setZ(0.0)
        environment.earth.setScale(VBase3(8, 8, 8))
        environment.earth.setBin("background", 1)
        environment.ambientLight = AmbientLight("ambientLight")
        environment.ambientLight.setColor(Vec4(0.192481249571, 0.192481249571, 0.192481249571, 1))
        environment.directionalLight = DirectionalLight("directionalLight")
        environment.directionalLight.setDirection(Vec3(-5, -5, -5))
        environment.directionalLight.setColor(Vec4(0.244110241532, 0.244110241532, 0.244110241532, 1))
        environment.directionalLight.setSpecularColor(Vec4(0.244110241532, 0.244110241532, 0.244110241532, 1))
        environment.domenum = 6
        environment.playerShip = Ship(player1ship, 427.0, -283.0, 5, -92.0, environment, 12, 1)
        if multiplayer:
            environment.player2Ship = Ship(player2ship, 427.0, -310.0, 5, -92.0, environment, 12, 2)
        self.xpoints = [530.0, 739.0, 739.0, 853.0, 1094.0, 1205.0, 1342.0, 1439.0, 1473.0, 1505.0, 1505.0, 1472.0, 1399.0, 1308.0, 1218.0, 1018.0, 732.0, 650.0, 513.0, 425.0, 316.0, 144.0, 81.0, -259.0, -391.0, -544.0, -605.0, -679.0, -679.0, -677.0, -635.0, -626.0, -626.0, -672.0, -672.0, -659.0, -550.0, -313.0, 1.0, 111.0, 194.0, 276.0, 393.0]
        self.ypoints = [-341.0, -553.0, -553.0, -626.0, -676.0, -672.0, -571.0, -302.0, -206.0, -153.0, 173.0, 295.0, 511.0, 618.0, 619.0, 621.0, 578.0, 507.0, 369.0, 329.0, 344.0, 518.0, 573.0, 671.0, 671.0, 668.0, 640.0, 576.0, 416.0, 229.0, 154.0, 11.0, -307.0, -386.0, -584.0, -673.0, -675.0, -666.0, -638.0, -628.0, -576.0, -434.0, -310.0]
        self.xplaces = [427.0, 427.0, 411.0, 411.0, 411.0]
        self.yplaces = [-310.0, -334.0, -334.0, -309.0, -282.0]
        self.hs = [-92.0, -92.0, -92.0, -92.0, -92.0]
        shiptaken = [False, False, False, False, False, False]
        shiptaken[player1ship - 1] = True
        if multiplayer:
            shiptaken[player2ship - 1] = True
        self.startPlaces = [0, 4, 7, 11, 14, 17, 21, 24, 28, 31, 36, 38, 0]
        self.pointsnum = 43
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
            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, 12, self.startPlaces, i+1))
        environment.checkpoints.append(Checkpoint(1094.0, -676.0, 0, -93.0))
        environment.checkpoints.append(Checkpoint(1439.0, -302.0, 0, -23.0))
        environment.checkpoints.append(Checkpoint(1472.0, 295.0, 0, 15.0))
        environment.checkpoints.append(Checkpoint(1218.0, 619.0, 0, 91.0))
        environment.checkpoints.append(Checkpoint(650.0, 507.0, 0, 133.0))
        environment.checkpoints.append(Checkpoint(144.0, 518.0, 0, 46.0))
        environment.checkpoints.append(Checkpoint(-391.0, 671.0, 0, 91.0))
        environment.checkpoints.append(Checkpoint(-679.0, 416.0, 0, 180.0))
        environment.checkpoints.append(Checkpoint(-626.0, 11.0, 0, 178.0))
        environment.checkpoints.append(Checkpoint(-550.0, -675.0, 0, 271.0))
        environment.checkpoints.append(Checkpoint(1.0, -638.0, 0, 271.0))
        environment.checkpoints.append(Startingline(446.0, -310.0, 0, -92.0))
        environment.powerups.append(Powerup(-313.0, -666.0, 5))
        environment.powerups.append(Powerup(-313.0, -677.0, 5))
        environment.powerups.append(Powerup(-313.0, -690.0, 5))
        environment.powerups.append(Powerup(-313.0, -653.0, 5))
        environment.powerups.append(Powerup(-313.0, -638.0, 5))
        environment.powerups.append(Powerup(-313.0, -625.0, 5))
        environment.powerups.append(Powerup(684.0, -575.0, 5))
        environment.powerups.append(Powerup(697.0, -575.0, 5))
        environment.powerups.append(Powerup(716.0, -575.0, 5))
        environment.powerups.append(Powerup(736.0, -575.0, 5))
        environment.powerups.append(Powerup(751.0, -575.0, 5))
        environment.powerups.append(Powerup(768.0, -575.0, 5))
        environment.powerups.append(Powerup(1311.0, -534.0, 5))
        environment.powerups.append(Powerup(1342.0, -571.0, 5))
        environment.powerups.append(Powerup(1369.0, -597.0, 5))
        environment.powerups.append(Powerup(1459.0, -200.0, 5))
        environment.powerups.append(Powerup(1473.0, -207.0, 5))
        environment.powerups.append(Powerup(1487.0, -215.0, 5))
        environment.powerups.append(Powerup(1304.0, 561.0, 5))
        environment.powerups.append(Powerup(1304.0, 576.0, 5))
        environment.powerups.append(Powerup(1304.0, 592.0, 5))
        environment.powerups.append(Powerup(1304.0, 619.0, 5))
        environment.powerups.append(Powerup(1304.0, 604.0, 5))
        environment.powerups.append(Powerup(789.0, 588.0, 5))
        environment.powerups.append(Powerup(789.0, 618.0, 5))
        environment.powerups.append(Powerup(452.0, 272.0, 5))
        environment.powerups.append(Powerup(452.0, 292.0, 5))
        environment.powerups.append(Powerup(452.0, 309.0, 5))
        environment.powerups.append(Powerup(452.0, 331.0, 5))
        environment.powerups.append(Powerup(212.0, 477.0, 5))
        environment.powerups.append(Powerup(202.0, 463.0, 5))
        environment.powerups.append(Powerup(191.0, 448.0, 5))
        environment.powerups.append(Powerup(-256.0, 624.0, 5))
        environment.powerups.append(Powerup(-256.0, 662.0, 5))
        environment.powerups.append(Powerup(-643.0, 666.0, 5))
        environment.powerups.append(Powerup(-629.0, 648.0, 5))
        environment.powerups.append(Powerup(-617.0, 632.0, 5))
        environment.powerups.append(Powerup(-602.0, 619.0, 5))
        environment.powerups.append(Powerup(-621.0, 67.0, 5))
        environment.powerups.append(Powerup(-629.0, -184.0, 5))
        environment.powerups.append(Powerup(-637.0, -208.0, 5))
        environment.powerups.append(Powerup(-616.0, -208.0, 5))
        environment.powerups.append(Powerup(-672.0, -507.0, 5))
        environment.powerups.append(Powerup(303.0, -394.0, 5))
        environment.powerh.append(Powerh(1162.0, -658.0, 5))
        environment.powerh.append(Powerh(1162.0, -672.0, 5))
        environment.powerh.append(Powerh(1162.0, -682.0, 5))
        environment.powerh.append(Powerh(1325.0, -553.0, 5))
        environment.powerh.append(Powerh(1355.0, -585.0, 5))
        environment.powerh.append(Powerh(1411.0, 448.0, 5))
        environment.powerh.append(Powerh(1426.0, 452.0, 5))
        environment.powerh.append(Powerh(1439.0, 459.0, 5))
        environment.powerh.append(Powerh(1453.0, 473.0, 5))
        environment.powerh.append(Powerh(789.0, 568.0, 5))
        environment.powerh.append(Powerh(789.0, 603.0, 5))
        environment.powerh.append(Powerh(383.0, 329.0, 5))
        environment.powerh.append(Powerh(383.0, 306.0, 5))
        environment.powerh.append(Powerh(383.0, 283.0, 5))
        environment.powerh.append(Powerh(383.0, 265.0, 5))
        environment.powerh.append(Powerh(-256.0, 606.0, 5))
        environment.powerh.append(Powerh(-256.0, 643.0, 5))
        environment.powerh.append(Powerh(-256.0, 676.0, 5))
        environment.powerh.append(Powerh(-656.0, 469.0, 5))
        environment.powerh.append(Powerh(-672.0, 469.0, 5))
        environment.powerh.append(Powerh(-687.0, 469.0, 5))
        environment.powerh.append(Powerh(-672.0, -487.0, 5))
        environment.powerh.append(Powerh(318.0, -409.0, 5))
        base.camera.setPos(Point3(412.009, -282.477, 9))
        if multiplayer:
            environment.cam2.setPos(Point3(412.009, -309.477, 9))
        environment.laps = 2
        self.finishCredits = [1000, 500, 250, 166, 125, 0]
        self.finishPlace = 1
