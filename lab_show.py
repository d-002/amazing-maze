from tkinter import *
from tkinter.ttk import *

from labyrinthe import *
from arbre import *
import sys

n = 29
m = 49

class Labyrinthe(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.creer_widgets()
        self.init()

    def creer_widgets(self):
        Label(text=f'Labyrinthe parfait {n}*{m}').grid(columnspan=3)
        self.canv = Canvas(self, bg='white', height=600, width=1000)
        self.canv.grid(columnspan=3)
        Button(self, text='Quitter', command=self.destroy).grid()
        Button(self, text='Nouveau', command=self.init).grid(column=1, row=2)
        Button(self, text='Solution', command=self.solution).grid(column=2, row=2)

    def init(self):
        lab = generation(n, m)
        self.maze = lab
        self.arbre = Noeud(0)
        pas = 20
        o = pas>>1 # offset
        self.canv.delete('all')
        for y in range(n):
            y_= y+1 # cache pour aller plus vite
            for x in range(m):
                x_ = x+1
                cell = self.maze[y][x]
                if cell[0]: self.canv.create_line(o+pas*x, o+pas*y, o+pas*x_, o+pas*y)
                if cell[1]: self.canv.create_line(o+pas*x_, o+pas*y, o+pas*x_, o+pas*y_)
                if cell[2]: self.canv.create_line(o+pas*x, o+pas*y_, o+pas*x_, o+pas*y_)
                if cell[3]: self.canv.create_line(o+pas*x, o+pas*y, o+pas*x, o+pas*y_)

    def accroche(self, node, visites, lab):
        k = node.valeur
        if k == n * m - 1:
            return node
        i = k // len(lab[0])
        j = k % len(lab[0])
        voisins = []
        for x in range(len(lab[i][j])):
            if lab[i][j][x] == 0:
                voisins.append(x)
        if i == 0 and j == 0:
            for x in range(len(voisins)):
                if voisins[x] == 3:
                    voisins.pop(x)
        if 0 in voisins and (i - 1) * len(lab[0]) + j not in visites:
            nouveau_noeud = Noeud((i - 1) * len(lab[0]) + j)
            node.millieu = nouveau_noeud
            nouveau_noeud.pere = node
            visites.append((i - 1) * len(lab[0]) + j)
            return self.accroche(nouveau_noeud, visites, self.maze)
        if 1 in voisins and (i + 1) * len(lab[0]) + j not in visites:
            nouveau_noeud = Noeud((i + 1) * len(lab[0]) + j)
            node.millieu = nouveau_noeud
            nouveau_noeud.pere = node
            visites.append((i + 1) * len(lab[0]) + j)
            return self.accroche(nouveau_noeud, visites, self.maze)
        if 2 in voisins and i * len(lab[0]) + (j + 1) not in visites:
            nouveau_noeud = Noeud(i * len(lab[0]) + (j + 1))
            node.droit = nouveau_noeud
            nouveau_noeud.pere = node
            visites.append(i * len(lab[0]) + (j + 1))
            return self.accroche(nouveau_noeud, visites, self.maze)
        if 3 in voisins and i * len(lab[0]) + (j - 1) not in visites:
            nouveau_noeud = Noeud(i * len(lab[0]) + (j - 1))
            node.gauche = nouveau_noeud
            nouveau_noeud.pere = node
            visites.append(i * len(lab[0]) + (j - 1))
            return self.accroche(nouveau_noeud, visites, self.maze)

    def recherche(self, valeur, noeud):
        if noeud is None:
            return
        if noeud.valeur == valeur:
            return noeud
        if valeur < noeud.valeur:
            return self.recherche(valeur, noeud.gauche)
        if valeur > noeud.valeur:
            return self.recherche(valeur, noeud.droit)

    def solution(self):
        chemin = []
        noeud_courant = self.final
        while noeud_courant.pere is not None:
            chemin.append(noeud_courant.valeur)
            noeud_courant = noeud_courant.pere
        chemin.append(0)
        chemin.reverse()
        return self.dessiner(chemin)

    def dessiner(self, chemin):
        pas = 20
        for i in range(n):
            for j in range(m):
                if (i * m + j) in chemin:
                    self.canv.create_oval(5 + pas * j + pas // 3, 5 + pas * i + pas // 3, 5 + pas * j + 2 * pas // 3,
                                          5 + pas * i + 2 * pas // 3, fill='red')

if __name__ == '__main__':
    app = Labyrinthe()
    app.title('Labyrinthe parfait')
    app.mainloop()
