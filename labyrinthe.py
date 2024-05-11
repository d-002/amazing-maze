from random import *

def voisins(maze, X, Y, n, m, check):
    # renvoie les voisons non visités autour de la cellule (X, Y)
    N = []
    for x, y, i in [(X, Y-1, 0), (X+1, Y, 1), (X, Y+1, 2), (X-1, Y, 3)]:
        if 0 <= x < m and 0 <= y < n and check(x, y, i):
            N.append([(x, y), i]) # position, indice du voisin
    return N

def generation(n, m):
    lab = [[[1, 1, 1, 1, 0] for _ in range(m)] for _ in range(n)]
    lab[0][0][3] = lab[n-1][m-1][1] = 0

    pos = (0, 0)
    pile = [pos]

    check = lambda x, y, i: not lab[y][x][4] # besoin que la cellule soit vide ici

    while pile:
        x, y = pos
        lab[y][x][4] = 1

        N = voisins(lab, x, y, n, m, check)
        if len(N):
            pos_, index = choice(N)
            x_, y_ = pos_
            # récupérer l'index de mur de la cellule voisine
            index_ = (index+2) % 4
            lab[y][x][index] = 0
            lab[y_][x_][index_] = 0

            pile.insert(0, pos)
            pos = (x_, y_)

        else: # pas de voisins libre : retour
            pos = pile.pop()

    return lab

# print(generation(3, 3))
