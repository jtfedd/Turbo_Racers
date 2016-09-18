from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.showbase.PythonUtil import fitDestAngle2Src
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.filter.CommonFilters import CommonFilters
from direct.stdpy.file import *
from direct.showbase import Audio3DManager

from operator import attrgetter

import sys, imp, os, random, math

# Global collision variables
base.cTrav = CollisionTraverser('Collision Detection')
collisionHandler = CollisionHandlerPusher()
collisionHandler.addInPattern('%fn-into')

NumShipColl = 0
NumPowerColl = 0

collisionMask = BitMask32.bit(1)
offMask = BitMask32.allOff()

# Audio
audio3d = None

# Camera masks
cam1Mask = BitMask32.bit(0)
cam2Mask = BitMask32.bit(1)

#dt
dt = 0

def sign(num):
    if num >= 0:
        return 1
    if num < 0:
        return -1

class Multiplayer3DAudio(DirectObject):
    def __init__(self, environment):
        self.environment = environment
        self.audio3d1 = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.cam)
        if self.environment.multiplayer:
            self.audio3d2 = Audio3DManager.Audio3DManager(base.sfxManagerList[0], self.environment.cam2)
        
    def loadSfx(self, path):
        return self.audio3d1.loadSfx(path)
    
    def attachSoundToObject(self, sound, object):
        self.audio3d1.attachSoundToObject(sound, object)
        if self.environment.multiplayer:
            self.audio3d2.attachSoundToObject(sound, object)
        
    def detachSound(self, sound):
        self.audio3d1.detachSound(sound)
        if self.environment.multiplayer:
            self.audio3d2.detachSound(sound)

class Ship(DirectObject):
    def __init__(self, modelnum, x, y, z, h, environment, checkpoints, shipnum):
        self.name = 'user'
        self.user = environment.user
        self.dist = 0
        self.shielded = False
        self.shieldTime = 0
        self.environment = environment
        self.target = None
        self.scope = None
        self.lastPower = 'none'
        self.power = 'none'
        
        self.maxHealth = 100
        if self.environment.userUpgrades:
            self.maxHealth += 20 * self.user.upgrades[3]
        self.health = self.maxHealth
        
        self.MaxSpeed = 50
        if self.environment.userUpgrades:
            self.MaxSpeed += 5*self.user.upgrades[0]
        self.maxSpeed = self.MaxSpeed
            
        self.accelFact = 0.5
        if self.environment.userUpgrades:
            self.accelFact += 0.5*self.user.upgrades[1]
            
        self.turnFact = 5
        if self.environment.userUpgrades:
            self.turnFact += 0.5*self.user.upgrades[2]
            
        self.upgrade = False
        self.lastupgrade = self.upgrade
        self.powerSymbol = OnscreenImage(image = 'models/images/none.png',
                                        pos = (-1.2,0,-0.8),
                                        scale = (0.2, 1, 0.2))
        self.powerSymbol.setTransparency(TransparencyAttrib.MAlpha)
        self.boostTime = 0
        self.dead = False
        self.lap = 1
        self.checkPos = 0
        self.numCheck = checkpoints
        self.shipnum = shipnum
        self.modelnum = modelnum
        self.checkpoints = environment.checkpoints
        self.lapText = OnscreenText(text = 'Lap '+str(self.lap),
                                    fg = (1,1,0,1),
                                    pos = (-1, 0.8, 0),
                                    scale = 0.15,
                                    mayChange = 1)
                                    
        self.pos = 1
        self.postext = str(self.pos)
        if self.pos == 1:
            self.postext += 'st'
        elif self.pos == 2:
            self.postext += 'nd'
        elif self.pos == 3:
            self.postext += 'rd'
        else:
            self.postext += 'th'
        self.posText = OnscreenText(text = self.postext,
                                    fg = (1,1,0,1),
                                    pos = (1, 0.8, 0),
                                    scale = 0.15,
                                    mayChange = 1)
                                    
        #health
        self.healthImage = OnscreenImage(image = 'models/textures/heart.png',
                                         pos = (1, 0, -0.8),
                                         scale = (0.1, 1, 0.1))
        self.healthImage.setTransparency(TransparencyAttrib.MAlpha)
        self.healthText = OnscreenText(text = str(self.health)+'/'+str(self.maxHealth),
                                        fg = (1,0,0,1),
                                        pos = (1.3, -0.8, 0),
                                        scale = 0.07,
                                        mayChange = 1)

        if self.shipnum == 2:
            self.lapText.setPos(-1, -0.2)
            self.posText.setPos(1, -0.2)
        if self.shipnum == 1 and environment.multiplayer:
            self.powerSymbol.setPos(-1.2, 0, 0.2)
            self.healthImage.setPos(1, 0, 0.2)
            self.healthText.setPos(1.3, 0.2)

        sizes = [1.3, 1.0, 1.5, 1.5, 0.9, 1]
        self.ship = loader.loadModel('models/ship'+str(modelnum))
        self.size = sizes[modelnum - 1]
        self.ship.setScale(sizes[modelnum - 1])
        self.ship.setX(x)
        self.ship.setY(y)
        self.ship.setZ(z)
        self.ship.setH(h)
        self.ship.reparentTo(render)
        self.speed = 0
        self.targetr = 0
        
        self.dPos = self.ship.getPos()
        self.prePos = self.ship.getPos()
        
        self.immuneTime = 0
        self.immune = False
        
        # sounds
        
        self.sound = audio3d.loadSfx('sounds/sfx/engine' + str(modelnum) + '.wav')
        audio3d.attachSoundToObject(self.sound, self.ship)
        self.sound.setLoop(True)
        self.sound.setPlayRate(0.5)
        self.sound.setVolume(0.8)
        #self.sound.play()     Handled by Environment
        
        self.shieldsound = audio3d.loadSfx('sounds/sfx/shield.wav')
        audio3d.attachSoundToObject(self.shieldsound, self.ship)
        self.shieldsound.setLoop(True)
        
        self.powersound = audio3d.loadSfx('sounds/sfx/powerup.wav')
        audio3d.attachSoundToObject(self.powersound, self.ship)
        
        self.healthsound = audio3d.loadSfx('sounds/sfx/health.wav')
        audio3d.attachSoundToObject(self.healthsound, self.ship)
        
        self.turbosoundshort = audio3d.loadSfx('sounds/sfx/turbo.wav')
        audio3d.attachSoundToObject(self.turbosoundshort, self.ship)
        
        self.turbosoundlong = audio3d.loadSfx('sounds/sfx/turbolong.wav')
        audio3d.attachSoundToObject(self.turbosoundlong, self.ship)
        
        self.checksound = loader.loadSfx('sounds/sfx/checkpoint.wav')
        
        #Camera floaters

        self.cfloater = NodePath(PandaNode("floater"))
        self.cfloater.reparentTo(render)
        self.cfloater.setPos(self.ship.getPos())
        self.cfloater.setZ(self.ship.getZ() + 5)

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        self.floater.setPos(self.ship.getPos())
        self.floater.setZ(self.ship.getZ() + 0.2)
        
        self.dfloater = NodePath(PandaNode("floater"))                          # This is for distance measurements that require nodes, not points
        self.dfloater.reparentTo(render)
        
        #Collisions

        self.csphere = CollisionSphere(0,0,0,3/self.size)
        global NumShipColl
        self.cString = 'ship' + str(NumShipColl)
        NumShipColl += 1
        self.cnode = self.ship.attachNewNode(CollisionNode(self.cString))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        collisionHandler.addCollider(self.cnode, self.ship)
        base.cTrav.addCollider(self.cnode, collisionHandler)
        
        self.accept(self.cString + '-into', self.handleCollision)
        #self.cnode.show()

    def update(self, dir):
        if self.lap > self.environment.laps:
            if self.environment.afterRaceAction == 'careermenu':
                for i in range(len(self.ships)):
                    if self.ships[i].name == 'user':
                        self.environment.places[0] = i
                    if self.ships[i].name == 'cpu1':
                        self.environment.places[1] = i
                    if self.ships[i].name == 'cpu2':
                        self.environment.places[2] = i
                    if self.ships[i].name == 'cpu3':
                        self.environment.places[3] = i
                    if self.ships[i].name == 'cpu4':
                        self.environment.places[4] = i
                    if self.ships[i].name == 'cpu5':
                        self.environment.places[5] = i
            
            self.environment.allShips.remove(self)
            finishText = ''
            if self.pos == 1:
                finishText = 'Congratulations, you finished '+self.postext+'!'
            elif self.pos == 2:
                finishText = 'Good job, you finished '+self.postext+'!'
            else:
                finishText = 'Too bad, you finished '+self.postext+'.'
            if self.shipnum == 1:
                self.environment.p1Finished = True
                self.environment.arrow.removeNode()
                tempship = CPUShip(self.modelnum, self.ship.getX(), self.ship.getY(), self.ship.getZ(), self.ship.getH(), self.environment.Race.xpoints, self.environment.Race.ypoints, self.environment.Race.pointsnum, self.environment, self.numCheck, self.environment.Race.startPlaces, 1)
                tempship.name = self.name
                tempship.lap = self.lap
                tempship.speed = self.speed
                tempship.power = self.power
                tempship.upgrade = self.upgrade
                tempship.MaxSpeed = self.MaxSpeed
                tempship.maxSpeed = tempship.MaxSpeed
                tempship.maxHealth = self.maxHealth
                tempship.health = self.health
                tempship.turnFact = self.turnFact + 2
                tempship.accelFact = self.accelFact
                tempship.boostTime = self.boostTime
                tempship.sound.play()
                for powerup in self.environment.activePowerups:
                    if powerup.target == self:
                        powerup.target = tempship
                self.environment.playerShip = tempship
                self.environment.allShips.append(self.environment.playerShip)
                self.environment.ships.append(self.environment.playerShip)
                self.environment.p1Text.setText(finishText)
                if self.environment.multiplayer:
                    if self.environment.player2Ship.target == self:
                        self.environment.player2Ship.target = self.environment.playerShip
                
            if self.shipnum == 2:
                self.environment.p2Finished = True
                self.environment.arrow2.removeNode()
                tempship = CPUShip(self.modelnum, self.ship.getX(), self.ship.getY(), self.ship.getZ(), self.ship.getH(), self.environment.Race.xpoints, self.environment.Race.ypoints, self.environment.Race.pointsnum, self.environment, self.numCheck, self.environment.Race.startPlaces, 1)
                tempship.name = self.name
                tempship.lap = self.lap
                tempship.speed = self.speed
                tempship.power = self.power
                tempship.upgrade = self.upgrade
                tempship.MaxSpeed = self.MaxSpeed
                tempship.maxSpeed = tempship.MaxSpeed
                tempship.maxHealth = self.maxHealth
                tempship.health = self.health
                tempship.turnFact = self.turnFact + 2
                tempship.accelFact = self.accelFact
                tempship.boostTime = self.boostTime
                tempship.sound.play()
                for powerup in self.environment.activePowerups:
                    if powerup.target == self:
                        powerup.target = tempship
                self.environment.player2Ship = tempship
                self.environment.allShips.append(self.environment.player2Ship)
                self.environment.ships.append(self.environment.player2Ship)
                self.environment.p2Text.setText(finishText)
                if self.environment.multiplayer:
                    if self.environment.playerShip.target == self:
                        self.environment.playerShip.target = self.environment.player2Ship
            self.cleanup()
            return
        self.dist = math.sqrt((self.ship.getX() - self.checkpoints[self.checkPos].check.getX())**2 + (self.ship.getY() - self.checkpoints[self.checkPos].check.getY())**2)
        self.dead = False
        self.scope.update()
        self.lapText.setText('Lap '+str(self.lap)+'/'+str(self.environment.laps))
        
        self.healthText.setText(str(self.health)+'/'+str(self.maxHealth))
        if self.power != self.lastPower:
            filepath = 'models/images/' + self.power
            self.lastPower = self.power
            self.powerSymbol.setImage(filepath + '.png')
            self.powerSymbol.setTransparency(TransparencyAttrib.MAlpha)
            
        if self.upgrade != self.lastupgrade and self.upgrade:
            filepath = 'models/images/' + self.power + 'up'
            self.lastupgrade = self.upgrade
            self.powerSymbol.setImage(filepath + '.png')
            self.powerSymbol.setTransparency(TransparencyAttrib.MAlpha)
            
        if self.boostTime > 0:
            self.boostTime -= dt
            if self.boostTime <= 0:
                self.boostTime = 0
                self.maxSpeed = self.MaxSpeed
                self.speed = self.speed/2
                if self.speed > self.maxSpeed:
                    self.speed = self.maxSpeed
                    
        if self.shieldTime > 0:
            self.shieldTime -= dt
            if self.shieldTime <= 0:
                self.shieldTime = 0
                self.shielded = False
                if self.shieldsound.status() == self.shieldsound.PLAYING:
                    self.shieldsound.stop()
                self.cnode.hide()
                
        #place
        
        self.ships = self.environment.allShips
        
        self.ships.sort(key = attrgetter('dist'))
        self.ships.sort(key = attrgetter('checkPos'), reverse = True)
        self.ships.sort(key = attrgetter('lap'), reverse = True)
        
        self.pos = self.ships.index(self) + 1
                
        self.postext = str(self.pos)
        if self.pos == 1:
            self.postext += 'st'
        elif self.pos == 2:
            self.postext += 'nd'
        elif self.pos == 3:
            self.postext += 'rd'
        else:
            self.postext += 'th'
        self.posText.setText(self.postext)
        
        self.prePos = self.ship.getPos()
        
        if self.immuneTime > 0:
            self.immuneTime -= dt
            if self.immuneTime < 0:
                self.immune = False
        
        # Movement
        if dir[0]: #foreward
            if self.speed >= 0:
                self.speed += (self.maxSpeed/self.size - self.speed)*self.accelFact*dt
            if self.speed < 0:
                self.speed += 60*dt
        elif dir[1]: #backward
            if self.speed <= 0:
                self.speed -= (self.maxSpeed/self.size + self.speed)*self.accelFact*dt
            if self.speed > 0:
                self.speed -= 60*dt
        else:
            if self.speed > 0:
                self.speed -= 0.1
            if self.speed < 0:
                self.speed += 0.1
            if self.speed < 0.1 and self.speed > -0.1:
                self.speed = 0
        self.ship.setY(self.ship, self.speed * dt)
        leftr = False
        rightr = False
        tfact = self.speed / 10
        if tfact > self.turnFact:
            tfact = self.turnFact
        if dir[2]: #left
            if self.ship.getR() < 0:
                self.ship.setH(self.ship.getH() - self.ship.getR() * tfact * self.size * dt)
                if self.speed > (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size):
                    self.speed = (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size)
            self.targetr = -45
            leftr = True
        elif dir[3]: #right
            if self.ship.getR() > 0:
                self.ship.setH(self.ship.getH() - self.ship.getR() * tfact * self.size * dt)
                if self.speed > (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size):
                    self.speed = (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size)
            self.targetr = 45
            rightr = True
        elif leftr == False and rightr == False:
            self.targetr = 0
        if self.ship.getR() > self.targetr:
            self.ship.setR(self.ship.getR() - 75 * dt)
        if self.ship.getR() < self.targetr:
            self.ship.setR(self.ship.getR() + 75 * dt)
            
        self.ship.setZ(5)               #stay at constant height
        
        #set engine speed
        self.sound.setPlayRate(math.fabs(sign(self.speed)*.5+self.speed/50))

        #die if health is low
        if self.health <= 0:
            self.die()
            
        self.dPos = self.ship.getPos()

    def handleCollision(self, collEntry):
        otherObjNodePath = collEntry.getIntoNodePath()
        activePowerups = self.environment.activePowerups
        powerh = self.environment.powerh
        powerups = self.environment.powerups
        ships = self.environment.allShips
        checkpoints = self.checkpoints
        for powerup in powerups:
            if powerup.cnode == otherObjNodePath:
                #print 'Colliding with powerup'
                powerup.giveTo(self)
                return
        for powerh in powerh:
            if powerh.cnode == otherObjNodePath:
                #print 'Colliding with powerhealth'
                powerh.giveTo(self)
                return
        for powerup in activePowerups:
            if powerup.cnode == otherObjNodePath:
                #print 'Colliding with active powerup'
                if powerup.parent != self:
                    powerup.hit(self)
                return
        for checkpoint in checkpoints:
            if checkpoint.cnode == otherObjNodePath and checkpoint == checkpoints[self.checkPos]:
                #print 'Going through next checkpoint'
                self.checkPos += 1
                if self.checkPos == self.numCheck:
                    self.checkPos = 0
                    self.lap += 1
                self.checksound.play()
        if self.environment.cDieNode == otherObjNodePath:
            #print 'Colliding with terrain'
            self.die()
            return
        
    def die(self):
        if not self.dead:
            self.environment.explosions.append(Explosion(self.ship.getX(), self.ship.getY(), self.ship.getZ(), 10, 1, self.environment))
            if self.environment.multiplayer:
                self.environment.explosions.append(Explosion(self.ship.getX(), self.ship.getY(), self.ship.getZ(), 10, 2, self.environment))
            self.speed = 0
            lastCheck = self.checkPos - 1
            if lastCheck < 0:
                lastCheck = self.numCheck - 1
            self.ship.setX(self.environment.checkpoints[lastCheck].check.getX())
            self.ship.setY(self.environment.checkpoints[lastCheck].check.getY())
            self.ship.setZ(self.environment.checkpoints[lastCheck].check.getZ()+5)
            self.ship.setH(self.environment.checkpoints[lastCheck].check.getH())
            if self.shipnum == 1:
                base.camera.setPos(self.ship, (0, -15, 4))
                base.camera.setZ(9)
            else:
                self.environment.cam2.setPos(self.ship, (0, -15, 4))
                base.camera.setZ(9)
            self.health = self.maxHealth
            self.dead = True
            #reset powerups
            self.power = 'none'
            self.upgrade = False
            self.lastupgrade = False
            self.boostTime = 0
            self.shieldTime = 0
            self.maxSpeed = self.MaxSpeed
            self.shielded = False
            if self.shieldsound.status() == self.shieldsound.PLAYING:
                self.shieldsound.stop()
            self.cnode.hide()
            self.dPos = self.ship.getPos()
            self.prePos = self.ship.getPos()
            self.immuneTime = 1.5
            self.immune = True

    def shootPowerup(self):
        if self.power == 'rocket':
            if self.shipnum == 1 and self.environment.cam1Back:
                self.environment.activePowerups.append(Rocket(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            elif self.shipnum == 2 and self.environment.cam2Back:
                self.environment.activePowerups.append(Rocket(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            else:
                self.environment.activePowerups.append(Rocket(self.ship.getPos(), self.ship.getH(), self, self.upgrade, self.target))
            
        if self.power == 'cruise':
            if self.shipnum == 1 and self.environment.cam1Back:
                self.environment.activePowerups.append(Cruise(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            elif self.shipnum == 2 and self.environment.cam2Back:
                self.environment.activePowerups.append(Cruise(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            else:
                self.environment.activePowerups.append(Cruise(self.ship.getPos(), self.ship.getH(), self, self.upgrade, self.target))
            
        if self.power == 'desin':
            if self.shipnum == 1 and self.environment.cam1Back:
                self.environment.activePowerups.append(Desin(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            elif self.shipnum == 2 and self.environment.cam2Back:
                self.environment.activePowerups.append(Desin(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            else:
                self.environment.activePowerups.append(Desin(self.ship.getPos(), self.ship.getH(), self, self.upgrade, self.target))
            
        if self.power == 'boost':
            self.maxSpeed = self.MaxSpeed*2
            self.speed = self.speed*2
            self.boostTime += 1
            if not self.upgrade:
                self.turbosoundshort.play()
            if self.upgrade:
                self.boostTime += 1
                self.turbosoundlong.play()
                
        if self.power == 'shield':
            self.shielded = True
            self.cnode.show()
            self.shieldTime += 5
            if self.upgrade:
                self.shieldTime += 5
            if self.shieldsound.status() != self.shieldsound.PLAYING:
                self.shieldsound.play()
                
        if self.power == 'mine':
            self.environment.activePowerups.append(Mine(self.ship.getPos(), self))
            if self.upgrade:
                self.environment.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY()+5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY(), self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY()-5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX(), self.ship.getY()+5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX(), self.ship.getY()-5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY()+5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY(), self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY()-5, self.ship.getZ()), self))
            
        if self.power == 'seismic':
            self.environment.activePowerups.append(Seismic(self.ship.getPos(), self, self.upgrade))
            
        #powerup cleanup
        self.power = 'none'
        self.upgrade = False
        self.lastupgrade = False
        
    def checkCrashDamage(self):
        self.dfloater.setPos(self.dPos)
        dist = self.ship.getDistance(self.dfloater)
        if dist != 0 and not self.immune:
            if not self.shielded:
                self.health -= int(round(math.ceil(dist/dt)/3))
            
            currPos = self.ship.getPos()
            currHpr = self.ship.getHpr()
            
            self.ship.setPos(self.prePos)
            a1 = self.ship.getH()
            self.dfloater.setPos(currPos)
            self.ship.lookAt(self.dfloater)
            a2 = self.ship.getH()
            dist = self.ship.getDistance(self.dfloater)
            self.ship.setPos(currPos)
            self.ship.setHpr(currHpr)
            
            angle = a1-a2
            dist2 = dist*math.cos(math.radians(angle))
            
            self.speed = dist2/dt/self.size
        
        
    def getH(self):
        return self.ship.getH()

    def getPos(self):
        return self.ship.getPos()

    def getZ(self):
        return self.ship.getZ()

    def getY(self):
        return self.ship.getY()

    def getX(self):
        return self.ship.getX()
    
    def cleanup(self):
        self.ship.removeNode()
        self.powerSymbol.destroy()
        self.lapText.destroy()
        self.posText.destroy()
        self.healthImage.destroy()
        self.healthText.destroy()
        self.cfloater.removeNode()
        self.floater.removeNode()
        self.scope.cleanup()
        audio3d.detachSound(self.sound)
        audio3d.detachSound(self.shieldsound)
        audio3d.detachSound(self.powersound)
        audio3d.detachSound(self.healthsound)
        audio3d.detachSound(self.turbosoundlong)
        audio3d.detachSound(self.turbosoundshort)
        self.sound.stop()
        if self.shieldsound.status() == self.shieldsound.PLAYING:
            self.shieldsound.stop()
        if self.powersound.status() == self.powersound.PLAYING:
            self.powersound.stop()
        if self.healthsound.status() == self.healthsound.PLAYING:
            self.healthsound.stop()

class CPUShip(DirectObject):
    def __init__(self, modelnum, x, y, z, h, xpoints, ypoints, pointsnum, environment, checkpoints, startPlaces, cpuNum):
        self.name = 'cpu'+str(cpuNum)
        self.cpuNum = cpuNum
        self.shielded = False                           #Are we currently shielded?
        self.shieldTime = 0                             #Time until shield expires
        self.power = 'none'                             #Current powerup held
        self.lastPower = self.power                     #Powerup held last frame
        self.powerTime = 0                              #Time until currently held powerup is deployed
        self.upgrade = False                            #Is our powerup upgraded?
        self.lastUpgrade = self.upgrade                 #Was our powerup upgraded last frame?
        self.boostTime = 0                              #Time until boost expires
        self.dist = 0                                   #Distance to next checkpoint, used to determine position in race
        
        self.dead = False                               #used for multiple collisions on same frame
        self.lap = 1                                    #what lap are we on?
        self.checkPos = 0                               #index of next checkpoint
        self.numCheck = checkpoints                     #number of checkpoints
        self.checkpoints = environment.checkpoints      #list of checkpoints
        self.startPlaces = startPlaces                  #points to start at according to checkPos
        self.environment = environment                  #environment
        self.target = None                              #Computer ships don't target
        
        # Upgrades
        
        upgrades = []
        if cpuNum == 1:
            upgrades = environment.user.cpu1Upgrades
        if cpuNum == 2:
            upgrades = environment.user.cpu2Upgrades
        if cpuNum == 3:
            upgrades = environment.user.cpu3Upgrades
        if cpuNum == 4:
            upgrades = environment.user.cpu4Upgrades
        if cpuNum == 5:
            upgrades = environment.user.cpu5Upgrades
            
        self.maxHealth = 100
        self.MaxSpeed = 50
        self.accelFact = 0.5
        self.turnFact = 7
        if self.environment.CPUUpgrades:
            self.MaxSpeed += 5*upgrades[0]
            self.accelFact += 0.5*upgrades[1]
            self.turnFact += 0.5*upgrades[2]
            self.maxHealth += 20*upgrades[3]
        self.maxSpeed = self.MaxSpeed
        self.health = self.maxHealth
        
        #AI variables
        self.place = 0                          #index of location in ai points to follow
        self.xs = xpoints                       #x's of points to follow
        self.ys = ypoints                       #y's of points to follow
        self.max = pointsnum                    #number of points to follow
        self.prex = x                           #x position last frame
        self.prey = y                           #y position last frame
        self.dir = [0, 0, 0, 0, 0, 0, 0, 0]     #directional variable for steering
        
        self.turnTimer = 0                      #variables to prevent driving in circles
        self.turnDir = 'left'

        #normal stuff
        sizes = [1.3, 1.0, 1.5, 1.5, 0.9, 1.0]
        self.ship = loader.loadModel('models/ship'+str(modelnum))
        self.ship.setScale(sizes[modelnum - 1])
        self.size = sizes[modelnum - 1]
        self.ship.setX(x)
        self.ship.setY(y)
        self.ship.setZ(z)
        self.ship.setH(h)
        self.ship.reparentTo(render)
        self.override = False
        self.prevSpeed = 0
        self.tr = 0
        self.tp = 0
        self.speed = 0
        self.targetr = 0
        self.overp = False
        
        self.dPos = self.ship.getPos()
        self.prePos = self.ship.getPos()
        
        self.immuneTime = 0
        self.immune = False
        
        self.stuckTime = 0
        self.stuck = 1
        
        #sounds
        
        self.sound = audio3d.loadSfx('sounds/sfx/engine' + str(modelnum) + '.wav')
        audio3d.attachSoundToObject(self.sound, self.ship)
        self.sound.setLoop(True)
        self.sound.setPlayRate(0.5)
        self.sound.setVolume(0.8)
        
        self.shieldsound = audio3d.loadSfx('sounds/sfx/shield.wav')
        audio3d.attachSoundToObject(self.shieldsound, self.ship)
        self.shieldsound.setLoop(True)
        
        self.powersound = audio3d.loadSfx('sounds/sfx/powerup.wav')
        audio3d.attachSoundToObject(self.powersound, self.ship)
        
        self.healthsound = audio3d.loadSfx('sounds/sfx/health.wav')
        audio3d.attachSoundToObject(self.healthsound, self.ship)
        
        self.turbosoundshort = audio3d.loadSfx('sounds/sfx/turbo.wav')
        audio3d.attachSoundToObject(self.turbosoundshort, self.ship)
        
        self.turbosoundlong = audio3d.loadSfx('sounds/sfx/turbolong.wav')
        audio3d.attachSoundToObject(self.turbosoundlong, self.ship)
        
        #Camera floaters

        self.cfloater = NodePath(PandaNode("floater"))
        self.cfloater.reparentTo(render)
        self.cfloater.setPos(self.ship.getPos())
        self.cfloater.setZ(self.ship.getZ() + 5)

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        self.floater.setPos(self.ship.getPos())
        self.floater.setZ(self.ship.getZ() + 0.2)
        
        self.dfloater = NodePath(PandaNode("floater"))                          # This is for distance measurements that require nodes, not points
        self.dfloater.reparentTo(render)

        #collision stuff
        self.csphere = CollisionSphere(0,0,0,3/self.size)
        global NumShipColl
        self.cString = 'ship' + str(NumShipColl)
        NumShipColl += 1
        self.cnode = self.ship.attachNewNode(CollisionNode(self.cString))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        collisionHandler.addCollider(self.cnode, self.ship)
        base.cTrav.addCollider(self.cnode, collisionHandler)
        self.accept(self.cString + '-into', self.handleCollision)
        #self.cnode.show()

    def update(self):
        self.dist = math.sqrt((self.ship.getX() - self.checkpoints[self.checkPos].check.getX())**2 + (self.ship.getY() - self.checkpoints[self.checkPos].check.getY())**2)
        self.dead = False
        
        self.stuckTime += dt*self.stuck
        if self.speed > 5 and self.stuck > 0:
            self.stuckTime = 0
            
        if self.stuckTime > 2:
            self.stuck = -1
            self.stuckTime = 0
            
        if self.stuckTime < -1.5:
            self.stuck = 1
            self.stuckTime = -3
        
        if self.dir[2]:
            if self.turnDir == 'left':
                self.turnTimer += dt
            else:
                self.turnTimer = 0
            self.turnDir = 'left'
        if self.dir[3]:
            if self.turnDir == 'right':
                self.turnTimer += dt
            else:
                self.turnTimer = 0
            self.turnDir = 'left'
        
        self.determineDir()
        
        if self.boostTime > 0:
            self.boostTime -= dt
            if self.boostTime <= 0:
                self.boostTime = 0
                self.maxSpeed = self.MaxSpeed
                self.speed = self.speed/2
                if self.speed > self.maxSpeed:
                    self.speed = self.maxSpeed
                    
        if self.shieldTime > 0:
            self.shieldTime -= dt
            if self.shieldTime <= 0:
                self.shieldTime = 0
                self.shielded = False
                self.cnode.hide()
                if self.shieldsound.status() == self.shieldsound.PLAYING:
                    self.shieldsound.stop()
        
        if self.powerTime > 0:
            self.powerTime -= dt
            if self.powerTime <= 0:
                self.shootPowerup()
                self.powerTime = 0
                
        self.prePos = self.ship.getPos()
        
        if self.immuneTime > 0:
            self.immuneTime -= dt
            if self.immuneTime < 0:
                self.immune = False
        
        if self.dir[0]: #foreward
            if self.speed >= 0:
                self.speed += (self.maxSpeed/self.size - self.speed)*self.accelFact*dt
            if self.speed < 0:
                self.speed += 60*dt
        elif self.dir[1]: #backward
            if self.speed <= 0:
                self.speed -= (self.maxSpeed/self.size + self.speed)*self.accelFact*dt
            if self.speed > 0:
                self.speed -= 60*dt
        else:
            if self.speed > 0:
                self.speed -= 0.1
            if self.speed < 0:
                self.speed += 0.1
            if self.speed < 0.1 and self.speed > -0.1:
                self.speed = 0
        self.ship.setY(self.ship, self.speed * dt)
        leftr = False
        rightr = False
        tfact = self.speed / 10
        if tfact > self.turnFact:
            tfact = self.turnFact
        if self.dir[2]: #left
            if self.ship.getR()*self.stuck < 0:
                self.ship.setH(self.ship.getH() - self.ship.getR() * tfact * self.size * dt)
                if self.speed > (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size):
                    self.speed = (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size)
            self.targetr = -45*self.stuck
            leftr = True
        elif self.dir[3]: #right
            if self.ship.getR()*self.stuck > 0:
                self.ship.setH(self.ship.getH() - self.ship.getR() * tfact * self.size * dt)
                if self.speed > (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size):
                    self.speed = (self.maxSpeed/self.size)-(math.fabs(self.ship.getR())/(self.turnFact)/self.size)
            self.targetr = 45*self.stuck
            rightr = True
        elif leftr == False and rightr == False:
            self.targetr = 0
        if self.ship.getR() > self.targetr:
            self.ship.setR(self.ship.getR() - 75 * dt)
        if self.ship.getR() < self.targetr:
            self.ship.setR(self.ship.getR() + 75 * dt)
            
        self.ship.setZ(5)
                
        #Powerups
        if self.power != self.lastPower and self.power != 'none':       #If a powerup was just taken...
            if random.randrange(3) == 1:                                #then decide whether to use it (1 in 3 chance)... (Otherwise, wait for it to be upgraded)
                self.powerTime = random.randrange(7)                    #If use it, decide when (7 seconds or under).
            
        if self.upgrade != self.lastUpgrade and self.upgrade:           #If an upgrade was just taken...
            self.powerTime = random.randrange(7)                        #Decide when to use it(7 seconds or under).
            
        self.lastPower = self.power
        self.lastUpgrade = self.upgrade
            
        #set engine speed
        self.sound.setPlayRate(math.fabs(sign(self.speed)*.5+self.speed/50))

                
        if self.health <= 0:    # Die if health is gone
            self.die()
            
        self.dPos = self.ship.getPos()

    def determineDir(self):     # AI to determine how to steer
        px = self.xs[self.place]
        py = self.ys[self.place]
        pz = 5
        
        a1 = self.ship.getH()
        currHpr = self.ship.getHpr()
        self.dfloater.setPos(px, py, pz)
        self.ship.lookAt(self.dfloater)
        a2 = self.ship.getH()
        dist = self.ship.getDistance(self.dfloater)
        self.ship.setHpr(currHpr)
        
        a2 = fitDestAngle2Src(a1, a2)
        
        angle = a1-a2
        
        dist2 = dist*math.sin(math.radians(math.fabs(angle)))
        
        if dist2 > 1:
            if angle < 0:
                self.dir[2] = 1
                self.dir[3] = 0
            else:
                self.dir[2] = 0
                self.dir[3] = 1
        else:
            self.dir[2] = 0
            self.dir[3] = 0
        
        if self.stuck == 1:
            self.dir[0] = 1
            self.dir[1] = 0
        else:
            self.dir[0] = 0
            self.dir[1] = 1
        
        x = self.ship.getX()
        y = self.ship.getY()

        if x > px - 7 and x < px + 7 and y > py - 7 and y < py + 7:     # If close to target advance to next
            self.place += 1
        if self.turnTimer > 5:
            self.place += 1
            self.turnTimer = 0
        if self.place >= self.max:
            self.place = 0

    def handleCollision(self, collEntry):          # Handle collisions in different situations
        otherObjNodePath = collEntry.getIntoNodePath()
        activePowerups = self.environment.activePowerups
        powerh = self.environment.powerh
        powerups = self.environment.powerups
        ships = self.environment.allShips
        checkpoints = self.checkpoints
        for powerup in powerups:                    #collisions with powerups...
            if powerup.cnode == otherObjNodePath:
                #print 'Colliding with powerup'
                powerup.giveTo(self)
                return
        for powerh in powerh:                       #collisions with health bonuses...
            if powerh.cnode == otherObjNodePath:
                #print 'Colliding with powerhealth'
                powerh.giveTo(self)
                return
        for powerup in activePowerups:              #collisions with missles, mines, etc...
            if powerup.cnode == otherObjNodePath:
                #print 'Colliding with active powerup'
                if powerup.parent != self:
                    powerup.hit(self)
                return
        for checkpoint in checkpoints:              #going through checkpoints...
            if checkpoint.cnode == otherObjNodePath and checkpoint == checkpoints[self.checkPos]:
                #print 'Going through next checkpoint'
                self.checkPos += 1
                if self.checkPos == self.numCheck:
                    self.checkPos = 0
                    self.lap += 1
        if otherObjNodePath == self.environment.cDieNode:       #collisions with terrain...
            #print 'Colliding with terrain'
            self.die()
            return
        
    def die(self):                      # Die: go back to last checkpoint and place explosions
        if not self.dead:
            checkpoints = self.checkpoints
            self.place = self.startPlaces[self.checkPos]
            self.environment.explosions.append(Explosion(self.ship.getX(), self.ship.getY(), self.ship.getZ(), 10, 1, self.environment))
            if self.environment.multiplayer:
                self.environment.explosions.append(Explosion(self.ship.getX(), self.ship.getY(), self.ship.getZ(), 10, 2, self.environment))
            self.speed = 0
            lastCheck = self.checkPos - 1
            if lastCheck < 0:
                lastCheck = self.numCheck - 1
            self.ship.setX(self.checkpoints[lastCheck].check.getX())
            self.ship.setY(self.checkpoints[lastCheck].check.getY())
            self.ship.setZ(self.checkpoints[lastCheck].check.getZ() + 5)
            self.ship.setH(self.checkpoints[lastCheck].check.getH())
            self.health = self.maxHealth
            self.dead = True
            #reset powerups
            self.power = 'none'
            self.upgrade = False
            self.lastupgrade = False
            self.boostTime = 0
            self.shieldTime = 0
            self.maxSpeed = self.MaxSpeed
            self.shielded = False
            if self.shieldsound.status() == self.shieldsound.PLAYING:
                self.shieldsound.stop()
            self.cnode.hide()
            self.dPos = self.ship.getPos()
            self.prePos = self.ship.getPos()
            self.immuneTime = 1.5
            self.immune = True

    def shootPowerup(self):
        if self.power == 'rocket':
            self.environment.activePowerups.append(Rocket(self.ship.getPos(), self.ship.getH(), self, self.upgrade, None))
            
        if self.power == 'cruise':
            self.environment.activePowerups.append(Cruise(self.ship.getPos(), self.ship.getH(), self, self.upgrade, None))
            
        if self.power == 'desin':
            self.environment.activePowerups.append(Desin(self.ship.getPos(), self.ship.getH(), self, self.upgrade, None))
            
        if self.power == 'boost':
            self.maxSpeed = self.maxSpeed*2
            self.speed = self.speed*2
            self.boostTime += 1
            if not self.upgrade:
                self.turbosoundshort.play()
            if self.upgrade:
                self.turbosoundlong.play()
                self.boostTime += 1
                
        if self.power == 'shield':
            self.shielded = True
            self.cnode.show()
            self.shieldTime += 5
            if self.upgrade:
                self.shieldTime += 5
            if self.shieldsound.status() != self.shieldsound.PLAYING:
                self.shieldsound.play()
                
        if self.power == 'mine':
            self.environment.activePowerups.append(Mine(self.ship.getPos(), self))
            if self.upgrade:
                self.environment.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY()+5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY(), self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY()-5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX(), self.ship.getY()+5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX(), self.ship.getY()-5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY()+5, self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY(), self.ship.getZ()), self))
                self.environment.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY()-5, self.ship.getZ()), self))
                
        if self.power == 'seismic':
            self.environment.activePowerups.append(Seismic(self.ship.getPos(), self, self.upgrade))

        #powerup cleanup
        self.power = 'none'
        self.upgrade = False
        self.lastupgrade = False
        
    def checkCrashDamage(self):
        self.dfloater.setPos(self.dPos)
        dist = self.ship.getDistance(self.dfloater)
        if dist != 0 and not self.immune:
            if not self.shielded:
                self.health -= int(round(math.ceil(dist/dt)/3))
            
            currPos = self.ship.getPos()
            currHpr = self.ship.getHpr()
            
            self.ship.setPos(self.prePos)
            a1 = self.ship.getH()
            self.dfloater.setPos(currPos)
            self.ship.lookAt(self.dfloater)
            a2 = self.ship.getH()
            dist = self.ship.getDistance(self.dfloater)
            self.ship.setPos(currPos)
            self.ship.setHpr(currHpr)
            
            angle = a1-a2
            dist2 = dist*math.cos(math.radians(angle))
            
            self.speed = dist2/dt/self.size
        
    def getH(self):
        return self.ship.getH()

    def getPos(self):
        return self.ship.getPos()

    def getZ(self):
        return self.ship.getZ()

    def getY(self):
        return self.ship.getY()

    def getX(self):
        return self.ship.getX()
    
    def cleanup(self):
        self.ship.removeNode()
        audio3d.detachSound(self.sound)
        audio3d.detachSound(self.shieldsound)
        audio3d.detachSound(self.powersound)
        audio3d.detachSound(self.healthsound)
        audio3d.detachSound(self.turbosoundlong)
        audio3d.detachSound(self.turbosoundshort)
        self.sound.stop()
        if self.healthsound.status() == self.healthsound.PLAYING:
            self.healthsound.stop()
        if self.shieldsound.status() == self.shieldsound.PLAYING:
            self.shieldsound.stop()
        if self.powersound.status() == self.powersound.PLAYING:
            self.powersound.stop()

class Rocket(DirectObject):
    def __init__(self, pos, h, parent, upgrade, target):
        self.dead = False
        self.upgrade = upgrade
        self.parent = parent
        self.target = target
        self.model = loader.loadModel("models/rocket")
        self.model.setH(h)
        self.model.setPos(pos)
        self.model.setScale(0.2)
        self.model.reparentTo(render)
        
        if self.target == None:
            self.place = self.parent.place
            self.otherShips = []
            for ship in self.parent.environment.allShips:
                if ship != self.parent:
                    self.otherShips.append(ship)
            self.shipPlace = 0
            self.shipMax = len(self.otherShips)

        self.csphere = CollisionSphere(0,0,0,3)
        self.csphere.setTangible(False)
        global NumPowerColl
        self.cString = 'power' + str(NumPowerColl)
        NumPowerColl += 1
        self.cnode = self.model.attachNewNode(CollisionNode(self.cString))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        collisionHandler.addCollider(self.cnode, self.model)
        base.cTrav.addCollider(self.cnode, collisionHandler)
        self.accept(self.cString + '-into', self.handleCollision)
        
        self.sound = audio3d.loadSfx('sounds/sfx/rocket.wav')
        self.sound.setLoop(True)
        audio3d.attachSoundToObject(self.sound, self.model)
        self.sound.play()
        #self.cnode.show()

    def update(self):
        if self.upgrade:
            self.setDir()
        self.model.setY(self.model, 500 * dt)

    def handleCollision(self, collEntry):
        otherObjNodePath = collEntry.getIntoNodePath()
        if otherObjNodePath == self.parent.environment.cPushNode or otherObjNodePath == self.parent.environment.cDieNode:
            self.die()
            return
        for checkpoint in self.parent.environment.checkpoints:
            if otherObjNodePath == checkpoint.cFrame:
                self.die()
                return

    def hit(self, ship):
        if not ship.shielded:
            ship.speed -= 20/ship.size
            if ship.speed < 0:
                ship.speed = 0
            ship.health -= 40
        self.die()

    def setDir(self):
        x = self.model.getX()
        y = self.model.getY()
        
        if self.target is not None:
            currentH = self.model.getH()
            self.model.lookAt(self.target.ship)
            targetH = self.model.getH()
            self.model.setH(currentH)
            
            targetH = fitDestAngle2Src(currentH, targetH)
            
            angle = targetH - currentH
            turnmax = 300*dt
            
            if angle > turnmax:
                self.model.setH(self.model.getH()+turnmax)
            elif angle < -turnmax:
                self.model.setH(self.model.getH()-turnmax)
            else:
                self.model.setH(self.model.getH()+angle)
        else:
            px = self.parent.xs[self.place]
            py = self.parent.ys[self.place]
            if x > px - 5 and x < px + 5 and y > py - 5 and y < py + 5:     # If close to target advance to next
                self.place += 1
            if self.place == self.parent.max:
                self.place = 0
            try:
                if x > self.otherShips[self.shipPlace].ship.getX() - 20 and x < self.otherShips[self.shipPlace].ship.getX() + 20 and y > self.otherShips[self.shipPlace].ship.getY() - 20 and y < self.otherShips[self.shipPlace].ship.getY() + 20:
                    self.target = self.otherShips[self.shipPlace]
                else:
                    self.shipPlace += 1
                    if self.shipPlace == self.shipMax:
                        self.shipPlace = 0
            except AssertionError:
                if not self.parent.environment.multiplayer:
                    self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                else:
                    foundnewShip = False
                    for ship in self.otherShips:
                        if ship == self.parent.environment.playerShip:
                            self.otherShips[self.shipPlace] = self.parent.environment.player2Ship
                            foundnewShip = True
                    if not foundnewShip:
                        for ship in self.otherShips:
                            if ship == self.parent.environment.player2Ship:
                                self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                                foundnewShip = True
            currentH = self.model.getH()
            self.model.lookAt((px, py, 5))
            targetH = self.model.getH()
            self.model.setH(currentH)
            
            targetH = fitDestAngle2Src(currentH, targetH)
            
            angle = targetH - currentH
            turnmax = 300*dt
            
            if angle > turnmax:
                self.model.setH(self.model.getH()+turnmax)
            elif angle < -turnmax:
                self.model.setH(self.model.getH()-turnmax)
            else:
                self.model.setH(self.model.getH()+angle)
                
    def die(self):
        if not self.dead:
            self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 1, self.parent.environment))
            if self.parent.environment.multiplayer:
                self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 2, self.parent.environment))
            self.model.removeNode()
            self.parent.environment.activePowerups.remove(self)
            self.dead = True
            audio3d.detachSound(self.sound)
            self.sound.stop()
            
    def cleanup(self):
        self.model.removeNode()
        audio3d.detachSound(self.sound)
        self.sound.stop()

class Cruise(DirectObject):
    def __init__(self, pos, h, parent, upgrade, target):
        self.dead = False
        self.upgrade = upgrade
        self.parent = parent
        self.target = target
        self.model = loader.loadModel("models/cruise")
        self.model.setH(h)
        self.model.setPos(pos)
        self.model.setScale(0.5)
        self.model.reparentTo(render)
        
        if self.target == None:
            self.place = self.parent.place
            self.otherShips = []
            for ship in self.parent.environment.allShips:
                if ship != self.parent:
                    self.otherShips.append(ship)
            self.shipPlace = 0
            self.shipMax = len(self.otherShips)

        self.csphere = CollisionSphere(0,0,0,3)
        self.csphere.setTangible(False)
        global NumPowerColl
        self.cString = 'power' + str(NumPowerColl)
        NumPowerColl += 1
        self.cnode = self.model.attachNewNode(CollisionNode(self.cString))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        collisionHandler.addCollider(self.cnode, self.model)
        base.cTrav.addCollider(self.cnode, collisionHandler)
        self.accept(self.cString + '-into', self.handleCollision)
        #self.cnode.show()
        
        self.sound = audio3d.loadSfx('sounds/sfx/cruise.wav')
        self.sound.setLoop(True)
        audio3d.attachSoundToObject(self.sound, self.model)
        self.sound.play()

    def update(self):
        if self.upgrade:
            self.setDir()
        self.model.setY(self.model, 125 * dt)

    def handleCollision(self, collEntry):
        otherObjNodePath = collEntry.getIntoNodePath()
        if otherObjNodePath == self.parent.environment.cPushNode or otherObjNodePath == self.parent.environment.cDieNode:
            self.die()
            return
        for checkpoint in self.parent.environment.checkpoints:
            if otherObjNodePath == checkpoint.cFrame:
                self.die()
                return

    def hit(self, ship):
        if not ship.shielded:
            ship.speed -= 30/ship.size
            if ship.speed < 0:
                ship.speed = 0
            ship.health -= 50
        self.die()

    def setDir(self):
        x = self.model.getX()
        y = self.model.getY()
        
        if self.target is not None:
            currentH = self.model.getH()
            self.model.lookAt(self.target.ship)
            targetH = self.model.getH()
            self.model.setH(currentH)
            
            targetH = fitDestAngle2Src(currentH, targetH)
            
            angle = targetH - currentH
            turnmax = 40*dt
            
            if angle > turnmax:
                self.model.setH(self.model.getH()+turnmax)
            elif angle < -turnmax:
                self.model.setH(self.model.getH()-turnmax)
            else:
                self.model.setH(self.model.getH()+angle)
        else:
            px = self.parent.xs[self.place]
            py = self.parent.ys[self.place]
            if x > px - 5 and x < px + 5 and y > py - 5 and y < py + 5:     # If close to target advance to next
                self.place += 1
            if self.place == self.parent.max:
                self.place = 0
            try:
                if x > self.otherShips[self.shipPlace].ship.getX() - 20 and x < self.otherShips[self.shipPlace].ship.getX() + 20 and y > self.otherShips[self.shipPlace].ship.getY() - 20 and y < self.otherShips[self.shipPlace].ship.getY() + 20:
                    self.target = self.otherShips[self.shipPlace]
                else:
                    self.shipPlace += 1
                    if self.shipPlace == self.shipMax:
                        self.shipPlace = 0
            except AssertionError:
                if not self.parent.environment.multiplayer:
                    self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                else:
                    foundnewShip = False
                    for ship in self.otherShips:
                        if ship == self.parent.environment.playerShip:
                            self.otherShips[self.shipPlace] = self.parent.environment.player2Ship
                            foundnewShip = True
                    if not foundnewShip:
                        for ship in self.otherShips:
                            if ship == self.parent.environment.player2Ship:
                                self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                                foundnewShip = True
            
            currentH = self.model.getH()
            self.model.lookAt((px, py, 5))
            targetH = self.model.getH()
            self.model.setH(currentH)
            
            targetH = fitDestAngle2Src(currentH, targetH)
            
            angle = targetH - currentH
            turnmax = 40*dt
            
            if angle > turnmax:
                self.model.setH(self.model.getH()+turnmax)
            elif angle < -turnmax:
                self.model.setH(self.model.getH()-turnmax)
            else:
                self.model.setH(self.model.getH()+angle)

    def die(self):
        if not self.dead:
            self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 1, self.parent.environment))
            if self.parent.environment.multiplayer:
                self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 2, self.parent.environment))
            self.model.removeNode()
            self.parent.environment.activePowerups.remove(self)
            self.dead = True
            audio3d.detachSound(self.sound)
            self.sound.stop()
            
    def cleanup(self):
        self.model.removeNode()
        audio3d.detachSound(self.sound)
        self.sound.stop()
            
class Desin(DirectObject):
    def __init__(self, pos, h, parent, upgrade, target):
        self.dead = False
        self.upgrade = upgrade
        self.parent = parent
        self.target = target
        self.model = loader.loadModel("models/desinigrate")
        self.model.setPos(pos)
        self.model.setH(h+180)
        self.model.setScale(0.2)
        self.model.reparentTo(render)
        
        if self.target == None:
            self.place = self.parent.place
            self.otherShips = []
            for ship in self.parent.environment.allShips:
                if ship != self.parent:
                    self.otherShips.append(ship)
            self.shipPlace = 0
            self.shipMax = len(self.otherShips)

        self.csphere = CollisionSphere(0,0,0,3)
        self.csphere.setTangible(False)
        global NumPowerColl
        self.cString = 'power' + str(NumPowerColl)
        NumPowerColl += 1
        self.cnode = self.model.attachNewNode(CollisionNode(self.cString))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        collisionHandler.addCollider(self.cnode, self.model)
        base.cTrav.addCollider(self.cnode, collisionHandler)
        self.accept(self.cString + '-into', self.handleCollision)
        #self.cnode.show()
        
        self.sound = audio3d.loadSfx('sounds/sfx/energy.wav')
        self.sound.setLoop(True)
        audio3d.attachSoundToObject(self.sound, self.model)
        self.sound.play()

    def update(self):
        if self.upgrade:
            self.determineDir()
        self.model.setY(self.model, -500 * dt)

    def handleCollision(self, collEntry):
        otherObjNodePath = collEntry.getIntoNodePath()
        if otherObjNodePath == self.parent.environment.cPushNode or otherObjNodePath == self.parent.environment.cDieNode:
            self.die()
            return
        for checkpoint in self.parent.environment.checkpoints:
            if otherObjNodePath == checkpoint.cFrame:
                self.die()
                return

    def hit(self, ship):
        if not ship.shielded:
            ship.speed -= 30/ship.size
            if ship.speed < 0:
                ship.speed = 0
            ship.health -= 70
        self.die()

    def determineDir(self):
        x = self.model.getX()
        y = self.model.getY()
        
        if self.target is not None:
            self.model.lookAt(self.target.ship)
            self.model.setH(self.model.getH() + 180)
            self.model.setP(-self.model.getP())
            
        else:
            px = self.parent.xs[self.place]
            py = self.parent.ys[self.place]
            if x > px - 5 and x < px + 5 and y > py - 5 and y < py + 5:     # If close to target advance to next
                self.place += 1
            if self.place == self.parent.max:
                self.place = 0
            try:
                if x > self.otherShips[self.shipPlace].ship.getX() - 20 and x < self.otherShips[self.shipPlace].ship.getX() + 20 and y > self.otherShips[self.shipPlace].ship.getY() - 20 and y < self.otherShips[self.shipPlace].ship.getY() + 20:
                    self.target = self.otherShips[self.shipPlace]
                else:
                    self.shipPlace += 1
                    if self.shipPlace == self.shipMax:
                        self.shipPlace = 0
            except AssertionError:
                if not self.parent.environment.multiplayer:
                    self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                else:
                    foundnewShip = False
                    for ship in self.otherShips:
                        if ship == self.parent.environment.playerShip:
                            self.otherShips[self.shipPlace] = self.parent.environment.player2Ship
                            foundnewShip = True
                    if not foundnewShip:
                        for ship in self.otherShips:
                            if ship == self.parent.environment.player2Ship:
                                self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                                foundnewShip = True
            self.model.lookAt((px, py, 5))
            self.model.setH(self.model.getH() + 180)
            self.model.setP(-self.model.getP())

    def die(self):
        if not self.dead:
            self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 1, self.parent.environment))
            if self.parent.environment.multiplayer:
                self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 2, self.parent.environment))
            self.model.removeNode()
            self.parent.environment.activePowerups.remove(self)
            self.dead = True
            audio3d.detachSound(self.sound)
            self.sound.stop()
            
    def cleanup(self):
        self.model.removeNode()
        audio3d.detachSound(self.sound)
        self.sound.stop()

class Mine(DirectObject):
    def __init__(self, pos, parent):
        self.target = None
        self.dead = False
        self.Hit = False
        self.parent = parent
        self.velocity = 0
        self.model = loader.loadModel('models/mine')
        self.model.setPos(pos)
        self.model.setH(random.randrange(360))
        self.model.setScale(1.3)
        self.model.reparentTo(render)
        
        self.sound = audio3d.loadSfx('sounds/sfx/mine.wav')
        audio3d.attachSoundToObject(self.sound, self.model)
        self.sound.play()
        
        self.cnode = self.model.find('**/Cube')
    def update(self):
        if self.model.getZ() > 0:
            self.model.setZ(self.model.getZ() - 5*dt)
        if self.model.getZ() < 0:
            self.model.setZ(0)
    def hit(self, ship):
        if not ship.shielded and not self.Hit:
            ship.speed -= 10/ship.size
            if ship.speed < 0:
                ship.speed = 0
            ship.health -= 20
        self.Hit = True
        self.die()
        
    def die(self):
        if not self.dead:
            self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 4, 1, self.parent.environment))
            if self.parent.environment.multiplayer:
                self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 4, 2, self.parent.environment))
            self.parent.environment.activePowerups.remove(self)
            self.dead = True
            self.cleanup()
            
    def cleanup(self):
        self.model.removeNode()
        if self.sound.status() == self.sound.PLAYING:
            self.sound.stop()
        audio3d.detachSound(self.sound)
        
class Seismic(DirectObject):
    def __init__(self, pos, parent, upgrade):
        self.target = None
        self.dead = False
        self.parent = parent
        self.upgrade = upgrade
        self.shipPlace = 0
        if not self.upgrade:
            self.time = 5

        self.otherShips = []
        for ship in self.parent.environment.allShips:
            if ship != self.parent:
                self.otherShips.append(ship)
        self.shipMax = len(self.otherShips)
        
        self.model = loader.loadModel('models/seismic')
        self.model.setPos(pos)
        self.model.setScale(0.5)
        self.model.setH(random.randrange(360))
        self.model.setR(random.randrange(360))
        self.model.setP(random.randrange(360))
        self.model.reparentTo(render)
        
        self.dh = random.randrange(40)
        self.dr = random.randrange(40)
        self.dp = random.randrange(40)
        
        self.csphere = CollisionSphere(0,0,0,0.5)
        self.csphere.setTangible(False)
        self.cnode = self.model.attachNewNode(CollisionNode('cnode'))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        
        self.sound = audio3d.loadSfx('sounds/sfx/energy.wav')
        self.sound.setLoop(True)
        audio3d.attachSoundToObject(self.sound, self.model)
        self.sound.play()
        
    def update(self):
        self.model.setH(self.model.getH() + self.dh)
        self.model.setR(self.model.getR() + self.dr)
        self.model.setP(self.model.getP() + self.dp)
        x = self.model.getX()
        y = self.model.getY()
        if not self.upgrade:
            if self.time > 0:
                self.time -= dt
            if self.time < 0:
                self.explode()
        else:
            try:
                if x > self.otherShips[self.shipPlace].ship.getX() - 30 and x < self.otherShips[self.shipPlace].ship.getX() + 30 and y > self.otherShips[self.shipPlace].ship.getY() - 30 and y < self.otherShips[self.shipPlace].ship.getY() + 30:
                    self.explode()
            except AssertionError:
                if not self.parent.environment.multiplayer:
                    self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                else:
                    foundnewShip = False
                    for ship in self.otherShips:
                        if ship == self.parent.environment.playerShip:
                            self.otherShips[self.shipPlace] = self.parent.environment.player2Ship
                            foundnewShip = True
                    if not foundnewShip:
                        for ship in self.otherShips:
                            if ship == self.parent.environment.player2Ship:
                                self.otherShips[self.shipPlace] = self.parent.environment.playerShip
                                foundnewShip = True
            else:
                self.shipPlace += 1
                if self.shipPlace == self.shipMax:
                    self.shipPlace = 0
        
    def hit(self, ship):
        if not ship.shielded:
            ship.speed -= 40/ship.size
            if ship.speed < 0:
                ship.speed = 0
            ship.health -= 80
        self.die()
        
    def explode(self):
        self.parent.environment.activePowerups.append(Shock(self.model.getPos(), self.parent))
        self.parent.environment.activePowerups.remove(self)
        self.cleanup()
            
    def die(self):
        if not self.dead:
            self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 1, self.parent.environment))
            if self.parent.environment.multiplayer:
                self.parent.environment.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 2, self.parent.environment))
            self.parent.environment.activePowerups.remove(self)
            self.dead = True
            self.cleanup()
            
    def cleanup(self):
        self.model.removeNode()
        audio3d.detachSound(self.sound)
        self.sound.stop()
            
class Shock(DirectObject):
    def __init__(self, pos, parent):
        self.target = None
        self.parent = parent
        self.time = 1
        self.hitShips = []
        
        self.model = loader.loadModel('models/shock')
        self.model.setPos(pos)
        self.model.setH(random.randrange(360))
        self.model.setScale(1)
        self.model.reparentTo(render)
        
        self.cnode = self.model.find('**/cmodel')
        
        self.sound = audio3d.loadSfx('sounds/sfx/seismic.wav')
        audio3d.attachSoundToObject(self.sound, self.model)
        self.sound.play()
        
    def update(self):
        self.model.setScale(self.model.getScale() + 25*dt)
        if self.time > 0:
            self.time -= dt
        if self.time < 0:
            self.parent.environment.activePowerups.remove(self)
            self.cleanup()
            
    def hit(self, ship):
        alreadyHit = False
        for Ship in self.hitShips:
            if Ship == ship:
                alreadyHit = True
        if not alreadyHit:
            if not ship.shielded:
                self.parent.environment.explosions.append(Explosion(ship.ship.getX(), ship.ship.getY(), ship.ship.getZ(), 5, 1, self.parent.environment))
                if self.parent.environment.multiplayer:
                    self.parent.environment.explosions.append(Explosion(ship.ship.getX(), ship.ship.getY(), ship.ship.getZ(), 5, 2, self.parent.environment))
                ship.speed -= 30/ship.size
                ship.health -= 60
                self.hitShips.append(ship)
                
    def cleanup(self):
        self.model.removeNode()
        if self.sound.status() == self.sound.PLAYING:
            self.sound.stop()
        audio3d.detachSound(self.sound)
                
class Powerup(DirectObject):
    powerups = ['boost', 'shield', 'cruise', 'rocket', 'mine', 'seismic', 'desin']
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.time = 0
        self.gone = False
        self.powerup = loader.loadModel("models/powerup")
        self.powerup.setX(x)
        self.powerup.setY(y)
        self.powerup.setZ(z)
        self.powerup.setScale(1)
        self.powerup.reparentTo(render)
        
        self.dh = 90+random.randrange(90)
        self.dp = 90+random.randrange(90)
        self.dr = 90+random.randrange(90)
        
        self.csphere = CollisionSphere(0,0,0,1.1)
        self.csphere.setTangible(False)
        self.cnode = self.powerup.attachNewNode(CollisionNode('cnode'))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        #self.cnode.show()
    def update(self, time):
        if self.gone:
            self.time += time
        if self.time > 5:
            self.gone = False
            self.time = 0
            self.powerup.show()
        self.powerup.setH(self.powerup.getH()+self.dh*dt)
        self.powerup.setP(self.powerup.getP()+self.dp*dt)
        self.powerup.setR(self.powerup.getR()+self.dr*dt)

    def giveTo(self, ship):
        if not self.gone:
            if ship.power == 'none':
                ship.power = Powerup.powerups[random.randrange(7)]
                self.gone = True
                self.powerup.hide()
                ship.powersound.play()
            elif not ship.upgrade:
                ship.upgrade = True
                self.gone = True
                self.powerup.hide()
                ship.powersound.play()
            
    def cleanup(self):
        self.powerup.removeNode()

class Powerh(DirectObject):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.time = 0
        self.gone = False
        self.powerh = loader.loadModel("models/powerhealth")
        self.powerh.setX(x)
        self.powerh.setY(y)
        self.powerh.setZ(z)
        self.powerh.setScale(1)
        self.powerh.reparentTo(render)
        
        self.dh = 90+random.randrange(90)
        self.dp = 90+random.randrange(90)
        self.dr = 90+random.randrange(90)
        
        self.csphere = CollisionSphere(0,0,0,1.1)
        self.csphere.setTangible(False)
        self.cnode = self.powerh.attachNewNode(CollisionNode('cnode'))
        self.cnode.node().addSolid(self.csphere)
        self.cnode.node().setCollideMask(collisionMask)
        #self.cnode.show()

    def update(self, time):
        if self.gone:
            self.time += time
        if self.time > 5:
            self.gone = False
            self.time = 0
            self.powerh.show()
        self.powerh.setH(self.powerh.getH()+self.dh*dt)
        self.powerh.setP(self.powerh.getP()+self.dp*dt)
        self.powerh.setR(self.powerh.getR()+self.dr*dt)
            
    def giveTo(self, ship):
        if not self.gone:
            self.gone = True
            self.powerh.hide()
            ship.health += 20
            if ship.health > ship.maxHealth:
                ship.health = ship.maxHealth
            ship.healthsound.play()
            
    def cleanup(self):
        self.powerh.removeNode()
        
class Barrier(DirectObject):
    def __init__(self, x, y, h):
        self.model = loader.loadModel('models/barrier')
        self.model.setPos(x, y, 0)
        self.model.setH(h)
        self.model.reparentTo(render)
        
    def cleanup(self):
        self.model.removeNode()

class Checkpoint(DirectObject):
    def __init__(self, x, y, z, h):
        self.check = loader.loadModel('models/checkpoint')
        self.check.setX(x)
        self.check.setY(y)
        self.check.setZ(z)
        self.check.setH(h)
        self.check.setScale(5)
        self.check.reparentTo(render)

        self.cnode = self.check.find('**/checkpointc')
        self.cFrame = self.check.find('**/checkpoint')
        
    def cleanup(self):
        self.check.removeNode()

class Startingline(DirectObject):
    def __init__(self, x, y, z, h):
        self.check = loader.loadModel('models/startingline')
        self.check.setX(x)
        self.check.setY(y)
        self.check.setZ(z)
        self.check.setH(h)
        self.check.setScale(5)
        self.check.reparentTo(render)

        self.cnode = self.check.find('**/checkpointc')
        self.cFrame = self.check.find('**/checkpoint')
        
    def cleanup(self):
        self.check.removeNode()

class Explosion(DirectObject):
    def __init__(self, x, y, z, scale, cam, environment):
        self.environment = environment
        self.cam = cam
        self.explosion = loader.loadModel('models/explosion/explosion')
        self.explosion.setTransparency(TransparencyAttrib.MDual, 1)
        self.explosion.setX(x)
        self.explosion.setY(y)
        self.explosion.setZ(z)
        self.explosion.setScale(scale)
        self.explosion.find('**/+SequenceNode').node().pose(1)
        self.explosion.find('**/+SequenceNode').node().loop(1)
        self.explosion.reparentTo(render)
        self.explosion.setShaderOff()
        self.explosion.setLightOff()
        self.time = 0

        if self.cam == 1:
            self.explosion.lookAt(base.cam)
        else:
            self.explosion.lookAt(self.environment.cam2)
            
        if self.environment.multiplayer:
            if self.cam == 1:
                self.explosion.hide(cam2Mask)
            else:
                self.explosion.hide(cam1Mask)
                
        self.sound = audio3d.loadSfx('sounds/sfx/explosion1.wav')
        audio3d.attachSoundToObject(self.sound, self.explosion)
        self.sound.setVolume(1)
        self.sound.play()

    def update(self, time):
        if self.cam == 1:
            self.explosion.lookAt(base.cam)
        else:
            self.explosion.lookAt(self.environment.cam2)
        self.time += time
        if self.time > 2:
            self.cleanup()
            
    def cleanup(self):
        self.environment.explosions.remove(self)
        self.explosion.removeNode()
        if self.sound.status() == self.sound.PLAYING:
            self.sound.stop()
        audio3d.detachSound(self.sound)
            
class Scope(DirectObject):
    def __init__(self, parent, cam, environment):
        self.environment = environment
        self.cam = cam
        self.mask = None
        self.model = None
        self.parent = parent
        self.otherships = []
        for ship in self.environment.allShips:
            if ship != self.parent:
                self.otherships.append(ship)
        self.index = 0
        self.max = len(self.otherships)
        self.lastupgrade = self.parent.upgrade
        self.parent.target = self.otherships[self.index]
        if self.environment.multiplayer:
            if self.cam == 1:
                self.mask = cam2Mask
            else:
                self.mask = cam1Mask
                
        self.sound = loader.loadSfx('sounds/sfx/targeting.wav')
        self.sound.setLoop(True)
        self.sound.setVolume(.7)

    def update(self):
        if self.parent.upgrade != self.lastupgrade:
            self.lastupgrade = self.parent.upgrade
            if self.parent.upgrade and (self.parent.power == 'rocket' or self.parent.power == 'cruise' or self.parent.power == 'desin'):
                self.model = loader.loadModel('models/target')
                self.model.setPos(self.parent.target.ship.getPos())
                self.model.setScale(10)
                self.model.reparentTo(render)
                self.model.setShaderOff()
                self.model.setLightOff()
                if self.environment.multiplayer:
                    self.model.hide(self.mask)
                self.sound.play()
            if not self.parent.upgrade and self.model is not None:
                self.model.removeNode()
                self.sound.stop()
                self.model = None
                
        if self.parent.upgrade and (self.parent.power == 'rocket' or self.parent.power == 'cruise' or self.parent.power == 'desin'):
            self.model.setX(self.parent.target.ship.getX())
            self.model.setY(self.parent.target.ship.getY())
            self.model.setZ(self.parent.target.ship.getZ())
            if self.cam == 1:
                self.model.lookAt(base.cam)
            else:
                self.model.lookAt(self.environment.cam2)
            
    def cycleUp(self):
        self.index += 1
        if self.index == self.max:
            self.index = 0
        self.parent.target = self.otherships[self.index]
        
    def cycleDown(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.max - 1
        self.parent.target = self.otherships[self.index]
        
    def cleanup(self):
        if self.model is not None:
            self.model.removeNode()
        if self.sound.status() == self.sound.PLAYING:
            self.sound.stop()
        
class Environment(DirectObject):
    def __init__(self, game, user, multiplayer, player1ship, player2ship, playWorld, playRace, numCPUs, userUpgrades, CPUUpgrades, afterRaceAction, config):
        self.game = game
        self.multiplayer = multiplayer
        self.user = user
        self.afterRaceAction = afterRaceAction
        self.config = config

        ################
        #Game variables#
        ################
        
        self.loadingbar = DirectWaitBar(text = '', range = 55, value = 0, pos = (0, 0, -.8), barColor = (0, 1, 0, 1), scale = (1, 1, .2))
        base.graphicsEngine.renderFrame()
        
        self.earth = None
        self.ships = []
        self.barriers = []
        self.powerups = []
        self.powerh = []
        self.checkpoints = []
        self.activePowerups = []
        self.explosions = []
        self.laps = 0
        self.finishPlaces = [0, 0, 0, 0, 0, 0]
        
        self.userUpgrades = userUpgrades
        self.CPUUpgrades = CPUUpgrades

        self.ambientLight = None
        self.directionalLight = None
        
        self.p1Finished = False
        self.p2Finished = False
        if not multiplayer:
            self.p2Finished = True
        
        self.p1Text = OnscreenText(text = '',
                                   fg = (1,1,1,1),
                                   pos = (0, 0.5, 0),
                                   scale = 0.07,
                                   mayChange = 1)
                                   
        self.p2Text = OnscreenText(text = '',
                                   fg = (1,1,1,1),
                                   pos = (0, -0.5, 0),
                                   scale = 0.07,
                                   mayChange = 1)
                                   
        self.Finished = False
        self.FinishedText = OnscreenText(text = 'Press space to begin!',
                                         fg = (1,1,1,1),
                                         pos = (0, 0, 0),
                                         scale = 0.07,
                                         mayChange = 1)
                                         
        self.Started = False
        self.StartText = OnscreenText(text = '',
                                      fg = (1, 1, 0, 1),
                                      pos = (0, 0, 0),
                                      scale = 0.2,
                                      mayChange = 1)
        self.startTime = -1
        
        self.places = [0,0,0,0,0,0]
        
        self.camMode = "follow"
        self.cam2Mode = "follow"
        self.cam1Back = False
        self.cam2Back = False

        #base.cTrav.showCollisions(render)
        
        ##########
        #Sound FX#
        ##########
        
        self.startSound = loader.loadSfx('sounds/sfx/start.wav')

        ###################
        #Multiplayer Setup#
        ###################

        if multiplayer:
            #cameras
            cam2node = Camera('cam2')
            self.cam2 = NodePath(cam2node)
            self.cam2.reparentTo(render)
            self.cam2.setPos(0, 0, 0)

            #display regions
            self.rtop = base.cam.node().getDisplayRegion(base.cam.node().getNumDisplayRegions()-1)
            self.rbottom = base.win.makeDisplayRegion(0, 1, 0, 0.5)
            self.rbottom.setCamera(self.cam2)
            self.rbottom.setClearDepthActive(True)
            self.rtop.setClearDepthActive(True)
            self.rtop.setDimensions(0, 1, 0.5, 1)

            #set lenses
            base.cam.node().getLens().setAspectRatio(float(self.rtop.getPixelWidth()) / float(self.rtop.getPixelHeight()))
            self.cam2.node().getLens().setAspectRatio(float(self.rbottom.getPixelWidth()) / float(self.rbottom.getPixelHeight()))
            
        global audio3d
        audio3d = Multiplayer3DAudio(self)

        #######
        #Setup#
        #######
        #base.oobe()
        self.loadingbar['value']+=1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        
        base.disableMouse()
        
        #hide mouse
        props = WindowProperties()
        props.setCursorHidden(True) 
        base.win.requestProperties(props)

        race = "race" + str(playRace)
        world = str(playWorld)

        file, filename, description = imp.find_module(race, [world])
        racemod = imp.load_module(race, file, filename, description)

        self.Race = racemod.Race(self, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades)

        self.earth.reparentTo(render)
        self.cPushNode = self.earth.find('**/cpushMesh')
        self.cDieNode = self.earth.find('**/cdieMesh')
        
        self.sky = loader.loadModel('skydomes/'+str(self.domenum))
        self.sky.setZ(-75)
        self.sky.setScale(100)
        self.sky.reparentTo(render)
        self.sky.setBin("background", 1)
        self.sky.setLightOff()
        
        for obj in self.barriers:
            obj.model.setBin("background", 1)
        
        self.ambientLightNode = render.attachNewNode(self.ambientLight)
        self.directionalLightNode = render.attachNewNode(self.directionalLight)

        render.setLight(self.ambientLightNode)
        render.setLight(self.directionalLightNode)
        
        base.cam.node().setCameraMask(cam1Mask)
        if multiplayer:
            self.cam2.node().setCameraMask(cam2Mask)

        # arrow
        self.arrow = loader.loadModel('models/arrow')
        self.arrow.reparentTo(camera)
        self.arrow.setScale(.05)
        self.arrow.setPos(0, 5, 1)
        self.arrow.hide(cam2Mask)

        if multiplayer:
            self.arrow2 = loader.loadModel('models/arrow')
            self.arrow2.reparentTo(self.cam2)
            self.arrow2.setPos(0, 5, 1)
            self.arrow2.setScale(.05)
            self.arrow2.hide(cam2Mask)

        self.allShips = []

        self.allShips.append(self.playerShip)
        if multiplayer:
            self.allShips.append(self.player2Ship)
        for ship in self.ships:
            self.allShips.append(ship)
            
        self.playerShip.scope = Scope(self.playerShip, 1, self)
        if multiplayer:
            self.player2Ship.scope = Scope(self.player2Ship, 2, self)
            
        #########
        #Loading#
        #########
        self.loadingbar['value'] += 5
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/ship1')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/ship2')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/ship3')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/ship4')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/ship5')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/ship6')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/rocket')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/cruise')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/target')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/mine')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/desinigrate')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/seismic')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/shock')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/explosion/explosion')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        
        imageloader = OnscreenImage(image = 'models/images/boost.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/boostup.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/cruise.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/cruiseup.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/desin.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/desinup.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/mine.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/mineup.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/none.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/rocket.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/rocketup.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/seismic.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/seismicup.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/shield.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.setImage('models/images/shieldup.png')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        imageloader.destroy()
        
        loader.loadSfx('sounds/sfx/checkpoint.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/cruise.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/energy.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/explosion1.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/health.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/mine.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/powerup.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/rocket.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/seismic.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/shield.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/silence.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/start.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/targeting.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/turbo.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        loader.loadSfx('sounds/sfx/turbolong.wav')
        self.loadingbar['value'] += 1
        self.game.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()

        ##########
        #Gameplay#
        ##########
        
        self.updateTask = taskMgr.add(self.controlUpdate, "update-task")

        self.accept("space", self.startStop)
        self.accept("p", self.pause)
        self.paused = False

        #player 1
        self.accept("arrow_up", self.setdir, [0, 1])
        self.accept("arrow_up-up", self.setdir, [0, 0])
        self.accept("arrow_down", self.setdir, [1, 1])
        self.accept("arrow_down-up", self.setdir, [1, 0])
        self.accept("arrow_left", self.setdir, [2, 1])
        self.accept("arrow_left-up", self.setdir, [2, 0])
        self.accept("arrow_right", self.setdir, [3, 1])
        self.accept("arrow_right-up", self.setdir, [3, 0])
        self.accept("k", self.shootp1powerup, [])
        self.accept("j", self.playerShip.scope.cycleUp, [])
        self.accept("l", self.playerShip.scope.cycleDown, [])
        self.accept("i", self.changeCam1Mode)
        self.accept("o", self.lookBack)
        self.accept("o-up", self.lookForward)

        #player 2
        self.accept("t", self.setdir2, [0, 1])
        self.accept("t-up", self.setdir2, [0, 0])
        self.accept("g", self.setdir2, [1, 1])
        self.accept("g-up", self.setdir2, [1, 0])
        self.accept("f", self.setdir2, [2, 1])
        self.accept("f-up", self.setdir2, [2, 0])
        self.accept("h", self.setdir2, [3, 1])
        self.accept("h-up", self.setdir2, [3, 0])
        self.accept("w", self.changeCam2Mode)
        self.accept("e", self.lookBack2)
        self.accept("e-up", self.lookForward2)
        if self.multiplayer:
            self.accept("a", self.player2Ship.scope.cycleUp, [])
            self.accept("d", self.player2Ship.scope.cycleDown, [])
            self.accept("s", self.shootp2powerup, [])

        self.dir = [0, 0, 0, 0]
        self.dir2 = [0, 0, 0, 0]
        
        self.time = 0
        self.lastTime = 0
        
        #bloom
        
        if self.config.getBloom():
            self.filters = CommonFilters(base.win, base.cam)
            self.filters.setBloom(blend=(0,0,0,1), desat=0, intensity=1.0, size="small")
            if self.multiplayer:
                self.filters2 = CommonFilters(base.win, self.cam2)
                self.filters2.setBloom(blend=(0,0,0,1), desat=0, intensity=1.0, size="small")
            render.setShaderAuto()
        
        #music
        self.music = loader.loadSfx('sounds/music/'+playWorld+'.mp3')
        self.music.setVolume(.7)
        self.music.setLoop(True)
        self.music.play()
        
        for ship in self.allShips:
            ship.sound.play()
            
        self.game.background.setImage('models/textures/loadingback.png') 
        self.loadingbar.finish()
        base.graphicsEngine.renderFrame()
        self.loadingbar.destroy()
        self.game.background.destroy()

    def setdir(self, btn, value):
        self.dir[btn] = value

    def setdir2(self, btn, value):
        self.dir2[btn] = value

    def controlUpdate(self, task):
        global dt
        dt = globalClock.getDt()
        #starting race
        if self.startTime > 0:
            self.startTime -= dt
        if self.startTime < 4 and self.startTime > 3:
            self.StartText.setText('3')
            if self.startSound.status() != self.startSound.PLAYING:
                self.startSound.play()
        if self.startTime < 3 and self.startTime > 2:
            self.StartText.setText('2')
        if self.startTime < 2 and self.startTime > 1:
            self.StartText.setText('1')
        if self.startTime < 1 and self.startTime > 0:
            self.StartText.setText('GO')
            self.Started = True
        if self.startTime < 0:
            if self.StartText is not None and self.Started == True:
                self.StartText.destroy()
        #explosions
        self.time = task.time - self.lastTime
        self.lastTime = task.time
        for explosion in self.explosions:
            explosion.update(self.time)
        #arrows
        if not self.p1Finished:
            self.arrow.lookAt(self.checkpoints[self.playerShip.checkPos].check)
            self.arrow.setP(0)
        if self.multiplayer and not self.p2Finished:
            self.arrow2.lookAt(self.checkpoints[self.player2Ship.checkPos].check)
            self.arrow2.setP(0)
        #ships
        if self.Started:
            if not self.p1Finished:
                self.playerShip.update(self.dir)
            if self.multiplayer and not self.p2Finished:
                self.player2Ship.update(self.dir2)
            for ship in self.ships:
                ship.update()

        #powerups
        for powerup in self.powerups:
            powerup.update(self.time)
        for powerh in self.powerh:
            powerh.update(self.time)

        #active powerups
        for powerup in self.activePowerups:
            powerup.update()
            
        #Collisions
        base.cTrav.traverse(render)
        
        #Pusher damage
        if self.Started:
            if not self.p1Finished:
                self.playerShip.checkCrashDamage()
            if self.multiplayer and not self.p2Finished:
                self.player2Ship.checkCrashDamage()
            for ship in self.ships:
                ship.checkCrashDamage()

        #camera
        
        if self.camMode == "follow":
            self.playerShip.cfloater.setPos(self.playerShip.ship.getPos())
            self.playerShip.cfloater.setZ(self.playerShip.ship.getZ() + 4)
            camvec = self.playerShip.cfloater.getPos() - base.camera.getPos()
            camdist = camvec.length()
            camvec.normalize()
            if (camdist > 15):
                base.camera.setPos(base.camera.getPos() + camvec*(camdist-15))
                camdist = 15
            self.playerShip.floater.setPos(self.playerShip.ship.getPos())
            self.playerShip.floater.setZ(self.playerShip.ship.getZ() + 3)
            base.camera.lookAt(self.playerShip.floater)
        if self.camMode == "fpv":
            base.camera.setPos(self.playerShip.ship.getPos())
            base.camera.setHpr(self.playerShip.ship.getH(), self.playerShip.ship.getP(), self.playerShip.ship.getR()/5)
        if self.cam1Back:
            if self.camMode == "follow":
                base.camera.setP(0)
                base.camera.setH(base.camera.getH()+180)
            if self.camMode == "fpv":
                base.camera.setR(0)
                base.camera.setH(base.camera.getH()+180)

        #cam2

        if self.multiplayer:
            if self.cam2Mode == "follow":
                self.player2Ship.cfloater.setPos(self.player2Ship.ship.getPos())
                self.player2Ship.cfloater.setZ(self.player2Ship.ship.getZ() + 4)
                camvec = self.player2Ship.cfloater.getPos() - self.cam2.getPos()
                camdist = camvec.length()
                camvec.normalize()
                if (camdist > 15):
                    self.cam2.setPos(self.cam2.getPos() + camvec*(camdist-15))
                    camdist = 15
                self.player2Ship.floater.setPos(self.player2Ship.ship.getPos())
                self.player2Ship.floater.setZ(self.player2Ship.ship.getZ() + 3)
                self.cam2.lookAt(self.player2Ship.floater)
            if self.cam2Mode == "fpv":
                self.cam2.setPos(self.player2Ship.ship.getPos())
                self.cam2.setHpr(self.player2Ship.ship.getH(), self.player2Ship.ship.getP(), self.player2Ship.ship.getR()/5)
            if self.cam2Back:
                if self.cam2Mode == "follow":
                    self.cam2.setP(0)
                    self.cam2.setH(self.cam2.getH()+180)
                if self.cam2Mode == "fpv":
                    self.cam2.setR(0)
                    self.cam2.setH(self.cam2.getH()+180)
                
        if self.p1Finished and self.p2Finished:                 #The race is over
            self.FinishedText.setText('Press Space to continue.')
            self.Finished = True
        
        return Task.cont
    
    def startStop(self):
        if self.Started:
            self.endGame()
        else:
            self.startTime = 5
            self.FinishedText.setText('')
            
    def shootp1powerup(self):
        self.playerShip.shootPowerup()
        
    def changeCam1Mode(self):
        if self.camMode == "follow":
            self.camMode = "fpv"
        else:
            self.camMode = "follow"
            
    def lookBack(self):
        self.cam1Back = True
        
    def lookBack2(self):
        self.cam2Back = True
        
    def lookForward(self):
        self.cam1Back = False
        
    def lookForward2(self):
        self.cam2Back = False
            
    def changeCam2Mode(self):
        if self.cam2Mode == "follow":
            self.cam2Mode = "fpv"
        else:
            self.cam2Mode = "follow"
            
    def shootp2powerup(self):
        self.player2Ship.shootPowerup()
        
    def pause(self):
        if self.paused:
            base.enableAllAudio()
            try:
                self.updateTask = taskMgr.add(self.controlUpdate, "update-task")
            except:
                pass
            if self.pauseImage is not None:
                self.pauseImage.destroy()
            self.paused = False
        else:
            base.disableAllAudio()
            try:
                taskMgr.remove(self.updateTask)
            except:
                pass
            self.pauseImage = OnscreenImage(image = 'models/textures/pauseback.png',
                                            scale = (1.6, 0, 1))
            self.pauseImage.setTransparency(TransparencyAttrib.MAlpha)
            self.paused = True

    def endGame(self):
        #cleanup
        for ship in self.allShips:
            ship.cleanup()
        for barrier in self.barriers:
            barrier.cleanup()
        for power in self.powerh:
            power.cleanup()
        for power in self.powerups:
            power.cleanup()
        for checkpoint in self.checkpoints:
            checkpoint.cleanup()
        for power in self.activePowerups:
            power.cleanup()
        for explosion in self.explosions:
            explosion.cleanup()
        self.earth.removeNode()
        self.sky.removeNode()
        if not self.p1Finished:
            self.arrow.removeNode()
        if self.multiplayer and not self.p2Finished:
            self.arrow2.removeNode()
        
        render.clearLight(self.ambientLightNode)
        render.clearLight(self.directionalLightNode)
        self.ambientLightNode.removeNode()
        self.directionalLightNode.removeNode()
        
        if self.config.getBloom():
            self.filters.cleanup()
            if self.multiplayer:
                self.filters2.cleanup()
            render.setShaderOff()
        
        if self.multiplayer:
            base.win.removeDisplayRegion(self.rbottom)
            self.rtop.setDimensions(0, 1, 0, 1)
            base.cam.node().getLens().setAspectRatio(float(self.rtop.getPixelWidth()) / float(self.rtop.getPixelHeight()))
            self.cam2.removeNode()

        props = WindowProperties()
        props.setCursorHidden(False) 
        base.win.requestProperties(props)
        
        if not self.paused:
            taskMgr.remove(self.updateTask)
        else:
            self.pauseImage.destroy()
        
        self.music.stop()
        
        text = ''
        if self.afterRaceAction == 'usermenu' and self.Finished:
            text = 'Click Replay Race to play again, or\nclick Continue to return to menu.'
        elif self.afterRaceAction == 'careermenu' and self.Finished:
            text = self.p1Text.getText()
        else:
            text = 'Race was not finished'
        self.p1Text.destroy()
        self.p2Text.destroy()
        self.FinishedText.destroy()
        
        if self.afterRaceAction == 'careermenu' and self.places[0] >= 1 and self.Finished:
            self.Finished = False
        
        self.FinishCredits = self.Race.finishCredits
        
        self.ignoreAll()
        self.game.afterRace(self.afterRaceAction, text, self.Finished, self.FinishCredits, self.places)