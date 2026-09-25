# MIROIR — tirage de tarot

Un tirage de tarot en **un seul fichier**. Aucune image, aucune dépendance, aucun build :
on ouvre `index.html` dans un navigateur, ça marche.

> Un tirage ne prédit rien. Les lames servent de miroir : ce qu'on y lit vient de soi.
> C'est écrit en haut de la page, et c'est la ligne de conduite du projet — on ne promet
> jamais une prédiction.

## Ce qui tourne aujourd'hui

- **Les 78 lames** : 22 arcanes majeurs + 56 mineurs, toutes dessinées au code (canvas 2D),
  dans l'esprit de `viv_cards_art.js` de VIVARIUM. Un bouton bascule sur les 22 majeurs seuls.
- **3 tirages** : une lame · trois lames (ce qui a mené là / là où tu en es / la pente) · la croix (5).
- **Mélange honnête** : Fisher-Yates sur `crypto.getRandomValues`, orientation tirée à 50/50.
  Rien n'est truqué, rien n'est influencé par la question posée.

## Le vrai sujet : la lecture est COMPOSÉE

C'est le seul point qui distingue ce projet des mille autres applis de tarot.

Il n'y a **aucun paragraphe pré-écrit par carte**. Chaque bloc s'assemble à partir de
`lame × orientation × position dans le tirage`, puis quatre règles relisent le **voisinage** :

| règle | ce qu'elle regarde | portée |
|---|---|---|
| dominante d'élément | 2 lames ou plus du même élément | tout le jeu |
| tension d'axes | deux axes qui se contredisent (ordre ↔ rupture, élan ↔ intérieur…) | tout le jeu |
| part de renversées | aucune / une partie / toutes | tout le jeu |
| part de majeurs | le fond (majeurs) contre le quotidien (mineurs) | jeu complet |
| répétition de rang | le même rang dans plusieurs couleurs — « Le Sept sort trois fois » | mineurs |
| figures de cour | 2 figures ou plus : des attitudes, ou des personnes | mineurs |
| hauteur des rangs | rangs bas (commencements) ou hauts (fin de cycle) | mineurs |
| sens de la progression | les numéros montent ou descendent | majeurs seuls |

Deux précisions qui ont orienté le code :

- **Une règle « couleur dominante » serait redondante.** Bâtons = feu, Coupes = eau, Épées = air,
  Deniers = terre : chez les mineurs, la dominante d'élément *est* la dominante de couleur.
- **La progression des numéros est réservée aux majeurs.** Comparer un rang de mineur (1 à 14)
  à un numéro d'arcane (0 à 21) ne veut rien dire.

Conséquence : les mêmes cartes à des places différentes ne donnent pas le même texte.

## Les 56 mineurs sont ENGENDRÉS, pas écrits

Dans le Tarot de Marseille, les mineurs n'ont **aucune illustration narrative** : le lecteur
s'appuie sur la **couleur** (le domaine) et sur le **nombre** (le mode). Le sens se compose donc
de la même façon — 4 couleurs × 14 rangs = 56 lames, sans 56 textes recopiés.

| couleur | élément | domaine |
|---|---|---|
| Bâtons | feu | du travail, de ce qu'on entreprend |
| Coupes | eau | des liens, de ce qu'on ressent |
| Épées | air | des mots, des décisions et des conflits |
| Deniers | terre | de l'argent, du corps, de ce qui se compte |

Les rangs vont de l'As (l'énergie pure) au Dix (l'achèvement qui déborde), puis Valet, Cavalier,
Reine, Roi (début · mouvement · maîtrise du dedans · maîtrise du dehors).

**Le dessin suit la même logique.** Bâtons et Épées se **croisent** — et le rang impair ajoute
une pièce droite au centre, *derrière* les croisements ; Coupes et Deniers s'alignent en
**rangées de deux**. Une règle, 40 cartes. Les figures de cour sont des personnages qui portent
l'emblème de leur couleur.

⚠️ Deux pièges de langue, réglés parce que les noms sont **assemblés** :
- **l'élision** : « Cavalier **d'**Épées », jamais « de Épées » ;
- **l'article et son genre** : « **Le** Roi de Deniers », « **La** Reine d'Épées », « **L'**As de
  Bâton ». Les majeurs portent déjà leur article dans leur nom, les mineurs non.
Les 56 phrases engendrées sont contrôlées d'un coup : 0 faute.

## Le permalien

Un tirage tient dans l'URL : `#t=croix&j=78&c=M1.b5r.c9.e14.d2r` (tirage, jeu, puis les lames,
`r` pour renversée). L'adresse suit toujours ce qui est à l'écran, et un bouton la copie.

**Le lien rejoue les mêmes lames — ce n'est pas un nouveau tirage, et la page le dit.** Sans ce
bandeau, celui qui reçoit le lien croirait avoir tiré lui-même.

Deux pièges, tous deux invisibles sans un chargement vraiment à froid :

- **Coller un lien dans un onglet déjà ouvert ne recharge pas la page** — le navigateur ne change
  que le fragment. Sans écouteur `hashchange`, le lien ne fait rien *et on croit qu'il marche*,
  parce que le tirage précédent reste affiché. C'est exactement comme ça que je me suis trompé
  deux fois : une fois en croyant le bandeau cassé, une fois en croyant le rejeu réussi.
- **« Copié » ne s'annonce qu'APRÈS que la promesse a tenu.** Un `try/catch` synchrone autour
  d'une API à promesse n'attrape jamais le refus : le bouton mentirait. En cas de refus, le lien
  est affiché en clair, à copier à la main.

## La sonde d'ablation

`ART.lame(a, {recette, nocache})` permet de redessiner une lame avec une **autre recette et la
même graine**. On s'en sert pour prouver qu'une lame dessine vraiment quelque chose : on la
compare à **son propre fond seul** et on compte les pixels qui diffèrent.

- témoin « fond seul » : **0,00 %** — la sonde sait échouer
- les 22 lames : entre **9,1 %** et **38,3 %** de leur zone d'image

⚠️ **Une première sonde comptait les pixels clairs. Elle était fausse** : le témoin vide marquait
4414 et Le Pendu 3227 (une lame couverte de robes sombres passait pour vide). Elle aurait validé
une carte absente. Ne pas revenir à une mesure de clarté.

**Deuxième garde : les motifs fantômes.** La boucle de dessin sautait en silence un nom de motif
absent — la recette du Diable appelait `flamme`, qui n'a jamais existé. Les noms manquants sont
maintenant enregistrés dans `ART.inconnus`. Garde falsifiée : une recette bidon la fait passer
de 0 à 1 entrée, avec le nom fautif.

## Les cinq scènes redessinées

Le Chariot, La Roue, La Force, Le Diable et Le Jugement lisaient mal en motifs empilés. Ils sont
redessinés en **scènes complètes**, d'après l'iconographie du Tarot de Marseille :

| lame | ce que la scène doit montrer | ablation |
|---|---|---|
| VII Le Chariot | dais jaune pâle sur 4 colonnes (2 rouges, 2 bleues), prince couronné, 2 chevaux opposés | 29,1 % |
| X La Roue | sphinx bleu couronné à ailes rouges au sommet, chien jaune qui monte, singe qui descend, manivelle vide | 16,3 % |
| XI La Force | chapeau en lemniscate surmonté d'une couronne, mains à la gueule du lion jaune | 27,0 % |
| XV Le Diable | ailes de chauve-souris, torche, piédestal, deux petits liés par le cou | 23,3 % |
| XX Le Jugement | ange dans la nuée, trompette à bannière croisée, trois personnages dont un **de dos** | 37,0 % |

Sources d'iconographie : [Le Chariot (Wikipédia)](https://fr.wikipedia.org/wiki/Le_Chariot) ·
[La Roue de Fortune (Wikipédia)](https://fr.wikipedia.org/wiki/La_Roue_de_Fortune) ·
[symbolisme des lames, apprendre-tarotdemarseille.com](https://www.apprendre-tarotdemarseille.com/guide-interpr%C3%A9tation-gratuit-tarot-de-marseille/symbolisme/xi-la-force-symbolisme/)

## Ce qui reste à faire

- Repasser les lames qui restent approximatives : les pattes des chevaux du Chariot, le corps
  du lion de la Force, les cornes du Diable (peu visibles sous la coiffe).
- Les entrelacs floraux qui accompagnent les pips de Marseille ne sont pas dessinés : les
  emblèmes sont nus sur le fond.
- Les répétitions ne signalent que le rang le plus fréquent : un tirage qui porte à la fois
  deux Cinq et deux Rois n'en nomme qu'un.
- Le texte est **assemblé** : toute nouvelle tournure doit être vérifiée sur **toutes** les
  combinaisons, pas seulement celle qu'un tirage a donnée. Deux fautes d'article
  (« penche vers eau », « du côté l'émotion ») sont passées comme ça.

## Vérifier

Ouvrir `index.html`. Pour les sondes, il faut un vrai serveur (le `file://` ne suffit pas
pour lire les pixels d'un canvas) :

```bash
python -m http.server 8777
```

puis `http://127.0.0.1:8777/index.html`.

⚠️ Selon l'environnement, un proxy local peut **tronquer** la réponse vers 8 Ko — la page
s'affiche alors sans son `<script>`, et tout semble mort sans la moindre erreur en console.
Symptôme : `document.scripts.length === 0`. Vérifier avec
`curl -s http://127.0.0.1:8777/index.html | wc -c` contre la taille du fichier ; si ça coupe,
vérifier sur le site publié plutôt que sur le serveur local.
