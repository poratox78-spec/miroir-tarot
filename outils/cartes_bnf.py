# -*- coding: utf-8 -*-
"""
Refabrique le dossier cartes/ depuis Wikimedia Commons.

La source : « Jeu de tarot à enseignes italiennes dit "de Marseille", sur le modèle du tarot
de Nicolas Conver », tirage situé entre 1890 et 1900, numérisé par la Bibliothèque nationale
de France sous la cote btv1b10539497f. DOMAINE PUBLIC (champs LicenseShortName « Public
domain », License « pd », UsageTerms « Public domain » relevés via l'API Commons).

LA TABLE — c'est le seul point qui ne se devine pas, et il a été établi en regardant des
planches-contact des 156 vues, puis vérifié de bout en bout :

    vues IMPAIRES = les faces, vues PAIRES = les dos
    Deniers   As→Roy : 1, 3, … 27       (repère : 21 « VALET DE DENIERS », 27 « ROY DE DENIERS »)
    Coupes    As→Roy : 29, 31, … 55     (repère : 49 « VALET DE COUPE »,  55 « ROY DE COUPE »)
    Épées     As→Roy : 57, 59, … 83     (repère : 77 « VALET D'EPEE »,    83 « ROY D'EPEE »)
    Bâtons    As→Roy : 85, 87, … 111
    Majeurs   I→XXI  : 113, 115, … 153  (repère : 113 « LE BATELEUR », 153 « LE MONDE »)
    Le Mat            : 155             (il ferme le jeu, il n'ouvre pas)

Les identifiants sont ceux du moteur (§MINEURS) : d1…d14, c1…c14, e1…e14, b1…b14, M0…M21.

Dépendances : Pillow. Usage :  python outils/cartes_bnf.py [largeur] [qualité]
Sans argument, il reproduit exactement les images du dépôt (260 px, qualité 76).
"""
import hashlib, os, statistics, sys, time, urllib.parse, urllib.request
from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST   = os.path.join(RACINE, "cartes")
CACHE  = os.path.join(RACINE, ".cache-bnf")
TITRE  = ('Jeu de tarot à enseignes italiennes dit "de Marseille", sur le modèle du tarot de '
          'Nicolas Conver - jeu de cartes, estampe - btv1b10539497f (%03d of 156).jpg')
UA     = {"User-Agent": "miroir-tarot/1.0 (projet perso non commercial; "
                        "github.com/poratox78-spec/miroir-tarot)"}
FOND   = 198        # au-dessus de ce gris, c'est le fond blanc du scan, pas la carte
RAPPORT = 0.5102    # rapport largeur/hauteur retenu (mesuré : 0,509 … 0,517)

# ⚠ Ces deux réglages sont ceux des images COMMITÉES dans cartes/. Lancé sans argument, le
# script doit reproduire le dépôt à l'octet près — sinon la commande qu'on documente ne
# refabrique pas ce qui est livré, et le dossier de travail diverge du site sans rien dire.
# (C'est arrivé : les défauts étaient restés à 280/78 alors que le livré était en 260/76,
# et la page refabriquée pesait 3,32 Mo au lieu de 2,75.)
LARGEUR = 260       # couvre le pire cas d'affichage : 108 px CSS × 2, ou 77 × 3 sur mobile dense
QUALITE = 76

def table():
    t = {}
    for lettre, depart in [("d", 1), ("c", 29), ("e", 57), ("b", 85)]:
        for rang in range(1, 15):
            t["%s%d" % (lettre, rang)] = depart + 2 * (rang - 1)
    for n in range(1, 22):
        t["M%d" % n] = 113 + 2 * (n - 1)
    t["M0"] = 155
    t["dos"] = 2
    return t

def aspirer(vue):
    """Récupère une vue, en cache sur le disque. Poli : une requête à la fois, et on attend
    quand Commons répond 429 plutôt que de marteler."""
    os.makedirs(CACHE, exist_ok=True)
    chemin = os.path.join(CACHE, "%03d.jpg" % vue)
    if os.path.exists(chemin) and os.path.getsize(chemin) > 5000:
        return chemin
    url = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
           + urllib.parse.quote((TITRE % vue).replace(" ", "_")) + "?width=640")
    for essai in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                open(chemin, "wb").write(r.read())
            return chemin
        except Exception as e:
            if essai == 4:
                raise
            time.sleep(5 * (essai + 1))

def bords(im):
    """Le recadrage est MESURÉ, pas deviné : on entre depuis chaque bord tant que la ligne
    reste aussi claire que le fond du scan."""
    g = im.convert("L")
    l, h = g.size
    col = [statistics.mean(g.crop((x, 0, x + 1, h)).get_flattened_data()) for x in range(l)]
    lig = [statistics.mean(g.crop((0, y, l, y + 1)).get_flattened_data()) for y in range(h)]
    def entrer(v):
        a = 0
        while a < len(v) - 1 and v[a] >= FOND: a += 1
        b = len(v) - 1
        while b > a and v[b] >= FOND: b -= 1
        return a, b + 1
    x0, x1 = entrer(col)
    y0, y1 = entrer(lig)
    return x0, y0, x1, y1

def main():
    larg = int(sys.argv[1]) if len(sys.argv) > 1 else LARGEUR
    qual = int(sys.argv[2]) if len(sys.argv) > 2 else QUALITE
    os.makedirs(DEST, exist_ok=True)
    t = table()
    rapports, poids, empreintes = [], {}, {}
    for nom, vue in sorted(t.items(), key=lambda kv: kv[1]):
        im = Image.open(aspirer(vue)).convert("RGB")
        c = im.crop(bords(im))
        rapports.append(c.width / c.height)
        c = c.resize((larg, round(larg / RAPPORT)), Image.LANCZOS)
        p = os.path.join(DEST, nom + ".webp")
        c.save(p, "WEBP", quality=qual, method=6)
        poids[nom] = os.path.getsize(p)
        empreintes.setdefault(hashlib.sha1(open(p, "rb").read()).hexdigest(), []).append(nom)
        time.sleep(0.2)

    # ── les gardes : elles doivent pouvoir échouer, sinon elles ne disent rien ─────────────
    ecrits = len(poids)
    doublons = [v for v in empreintes.values() if len(v) > 1]
    petits = [n for n, o in poids.items() if o < 6000]
    print("réglages                  : %d px, qualité %d%s"
          % (larg, qual, "" if (larg, qual) == (LARGEUR, QUALITE)
             else "   ⚠ DIFFÈRENT du dépôt (%d px, q%d) : les images vont diverger du site"
                  % (LARGEUR, QUALITE)))
    print("cartes écrites            : %d (attendu 79 : 78 faces + le dos)" % ecrits)
    print("rapport après recadrage   : min %.3f | médiane %.3f | max %.3f"
          % (min(rapports), statistics.median(rapports), max(rapports)))
    print("poids                     : total %.2f Mo | moyen %d ko | max %d ko"
          % (sum(poids.values()) / 1048576, sum(poids.values()) / ecrits / 1024,
             max(poids.values()) / 1024))
    print("empreintes distinctes     : %d" % len(empreintes))
    print("DOUBLONS                  : %s" % (doublons or "aucun"))
    print("fichiers suspects (<6 ko) : %s" % (petits or "aucun"))
    ok = (ecrits == 79 and not doublons and not petits)
    print("\n%s" % ("TOUT EST EN PLACE." if ok else "ÉCHEC : voir ci-dessus."))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
