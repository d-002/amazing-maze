class Noeud:
    def __init__(self, v):
        self.valeur = v
        self.pere = None
        self.gauche = None
        self.milieu = None
        self.droit = None

class Arbre:
    def __init__(self):
        self.racine = None

    def trouve_valeur(self, val):
        l = [self.racine]
        while len(l): # continuer jusqu'à la fin
            n = l.pop()
            if n is not None:
                if n.valeur == val:
                    return n
                l += n.gauche, n.milieu, n.droit
