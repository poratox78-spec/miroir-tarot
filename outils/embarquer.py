# -*- coding: utf-8 -*-
"""
Embarque les 78 lames, le dos et les trois fontes DANS index.html.

Pourquoi : une fois la page chargée, plus rien ne doit passer par le réseau. Pas pour
l'économie — les fichiers venaient déjà du même site — mais parce qu'un jeu qui tient
entièrement dans un fichier s'ouvre hors ligne, se copie sur une clé, et ne dépend de
personne. C'était le principe du projet avant les images ; il est rétabli.

La page se lit de haut en bas : l'écran de chargement est déclaré AVANT les données, et
chaque tranche est suivie d'un appel à __av() qui fait avancer la barre à mesure que les
octets arrivent. La progression est donc réelle, pas une animation qui fait semblant.

⚠ Les marqueurs doivent être UNIQUES. Le premier essai utilisait « --> » comme début : il
tombait sur le commentaire d'en-tête du fichier, et l'outil a effacé toute la page sans que
rien ne le signale. D'où `entre()` qui exige l'unicité, et la garde d'ancres avant d'écrire.

Relançable à l'identique. Usage :  python outils/embarquer.py
"""
import base64, io, os, sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(RACINE, "index.html")
TRANCHES = 10                      # autant de paliers visibles sur la barre
SAUT = chr(10)

# ce sans quoi il n'y a plus de produit : l'outil refuse d'écrire une page qui en perd une
ANCRES = ["<style>", "</style>", "<body>", "<header>", 'id="table"', "'use strict'",
          "<footer>", "function ajusterLames", "const ART = (function(){",
          'id="chargement"', "function peindre"]

def uri(chemin, genre):
    return "data:%s;base64,%s" % (genre, base64.b64encode(open(chemin, "rb").read()).decode())

def entre(texte, debut, fin, neuf):
    for m in (debut, fin):
        if texte.count(m) != 1:
            print("marqueur présent %d fois, il en faut une : %s" % (texte.count(m), m))
            sys.exit(1)
    d, f = texte.index(debut), texte.index(fin)
    if f < d:
        print("marqueurs inversés : %s après %s" % (debut, fin)); sys.exit(1)
    return texte[:d + len(debut)] + neuf + texte[f:]

def main():
    avant = io.open(PAGE, encoding="utf-8").read()
    s = avant

    # ── les fontes ────────────────────────────────────────────────────────────────────────
    bloc = ""
    for nom, fichier, gras in [("Fell", "fell.woff2", 400), ("FellPC", "fellsc.woff2", 400),
                               ("Gothique", "gothique.woff2", 700)]:
        u = uri(os.path.join(RACINE, "polices", fichier), "font/woff2")
        bloc += (SAUT + '  @font-face{ font-family:"%s"; src:url(%s) format("woff2");' % (nom, u)
                 + SAUT + '              font-weight:%d; font-style:normal; font-display:swap; }' % gras)
    s = entre(s, "/* ##POLICES-DEBUT## */", "/* ##POLICES-FIN## */", bloc + SAUT + "  ")

    # ── les lames ─────────────────────────────────────────────────────────────────────────
    noms = sorted(f[:-5] for f in os.listdir(os.path.join(RACINE, "cartes")) if f.endswith(".webp"))
    if len(noms) != 79:
        print("attendu 79 images dans cartes/, trouvé %d" % len(noms)); sys.exit(1)
    pas = (len(noms) + TRANCHES - 1) // TRANCHES
    tete = (SAUT + "<script>window.LAMES={};window.__av=function(p){"
            "var e=document.getElementById('chargement-part');if(e)e.style.width=p+'%';};</script>")
    morceaux = [tete]
    for i in range(0, len(noms), pas):
        tranche = noms[i:i + pas]
        paires = ",".join('"%s":"%s"' % (n, uri(os.path.join(RACINE, "cartes", n + ".webp"), "image/webp"))
                          for n in tranche)
        avance = round(min(100, (i + len(tranche)) / len(noms) * 100))
        morceaux.append(SAUT + "<script>Object.assign(LAMES,{%s});__av(%d)</script>" % (paires, avance))
    s = entre(s, "<!-- ##LAMES-DEBUT## -->", "<!-- ##LAMES-FIN## -->", "".join(morceaux) + SAUT)

    # ── on REFUSE d'écrire une page mutilée ───────────────────────────────────────────────
    perdues = [a for a in ANCRES if a not in s]
    if perdues:
        print("REFUS : la page perdrait %s" % perdues); sys.exit(1)
    if len(s) <= len(avant) and "base64" not in avant:
        print("REFUS : la page devrait grossir (%d → %d)" % (len(avant), len(s))); sys.exit(1)

    io.open(PAGE, "w", encoding="utf-8", newline="").write(s)

    # ── les gardes, lues sur ce qui a été écrit ───────────────────────────────────────────
    ecrit = io.open(PAGE, encoding="utf-8").read()
    dedans = ecrit.count(':"data:image/webp;base64,')
    restes = [m for m in ("url(cartes/", "url(polices/") if m in ecrit]
    print("lames embarquées           : %d (attendu 79)" % dedans)
    print("tranches de chargement     : %d" % (len(morceaux) - 1))
    print("renvois à un fichier local : %s" % (restes or "aucun"))
    print("ancres de structure        : %d / %d" % (len([a for a in ANCRES if a in ecrit]), len(ANCRES)))
    print("page                       : %.2f Mo" % (len(ecrit.encode("utf-8")) / 1048576))
    ok = (dedans == 79 and not restes and all(a in ecrit for a in ANCRES))
    print(SAUT + ("LA PAGE SE SUFFIT À ELLE-MÊME." if ok else "ÉCHEC : voir ci-dessus."))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
