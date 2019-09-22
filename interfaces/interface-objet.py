import turtle

#definit le dossier où sont les images
dir = "img/"

#taille des images en pixels
imgSize = 100

#definit la taille de l'ecran
turtle.setup(1000,1000)
screen = turtle.Screen()

#Images correspondantes aux cases
green = dir+"cases/green.gif"
screen.addshape(green)
red = dir+"cases/red.gif"
screen.addshape(red)
blue = dir+"cases/blue.gif"
screen.addshape(blue)
yellow = dir+"cases/yellow.gif"
screen.addshape(yellow)

imagesCases=[green,red,blue,yellow]

#Image de l'or
imageGold = dir+"others/gold.gif"
screen.addshape(imageGold)

#Images des joueurs
imagesJoueurs = []
for i in range(1,5):
    imgPath = dir + "persos/j" + str(i) + ".gif"
    screen.addshape(imgPath)
    imagesJoueurs += [imgPath,]

#Listes de stockage des turtles du plateau
turtles = []
perso = []
turtle_star=turtle.Turtle()

def cherchePlace(indice, plateau):
    """
    Cherche les coordonnées d'une case sur l'écran correspondant à un indice du plateau.
    :param ind: (int) l'indice pour lequel on cherche la place.
    :param plateau: (list) liste d'entiers correspondant au plateau.
    :return: (float,float) les coordonnées de la case
    :CU: -1 < ind < len(plateau)
    """
    side_size = len(plateau)/4
    x_size=-((side_size+1)*imgSize)/2+(imgSize / 2)
    y_size=((side_size+1)*imgSize)/2-(imgSize / 2)
    if(indice <= side_size):
        x = indice
        y = 0
    elif(indice < 2*side_size):
        x = side_size
        y = indice-side_size
    elif(indice < 3*side_size):
        x = side_size-(indice%side_size)
        y = side_size
    else:
        x = 0
        y = side_size-(indice%side_size)
            
    return(x_size+(x*imgSize),y_size-(y*imgSize))

def creePlateau(plateau):
    """
    Crée le plateau sur l'écran. Le plateau est décrit par une liste d'entiers.
    :param plateau: (list) liste d'entiers correspondant au plateau à dessiner.
    Un 1 dans la liste correspond à une case verte, un 2 correspond à une case rouge et un 3 à une case bleue.
    :return: (None)
    :CU: len(plateau) doit être un multiple de 4
    """
    for i in range(len(plateau)):
        x,y=cherchePlace(i,plateau) 
        case = plateau[i]
        if(case.couleur > 0):
            t = turtle.Turtle()
            turtles.append(t)
            t.speed(0)
            t.up()
            t.goto(x,y)
            t.down()
            t.shape(imagesCases[plateau[i].couleur-1])
            
            
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
        i = joueurs[p].position
        
        x,y=cherchePlace(i,plateau)
        t = turtle.Turtle()
        perso.append(t)
        t.speed(0)
        t.up()
        t.goto(x,y)
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
        t=perso.pop()
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
    x,y=cherchePlace(indice,plateau)
    turtle_star.speed(0)
    turtle_star.up()
    turtle_star.goto(x,y)
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
    x,y=cherchePlace(joueur.position,plateau)
    t = perso[joueur.id]
    t.up()
    t.goto(x,y)
    t.down()