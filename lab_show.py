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

    def accroche(self, node):
        def est_ouvert(x_, y_, i):
            # utilisé par accroche en tant que fonction pour ajouter ou non
            # à la liste de voisins. renvoie True si un chemin ouvert existe
            # entre deux noeuds et si on ne backtrack pas

            x, y = node.valeur
            if node.pere is None: retour = False
            else: retour = (x_, y_) == node.pere.valeur
            return not self.maze[y][x][i] and not retour

        x, y = node.valeur
        v = voisins(self.maze, x, y, len(self.maze), len(self.maze[0]), est_ouvert)

        # remplir le père de gauche à droite jusqu'à ce qu'il n'y ait plus d'autres voisins
        for pos, attr in zip(v, ['gauche', 'milieu', 'droit']):
            n = Noeud(pos[0])
            n.pere = node
            exec('node.%s = n' %attr)
            self.accroche(n)

    def recherche(self, valeur, noeud):
        l = [noeud]
        while len(l):
            n = l.pop()
            if n is not None:
                if n.valeur == valeur: return n
                l += [n.gauche, n.milieu, n.droit]

    def solution(self):
        arbre = Arbre()
        arbre.racine = Noeud((0, 0))
        self.accroche(arbre.racine)

        # trouver la fin, puis backtrack
        fin = self.recherche((len(self.maze[0])-1, len(self.maze)-1), arbre.racine)
        chemin = [fin]
        while type(chemin[-1]) == Noeud:
            chemin.append(chemin[-1].pere)
        chemin.pop() # enlever la racine

        # ne mettre que les valeurs dans le chemin pour self.dessiner
        for i in range(len(chemin)):
            chemin[i] = chemin[i].valeur

        self.dessiner(chemin)

    def dessiner(self, chemin):
        pas = 20
        o = pas>>1
        for x in range(len(self.maze[0])):
            for y in range(len(self.maze)):
                if (x, y) in chemin:
                    self.canv.create_oval(o + pas * x + pas // 3, o + pas * y + pas // 3,
                                          o + pas * x + 2 * pas // 3, o + pas * y + 2 * pas // 3,
                                          fill='red')

if __name__ == '__main__':
    app = Labyrinthe()
    app.title('Labyrinthe parfait')
    app.mainloop()
