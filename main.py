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
GREEN = Vec4(0, 1, 0, 1)
RED = Vec4(1, 0, 0, 1)

number_player = 1
number_turn = ""
board_pos = []
board_pos_value = []
board_dice = 0
sizeboard_entry = ""
players = []
gold_position = ""
players_object = []
scoreboards = []
list_square_color = []


class Game(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        global number_player
        global sizeboard_entry
        global coordPlayer
        self.keyMap = {
            "up": False,
        }

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.disableMouse()

        self.font = loader.loadFont("Fonts/Roboto-Bold.ttf")

        self.titleMenu = DirectDialog(frameSize=(-1.5, 1.5, -1.5, 1.5),
                                      fadeScreen=0.4,
                                      relief=DGG.FLAT,
                                      frameTexture="UI/background.jpg")
        self.optionMenu = DirectDialog(frameSize=(-1.5, 1.5, -1.5, 1.5),
                                       fadeScreen=0.4,
                                       relief=DGG.FLAT,
                                       frameTexture="UI/background.jpg")

        buttonImages = (
            loader.loadTexture("UI/button.png")
        )

        def addPlayer():
            global number_player
            if(number_player < 4):
                number_player += 1
                number_player_text.setText("Number of Player : " + str(number_player))

        def removePlayer():
            global number_player
            if(number_player > 1):
                number_player -= 1
                number_player_text.setText("Number of Player : " + str(number_player))

        title = DirectLabel(text="ChariotParty",
                            scale=0.1,
                            pos=(0, 0, 0),
                            parent=self.titleMenu,
                            relief=None,
                            text_font=self.font,
                            text_fg=(76, 178, 178, 1))

        btn = DirectButton(text="Start",
                           command=self.begin,
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
                           command=self.startGame,
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

        number_player_text = OnscreenText(text=f"Number of player : {number_player}", pos=(0, 0.50),
                         scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        number_turn_text = OnscreenText(text="Number of turn :", pos=(0, 0.30),
                         scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        size_board_text = OnscreenText(text="Board size :", pos=(0, 0.10),
                         scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        numberTurn = OnscreenText(text=number_turn, pos=(1, 0.5),
                                  scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)
        sizeBoard = OnscreenText(text=sizeboard_entry, pos=(1, 0),
                                 scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.optionMenu)

        # callback function to set  text

        def setNumberTurn(textEntered):
            numberTurn.setText(textEntered)

        def setSizeBoard(textEntered):
            sizeBoard.setText(textEntered)

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
        music = loader.loadMusic("Sounds/Musics/ambiance.ogg")
        square = loader.loadModel(
            "Models/cube.egg")

        # setPos(x,y,z) start x:right y:forward z:up
        self.camera.setPos(4, -25, 20)
        self.camera.setHpr(0, -30, 0)

        music.setLoop(True)
        music.play()

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])

        updateTask = taskMgr.add(self.update, "update")

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        global board_dice
        # Get the amount of time since the last update
        dt = globalClock.getDt()
        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.

        if self.keyMap["up"]:
            for i in range(0, number_player):
                self.movePlayer(players[i], players_object[i])
                self.applyEffect(players[i])
                self.updateScoreBoard(players[i], scoreboards[i])
        return Task.cont

    def movePlayer(self, player, player_object):
        random_move = randint(1, 6)
        index_board_player = next((index for (index, d) in enumerate(
            board_pos) if d["x"] == player["position"]["x"] and d["y"] == player["position"]["y"]), None)

        if (index_board_player + random_move) >= len(board_pos): 
            new_turn = (index_board_player + random_move) - len(board_pos)
            board_dice = board_pos[new_turn]
        else:
            board_dice = board_pos[index_board_player + random_move]
        player_object.setPos(board_dice["x"],
                           board_dice["y"], 2)
        player["position"] = {
            "x": int(player_object.getPos().x),
            "y": int(player_object.getPos().y),
            "z": int(player_object.getPos().z - 1)
        }

    def begin(self):
        self.titleMenu.hide()
        self.optionMenu.show()
    
    def startGame(self):
        self.optionMenu.hide()
        self.createBoard()
        self.effectSquare()
        self.createPlayer()
        self.createScoreBoard()
        self.placeGold()


    def createScoreBoard(self):
        for i in range(len(players)):
            player_scoreboard = OnscreenText(text=f"Player {players[i]['id']}   Charbon: {players[i]['carbon']} Gold: {players[i]['gold']}  Turn : {players[i]['turn']}", pos=(4, 14 - (i+2)), scale=1, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.render)
            scoreboards.append(player_scoreboard)
    
    def updateScoreBoard(self, player ,scoreboard):
        scoreboard.setText(f"Player {player['id']}   Charbon: {player['carbon']} Gold: {player['gold']}  Turn : {player['turn']}")

    # def updatePlayer(player, case_value):
    #     if case_value.getPos

    def placeGold(self):
        random_pos = board_pos[randint(1, len(board_pos))]
        gold = loader.loadModel(
            "Models/cube.egg")
        gold.setScale(0.5)
        gold.setColor(GREEN)
        gold.setPos(random_pos["x"], random_pos["y"], 2)
        gold.reparentTo(self.render)
        gold_position = gold.getPos()

    def createPlayer(self):
        for i in range(0, number_player):
            player = loader.loadModel(
                "Models/cube.egg")
            player.setScale(0.5)
            player.setColor(WHITE)
            player.setPos(4, 2, 2)
            coordPlayer = {
                "x": int(player.getPos().x),
                "y": int(player.getPos().y),
                "z": int(player.getPos().z - 1)
            }
            players.append(
                {"id": i, "position": coordPlayer, "carbon": 5, "gold": 0, "turn": 0})
            players_object.append(player)
            player.reparentTo(self.render)

    def createBoard(self):
        global sizeboard_entry
        self.optionMenu.hide()
        self.titleMenu.hide()

        random_position = randint(1, int(sizeboard_entry.get()))

        rangeBoard = int(int(sizeboard_entry.get())/4)
        for i in range(1, rangeBoard-1):
            square = loader.loadModel(
                "Models/cube.egg")
            square.setScale(0.5)
            square.setPos(2 + (i*2), 2, 1)

            coord = {
                "x": int(square.getPos().x),
                "y": int(square.getPos().y),
                "z": int(square.getPos().z)
            }
            board_pos_value.append(square)
            board_pos.append(coord)
            square.reparentTo(self.render)
        for i in range(1, rangeBoard-1):
            square = loader.loadModel(
                "Models/cube.egg")
            square.setScale(0.5)
            square.setPos(8, 2 + (i*2), 1)
            coord = {
                "x": int(square.getPos().x),
                "y": int(square.getPos().y),
                "z": int(square.getPos().z)
            }
            board_pos_value.append(square)
            board_pos.append(coord)
            square.reparentTo(self.render)
        for i in range(1, rangeBoard-1):
            square = loader.loadModel(
                "Models/cube.egg")
            square.setScale(0.5)
            square.setPos(8 - (i*2), 8, 1)
            coord = {
                "x": int(square.getPos().x),
                "y": int(square.getPos().y),
                "z": int(square.getPos().z)
            }
            board_pos_value.append(square)
            board_pos.append(coord)
            square.reparentTo(self.render)
        for i in range(rangeBoard-1):
            square = loader.loadModel(
                "Models/cube.egg")
            square.setScale(0.5)
            square.setPos(2, 8 - (i*2), 1)
            coord = {
                "x": int(square.getPos().x),
                "y": int(square.getPos().y),
                "z": int(square.getPos().z)
            }
            board_pos_value.append(square)
            board_pos.append(coord)
            square.reparentTo(self.render)

    def applyEffect(self, player):
        index_board_player = next((index for (index, d) in enumerate(
            board_pos) if d["x"] == player["position"]["x"] and d["y"] == player["position"]["y"]), None)
        
        result = list_square_color[index_board_player]
        if result == 1:
            player["carbon"]=3
        elif result == 2:
            player["carbon"]=0

    def effectSquare(self):
        for i in range(len(board_pos_value)):
            random_color = randint(1,3)
            if random_color == 1:
                board_pos_value[i].setColor(GREEN)
            elif random_color == 2:
                board_pos_value[i].setColor(RED)
            elif random_color == 3:
                board_pos_value[i].setColor(BLACK)
            list_square_color.append(random_color)
            # prob = [25,20,5,50]
            # random_color = random.choice(board, prob)
            # for i in range():
            #     board_pos_value.setColor(BLACK)
            #     print(random_color)

    def quit(self):
        base.userExit()


game = Game()
game.run()










# while (player["turn"] <= number_turn):

# A handy little function for getting the proper position for a given square

# def SquarePos(i):
#     return Point3((i % 8) - 3.5, int(i/8) - 3.5, 0)

# # Helper function for determining wheter a square should be white or black
# # The modulo operations (%) generate the every-other pattern of a chess-board
# def SquareColor(i):
#     if (i + ((i/8) % 2)) % 2:
#         return BLACK
#     else:
#         return WHITE

# def build_dict(seq, key):
#     return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

# info_by_name = build_dict(lst, key="name")
# tom_info = info_by_name.get("Tom")



        # def spinCameraTask(self, task):
        #     angleDegrees = task.time * 6.0
        #     angleRadians = angleDegrees * (pi / 180.0)
        #     self.camera.setPos(20 * sin(angleRadians), -
        #                        20.0 * cos(angleRadians), 3)
        #     self.camera.setHpr(angleDegrees, 0, 0)
        #     return Task.cont

        # self.taskMgr.add(spinCameraTask, "SpinCameraTask")


    # def color():
    #     random_color = randint(1, 3)
    #     if random_color == 1:
    #         color = Vec4(1, 1, 1, 1)
    #     elif random_color == 2:
    #         color = Vec4(50, 205, 50, 1)
    #     elif random_color == 3:
    #         color = Vec4(178, 34, 34, 1)
    #     return color

        # self.squareRoot = render.attachNewNode("squareRoot")
        # for i in range(int(sizeboard_entry.getNumCharacters())):
        #     # Load, parent, color, and position the model (a single square polygon)
        #     self.squares[i] = loader.loadModel(
        #         "Models/cube.egg")
        # self.squares[i].reparentTo(self.squareRoot)
        # self.squares[i].setPos(SquarePos(i))
        # self.squares[i].setColor(SquareColor(i))
