# -*- coding: utf-8 -*-
"""
Relève la palette de l'interface SUR les cartes, au lieu de la choisir à l'œil.

C'est de ce relevé que sortent les variables CSS de la page : l'encre du bois est
bleu-ardoise (#2d343c) et non noire, le papier est #bdae9b, et les trois couleurs
imprimées sont l'ocre, la brique et le bleu. Le violet de la première version de MIROIR
n'apparaissait sur AUCUNE carte : c'était la part inventée, et c'est elle qui a sauté.

À lancer après outils/cartes_bnf.py, qui laisse les scans dans .cache-bnf/.
Usage :  python outils/palette.py
"""
import colorsys, os, sys
from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RACINE, ".cache-bnf")

def pixels(vue, l, h):
    im = Image.open(os.path.join(CACHE, "%03d.jpg" % vue)).convert("RGB")
    L, H = im.size
    # on reste DANS la carte : le bord porte le blanc du scan, qui fausserait tout
    im = im.crop((int(L * .10), int(H * .10), int(L * .90), int(H * .90))).resize((l, h))
    return list(im.get_flattened_data())

def moyenne(L):
    n = len(L)
    return "#%02x%02x%02x" % tuple(int(sum(x[i] for x in L) / n * 255) for i in range(3))

def main():
    if not os.path.isdir(CACHE):
        print("Pas de .cache-bnf/ : lance d'abord outils/cartes_bnf.py."); return 1
    faces = [v for v in range(1, 157, 2) if os.path.exists(os.path.join(CACHE, "%03d.jpg" % v))]
    if not faces:
        print("Aucune face dans .cache-bnf/."); return 1
    seaux, papier, encre = {}, [], []
    for vue in faces:
        for px in pixels(vue, 36, 70):
            r, g, b = [c / 255 for c in px]
            teinte, clarte, satur = colorsys.rgb_to_hls(r, g, b)
            if clarte > .62 and satur < .32: papier.append((r, g, b))
            if clarte < .22: encre.append((r, g, b))
            if satur < .18 or clarte < .10 or clarte > .93: continue
            seaux.setdefault(round(teinte * 36), []).append((r, g, b))
    print("faces échantillonnées : %d" % len(faces))
    for k, v in sorted(seaux.items(), key=lambda kv: -len(kv[1]))[:6]:
        print("  teinte %3d°  %7d px  %s" % (k * 10, len(v), moyenne(v)))
    print("  PAPIER       %7d px  %s" % (len(papier), moyenne(papier)))
    print("  ENCRE        %7d px  %s" % (len(encre), moyenne(encre)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
