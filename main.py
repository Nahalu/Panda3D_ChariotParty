from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.task import Task
from math import pi, sin, cos

from random import *

BLACK = Vec4(0, 0, 0, 1)
WHITE = Vec4(1, 1, 1, 1)
HIGHLIGHT = Vec4(0, 1, 1, 1)
PIECEBLACK = Vec4(.15, .15, .15, 1)

number_player = 0
gold_position = 24
list_player = []
board = []
board_case_value = []
number_turn = ""
sizeboard_entry = ""


class Game(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        global number_player
        global sizeboard_entry
        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.disableMouse()

        # def spinCameraTask(self, task):
        #     angleDegrees = task.time * 6.0
        #     angleRadians = angleDegrees * (pi / 180.0)
        #     self.camera.setPos(20 * sin(angleRadians), -
        #                        20.0 * cos(angleRadians), 3)
        #     self.camera.setHpr(angleDegrees, 0, 0)
        #     return Task.cont

        # self.taskMgr.add(spinCameraTask, "SpinCameraTask")

        self.font = loader.loadFont("Fonts/Roboto-Bold.ttf")

        self.titleMenu = DirectDialog(frameSize=(-1.5, 1.5, -1.5, 1.5),
                                      fadeScreen=0.4,
                                      relief=DGG.FLAT,
                                      frameTexture="UI/background.jpg")
        self.optionMenu = DirectDialog(frameSize=(-1.5, 1.5, -1.5, 1.5),
                                       fadeScreen=0.4,
                                       relief=DGG.FLAT,
                                       frameTexture="UI/background.jpg")
        # self.gameBoard = DirectDialog(frameSize=(-1, 1, -1, 1),
        #                               fadeScreen=0.4,
        #                               relief=DGG.FLAT,
        #                               frameTexture="UI/background.jpg")

        buttonImages = (
            loader.loadTexture("UI/button.png"),
            loader.loadTexture("UI/button.png"),
            loader.loadTexture("UI/button.png"),
            loader.loadTexture("UI/button.png")
        )

        def addPlayer():
            global number_player
            if(number_player < 4):
                number_player += 1
                a.setText("Number of Player : " + str(number_player))

        def removePlayer():
            global number_player
            if(number_player > 0):
                number_player -= 1
                a.setText("Number of Player : " + str(number_player))

        title = DirectLabel(text="ChariotParty",
                            scale=0.1,
                            pos=(0, 0, 0),
                            parent=self.titleMenu,
                            relief=None,
                            text_font=self.font,
                            text_fg=(76, 178, 178, 1))

        btn = DirectButton(text="Start",
                           command=self.startGame,
                           text_fg=(76, 178, 178, 1),
                           pos=(-0.3, 0, -0.2),
                           parent=self.titleMenu,
                           scale=0.07,
                           text_font=self.font,
                           clickSound=loader.loadSfx("Sounds/click.ogg"),
                           frameTexture=buttonImages,
                           frameSize=(-4, 4, -1, 1),
                           text_scale=0.75,
                           relief=DGG.FLAT,
                           text_pos=(0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text="Quit",
                           command=self.quit,
                           text_fg=(76, 178, 178, 1),
                           pos=(0.3, 0, -0.2),
                           parent=self.titleMenu,
                           scale=0.07,
                           text_font=self.font,
                           clickSound=loader.loadSfx("Sounds/click.ogg"),
                           frameTexture=buttonImages,
                           frameSize=(-4, 4, -1, 1),
                           text_scale=0.75,
                           relief=DGG.FLAT,
                           text_pos=(0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text="Start",
                           command=self.initBoard,
                           text_fg=(76, 178, 178, 1),
                           pos=(0, 0, -0.2),
                           parent=self.optionMenu,
                           scale=0.07,
                           text_font=self.font,
                           clickSound=loader.loadSfx("Sounds/click.ogg"),
                           frameTexture=buttonImages,
                           frameSize=(-4, 4, -1, 1),
                           text_scale=0.75,
                           relief=DGG.FLAT,
                           text_pos=(0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text="+",
                           command=addPlayer,
                           text_fg=(76, 178, 178, 1),
                           pos=(-0.1, 0, 0.41),
                           parent=self.optionMenu,
                           scale=0.07,
                           text_font=self.font,
                           clickSound=loader.loadSfx("Sounds/click.ogg"),
                           frameTexture=buttonImages,
                           frameSize=(-1, 1, -1,    1),
                           text_scale=0.75,
                           relief=DGG.FLAT,
                           text_pos=(0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text="-",
                           command=removePlayer,
                           text_fg=(76, 178, 178, 1),
                           pos=(0.1, 0, 0.41),
                           parent=self.optionMenu,
                           scale=0.07,
                           text_font=self.font,
                           clickSound=loader.loadSfx("Sounds/click.ogg"),
                           frameTexture=buttonImages,
                           frameSize=(-1, 1, -1, 1),
                           text_scale=0.75,
                           relief=DGG.FLAT,
                           text_pos=(0, -0.2))
        btn.setTransparency(True)

        # add some text

        a = OnscreenText(text=f"Number of player : {number_player}", pos=(0, 0.50),
                         scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        b = OnscreenText(text="Number of turn :", pos=(0, 0.30),
                         scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        c = OnscreenText(text="Board size :", pos=(0, 0.10),
                         scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        numberTurn = OnscreenText(text=number_turn, pos=(1, 0.5),
                                  scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)
        sizeBoard = OnscreenText(text=sizeboard_entry, pos=(1, 0.5),
                                 scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        for i in range(1, 5):
            textObject = OnscreenText(text=number_turn, pos=(1, 0.45 * -i/2),
                                      scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        # callback function to set  text

        def setNumberTurn(textEntered):
            textObject.setText(textEntered)

        def setSizeBoard(textEntered):
            textObject.setText(textEntered)

        # clear the text

        def clearTextSize():
            sizeboard_entry.enterText('')

        def clearTextTurn():
            number_turn_entry.enterText('')

        # add text entry
        sizeboard_entry = DirectEntry(text="", width=15, pos=(-0.35, 0, 0), scale=.05, command=setSizeBoard,
                                      initialText="", numLines=1, focus=1, focusInCommand=clearTextSize, clickSound=loader.loadSfx("Sounds/click.ogg"), parent=self.optionMenu,)
        number_turn_entry = DirectEntry(text="", scale=.05, width=15, pos=(-0.35, 0, 0.20), command=setNumberTurn,
                                        initialText="", numLines=1, focusInCommand=clearTextTurn, parent=self.optionMenu)

        self.optionMenu.hide()
        self.scene = self.loader.loadModel("models/environment")
        # self.gameBoard.hide()
        music = loader.loadMusic("Sounds/Musics/ambiance.ogg")
        square = loader.loadModel(
            "Models/cube.egg")

        for i in range(20):
            square = loader.loadModel(
                "Models/cube.egg")
            square.setScale(0.5)
            square.setColor(BLACK)
            square.setPos(-5 * i/3, 1, -1)
            square.reparentTo(self.render)

        # tex = loader.loadTexture('Models/dice_1.rgb')
        # square.setTexture(tex, 1)

        self.camera.setPos(0, -20, 0)
        self.camera.setHpr(10, 10, 0)
        # self.camera.reparentTo(self.gameBoard)

        music.setLoop(True)
        # music.setVolume(0.075)
        music.play()

    # A handy little function for getting the proper position for a given square
    def SquarePos(i):
        return Point3((i % 8) - 3.5, int(i/8) - 3.5, 0)

    # Helper function for determining wheter a square should be white or black
    # The modulo operations (%) generate the every-other pattern of a chess-board
    def SquareColor(i):
        if (i + ((i/8) % 2)) % 2:
            return BLACK
        else:
            return WHITE

    def startGame(self):
        self.titleMenu.hide()
        # self.gameBoard.hide()
        self.optionMenu.show()

    def initBoard(self):
        self.optionMenu.hide()
        self.titleMenu.hide()
        # self.gameBoard.show()
        for i in range(1, number_player):
            list_player.append(
                {'id': i, 'position': 0, 'carbon': 0, 'gold': 0})
        board = [0 for x in range(int(sizeboard_entry.getNumCharacters()))]
        random_position = randint(1, int(sizeboard_entry.getNumCharacters()))

        for i in board:
            random_color = randint(1, 3)
            board_case_value.append(random_color)
        # self.squareRoot = render.attachNewNode("squareRoot")
        # for i in range(int(sizeboard_entry.getNumCharacters())):
        #     # Load, parent, color, and position the model (a single square polygon)
        #     self.squares[i] = loader.loadModel(
        #         "Models/cube.egg")
            # self.squares[i].reparentTo(self.squareRoot)
            # self.squares[i].setPos(SquarePos(i))
            # self.squares[i].setColor(SquareColor(i))

    def quit(self):
        base.userExit()


game = Game()
game.run()
