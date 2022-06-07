import tkinter
from math import cos, sin, pi
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

x = []  # création des variables globales x, z, time et varz en dehors de la fonction refresh()
z = []
time = []
varz = []
varx = []

# Fonction physique calculant la trajectoire
def trajectoire(angle, vitesse, hauteur):
    g = 9.81  # accelération de la pesanteur (m/s²)
    v_init = vitesse  # vitesse de départ (m/s)
    a = angle  # angle de départ (°)
    if angle == 90 or angle == -90:  # à x0 = 0, la trajectoire pour a = 90° est fausse...
        x0 = 1  # ...On lui donne donc une autre valeur...
    else:
        x0 = 0  # point de départ (m)
    z0 = hauteur  # hauteur de départ (m)
    tau = 0.1  # fréquence d'affichage des points

    dx = x0
    dz = z0
    t = 0  # s
    t_list = [t]  # liste contenant le temps, utile pour les autres graphs

    vx = v_init * cos(a * pi / 180)
    vz = v_init * sin(a * pi / 180)
    vxlist = [vx]
    vzlist = [vz]  # liste contenant les variations de z, utilisé pour les autres graphs
    # x et z sont des variables de type float, qu'il faut stocker dans des listes si on veut effectuer des traces
    xliste = [dx]
    zliste = [dz]
    i = 0  # compteur

    # Calcul pas à pas des valeurs prises par t, x, z, vz (vx est constante)...
    while dz >= 0:
        dx += vx * tau
        dz += + vz * tau
        t += tau
        vz = vz - g * tau
        t_list.append(t)
        vzlist.append(abs(vz))
        vxlist.append(vx)
        # Stockage des valeurs calculees dans les listes creees
        xliste.append(dx)
        zliste.append(dz)

        i = i + 1
    if angle == 90 or angle == -90:  # ...avant de corriger la courbe
        for i in range(len(xliste)):
            xliste[i] = 0
    return xliste, zliste, t_list, vzlist, vxlist


# INTERFACE TKINTER ----------------------------------------------------------------------------------------------

# Fonctions Tkinter x Matplotlib permettant de mettre à jour l'interface
def refresh():
    global x, z, time, varz, varx  # Permet d'utiliser les listes des valeurs x et z sans appel de fonction
    alph = alpha.get()
    spd = v0.get()  # impossible à convertir directement en int (cas où entrée="")
    high = h.get()  # ^ même situation ^
    if len(spd) == 0:  # Cas où l'entrée est vide (spd/high est tjr un string)
        spd = 10
    if len(high) == 0:
        high = 10
    spd = int(spd)
    high = int(high)

    x,z,time,varz,varx= trajectoire(alph,spd,high)
    sub.clear()  # retire les points du graph...
    sub.plot(x, z, 'k1')  # ... puis attribue de nouvelles valeurs à la courbe
    sub.set_title('Trajectoire')  # titre graph
    sub.set_ylabel('hauteur (m)')  # titre ord
    sub.set_xlabel('distance (m)')  # titre abs
    graph.draw()


def gravity():  # Affiche les vecteurs gravité
    points = [x, z]  # Liste contenant des couples de données
    if len(points[0]) != 0:
        echelle = max(x) / 9  # Echelle pour rendre les vecteurs plus visible
        if check_grav.get() == 1:  # Quand le bouton est on ...
            for i in range(len(x)):
                if i % 3 == 0:
                    sub.arrow(points[0][i], points[1][i], 0, -echelle, width=0.01,
                              color='red')  # création vecteur gravité
                    graph.draw()  # afficher les vecteurs
        else:  # Quand le bouton est off ...
            for i in range(len(x)):
                if i % 3 == 0:
                    sub.arrow(points[0][i], points[1][i], 0, -echelle, width=0.3 * echelle / 9,
                              color='white')  # "Masque" les vecteurs
                    graph.draw()
    else:  # cas où le graphique n'est pas encore tracé
        sub.set_title('Erreur: Pas de valeurs')
        graph.draw()


def vite():
    points = [x, z]  # Liste contenant le couple de données x et z
    tau = 0.1
    if len(points[0]) != 0:
        if check_vite.get() == 1:  # Quand le bouton est on ...
            for i in range(len(x)):
                if i % 3 == 0:
                    try:
                        vx = (x[i + 1] - x[i]) / tau
                        vz = (z[i + 1] - z[i]) / tau
                        sub.quiver(points[0][i], points[1][i], vx, vz, width=0.01, color='purple',
                                   headwidth=2)  # création vecteur direction
                        graph.draw()  # afficher les vecteurs
                    except IndexError:
                        pass
        else:  # Quand le bouton est off ...
            try:
                for i in range(len(x)):
                    sub.quiver(points[0][i], points[1][i], points[0][i + 1], points[1][i + 1], width=0.3,
                               color='white')  # "Masque" les vecteurs
                    graph.draw()
            except IndexError:
                pass
    else:  # cas où le graphique n'est pas encore tracé
        sub.set_title('Erreur: Pas de valeurs')
        graph.draw()


def deselect():  # déselectionne les options vecteur gravité / vitesse
    gravite.deselect()
    vecteur.deselect()


def multi_graph(): #création d'une fenètre avec différents graphiques
    global mult
    mult = tkinter.Tk(className=' Autres graphiques... ')

    x_t = Figure(figsize=(3, 2), dpi=100)
    z_t = Figure(figsize=(3, 2), dpi=100)
    vx = Figure(figsize=(3, 2), dpi=100)
    vz = Figure(figsize=(3, 2), dpi=100)

    x_t_sub = x_t.add_subplot(111)
    z_t_sub = z_t.add_subplot(111)
    vx_sub = vx.add_subplot(111)
    vz_sub = vz.add_subplot(111)

    x_t_sub.plot(time, x, 'r.')
    z_t_sub.plot(time, z, 'r.')
    vx_sub.plot(time, varx, 'r.')
    vz_sub.plot(time, varz, 'r.')

    x_t_sub.set_title('X en fonction du temps')
    z_t_sub.set_title('Z en fonction du temps')
    vx_sub.set_title('varX en fonction du temps')
    vz_sub.set_title('varZ en fonction du temps')

    x_t.patch.set_facecolor('#1D2384')
    z_t.patch.set_facecolor('#1D2384')
    vx.patch.set_facecolor('#1D2384')
    vz.patch.set_facecolor('#1D2384')

    FigureCanvasTkAgg(x_t, master=mult).get_tk_widget().grid(column=1, row=1)
    FigureCanvasTkAgg(z_t, master=mult).get_tk_widget().grid(column=1, row=2)
    FigureCanvasTkAgg(vx, master=mult).get_tk_widget().grid(column=2, row=1, sticky=tkinter.E)
    FigureCanvasTkAgg(vz, master=mult).get_tk_widget().grid(column=2, row=2, sticky=tkinter.E)

    mult.resizable(width=False, height=False)  # contraint la fenêtre à garder sa résolution
    mult.geometry("600x400")
    mult.mainloop()


# Création de la fenêtre
window = tkinter.Tk(className=' Simulation - Chute Libre')

# Création du plot vide
fig = Figure(figsize=(5, 4), dpi=100)
sub = fig.add_subplot(111)
sub.plot()  # plot du graph
fig.patch.set_facecolor('#1D2384')  # couleur du bg graph

graph = FigureCanvasTkAgg(fig, master=window)
graph.get_tk_widget().pack(side='right')

# Définition des boutons et objets à interagir
check_grav = tkinter.IntVar()  # variable bool indiquant l'état du checkbutton gravité
check_vite = tkinter.IntVar()  # variable bool indiquant l'état du checkbutton vecteur

text_vitesse = tkinter.Label(window, text='Vitesse initiale (m/s) :', bg='#895131', fg="#FFFFFF")
v0 = tkinter.Entry(window, bg='#FFD7C0')
text_alpha = tkinter.Label(window, text='Angle initial (°) :', bg='#895131', fg="#FFFFFF")
alpha = tkinter.Scale(window, orient='horizontal', from_=-90, to=90, bg='#FFC7A5', troughcolor='white')
text_hauteur = tkinter.Label(window, text='Hauteur (m) :', bg='#895131', fg="#FFFFFF")
h = tkinter.Entry(window, bg='#FFD7C0')

valider = tkinter.Button(window, text='Valider', command=lambda: [refresh(), deselect(), mult.withdraw()], bg='#895131',
                         fg="#FFFFFF")

quitter = tkinter.Button(window, text='Quitter', command=quit, bg='#895131', fg="#FFFFFF")
vecteur = tkinter.Checkbutton(window, text='Afficher \n vecteur direction', bd=2, indicator=0, bg='#EA9767',
                              command=vite, variable=check_vite)
gravite = tkinter.Checkbutton(window, text='Afficher \n vecteur gravité', bd=2, indicator=0, bg='#EA9767',
                              command=gravity, variable=check_grav)
other = tkinter.Button(window, text='Autres graph', bg='#895131', fg="#FFFFFF", command=multi_graph)

# Packaging des boutons (ordre important)
text_vitesse.pack()  # Vitesse initiale
v0.pack()  # saisie Vitesse
text_alpha.pack()  # Angle initial
alpha.pack()  # saisie Angle
text_hauteur.pack()
h.pack()
valider.pack()  # Envoi les infos vitesse et angle

quitter.pack(side='bottom')  # Bouton quitter

vecteur.pack(side='bottom')  # Switch vecteur direction sur le graphique
gravite.pack(side='bottom')  # Switch vecteur gravité sur le graphique
other.pack(side='bottom')

window.resizable(width=False, height=False)  # contraint la fenêtre à garder sa résolution
window.config(bg='#386C91')
window.geometry("630x390")
window.mainloop()
