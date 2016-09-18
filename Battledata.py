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
    def __init__(self, battle):
        self.battle = battle
        self.audio3d1 = Audio3DManager.Audio3DManager(base.sfxManagerList[0], base.cam)
        self.audio3d2 = Audio3DManager.Audio3DManager(base.sfxManagerList[0], self.battle.cam2)
        
    def loadSfx(self, path):
        return self.audio3d1.loadSfx(path)
    
    def attachSoundToObject(self, sound, object):
        self.audio3d1.attachSoundToObject(sound, object)
        self.audio3d2.attachSoundToObject(sound, object)
        
    def detachSound(self, sound):
        self.audio3d1.detachSound(sound)
        self.audio3d2.detachSound(sound)

class Ship(DirectObject):
    def __init__(self, modelnum, x, y, z, h, battle, shipnum):
        self.name = 'user'
        self.dist = 0
        self.shielded = False
        self.shieldTime = 0
        self.battle = battle
        self.target = None
        self.scope = None
        self.lastPower = 'none'
        self.power = 'none'
        
        self.maxHealth = 250
        self.health = self.maxHealth
        self.MaxSpeed = 50
        self.maxSpeed = self.MaxSpeed
        self.accelFact = 0.5
        self.turnFact = 5
            
        self.upgrade = False
        self.lastupgrade = self.upgrade
        self.powerSymbol = OnscreenImage(image = 'models/images/none.png',
                                        pos = (-1.2,0,-0.8),
                                        scale = (0.2, 1, 0.2))
        self.powerSymbol.setTransparency(TransparencyAttrib.MAlpha)
        self.boostTime = 0
        self.dead = False
        self.shipnum = shipnum
        self.modelnum = modelnum
                                    
        self.pos = 1
        self.postext = str(self.pos)
        if self.pos == 1:
            self.postext += 'st'
        elif self.pos == 2:
            self.postext += 'nd'
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
            self.posText.setPos(1, -0.2)
        if self.shipnum == 1:
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
        
        # sounds
        
        self.sound = audio3d.loadSfx('sounds/sfx/engine' + str(modelnum) + '.wav')
        audio3d.attachSoundToObject(self.sound, self.ship)
        self.sound.setLoop(True)
        self.sound.setPlayRate(0.5)
        self.sound.setVolume(0.8)
        #self.sound.play()     Handled by battle
        
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

    def update(self, dir):
        self.dead = False
        self.scope.update()
        
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
        
        if not self.battle.Finished:
            if self.shipnum == 1:
                if self.battle.player2Ship.health <= self.health:
                    self.posText.setText('1st')
                else:
                    self.posText.setText('2nd')
            else:
                if self.battle.playerShip.health < self.health:
                    self.posText.setText('1st')
                else:
                    self.posText.setText('2nd')
        
        self.prePos = self.ship.getPos()
        
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
        
        self.dPos = self.ship.getPos()

        #die if health is low
        if self.health <= 0:
            self.die()

    def handleCollision(self, collEntry):
        otherObjNodePath = collEntry.getIntoNodePath()
        activePowerups = self.battle.activePowerups
        powerups = self.battle.powerups
        for powerup in powerups:
            if powerup.cnode == otherObjNodePath:
                #print 'Colliding with powerup'
                powerup.giveTo(self)
                return
        for powerup in activePowerups:
            if powerup.cnode == otherObjNodePath:
                #print 'Colliding with active powerup'
                if powerup.parent != self:
                    powerup.hit(self)
                return
        
    def die(self):
        if not self.dead:
            self.battle.explosions.append(Explosion(self.ship.getX(), self.ship.getY(), self.ship.getZ(), 10, 1, self.battle))
            self.battle.explosions.append(Explosion(self.ship.getX(), self.ship.getY(), self.ship.getZ(), 10, 2, self.battle))
            if self.shipnum == 1:
                self.battle.player1Dead = True
                self.battle.p1Text.setText('Too bad, you lost.')
                self.battle.p2Text.setText('Congratulations, you won!')
            else:
                self.battle.player2Dead = True
                self.battle.p2Text.setText('Too bad, you lost.')
                self.battle.p1Text.setText('Congratulations, you won!')
            self.dead = True
            self.cleanup()

    def shootPowerup(self):
        if self.power == 'rocket':
            if self.shipnum == 1 and self.battle.cam1Back:
                self.battle.activePowerups.append(Rocket(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            elif self.shipnum == 2 and self.battle.cam2Back:
                self.battle.activePowerups.append(Rocket(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            else:
                self.battle.activePowerups.append(Rocket(self.ship.getPos(), self.ship.getH(), self, self.upgrade, self.target))
            
        if self.power == 'cruise':
            if self.shipnum == 1 and self.battle.cam1Back:
                self.battle.activePowerups.append(Cruise(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            elif self.shipnum == 2 and self.battle.cam2Back:
                self.battle.activePowerups.append(Cruise(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            else:
                self.battle.activePowerups.append(Cruise(self.ship.getPos(), self.ship.getH(), self, self.upgrade, self.target))
            
        if self.power == 'desin':
            if self.shipnum == 1 and self.battle.cam1Back:
                self.battle.activePowerups.append(Desin(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            elif self.shipnum == 2 and self.battle.cam2Back:
                self.battle.activePowerups.append(Desin(self.ship.getPos(), self.ship.getH()+180, self, self.upgrade, self.target))
            else:
                self.battle.activePowerups.append(Desin(self.ship.getPos(), self.ship.getH(), self, self.upgrade, self.target))
            
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
            self.battle.activePowerups.append(Mine(self.ship.getPos(), self))
            if self.upgrade:
                self.battle.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY()+5, self.ship.getZ()), self))
                self.battle.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY(), self.ship.getZ()), self))
                self.battle.activePowerups.append(Mine((self.ship.getX()+5, self.ship.getY()-5, self.ship.getZ()), self))
                self.battle.activePowerups.append(Mine((self.ship.getX(), self.ship.getY()+5, self.ship.getZ()), self))
                self.battle.activePowerups.append(Mine((self.ship.getX(), self.ship.getY()-5, self.ship.getZ()), self))
                self.battle.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY()+5, self.ship.getZ()), self))
                self.battle.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY(), self.ship.getZ()), self))
                self.battle.activePowerups.append(Mine((self.ship.getX()-5, self.ship.getY()-5, self.ship.getZ()), self))
            
        if self.power == 'seismic':
            self.battle.activePowerups.append(Seismic(self.ship.getPos(), self, self.upgrade))
            
        #powerup cleanup
        self.power = 'none'
        self.upgrade = False
        self.lastupgrade = False
        
    def checkCrashDamage(self):
        self.dfloater.setPos(self.dPos)
        dist = self.ship.getDistance(self.dfloater)
        if dist != 0:
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
            for ship in self.parent.battle.ships:
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
        if otherObjNodePath == self.parent.battle.cPushNode or otherObjNodePath == self.parent.battle.cDieNode:
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
                self.die()
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
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 1, self.parent.battle))
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 2, self.parent.battle))
            self.model.removeNode()
            self.parent.battle.activePowerups.remove(self)
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
            for ship in self.parent.battle.ships:
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
        if otherObjNodePath == self.parent.battle.cPushNode or otherObjNodePath == self.parent.battle.cDieNode:
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
                self.die()
            
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
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 1, self.parent.battle))
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 2, self.parent.battle))
            self.model.removeNode()
            self.parent.battle.activePowerups.remove(self)
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
            for ship in self.parent.battle.ships:
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
        if otherObjNodePath == self.parent.battle.cPushNode or otherObjNodePath == self.parent.battle.cDieNode:
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
                self.die()
            self.model.lookAt((px, py, 5))
            self.model.setH(self.model.getH() + 180)
            self.model.setP(-self.model.getP())

    def die(self):
        if not self.dead:
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 1, self.parent.battle))
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 8, 2, self.parent.battle))
            self.model.removeNode()
            self.parent.battle.activePowerups.remove(self)
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
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 4, 1, self.parent.battle))
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 4, 2, self.parent.battle))
            self.parent.battle.activePowerups.remove(self)
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
        for ship in self.parent.battle.ships:
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
                self.die()
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
        self.parent.battle.activePowerups.append(Shock(self.model.getPos(), self.parent))
        self.parent.battle.activePowerups.remove(self)
        self.cleanup()
            
    def die(self):
        if not self.dead:
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 1, self.parent.battle))
            self.parent.battle.explosions.append(Explosion(self.model.getX(), self.model.getY(), self.model.getZ(), 5, 2, self.parent.battle))
            self.parent.battle.activePowerups.remove(self)
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
            self.parent.battle.activePowerups.remove(self)
            self.cleanup()
            
    def hit(self, ship):
        alreadyHit = False
        for Ship in self.hitShips:
            if Ship == ship:
                alreadyHit = True
        if not alreadyHit:
            if not ship.shielded:
                self.parent.battle.explosions.append(Explosion(ship.ship.getX(), ship.ship.getY(), ship.ship.getZ(), 5, 1, self.parent.battle))
                self.parent.battle.explosions.append(Explosion(ship.ship.getX(), ship.ship.getY(), ship.ship.getZ(), 5, 2, self.parent.battle))
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

class Explosion(DirectObject):
    def __init__(self, x, y, z, scale, cam, battle):
        self.battle = battle
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
            self.explosion.lookAt(self.battle.cam2)
            
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
            self.explosion.lookAt(self.battle.cam2)
        self.time += time
        if self.time > 2:
            self.cleanup()
            
    def cleanup(self):
        self.battle.explosions.remove(self)
        self.explosion.removeNode()
        if self.sound.status() == self.sound.PLAYING:
            self.sound.stop()
        audio3d.detachSound(self.sound)
            
class Scope(DirectObject):
    def __init__(self, parent, cam, battle):
        self.battle = battle
        self.cam = cam
        self.mask = None
        self.model = None
        self.parent = parent
        self.otherships = []
        for ship in self.battle.ships:
            if ship != self.parent:
                self.otherships.append(ship)
        self.index = 0
        self.max = len(self.otherships)
        self.lastupgrade = self.parent.upgrade
        self.parent.target = self.otherships[self.index]
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
                self.model.lookAt(self.battle.cam2)
            
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
        
class Battle(DirectObject):
    def __init__(self, game, user, player1ship, player2ship, playWorld, afterRaceAction, config):
        self.game = game
        self.afterRaceAction = afterRaceAction
        self.config = config

        ################
        #Game variables#
        ################
        
        self.loadingbar = DirectWaitBar(text = '', range = 55, value = 0, pos = (0, 0, -.8), barColor = (0, 1, 0, 1), scale = (1, 1, .2))
        base.graphicsEngine.renderFrame()

        self.earth = None
        self.powerups = []
        self.activePowerups = []
        self.explosions = []

        self.ambientLight = None
        self.directionalLight = None
        
        self.player1Dead = False
        self.player2Dead = False
        
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
                
        self.camMode = "follow"
        self.cam2Mode = "follow"
        self.cam1Back = False
        self.cam2Back = False
        
        ##########
        #Sound FX#
        ##########
        
        self.startSound = loader.loadSfx('sounds/sfx/start.wav')

        ###################
        #Multiplayer Setup#
        ###################

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
        
        race = 'battle'
        world = str(playWorld)

        file, filename, description = imp.find_module(race, [world])
        racemod = imp.load_module(race, file, filename, description)

        self.Race = racemod.Race(self, user, player1ship, player2ship)

        self.earth.reparentTo(render)
        self.cPushNode = self.earth.find('**/cpushMesh')
        self.cDieNode = self.earth.find('**/cdieMesh')
        if world != 'championship':
            self.sky = loader.loadModel('skydomes/3')
        else:
            self.sky = loader.loadModel('skydomes/7')
        self.sky.setZ(-75)
        self.sky.setScale(100)
        self.sky.reparentTo(render)
        self.sky.setBin("background", 1)
        self.sky.setLightOff()
        
        self.ambientLightNode = render.attachNewNode(self.ambientLight)
        self.directionalLightNode = render.attachNewNode(self.directionalLight)

        render.setLight(self.ambientLightNode)
        render.setLight(self.directionalLightNode)
        
        base.cam.node().setCameraMask(cam1Mask)
        self.cam2.node().setCameraMask(cam2Mask)

        # arrow
        self.arrow = NodePath(PandaNode("floater"))
        self.arrow.reparentTo(camera)
        self.arrow.setPos(0, 5, 1)
        
        self.compass = loader.loadModel('models/arrowflat')
        self.compass.setLightOff()
        self.compass.reparentTo(camera)
        self.compass.setPos(0, 5, 1)
        self.compass.setScale(0.1)
        self.compass.hide(cam2Mask)

        self.arrow2 = NodePath(PandaNode("floater"))
        self.arrow2.reparentTo(self.cam2)
        self.arrow2.setPos(0, 5, 1)
        
        self.compass2 = loader.loadModel('models/arrowflat')
        self.compass2.setLightOff()
        self.compass2.reparentTo(self.cam2)
        self.compass2.setPos(0, 5, 1)
        self.compass2.setScale(0.1)
        self.compass2.hide(cam1Mask)

        self.ships = []

        self.ships.append(self.playerShip)
        self.ships.append(self.player2Ship)
            
        self.playerShip.scope = Scope(self.playerShip, 1, self)
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
            self.filters2 = CommonFilters(base.win, self.cam2)
            self.filters2.setBloom(blend=(0,0,0,1), desat=0, intensity=1.0, size="small")
            render.setShaderAuto()
        
        #music
        self.music = loader.loadSfx('sounds/music/'+playWorld+'.mp3')
        self.music.setVolume(.7)
        self.music.setLoop(True)
        self.music.play()
        
        for ship in self.ships:
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
        if not (self.player1Dead or self.player2Dead):
            self.arrow.lookAt(self.player2Ship.ship)
            self.arrow.setP(0)
            self.compass.setR(base.camera, -self.arrow.getH()+180)
            self.arrow2.lookAt(self.playerShip.ship)
            self.arrow2.setP(0)
            self.compass2.setR(self.cam2, -self.arrow2.getH()+180)
        #ships
        if self.Started:
            if not self.player1Dead:
                if not self.player2Dead:
                    self.playerShip.update(self.dir)
                else:
                    self.playerShip.update([0, 0, 0, 0])
            if not self.player2Dead:
                if not self.player1Dead:
                    self.player2Ship.update(self.dir2)
                else:
                    self.player2Ship.update([0, 0, 0, 0])

        #powerups
        for powerup in self.powerups:
            powerup.update(self.time)

        #active powerups
        for powerup in self.activePowerups:
            powerup.update()
            
        #Collisions
        base.cTrav.traverse(render)
        
        #Pusher damage
        if self.Started:
            if not self.player1Dead:
                self.playerShip.checkCrashDamage()
            if not self.player2Dead:
                self.player2Ship.checkCrashDamage()

        #camera
        if not self.player1Dead:
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
        if not self.player2Dead:
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
                
        if self.player1Dead or self.player2Dead:                 #The race is over
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
        for ship in self.ships:
            ship.cleanup()
        for power in self.powerups:
            power.cleanup()
        for power in self.activePowerups:
            power.cleanup()
        for explosion in self.explosions:
            explosion.cleanup()
        self.earth.removeNode()
        self.sky.removeNode()
        self.arrow.removeNode()
        self.compass.removeNode()
        self.arrow2.removeNode()
        self.compass2.removeNode()
        
        render.clearLight(self.ambientLightNode)
        render.clearLight(self.directionalLightNode)
        self.ambientLightNode.removeNode()
        self.directionalLightNode.removeNode()
        
        if self.config.getBloom():
            self.filters.cleanup()
            self.filters2.cleanup()
            render.setShaderOff()
        
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
            text = 'Battle was not finished'
        self.p1Text.destroy()
        self.p2Text.destroy()
        self.FinishedText.destroy()
        
        if self.afterRaceAction == 'careermenu' and self.places[0] >= 1 and self.Finished:
            self.Finished = False
        
        self.ignoreAll()
        self.game.afterRace(self.afterRaceAction, text, self.Finished, 0, None)