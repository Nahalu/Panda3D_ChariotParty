import turtle
from turtle import Shape
from tkinter import PhotoImage
from random import *

# definit le dossier où sont les images
dir = "img/"

# taille des images en pixels
imgSize = 100
played = False
# definit la taille de l'ecran
turtle.setup(1000, 1500)
screen = turtle.Screen()

# Images correspondantes aux cases
green = dir+"cases/green.gif"
screen.addshape(green)
red = dir+"cases/red.gif"
screen.addshape(red)
blue = dir+"cases/blue.gif"
screen.addshape(blue)

imagesCases = [green, red, blue]

# Image de l'or
imageGold = dir + "others/gold.gif"
screen.addshape(imageGold)

# Images du dés
imagesDice = []
for i in range(1, 6):
    imgPath = dir + "dices/dice_" + str(i) + ".gif"
    smaller = PhotoImage(file=imgPath).subsample(3, 3)
    screen.addshape(imgPath, Shape("image", smaller))
    imagesDice += [imgPath, ]

# Images des joueurs
imagesJoueurs = []
for i in range(1, 5):
    imgPath = dir + "persos/j" + str(i) + ".gif"
    screen.addshape(imgPath)
    imagesJoueurs += [imgPath, ]

# Listes de stockage des turtles du plateau
turtles = []
perso = []
players = []
score = turtle.Turtle()
turtle_star = turtle.Turtle()
turtle_dice = turtle.Turtle()


def cherchePlace(indice, plateau):
    """
    Cherche les coordonnées d'une case sur l'écran correspondant à un indice du plateau.
    :param ind: (int) l'indice pour lequel on cherche la place.
    :param plateau: (list) liste d'entiers correspondant au plateau.
    :return: (float,float) les coordonnées de la case
    :CU: -1 < ind < len(plateau)
    """
    side_size = len(plateau)/4
    x_size = -((side_size+1)*imgSize)/2+(imgSize / 2)
    y_size = ((side_size+1)*imgSize)/2-(imgSize / 2)
    if(indice <= side_size):
        x = indice
        y = 0
    elif(indice < 2*side_size):
        x = side_size
        y = indice-side_size
    elif(indice < 3*side_size):
        x = side_size-(indice % side_size)
        y = side_size
    else:
        x = 0
        y = side_size-(indice % side_size)

    return(x_size+(x*imgSize), y_size-(y*imgSize))


def creePlateau(plateau):
    """
    Crée le plateau sur l'écran. Le plateau est décrit par une liste d'entiers.
    :param plateau: (list) liste d'entiers correspondant au plateau à dessiner.
    Un 1 dans la liste correspond à une case verte, un 2 correspond à une case rouge et un 3 à une case bleue.
    :return: (None)
    :CU: len(plateau) doit être un multiple de 4
    """
    for i in range(len(plateau)):
        x, y = cherchePlace(i, plateau)
        case = plateau[i]
        if(case > 0):
            t = turtle.Turtle()
            turtles.append(t)
            t.speed(0)
            t.up()
            t.goto(x, y)
            t.down()
            t.shape(imagesCases[plateau[i]-1])


def creeJoueurs(joueurs, plateau):
    """
    Ajoute les joueurs sur le plateau.
    :param joueurs: (list) liste de dictionnaires.
    :param plateau: (list) liste d'entiers correspondant au plateau.
    :return: (None)
    :CU: chaque dictionnaire doit contenir une clé "position" correspondant à une position sur le plateau m.
    Pour chaque dictionnaire de joueurs, -1 < j["position"] < len(plateau)
    """

    for p in range(len(joueurs)):
        i = joueurs[p]["position"]

        x, y = cherchePlace(i, plateau)
        t = turtle.Turtle()
        perso.append(t)
        t.speed(0)
        t.up()
        t.goto(x, y)
        t.down()
        t.shape(imagesJoueurs[p])


def effacePlateau():
    """
    Efface tous les éléments du plateau (or, joueurs, cases).
    """
    for i in range(len(turtles)):
        t = turtles.pop()
        t.clear()
        t.ht()
    for j in range(len(perso)):
        t = perso.pop()
        t.clear()
        t.ht()
    turtle_star.reset()


def placeOr(indice, plateau):
    """
    Place l'or sur le plateau.
    :param indice: (int) indice de la case où doit être positionnée l'or.
    :param plateau: (list) liste d'entiers correspondant au plateau.
    :return: (None)
    :CU: -1 < ind < len(plateau)
    """
    x, y = cherchePlace(indice, plateau)
    turtle_star.speed(0)
    turtle_star.up()
    turtle_star.goto(x, y)
    turtle_star.down()
    turtle_star.shape(imageGold)


def bougeJoueur(joueur, plateau):
    """
    Modifie la position d'un joueur sur le plateau.
    :param joueur: Dictionnaire d'un joueur.
    :param plateau: (list) liste d'entiers correspondant au plateau.
    :return: (None)
    :CU: le dictionnaire doit contenir une clé "position" correspondant à une position sur le plateau et une clé "id" correspondant à l'indice du joueur.
    -1 < joueur["position"] < len(plateau)
    """
    x, y = cherchePlace(joueur["position"], plateau)
    t = perso[joueur["id"]]
    t.up()
    t.goto(x, y)
    t.down()


def addPlayerScoreBoard(list_player):

    for p in range(len(list_player)):

        player = list_player[p]
        t = turtle.Turtle()
        players.append(t)
        t.speed(0)
        t.up()
        t.goto(600, 1 + (p * 120))
        t.down()
        t.color('white')
        style = ('Courier', 30, 'bold')
        t.write(f'{player["name"]}\nCharbon : {player["carbon"]} Or : {player["gold"]} ',
                font=style, align='center')


def updateScoreBoard(player):

    t = players[player["id"]]
    t.clear()
    style = ('Courier', 30, 'bold')
    t.write(f'{player["name"]}\nCharbon : {player["carbon"]} Or : {player["gold"]} ',
            font=style, align='center')


def addDice():
    turtle_dice.speed(0)
    turtle_dice.up()
    turtle_dice.goto(0, 0)
    turtle_dice.down()
    turtle_dice.shape(imagesDice[0])


def roll_dice_result():
    dice_result = randint(1, 6)
    updateDiceScore(dice_result)
    played = True


def active_dice(bool):
    global screen
    global played
    if(bool == True):
        while played != True:
            screen.onkey(roll_dice_result, "Return")
            played = False
            return True
            break
    else:
        return False


def updateDiceScore(dice_result):
    for i in range(1, 6):
        if (i == dice_result):
            turtle_dice.clear()
            turtle_dice.shape(imagesDice[i-1])
            turtle_dice.onclick(None)


def addTurnScore():
    score.speed(0)
    score.up()
    score.goto(0, 400)
    score.down()
    score.color('black')
    style = ('Courier', 40, 'bold')
    score.write(f'Round 1 ',
                font=style, align='center')


def updateTurnScore(number_of_turn):
    score.clear()
    style = ('Courier', 40, 'bold')
    score.write(f'Round {number_of_turn} ',
                font=style, align='center')

# TRI A BULLE
# flag = True
# while flag == True:
#     flag = False
#     for i in range(len(T)-1):
#         if comp(T[i], T[i+1]) == -1:
#             comp = T[i+1]
#             T[i+1] = T[i]
#             T[i] = comp
#             flag = True
