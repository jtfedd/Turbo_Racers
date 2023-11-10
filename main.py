class Configloader():
    def __init__(self):
        file = open('config/config.txt', 'r')
        data = file.read()
        self.items = data.split('\n')
    def getFullscreen(self):
        full = self.items[0].split('=')
        return int(full[1])
    def getResolution(self):
        res = self.items[1].split('=')
        return res[1]
    def getFrameRateMeter(self):
        frm = self.items[2].split('=')
        return int(frm[1])
    def getBloom(self):
        bloom = self.items[3].split('=')
        return int(bloom[1])
    def get3D(self):
        threed = self.items[4].split('=')
        return int(threed[1])
    def saveConfig(self, full, res, frm, bloom, threed):
        file = open('config/config.txt', 'w')
        file.write('fullscreen='+str(full)+'\n')
        file.write('resolution='+res+'\n')
        file.write('frameratemeter='+str(frm)+'\n')
        file.write('bloom='+str(bloom)+'\n')
        file.write('3d='+str(threed)+'\n')
        file.close()

from pandac.PandaModules import *
CONFIG = Configloader()
fullscreen = CONFIG.getFullscreen()
loadPrcFileData("", "fullscreen "+str(fullscreen))
loadPrcFileData("", CONFIG.getResolution())
loadPrcFileData("", "red-blue-stereo "+str(CONFIG.get3D()))
loadPrcFileData("", "show-frame-rate-meter  "+str(CONFIG.getFrameRateMeter()))

import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
from direct.task.Task import Task
from direct.stdpy.file import *
import sys, imp, os

from Environment import *
from Battledata import *

class Game(DirectObject):
    def __init__(self):
        """ Game class. main keeps track of where the user is,
        also handles updating the menu screen. Game will also
        start races and handle the coordinating of all the screens."""
        
        base.camLens.setFov(90)
        
        #load the loading screen
        self.background = OnscreenImage(image = 'models/textures/loadingback.png',
                                        pos = (0,0,0),
                                        scale = (base.camLens.getAspectRatio(), 1, 1))
        self.background.setImage('models/textures/mainback.png')                #load the rest for future use
        self.background.setImage('models/textures/mainbackno.png')
        self.background.setImage('models/textures/optionsback.png')
        self.background.setImage('models/textures/loadingback.png')             #and set the loading screen back
        #And render it
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        
        #Load all buttons, which will significantly reduce in-menu loading time
        self.loadingbar = DirectWaitBar(text = '', range = 38, value = 0, pos = (0, 0, -.8), barColor = (0, 1, 0, 1), scale = (1, 1, .2))
        loader.loadModel('models/buttons/0')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/1')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/2')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/3')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/4')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/5')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/arctic')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/back')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/blank')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/canyon')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/career')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/champ')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/city')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/continue')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/exit')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/garage')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/help')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/mountain')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/larrow')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/lavaland')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/login')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/main')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/multi')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/no')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/options')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/race')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/rarrow')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/replay')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/ship1')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/ship2')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/ship3')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/ship4')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/ship5')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/ship6')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/single')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/yes')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/2prace')
        self.loadingbar['value'] += 1
        base.graphicsEngine.renderFrame()
        loader.loadModel('models/buttons/battle')
        
        self.music = loader.loadSfx('sounds/music/menu.wav')
        self.music.setLoop(True)
        self.music.setVolume(.7)
        self.music.play()
        
        self.click = loader.loadSfx('sounds/sfx/click.wav')
        
        self.loadingbar.finish()
        base.graphicsEngine.renderFrame()
        self.loadingbar.destroy()

        self.background.setImage('models/textures/mainback.png')

        self.input = Input(self)            #create an input handler

        self.user = None

        self.pos = 'open'  # pos (position) tells where the user is
        self.window = openingscreen(self) # window holds the class that has all of the buttons
        self.career = False
        self.multiplayer = False
        self.player = 1
        self.sit = 0

        self.player1ship = None
        self.player2ship = None
        self.playWorld = None
        self.playRace = None
        self.numCPUs = 5
        self.userUpgrades = False
        self.CPUUpgrades = False

        self.raceOutcome = None
        
    def openingscreen(self):
        self.background.setImage('models/textures/mainback.png')
        self.window.destroy()
        self.pos = 'open'
        self.window = openingscreen(self)

    def help(self):
        self.window.destroy()
        self.pos = 'help'
        self.window = help(self)

    def login(self):
        self.window.destroy()
        self.pos = 'login'
        self.window = login(self)

    def options(self):
        self.background.setImage('models/textures/optionsback.png')
        self.window.destroy()
        self.pos = 'login'
        self.window = options(self)

    def usermenu(self):
        self.window.destroy()
        if self.user.won == False:
            self.background.setImage('models/textures/mainbackno.png')
        if self.user.won:
            self.background.setImage('models/textures/mainback.png')
        self.pos = 'user'
        self.window = usermenu(self, self.user)
        
    def multimenu(self):
        self.window.destroy()
        self.pos = 'multimenu'
        self.window = multimenu(self)

    def careermenu(self):
        self.window.destroy()
        self.pos = 'career'
        self.window = careermenu(self, self.user)

    def garage(self):
        self.window.destroy()
        self.pos = 'garage'
        self.window = garage(self, self.user)

    def chooseShip(self, condition):
        self.window.destroy()
        self.pos = 'ship'
        self.window = chooseShip(self, self.player, self.multiplayer, condition)

    def chooseWorld(self):
        self.window.destroy()
        self.pos = 'world'
        self.window = chooseWorld(self)

    def chooseRace(self):
        self.window.destroy()
        self.pos = 'race'
        self.window = chooseRace(self)

    def chooseCPUs(self):
        self.window.destroy()
        self.pos = 'cpus'
        self.window = chooseCPUs(self)

    def getUserUpgrades(self):
        self.window.destroy()
        self.pos = 'upgrades'
        self.window = getUserUpgrades(self)

    def getCPUUpgrades(self):
        self.window.destroy()
        self.pos = 'upgrades'
        self.window = getCPUUpgrades(self)

    def getReady(self, afterRaceAction):
        self.window.destroy()
        self.pos = 'ready'
        self.window = getReady(self, afterRaceAction)
        
    def credits(self, action):
        self.background.setImage('models/textures/optionsback.png')
        self.window.destroy()
        self.pos = 'credits'
        self.window = Credits(self, action)

    def Race(self, afterRaceAction):
        self.window.destroy()
        self.music.stop()
        self.pos = 'game'
        self.background.setImage('models/textures/loadingback.png')
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()
        
        if self.multiplayer:
            self.userUpgrades = False
            self.CPUUpgrades = False
        if self.sit != 6:
            Environment(self, self.user, self.multiplayer, self.player1ship, self.player2ship, self.playWorld, self.playRace, self.numCPUs, self.userUpgrades, self.CPUUpgrades, afterRaceAction, CONFIG)
        else:
            Battle(self, self.user, self.player1ship, self.player2ship, self.playWorld, afterRaceAction, CONFIG)

    def afterRace(self, afterRaceAction, text, finished, finishCredits, finishPlaces):
        self.background = OnscreenImage(image = 'models/textures/mainback.png',
                                        pos = (0,0,0),
                                        scale = (base.camLens.getAspectRatio(), 1, 1))

        if self.user.won == False:
            self.background.setImage('models/textures/mainbackno.png')

        self.window = afterRace(self, afterRaceAction, text, finished, finishCredits, finishPlaces)
        
    def newShip(self):
        self.window.destroy()
        self.pos = 'new ship'
        self.window = newShip(self)

class Input(DirectObject):
    def __init__(self, game):
  
        self.game = game                        #recognise the game object

        self.accept('escape', self.escape)      #handle escape
        self.accept('f1', self.printScreen)              #handle take screenshot

    def escape(self):
        sys.exit()

    def printScreen(self):
        base.screenshot('screenshots/')

class openingscreen(DirectObject):
    def __init__(self, game):
        self.game = game
        #buttons
        login = loader.loadModel('models/buttons/login')
        self.loginb = DirectButton(geom = (login.find('**/login'),
                                           login.find('**/loginlight'),
                                           login.find('**/loginlight'),
                                           login.find('**/loginlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.login,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (0,0,-0.6))
        options = loader.loadModel('models/buttons/options')
        self.optionsb = DirectButton(geom = (options.find('**/options'),
                                             options.find('**/optionslight'),
                                             options.find('**/optionslight'),
                                             options.find('**/optionslight')),
                                     borderWidth = (0,0),
                                     frameColor = (0,0,0,0),
                                     command = self.game.options,
                                     rolloverSound = None,
                                     clickSound = game.click,
                                     scale = 0.3,
                                     pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        credits = loader.loadModel('models/buttons/credits')
        self.creditsb = DirectButton(geom = (credits.find('**/credits'),
                                             credits.find('**/creditslight'),
                                             credits.find('**/creditslight'),
                                             credits.find('**/creditslight')),
                                     borderWidth = (0,0),
                                     frameColor = (0,0,0,0),
                                     command = self.game.credits,
                                     extraArgs = ['mainmenu'],
                                     rolloverSound = None,
                                     clickSound = game.click,
                                     scale = 0.1,
                                     pos = (0.755*base.camLens.getAspectRatio(),0, 0.93))
        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  scale = 0.1,
                                  rolloverSound = None,
                                  clickSound = None,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        help = loader.loadModel('models/buttons/help')
        self.helpb = DirectButton(geom = (help.find('**/help'),
                                          help.find('**/helplight'),
                                          help.find('**/helplight'),
                                          help.find('**/helplight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.game.help,
                                  rolloverSound = None,
                                  clickSound = game.click,
                                  scale = 0.1,
                                  pos = (0.855 * base.camLens.getAspectRatio(), 0, 0.93))

    def destroy(self):
        self.loginb.destroy()
        self.creditsb.destroy()
        self.optionsb.destroy()
        self.exitb.destroy()
        self.helpb.destroy()

class help(DirectObject):
    def __init__(self, game):
        self.game = game
        #text
        self.count = 1
        self.max = 7
        self.inst = OnscreenImage(image = 'models/textures/instback.png',
                                  pos = (0,0,0),
                                  scale = (1.2, 1, 0.65))
        self.inst.setTransparency(TransparencyAttrib.MAlpha)

        inst_file = open('help/'+str(self.count)+'.txt', 'r')
        inst_text = inst_file.read()
        inst_file.close()
        
        self.text = OnscreenText(text = inst_text,
                                 pos = (0,0.55,0),
                                 scale = 0.065,
                                 fg = (0.25,1,1,1),
                                 mayChange = 1)
        #buttons
        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  scale = 0.1,
                                  rolloverSound = None,
                                  clickSound = None,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.openingscreen,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))

        la = loader.loadModel('models/buttons/larrow')
        self.lab = DirectButton(geom = (la.find('**/larrow'),
                                        la.find('**/larrowlight'),
                                        la.find('**/larrowlight'),
                                        la.find('**/larrowlight')),
                                borderWidth = (0,0),
                                frameColor = (0,0,0,0),
                                command = self.rotateleft,
                                rolloverSound = None,
                                clickSound = game.click,
                                scale = 0.1,
                                pos = (-0.68*base.camLens.getAspectRatio(),0,0.7))

        ra = loader.loadModel('models/buttons/rarrow')
        self.rab = DirectButton(geom = (ra.find('**/rarrow'),
                                        ra.find('**/rarrowlight'),
                                        ra.find('**/rarrowlight'),
                                        ra.find('**/rarrowlight')),
                                borderWidth = (0,0),
                                frameColor = (0,0,0,0),
                                command = self.rotateright,
                                rolloverSound = None,
                                clickSound = game.click,
                                scale = 0.1,
                                pos = (0.68*base.camLens.getAspectRatio(),0,0.7))

    def rotateleft(self):
        self.count -= 1
        if self.count == 0:
            self.count = self.max
            
        inst_file = open('help/'+str(self.count)+'.txt', 'r')
        inst_text = inst_file.read()
        inst_file.close()

        self.text.setText(inst_text)

    def rotateright(self):
        self.count += 1
        if self.count > self.max:
            self.count = 1
            
        inst_file = open('help/'+str(self.count)+'.txt', 'r')
        inst_text = inst_file.read()
        inst_file.close()

        self.text.setText(inst_text)

    def destroy(self):
        self.exitb.destroy()
        self.backb.destroy()
        self.lab.destroy()
        self.rab.destroy()
        self.inst.destroy()
        self.text.destroy()

class options(DirectObject):
    def __init__(self, game):
        self.game = game
        #buttons
        save = loader.loadModel('models/buttons/saveandexit')
        self.saveb = DirectButton(geom = (save.find('**/saveandexit'),
                                          save.find('**/saveandexitlight'),
                                          save.find('**/saveandexitlight'),
                                          save.find('**/saveandexitlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.saveandexit,
                                   rolloverSound = None,
                                   clickSound = None,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  scale = 0.1,
                                  rolloverSound = None,
                                  clickSound = None,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))
                                  
        self.tempfull = CONFIG.getFullscreen()
        self.tempres = CONFIG.getResolution()
        self.tempfrm = CONFIG.getFrameRateMeter()
        self.tempbloom = CONFIG.getBloom()
        self.temp3d = CONFIG.get3D()
        
        color = (0, 0, 0, 1)
        
        self.fullb = DirectButton(text = 'Fullscreen On/Off',
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.setFullscreen,
                                  scale = 0.1,
                                  text_fg = color,
                                  rolloverSound = None,
                                  clickSound = game.click,
                                  pos = (0,0,0.8))
        self.fulltext = OnscreenText(text = 'Turbo Racers can run either fullscreen or windowed.', scale = 0.1, fg = color, pos = (0,0.7))
        
        self.resb = DirectButton(text = 'Resolution win-size somesize or other',
                                 borderWidth = (0,0),
                                 frameColor = (0,0,0,0),
                                 command = self.setResolution,
                                 scale = 0.1,
                                 text_fg = color,
                                 rolloverSound = None,
                                 clickSound = game.click,
                                 pos = (0,0,0.5))
        self.restext = OnscreenText(text = 'The dimensions of the screen.', scale = 0.1, fg = color, pos = (0,0.4))
        
        self.frmb = DirectButton(text = 'Frame Rate Meter On/Off',
                                 borderWidth = (0,0),
                                 frameColor = (0,0,0,0),
                                 command = self.setFrameRateMeter,
                                 scale = 0.1,
                                 text_fg = color,
                                 rolloverSound = None,
                                 clickSound = game.click,
                                 pos = (0,0,0.2))
        self.frmtext = OnscreenText(text = 'Shows the frame rate in frames per second.', scale = 0.1, fg = color, pos = (0,0.1))
        
        self.bloomb = DirectButton(text = 'Bloom On/Off',
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.setBloom,
                                   scale = 0.1,
                                   text_fg = color,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   pos = (0,0,-0.1))
        self.bloomtext = OnscreenText(text = 'Adds a glow effect to certain objects in gameplay.', scale = 0.1, fg = color, pos = (0,-0.2))
        
        self.threedb = DirectButton(text = 'Red/Cyan 3D On/Off',
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.set3d,
                                   scale = 0.1,
                                   text_fg = color,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   pos = (0,0,-0.4))
        self.threedbtext = OnscreenText(text = 'Runs the game with stereoscopic 3D enabled.', scale = 0.1, fg = color, pos = (0,-0.5))
        
        self.updateButtons()
        
    def updateButtons(self):
        if self.tempfull:
            self.fullb["text"] = 'Fullscreen On'
        else:
            self.fullb["text"] = 'Fullscreen Off'
        
        self.resb["text"] = 'Resolution '+self.tempres
        
        if self.tempfrm:
            self.frmb["text"] = 'Frame Rate Meter On'
        else:
            self.frmb["text"] = 'Frame Rate Meter Off'
            
        if self.tempbloom:
            self.bloomb["text"] = 'Bloom On'
        else:
            self.bloomb["text"] = 'Bloom Off'
        
        if self.temp3d:
            self.threedb["text"] = 'Red/Cyan 3D On'
        else:
            self.threedb["text"] = 'Red/Cyan 3D Off'
            
    def saveandexit(self):
        CONFIG.saveConfig(self.tempfull, self.tempres, self.tempfrm, self.tempbloom, self.temp3d)
        sys.exit()
        
    def setFullscreen(self):
        if self.tempfull:
            self.tempfull = 0
        else:
            self.tempfull = 1
        self.updateButtons()
    
    def setResolution(self):
        resolutions = ["win-size 800 600", "win-size 1024 768", "win-size 1280 1024", "win-size 1600 900", "win-size 1680 1050", "win-size 1920 1080"]
        index = resolutions.index(self.tempres)
        newindex = index+1
        if newindex >= len(resolutions):
            newindex = 0
        self.tempres = resolutions[newindex]
        self.updateButtons()
    
    def setFrameRateMeter(self):
        if self.tempfrm:
            self.tempfrm = 0
        else:
            self.tempfrm = 1
        self.updateButtons()
    
    def setBloom(self):
        if self.tempbloom:
            self.tempbloom = 0
        else:
            self.tempbloom = 1
        self.updateButtons()
        
    def set3d(self):
        if self.temp3d:
            self.temp3d = 0
        else:
            self.temp3d = 1
        self.updateButtons()

    def destroy(self):
        self.backb.destroy()
        self.exitb.destroy()
        self.fullb.destroy()
        self.resb.destroy()
        self.frmb.destroy()
        self.bloomb.destroy()
        self.fulltext.destroy()
        self.restext.destroy()
        self.frmtext.destroy()
        self.bloomtext.destroy()

class login(DirectObject):
    def __init__(self, game):
        self.game = game
        self.User = None
        #buttons
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.openingscreen,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  scale = 0.1,
                                  rolloverSound = None,
                                  clickSound = None,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        #load saved games
        self.users = []
        self.user = 0
        for file in sorted(os.listdir('saved')):
            if file.endswith('.py'):
                modulename = file[:-3]
                try:
                    file, filename, description = imp.find_module(modulename, ['saved'])
                    Savedmodule = imp.load_module(modulename, file, filename, description)
                    if hasattr(Savedmodule, 'SavedGame'):
                        try:
                            self.users.append(Savedmodule.SavedGame())
                        except Exception as e:
                            print('Error %s' % e)
                    else:
                        print('No saved game in %s' % Savedmodule)
                finally:
                    if file:
                        file.close()

        # print out
        counter = 0
        self.userlist = []
        for i in self.users:
            counter = counter + 1
            bk_text = i.name

            self.userlist.append(DirectButton(text = (bk_text, bk_text, bk_text, bk_text),
                                              pos = (-.8*base.camLens.getAspectRatio(),0,.45-(0.1*counter)),
                                              borderWidth = (0,0),
                                              frameColor = (0,0,0,0),
                                              text_fg = (0,0,0,1),
                                              command = self.login,
                                              rolloverSound = None,
                                              clickSound = game.click,
                                              extraArgs = [i.name],
                                              scale = 0.07,
                                              text_align = TextNode.ALeft))

        self.Entry = DirectEntry(text = "" ,scale=.1,command=self.login,initialText="", numLines = 1,pos = (-0.495,0,-.55),focus = 1, frameColor = (0.5,0.5,0.5,1), text_fg = (0,0,0,1), suppressKeys=1, rolloverSound = None, clickSound = game.click)

    def login(self, name):
        self.User = None
        found = False
        for user in self.users:
            if user.name == name:
                self.User = user
                found = True
                
        if found == False:
            self.User = SavedGame(name)

        save(self.User)
        self.game.usermenu()

    def destroy(self):
        for b in self.userlist:
            b.destroy()
        self.Entry.destroy()
        self.exitb.destroy()
        self.backb.destroy()
        self.game.user = self.User
        

class usermenu(DirectObject):
    def __init__(self, game, user):
        self.game = game
        self.user = user
        self.game.player = 1
        #buttons
        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        main = loader.loadModel('models/buttons/main')
        self.mainb = DirectButton(geom = (main.find('**/main'),
                                          main.find('**/mainlight'),
                                          main.find('**/mainlight'),
                                          main.find('**/mainlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.openingscreen,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))

        single = loader.loadModel('models/buttons/single')
        self.singleb = DirectButton(geom = (single.find('**/single'),
                                            single.find('**/singlelight'),
                                            single.find('**/singlelight'),
                                            single.find('**/singlelight')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = self.game.chooseShip,
                                    rolloverSound = None,
                                    clickSound = game.click,
                                    extraArgs = [1],
                                    scale = 0.4,
                                    pos = (-0.7 * base.camLens.getAspectRatio(), 0, -0.63))

        multi = loader.loadModel('models/buttons/multi')
        self.multib = DirectButton(geom = (multi.find('**/multi'),
                                           multi.find('**/multilight'),
                                           multi.find('**/multilight'),
                                           multi.find('**/multilight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.multimenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.4,
                                   pos = (0.7 * base.camLens.getAspectRatio(), 0, -0.63))

        career = loader.loadModel('models/buttons/career')
        self.careerb = DirectButton(geom = (career.find('**/career'),
                                            career.find('**/careerlight'),
                                            career.find('**/careerlight'),
                                            career.find('**/careerlight')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = game.careermenu,
                                    rolloverSound = None,
                                    clickSound = game.click,
                                    scale = 0.4,
                                    pos = (0, 0, -0.63))

    def destroy(self):
        self.exitb.destroy()
        self.mainb.destroy()
        self.singleb.destroy()
        self.multib.destroy()
        self.careerb.destroy()
        
class multimenu(DirectObject):
    def __init__(self, game):
        self.game = game
        
        self.text = OnscreenText(text = 'Battle or race?',
                                 fg = (1,1,1,1),
                                 scale = 0.07,
                                 pos = (0,-0.4,0))
                                 
        #buttons
        
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))
                                  
        race = loader.loadModel('models/buttons/2prace')
        self.raceb = DirectButton(geom = (race.find('**/2prace'),
                                          race.find('**/2pracelight'),
                                          race.find('**/2pracelight'),
                                          race.find('**/2pracelight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.game.chooseShip,
                                  extraArgs = [2],
                                  rolloverSound = None,
                                  clickSound = self.game.click,
                                  scale = 0.4,
                                  pos = (0.3 * base.camLens.getAspectRatio(), 0, 0))
                                  
        battle = loader.loadModel('models/buttons/battle')
        self.battleb = DirectButton(geom = (battle.find('**/battle'),
                                            battle.find('**/battlelight'),
                                            battle.find('**/battlelight'),
                                            battle.find('**/battlelight')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = self.game.chooseShip,
                                    extraArgs = [5],
                                    rolloverSound = None,
                                    clickSound = self.game.click,
                                    scale = 0.4,
                                    pos = (-0.3 * base.camLens.getAspectRatio(), 0, 0))
                                    
    def destroy(self):
        self.text.destroy()
        self.backb.destroy()
        self.exitb.destroy()
        self.raceb.destroy()
        self.battleb.destroy()

class careermenu(DirectObject):
    def __init__(self, game, user):
        self.game = game
        self.user = user

        #text

        self.inst = OnscreenImage(image = 'models/textures/instback.png',
                                  pos = (-0.47*base.camLens.getAspectRatio(),0,0),
                                  scale = (0.8, 1, 0.5))
        self.inst.setTransparency(TransparencyAttrib.MAlpha)
        
        inst_text = ''
        if self.user.won:
            inst_file = open('championship/won.txt', 'r')
            inst_text = inst_file.read()
            inst_file.close()
        else:
            inst_file = open(self.user.world+'/story'+str(self.user.race)+'.txt', 'r')
            inst_text = inst_file.read()
            inst_file.close()

        self.text = OnscreenText(text = inst_text,
                                 pos = (-0.47*base.camLens.getAspectRatio(),0.4,0),
                                 scale = 0.065,
                                 fg = (0.25,1,1,1))

        self.credits = OnscreenText(text = 'Credits = ' + str(self.user.credits),
                                    pos = (-0.75*base.camLens.getAspectRatio(),-0.8,0),
                                    scale = 0.07,
                                    fg = (1,0.5,0,1),
                                    align = TextNode.ALeft)

        #buttons

        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        garage = loader.loadModel('models/buttons/garage')
        self.garageb = DirectButton(geom = (garage.find('**/garage'),
                                            garage.find('**/garagelight'),
                                            garage.find('**/garagelight'),
                                            garage.find('**/garagelight')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = self.game.garage,
                                    rolloverSound = None,
                                    clickSound = game.click,
                                    scale = 0.3,
                                    pos = (-0.877*base.camLens.getAspectRatio(),0,-0.8))

        race = loader.loadModel('models/buttons/race')
        self.raceb = DirectButton(geom = (race.find('**/race'),
                                          race.find('**/racelight'),
                                          race.find('**/racelight'),
                                          race.find('**/racedisabled')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.game.chooseShip,
                                  rolloverSound = None,
                                  clickSound = game.click,
                                  extraArgs = [3],
                                  scale = 0.4,
                                  pos = (0.8*base.camLens.getAspectRatio(),0,-0.7))
                                  
        if self.user.won:
            self.raceb['state'] = DGG.DISABLED

    def destroy(self):
        self.backb.destroy()
        self.exitb.destroy()
        self.garageb.destroy()
        self.inst.destroy()
        self.text.destroy()
        self.raceb.destroy()
        self.credits.destroy()

class garage(DirectObject):
    def __init__(self, game, user):
        self.game = game
        self.user = user
        #credits
        self.credits = OnscreenText(text = 'Credits = '+str(self.user.credits),
                                    fg = (0,1,0.5,1),
                                    scale = 0.07,
                                    pos = (0,0.9,0),
                                    mayChange = 1)
        #buttons
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.careermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))
        
        self.bsounds = [loader.loadSfx('sounds/sfx/engine.wav'), loader.loadSfx('sounds/sfx/turbo.wav'), loader.loadSfx('sounds/sfx/steering.wav'), loader.loadSfx('sounds/sfx/shield.wav')]
        self.buttons = []
        self.des = []
        self.cost = []

        for i in range(4):
            temp = loader.loadModel('models/buttons/blank')
            tempb = DirectButton(geom = (temp.find('**/blank'),
                                         temp.find('**/blanklight'),
                                         temp.find('**/blanklight'),
                                         temp.find('**/blankdisabled')),
                                 borderWidth = (0,0),
                                 frameColor = (0,0,0,0),
                                 command = self.transaction,
                                 rolloverSound = None,
                                 clickSound = self.bsounds[i],
                                 extraArgs = [i],
                                 scale = 0.3,
                                 pos = (0,0,0.5-i*0.4))

            self.buttons.append(tempb)
            tempcost = OnscreenText(text = str((self.user.upgrades[i]+1)*500),
                                    scale = 0.08,
                                    fg = (1,1,1,1),
                                    pos = (0,0.5-i*0.4,0),
                                    mayChange = 1)
            self.cost.append(tempcost)

        self.checkButtons()

        enginetext = 'Engine: gives your ship a higher top speed. '
        turbotext = 'Turbo: gives your ship faster acceleration. '
        steeringtext = 'Steering: gives your ship better steering control. '
        shieldtext = 'Shield: gives your ship more hitpoints so it is harder to blow up. '
        self.texts = [enginetext, turbotext, steeringtext, shieldtext]
        for i in range(4):
            temptex = OnscreenText(text = self.texts[i]+str(self.user.upgrades[i])+' bought.',
                                   scale = 0.08,
                                   fg = (1,1,1,1),
                                   pos = (0,0.3-i*0.4),
                                   mayChange = 1)
            self.des.append(temptex)

    def transaction(self, i):
        self.game.user.credits -= (self.game.user.upgrades[i]+1)*500
        self.game.user.upgrades[i]+=1
        self.user = self.game.user
        self.credits.setText('Credits = '+str(self.user.credits))
        if self.user.upgrades[i]<5:
            self.cost[i].setText(str((self.user.upgrades[i]+1)*500))
            self.des[i].setText(self.texts[i]+str(self.user.upgrades[i])+' bought.')
        else:
            self.cost[i].setText('not availible')
            self.buttons[i]["state"] = DGG.DISABLED
            self.des[i].setText(self.texts[i]+str(self.user.upgrades[i])+' bought.')
        self.checkButtons()
        save(self.user)

    def checkButtons(self):
        for i in range(4):
            if (self.user.upgrades[i]+1)*500 > self.user.credits:
                self.buttons[i]['state'] = DGG.DISABLED
            if self.user.upgrades[i] == 5:
                self.buttons[i]['state'] = DGG.DISABLED
                self.cost[i].setText('not availible')
                

    def destroy(self):
        self.backb.destroy()
        self.exitb.destroy()
        for b in self.buttons:
            b.destroy()
        self.credits.destroy()
        for c in self.cost:
            c.destroy()
        for t in self.des:
            t.destroy()

class chooseShip(DirectObject):
    def __init__(self, game, player, multiplayer, sit):
        self.game = game
        self.player = player
        self.sit = sit
        self.game.sit = sit
        if self.sit == 2 or self.sit == 5:
            self.game.multiplayer = True
        if self.sit == 3 or self.sit == 1:
            self.game.multiplayer = False

        self.back = OnscreenImage(image = 'models/textures/instback.png',
                                  pos = (0,0,0),
                                  scale = (1, 1, 0.7))
        self.back.setTransparency(TransparencyAttrib.MAlpha)

        #text
        if self.game.multiplayer:
            self.text = OnscreenText(text = 'Choose ship for player '+str(player),
                                     fg = (1,1,1,1),
                                     scale = 0.07,
                                     pos = (0,-0.8,0))
        else:
            self.text = OnscreenText(text = 'Choose ship',
                                     fg = (1,1,1,1),
                                     scale = 0.07,
                                     pos = (0,-0.8,0))

        #buttons
        positions = [(-0.6,0,0.3), (0,0,0.3), (0.6,0,0.3), (-0.6,0,-0.3), (0,0,-0.3), (0.6,0,-0.3)]
        self.buttons = []
        for i in range(6):
            tempb = loader.loadModel('models/buttons/ship'+str(i+1))
            tempbutton = DirectButton(geom = (tempb.find('**/ship'+str(i+1)),
                                               tempb.find('**/ship'+str(i+1)+'light'),
                                               tempb.find('**/ship'+str(i+1)+'light'),
                                               tempb.find('**/locked')),
                                      borderWidth = (0,0),
                                      frameColor = (0,0,0,0),
                                      command = self.selectShip,
                                      rolloverSound = None,
                                      clickSound = game.click,
                                      extraArgs = [i+1],
                                      scale = 0.6,
                                      pos = positions[i])
            self.buttons.append(tempbutton)
            found = False
            if self.game.user.ships[i] != 1:
                self.buttons[i]['state'] = DGG.DISABLED

        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.careermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        if self.sit != 3:
            self.backb["command"] = self.game.usermenu

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

    def selectShip(self, num):
        if self.player == 1:
            self.game.player1ship = num
        else:
            self.game.player2ship = num
        if self.sit == 1:
            self.game.chooseWorld()
        if self.sit == 2:
            self.game.player = 2
            self.game.chooseShip(4)
        if self.sit == 3:
            self.game.playWorld = self.game.user.world
            self.game.playRace = self.game.user.race
            self.game.numCPUs = 5
            self.game.userUpgrades = True
            self.game.CPUUpgrades = True
            self.game.getReady('careermenu')
        if self.sit == 4:
            self.game.chooseWorld()
        if self.sit == 5:
            self.game.player = 2
            self.game.chooseShip(6)
        if self.sit == 6:
            self.game.chooseWorld()

    def destroy(self):
        self.text.destroy()
        self.backb.destroy()
        self.exitb.destroy()
        self.back.destroy()
        for b in self.buttons:
            b.destroy()

class chooseWorld(DirectObject):
    def __init__(self, game):
        self.game = game

        #instruction text

        self.inst = OnscreenText(text = 'Choose world',
                                 fg = (1,1,1,1),
                                 scale = 0.07,
                                 pos = (0,-0.8,0))

        self.back = OnscreenImage(image = 'models/textures/instback.png',
                                  pos = (0,0,0),
                                  scale = (1, 1, 0.7))
        self.back.setTransparency(TransparencyAttrib.MAlpha)

        #buttons
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        if self.game.sit == 3:
            self.backb["command"] = self.game.careermenu

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        #world buttons

        positions = [(-0.6,0,0.3), (0,0,0.3), (0.6,0,0.3), (-0.6,0,-0.3), (0,0,-0.3), (0.6,0,-0.3)]

        city = loader.loadModel('models/buttons/city')
        self.cityb = DirectButton(geom = (city.find('**/city'),
                                          city.find('**/citylight'),
                                          city.find('**/citylight'),
                                          city.find('**/locked')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.chooseWorld,
                                  rolloverSound = None,
                                  clickSound = game.click,
                                  extraArgs = ['city'],
                                  state = DGG.DISABLED,
                                  scale = 0.6,
                                  pos = positions[0])
        
        mountain = loader.loadModel('models/buttons/mountain')
        self.mountainb = DirectButton(geom = (mountain.find('**/mountain'),
                                            mountain.find('**/mountainlight'),
                                            mountain.find('**/mountainlight'),
                                            mountain.find('**/locked')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = self.chooseWorld,
                                    rolloverSound = None,
                                    clickSound = game.click,
                                    extraArgs = ['mountain'],
                                    state = DGG.DISABLED,
                                    scale = 0.6,
                                    pos = positions[1])

        arctic = loader.loadModel('models/buttons/arctic')
        self.arcticb = DirectButton(geom = (arctic.find('**/arctic'),
                                            arctic.find('**/arcticlight'),
                                            arctic.find('**/arcticlight'),
                                            arctic.find('**/locked')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = self.chooseWorld,
                                    rolloverSound = None,
                                    clickSound = game.click,
                                    extraArgs = ['arctic'],
                                    state = DGG.DISABLED,
                                    scale = 0.6,
                                    pos = positions[2])

        lava = loader.loadModel('models/buttons/lavaland')
        self.lavab = DirectButton(geom = (lava.find('**/lavaland'),
                                          lava.find('**/lavalandlight'),
                                          lava.find('**/lavalandlight'),
                                          lava.find('**/locked')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.chooseWorld,
                                  rolloverSound = None,
                                  clickSound = game.click,
                                  extraArgs = ['lavaland'],
                                  state = DGG.DISABLED,
                                  scale = 0.6,
                                  pos = positions[3])

        canyon = loader.loadModel('models/buttons/canyon')
        self.canyonb = DirectButton(geom = (canyon.find('**/canyon'),
                                            canyon.find('**/canyonlight'),
                                            canyon.find('**/canyonlight'),
                                            canyon.find('**/locked')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = self.chooseWorld,
                                    rolloverSound = None,
                                    clickSound = game.click,
                                    extraArgs = ['canyon'],
                                    state = DGG.DISABLED,
                                    scale = 0.6,
                                    pos = positions[4])

        champ = loader.loadModel('models/buttons/champ')
        self.champb = DirectButton(geom = (champ.find('**/champ'),
                                           champ.find('**/champlight'),
                                           champ.find('**/champlight'),
                                           champ.find('**/locked')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.chooseWorld,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   extraArgs = ['championship'],
                                   state = DGG.DISABLED,
                                   scale = 0.6,
                                   pos = positions[5])

        user = self.game.user
        if user.world == 'city':
            self.cityb["state"] = DGG.NORMAL

        if user.world == 'mountain':
            self.cityb["state"] = DGG.NORMAL
            self.mountainb["state"] = DGG.NORMAL

        if user.world == 'arctic':
            self.cityb["state"] = DGG.NORMAL
            self.mountainb["state"] = DGG.NORMAL
            self.arcticb["state"] = DGG.NORMAL

        if user.world == 'lavaland':
            self.cityb["state"] = DGG.NORMAL
            self.mountainb["state"] = DGG.NORMAL
            self.arcticb["state"] = DGG.NORMAL
            self.lavab["state"] = DGG.NORMAL

        if user.world == 'canyon':
            self.cityb["state"] = DGG.NORMAL
            self.mountainb["state"] = DGG.NORMAL
            self.arcticb["state"] = DGG.NORMAL
            self.lavab["state"] = DGG.NORMAL
            self.canyonb["state"] = DGG.NORMAL

        if user.world == 'championship':
            self.cityb["state"] = DGG.NORMAL
            self.mountainb["state"] = DGG.NORMAL
            self.arcticb["state"] = DGG.NORMAL
            self.lavab["state"] = DGG.NORMAL
            self.canyonb["state"] = DGG.NORMAL
            self.champb["state"] = DGG.NORMAL
        
    def chooseWorld(self, world):
        self.game.playWorld = world
        if self.game.sit != 6:
            self.game.chooseRace()
        else:
            self.game.getReady('usermenu')

    def destroy(self):
        self.inst.destroy()
        self.backb.destroy()
        self.exitb.destroy()
        self.cityb.destroy()
        self.mountainb.destroy()
        self.arcticb.destroy()
        self.lavab.destroy()
        self.canyonb.destroy()
        self.champb.destroy()
        self.back.destroy()

class chooseRace(DirectObject):
    def __init__(self, game):
        self.game = game

        #instructional text

        self.inst = OnscreenText(text = 'Choose race',
                                 fg = (1,1,1,1),
                                 scale = 0.07,
                                 pos = (0,-0.8,0))

        #black background

        self.back = OnscreenImage(image = 'models/textures/instback.png',
                                  pos = (0,0,0),
                                  scale = (1, 1, 0.7))
        self.back.setTransparency(TransparencyAttrib.MAlpha)

        #buttons

        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        if self.game.sit == 3:
            self.backb["command"] = self.game.careermenu

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        #race buttons

        self.buttontexts = []
        self.buttonfile = open(self.game.playWorld+'/races.txt', 'r')

        for i in range(5):
            self.buttontexts.append(self.buttonfile.readline())

        self.buttonfile.close()

        self.buttons = []

        for i in range(5):
            self.buttons.append(DirectButton(text = (self.buttontexts[i],
                                                     self.buttontexts[i],
                                                     self.buttontexts[i],
                                                     'Locked'),
                                             borderWidth = (0,0),
                                             frameColor = (0,0,0,0),
                                             command = self.chooseRace,
                                             rolloverSound = None,
                                             clickSound = game.click,
                                             extraArgs = [i+1],
                                             scale = 0.1,
                                             text_fg = (0.25,1,1,1),
                                             pos = (0,0,.45-(0.23*i))))

            if self.game.user.race <= i and self.game.playWorld == self.game.user.world:
                self.buttons[i]["state"] = DGG.DISABLED

    def chooseRace(self, raceNum):
        self.game.playRace = raceNum
        self.game.chooseCPUs()

    def destroy(self):
        self.inst.destroy()
        self.backb.destroy()
        self.exitb.destroy()
        self.back.destroy()
        for i in range(5):
            self.buttons[i].destroy()

class chooseCPUs(DirectObject):
    def __init__(self, game):
        self.game = game

        #instructional text

        self.inst = OnscreenText(text = 'Choose number of computer players',
                                 scale = 0.07,
                                 fg = (1,1,1,1),
                                 pos = (0,-0.4,0))

        #buttons

        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        if self.game.sit == 3:
            self.backb["command"] = self.game.careermenu

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))
        
        self.buttons = []

        fact = 1
        if self.game.multiplayer:
            fact = 0

        for i in range(5):
            tempb = loader.loadModel('models/buttons/'+str(i+fact))
            self.buttons.append(DirectButton(geom = (tempb.find('**/'+str(i+fact)),
                                                     tempb.find('**/'+str(i+fact)+'light'),
                                                     tempb.find('**/'+str(i+fact)+'light'),
                                                     tempb.find('**/'+str(i+fact)+'light')),
                                             borderWidth = (0,0),
                                             frameColor = (0,0,0,0),
                                             command = self.chooseCPUs,
                                             rolloverSound = None,
                                             clickSound = game.click,
                                             extraArgs = [i+fact],
                                             scale = 0.4,
                                             pos = (-0.9+(0.45*i), 0, 0)))

    def chooseCPUs(self, num):
        self.game.numCPUs = num
        if self.game.sit == 4:
            self.game.getReady('usermenu')
        if self.game.sit == 1:
            self.game.getUserUpgrades()
    def destroy(self):
        self.inst.destroy()
        self.backb.destroy()
        self.exitb.destroy()
        for i in range(5):
            self.buttons[i].destroy()

class getUserUpgrades(DirectObject):
    def __init__(self, game):
        self.game = game

        #Instructions

        self.inst = OnscreenText(text = 'Use upgrades for your ship?',
                                 fg = (1,1,1,1),
                                 scale = 0.07,
                                 pos = (0, 0.3, 0))

        #Buttons
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        if self.game.sit == 3:
            self.backb["command"] = self.game.careermenu

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        yes = loader.loadModel('models/buttons/yes')
        self.yesb = DirectButton(geom = (yes.find('**/yes'),
                                         yes.find('**/yeslight'),
                                         yes.find('**/yeslight'),
                                         yes.find('**/yeslight')),
                                 borderWidth = (0,0),
                                 frameColor = (0,0,0,0),
                                 command = self.getUserUpgrades,
                                 rolloverSound = None,
                                 clickSound = game.click,
                                 extraArgs = [True],
                                 scale = 0.3,
                                 pos = (-0.3, 0, 0))

        no = loader.loadModel('models/buttons/no')
        self.nob = DirectButton(geom = (no.find('**/no'),
                                        no.find('**/nolight'),
                                        no.find('**/nolight'),
                                        no.find('**/nolight')),
                                borderWidth = (0,0),
                                frameColor = (0,0,0,0),
                                command = self.getUserUpgrades,
                                rolloverSound = None,
                                clickSound = game.click,
                                extraArgs = [False],
                                scale = 0.3,
                                pos = (0.3, 0, 0))

    def getUserUpgrades(self, upgrades):
        self.game.userUpgrades = upgrades
        self.game.getCPUUpgrades()

    def destroy(self):
        self.inst.destroy()
        self.backb.destroy()
        self.exitb.destroy()
        self.yesb.destroy()
        self.nob.destroy()

class getCPUUpgrades(DirectObject):
    def __init__(self, game):
        self.game = game

        #Instructions

        self.inst = OnscreenText(text = 'Computer players use upgrades?',
                                 fg = (1,1,1,1),
                                 scale = 0.07,
                                 pos = (0, 0.3, 0))

        #Buttons
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        if self.game.sit == 3:
            self.backb["command"] = self.game.careermenu

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        yes = loader.loadModel('models/buttons/yes')
        self.yesb = DirectButton(geom = (yes.find('**/yes'),
                                         yes.find('**/yeslight'),
                                         yes.find('**/yeslight'),
                                         yes.find('**/yeslight')),
                                 borderWidth = (0,0),
                                 frameColor = (0,0,0,0),
                                 command = self.getCPUUpgrades,
                                 rolloverSound = None,
                                 clickSound = game.click,
                                 extraArgs = [True],
                                 scale = 0.3,
                                 pos = (-0.3, 0, 0))

        no = loader.loadModel('models/buttons/no')
        self.nob = DirectButton(geom = (no.find('**/no'),
                                        no.find('**/nolight'),
                                        no.find('**/nolight'),
                                        no.find('**/nolight')),
                                borderWidth = (0,0),
                                frameColor = (0,0,0,0),
                                command = self.getCPUUpgrades,
                                rolloverSound = None,
                                clickSound = game.click,
                                extraArgs = [False],
                                scale = 0.3,
                                pos = (0.3, 0, 0))

    def getCPUUpgrades(self, upgrades):
        self.game.CPUUpgrades = upgrades
        self.game.getReady('usermenu')

    def destroy(self):
        self.inst.destroy()
        self.backb.destroy()
        self.exitb.destroy()
        self.yesb.destroy()
        self.nob.destroy()

class getReady(DirectObject):
    def __init__(self, game, afterRaceAction):
        self.game = game
        #Instructions
        self.insttext = ''
        self.action = ''
        if self.game.sit != 6:
            self.insttext = 'Click to begin your race!'
            self.action = 'race'
        else:
            self.insttext = 'Click to begin your battle!'
            self.action = 'battle'
        self.inst = OnscreenText(text = self.insttext,
                                 fg = (1,1,1,1),
                                 scale = 0.07,
                                 pos = (0, 0.3, 0))

        #Buttons
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.game.usermenu,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0.8))
        if self.game.sit == 3:
            self.backb["command"] = self.game.careermenu

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        race = loader.loadModel('models/buttons/'+self.action)
        self.raceb = DirectButton(geom = (race.find('**/'+self.action),
                                          race.find('**/'+self.action+'light'),
                                          race.find('**/'+self.action+'light'),
                                          race.find('**/'+self.action+'light')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.game.Race,
                                  rolloverSound = None,
                                  clickSound = game.click,
                                  extraArgs = [afterRaceAction],
                                  scale = 0.4,
                                  pos = (0,0,0))

    def destroy(self):
        self.inst.destroy()
        self.backb.destroy()
        self.raceb.destroy()
        self.exitb.destroy()
        
class newShip(DirectObject):
    def __init__(self, game):
        self.game = game

        self.back = OnscreenImage(image = 'models/textures/instback.png',
                                  pos = (0,0,0),
                                  scale = (1, 1, 0.7))
        self.back.setTransparency(TransparencyAttrib.MAlpha)

        #text
        self.text = OnscreenText(text = 'Choose new ship',
                                 fg = (1,1,1,1),
                                 scale = 0.07,
                                 pos = (0,-0.8,0))

        #buttons
        positions = [(-0.6,0,0.3), (0,0,0.3), (0.6,0,0.3), (-0.6,0,-0.3), (0,0,-0.3), (0.6,0,-0.3)]
        self.buttons = []
        for i in range(6):
            tempb = loader.loadModel('models/buttons/ship'+str(i+1))
            tempbutton = DirectButton(geom = (tempb.find('**/ship'+str(i+1)),
                                               tempb.find('**/ship'+str(i+1)+'light'),
                                               tempb.find('**/ship'+str(i+1)+'light'),
                                               tempb.find('**/locked')),
                                      borderWidth = (0,0),
                                      frameColor = (0,0,0,0),
                                      command = self.selectShip,
                                      rolloverSound = None,
                                      clickSound = game.click,
                                      extraArgs = [i],
                                      scale = 0.5,
                                      pos = positions[i])
            self.buttons.append(tempbutton)
            found = False
            if self.game.user.ships[i] == 1:
                self.buttons[i]['state'] = DGG.DISABLED

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

    def selectShip(self, num):
        self.game.user.ships[num] = 1
        save(self.game.user)
        self.game.careermenu()

    def destroy(self):
        self.text.destroy()
        self.exitb.destroy()
        self.back.destroy()
        for b in self.buttons:
            b.destroy()

class afterRace(DirectObject):
    def __init__(self, game, afterRaceAction, text, finished, finishCredits, finishPlaces):
        self.game = game
        self.afterRaceAction = afterRaceAction
        self.finished = finished
        self.newWorld = False
        
        self.game.music.play()
        
        if self.finished and self.afterRaceAction == 'careermenu':
            self.game.user.race += 1
            if self.game.user.race > 5:
                self.game.user.race = 1
                if self.game.user.world == 'city':
                    self.game.user.world = 'mountain'
                elif self.game.user.world == 'mountain':
                    self.game.user.world = 'arctic'
                elif self.game.user.world == 'arctic':
                    self.game.user.world = 'lavaland'
                elif self.game.user.world == 'lavaland':
                    self.game.user.world = 'canyon'
                elif self.game.user.world == 'canyon':
                    self.game.user.world = 'championship'
                elif self.game.user.world == 'championship':
                    self.game.user.won = True
                    self.game.user.race = 5
                    self.afterRaceAction = 'credits'
                        
                if not self.game.user.won:
                    self.newWorld = True
            self.game.user.credits += finishCredits[finishPlaces[0]]
            self.game.user.cpu1Credits += finishCredits[finishPlaces[1]]
            self.game.user.cpu2Credits += finishCredits[finishPlaces[2]]
            self.game.user.cpu3Credits += finishCredits[finishPlaces[3]]
            self.game.user.cpu4Credits += finishCredits[finishPlaces[4]]
            self.game.user.cpu5Credits += finishCredits[finishPlaces[5]]
            
            user = self.game.user
            
            for i in range(4):
                if user.cpu1Upgrades[i] < user.upgrades[i]:
                    user.cpu1Upgrades[i] = user.upgrades[i]
                if user.cpu2Upgrades[i] < user.upgrades[i]:
                    user.cpu2Upgrades[i] = user.upgrades[i]
                if user.cpu3Upgrades[i] < user.upgrades[i]:
                    user.cpu3Upgrades[i] = user.upgrades[i]
                if user.cpu4Upgrades[i] < user.upgrades[i]:
                    user.cpu4Upgrades[i] = user.upgrades[i]
                if user.cpu5Upgrades[i] < user.upgrades[i]:
                    user.cpu5Upgrades[i] = user.upgrades[i]
            
            for i in range(1, 6):
                self.upgradeCPU(i)
                
            save(self.game.user)

        #black background

        self.back = OnscreenImage(image = 'models/textures/instback.png',
                                  pos = (0,0,0.4),
                                  scale = (1, 1, 0.3))
        self.back.setTransparency(TransparencyAttrib.MAlpha)
        
        #instructional text

        self.inst = OnscreenText(text = text,
                                 fg = (0,1,1,1),
                                 scale = 0.07,
                                 pos = (0,0.4,0))

        #buttons

        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))

        cont = loader.loadModel('models/buttons/continue')
        self.contb = DirectButton(geom = (cont.find('**/continue'),
                                          cont.find('**/continuelight'),
                                          cont.find('**/continuelight'),
                                          cont.find('**/continuelight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = self.cont,
                                  rolloverSound = None,
                                  clickSound = game.click,
                                  scale = 0.4,
                                  pos = (0.8*base.camLens.getAspectRatio(),0,-0.7))

        replay = loader.loadModel('models/buttons/replay')
        self.replayb = DirectButton(geom = (replay.find('**/replay'),
                                            replay.find('**/replaylight'),
                                            replay.find('**/replaylight'),
                                            replay.find('**/replaydisabled')),
                                    borderWidth = (0,0),
                                    frameColor = (0,0,0,0),
                                    command = self.game.Race,
                                    rolloverSound = None,
                                    clickSound = game.click,
                                    extraArgs = [afterRaceAction],
                                    scale = 0.4,
                                    pos = (-0.8*base.camLens.getAspectRatio(),0,-0.7))
        if afterRaceAction == 'careermenu' and finished:
            self.replayb['state'] = DGG.DISABLED
            
    def upgradeCPU(self, num):
        credits = 0
        upgrades = [0,0,0,0]
        user = self.game.user
        if num == 1:
            credits = user.cpu1Credits
            upgrades = user.cpu1Upgrades
        if num == 2:
            credits = user.cpu2Credits
            upgrades = user.cpu2Upgrades
        if num == 3:
            credits = user.cpu3Credits
            upgrades = user.cpu3Upgrades
        if num == 4:
            credits = user.cpu4Credits
            upgrades = user.cpu4Upgrades
        if num == 5:
            credits = user.cpu5Credits
            upgrades = user.cpu5Upgrades
            
        low = upgrades[0]
        lownum = 0
        for i in range(4):
            if upgrades[i] < low:
                low = upgrades[i]
                lownum = i
        if credits >= (low+1)*500 and low<5:
            credits -= (low+1)*500
            upgrades[lownum] += 1
            
        if num == 1:
            self.game.user.cpu1Credits = credits
            self.game.user.cpu1Upgrades = upgrades
        if num == 2:
            self.game.user.cpu2Credits = credits
            self.game.user.cpu2Upgrades = upgrades
        if num == 3:
            self.game.user.cpu3Credits = credits
            self.game.user.cpu3Upgrades = upgrades
        if num == 4:
            self.game.user.cpu4Credits = credits
            self.game.user.cpu4Upgrades = upgrades
        if num == 5:
            self.game.user.cpu5Credits = credits
            self.game.user.cpu5Upgrades = upgrades

    def cont(self):
        if self.afterRaceAction == 'usermenu':
            self.game.usermenu()
        elif self.newWorld:
            self.game.newShip() 
        elif self.afterRaceAction == 'careermenu':
            self.game.careermenu()
        elif self.afterRaceAction == 'credits':
            self.game.credits('careermenu')
    def destroy(self):
        self.back.destroy()
        self.inst.destroy()
        self.exitb.destroy()
        self.contb.destroy()
        self.replayb.destroy()
        
class Credits(DirectObject):
    def __init__(self, game, action):
        self.game = game
        self.action = action
        self.dist = 3.2
        
        self.x = 0
        self.y = -1.2
        
        credits_file = open('credits.txt', 'r')
        credits_text = credits_file.read()
        credits_file.close()
        
        self.words = OnscreenText(text = credits_text,
                                  pos = (self.x, self.y),
                                  scale = 0.07)
        
        exit = loader.loadModel('models/buttons/exit')
        self.exitb = DirectButton(geom = (exit.find('**/exit'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight'),
                                          exit.find('**/exitlight')),
                                  borderWidth = (0,0),
                                  frameColor = (0,0,0,0),
                                  command = sys.exit,
                                  rolloverSound = None,
                                  clickSound = None,
                                  scale = 0.1,
                                  pos = (0.955 * base.camLens.getAspectRatio(), 0, 0.93))
        
        back = loader.loadModel('models/buttons/back')
        self.backb = DirectButton(geom = (back.find('**/back'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight'),
                                          back.find('**/backlight')),
                                   borderWidth = (0,0),
                                   frameColor = (0,0,0,0),
                                   command = self.cont,
                                   rolloverSound = None,
                                   clickSound = game.click,
                                   scale = 0.3,
                                   pos = (-0.877*base.camLens.getAspectRatio(),0,0))
                                   
        self.updateTask = taskMgr.add(self.update, "update-credits")
        
    def update(self, task):
        self.y += .125*globalClock.getDt()
        if self.words is not None:
            self.words.setPos(self.x, self.y)
        
        if self.y > self.dist:
            self.cont()
            
        return task.cont
            
    def cont(self):
        taskMgr.remove("update-credits")
        if self.action == 'mainmenu':
            self.game.background.setImage('models/textures/mainback.png')
            self.game.openingscreen()
        else:
            self.game.background.setImage('models/textures/mainbackno.png')
            self.game.careermenu()
        
    def destroy(self):
        if self.words is not None:
            self.words.destroy()
        self.exitb.destroy()
        self.backb.destroy()

def save(user):
    file = open('saved/'+user.name+'.py', 'w')                          #open the save file
    file.write('class SavedGame:\n')                                    #initialize the file
    file.write('    def __init__(self):\n')                             #more initializing
    if user.won:
        file.write('        self.won = True\n')
    else:
        file.write('        self.won = False\n')
    file.write('        self.name = \''+user.name+'\'\n')              #save the player's name
    file.write('        self.credits = '+str(user.credits)+'\n')   #save the player's credits
    file.write('        self.world = \''+user.world+'\'\n')            #save the player's world
    file.write('        self.race = '+str(user.race)+'\n')         #save the player's race
    file.write('        self.upgrades = [')                             #save the player's upgrades
    for i in range(4):
        file.write(str(user.upgrades[i]))
        if i < 3:
            file.write(',')
        else:
            file.write(']\n')
    file.write('        self.ships = [')                            #save the player's ships
    for i in range(6):
        file.write(str(user.ships[i]))
        if i < 5:
            file.write(',')
        else:
            file.write(']\n')
    file.write('        self.cpu1Credits = '+str(user.cpu1Credits)+'\n')        #save cpu1's credits
    file.write('        self.cpu1Upgrades = [')                                 #save cpu1's upgrades
    for i in range(4):
        file.write(str(user.cpu1Upgrades[i]))
        if i < 3:
            file.write(',')
        else:
            file.write(']\n')
    file.write('        self.cpu2Credits = '+str(user.cpu2Credits)+'\n')        #save cpu2's credits
    file.write('        self.cpu2Upgrades = [')                                 #save cpu2's upgrades
    for i in range(4):
        file.write(str(user.cpu2Upgrades[i]))
        if i < 3:
            file.write(',')
        else:
            file.write(']\n')
    file.write('        self.cpu3Credits = '+str(user.cpu3Credits)+'\n')        #save cpu3's credits
    file.write('        self.cpu3Upgrades = [')                                 #save cpu3's upgrades
    for i in range(4):
        file.write(str(user.cpu3Upgrades[i]))
        if i < 3:
            file.write(',')
        else:
            file.write(']\n')
    file.write('        self.cpu4Credits = '+str(user.cpu4Credits)+'\n')        #save cpu4's credits
    file.write('        self.cpu4Upgrades = [')                                 #save cpu4's upgrades
    for i in range(4):
        file.write(str(user.cpu4Upgrades[i]))
        if i < 3:
            file.write(',')
        else:
            file.write(']\n')
    file.write('        self.cpu5Credits = '+str(user.cpu5Credits)+'\n')        #save cpu5's credits
    file.write('        self.cpu5Upgrades = [')                                 #save cpu5's upgrades
    for i in range(4):
        file.write(str(user.cpu5Upgrades[i]))
        if i < 3:
            file.write(',')
        else:
            file.write(']\n')
    file.close()
        
class SavedGame():
    def __init__(self, name):
        self.won = False
        self.name = name
        self.credits = 0
        self.world = 'city'
        self.race = 1
        self.upgrades = [0,0,0,0]
        self.ships = [0,1,0,0,0,0]
        self.cpu1Credits = 0
        self.cpu1Upgrades = [0,0,0,0]
        self.cpu2Credits = 0
        self.cpu2Upgrades = [0,0,0,0]
        self.cpu3Credits = 0
        self.cpu3Upgrades = [0,0,0,0]
        self.cpu4Credits = 0
        self.cpu4Upgrades = [0,0,0,0]
        self.cpu5Credits = 0
        self.cpu5Upgrades = [0,0,0,0]

game = Game()

run()
