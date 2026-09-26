# Ce que le correcteur OMEGA dit de MIROIR — et ce que MIROIR dit d'OMEGA

Relevé du 26/09/2026. **Rien n'a été corrigé dans OMEGA** : ce fichier ne fait que noter, pour
plus tard.

## Comment la mesure a été faite

Les 4 828 phrases distinctes que MIROIR peut écrire (lecture lame par lame pour les 78 lames ×
2 sens × toutes les places, lectures d'ensemble, vannes de charriage, registres) ont été passées
au **moteur réel** : `dictee/navigateur_flags_dump.js`, qui interroge `diagnoseAll` dans un vrai
Chrome avec l'extension chargée. Pas le harnais Python, qui ne reproduit pas l'arbitrage réel.

## Résultat brut

| | |
|---|---|
| phrases passées | 4 828 |
| phrases sans aucune marque | 4 081 (84,5 %) |
| phrases avec au moins une marque | 747 (15,5 %) |
| **marques rouges** | **0** |
| marques oranges | 781 |

**Zéro rouge sur 4 828 phrases** : aucune faute d'orthographe caractérisée dans les textes de
MIROIR.

## Ce que MIROIR devait corriger (fait)

Trois tournures bancales, pas des fautes, mais du français mal écrit — le correcteur les a
signalées et il avait raison :

1. « vers quelque chose de plus simple ou de **pas réglé** » → « …ou qui n'a jamais été réglé ».
2. « **ses projets, c'est** plein à ras bord chez X » → « **Sur** ses projets, c'est… ».
3. « **son argent, ça** vient de secouer chez X » → « **Sur** son argent, ça… ».

Un groupe pluriel repris par « c'est » ou « ça » passe à l'oral, mais s'écrit mal.

## Points notés pour OMEGA (rien n'a été touché)

### 1 · La tête d'un groupe nominal « Le X de Y-pluriel » — 400 marques

    « Le Quatre de Bâtons installe, pose et rend stable »   → propose « installent »
    « Le Dix de Coupes achève le cycle »                    → propose « achèvent »

Le sujet est **Quatre**, singulier, annoncé par **Le**. Le moteur prend le nom pluriel le plus
proche du verbe (**Bâtons**, **Coupes**) pour tête du groupe. Le déterminant de tête est pourtant
disponible et non ambigu.

À elles deux, ces deux formes font **346 des 400 marques** de la règle d'accord verbe.

### 2 · « a/à » au palier AUTO sur une locution figée — 135 marques

    « Et tout ça à l'envers, évidemment. »   → propose « a », au palier **auto**

C'est un **mot juste réécrit**, au palier qui applique. « à l'envers » est une locution figée.
La piste : une liste fermée de locutions en « à » (à l'envers, à l'endroit, à la fois, à peu
près…) qui interdirait la substitution. Le cas de confusion légitime est « ça a l'air ».

### 3 · « ou/où » sur une coordination de deux propositions — 175 marques

    « il arrive ou il part »                        → propose « où »
    « Est-ce que tu t'en sers, ou est-ce que… »     → propose « où »

Quand « ou » coordonne deux propositions complètes, ce n'est jamais « où ».

### 4 · Genre d'un composé à traits d'union — 28 marques

    « un face-à-face qui tient »   → propose « une »

« face-à-face » est masculin ; le moteur semble lire le genre de « face ».

### 5 · Accord d'un attribut impersonnel — 14 marques

    « c'est plein à ras bord »   → propose « pleins »

Dans « c'est plein », « plein » est invariable.

### 6 · Deux marques mineures, non élucidées

- **virgule** (18) : une virgule réclamée dans des phrases qui en ont déjà une, sans que la
  position ait pu être identifiée — le dump ne rend pas l'index pour ces marques.
- **infinitif après semi-auxiliaire** (3) : « La **lame** est à l'envers » → propose « lamer ».

## Deuxième passe — 6 844 phrases (26/09, après la journée)

Le corpus a grossi (les deux tons de charriage, les 72 relances, les registres) : **6 844 phrases,
toujours 0 rouge**, 1 001 oranges. Les familles ci-dessus se retrouvent aux mêmes proportions —
tête du groupe nominal 492, ou/où 219, a/à au palier auto 180.

**Deux familles nouvelles**, toutes deux sur du texte correct :

### 7 · Inversion du sujet avec « -tu » — 25 marques

    « Quelle option choisirais-tu si personne ne regardait ? »   → propose « choisirait »
    « Quelles règles t'appliques-tu, et d'où viennent-elles ? »   → « viennent » → « vient »

Le pronom inversé après trait d'union n'est pas pris pour le sujet ; dans le second cas c'est
« elles » qui commande, pas le singulier.

### 8 · « le sujet clos » — 24 marques

    « considère le sujet clos à vie »   → propose « clôt »

Le mot **sujet** est lu comme un sujet grammatical, et **clos** comme le verbe *clore*. C'est un
adjectif.

## Ce que cette campagne vaut comme corpus

Ces 4 828 phrases sont du **français correct, écrit, varié et inédit** — donc un banc de faux
positifs gratuit, du genre que le corpus dys ne fournit pas. Le fichier d'entrée se régénère à
volonté depuis `index.html`.
