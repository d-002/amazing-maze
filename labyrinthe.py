from random import *


# j'ai eu du mal a utiliser la structure_pile, donc je me suis débrouillé autrement


def generation(n, m):
    lab = [[[1, 1, 1, 1, 0] for j in range(m)] for i in range(n)]
    lab[0][0][3] = 0
    lab[n - 1][m - 1][2] = 0
    pile = [(0, 0)]  # je dois mettre quelque chose dans la pile afin qu'elle ne soit pas vide
    while pile:
        i, j = pile[-1]
        lab[i][j][4] = 1
        cotes = []
        if i > 0 and lab[i - 1][j][4] == 0:
            cotes.append((i - 1, j))
        if i < n - 1 and lab[i + 1][j][4] == 0:
            cotes.append((i + 1, j))
        if j > 0 and lab[i][j - 1][4] == 0:
            cotes.append((i, j - 1))
        if j < m - 1 and lab[i][j + 1][4] == 0:
            cotes.append((i, j + 1))
        if cotes:
            cote_i, cote_j = choice(cotes)
            if cote_i < i:
                lab[i][j][0] = 0
                lab[cote_i][cote_j][2] = 0
            elif cote_i > i:
                lab[i][j][2] = 0
                lab[cote_i][cote_j][0] = 0
            elif cote_j < j:
                lab[i][j][3] = 0
                lab[cote_i][cote_j][1] = 0
            else:
                lab[i][j][1] = 0
                lab[cote_i][cote_j][3] = 0
            pile.append((cote_i, cote_j))
        else:
            pile.pop()
    for i in lab:
        for j in i:
            j[1], j[2] = j[2], j[1]
    return lab


# print(generation(3, 3))
