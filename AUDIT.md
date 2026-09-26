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
