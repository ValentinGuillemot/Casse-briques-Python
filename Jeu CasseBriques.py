#-*- coding : utf-8 -*-
#Importation du module nécessaire :
from tkinter import*

#*************
#********************************
#*************
# Fonction pour le déplacement de la plateforme :
def déplacement(event) :
    c = can.coords(figure) #Récupération des coordonnées de la plateforme pour vérifier si elle n'est pas au bord de la fenêtre de jeu
    if event.keysym == 'Left' and c[0]>5 : #Déplace la figure à gauche si le joueur appuie sur "Gauche" et si elle n'est pas déjà au bord de l'écran
        can.move(figure, -15, 0)
        can.move(centre, -15, 0)
    if event.keysym == 'Right' and c[0]<380 : #Fait la même chose pour la droite.
        can.move(figure, 15, 0)
        can.move(centre, 15, 0)

#*************
#Fonctions pour le déplacement de la balle :
def mouvement() :
    bouton2.config(state = NORMAL, text = 'Pause', command = stop)
    bouton3.config(state = NORMAL, text = 'Recommencer', command = reco)
    global balle, figure, jeu, vx, vy, echec, score #Appel de toutes les variables utilisées dans la fonction
    #Bloc codant l'arrêt du jeu si la balle a été manquée 3 fois
    if echec == 3:
        jeu = False
        print ("Vous avez perdu !")
        print ("Votre score est :", score)
        #label.pack(side = RIGHT)
        bouton1.config(state = DISABLED, text = 'Perdu')
        bouton2.config(state = DISABLED, text = score )
        bouton3.config(padx = 0)
    if jeu : #Si le jeu est en marche :
        can.move(balle, vx, vy) #Déplacement de la balle selon un mouvement vertical (vy) et horizontal (vx)
        place_b = can.coords(balle) #Récupère les coordonnées de la balle
        place_f = can.coords(figure) #Récupère les coordonnées de la plateforme
        if place_b[0]+70> 500 : #Fait rebondir la balle contre la paroi de droite 
            vx = -5
        if place_b[1]+70> 500 : #Fait rebondir la balle contre la paroi au niveau de la plateforme
            vy = -5
            echec += 1
            perte = 3-echec
            vitalite.delete(tentatives[perte])
            if score > 0 :
                score += -5
        if place_b[0]-5< 0 : #Fait rebondir la balle contre la paroi de gauche
            vx = 5
        if place_b[1]-5<0 : #Fait rebondir la balle contre la paroi à l'opposé de la plateforme
            vy = 5

            
    #Rebond contre la plateforme :
        if place_b[1]+20>place_f[1] and place_b[1]+20<place_f[1]+10 and place_f[0]-20 <= place_b[0] and place_b[0] <= place_f[2]-10 : #Si la balle se trouve au niveau de la plateforme, elle rebondit.
            vy = -5
            if place_f[0]+20 >= place_b[0] : #Si la balle touche la gauche de la plateforme, elle rebondit vers la gauche
                vx = -5
            if place_f[0]+35<= place_b[0] : #Si la balle touche la droite de la plateforme, elle rebondit vers la droite
                vx = 5
            if place_f[0]+20 < place_b[0] and place_b[0] < place_f[0]+35 : #Si la balle touche le milieu de la plateforme, elle rebondit en ligne droite.
                vx = 0

                
    #Rebond contre les briques (programmés du bas vers le haut) :
        impact(place_b, 140, 134, briques_c, rectangle_c, 1)
        impact(place_b, 105, 99, briques_c, rectangle_c, -1)

        impact(place_b, 100, 94, briques_b, rectangle_b, 1)
        impact(place_b, 65, 59, briques_b, rectangle_b, -1)

        impact(place_b, 60, 54, briques_a, rectangle_a, 1)
        impact(place_b, 25, 16, briques_a, rectangle_a, -1)
            
        #Arrêt du jeu si toutes les briques ont été détruites
        reussite = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if briques_a == reussite and briques_b == reussite and briques_c == reussite :
            print ("Vous avez gagné !")
            print ("La balle a été manquée", echec, "fois.")
            print ("Votre score est :", score)
            jeu = False
            bouton1.config(state = DISABLED, text = 'Gagné')
            bouton2.config(state = DISABLED, text = score)
        if jeu :
            can.after(10, mouvement) #La fonction s'appelle à nouveau toutes les 10 ms
    jeu = True #Permet de relancer la fonction même après l'avoir arrêtée avec le bouton Pause (défini plus tard)

def stop() : #Fonction pour arrêter le mouvement de la balle
    global jeu
    jeu = False #Modifie la valeur de la variable bouléenne qui permet le déplacement de la balle

def impact(place_b, dx, ddx, briques, rectangles, zone) :
    global vy, score
    if place_b[1] < dx and place_b[1] > ddx :
        x = 0
        while x <= 9 :
            y = 40*x
            if briques[x] > 0 :
                if place_b[0] >= 35+y and place_b[0] <= 75+y or place_b[2] >= 35+y and place_b[2] <= 75+y :
                    if briques[x] == 1 :
                        can.delete(rectangles[x])
                    else :
                        if briques[x] == 2 :
                            emp = can.coords(rectangles[x])
                            can.delete(rectangles[x])
                            rectangles[x] = can.create_rectangle(emp[0], emp[1], emp[2], emp[3], fill = 'yellow')
                        if briques[x] == 3 :
                            emp = can.coords(rectangles[x])
                            can.delete(rectangles[x])
                            rectangles[x] = can.create_rectangle(emp[0], emp[1], emp[2], emp[3], fill = 'orange')
                    vy = 5*zone
                    briques[x] += -1
                    score += 10
            x += 1
        
                
    



#Fonction pour recommencer le jeu
def reco() :
    bouton2.config(state = DISABLED, text = 'Pause', command = stop)
    bouton1.config(text = 'Jouer', state = NORMAL)
    bouton3.config(text = 'Recommencer', command = reco, state = DISABLED)
    global jeu, rectangle_a, rectangle_b, rectangle_c, briques_a, briques_b, briques_c, balle, score, x, y, dx, dy, vx, vy, centre, figure, echec
    compteur = 0
    while compteur < 10 :
        can.delete(rectangle_a[compteur])
        briques_a[compteur] = 0
        can.delete(rectangle_b[compteur])
        briques_b[compteur] = 0
        can.delete(rectangle_c[compteur])
        briques_c[compteur] = 0
        compteur += 1
    can.delete(figure)
    can.delete(centre)
    figure = can.create_rectangle(265, 415, 195, 410, fill='green')
    centre = can.create_rectangle(235, 415, 225, 410, fill='black')
    can.delete(balle)
    balle = can.create_oval(x, y, dx, dy, fill = 'red')
    if echec >= 1 :
        tentatives[2] = vitalite.create_oval(165, 2, 192, 28, fill = 'red')
        if echec >= 2 :
            tentatives[1] = vitalite.create_oval(91, 2, 118, 28, fill = 'red')
            if echec == 3 :
                tentatives[0] = vitalite.create_oval(18, 2, 45, 28, fill = 'red')
            
            
    echec = 0
    score = 0
    vx = 0
    vy = -5
    jeu = False
        
    
    briques_a=[1,2,3,3,3,3,3,3,2,1] #Chaine de briques la plus haute
    hauteur = 0
    rectangle_a = construire(briques_a, hauteur)
    briques_c = [1,2,3,2,1,1,2,3,2,1]  #Chaine de briques la moins haute suivant la même configuration que la première
    hauteur = 80
    rectangle_c = construire(briques_c, hauteur)
    briques_b=[1,2,3,2,1,1,2,3,2,1] #Chaine de briques centrale
    hauteur = 40
    rectangle_b = construire(briques_b, hauteur)
        

    
#********************************
# Fonctions pour la création des briques :

#Construction d'une brique à partir d'une variable :
def construction(x, z, briques, rectangle) : #Fonction prenant pour argument la position dans la liste (x), la coordonnée verticale (hauteur) de la chaine de brique et une liste de valeurs
    y = 40*x
    #Création d'une brique (représentée par un rectangle) en fonction d'une valeur.
    if briques[x] == 1 :
        rectangle.append (can.create_rectangle(35+y, 60+z, 75+y, 30+z, fill='yellow'))
    if briques[x] == 2 :
        rectangle.append (can.create_rectangle(35+y, 60+z, 75+y, 30+z, fill='orange'))
    if briques[x]== 3 :
        rectangle.append (can.create_rectangle(35+y, 60+z, 75+y, 30+z, fill='red'))
        
#Construction d'une ligne de briques à partir d'une chaîne de caractère :
def construire(briques, z) : #Prend pour argument une liste de nombres et une hauteur (position où la chaine de brique va apparaitre
    rectangle = []
    a = len(briques) #Récupération de la longueur de la chaine de caractère
    b = 0
    while b < a :
        construction(b, z, briques, rectangle) #Lecture de la liste de valeurs et création d'une brique pour chacun de ses éléments
        b += 1
    return rectangle

#Modification de la difficulté :

def difficile() :
    global briques_d, hauteur_d, briques_e, hauteur_e, nbc
    if nbc < 5 :
        bouton2.config(state = NORMAL)
        if nbc == 3 :
            briques_d=[1, 2, 3, 1, 1, 1, 1, 3, 2, 1]
            rectangle_d = construire(briques_d, hauteur_d)
        if nbc == 4 :
            briques_e = [1, 2, 3, 3, 3, 3, 3, 3, 2, 1]
            rectangle_e = construire(briques_e, hauteur_e)
        nbc += 1
    else :
        bouton3.config(state = DISABLED)
            
    
#*********************************
#Programme principal :

#Coordonnées initiales de la balle :
x = 221
y = 371
dx = 241
dy = 391
#Coordonnées de déplacement initial de la balle :
vx = 0 #Déplacement horizontal (la balle part en ligne droite au début du jeu)
vy = -5 #Déplacement vertical (la balle part vers le haut au début du jeu)

#Création de la fenêtre et du Canevas grâce à Tkinter :
fenetre = Tk()
fenetre.geometry("500x550+100+100")
fenetre.title("Jeu de Casse-briques")
can = Canvas(fenetre, width = 450, height = 450, bg = 'white')
can.pack(side = TOP)
vitalite = Canvas(fenetre, width = 210, height = 30, bg = 'white')
vitalite.pack(side = TOP)
tentatives = []
tentatives.append(vitalite.create_oval(18, 2, 45, 28, fill = 'red'))
tentatives.append(vitalite.create_oval(91, 2, 118, 28, fill = 'red'))
tentatives.append(vitalite.create_oval(165, 2, 192, 28, fill = 'red'))

#Création de la plateforme et de la balle :
figure = can.create_rectangle(265, 415, 195, 410, fill='green')
centre = can.create_rectangle(235, 415, 225, 410, fill='black') #Carré noir servant à repérer le centre de la plateforme pour aider l'utilisateur à faire rebondir la balle sur le côté désiré
fenetre.bind("<KeyPress>", déplacement)
balle = can.create_oval(x, y, dx, dy, fill='red')

#Création de boutons pour lancer et arrêter le jeu :
jeu = True #Variable bouléenne permettant le lancement et l'arrêt du jeu.
echec = 0
score = 0
bouton1 = Button(fenetre, text='Jouer', command = mouvement)
bouton2 = Button(fenetre, text = 'Pause', command = stop, state = DISABLED)
bouton3 = Button(fenetre, text = '+ Dur', command = difficile, state = DISABLED)
bouton1.pack(side = LEFT, padx = 90)
bouton2.pack(side = LEFT)
bouton3.pack(side = LEFT, padx = 75)

#Création des briques :
briques_a=[1,2,3,3,3,3,3,3,2,1] #Chaine de briques la plus haute
hauteur = 0
rectangle_a = construire(briques_a, hauteur)
briques_c = [1,2,3,2,1,1,2,3,2,1]  #Chaine de briques la moins haute suivant la même configuration que la première
hauteur = 80
rectangle_c = construire(briques_c, hauteur)
briques_b=[1,2,3,1,1,1,1,3,2,1] #Chaine de briques centrale
hauteur = 40
rectangle_b = construire(briques_b, hauteur)

nbc = 3

briques_d=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hauteur_d = 120
rectangle_d = construire(briques_d, hauteur_d)
briques_e = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
hauteur_e = 160
rectangle_e = construire(briques_e, hauteur_e)

fenetre.mainloop
