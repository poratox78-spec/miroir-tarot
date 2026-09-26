# -*- coding: utf-8 -*-
"""
ÉLARGIT LA TABLE DE THÈMES PAR LA MORPHOLOGIE, à partir des lexiques d'OMEGA.

Pourquoi : la table de MIROIR est écrite à la main en GRAINES lisibles (« travail », « fatigue »,
« choisir »). Mais quelqu'un écrit « je travaille », « je suis fatiguée », « j'ai choisi ». Lister
toutes les formes à la main serait interminable et se périmerait. On les engendre.

Source : data_local/Lexique4.tsv du dépôt OMEGA PENDU (colonnes : mot, lemme, catégorie,
fréquence de la forme écrite). Rien n'est recopié dans MIROIR : seules les formes fléchies des
graines déjà choisies à la main en sortent.

DEUX GARDES, et elles viennent toutes les deux d'une mesure, pas d'une intuition :

  ① le lemme de CITATION d'abord. « couple » est rattaché au verbe « coupler » dans Lexique ;
    sans cette garde, le thème amour recevait « couplera », « couplant », « couplée ».
    On prend donc le lemme dont la forme de citation EST la graine, sinon le plus fréquent.

  ② les MOTS-OUTILS dehors, et pas de seuil de fréquence. La graine « dois » tirait tout le
    paradigme de « devoir » — dont « du », fréquence 4124, qui aurait déclenché « choix » sur
    presque toutes les questions. Un seuil de fréquence NE MARCHE PAS ici : « moi », graine
    voulue, culmine à 5018, au-dessus de « du ». Ce qui les sépare n'est pas la fréquence mais
    la NATURE : « du » est un article. On écarte donc toute forme qui a une lecture
    article / préposition / conjonction / pronom / auxiliaire.
    Et les modaux (dois, faut, peux, veux…) ne s'élargissent pas du tout : leur paradigme est
    de la grammaire, pas du sens.

Usage :
    python outils/elargir_lexique.py [chemin/vers/OMEGA PENDU]

Le script réécrit le bloc LEXIQUE_ELARGI dans index.html, entre ses deux balises.
"""
import collections
import io
import json
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(ICI, '..', 'index.html')
OMEGA_DEFAUT = os.path.expanduser(r'~\Documents\GitHub\OMEGA PENDU')

CONTENU = ('NOM', 'VER', 'ADJ', 'ADV')
OUTILS = ('ART', 'PRE', 'CON', 'PRO', 'AUX')
SANS_ELARGIR = {'dois', 'faut', 'peux', 'veux', 'vais', 'suis', 'est', 'ai', 'fait'}

DEBUT = '// ⟦LEXIQUE_ELARGI — engendré par outils/elargir_lexique.py, ne pas éditer à la main⟧'
FIN = '// ⟦fin LEXIQUE_ELARGI⟧'


def desaccentue(mot):
    return ''.join(c for c in unicodedata.normalize('NFD', mot.lower())
                   if unicodedata.category(c) != 'Mn')


def lire_graines(page):
    bloc = page[page.index('const LEXIQUE = {'):page.index('// mots trop courants')]
    return {theme: re.findall(r'"([^"]+)"', corps)
            for theme, corps in re.findall(r'(\w+):\s*\[(.*?)\]', bloc, re.S)}


def lire_lexique4(chemin):
    formes = collections.defaultdict(set)
    candidats = collections.defaultdict(list)
    categories = collections.defaultdict(set)
    with io.open(chemin, encoding='utf-8') as f:
        f.readline()
        for ligne in f:
            col = ligne.rstrip('\n').split('\t')
            if len(col) < 12:
                continue
            mot, lemme, cat = desaccentue(col[0]), desaccentue(col[3]), col[4]
            if not mot or not lemme:
                continue
            try:
                freq = float(col[10] or 0)          # FreqOrtho : la forme écrite
            except ValueError:
                freq = 0.0
            formes[(lemme, cat)].add(mot)
            candidats[mot].append((lemme, cat, freq))
            categories[mot].add(cat)
    return formes, candidats, categories


def famille(graine, formes, candidats, categories):
    if graine in SANS_ELARGIR:
        return {graine}
    cands = candidats.get(graine)
    if not cands:
        return {graine}
    propres = [c for c in cands if c[0] == graine]          # garde ①
    choix = max(propres or cands, key=lambda c: c[2])
    if not choix[1].startswith(CONTENU):
        return {graine}
    retenues = {graine}
    for forme in formes[(choix[0], choix[1])]:
        if any(c.startswith(OUTILS) for c in categories.get(forme, ())):   # garde ②
            continue
        retenues.add(forme)
    return retenues


def main():
    racine = sys.argv[1] if len(sys.argv) > 1 else OMEGA_DEFAUT
    lex4 = os.path.join(racine, 'data_local', 'Lexique4.tsv')
    if not os.path.exists(lex4):
        print('✗ introuvable : ' + lex4)
        print('  usage : python outils/elargir_lexique.py "<racine du dépôt OMEGA PENDU>"')
        return 2

    page = io.open(PAGE, encoding='utf-8').read()
    graines = lire_graines(page)
    formes, candidats, categories = lire_lexique4(lex4)

    elargi = {}
    for theme, mots in graines.items():
        ens = set()
        for mot in mots:
            ens |= famille(mot, formes, candidats, categories)
        elargi[theme] = sorted(ens)

    nb_graines = sum(len(v) for v in graines.values())
    nb_formes = sum(len(v) for v in elargi.values())

    # collisions : une forme dans deux thèmes. Elles sont légitimes (« copain » est amitié ET
    # amour) mais on les affiche, pour qu'une nouvelle collision se remarque.
    ou = collections.defaultdict(set)
    for theme, mots in elargi.items():
        for mot in mots:
            ou[mot].add(theme)
    collisions = {m: sorted(t) for m, t in ou.items() if len(t) > 1}

    lignes = [DEBUT,
              '// %d graines → %d formes. Régénérer après toute modification de LEXIQUE.'
              % (nb_graines, nb_formes),
              'const LEXIQUE_ELARGI = {']
    for theme in sorted(elargi):
        lignes.append('  %s: %s,' % (theme, json.dumps(' '.join(elargi[theme]), ensure_ascii=False)))
    lignes += ['};', FIN]
    bloc = '\n'.join(lignes)

    if DEBUT in page:
        page = re.sub(re.escape(DEBUT) + r'.*?' + re.escape(FIN), lambda _: bloc, page, flags=re.S)
    else:
        ancre = 'const VIDES = ['
        page = page.replace(ancre, bloc + '\n\n' + ancre)
    io.open(PAGE, 'w', encoding='utf-8', newline='\n').write(page)

    print('graines : %d → formes : %d (×%.1f)' % (nb_graines, nb_formes, nb_formes / nb_graines))
    print('collisions entre thèmes : %d  %s' % (len(collisions), collisions))
    print('écrit dans index.html')
    return 0


if __name__ == '__main__':
    sys.exit(main())
