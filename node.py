# node.py - VERSION SIMPLIFIÉE (structure seulement)
class Noeud:
    def __init__(self, info):
        self.info = info
        self.succ_gauche = None   # premier fils
        self.succ_droit = None    # frère suivant
        self.parent = None

    def __str__(self):
        return str(self.info)

    def nb_enfants(self):
        count = 0
        courant = self.succ_gauche
        while courant:
            count += 1
            courant = courant.succ_droit
            
        return count

    def est_feuille(self):
        return self.succ_gauche is None


class ArbreNaire:
    def __init__(self, degre=4):
        self.racine = None
        self.degre = degre

    def est_vide(self):
        return self.racine is None


# ---------------------------------------------------------------------------
# Représentation contiguë (vecteur/tableau)
# ---------------------------------------------------------------------------


class NoeudVecteur:
    """Nœud en représentation contiguë.

    - Stocké dans un tableau (liste) à l'indice i
    - `parent` est l'indice du parent (-1 si racine)
    - `enfants` est une liste de taille `degre` contenant des indices (ou -1)
    """

    def __init__(self, info, degre, parent=-1):
        self.info = info
        self.parent = parent
        self.enfants = [-1] * degre

    def __str__(self):
        return str(self.info)


class ArbreVecteur:
    """Arbre n-aire stocké dans un tableau (représentation contiguë)."""

    def __init__(self, degre=4):
        self.degre = degre
        self.noeuds = []  # liste de NoeudVecteur
        self.racine = -1

    def est_vide(self):
        return self.racine == -1

    def creer_racine(self, info):
        if not self.est_vide():
            return self.racine
        self.noeuds.append(NoeudVecteur(info, self.degre, parent=-1))
        self.racine = 0
        return self.racine

    def ajouter_fils(self, parent_index, info):
        if parent_index < 0 or parent_index >= len(self.noeuds):
            return -1

        parent = self.noeuds[parent_index]
        try:
            pos = parent.enfants.index(-1)
        except ValueError:
            return -1

        new_index = len(self.noeuds)
        self.noeuds.append(NoeudVecteur(info, self.degre, parent=parent_index))
        parent.enfants[pos] = new_index
        return new_index