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