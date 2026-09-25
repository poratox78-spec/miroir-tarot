# MIROIR — tirage de tarot

Un tirage de tarot en **un seul fichier**. Aucune image, aucune dépendance, aucun build :
on ouvre `index.html` dans un navigateur, ça marche.

> Un tirage ne prédit rien. Les lames servent de miroir : ce qu'on y lit vient de soi.
> C'est écrit en haut de la page, et c'est la ligne de conduite du projet — on ne promet
> jamais une prédiction.

## Ce qui tourne aujourd'hui

- **22 arcanes majeurs**, dessinés au code (canvas 2D), dans l'esprit de `viv_cards_art.js` de VIVARIUM.
- **3 tirages** : une lame · trois lames (ce qui a mené là / là où tu en es / la pente) · la croix (5).
- **Mélange honnête** : Fisher-Yates sur `crypto.getRandomValues`, orientation tirée à 50/50.
  Rien n'est truqué, rien n'est influencé par la question posée.

## Le vrai sujet : la lecture est COMPOSÉE

C'est le seul point qui distingue ce projet des mille autres applis de tarot.

Il n'y a **aucun paragraphe pré-écrit par carte**. Chaque bloc s'assemble à partir de
`lame × orientation × position dans le tirage`, puis quatre règles relisent le **voisinage** :

| règle | ce qu'elle regarde |
|---|---|
| dominante d'élément | 2 lames ou plus du même élément |
| tension d'axes | deux axes qui se contredisent (ordre ↔ rupture, élan ↔ intérieur…) |
| part de renversées | aucune / une partie / toutes |
| sens de la progression | les numéros montent ou descendent |

Conséquence : les mêmes cartes à des places différentes ne donnent pas le même texte.

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

- **Les 56 arcanes mineurs** (4 couleurs × 14) et leurs appuis. C'est le gros du travail.
- Repasser les lames qui restent approximatives : les pattes des chevaux du Chariot, le corps
  du lion de la Force, les cornes du Diable (peu visibles sous la coiffe).
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
