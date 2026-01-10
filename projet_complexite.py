# -*- coding: utf-8 -*-
"""projet_complexite.py - VERSION MONO-FICHIER
M1 BIOINFO - ALGO Av. et Complexité

Ce fichier regroupe:
- Représentation chaînée (premier fils / frère suivant)
- Représentation contiguë (vecteur/tableau)
- Opérations + complexités
- Menu à choix multiples

Exécution:
    python projet_complexite.py
"""

from __future__ import annotations

from collections import deque
import statistics as stats
from time import perf_counter


_MAX_LABEL_LEN = 20


def _normalize_label(value: object) -> str:
    return "" if value is None else str(value)


def _check_label(value: object, *, field_name: str = "Info") -> str | None:
    """Validate and normalize a node label.

    Teacher constraint: words/strings of length <= 20.
    Returns the normalized label if valid, else None.
    """

    label = _normalize_label(value).strip()
    if label == "":
        print(f" {field_name} vide. Réessayez.")
        return None
    if len(label) > _MAX_LABEL_LEN:
        print(f" {field_name} trop longue (>{_MAX_LABEL_LEN}). Réessayez.")
        return None
    return label

# Tkinter est optionnel (si exécution sans interface graphique)
try:
    import tkinter as tk
    from tkinter import Canvas

    _TK_AVAILABLE = True
except Exception:
    tk = None
    Canvas = None
    _TK_AVAILABLE = False


# =============================================================================
# PARTIE II — Représentations mémoire
# =============================================================================


class Noeud:
    """Nœud en représentation chaînée (premier fils / frère suivant)."""

    def __init__(self, info: str):
        self.info = info
        self.succ_gauche: Noeud | None = None  # premier fils
        self.succ_droit: Noeud | None = None  # frère suivant
        self.parent: Noeud | None = None

    def __str__(self) -> str:
        return str(self.info)

    def nb_enfants(self) -> int:
        count = 0
        courant = self.succ_gauche
        while courant:
            count += 1
            courant = courant.succ_droit
        return count

    def est_feuille(self) -> bool:
        return self.succ_gauche is None


class ArbreNaire:
    """Arbre n-aire en représentation chaînée."""

    def __init__(self, degre: int = 4):
        self.racine: Noeud | None = None
        self.degre = degre

    def est_vide(self) -> bool:
        return self.racine is None


class NoeudVecteur:
    """Nœud en représentation contiguë.

    - Stocké dans un tableau (liste) à l'indice i
    - `parent` est l'indice du parent (-1 si racine)
    - `enfants` est une liste de taille `degre` contenant des indices (ou -1)
    """

    def __init__(self, info: str, degre: int, parent: int = -1):
        self.info = info
        self.parent = parent
        self.enfants = [-1] * degre

    def __str__(self) -> str:
        return str(self.info)


class ArbreVecteur:
    """Arbre n-aire stocké dans un tableau (représentation contiguë)."""

    def __init__(self, degre: int = 4):
        self.degre = degre
        self.noeuds: list[NoeudVecteur] = []
        self.racine = -1

    def est_vide(self) -> bool:
        return self.racine == -1

    def creer_racine(self, info: str) -> int:
        if not self.est_vide():
            return self.racine

        info_ok = _check_label(info, field_name="Info racine")
        if info_ok is None:
            return -1

        self.noeuds.append(NoeudVecteur(info_ok, self.degre, parent=-1))
        self.racine = 0
        return self.racine

    def ajouter_fils(self, parent_index: int, info: str) -> int:
        if parent_index < 0 or parent_index >= len(self.noeuds):
            return -1

        info_ok = _check_label(info, field_name="Info du nouveau nœud")
        if info_ok is None:
            return -1

        parent = self.noeuds[parent_index]
        try:
            pos = parent.enfants.index(-1)
        except ValueError:
            return -1

        new_index = len(self.noeuds)
        self.noeuds.append(NoeudVecteur(info_ok, self.degre, parent=parent_index))
        parent.enfants[pos] = new_index
        return new_index


# =============================================================================
# PARTIE III — Opérations sur les arbres (chaînée)
# =============================================================================


def creer_racine(arbre: ArbreNaire, info: str) -> Noeud | None:
    """Crée la racine de l'arbre. Complexité: O(1)"""

    info_ok = _check_label(info, field_name="Info racine")
    if info_ok is None:
        return None

    arbre.racine = Noeud(info_ok)
    return arbre.racine


def ajouter_fils(arbre: ArbreNaire, parent: Noeud | None, info: str) -> Noeud | None:
    """Ajoute un fils à un parent. Complexité: O(k) où k = nb enfants du parent."""

    if parent is None:
        return None

    info_ok = _check_label(info, field_name="Info du nouveau nœud")
    if info_ok is None:
        return None

    if parent.nb_enfants() >= arbre.degre:
        print(f"Erreur : degré maximal ({arbre.degre}) atteint pour {parent.info}")
        return None

    nouveau = Noeud(info_ok)
    nouveau.parent = parent

    if parent.succ_gauche is None:
        parent.succ_gauche = nouveau
    else:
        courant = parent.succ_gauche
        while courant.succ_droit:
            courant = courant.succ_droit
        courant.succ_droit = nouveau

    return nouveau


def rechercher(arbre: ArbreNaire, info: str, noeud: Noeud | None = None) -> Noeud | None:
    """Recherche un nœud par son information. Complexité: O(n) temps, O(h) espace."""

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


def compter_noeuds(arbre: ArbreNaire, noeud: Noeud | None = None) -> int:
    """Compte le nombre total de nœuds. Complexité: O(n)."""

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


def calculer_hauteur(arbre: ArbreNaire, noeud: Noeud | None = None) -> int:
    """Calcule la hauteur de l'arbre. Complexité: O(n) temps, O(h) espace."""

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


def chemin_entre_noeuds(a: Noeud | None, b: Noeud | None) -> list[Noeud]:
    """Chemin entre deux nœuds (adresses) via parents + LCA. Complexité: O(h)."""

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


def inserer_noeud(arbre: ArbreNaire, info_parent: str, info_nouveau: str) -> Noeud | None:
    """Insère un nœud sous un parent identifié par son info. Complexité: O(n)+O(k)."""

    parent = rechercher(arbre, info_parent)
    if parent is None:
        print(f" Parent '{info_parent}' non trouvé !")
        return None

    info_ok = _check_label(info_nouveau, field_name="Info du nouveau nœud")
    if info_ok is None:
        return None

    nouveau_noeud = ajouter_fils(arbre, parent, info_ok)

    if nouveau_noeud:
        print(f" Nœud '{nouveau_noeud.info}' inséré avec succès sous '{parent.info}'")
    else:
        print(f" Impossible d’insérer le nœud sous '{parent.info}' (degré maximum atteint ?) ")

    return nouveau_noeud


def modifier_noeud(arbre: ArbreNaire, info_cible: str, nouvelle_info: str) -> bool:
    """Modifie l'information d'un nœud (par valeur). Complexité: O(n)."""

    nouvelle_ok = _check_label(nouvelle_info, field_name="Nouvelle info")
    if nouvelle_ok is None:
        return False

    noeud = rechercher(arbre, info_cible)
    if noeud is None:
        print(f" Nœud '{info_cible}' non trouvé !")
        return False

    ancienne = noeud.info
    noeud.info = nouvelle_ok
    print(f" Nœud modifié: '{ancienne}' → '{nouvelle_ok}'")
    return True


def _trouver_noeud_et_prev_frere(parent: Noeud | None, cible: Noeud | None):
    """Retourne (prev, found) où prev est le frère précédent de found (ou None si found est premier fils)."""

    if parent is None or parent.succ_gauche is None or cible is None:
        return None, None

    prev = None
    courant = parent.succ_gauche
    while courant:
        if courant == cible:
            return prev, courant
        prev = courant
        courant = courant.succ_droit

    return None, None


def supprimer_noeud(arbre: ArbreNaire, info_cible: str) -> bool:
    """Supprime un nœud identifié par son information.

    Cas gérés:
    - Feuille: suppression simple.
    - Avec enfants: on rattache ses enfants au parent (à la place du nœud).
    - Racine: suppression autorisée uniquement si la racine est une feuille.

    Complexité: O(n) (recherche) + O(k) (reliens).
    """

    cible = rechercher(arbre, info_cible)
    if cible is None:
        print(f" Nœud '{info_cible}' non trouvé !")
        return False

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

    premier_fils = found.succ_gauche
    if premier_fils is None:
        # Feuille
        if prev is None:
            parent.succ_gauche = found.succ_droit
        else:
            prev.succ_droit = found.succ_droit
        print(f" Feuille '{info_cible}' supprimée.")
        return True

    # Nœud avec enfants: rattacher enfants au parent à la place du nœud
    dernier_fils = premier_fils
    while dernier_fils.succ_droit:
        dernier_fils = dernier_fils.succ_droit

    if prev is None:
        parent.succ_gauche = premier_fils
    else:
        prev.succ_droit = premier_fils

    dernier_fils.succ_droit = found.succ_droit

    courant = premier_fils
    while courant and courant != found.succ_droit:
        courant.parent = parent
        courant = courant.succ_droit

    print(f" Nœud '{info_cible}' supprimé (enfants rattachés à '{parent.info}').")
    return True


# =============================================================================
# Affichages
# =============================================================================


def afficher_profondeur(noeud: Noeud | None, niveau: int = 0) -> None:
    """Affiche en profondeur (DFS). Complexité: O(n)."""

    if noeud is None:
        return

    if niveau == 0:
        print("🌲 " + str(noeud.info))
    else:
        print("    " * (niveau - 1) + "└── " + str(noeud.info))

    fils = noeud.succ_gauche
    while fils:
        afficher_profondeur(fils, niveau + 1)
        fils = fils.succ_droit


def afficher_largeur(arbre: ArbreNaire) -> None:
    """Affichage en largeur (BFS). Complexité: O(n)."""

    if arbre.racine is None:
        print("🌳 L'arbre est vide!")
        return

    file = deque([arbre.racine])
    niveau = 0

    while file:
        taille_niveau = len(file)

        print(f"\n Niveau {niveau} :" if niveau == 0 else f"\n Niveau {niveau}:")
        print("-" * 30)

        for _ in range(taille_niveau):
            noeud = file.popleft()

            parent = noeud.parent.info if noeud.parent else "RACINE"
            enfants = noeud.nb_enfants()
            type_noeud = "feuille" if enfants == 0 else ""

            print(f" {noeud.info:10} | Parent: {parent:8} | Enfants: {enfants} |  {type_noeud} ")

            fils = noeud.succ_gauche
            while fils:
                file.append(fils)
                fils = fils.succ_droit

        niveau += 1

    print("=" * 50)


def afficher_sous_arbre(noeud: Noeud) -> None:
    """Affiche un sous-arbre (DFS). Complexité: O(t)."""

    afficher_profondeur(noeud)


def afficher_graphique_tkinter(arbre: ArbreNaire) -> None:
    """Affiche l'arbre avec tkinter. Complexité: O(n)."""

    if not _TK_AVAILABLE:
        print("Tkinter non disponible dans cet environnement.")
        return

    if arbre.racine is None:
        print("🌳 L'arbre est vide!")
        return

    fenetre = tk.Tk()
    fenetre.title("Visualisation d'arbre n-aire")
    fenetre.geometry("800x600")

    canvas = Canvas(fenetre, width=800, height=600, bg="white")
    canvas.pack()

    rayon = 20
    espace_horizontal = 100
    espace_vertical = 80

    def dessiner_noeud(x, y, noeud, niveau):
        if noeud is None:
            return

        couleur = "lightblue" if noeud.nb_enfants() > 0 else "lightgreen"

        canvas.create_oval(
            x - rayon,
            y - rayon,
            x + rayon,
            y + rayon,
            fill=couleur,
            outline="black",
            width=2,
        )
        canvas.create_text(x, y, text=noeud.info, font=("Arial", 10, "bold"))
        canvas.create_text(x, y + 15, text=f"({noeud.nb_enfants()})", font=("Arial", 8))

        enfant = noeud.succ_gauche
        count = 0
        nb_enfants = noeud.nb_enfants()

        while enfant:
            if nb_enfants == 1:
                enfant_x = x
            else:
                spread = (nb_enfants - 1) * espace_horizontal
                enfant_x = x - spread / 2 + count * espace_horizontal

            enfant_y = y + espace_vertical

            canvas.create_line(x, y + rayon, enfant_x, enfant_y - rayon, fill="gray", width=1)
            dessiner_noeud(enfant_x, enfant_y, enfant, niveau + 1)

            enfant = enfant.succ_droit
            count += 1

    dessiner_noeud(400, 50, arbre.racine, 0)
    canvas.create_text(400, 20, text=f"Arbre {arbre.degre}-aire", font=("Arial", 12, "bold"))

    print("🎨 Fenêtre graphique ouverte (fermez-la pour continuer)...")
    fenetre.mainloop()


# =============================================================================
# Arbre complet, sous-arbre complet maximal, extraction
# =============================================================================


def extraire_sous_arbre(arbre: ArbreNaire, info_racine_sous_arbre: str) -> ArbreNaire | None:
    """Extrait (copie) un sous-arbre. Complexité: O(t)."""

    racine_src = rechercher(arbre, info_racine_sous_arbre)
    if racine_src is None:
        print(f" Racine '{info_racine_sous_arbre}' non trouvée !")
        return None

    new_tree = ArbreNaire(degre=arbre.degre)

    def copier(noeud_src: Noeud, parent_dst: Noeud | None = None) -> Noeud:
        noeud_dst = Noeud(noeud_src.info)
        noeud_dst.parent = parent_dst

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


def est_arbre_complet(arbre: ArbreNaire) -> bool:
    """Vérifie si un arbre n-aire est complet. Complexité: O(n)."""

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
            return False

        enfant = noeud.succ_gauche
        while enfant:
            file.append(enfant)
            enfant = enfant.succ_droit

    return True


def sous_arbre_complet_maximal(arbre: ArbreNaire):
    """Trouve un sous-arbre complet maximal (par nombre de nœuds).

    Implémentation simple: O(n^2) (test complet sur chaque racine candidate).
    """

    if arbre.racine is None:
        return None, 0

    noeuds = []
    file = deque([arbre.racine])
    while file:
        n = file.popleft()
        noeuds.append(n)
        enfant = n.succ_gauche
        while enfant:
            file.append(enfant)
            enfant = enfant.succ_droit

    def est_complet_sous_arbre(racine: Noeud) -> bool:
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


def construire_arbre_complet(nb_noeuds: int, degre: int = 4) -> ArbreNaire:
    """Construit un arbre complet en remplissage BFS. Complexité: O(nb_noeuds)."""

    arbre = ArbreNaire(degre=degre)
    if nb_noeuds <= 0:
        return arbre

    nodes = [Noeud(f"N{i}") for i in range(nb_noeuds)]
    arbre.racine = nodes[0]

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


def evaluation_experimentale(taille_list: list[int], degre: int = 4, repeats: int = 30):
    """Retourne un tableau expérimental.

    Mesure deux opérations :
    - est_arbre_complet
    - sous_arbre_complet_maximal

    Pour réduire le bruit, on répète `repeats` fois et on retourne (moyenne, écart-type).

    Retour:
        [(n, mean_complete, std_complete, mean_max, std_max), ...]
    """

    if repeats <= 0:
        repeats = 1

    resultats = []
    for n in taille_list:
        temps_complet = []
        temps_max = []

        for _ in range(repeats):
            arbre = construire_arbre_complet(n, degre=degre)

            t0 = perf_counter()
            _ = est_arbre_complet(arbre)
            t1 = perf_counter()

            t2 = perf_counter()
            _ = sous_arbre_complet_maximal(arbre)
            t3 = perf_counter()

            temps_complet.append(t1 - t0)
            temps_max.append(t3 - t2)

        mc = stats.mean(temps_complet)
        mm = stats.mean(temps_max)
        sc = stats.pstdev(temps_complet)
        sm = stats.pstdev(temps_max)
        resultats.append((n, mc, sc, mm, sm))

    return resultats


# =============================================================================
# Transformation en arbre binaire (illustration)
# =============================================================================


class NoeudBinaire:
    """Nœud binaire (gauche/droit) issu de la transformation premier-fils / frère-suivant."""

    def __init__(self, info: str):
        self.info = info
        self.gauche: NoeudBinaire | None = None
        self.droit: NoeudBinaire | None = None

    def __str__(self) -> str:
        return str(self.info)


def transformer_en_arbre_binaire(arbre: ArbreNaire) -> NoeudBinaire | None:
    """Transforme un arbre n-aire en arbre binaire (premier fils / frère suivant). Complexité: O(n)."""

    if arbre.racine is None:
        return None

    def convertir(noeud: Noeud | None) -> NoeudBinaire | None:
        if noeud is None:
            return None
        b = NoeudBinaire(noeud.info)
        b.gauche = convertir(noeud.succ_gauche)
        b.droit = convertir(noeud.succ_droit)
        return b

    return convertir(arbre.racine)


def afficher_binaire_preordre(racine_binaire: NoeudBinaire | None) -> None:
    """Affichage préordre d'un arbre binaire. Complexité: O(n)."""

    def rec(n: NoeudBinaire | None):
        if n is None:
            return
        print(n.info, end=" ")
        rec(n.gauche)
        rec(n.droit)

    rec(racine_binaire)
    print()


# =============================================================================
# Représentation contiguë (vecteur) — exemples + affichage
# =============================================================================


def construire_arbre_vecteur_exemple1(degre: int = 4) -> ArbreVecteur:
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


def construire_arbre_vecteur_exemple2(degre: int = 4) -> ArbreVecteur:
    arbre = ArbreVecteur(degre=degre)
    r = arbre.creer_racine("R")

    a = arbre.ajouter_fils(r, "A")
    b = arbre.ajouter_fils(r, "B")
    c = arbre.ajouter_fils(r, "C")

    a1 = arbre.ajouter_fils(a, "A1")
    a2 = arbre.ajouter_fils(a, "A2")
    arbre.ajouter_fils(a2, "A21")

    arbre.ajouter_fils(b, "B1")
    _ = c
    _ = a1

    return arbre


def afficher_arbre_vecteur(arbre_vecteur: ArbreVecteur) -> None:
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


# =============================================================================
# Menu + constructeurs d'exemples
# =============================================================================


def const_arbre1() -> ArbreNaire:
    """Construit l'arbre exemple 1."""

    arbre = ArbreNaire(degre=4)
    racine = creer_racine(arbre, "A")

    b = ajouter_fils(arbre, racine, "B")
    c = ajouter_fils(arbre, racine, "C")
    d = ajouter_fils(arbre, racine, "D")
    e = ajouter_fils(arbre, racine, "E")

    f = ajouter_fils(arbre, b, "F")
    g = ajouter_fils(arbre, b, "G")

    ajouter_fils(arbre, c, "H")

    ajouter_fils(arbre, d, "I")
    ajouter_fils(arbre, d, "J")

    ajouter_fils(arbre, e, "K")

    ajouter_fils(arbre, f, "L")
    ajouter_fils(arbre, f, "M")
    ajouter_fils(arbre, g, "N")

    return arbre


def const_arbre2() -> ArbreNaire:
    """Construit un 2e exemple (non complet)."""

    arbre = ArbreNaire(degre=4)
    r = creer_racine(arbre, "R")

    a = ajouter_fils(arbre, r, "A")
    b = ajouter_fils(arbre, r, "B")
    c = ajouter_fils(arbre, r, "C")

    ajouter_fils(arbre, a, "A1")
    a2 = ajouter_fils(arbre, a, "A2")
    ajouter_fils(arbre, a2, "A21")

    ajouter_fils(arbre, b, "B1")
    _ = c

    return arbre


def _print_menu() -> None:
    print("\n" + "=" * 60)
    print("MENU - ARBRES N-AIRES (degré 4)")
    print("=" * 60)
    print("1) Construire exemple 1")
    print("2) Construire exemple 2")
    print("3) Afficher DFS")
    print("4) Afficher BFS")
    print("5) Hauteur")
    print("6) Rechercher un nœud")
    print("7) Chemin entre 2 nœuds")
    print("8) Insérer un nœud")
    print("9) Modifier un nœud")
    print("10) Supprimer un nœud")
    print("11) Afficher un sous-arbre")
    print("12) Vérifier si l'arbre est complet")
    print("13) Sous-arbre complet maximal")
    print("14) Extraire un sous-arbre (copie)")
    print("15) Transformer en arbre binaire (préordre)")
    print("16) Évaluation expérimentale (tableau)")
    print("17) Affichage graphique (tkinter)")
    print("18) Exemples représentation vecteur")
    print("0) Quitter")


def _safe_input(prompt: str) -> str | None:
    """input() wrapper that avoids tracebacks on Ctrl+C / EOF.

    Returns None if the user cancels (KeyboardInterrupt) or if stdin is closed (EOFError).
    """

    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        return None


def _validate_label(label: str, *, field_name: str = "Info") -> bool:
    """Validate a node label according to the assignment constraints.

    The assignment specifies: words/strings of length <= 20.
    We keep UX minimal: print an error and let the caller return to the menu.
    """

    return _check_label(label, field_name=field_name) is not None


def _need_tree(arbre: ArbreNaire | None) -> bool:
    if arbre is None or arbre.racine is None:
        print(" Arbre vide. Choisissez d'abord 1 ou 2 pour construire un arbre.")
        return False
    return True


def lancer_menu() -> None:
    arbre = None

    while True:
        _print_menu()
        raw = _safe_input("\nVotre choix: ")
        if raw is None:
            print("\nArrêt du programme.")
            return
        choix = raw.strip()

        if choix == "0":
            print("Au revoir.")
            return

        if choix == "1":
            arbre = const_arbre1()
            print(" Arbre exemple 1 construit.")
            afficher_largeur(arbre)
            continue

        if choix == "2":
            arbre = const_arbre2()
            print(" Arbre exemple 2 construit.")
            afficher_largeur(arbre)
            continue

        if choix == "3":
            if not _need_tree(arbre):
                continue
            afficher_profondeur(arbre.racine)
            continue

        if choix == "4":
            if not _need_tree(arbre):
                continue
            afficher_largeur(arbre)
            continue

        if choix == "5":
            if not _need_tree(arbre):
                continue
            print(f"Hauteur: {calculer_hauteur(arbre)}")
            continue

        if choix == "6":
            if not _need_tree(arbre):
                continue
            raw = _safe_input("Info à rechercher: ")
            if raw is None:
                print("\nArrêt du programme.")
                return
            info = raw.strip()
            if not _validate_label(info, field_name="Info"):
                continue
            n = rechercher(arbre, info)
            if n:
                parent = n.parent.info if n.parent else "RACINE"
                print(f" Trouvé: {n.info} (parent={parent}, enfants={n.nb_enfants()})")
            else:
                print(" Non trouvé.")
            continue

        if choix == "7":
            if not _need_tree(arbre):
                continue
            raw_a = _safe_input("Info du nœud a: ")
            if raw_a is None:
                print("\nArrêt du programme.")
                return
            raw_b = _safe_input("Info du nœud b: ")
            if raw_b is None:
                print("\nArrêt du programme.")
                return
            a_info = raw_a.strip()
            b_info = raw_b.strip()
            if not _validate_label(a_info, field_name="Info du nœud a"):
                continue
            if not _validate_label(b_info, field_name="Info du nœud b"):
                continue
            a = rechercher(arbre, a_info)
            b = rechercher(arbre, b_info)
            chemin = chemin_entre_noeuds(a, b)
            if not chemin:
                print(" Chemin introuvable.")
            else:
                print("Chemin: " + " → ".join(n.info for n in chemin))
            continue

        if choix == "8":
            if not _need_tree(arbre):
                continue
            raw_p = _safe_input("Info du parent: ")
            if raw_p is None:
                print("\nArrêt du programme.")
                return
            raw_x = _safe_input("Info du nouveau nœud: ")
            if raw_x is None:
                print("\nArrêt du programme.")
                return
            p = raw_p.strip()
            x = raw_x.strip()
            if not _validate_label(p, field_name="Info du parent"):
                continue
            if not _validate_label(x, field_name="Info du nouveau nœud"):
                continue
            inserer_noeud(arbre, p, x)
            afficher_largeur(arbre)
            continue

        if choix == "9":
            if not _need_tree(arbre):
                continue
            raw_old = _safe_input("Info à modifier: ")
            if raw_old is None:
                print("\nArrêt du programme.")
                return
            raw_new = _safe_input("Nouvelle info: ")
            if raw_new is None:
                print("\nArrêt du programme.")
                return
            old = raw_old.strip()
            new = raw_new.strip()
            if not _validate_label(old, field_name="Info à modifier"):
                continue
            if not _validate_label(new, field_name="Nouvelle info"):
                continue
            modifier_noeud(arbre, old, new)
            afficher_largeur(arbre)
            continue

        if choix == "10":
            if not _need_tree(arbre):
                continue
            raw = _safe_input("Info du nœud à supprimer: ")
            if raw is None:
                print("\nArrêt du programme.")
                return
            info = raw.strip()
            if not _validate_label(info, field_name="Info du nœud à supprimer"):
                continue
            supprimer_noeud(arbre, info)
            afficher_largeur(arbre)
            continue

        if choix == "11":
            if not _need_tree(arbre):
                continue
            raw = _safe_input("Info racine du sous-arbre (ex: A, B, C, A2): ")
            if raw is None:
                print("\nArrêt du programme.")
                return
            info = raw.strip()
            if not _validate_label(info, field_name="Info racine du sous-arbre"):
                continue
            n = rechercher(arbre, info)
            if n is None:
                print(" Nœud non trouvé.")
            else:
                afficher_sous_arbre(n)
            continue

        if choix == "12":
            if not _need_tree(arbre):
                continue
            print("Complet" if est_arbre_complet(arbre) else "Non complet")
            continue

        if choix == "13":
            if not _need_tree(arbre):
                continue
            racine, taille = sous_arbre_complet_maximal(arbre)
            if racine is None:
                print(" Aucun sous-arbre complet.")
            else:
                print(f"Sous-arbre complet maximal: racine={racine.info}, taille={taille}")
                afficher_sous_arbre(racine)
            continue

        if choix == "14":
            if not _need_tree(arbre):
                continue
            raw = _safe_input("Info racine du sous-arbre à extraire (ex: C): ")
            if raw is None:
                print("\nArrêt du programme.")
                return
            info = raw.strip()
            if not _validate_label(info, field_name="Info racine du sous-arbre"):
                continue
            sous = extraire_sous_arbre(arbre, info)
            if sous is None:
                continue
            print("Sous-arbre extrait (copie) - BFS:")
            afficher_largeur(sous)
            continue

        if choix == "15":
            if not _need_tree(arbre):
                continue
            racine_b = transformer_en_arbre_binaire(arbre)
            print("Préordre binaire:")
            afficher_binaire_preordre(racine_b)
            continue

        if choix == "16":
            tailles = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
            repeats = 30
            res = evaluation_experimentale(tailles, degre=4, repeats=repeats)
            print("\nTableau expérimental (moyenne ± écart-type, en secondes):")
            print(f"repeats = {repeats}")
            print(f"{'n':>6} | {'complet (mean±std)':>24} | {'max (mean±std)':>24}")
            print("-" * 60)
            for n, mc, sc, mm, sm in res:
                print(f"{n:>6} | {mc:>10.6f}±{sc:<10.6f} | {mm:>10.6f}±{sm:<10.6f}")
            continue

        if choix == "17":
            if not _need_tree(arbre):
                continue
            afficher_graphique_tkinter(arbre)
            continue

        if choix == "18":
            print("\n1) Exemple vecteur 1")
            print("2) Exemple vecteur 2")
            raw = _safe_input("Votre choix: ")
            if raw is None:
                print("\nArrêt du programme.")
                return
            sub = raw.strip()
            if sub == "1":
                av = construire_arbre_vecteur_exemple1(degre=4)
                afficher_arbre_vecteur(av)
            elif sub == "2":
                av = construire_arbre_vecteur_exemple2(degre=4)
                afficher_arbre_vecteur(av)
            else:
                print(" Choix invalide.")
            continue

        print(" Choix invalide.")


def main() -> None:
    print("=" * 70)
    print("PROJET COMPLEXITE - ARBRES (MONO-FICHIER)")
    print("=" * 70)
    lancer_menu()


if __name__ == "__main__":
    main()
