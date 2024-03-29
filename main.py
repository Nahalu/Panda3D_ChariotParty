from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.task import Task
from math import pi, sin, cos

import time
from random import *
from datetime import date
from Helpers.compare import *

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
number_turn_entry = ""
players = []
gold_position = {}
players_object = []
scoreboards = []
list_square_color = []
turn_text_object = []
i = 0
turn = 1


class Game(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)
        global number_player
        global sizeboard_entry
        global number_turn_entry

        self.keyMap = {
            "up": False,
            "a": False,
            "z": False,
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
        self.scoreboardResult = DirectDialog(frameSize=(-1.5, 1.5, -1.5, 1.5),
                                             fadeScreen=0.4,
                                             relief=DGG.FLAT,
                                             frameTexture="UI/end.jpg")

        self.buttonImages = (
            loader.loadTexture("UI/button.png")
        )

        def addPlayer():
            global number_player
            if(number_player < 4):
                number_player += 1
                number_player_text.setText(
                    "Number of Player : " + str(number_player))

        def removePlayer():
            global number_player
            if(number_player > 1):
                number_player -= 1
                number_player_text.setText(
                    "Number of Player : " + str(number_player))

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
                           frameTexture=self.buttonImages,
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
                           frameTexture=self.buttonImages,
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
                           frameTexture=self.buttonImages,
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
                           frameTexture=self.buttonImages,
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
                           frameTexture=self.buttonImages,
                           frameSize=(-1, 1, -1, 1),
                           text_scale=0.75,
                           relief=DGG.FLAT,
                           text_pos=(0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text="Export",
                           command=self.exportResult,
                           text_fg=(76, 178, 178, 1),
                           pos=(-0.3, 0, -0.4),
                           parent=self.scoreboardResult,
                           scale=0.07,
                           text_font=self.font,
                           clickSound=loader.loadSfx("Sounds/click.ogg"),
                           frameTexture=self.buttonImages,
                           frameSize=(-4, 4, -1, 1),
                           text_scale=0.75,
                           relief=DGG.FLAT,
                           text_pos=(0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text="Restart",
                           command=self.restartGame,
                           text_fg=(76, 178, 178, 1),
                           pos=(0.3, 0, -0.4),
                           parent=self.scoreboardResult,
                           scale=0.07,
                           text_font=self.font,
                           clickSound=loader.loadSfx("Sounds/click.ogg"),
                           frameTexture=self.buttonImages,
                           frameSize=(-4, 4, -1, 1),
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

        numberTurn = OnscreenText(text=number_turn_entry, pos=(1, 0.5),
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
        self.scoreboardResult.hide()
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])

        # Task manager to listen to keydown event
        updateTask = taskMgr.add(self.update, "update")

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        global i
        global turn
        global number_turn_entry
        # Get the amount of time since the last update
        dt = globalClock.getDt()
        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["a"]:
            self.acceptDeal(players[i])
            time.sleep(0.2)
        if self.keyMap["z"]:
            self.refuseDeal()
            time.sleep(0.2)
        if self.keyMap["up"]:
            if (turn == int(number_turn_entry.get())+1):
                self.scoreboardResult.show()
                self.showResult()
            else:
                if(i < number_player):
                    self.movePlayer(players[i], players_object[i])
                    self.applyEffect(players[i])
                    self.buyGold(players[i])
                    self.updateScoreBoard(players[i], scoreboards[i])
                    self.updateTurn(turn_text_object[0], turn)
                    i += 1
                elif i == number_player:
                    turn += 1
                    i = 0
            time.sleep(0.1)
        return Task.cont

    def showResult(self):
        compare(players)
        result_scoreboard = OnscreenText(text=f"Scoreboard :", pos=(0, 0.6), scale=0.07, fg=(
            255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.scoreboardResult)
        for i in range(len(players)):
            result_scoreboard = OnscreenText(text=f"Player {players[i]['id']}   Charbon: {players[i]['carbon']} Gold: {players[i]['gold']} ", pos=(
                0, 0.5 - (i/5)), scale=0.07, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.scoreboardResult)

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

    def showBuyUI(self, player):
        deal_text = OnscreenText(text=f"Do you want to buy ? '\n'( Cost 10 Carbons) '\n' Press a to accept '\n'Press z to refuse", pos=(-2, 0), scale=0.9, fg=(
            255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.render)
        self.acceptOnce("a", self.updateKeyMap, ["a", True])
        self.acceptOnce("a-up", self.updateKeyMap, ["a", False])
        self.acceptOnce("z", self.updateKeyMap, ["z", True])
        self.acceptOnce("z-up", self.updateKeyMap, ["z", False])

    def buyGold(self, player):
        global gold_position
        player_coord = {player["position"]["x"], player["position"]["y"]}
        print(player_coord)
        print(gold_position)
        if (gold_position == player_coord):
            if(player["carbon"] >= 10):
                self.showBuyUI(player)

    def acceptDeal(self, player):
        player["carbon"] -= 10
        player["gold"] += 1

        self.placeGold()

    def refuseDeal(self):
        deal_text.remove_node()

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
        self.createTurn()

    def restartGame(self):
        print("restart")

    def exportResult(self):

        file1 = open(f"chariot-party-{date.today()}.txt", "w")
        for i in range(len(players)):
            L = [
                f"Player : {players[i]['id']}, Gold : {players[i]['gold']}, Carbon : {players[i]['carbon']}  \n"]

            file1.writelines(L)

    def createScoreBoard(self):
        for i in range(len(players)):
            player_scoreboard = OnscreenText(text=f"Player {players[i]['id']}   Charbon: {players[i]['carbon']} Gold: {players[i]['gold']} ", pos=(
                4, 14 - (i+2)), scale=1, fg=(255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.render)
            scoreboards.append(player_scoreboard)

    def updateScoreBoard(self, player, scoreboard):
        scoreboard.setText(
            f"Player {player['id']}   Charbon: {player['carbon']} Gold: {player['gold']} ")

    def createTurn(self):
        turn_text = OnscreenText(text=f"Turn - 1", pos=(4, -4), scale=1, fg=(
            255, 250, 250, 1), align=TextNode.ACenter, mayChange=1, parent=self.render)
        turn_text_object.append(turn_text)

    def updateTurn(self, turn_text, turn):
        turn_text.setText(f"Turn - {turn}")

    def placeGold(self):
        global gold_position
        random_pos = board_pos[randint(0, len(board_pos))]
        gold = loader.loadModel(
            "Models/cube.egg")
        gold.setScale(0.5)
        gold.setColor(GREEN)
        gold.setPos(random_pos["x"], random_pos["y"], 2)
        gold.reparentTo(self.render)
        gold_position = {random_pos["x"], random_pos["y"]}

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
                {"id": i, "position": coordPlayer, "carbon": 5, "gold": 0})
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
        for i in range(1, rangeBoard-1):
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
            player["carbon"] += 3
        elif result == 2:
            if player["carbon"] <= 0:
                player["carbon"] = 0
            else:
                player["carbon"] -= 3

    def effectSquare(self):
        # prob = [25,20,5,50]
        # list_random_color = random.choice(len(board_pos_value), prob)
        for i in range(len(board_pos_value)):
            random_color = randint(1, 3)
            if random_color == 1:
                board_pos_value[i].setColor(GREEN)
            elif random_color == 2:
                board_pos_value[i].setColor(RED)
            elif random_color == 3:
                board_pos_value[i].setColor(BLACK)
            list_square_color.append(random_color)

    def quit(self):
        base.userExit()


game = Game()
game.run()
