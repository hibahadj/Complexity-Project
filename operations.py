# operations.py - TOUTES les opérations
from node import Noeud, ArbreNaire, ArbreVecteur
from collections import deque
import tkinter as tk
from tkinter import Canvas
from time import perf_counter


class NoeudBinaire:
    """Nœud binaire (gauche/droit) issu de la transformation premier-fils / frère-suivant."""

    def __init__(self, info):
        self.info = info
        self.gauche = None  # premier fils
        self.droit = None   # frère suivant

    def __str__(self):
        return str(self.info)

# ============================================================================
# OPÉRATIONS DE BASE
# ============================================================================

def creer_racine(arbre, info):
    """Crée la racine de l'arbre
    Complexité: O(1)
    """
    arbre.racine = Noeud(info)
    return arbre.racine

def ajouter_fils(arbre, parent, info):
    """Ajoute un fils à un parent
    Complexité: O(k) où k = nombre d'enfants du parent
    """
    if parent is None:
        return None

    if parent.nb_enfants() >= arbre.degre:
        print(f"Erreur : degré maximal ({arbre.degre}) atteint pour {parent.info}")
        return None

    nouveau = Noeud(info)
    nouveau.parent = parent

    if parent.succ_gauche is None:
        parent.succ_gauche = nouveau
    else:
        courant = parent.succ_gauche
        while courant.succ_droit:
            courant = courant.succ_droit
        courant.succ_droit = nouveau

    return nouveau

def rechercher(arbre, info, noeud=None):
    '''Recherche un nœud par son information
    Complexité: O(n) temps, O(h) espace'''
    
    if noeud is None:
        noeud = arbre.racine

    if noeud is None:
        return None

    if noeud.info == info:
        return noeud

    fils = noeud.succ_gauche
    while fils:
        resultat = rechercher(arbre, info, fils)
        if resultat:
            return resultat
        fils = fils.succ_droit

    return None



def compter_noeuds(arbre, noeud=None):
    """Compte le nombre total de nœuds
    Complexité: O(n) où n = nombre de nœuds"""
    
    if noeud is None:
        noeud = arbre.racine

    if noeud is None:
        return 0

    count = 1
    fils = noeud.succ_gauche
    while fils:
        count += compter_noeuds(arbre, fils)
        fils = fils.succ_droit

    return count

def calculer_hauteur(arbre, noeud=None):
    """Calcule la hauteur de l'arbre
    Complexité: O(n) temps, O(h) espace (pile récursion)"""
    
    if noeud is None:
        noeud = arbre.racine

    if noeud is None:
        return 0

    if noeud.est_feuille():
        return 0

    hauteur_max = -1
    fils = noeud.succ_gauche
    while fils:
        h = calculer_hauteur(arbre, fils)
        hauteur_max = max(hauteur_max, h)
        fils = fils.succ_droit

    return hauteur_max + 1



def chemin_entre_noeuds(a, b):
    if a is None or b is None:
        return []

    chemin_a = []
    courant = a
    while courant:
        chemin_a.append(courant)
        courant = courant.parent

    chemin_b = []
    courant = b
    while courant:
        chemin_b.append(courant)
        courant = courant.parent

    chemin_a_set = set(chemin_a)

    lca = None
    for noeud in chemin_b:
        if noeud in chemin_a_set:
            lca = noeud
            break

    if lca is None:
        return []

    chemin_final = []

    courant = a
    while courant != lca:
        chemin_final.append(courant)
        courant = courant.parent
    chemin_final.append(lca)

    chemin_b_lca = []
    courant = b
    while courant != lca:
        chemin_b_lca.append(courant)
        courant = courant.parent

    chemin_final.extend(reversed(chemin_b_lca))

    return chemin_final


def inserer_noeud(arbre, info_parent, info_nouveau):
  
    # 1️⃣ Rechercher le parent
    parent = rechercher(arbre, info_parent)
    if parent is None:
        print(f" Parent '{info_parent}' non trouvé !")
        return None

    # 2️⃣ Ajouter le nouveau nœud sous ce parent
    nouveau_noeud = ajouter_fils(arbre, parent, info_nouveau)
    
    # 3️⃣ Affichage du résultat
    if nouveau_noeud:
        print(f" Nœud '{nouveau_noeud.info}' inséré avec succès sous '{parent.info}'")
    else:
        print(f" Impossible d’insérer le nœud sous '{parent.info}' (degré maximum atteint ?)")

    return nouveau_noeud


def modifier_noeud(arbre, info_cible, nouvelle_info):
    """Modifie l'information d'un nœud identifié par sa valeur.
    Complexité: O(n) (recherche) + O(1) (modification)
    """
    noeud = rechercher(arbre, info_cible)
    if noeud is None:
        print(f" Nœud '{info_cible}' non trouvé !")
        return False

    ancienne = noeud.info
    noeud.info = nouvelle_info
    print(f" Nœud modifié: '{ancienne}' → '{nouvelle_info}'")
    return True


def _trouver_noeud_et_prev_frere(parent, cible):
    """Retourne (prev, found) où prev est le frère précédent de found (ou None si found est premier fils)."""
    if parent is None or parent.succ_gauche is None:
        return None, None

    prev = None
    courant = parent.succ_gauche
    while courant:
        if courant == cible:
            return prev, courant
        prev = courant
        courant = courant.succ_droit

    return None, None


def supprimer_noeud(arbre, info_cible):
    """Supprime un nœud identifié par son information.

    Cas gérés:
    - Feuille: suppression simple.
    - Avec enfants: on rattache ses enfants au parent (à la place du nœud).
    - Racine: suppression autorisée uniquement si la racine est une feuille.

    Complexité: O(n) pour la recherche + O(k) pour la suppression (k = nb frères/enfants parcourus)
    """
    cible = rechercher(arbre, info_cible)
    if cible is None:
        print(f" Nœud '{info_cible}' non trouvé !")
        return False

    # Cas racine
    if cible == arbre.racine:
        if cible.succ_gauche is not None:
            print(" Impossible de supprimer la racine si elle a des enfants (choix simplifié).")
            return False
        arbre.racine = None
        print(f" Racine '{info_cible}' supprimée.")
        return True

    parent = cible.parent
    if parent is None:
        print(" Erreur: nœud orphelin.")
        return False

    prev, found = _trouver_noeud_et_prev_frere(parent, cible)
    if found is None:
        print(" Erreur interne: nœud non relié à son parent.")
        return False

    # Liste des enfants de la cible (si existants)
    premier_fils = cible.succ_gauche
    if premier_fils is None:
        # Feuille: on retire found de la liste des enfants du parent
        if prev is None:
            parent.succ_gauche = found.succ_droit
        else:
            prev.succ_droit = found.succ_droit
        print(f" Feuille '{info_cible}' supprimée.")
        return True

    # Nœud avec enfants: on rattache la liste d'enfants au parent à la place du nœud
    # 1) Trouver dernier fils de la cible
    dernier_fils = premier_fils
    while dernier_fils.succ_droit:
        dernier_fils = dernier_fils.succ_droit

    # 2) Relier la chaîne d'enfants au parent à l'emplacement du nœud cible
    if prev is None:
        parent.succ_gauche = premier_fils
    else:
        prev.succ_droit = premier_fils
    dernier_fils.succ_droit = found.succ_droit

    # 3) Mettre à jour les parents des enfants
    courant = premier_fils
    while courant and courant != found.succ_droit:
        courant.parent = parent
        courant = courant.succ_droit

    print(f" Nœud '{info_cible}' supprimé (enfants rattachés à '{parent.info}').")
    return True


def afficher_sous_arbre(noeud):
    """Affiche le sous-arbre de racine noeud en profondeur (DFS).
    Complexité: O(t) où t = nombre de nœuds du sous-arbre
    """
    afficher_profondeur(noeud)


def extraire_sous_arbre(arbre, info_racine_sous_arbre):
    """Extrait (copie) un sous-arbre de racine donnée et le retourne comme un nouvel ArbreNaire.
    Complexité: O(t) où t = nombre de nœuds du sous-arbre
    """
    racine_src = rechercher(arbre, info_racine_sous_arbre)
    if racine_src is None:
        print(f" Racine '{info_racine_sous_arbre}' non trouvée !")
        return None

    new_tree = ArbreNaire(degre=arbre.degre)

    def copier(noeud_src, parent_dst=None):
        noeud_dst = Noeud(noeud_src.info)
        noeud_dst.parent = parent_dst

        # Copier la liste des enfants
        enfant_src = noeud_src.succ_gauche
        prev_dst = None
        while enfant_src:
            enfant_dst = copier(enfant_src, noeud_dst)
            if prev_dst is None:
                noeud_dst.succ_gauche = enfant_dst
            else:
                prev_dst.succ_droit = enfant_dst
            prev_dst = enfant_dst
            enfant_src = enfant_src.succ_droit

        return noeud_dst

    new_tree.racine = copier(racine_src, None)
    return new_tree


def est_arbre_complet(arbre):
    """Vérifie si un arbre n-aire (degré arbre.degre) est complet.

    Définition utilisée (classique, niveaux remplis de gauche à droite):
    - Tous les niveaux sauf le dernier sont pleins.
    - Le dernier niveau est rempli de gauche à droite.

    Complexité: O(n)
    """
    if arbre.racine is None:
        return True

    degre = arbre.degre
    file = deque([arbre.racine])
    trou_trouve = False

    while file:
        noeud = file.popleft()
        nb = noeud.nb_enfants()

        if nb < degre:
            trou_trouve = True
        elif trou_trouve and nb > 0:
            # Après un "trou" (un nœud pas plein), tous les suivants doivent être des feuilles
            return False

        enfant = noeud.succ_gauche
        while enfant:
            file.append(enfant)
            enfant = enfant.succ_droit

    return True


def sous_arbre_complet_maximal(arbre):
    """Trouve un sous-arbre complet maximal (en nombre de nœuds).

    Retourne (racine, taille). Si plusieurs, retourne le premier trouvé.
    Complexité: O(n^2) (on teste la complétude sur chaque racine candidate)
    """
    if arbre.racine is None:
        return None, 0

    # Collecter tous les nœuds
    noeuds = []
    file = deque([arbre.racine])
    while file:
        n = file.popleft()
        noeuds.append(n)
        enfant = n.succ_gauche
        while enfant:
            file.append(enfant)
            enfant = enfant.succ_droit

    def est_complet_sous_arbre(racine):
        tmp = ArbreNaire(degre=arbre.degre)
        tmp.racine = racine
        return est_arbre_complet(tmp)

    best_root = None
    best_size = 0
    for n in noeuds:
        if est_complet_sous_arbre(n):
            tmp = ArbreNaire(degre=arbre.degre)
            tmp.racine = n
            size = compter_noeuds(tmp)
            if size > best_size:
                best_size = size
                best_root = n

    return best_root, best_size


def construire_arbre_complet(nb_noeuds, degre=4):
    """Construit un arbre complet (remplissage en largeur) avec nb_noeuds.
    Complexité: O(nb_noeuds)
    """
    arbre = ArbreNaire(degre=degre)
    if nb_noeuds <= 0:
        return arbre

    nodes = [Noeud(f"N{i}") for i in range(nb_noeuds)]
    arbre.racine = nodes[0]

    # Relier en ordre niveau (indexation type tas m-aire)
    for i in range(nb_noeuds):
        parent = nodes[i]
        first_child_index = degre * i + 1
        last_child_index = min(first_child_index + degre, nb_noeuds)
        prev = None
        for j in range(first_child_index, last_child_index):
            child = nodes[j]
            child.parent = parent
            if prev is None:
                parent.succ_gauche = child
            else:
                prev.succ_droit = child
            prev = child

    return arbre


def evaluation_experimentale(taille_list, degre=4):
    """Mesure le temps d'exécution de:
    - est_arbre_complet
    - sous_arbre_complet_maximal

    Retourne une liste de tuples: (n, t_complet, t_max_complet)
    Complexité globale: dépend des tailles; utile pour tableau expérimental.
    """
    resultats = []
    for n in taille_list:
        arbre = construire_arbre_complet(n, degre=degre)

        t0 = perf_counter()
        _ = est_arbre_complet(arbre)
        t1 = perf_counter()

        t2 = perf_counter()
        _ = sous_arbre_complet_maximal(arbre)
        t3 = perf_counter()

        resultats.append((n, t1 - t0, t3 - t2))

    return resultats


def transformer_en_arbre_binaire(arbre):
    """Transforme un arbre n-aire en arbre binaire (premier fils / frère suivant).

    Remarque: votre représentation chainée utilise déjà ce principe; ici on construit une
    structure binaire explicite (NoeudBinaire) pour l'illustrer.

    Complexité: O(n)
    """
    if arbre.racine is None:
        return None

    def convertir(noeud):
        if noeud is None:
            return None
        b = NoeudBinaire(noeud.info)
        b.gauche = convertir(noeud.succ_gauche)
        b.droit = convertir(noeud.succ_droit)
        return b

    return convertir(arbre.racine)


def afficher_binaire_preordre(racine_binaire):
    """Affichage préordre d'un arbre binaire (racine, gauche, droit).
    Complexité: O(n)
    """
    def rec(n):
        if n is None:
            return
        print(n.info, end=" ")
        rec(n.gauche)
        rec(n.droit)

    rec(racine_binaire)
    print()


# ============================================================================
# REPRÉSENTATION CONTIGUË (VECTEUR) - exemples + affichage
# ============================================================================


def construire_arbre_vecteur_exemple1(degre=4):
    """Construit un exemple d'arbre n-aire en représentation contiguë (vecteur)."""
    arbre = ArbreVecteur(degre=degre)
    a = arbre.creer_racine("A")

    b = arbre.ajouter_fils(a, "B")
    c = arbre.ajouter_fils(a, "C")
    d = arbre.ajouter_fils(a, "D")
    e = arbre.ajouter_fils(a, "E")

    f = arbre.ajouter_fils(b, "F")
    g = arbre.ajouter_fils(b, "G")

    arbre.ajouter_fils(c, "H")
    arbre.ajouter_fils(d, "I")
    arbre.ajouter_fils(d, "J")
    arbre.ajouter_fils(e, "K")

    arbre.ajouter_fils(f, "L")
    arbre.ajouter_fils(f, "M")
    arbre.ajouter_fils(g, "N")

    return arbre


def construire_arbre_vecteur_exemple2(degre=4):
    """Construit un 2e exemple (non complet) en représentation contiguë."""
    arbre = ArbreVecteur(degre=degre)
    r = arbre.creer_racine("R")

    a = arbre.ajouter_fils(r, "A")
    b = arbre.ajouter_fils(r, "B")
    c = arbre.ajouter_fils(r, "C")

    a1 = arbre.ajouter_fils(a, "A1")
    a2 = arbre.ajouter_fils(a, "A2")
    arbre.ajouter_fils(a2, "A21")

    arbre.ajouter_fils(b, "B1")
    _ = c  # C reste feuille
    _ = a1

    return arbre


def afficher_arbre_vecteur(arbre_vecteur):
    """Affiche l'arbre en représentation contiguë (tableau).
    Format adapté aux captures d'écran du rapport.
    """
    if arbre_vecteur is None or arbre_vecteur.est_vide():
        print("Arbre vecteur vide.")
        return

    print("\nReprésentation contiguë (vecteur/tableau):")
    print(f"Degré = {arbre_vecteur.degre}")
    print(f"Racine (index) = {arbre_vecteur.racine}")
    print("-" * 78)
    print(f"{'idx':>3} | {'info':<10} | {'parent':>6} | enfants (indices)\n" + "-" * 78)

    for i, n in enumerate(arbre_vecteur.noeuds):
        enfants_str = ", ".join(f"{x:>2}" for x in n.enfants)
        print(f"{i:>3} | {str(n.info):<10} | {n.parent:>6} | [{enfants_str}]")

    print("-" * 78)



"""
def modifier_noeud(noeud, nouvelle_info):
    Modifie l'information d'un nœud
    Complexité: O(1)
    
    if noeud is None:
        print("Erreur: nœud inexistant")
        return False

    ancienne_info = noeud.info
    noeud.info = nouvelle_info
    print(f"✓ Nœud modifié: '{ancienne_info}' → '{nouvelle_info}'")
    return True

def supprimer_noeud(arbre, noeud):
    Supprime un nœud de l'arbre
    Complexité: O(k) où k = nombre de frères
    
    if noeud is None:
        print("Erreur: nœud inexistant")
        return False

    # Cas 1: Supprimer la racine
    if noeud == arbre.racine:
        if noeud.succ_gauche is not None:
            print("Erreur: Impossible de supprimer la racine avec des fils")
            return False
        arbre.racine = None
        print(f"✓ Racine '{noeud.info}' supprimée")
        return True

    parent = noeud.parent
    if parent is None:
        print("Erreur: nœud orphelin")
        return False

    # Cas 2: Nœud avec fils → rattacher au parent
    if noeud.succ_gauche is not None:
        premier_fils = noeud.succ_gauche
        dernier_fils = premier_fils

        while dernier_fils.succ_droit:
            dernier_fils = dernier_fils.succ_droit

        if parent.succ_gauche == noeud:
            parent.succ_gauche = premier_fils
        else:
            frere = parent.succ_gauche
            while frere.succ_droit != noeud:
                frere = frere.succ_droit
            frere.succ_droit = premier_fils

        dernier_fils.succ_droit = noeud.succ_droit

        fils = premier_fils
        while fils != noeud.succ_droit:
            fils.parent = parent
            if fils.succ_droit is None:
                break
            fils = fils.succ_droit

        print(f"✓ Nœud '{noeud.info}' supprimé (fils rattachés)")

    # Cas 3: Feuille
    else:
        if parent.succ_gauche == noeud:
            parent.succ_gauche = noeud.succ_droit
        else:
            frere = parent.succ_gauche
            while frere.succ_droit != noeud:
                frere = frere.succ_droit
            frere.succ_droit = noeud.succ_droit

        print(f"✓ Feuille '{noeud.info}' supprimée")

    return True
"""



# ============================================================================
# FONCTIONS D'AFFICHAGE
# ============================================================================

def afficher_profondeur(noeud, niveau=0):
    """Affiche un arbre n-aire avec profondeur, sans | en trop."""
    if noeud is None:
        return

    # Racine
    if niveau == 0:
        print("🌲 " + str(noeud.info))
    else:
        print("    " * (niveau - 1) + "└── " + str(noeud.info))

    # Parcours des enfants
    fils = noeud.succ_gauche
    while fils:
        afficher_profondeur(fils, niveau + 1)
        fils = fils.succ_droit




def afficher_largeur(arbre):
    """Affichage en largeur (BFS)"""
    if arbre.racine is None:
        print("🌳 L'arbre est vide!")
        return

    file = deque([arbre.racine])
    niveau = 0
    

    while file:
        taille_niveau = len(file)
        
        # En-tête du niveau
        if niveau == 0:
            print(f"\n Niveau {niveau} :") #RACINE
        else:
            print(f"\n Niveau {niveau}:")
        print("-" * 30)
        
        for _ in range(taille_niveau):
            noeud = file.popleft()
            
            # Informations du nœud
            parent = noeud.parent.info if noeud.parent else "RACINE"
            enfants = noeud.nb_enfants()
            type_noeud = "feuille" if enfants == 0 else ""
            
            print(f" {noeud.info:10} | Parent: {parent:8} | Enfants: {enfants} |  {type_noeud} ")
            
            # Ajout des enfants
            fils = noeud.succ_gauche
            while fils:
                file.append(fils)
                fils = fils.succ_droit

        niveau += 1
    
    print("="*50)


def afficher_graphique_tkinter(arbre):
    """
    Affiche l'arbre avec tkinter (intégré à Python)
    Complexité: O(n) pour le dessin
    """
    if arbre.racine is None:
        print("🌳 L'arbre est vide!")
        return
    
    # Créer la fenêtre
    fenetre = tk.Tk()
    fenetre.title("Visualisation d'arbre n-aire")
    fenetre.geometry("800x600")
    
    # Canvas pour dessiner
    canvas = Canvas(fenetre, width=800, height=600, bg='white')
    canvas.pack()
    
    # Paramètres de dessin
    rayon = 20
    espace_horizontal = 100
    espace_vertical = 80
    
    def dessiner_noeud(x, y, noeud, niveau):
        """Dessine un nœud et ses enfants"""
        if noeud is None:
            return
        
        # Couleur selon le type de nœud
        if noeud.nb_enfants() > 0:
            couleur = 'lightblue'
        else:
            couleur = 'lightgreen'
        
        # Dessiner le cercle du nœud
        canvas.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, 
                          fill=couleur, outline='black', width=2)
        
        # Texte du nœud
        canvas.create_text(x, y, text=noeud.info, font=('Arial', 10, 'bold'))
        
        # Informations supplémentaires
        canvas.create_text(x, y+15, text=f"({noeud.nb_enfants()})", 
                          font=('Arial', 8))
        
        # Dessiner les enfants
        enfant = noeud.succ_gauche
        count = 0
        nb_enfants = noeud.nb_enfants()
        
        while enfant:
            # Position de l'enfant
            if nb_enfants == 1:
                enfant_x = x
            else:
                spread = (nb_enfants - 1) * espace_horizontal
                enfant_x = x - spread/2 + count * espace_horizontal
            
            enfant_y = y + espace_vertical
            
            # Ligne parent-enfant
            canvas.create_line(x, y+rayon, enfant_x, enfant_y-rayon, 
                             fill='gray', width=1)
            
            # Dessiner l'enfant récursivement
            dessiner_noeud(enfant_x, enfant_y, enfant, niveau+1)
            
            enfant = enfant.succ_droit
            count += 1
    
    # Calculer la position de départ (centré en haut)
    dessiner_noeud(400, 50, arbre.racine, 0)
    
    # Ajouter un titre
    canvas.create_text(400, 20, text=f"Arbre {arbre.degre}-aire", 
                      font=('Arial', 12, 'bold'))
    
    # Lancer la fenêtre
    print("🎨 Fenêtre graphique ouverte (fermez-la pour continuer)...")
    fenetre.mainloop()


