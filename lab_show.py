import tkinter.ttk as tk
import tkinter as tk
from labyrinthe import *
from arbre import *
import sys


n = 29
m = 49


class Labyrinthe(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.creer_widgets()
        self.initialisation()

    def creer_widgets(self):
        self.canv = tk.Canvas(self, bg='black', height=600, width=1000)
        self.canv.pack(side=tk.LEFT)
        self.bouton_quitter = tk.Button(self, text='Quitter', bg='light blue', command=self.destroy)
        self.bouton_quitter.pack(side=tk.BOTTOM)
        self.bouton_nouveau = tk.Button(self, text='Nouveau', command=lambda: self.initialisation())
        self.bouton_nouveau.pack(side=tk.BOTTOM)
        self.bouton_solution = tk.Button(self, text='Solution', command=lambda: self.solution(self.final))
        self.bouton_solution.pack(side=tk.BOTTOM)
        self.label1 = tk.Label(text=f'Labyrinthe parfait {n}*{m}', bg='light blue')
        self.label1.pack(side=tk.TOP)

    def initialisation(self):
        sys.setrecursionlimit(10000)
        lab = generation(n, m)
        self.maze = lab
        self.arbre = Noeud(0)
        a = self.accroche(self.arbre, [0], self.maze)
        if a:
            self.final = self.recherche(n * m - 1, a)
            pas = 20
            self.canv.delete('all')
            for i in range(n):
                for j in range(m):
                    if self.maze[i][j][0] == 1:
                        self.canv.create_line(5 + pas * j, 5 + pas * i, 5 + pas * (j + 1), 5 + pas * i)
                    if self.maze[i][j][1] == 1:
                        self.canv.create_line(5 + pas * j, 5 + pas * (i + 1), 5 + pas * (j + 1), 5 + pas * (i + 1))
                    if self.maze[i][j][2] == 1:
                        self.canv.create_line(5 + pas * (j + 1), 5 + pas * i, 5 + pas * (j + 1), 5 + pas * (i + 1))
                    if self.maze[i][j][3] == 1:
                        self.canv.create_line(5 + pas * j, 5 + pas * i, 5 + pas * j, 5 + pas * (i + 1))
        else:
            return self.initialisation()

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
        else:
            return None

    def recherche(self, valeur, noeud):
        if noeud is None:
            return None
        if noeud.valeur == valeur:
            return noeud
        if valeur < noeud.valeur:
            return self.recherche(valeur, noeud.gauche)
        if valeur > noeud.valeur:
            return self.recherche(valeur, noeud.droit)

    def solution(self, final):
        chemin = []
        noeud_courant = final
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
