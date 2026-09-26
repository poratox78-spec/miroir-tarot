# -*- coding: utf-8 -*-
"""
Fabrique les deux images de vitrine, à partir des vraies lames et des vraies fontes :

  MIROIR-couverture.png   630 × 500   la couverture itch.io (format qu'ils recommandent)
  social.png             1200 × 630   l'aperçu des liens (Discord, Twitter, Signal…)

Sans la seconde, un lien collé dans Discord n'affiche RIEN : le déplieur de liens lit les
balises Open Graph, et une balise og:image sans image publiquement joignable ne sert à rien.
Celle-ci est donc commitée, contrairement aux autres fichiers dérivés.

Dépendances : Pillow, et les .ttf dans polices/. Usage :  python outils/couverture.py
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POL = os.path.join(RACINE, "polices")
NUIT, HAUT = (20, 26, 32), (36, 49, 58)
OR, PARCH, MUET, GRIS = (201, 169, 89), (233, 223, 201), (142, 155, 165), (126, 140, 150)
PHRASE = "Un tirage ne pr\u00e9dit rien. Les lames servent de miroir."
CREDIT = "78 lames grav\u00e9es \u2014 scans BnF, domaine public \u00b7 tout tient dans une page"

def police(nom, taille):
    return ImageFont.truetype(os.path.join(POL, nom), taille)

def dessiner(L, H, lames, ech):
    im = Image.new("RGB", (L, H), NUIT)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = max(0.0, 1 - (y / (H * 0.72)) ** 1.4)
        d.line([(0, y), (L, y)], fill=tuple(int(NUIT[i] + (HAUT[i] - NUIT[i]) * t) for i in range(3)))

    for nom, angle, (cx, cy), (lc, hc) in lames:
        c = Image.open(os.path.join(RACINE, "cartes", nom + ".webp")).convert("RGBA")
        c.thumbnail((lc, hc), Image.LANCZOS)
        cadre = Image.new("RGBA", (c.width + 4, c.height + 4), (189, 174, 155, 195))
        cadre.paste(c, (2, 2))
        r = cadre.rotate(angle, expand=True, resample=Image.BICUBIC)
        ombre = Image.new("RGBA", r.size, (0, 0, 0, 0))
        ombre.paste((0, 0, 0, 115), (0, 0), r.split()[3])
        im.paste(ombre, (cx - r.width // 2 + 5, cy - r.height // 2 + 9), ombre)
        im.paste(r, (cx - r.width // 2, cy - r.height // 2), r)

    goth, sc = police("Gothique.ttf", ech["titre"]), police("FellSC.ttf", ech["sous"])
    corps, petit = police("FellCanon.ttf", ech["corps"]), police("FellCanon.ttf", ech["petit"])
    tw = d.textbbox((0, 0), "MIROIR", font=goth)[2]
    sw = d.textbbox((0, 0), "\u00b7 tarot", font=sc)[2]
    total = tw + ech["ecart"] + sw
    x0 = (L - total) // 2
    d.text((x0, ech["y_titre"]), "MIROIR", font=goth, fill=PARCH)
    d.text((x0 + tw + ech["ecart"], ech["y_sous"]), "\u00b7 tarot", font=sc, fill=OR)
    d.line([(x0, ech["y_trait"]), (x0 + total, ech["y_trait"])], fill=OR, width=1)
    pw = d.textbbox((0, 0), PHRASE, font=corps)[2]
    d.text(((L - pw) // 2, ech["y_phrase"]), PHRASE, font=corps, fill=MUET)

    voile = Image.new("RGBA", (L, ech["bande"]), (20, 26, 32, 215))
    bas = im.crop((0, H - ech["bande"], L, H)).convert("RGBA")
    im.paste(Image.alpha_composite(bas, voile).convert("RGB"), (0, H - ech["bande"]))
    bw = d.textbbox((0, 0), CREDIT, font=petit)[2]
    d.text(((L - bw) // 2, H - ech["bande"] + ech["y_credit"]), CREDIT, font=petit, fill=GRIS)
    return im

def main():
    if not os.path.exists(os.path.join(POL, "Gothique.ttf")):
        print("Il manque les .ttf dans polices/ (Gothique, FellSC, FellCanon)."); return 1

    couv = dessiner(630, 500,
        [("dos", -15, (158, 300), (133, 258)), ("M1", 0, (315, 292), (133, 258)),
         ("M13", 15, (472, 300), (133, 258))],
        dict(titre=60, sous=26, corps=19, petit=16, ecart=16,
             y_titre=26, y_sous=51, y_trait=98, y_phrase=111, bande=62, y_credit=22))
    p1 = os.path.join(RACINE, "MIROIR-couverture.png"); couv.save(p1)

    soc = dessiner(1200, 630,
        [("dos", -16, (300, 400), (168, 326)), ("M2", -6, (480, 384), (168, 326)),
         ("M1", 4, (660, 384), (168, 326)), ("M13", 16, (860, 400), (168, 326))],
        dict(titre=86, sous=36, corps=27, petit=20, ecart=22,
             y_titre=44, y_sous=80, y_trait=150, y_phrase=168, bande=70, y_credit=24))
    p2 = os.path.join(RACINE, "social.png"); soc.save(p2)

    for p, attendu in [(p1, (630, 500)), (p2, (1200, 630))]:
        im = Image.open(p)
        ok = im.size == attendu
        print("%-24s %dx%d %s  %d ko" % (os.path.basename(p), im.width, im.height,
              "" if ok else "TAILLE INATTENDUE", os.path.getsize(p) // 1024))
    return 0

if __name__ == "__main__":
    sys.exit(main())
