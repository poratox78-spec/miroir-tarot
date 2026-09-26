# Audit de MIROIR — 26/09/2026

Passe complète après la journée de construction. Tout ce qui suit est **mesuré**, pas estimé.

## 1 · Code mort et non-branché

| contrôle | résultat |
|---|---|
| fonctions et constantes définies | 82 — **aucune inutilisée** |
| classes CSS déclarées | 37 — **aucune orpheline** |
| motifs de dessin demandés par les recettes | 61 — **aucun absent** de la table |
| `ART.inconnus` en production | **0** |

## 2 · Les gardes savent-elles encore échouer ?

Une garde qu'on ne falsifie pas n'est pas une garde. Les trois ont été re-cassées exprès :

| garde | falsification | résultat |
|---|---|---|
| registre des motifs fantômes | dessiner une lame appelant `motif-inexistant` | **0 → 1**, et elle le nomme |
| la table ne devine pas | `themeDe("xylophonium brrr zzz")` | **null** — et `"mon taf"` → `travail` |
| le tirage est sourd à la question | 1 500 tirages avec question contre 1 500 sans | écart max **24** pour 58 attendus par lame — dans le bruit |

## 3 · Langue — 6 844 phrases au correcteur OMEGA

Toutes les phrases que MIROIR peut écrire (lecture lame par lame × 78 lames × 2 sens × toutes
les places × 10 thèmes, lectures d'ensemble, **les deux tons** de charriage, registres, relances),
passées à `diagnoseAll` dans un vrai Chrome.

| | |
|---|---|
| phrases | 6 844 |
| sans aucune marque | 5 885 (86 %) |
| **marques rouges** | **0** |
| marques oranges | 1 001 |

**Zéro rouge, et aucune des 1 001 oranges n'est une faute de MIROIR** : ce sont les familles de
faux positifs déjà relevées dans `NOTES-OMEGA.md`, plus deux nouvelles (voir ce fichier).

## 4 · Bancs

| banc | résultat |
|---|---|
| `bancs/questions_familieres.json` | **26/26** |
| `bancs/questions_sans_theme.json` | **20/20 restent muettes** |
| couverture thème × axe des relances | **72/72**, 0 repli silencieux sur 702 paires |
| répétition de relance dans un tirage | **0** sur 3 000 tirages de cinq lames |
| charriage, gabarits non remplacés | **0** sur 8 000 tirages par ton |

## 5 · Ce que l'audit a trouvé

**Un seul défaut, et il était dans la documentation.** La liste « ce qui reste à faire » du README
réclamait encore les entrelacs floraux, le corps du lion, les cornes du Diable, les pattes des
chevaux et les répétitions multiples — **tous faits depuis des heures**. Une liste de restes fausse
fait retravailler ce qui est fini et cache ce qui manque vraiment. Corrigée, avec l'avertissement.

## 6 · Le trafic Twitch réel — PROUVÉ le 26/09 sur `#nalahri`

C'était le dernier point non vérifié du projet. Rem a fourni une chaîne en direct, et la chaîne
complète a tourné sur du trafic vivant.

**Ce qui a failli conclure à tort** : deux fenêtres d'écoute de 16 et 22 secondes ont donné
**zéro pseudo**. Le chat est irrégulier — 4 messages sur une fenêtre de 20 s, 0 sur la suivante.
Conclure « le parseur ne marche pas » là-dessus aurait été une erreur de mesure.

La socket **brute** a tranché : les PRIVMSG arrivaient bien. Puis une vraie trame, capturée et
donnée telle quelle au parseur :

    @badge-info=subscriber/82;badges=vip/1,subscriber/60,pichu/1;…;display-name=Mp0o;…
     :mp0o!mp0o@mp0o.tmi.twitch.tv PRIVMSG #nalahri
    → {type:"message", pseudo:"mp0o", rang:"abonnes"}

Puis la chaîne entière, en direct :

| étape | résultat |
|---|---|
| panneau branché sur `#nalahri` | connecté |
| un vrai spectateur parle | son pseudo apparaît dans la liste |
| clic sur ce pseudo, avec « mon taf me gonfle » dans la barre | **Tirage pour malaedya**, question citée, registre **de travail** reconnu sur *taf*, charriage écrit |

**Le projet n'a plus de maillon non vérifié.**

## 7 · Après l'audit — les points faibles traités le même jour

L'audit ne cherchait que les défauts *mécaniques*. Une relecture critique a ensuite trouvé trois
faiblesses de conception, mesurées puis corrigées :

| point faible | mesure | corrigé |
|---|---|---|
| le permalien perdait la question, le pseudo et le ton | partager un charriage donnait une lecture plate | `&q=` `&p=` `&ton=`, rejeu vérifié à froid |
| une lame ne donnait que 3 textes distincts | la phrase du moteur ne variait jamais | 36 secondes formulations → **3 → 6** |
| gris le plus pâle à **3,50** de contraste | sous le seuil AA de 4,5 | remonté aux trois endroits |

Puis deux points mineurs : le réglage du **ton** apparaît désormais sous la lecture, là où il
agit, et le changer **réécrit la même donne** au lieu de retirer ; un **journal local** garde les
vingt derniers tirages, stockant exactement ce que porte le permalien — rejouer, c'est ouvrir le
lien, donc aucune logique dupliquée.

## 8 · La mise en page — le chiffre ne suffisait pas

| tirage | avant | après |
|---|---|---|
| une lame / trois lames | bas à 626 | **498** |
| la croix | bas à **1074**, soit 306 px de trop | **732**, débordement **0** |

La taille des lames se calcule à partir de la place réellement disponible (bornes 105–210 px),
recalculée à chaque pose et à chaque redimensionnement — un réglage fixe n'aurait valu que pour
un écran.

⚠️ **Et le calcul a menti une fois** : il annonçait « ça rentre » alors que la capture montrait
trois étiquettes qui se chevauchaient. Corrigé en retirant l'**intitulé de place** en mode serré —
dans une croix, les positions se lisent à leur place et la lecture les nomme toutes. *Sur une
question de mise en page, le nombre ne remplace pas le regard.*

---

# Addendum — 26/09/2026, après le passage aux vraies lames

Les chiffres de mise en page ci-dessus sont **périmés** : ils ont été mesurés sur des lames au
rapport 2/3. Depuis, la lame a sa vraie silhouette (0,513) et une troisième rangée de boutons
est apparue. Nouvelle campagne, mesurée en ligne, jamais en local — le panneau d'aperçu
neutralise les scripts d'une page locale, et le serveur local tronque encore la réponse.

## Ce que la nouvelle mesure a trouvé

| défaut | comment il s'est vu | état |
|---|---|---|
| `<html>` sans fond | du blanc apparaissait sous la page pendant le défilement | corrigé |
| `.role` à hauteur figée (15 px) | « CE QUI A MENÉ LÀ » passe sur deux lignes dans une lame de 108 px, et se faisait couper | corrigé |
| la rangée de commandes sur deux lignes | elle réclame **953 px** et n'en avait que **924** : ce n'était pas l'écran, c'était `max-width:960px` | panneau élargi à 1060 px |
| la croix débordait de **38 px** | le calcul disait « ça tient » pendant que la mesure disait le contraire | la mise en page **mesure** désormais |
| « Cavalier de Bâtons » sur trois lignes | 45 px de libellé par rangée, qui rabattaient la lame à son plancher | une ligne, nom entier gardé en infobulle |
| les lames dessinées restées violettes | mesuré au pixel : teinte **252°** sur un fond d'encre à **212°** | 22 valeurs pivotées, clarté conservée |

**La leçon, et c'est la deuxième fois** : les réserves de 78 et 38 px sont des *estimations* de
la place que prennent les libellés. Elles ont menti deux fois dans la même journée. Le code ne
les croit plus : après le calcul, il lit le bas réel de la table et redescend tant que ça
dépasse. Et comme les libellés ne sont écrits qu'**après** la pose, lame par lame, l'ajustement
est refait une fois que tout est écrit — mesurer avant, c'était mesurer des étiquettes vides.

## Les mises en page, remesurées en ligne

| écran | tirage | lame | débordement vertical | horizontal |
|---|---|---|---|---|
| 1366 × 768 | une lame | 108 × 210 | **0** | **0** |
| 1366 × 768 | trois lames | 108 × 210 | **0** | **0** |
| 1366 × 768 | la croix | 63 × 123 | **0** | **0** |
| 375 × 812 | trois lames | 77 × 150 | **0** | **0** |
| 375 × 812 | la croix | 77 × 150 | 159 (défile, assumé) | **0** |

Sur téléphone, l'en-tête, les sept boutons et le champ de question prennent 397 px avant la
table : la croix dépasse quoi qu'on fasse. Puisqu'on défile, le plancher monte à 150 px sous
620 px de large — des lames lisibles valent mieux que des lames qui rentrent.

## Les gardes des images

| garde | résultat | falsifiée ? |
|---|---|---|
| les 78 lames ont leur fichier | **78 / 78** chargées en 0,34 s, toutes en 280 × 549 | oui : une lame inventée (`zz99`) rend `null` et atterrit dans `PHOTO.manquants` |
| aucun doublon d'empreinte | **79 empreintes distinctes** sur 79 fichiers | un doublon signalerait une erreur de table |
| aucune lame vide | le repli remplit le `<img>` avec le dessin, même fichier absent | oui, vérifié sur `zz99` |
| l'outil reproduit le livré | `outils/cartes_bnf.py` relancé : **79 / 79 identiques à l'octet près** | — |
| bascule des deux jeux | photo → dessin → photo, sans retirer, sens conservé | — |

## La sonde d'ablation, relancée après le repalettage

- témoin (fond comparé à lui-même) : **0,00 %** — elle sait toujours échouer
- les 22 lames : de **10,4 %** (Tempérance) à **33,7 %** (Le Jugement)
- aucune lame sous 5 %, `ART.inconnus` **vide**

## Un piège d'outillage, à ne pas refaire

Ma boucle d'attente de GitHub Pages lisait le **dernier** build sans vérifier qu'il portait le
commit qu'on venait de pousser. Elle répondait « built » instantanément, sur le build
*précédent* — et j'ai mesuré des couleurs sur une page périmée avant de m'en apercevoir.
Il faut comparer `.[0].commit` à `git rev-parse HEAD`.

---

# Addendum — 26/09/2026, tout rentre dans la page

Les images venaient du même site que la page — rien ne fuitait nulle part — mais elles y
allaient quand même, lame par lame. Rem préfère **un fichier lourd et un chargement**. C'était
aussi le principe du projet avant les images ; il est rétabli.

## Mesuré en ligne, depuis la page elle-même

| | |
|---|---|
| ressources demandées après le document | **0** |
| requêtes déclenchées par un tirage | **0** |
| requêtes déclenchées par un changement de jeu | **0** |
| octets sur le fil | **2 105 078** (2,01 Mio) |
| octets décodés | 2 882 467 — compression **27 %** |
| DOM prêt | **375 ms** |

**Garde falsifiée** : une requête volontaire (`cartes/d13.webp?sonde=…`) fait bien passer le
compteur de 0 à 1. La sonde sait voir une requête ; elle n'en voit aucune parce qu'il n'y en a
aucune.

La barre de chargement ne fait pas semblant : l'écran est déclaré **avant** les données, et
chacune des dix tranches est suivie d'un appel qui la fait avancer à mesure que les octets
arrivent. Elle ne s'efface qu'au tout dernier script, quand la table est complète et les lames
posées — un écran qui part trop tôt ment sur ce qu'il annonce.

## Le défaut le plus grave de la journée : un outil qui a effacé la page

`outils/embarquer.py` remplace ce qu'il y a entre deux marqueurs. Son marqueur de début était
`" -->"` — qui tombe sur le **commentaire d'en-tête du fichier**, tout en haut. Il a donc effacé
tout ce qu'il y avait entre l'en-tête et la fin du bloc de données : le style, le corps, le
tirage. Et il a annoncé « LA PAGE SE SUFFIT À ELLE-MÊME », parce que ses gardes ne comptaient
que les images embarquées et l'absence de renvois à des fichiers locaux — deux choses encore
vraies dans une page détruite.

Rattrapé par `git checkout`. Ce qui a changé :

- `entre()` **exige l'unicité** de chaque marqueur et refuse de couper sinon ;
- les marqueurs sont devenus courts et uniques (`<!-- ##LAMES-DEBUT## -->`), le commentaire
  explicatif est sur sa propre ligne ;
- l'outil refuse d'écrire une page qui perdrait une de ses **onze ancres de structure**
  (`<style>`, `<body>`, `id="table"`, `<footer>`, `function peindre`…) ou qui **rétrécirait** ;
- les gardes se relisent sur le fichier **écrit**, pas sur la variable en mémoire.

*Une garde qui ne peut constater que ce qu'elle cherche ne garde rien. Celles-ci comptaient les
images dans une page qui n'avait plus de corps.*

## Ce que le code y gagne

`PHOTO` lit une table en mémoire au lieu d'aller chercher des fichiers : plus d'asynchrone,
plus de promesses, et la garde anti-course disparaît **avec la course qu'elle gardait** (le
`dataset.lame` qui empêchait une photo en retard d'écraser la lame du tirage suivant n'a plus
de retard à rattraper). Le dessin au code reste le second jeu et le filet.

Images redescendues à **260 px / q76** (1,84 Mo au lieu de 2,27) : puisqu'on paie tout
d'avance, autant payer moins, et 260 px couvre encore le pire cas — 108 px CSS × 2, ou
77 × 3 sur un téléphone dense.
