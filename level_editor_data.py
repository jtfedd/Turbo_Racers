from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import *
from direct.gui.DirectGui import *
import sys, os, math, imp
from operator import attrgetter

ratio = base.camLens.getAspectRatio()    # a little quick variable for making button placement easier

# key values
# camera
a = 0
s = 1
d = 2
w = 3
f = 4
g = 5
h = 6
t = 7
z = 8
x = 9
# terrain
j = 10
k = 11
l = 12
i = 13
# placement arrow
n = 14
m = 15
la = 16
ra = 17
ua = 18
da = 19
# misc.
ctrl = 20
enter = 21
backspace = 22

dt = globalClock.getDt()

ships = 0
checkpoints = 0
waypoints = 0

class setupShip(DirectObject):
    def __init__(self, x, y, num, h):
        self.model = loader.loadModel('models/ship2')
        self.model.setX(x)
        self.model.setY(y)
        self.model.setZ(5)
        self.model.setH(h)
        self.model.reparentTo(render)
        
        if num == None:
            global ships
            self.num = ships
            ships += 1
        else:
            self.num = num
        
        self.numlabel = None
        self.numentry = None
        
    def getNum(self):
        self.numlabel = OnscreenText(text = "Ship number:",
                                     scale = 0.07,
                                     fg = (1,1,1,1),
                                     pos = (-.2*ratio, 0, 0))
        self.numentry = DirectEntry(text = "",
                                    scale=.07,
                                    command=self.setNum,
                                    initialText=str(self.num), 
                                    numLines = 1,
                                    pos = (0,0,0),
                                    focus = 0, 
                                    frameColor = (0.5,0.5,0.5,1), 
                                    text_fg = (1,1,1,1), 
                                    suppressKeys=1, 
                                    rolloverSound = None, 
                                    clickSound = None)
                                    
    def setNum(self, numText):
        if numText == "":
            numText = "0"
        self.numlabel.destroy()
        self.numentry.destroy()
        self.num = int(numText)
        
    def delete(self, editor):
        self.model.removeNode()
        if self.numlabel is not None:
            self.numlabel.destroy()
            self.numentry.destroy()
        editor.ships.remove(self)
        
class setupPowerup(DirectObject):
    def __init__(self, x, y):
        self.model = loader.loadModel('models/powerup')
        self.model.setX(x)
        self.model.setY(y)
        self.model.setZ(5)
        self.model.reparentTo(render)
        
    def delete(self, editor):
        self.model.removeNode()
        editor.powerups.remove(self)

class setupPowerh(DirectObject):
    def __init__(self, x, y):
        self.model = loader.loadModel('models/powerhealth')
        self.model.setX(x)
        self.model.setY(y)
        self.model.setZ(5)
        self.model.reparentTo(render)
        
    def delete(self, editor):
        self.model.removeNode()
        editor.powerh.remove(self)
        
class setupCheckpoint(DirectObject):
    def __init__(self, x, y, h, checknum, waynum):
        self.model = loader.loadModel('models/checkpoint')
        self.model.setX(x)
        self.model.setY(y)
        self.model.setZ(0)
        self.model.setH(h)
        self.model.setScale(5)
        self.model.reparentTo(render)
        
        if checknum == None:
            global checkpoints
            self.checkNum = checkpoints
            checkpoints += 1
        else:
            self.checkNum = checknum
        if waynum == None:
            global waypoints
            self.wayNum = waypoints
            waypoints += 1
        else:
            self.wayNum = waynum
            
        self.checklabel = None
        self.waylabel = None
        
    def getCheckNum(self):
        self.checklabel = OnscreenText(text = "Checkpoint number:",
                                       scale = 0.07,
                                       fg = (1,1,1,1),
                                       pos = (-.2*ratio, 0))
        self.checkentry = DirectEntry(text = "" ,
                                      scale=.07,
                                      command=self.setCheckNum,
                                      initialText=str(self.checkNum), 
                                      numLines = 1,
                                      pos = (0,0,0),
                                      focus = 0, 
                                      frameColor = (0.5,0.5,0.5,1), 
                                      text_fg = (1,1,1,1), 
                                      suppressKeys=1, 
                                      rolloverSound = None, 
                                      clickSound = None)
                                    
    def setCheckNum(self, numText):
        if numText == "":
            numText = "0"
        self.checklabel.destroy()
        self.checkentry.destroy()
        self.checkNum = int(numText)
        
    def getWayNum(self):
        self.waylabel = OnscreenText(text = "AI Waypoint number:",
                                     scale = 0.07,
                                     fg = (1,1,1,1),
                                     pos = (-.2*ratio, -.1))
        self.wayentry = DirectEntry(text = "" ,
                                    scale=.07,
                                    command=self.setWayNum,
                                    initialText=str(self.wayNum), 
                                    numLines = 1,
                                    pos = (0,0,-.1),
                                    focus = 0, 
                                    frameColor = (0.5,0.5,0.5,1), 
                                    text_fg = (1,1,1,1), 
                                    suppressKeys=1, 
                                    rolloverSound = None, 
                                    clickSound = None)
                                    
    def setWayNum(self, numText):
        if numText == "":
            numText = "0"
        self.waylabel.destroy()
        self.wayentry.destroy()
        self.wayNum = int(numText)
        
    def delete(self, editor):
        self.model.removeNode()
        if self.waylabel is not None:
            self.waylabel.destroy()
            self.wayentry.destroy()
        if self.checklabel is not None:
            self.checklabel.destroy()
            self.checkentry.destroy()
        editor.checkpoints.remove(self)
    
class setupStartingline(DirectObject):
    def __init__(self, x, y, h):
        self.model = loader.loadModel('models/startingline')
        self.model.setX(x)
        self.model.setY(y)
        self.model.setZ(0)
        self.model.setH(h)
        self.model.setScale(5)
        self.model.reparentTo(render)
        
    def delete(self):
        self.model.removeNode()
        
class setupWaypoint(DirectObject):
    def __init__(self, x, y, num):
        self.model = loader.loadModel('models/waypoint')
        self.model.setZ(5)
        self.model.setX(x)
        self.model.setY(y)
        self.model.reparentTo(render)
        
        self.numlabel = None
        self.numentry = None
        
        if num == None:
            global waypoints
            self.num = waypoints
            waypoints += 1
        else:
            self.num = num
        
    def getWayNum(self):
        self.numlabel = OnscreenText(text = "AI Waypoint number:",
                                     scale = 0.07,
                                     fg = (1,1,1,1),
                                     pos = (-.2*ratio, 0, 0))
        self.numentry = DirectEntry(text = "" ,
                                    scale=.07,
                                    command=self.setWayNum,
                                    initialText=str(self.num), 
                                    numLines = 1,
                                    pos = (0,0,0),
                                    focus = 0, 
                                    frameColor = (0.5,0.5,0.5,1), 
                                    text_fg = (1,1,1,1), 
                                    suppressKeys=1, 
                                    rolloverSound = None, 
                                    clickSound = None)
                                    
    def setWayNum(self, numText):
        if numText == "":
            numText = "0"
        self.numlabel.destroy()
        self.numentry.destroy()
        self.num = int(numText)
        
    def delete(self, list):             #list special for waypoints
        self.model.removeNode()
        if self.numlabel is not None:
            self.numlabel.destroy()
            self.numentry.destroy()
        list.remove(self)
        
class setupBarrier(DirectObject):
    def __init__(self, x, y, h):
        self.model = loader.loadModel('models/barrier')
        self.model.setPos(x, y, 0)
        self.model.setH(h)
        self.model.reparentTo(render)
        
    def delete(self, editor):
        self.model.removeNode()
        editor.barriers.remove(self)

class Editor(DirectObject):
    def __init__(self):
        base.disableMouse()
        self.silence = loader.loadSfx('sounds/sfx/silence.wav')           # DirectOptionMenu cannot have sound set to none, so set it to silence.
        self.keys = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]           # There are a lot of keys!
        self.setupKeys()                # There enough key events to make them their own function for code readability's sake
        
        self.updateTask = taskMgr.add(self.controlUpdate, "update-task")
        
        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor(Vec4(.3, .3, .3, 1))
        self.ambientLightNode = render.attachNewNode(self.ambientLight)
        render.setLight(self.ambientLightNode)
        
        self.directionalLight = DirectionalLight("directionalLight")
        self.directionalLight.setDirection(Vec3(-5, -5, -5))
        self.directionalLight.setColor(Vec4(1, 1, 1, 1))
        self.directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        self.directionalLightNode = render.attachNewNode(self.directionalLight)
        render.setLight(self.directionalLightNode)
        
        self.arrow = loader.loadModel('models/ship2')
        self.arrow.reparentTo(render)
        self.arrow.setZ(5)
        
        self.terrain = None
        self.tpath = None
        
        self.ships = []
        self.barriers = []
        self.powerups = []
        self.powerh = []
        self.checkpoints = []
        self.waypoints = []
        self.startingline = None
        
        self.laps = 0
        self.minPlace = 0
        self.bgr = .4
        self.bgg = .4
        self.bgb = .4
        self.winCredits = 0
        
        self.Race = ''
        self.World = ''
        
        # Buttons
        
        self.setupButtons()
        
        # Terrain options
        self.tlabel = OnscreenText(text = "Terrain path:",
                                   scale = 0.07,
                                   fg = (1,1,1,1),
                                   pos = (-.5*ratio, -.9))
        self.tentry = DirectEntry(text = "" ,
                                  scale=.07,
                                  command=self.loadTerrain,
                                  initialText="", 
                                  numLines = 2,
                                  pos = (-.3*ratio,0,-.9),
                                  focus = 0, 
                                  frameColor = (0.5,0.5,0.5,1), 
                                  text_fg = (1,1,1,1), 
                                  suppressKeys=1, 
                                  rolloverSound = None, 
                                  clickSound = None)
                                               
        # Lighting options
        self.llabel1 = OnscreenText(text = "Ambient light brightness:",
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (-.6*ratio, -.8))
        self.llabel2 = OnscreenText(text = "Directional light brightness:",
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (-.6*ratio, -.9))
        self.lslider1 = DirectSlider(scale = .5, 
                                     range = (0, 1), 
                                     value = .3, 
                                     pos = (0, 0, -.8), 
                                     command = self.updateValues)
        self.lslider2 = DirectSlider(scale = .5,
                                     range = (0, 1),
                                     value = 1,
                                     pos = (0, 0, -.9),
                                     command = self.updateValues,
                                     thumb_rolloverSound = None,
                                     thumb_clickSound = None)
                                     
        # Settings options
        self.slabel1 = OnscreenText(text = "Laps:",
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (-.8*ratio, -.8))
        self.slabel2 = OnscreenText(text = "Minimum finish place:",
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (-.7*ratio, -.9))
        self.slabel3 = OnscreenText(text = "Credits for winning:",
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (.2*ratio, -.9))
        self.slabel5 = OnscreenText(text = "Race:",
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (-.8*ratio, -.6))
        self.slabel6 = OnscreenText(text = "World:",
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (-.8*ratio, -.7))
        self.sentry1 = DirectEntry(text = "" ,
                                   scale=.07,
                                   command=self.setLaps,
                                   initialText="0", 
                                   numLines = 1,
                                   pos = (-.7*ratio,0,-.8),
                                   focus = 0, 
                                   frameColor = (0.5,0.5,0.5,1), 
                                   text_fg = (1,1,1,1), 
                                   suppressKeys=1, 
                                   rolloverSound = None, 
                                   clickSound = None)
        self.sentry2 = DirectEntry(text = "" ,
                                   scale=.07,
                                   command=self.setMinPlace,
                                   initialText="0", 
                                   numLines = 1,
                                   pos = (-.45*ratio,0,-.9),
                                   focus = 0, 
                                   frameColor = (0.5,0.5,0.5,1), 
                                   text_fg = (1,1,1,1), 
                                   suppressKeys=1, 
                                   rolloverSound = None, 
                                   clickSound = None)
        self.sentry3 = DirectEntry(text = "" ,
                                   scale=.07,
                                   command=self.setWinCredits,
                                   initialText="0", 
                                   numLines = 1,
                                   pos = (.43*ratio,0,-.9),
                                   focus = 0, 
                                   frameColor = (0.5,0.5,0.5,1), 
                                   text_fg = (1,1,1,1), 
                                   suppressKeys=1, 
                                   rolloverSound = None, 
                                   clickSound = None)
        self.sentry4 = DirectEntry(text = "" ,
                                   scale=.07,
                                   command=self.setRace,
                                   initialText="", 
                                   numLines = 1,
                                   pos = (-.7*ratio,0,-.6),
                                   focus = 0, 
                                   frameColor = (0.5,0.5,0.5,1), 
                                   text_fg = (1,1,1,1), 
                                   suppressKeys=1, 
                                   rolloverSound = None, 
                                   clickSound = None)
        self.sentry5 = DirectEntry(text = "" ,
                                   scale=.07,
                                   command=self.setWorld,
                                   initialText="", 
                                   numLines = 1,
                                   pos = (-.7*ratio,0,-.7),
                                   focus = 0, 
                                   frameColor = (0.5,0.5,0.5,1), 
                                   text_fg = (1,1,1,1), 
                                   suppressKeys=1, 
                                   rolloverSound = None, 
                                   clickSound = None)
        self.slabel4 = OnscreenText(text = 'Background color:',
                                    scale = 0.07,
                                    fg = (1,1,1,1),
                                    pos = (.2*ratio, -.56))
        self.sslider1 = DirectSlider(scale = .5, range = (0, 1), value = self.bgr, pos = (.2*ratio, 0, -.62), command = self.updateValues)
        self.sslider2 = DirectSlider(scale = .5, range = (0, 1), value = self.bgg, pos = (.2*ratio, 0, -.7), command = self.updateValues)
        self.sslider3 = DirectSlider(scale = .5, range = (0, 1), value = self.bgb, pos = (.2*ratio, 0, -.78), command = self.updateValues)
        self.sColors = OnscreenImage(image = 'models/textures/rgb.png',
                                     pos = (-.15*ratio, 0, -.7),
                                     scale = (.04, 1, .12))
        self.sColors.setTransparency(TransparencyAttrib.MAlpha)
                                     
        self.alightBrightness = .3
        self.dlightBrightness = 1
        
        self.tlabel.hide()
        self.tentry.hide()
        self.llabel1.hide()
        self.llabel2.hide()
        self.lslider1.hide()
        self.lslider2.hide()
        self.slabel1.hide()
        self.slabel2.hide()
        self.slabel3.hide()
        self.slabel4.hide()
        self.slabel5.hide()
        self.slabel6.hide()
        self.sentry1.hide()
        self.sentry2.hide()
        self.sentry3.hide()
        self.sentry4.hide()
        self.sentry5.hide()
        self.sslider1.hide()
        self.sslider2.hide()
        self.sslider3.hide()
        self.sColors.hide()
        
        self.toptions = False
        self.loptions = False
        self.soptions = False
        
    def controlUpdate(self, task):
        # Central task to coordinate everything that runs frame-by-frame
        global dt
        dt = globalClock.getDt()
        
        # Camera
        # Speed of movement: dependant on Ctrl
        speed = 10
        if self.keys[ctrl] == 1:
            speed = 50
        speed *= dt
        # Set location based on keys
        if self.keys[a] == 1:
            base.camera.setX(base.camera.getX()-speed)
        if self.keys[d] == 1:
            base.camera.setX(base.camera.getX()+speed)
        if self.keys[s] == 1:
            base.camera.setY(base.camera.getY()-speed)
        if self.keys[w] == 1:
            base.camera.setY(base.camera.getY()+speed)
        if self.keys[z] == 1:
            base.camera.setZ(base.camera.getZ()-speed)
        if self.keys[x] == 1:
            base.camera.setZ(base.camera.getZ()+speed)
        # Set orientation based on keys
        if self.keys[f] == 1:
            base.camera.setH(base.camera.getH()+speed)
        if self.keys[h] == 1:
            base.camera.setH(base.camera.getH()-speed)
        if self.keys[t] == 1:
            base.camera.setP(base.camera.getP()+speed)
        if self.keys[g] == 1:
            base.camera.setP(base.camera.getP()-speed)
            
        # Arrow: uses same speed as camera
        if self.keys[la] == 1:
            self.arrow.setX(self.arrow.getX()-speed)
        if self.keys[ra] == 1:
            self.arrow.setX(self.arrow.getX()+speed)
        if self.keys[da] == 1:
            self.arrow.setY(self.arrow.getY()-speed)
        if self.keys[ua] == 1:
            self.arrow.setY(self.arrow.getY()+speed)
        if self.keys[n] == 1:
            self.arrow.setH(self.arrow.getH()+speed)
        if self.keys[m] == 1:
            self.arrow.setH(self.arrow.getH()-speed)
            
        if self.terrain is not None:
            if self.keys[j] == 1:
                self.terrain.setScale(self.terrain.getScale()-speed)
            if self.keys[l] == 1:
                self.terrain.setScale(self.terrain.getScale()+speed)
            if self.keys[k] == 1:
                self.terrain.setZ(self.terrain.getZ()-(speed/10))
            if self.keys[i] == 1:
                self.terrain.setZ(self.terrain.getZ()+(speed/10))
                
        if self.keys[enter] == 1:
            self.keys[enter] = 0
            for obj in self.ships:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.getNum()
            for obj in self.checkpoints:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.getCheckNum()
                    obj.getWayNum()
            for obj in self.waypoints:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.getWayNum()
        if self.keys[backspace] == 1:
            self.keys[backspace] = 0
            for obj in self.ships:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.delete(self)
            for obj in self.barriers:
                if self.arrow.getDistance(obj.model) < 10:
                    obj.delete(self)
            for obj in self.checkpoints:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.delete(self)
            for obj in self.waypoints:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.delete(self.waypoints)
            for obj in self.powerups:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.delete(self)
            for obj in self.powerh:
                if self.arrow.getDistance(obj.model) < 5:
                    obj.delete(self)
            if self.startingline is not None:
                if self.arrow.getDistance(self.startingline.model) < 5:
                    self.startingline.delete()
                    self.startingline = None
        
        return task.cont
    
    def updateValues(self):
        self.alightBrightness = self.lslider1["value"]
        self.ambientLight.setColor(Vec4(self.alightBrightness, self.alightBrightness, self.alightBrightness, 1))
        self.dlightBrightness = self.lslider2["value"]
        self.directionalLight.setColor(Vec4(self.dlightBrightness, self.dlightBrightness, self.dlightBrightness, 1))
        self.directionalLight.setSpecularColor(Vec4(self.dlightBrightness, self.dlightBrightness, self.dlightBrightness, 1))
        self.bgr = self.sslider1["value"]
        self.bgg = self.sslider2["value"]
        self.bgb = self.sslider3["value"]
        base.setBackgroundColor(self.bgr, self.bgg, self.bgb)
        
    def setValues(self):
        self.lslider1["value"] = self.alightBrightness
        self.lslider2["value"] = self.dlightBrightness
        self.sslider1["value"] = self.bgr
        self.sslider2["value"] = self.bgg
        self.sslider3["value"] = self.bgb
        self.sentry1["text"] = str(self.laps)
        self.sentry2["text"] = str(self.minPlace)
        self.sentry3["text"] = str(self.winCredits)
    
    def showTerrain(self):
        if self.toptions:               # If options are showing, hide them
            self.tlabel.hide()
            self.tentry.hide()
            self.toptions = False
        else:                           # If options are not showing, show them
            self.tlabel.show()
            self.tentry.show()
            self.toptions = True
            
    def loadTerrain(self, path):
        self.tpath = path
        if self.terrain is not None:
            self.terrain.removeNode()
        self.terrain = loader.loadModel(path)
        self.terrain.reparentTo(render)
        
    def showLights(self):
        if self.loptions:
            self.llabel1.hide()
            self.llabel2.hide()
            self.lslider1.hide()
            self.lslider2.hide()
            self.loptions = False
        else:
            self.llabel1.show()
            self.llabel2.show()
            self.lslider1.show()
            self.lslider2.show()
            self.loptions = True
            
    def setLaps(self, text):
        self.laps = int(text)
    
    def setMinPlace(self, text):
        self.minPlace = int(text)
    
    def setWinCredits(self, text):
        self.winCredits = int(text)
        
    def setRace(self, text):
        self.Race = text
        
    def setWorld(self, text):
        self.World = text
        
    def placeObject(self, objText):
        if objText == "Ship":
            tempShip = setupShip(self.arrow.getX(), self.arrow.getY(), None, self.arrow.getH())
            self.ships.append(tempShip)
        if objText == "Barrier":
            tempBarrier = setupBarrier(self.arrow.getX(), self.arrow.getY(), self.arrow.getH()+90)
            self.barriers.append(tempBarrier)
        if objText == "Powerup":
            tempPower = setupPowerup(self.arrow.getX(), self.arrow.getY())
            self.powerups.append(tempPower)
        if objText == "Powerhealth":
            tempPowerh = setupPowerh(self.arrow.getX(), self.arrow.getY())
            self.powerh.append(tempPowerh)
        if objText == "Checkpoint":
            tempCheck = setupCheckpoint(self.arrow.getX(), self.arrow.getY(), self.arrow.getH(), None, None)
            self.checkpoints.append(tempCheck)
        if objText == "Startingline":
            if self.startingline is None:
                self.startingline = setupStartingline(self.arrow.getX(), self.arrow.getY(), self.arrow.getH())
        if objText == "AI Waypoint":
            tempWaypoint = setupWaypoint(self.arrow.getX(), self.arrow.getY(), None)
            self.waypoints.append(tempWaypoint)
    
    def showSettings(self):
        if self.soptions:
            self.slabel1.hide()
            self.slabel2.hide()
            self.slabel3.hide()
            self.slabel4.hide()
            self.slabel5.hide()
            self.slabel6.hide()
            self.sentry1.hide()
            self.sentry2.hide()
            self.sentry3.hide()
            self.sentry4.hide()
            self.sentry5.hide()
            self.sslider1.hide()
            self.sslider2.hide()
            self.sslider3.hide()
            self.sColors.hide()
            self.soptions = False
        else:
            self.slabel1.show()
            self.slabel2.show()
            self.slabel3.show()
            self.slabel4.show()
            self.slabel5.show()
            self.slabel6.show()
            self.sentry1.show()
            self.sentry2.show()
            self.sentry3.show()
            self.sentry4.show()
            self.sentry5.show()
            self.sslider1.show()
            self.sslider2.show()
            self.sslider3.show()
            self.sColors.show()
            self.soptions = True
    
    def setupButtons(self):
        # Helper task to move all the buttons out of the way
        self.lightsb = DirectButton(rolloverSound = None,
                                    clickSound = None,
                                    borderWidth = (0.1, 0.1),
                                    text = ("Lighting", "Lighting", "Lighting", "Lighting"),
                                    command = self.showLights,
                                    scale = 0.1,
                                    pos = (.8*ratio, 0, .24))
                                    
        self.terrainb = DirectButton(rolloverSound = None,
                                     clickSound = None,
                                     borderWidth = (0.1, 0.1),
                                     text = ("Terrain", "Terrain", "Terrain", "Terrain"),
                                     command = self.showTerrain,
                                     scale = 0.1,
                                     pos = (.8*ratio, 0, .1))
                                     
        self.settingsb = DirectButton(rolloverSound = None,
                                      clickSound = None,
                                      borderWidth = (0.1, 0.1),
                                      text = ("Settings", "Settings", "Settings", "Settings"),
                                      command = self.showSettings,
                                      scale = 0.1,
                                      pos = (.8*ratio, 0, -.02))
        
        self.saveb = DirectButton(rolloverSound = None,
                                  clickSound = None,
                                  borderWidth = (0.1, 0.1),
                                  text = ("Save", "Save", "Save", "Save"),
                                  command = self.saveSetupLevel,
                                  scale = 0.1,
                                  pos = (.8*ratio, 0, -.5))
                                     
        self.loadb = DirectButton(rolloverSound = None,
                                  clickSound = None,
                                  borderWidth = (0.1, 0.1),
                                  text = ("Load", "Load", "Load", "Load"),
                                  command = self.loadLevel,
                                  scale = 0.1,
                                  pos = (.8*ratio, 0, -.61))
                                     
        self.newb = DirectButton(rolloverSound = None,
                                 clickSound = None,
                                 borderWidth = (0.1, 0.1),
                                 text = ("New", "New", "New", "New"),
                                 command = self.new,
                                 scale = 0.1,
                                 pos = (.8*ratio, 0, -.72))
                                
        self.exportb = DirectButton(rolloverSound = None,
                                    clickSound = None,
                                    borderWidth = (0.1, 0.1),
                                    text = ("Export", "Export", "Export", "Export"),
                                    command = self.exportLevel,
                                    scale = 0.1,
                                    pos = (.8*ratio, 0, -.36))
                                 
        self.exitb = DirectButton(text = ("X", "X", "X", "X"),
                                  borderWidth = (0.1, 0.1),
                                  command = sys.exit,
                                  scale = 0.1,
                                  rolloverSound = None,
                                  clickSound = None,
                                  pos = (0.955 * ratio, 0, 0.9))
                                  
        # Objects menu
        self.objMenu = DirectOptionMenu(textMayChange = 0,
                                        items = ["Place...", "Ship", "Barrier", "Powerup", "Powerhealth", "Checkpoint", "Startingline", "AI Waypoint"],
                                        command = self.placeObject,
                                        initialitem = 0,
                                        scale = 0.1,
                                        pos = (.6*ratio, 0, -.16),
                                        rolloverSound = None,
                                        clickSound = self.silence) # This is what cannot be set to None
    def setKey(self, key, value):
        
        # Small function to set a key to its value
        self.keys[key] = value
        
    def setupKeys(self):
        # Accept key events
        # Escape
        self.accept('escape', sys.exit)
        self.accept('f1', base.screenshot, ['screenshots/'])
        
        # Camera keys
        self.accept('a', self.setKey, [a, 1])
        self.accept('a-up', self.setKey, [a, 0])
        self.accept('s', self.setKey, [s, 1])
        self.accept('s-up', self.setKey, [s, 0])
        self.accept('d', self.setKey, [d, 1])
        self.accept('d-up', self.setKey, [d, 0])
        self.accept('w', self.setKey, [w, 1])
        self.accept('w-up', self.setKey, [w, 0])
        self.accept('f', self.setKey, [f, 1])
        self.accept('f-up', self.setKey, [f, 0])
        self.accept('g', self.setKey, [g, 1])
        self.accept('g-up', self.setKey, [g, 0])
        self.accept('h', self.setKey, [h, 1])
        self.accept('h-up', self.setKey, [h, 0])
        self.accept('t', self.setKey, [t, 1])
        self.accept('t-up', self.setKey, [t, 0])
        self.accept('z', self.setKey, [z, 1])
        self.accept('z-up', self.setKey, [z, 0])
        self.accept('x', self.setKey, [x, 1])
        self.accept('x-up', self.setKey, [x, 0])
        
        # Terrain keys
        self.accept('j', self.setKey, [j, 1])
        self.accept('j-up', self.setKey, [j, 0])
        self.accept('k', self.setKey, [k, 1])
        self.accept('k-up', self.setKey, [k, 0])
        self.accept('l', self.setKey, [l, 1])
        self.accept('l-up', self.setKey, [l, 0])
        self.accept('i', self.setKey, [i, 1])
        self.accept('i-up', self.setKey, [i, 0])
        
        # Placement arrow keys
        self.accept('n', self.setKey, [n, 1])
        self.accept('n-up', self.setKey, [n, 0])
        self.accept('m', self.setKey, [m, 1])
        self.accept('m-up', self.setKey, [m, 0])
        self.accept('arrow_left', self.setKey, [la, 1])
        self.accept('arrow_left-up', self.setKey, [la, 0])
        self.accept('arrow_right', self.setKey, [ra, 1])
        self.accept('arrow_right-up', self.setKey, [ra, 0])
        self.accept('arrow_up', self.setKey, [ua, 1])
        self.accept('arrow_up-up', self.setKey, [ua, 0])
        self.accept('arrow_down', self.setKey, [da, 1])
        self.accept('arrow_down-up', self.setKey, [da, 0])
        
        # Misc.
        self.accept('space', self.setKey, [ctrl, 1])
        self.accept('space-up', self.setKey, [ctrl, 0])
        self.accept('enter', self.setKey, [enter, 1])
        self.accept('enter-up', self.setKey, [enter, 0])
        self.accept('backspace', self.setKey, [backspace, 1])
        self.accept('backspace-up', self.setKey, [backspace, 0])
        
    def new(self):
        while len(self.ships) > 0:
            for ship in self.ships:
                ship.delete(self)
        while len(self.barriers) > 0:
            for barrier in self.barriers:
                barrier.delete(self)
        while len(self.checkpoints) > 0:
            for checkpoint in self.checkpoints:
                checkpoint.delete(self)
        while len(self.waypoints) > 0:
            for waypoint in self.waypoints:
                waypoint.delete(self.waypoints)
        while len(self.powerups) > 0:
            for powerup in self.powerups:
                powerup.delete(self)
        while len(self.powerh) > 0:
            for powerh in self.powerh:
                powerh.delete(self)
        if self.startingline is not None:
            self.startingline.delete()
            self.startingline = None
        
        self.laps = 0
        self.minPlace = 0
        self.winCredits = 0
        
    def loadLevel(self):
        self.new()
        
        race = "race"+self.Race+"setup"
        world = self.World
        
        file, filename, description = imp.find_module(race, [world])
        racemod = imp.load_module(race, file, filename, description)
        
        self.Setup = racemod.RaceSetup(self)
        
    def saveSetupLevel(self):
        file = open(self.World+'/race'+self.Race+'setup.py', 'w')
        
        file.write('from pandac.PandaModules import *\n')
        file.write('from direct.showbase.DirectObject import DirectObject\n')
        file.write('import random, sys, os, math\n')
        file.write('from level_editor_data import *\n')
        file.write('class RaceSetup(DirectObject):\n')
        file.write('    def __init__(self, editor):\n')
        file.write('        editor.bgr = '+str(self.bgr)+'\n')
        file.write('        editor.bgg = '+str(self.bgg)+'\n')
        file.write('        editor.bgb = '+str(self.bgb)+'\n')
        file.write('        editor.loadTerrain("'+self.tpath+'")\n')
        file.write('        editor.terrain.setScale('+str(self.terrain.getScale())+')\n')
        file.write('        editor.terrain.setZ('+str(self.terrain.getZ())+')\n')
        file.write('        editor.alightBrightness = '+str(self.alightBrightness)+'\n')
        file.write('        editor.dlightBrightness = '+str(self.dlightBrightness)+'\n')
        
        for ship in self.ships:
            file.write('        editor.ships.append(setupShip('+str(round(ship.model.getX()))+', '+str(round(ship.model.getY()))+', '+str(ship.num)+', '+str(round(ship.model.getH()))+'))\n')
        for barrier in self.barriers:
            file.write('        editor.barriers.append(setupBarrier('+str(round(barrier.model.getX()))+', '+str(round(barrier.model.getY()))+', '+str(round(barrier.model.getH()))+'))\n')
        for checkpoint in self.checkpoints:
            file.write('        editor.checkpoints.append(setupCheckpoint('+str(round(checkpoint.model.getX()))+', '+str(round(checkpoint.model.getY()))+', '+str(round(checkpoint.model.getH()))+', '+str(checkpoint.checkNum)+', '+str(checkpoint.wayNum)+'))\n')
        if self.startingline is not None:
            file.write('        editor.startingline = setupStartingline('+str(round(self.startingline.model.getX()))+', '+str(round(self.startingline.model.getY()))+', '+str(round(self.startingline.model.getH()))+')\n')
        for power in self.powerups:
            file.write('        editor.powerups.append(setupPowerup('+str(round(power.model.getX()))+', '+str(round(power.model.getY()))+'))\n')
        for power in self.powerh:
            file.write('        editor.powerh.append(setupPowerh('+str(round(power.model.getX()))+', '+str(round(power.model.getY()))+'))\n')
        for way in self.waypoints:
            file.write('        editor.waypoints.append(setupWaypoint('+str(round(way.model.getX()))+', '+str(round(way.model.getY()))+', '+str(way.num)+'))\n')
        
        file.write('        editor.laps = '+str(self.laps)+'\n')
        file.write('        editor.winCredits = '+str(self.winCredits)+'\n')
        file.write('        editor.minPlace = '+str(self.minPlace)+'\n')
        file.write('        editor.setValues()')
        
    def exportLevel(self):
        file = open(self.World+'/race'+self.Race+'.py', 'w')
        
        file.write('from pandac.PandaModules import *\n')
        file.write('from direct.showbase.DirectObject import DirectObject\n')
        file.write('import random, sys, os, math\n')
        file.write('from Environment import *\n')
        file.write('class Race(DirectObject):\n')
        file.write('    def __init__(self, environment, user, multiplayer, player1ship, player2ship, numCPUs, userUpgrades, CPUUpgrades):\n')
        file.write('        base.setBackgroundColor('+str(self.bgr)+', '+str(self.bgg)+', '+str(self.bgb)+')\n')
        file.write('        environment.earth = loader.loadModel("'+self.tpath+'")\n')
        file.write('        environment.earth.setZ('+str(self.terrain.getZ())+')\n')
        file.write('        environment.earth.setScale('+str(self.terrain.getScale())+')\n')
        file.write('        environment.earth.setBin("background", 1)\n')
        file.write('        environment.earth.find("**/trees").setBin("transparent", 1)\n')
        file.write('        environment.ambientLight = AmbientLight("ambientLight")\n')
        file.write('        environment.ambientLight.setColor(Vec4('+str(self.alightBrightness)+', '+str(self.alightBrightness)+', '+str(self.alightBrightness)+', 1))\n')
        file.write('        environment.directionalLight = DirectionalLight("directionalLight")\n')
        file.write('        environment.directionalLight.setDirection(Vec3(-5, -5, -5))\n')
        file.write('        environment.directionalLight.setColor(Vec4('+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', 1))\n')
        file.write('        environment.directionalLight.setSpecularColor(Vec4('+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', 1))\n')
        file.write('        environment.domenum = 7\n')    # ***************************************************
        
        self.ships.sort(key = attrgetter('num'))
        self.checkpoints.sort(key = attrgetter('checkNum'))
        
        file.write('        environment.playerShip = Ship(player1ship, '+str(round(self.ships[0].model.getX()))+', '+str(round(self.ships[0].model.getY()))+', 5, '+str(round(self.ships[0].model.getH()))+', environment, '+str(len(self.checkpoints)+1)+', 1)\n')
        file.write('        if multiplayer:\n')
        file.write('            environment.player2Ship = Ship(player2ship, '+str(round(self.ships[1].model.getX()))+', '+str(round(self.ships[1].model.getY()))+', 5, '+str(round(self.ships[1].model.getH()))+', environment, '+str(len(self.checkpoints)+1)+', 2)\n')
        
        allWaypoints = []
        for waypoint in self.waypoints:
            tempWaypoint = setupWaypoint(waypoint.model.getX(), waypoint.model.getY(), waypoint.num)
            allWaypoints.append(tempWaypoint)
        for checkpoint in self.checkpoints:
            tempWaypoint = setupWaypoint(checkpoint.model.getX(), checkpoint.model.getY(), checkpoint.wayNum)
            allWaypoints.append(tempWaypoint)
        allWaypoints.sort(key = attrgetter('num'))
        
        file.write('        self.xpoints = [')
        for i in range(len(allWaypoints)):
            file.write(str(round(allWaypoints[i].model.getX())))
            if i < len(allWaypoints)-1:
                file.write(', ')
            else:
                file.write(']\n')
                
        file.write('        self.ypoints = [')
        for i in range(len(allWaypoints)):
            file.write(str(round(allWaypoints[i].model.getY())))
            if i < len(allWaypoints)-1:
                file.write(', ')
            else:
                file.write(']\n')
        
        file.write('        self.xplaces = [')
        for i in range(1, 6):
            file.write(str(round(self.ships[i].model.getX())))
            if i < 5:
                file.write(', ')
            else:
                file.write(']\n')
        
        file.write('        self.yplaces = [')
        for i in range(1, 6):
            file.write(str(round(self.ships[i].model.getY())))
            if i < 5:
                file.write(', ')
            else:
                file.write(']\n')
                
        file.write('        self.hs = [')
        for i in range(1, 6):
            file.write(str(round(self.ships[i].model.getH())))
            if i < 5:
                file.write(', ')
            else:
                file.write(']\n')
                
        file.write('        shiptaken = [False, False, False, False, False, False]\n')
        file.write('        shiptaken[player1ship - 1] = True\n')
        file.write('        if multiplayer:\n')
        file.write('            shiptaken[player2ship - 1] = True\n')
        file.write('        self.startPlaces = [')
        for i in range(len(self.checkpoints)+1):
            if i == 0:
                file.write('0')
            else:
                file.write(str(self.checkpoints[i-1].wayNum))
            if i < len(self.checkpoints):
                file.write(', ')
            else:
                file.write(', 0]\n')
                
        file.write('        self.pointsnum = '+str(len(allWaypoints))+'\n')
        
        file.write('        fact = 0\n')
        file.write('        if multiplayer:\n')
        file.write('            fact = 1\n')
        file.write('        for i in range(numCPUs):\n')
        file.write('            tempship = 0\n')
        file.write('            foundship = False\n')
        file.write('            while not foundship:\n')
        file.write('                tempship = random.randrange(6)\n')
        file.write('                if not shiptaken[tempship]:\n')
        file.write('                    shiptaken[tempship] = True\n')
        file.write('                    foundship = True\n')
        file.write('            environment.ships.append(CPUShip(tempship + 1, self.xplaces[i + fact], self.yplaces[i + fact], 5, self.hs[i+fact], self.xpoints, self.ypoints, self.pointsnum, environment, '+str(len(self.checkpoints)+1)+', self.startPlaces, i+1))\n')
        
        for barrier in self.barriers:
            file.write('        environment.barriers.append(Barrier('+str(round(barrier.model.getX()))+', '+str(round(barrier.model.getY()))+', '+str(round(barrier.model.getH()))+'))\n')

        for checkpoint in self.checkpoints:
            file.write('        environment.checkpoints.append(Checkpoint('+str(round(checkpoint.model.getX()))+', '+str(round(checkpoint.model.getY()))+', 0, '+str(round(checkpoint.model.getH()))+'))\n')
        file.write('        environment.checkpoints.append(Startingline('+str(round(self.startingline.model.getX()))+', '+str(round(self.startingline.model.getY()))+', 0, '+str(round(self.startingline.model.getH()))+'))\n')
        
        for powerup in self.powerups:
            file.write('        environment.powerups.append(Powerup('+str(round(powerup.model.getX()))+', '+str(round(powerup.model.getY()))+', 5))\n')
            
        for powerh in self.powerh:
            file.write('        environment.powerh.append(Powerh('+str(round(powerh.model.getX()))+', '+str(round(powerh.model.getY()))+', 5))\n')
             
        camlocater = NodePath(PandaNode("floater"))
        camlocater.reparentTo(render)
        camlocater.setPos(self.ships[0].model, (0, -15, 4))
        cam1pos = camlocater.getPos()
        camlocater.setPos(self.ships[1].model, (0, -15, 4))
        cam2pos = camlocater.getPos()
        camlocater.removeNode()
        
        file.write('        base.camera.setPos('+str(cam1pos)+')\n')
        file.write('        if multiplayer:\n')
        file.write('            environment.cam2.setPos('+str(cam2pos)+')\n')
        
        file.write('        environment.laps = '+str(self.laps)+'\n')
        file.write('        self.finishCredits = ['+str(self.winCredits)+', '+str(self.winCredits/2)+', '+str(self.winCredits/4)+', '+str(self.winCredits/6)+', '+str(self.winCredits/8)+', 0]\n')
        file.write('        self.finishPlace = '+str(self.minPlace)+'\n')
        
        for w in allWaypoints:
            w.delete(allWaypoints)
            
    def exportBattle(self):
        file = open(self.World+'/battle.py', 'w')
        
        file.write('from pandac.PandaModules import *\n')
        file.write('from direct.showbase.DirectObject import DirectObject\n')
        file.write('import random, sys, os, math\n')
        file.write('from Battledata import *\n')
        file.write('class Race(DirectObject):\n')
        file.write('    def __init__(self, environment, user, player1ship, player2ship):\n')
        file.write('        base.setBackgroundColor('+str(self.bgr)+', '+str(self.bgg)+', '+str(self.bgb)+')\n')
        file.write('        environment.earth = loader.loadModel("'+self.tpath+'")\n')
        file.write('        environment.earth.setZ('+str(self.terrain.getZ())+')\n')
        file.write('        environment.earth.setScale('+str(self.terrain.getScale())+')\n')
        file.write('        environment.earth.setBin("background", 1)\n')
        file.write('        environment.earth.find("**/trees").setBin("transparent", 1)\n')
        file.write('        environment.ambientLight = AmbientLight("ambientLight")\n')
        file.write('        environment.ambientLight.setColor(Vec4('+str(self.alightBrightness)+', '+str(self.alightBrightness)+', '+str(self.alightBrightness)+', 1))\n')
        file.write('        environment.directionalLight = DirectionalLight("directionalLight")\n')
        file.write('        environment.directionalLight.setDirection(Vec3(-5, -5, -5))\n')
        file.write('        environment.directionalLight.setColor(Vec4('+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', 1))\n')
        file.write('        environment.directionalLight.setSpecularColor(Vec4('+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', '+str(self.dlightBrightness)+', 1))\n')
        file.write('        environment.domenum = 7\n')   # *****************************
        file.write('        environment.playerShip = Ship(player1ship, '+str(round(self.ships[0].model.getX()))+', '+str(round(self.ships[0].model.getY()))+', 5, '+str(round(self.ships[0].model.getH()))+', environment, 1)\n')
        file.write('        environment.player2Ship = Ship(player2ship, '+str(round(self.ships[1].model.getX()))+', '+str(round(self.ships[1].model.getY()))+', 5, '+str(round(self.ships[1].model.getH()))+', environment, 2)\n')
        for powerup in self.powerups:
            file.write('        environment.powerups.append(Powerup('+str(round(powerup.model.getX()))+', '+str(round(powerup.model.getY()))+', 5))\n')
        camlocater = NodePath(PandaNode("floater"))
        camlocater.reparentTo(render)
        camlocater.setPos(self.ships[0].model, (0, -15, 4))
        cam1pos = camlocater.getPos()
        camlocater.setPos(self.ships[1].model, (0, -15, 4))
        cam2pos = camlocater.getPos()
        camlocater.removeNode()
        
        file.write('        base.camera.setPos('+str(cam1pos)+')\n')
        file.write('        environment.cam2.setPos('+str(cam2pos)+')\n')