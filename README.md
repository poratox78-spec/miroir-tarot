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

**Chaque lame porte trois formulations par sens** (endroit et renversé) : 132 appuis pour les
majeurs, 84 pour les rangs mineurs. Avant, les mineurs n'en avaient **qu'une seule** — le texte
d'un mineur était entièrement déterministe, la même carte à la même place redonnait mot pour mot
la même phrase.

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

## Le « G2P du tarot » : la question donne le registre

Une table **mot → thème**, déterministe et vérifiable, dans l'esprit d'un G2P : 9 thèmes,
287 graines élargies à 1 593 formes, et 36 registres écrits (thème × élément).

**Ce qu'elle ne fait pas : elle ne change RIEN au tirage.** Les lames sont mélangées au hasard,
avant, et sans jamais voir la question. Faire autrement serait truquer le tirage.
**Ce qu'elle fait : elle change la langue de la lecture.** Un même élément ne dit pas la même
chose selon la question — l'eau parle de l'ambiance sur une question de travail, et de ce qui est
ressenti sans être dit sur une question d'amour.

Deux décisions de modèle, prises parce que le banc les a exigées :

- **« choix » et « soi » sont des FORMES de question, pas des domaines.** Un choix est toujours un
  choix *à propos de quelque chose* : ils ne l'emportent que si rien de concret n'est reconnu.
  Sans cette règle, « dois-je quitter mon travail » était rangé en « choix ».
- **Le pluriel s'essaie, il ne se coupe pas.** Couper le `s` d'avance cassait « sous » en « sou » ;
  le garder ratait « jobs ». On teste le mot tel quel, puis son singulier.

Les mots sont stockés **sans accent** et la question est normalisée pareil : quelqu'un qui écrit
vite, ou qui est dys, ne tape pas « santé » mais « sante ».

### La question entre dans chaque bloc

Le registre ne produisait qu'**une ligne**, tout à la fin. Désormais la **relance en italique** —
la question qu'on te retourne sous chaque lame — est choisie selon le **thème de ta question** ×
l'**axe de la lame** (élan, ordre, rupture, lien, passage, épreuve, intérieur, lumière).

9 thèmes × 8 axes = **72 relances**, qui couvrent les 78 lames sans avoir à en écrire 702.

| question | relance sur Le Pendu |
|---|---|
| amour | *Qu'est-ce que cette relation te demande de laisser derrière ?* |
| travail | *Qu'est-ce que tu gagnes à passer, et qu'est-ce que tu perds ?* |
| argent | *Ce que ça coûte, tu l'as compté, ou estimé ?* |
| sans thème | *Qu'est-ce que tu fais de ça aujourd'hui ?* |

Couverture vérifiée : **72/72**, et **0 repli silencieux** sur les 702 paires lame × thème — une
lame dont l'axe aurait manqué serait retombée sans bruit sur la relance générique.

### L'argot vient de la base d'OMEGA

Le thème **jeu** est nourri par les 24 mots de gaming de `dictee/argot_curated.tsv` d'OMEGA — la
liste curée à la main, qui a déjà passé sa garde « zéro vulgarité, zéro insulte, zéro
discrimination ». Réutiliser cette liste plutôt qu'en réinventer une évite d'avoir à refaire ce
tri.

Cinq mots d'argot courant ont été ajoutés aux thèmes existants, après **vérification du sens** :
`moula`, `khalass`, `hess` (argent), `poto` (amitié), `seum` (moral). Plus `jtm` et `bg`, qui sont
transparents.

⚠️ **Sept mots de la base n'ont PAS été versés** faute de sens vérifiable : `mif`, `khey`, `kho`,
`igo`, `patnè`, `hami`, `gow`. Ils sont probablement utiles (famille, amitié, amour) mais une
table qui devine fabrique des contresens — ils attendent une confirmation.

### La morphologie vient aussi d'OMEGA

Les graines sont écrites à la main en forme de citation (« travail », « fatigue », « choisir »).
Mais quelqu'un écrit « je travaille », « je suis fatiguée », « j'ai choisi ». `outils/elargir_lexique.py`
engendre les formes fléchies depuis `data_local/Lexique4.tsv` d'OMEGA : **287 graines → 1 593 formes**,
pour 14 Ko. Rien n'est chargé à l'exécution — la page reste autonome.

Deux gardes, mesurées et non devinées :

- **Le lemme de citation d'abord.** Lexique rattache « couple » au verbe *coupler* : sans garde,
  le thème amour recevait « couplera », « couplant », « couplée ».
- **Les mots-outils dehors, et surtout PAS de seuil de fréquence.** La graine « dois » tirait tout
  le paradigme de *devoir*, dont **« du »** (fréquence 4124) — qui aurait déclenché « choix » sur
  presque toute question. Et un seuil ne peut pas trancher : « moi », graine voulue, culmine à
  **5018**, au-dessus de « du ». Ce qui les sépare n'est pas la fréquence mais la **nature** :
  « du » est un article. On écarte donc toute forme ayant une lecture article, préposition,
  conjonction, pronom ou auxiliaire — et les modaux ne s'élargissent pas du tout.

4 collisions entre thèmes, toutes légitimes : *copain* est amitié **et** amour, *partie* est choix
**et** jeu.

### ⛔ Rattrapage d'orthographe par distance d'édition — RÉFUTÉ, retiré

Un scripteur dys écrit « travaile », « fatigua », « trveail ». Mesuré avec le générateur de fautes
dys d'OMEGA (`dictee/dys_gen.py`, calibré sur les 6 dictées appariées de l'ASEI) : la
reconnaissance tombe de **94,1 % sur l'original à 84,3 % sur le fautif**. Dix points, un vrai
problème.

Tentative : rattraper tout mot inconnu à **une opération** d'un mot de l'index (lettre en moins,
lettre changée, deux lettres inversées), borné à 6 lettres et abandonné en cas d'égalité.

| | |
|---|---|
| gain | 84,3 % → **86,3 %** (+2 points) |
| coût sur 3 000 phrases de français **correct** | **1 375 mots faussement rattachés**, contre 3 891 reconnus légitimement |

*chance → change*, *achève → achète*, *ressent → restent*. Ce sont des **mots justes réécrits** —
exactement le défaut qu'on reproche ailleurs. Deux points de gain pour 35 % de contamination :
retiré.

**Ce qui manquerait pour y arriver** : savoir si un mot est du français correct avant d'essayer de
le corriger. OMEGA a exactement ça (706 000 formes), mais l'embarquer briserait l'autonomie de la
page. Une piste tiendrait : un filtre compact des ~20 000 formes les plus fréquentes, ~25 Ko.
À ne tenter que si le gain mesuré le justifie — il ne le justifiait pas ici.

Banc : **45 questions réalistes, 45 justes**, et le témoin (des mots inventés) ne reconnaît rien —
la table ne devine pas, elle reconnaît ou se tait.

## Le mode charriage

Tape **un pseudo seul** dans la barre de question (un mot, sans espace) et la lecture devient un
charriage adressé à cette personne — pour la scène, le stream, la table.

**La règle de fabrication, et elle n'est pas négociable : la vanne vient TOUJOURS de la carte,
jamais de la personne.** La page ne sait rien de qui que ce soit — ni visage, ni âge, ni origine —
et c'est précisément ce qui rend le charriage tenable. On se moque de la situation que la lame
décrit ; le pseudo n'est que le destinataire. Une ligne le rappelle en bas de chaque lecture.

Les 22 majeurs ont leurs vannes propres ; les 56 mineurs se composent comme le reste, rang ×
couleur (« repart de zéro sur ses projets », « règne sur ses sentiments, le royaume compte deux
habitants »).

**Trois vannes par lame, six chutes pour les renversées** : 66 pour les majeurs, 42 pour les rangs
(× 4 couleurs), soit **1 638 combinaisons**. La première version n'en avait que 36 — une soirée de
stream en faisait le tour. Mesuré sur 4 000 tirages simulés : 1 247 formulations distinctes
rencontrées, aucun gabarit non remplacé.

**Deux tons, au choix du scripteur** : *doux* (ironie tranquille, pour une table entre amis) et
*piquant* (plus mordant, pour la scène). 108 vannes en doux, 72 en piquant — 1 517 et 1 051
formulations distinctes mesurées sur 8 000 tirages simulés, aucun gabarit non remplacé.

Le ton change la formulation, **jamais la règle** : même en piquant, la vanne porte sur la
situation que décrit la lame, pas sur la personne. C'est le choix qui revient à celui qui connaît
son public, pas au programme.

Le panneau du chat est **en bas de page**, replié, et la barre de question ne fait plus de
publicité au charriage : c'est un à-côté, pas le sujet.

## Le chat Twitch

Le panneau « Chat Twitch » se branche sur une chaîne et liste les pseudos qui parlent ; un clic
sur un pseudo tire pour lui, et « Charrier au hasard » en pioche un.

**Aucun identifiant n'est demandé.** Twitch autorise la lecture d'un chat public en anonyme
(pseudo `justinfan…`, sans mot de passe ni jeton, sur `wss://irc-ws.chat.twitch.tv`). C'est un
choix, pas une limite subie : il n'y a rien à autoriser, rien à stocker, rien qui puisse fuiter.
La page **ne peut pas écrire** dans le chat, et n'affiche **que les pseudos** — ce que les gens
écrivent ne ressort jamais ici.

Même découpage que `chat_twitch.py` du Déformateur :

- **la logique** — lire une ligne IRC, en tirer un pseudo et un rang. Aucune socket, donc
  vérifiable au banc : 8 cas (modérateur, abonné, anonyme, diffuseur, accueil, PING, JOIN, ligne
  vide), le filtre de rang, et une trame CRLF réelle découpée en trois. 0 échec.
- **le fil** — la connexion, le PING/PONG, la fermeture. Il ne décide de rien.

Garde-fous : filtre de rang (tout le monde / abonnés et VIP / modérateurs), liste plafonnée à 40
pseudos, et un bouton qui débranche tout.

**Vérifié sur le site publié** : la connexion aboutit (« connecté à #wedel_mathy »), le
dédoublonnage tient (« Zoe » puis « zoe » ne font qu'une entrée), le plafond s'arrête à 40, et un
clic sur un pseudo déclenche bien le tirage charrié.

⚠️ **Un maillon n'a pas pu être observé avec de vraies données** : l'arrivée d'un message, parce
que la chaîne était calme au moment du test. Les deux moitiés sont prouvées séparément — la socket
se connecte en vrai, et l'analyseur avale des trames IRC réelles au banc — mais leur jonction ne
se vérifie qu'en direct. Pour la confirmer en dix secondes pendant un live : ouvrir le panneau,
se brancher, et regarder si les pseudos apparaissent quand quelqu'un écrit.

⚠️ Écrire l'IRC sans barre oblique (contrainte du heredoc) m'a fait produire un séparateur de
lignes `/r?n/` — qui découpe sur la lettre **n**. Les lignes auraient été déchiquetées. Le banc
sur une trame réelle l'a attrapé.

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
