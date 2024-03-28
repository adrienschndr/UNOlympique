def creer_pile_vide():
    return []


def est_vide(p):
    return p == []


def empiler(n, p):
    p.append(n)
    return p


def depiler(p):
    if not est_vide(p):
        return p.pop()


def sommet(p):
    if est_vide(p):
        return None
    return p[-1]


def taille(p):
    return len(p)
