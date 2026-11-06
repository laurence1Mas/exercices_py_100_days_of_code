# Breakout Game

Un jeu de casse-briques écrit en Python avec le module graphique intégré `turtle`.

## Lancer le jeu

Depuis la racine du projet, lancez :

```powershell
.\.venv\Scripts\python.exe .\breakout_game\main.py
```

Le jeu ouvre une fenêtre de 800 × 600 pixels.

## Commandes

- **Flèche gauche** : déplacer la raquette vers la gauche.
- **Flèche droite** : déplacer la raquette vers la droite.
- **Fermer la fenêtre** : quitter le jeu.

## Règles

1. La balle se déplace automatiquement et rebondit sur les murs latéraux et le haut de la fenêtre.
2. La raquette est contrôlée au clavier. Si la balle la touche en descendant, elle repart vers le haut.
3. Quand la balle touche une brique, celle-ci disparaît et le score augmente de **10 points**.
4. Si la balle passe sous la raquette, la partie s’arrête et le jeu affiche **GAME OVER** avec le score final.

## Comment fonctionne le code

`main.py` assemble les éléments du jeu et coordonne la partie :

- Il crée la fenêtre et les objets (`Paddle`, `Ball`, `Brick` et `Scoreboard`).
- Il crée cinq rangées de briques, avec une couleur différente par rangée.
- Il relie les touches fléchées aux déplacements de la raquette.
- La fonction `game_loop()` met à jour l’écran, déplace la balle, vérifie les collisions et programme le tour suivant environ 100 ms plus tard. Cette mise à jour par minuterie laisse la fenêtre traiter les événements clavier et fermeture.
- `check_brick_collisions()` compare la position de la balle à celle des briques. À l’impact, elle masque et retire la brique, ajoute les points, puis inverse le mouvement de la balle sur l’axe du rebond.
- `check_paddle_collision()` vérifie que la balle croise le dessus de la raquette en descendant et qu’elle se trouve dans sa largeur. Elle replace alors la balle au-dessus de la raquette et la fait repartir vers le haut.
- Si la balle passe sous la raquette, `game_loop()` arrête les mises à jour et demande au tableau des scores d’afficher le résultat final.

## Organisation des fichiers

| Fichier | Rôle |
|---|---|
| `main.py` | Fenêtre, briques, contrôles, boucle du jeu et collisions. |
| `ball.py` | Apparence, déplacement et rebonds de la balle. |
| `paddle.py` | Apparence et déplacements de la raquette. |
| `brick.py` | Apparence et position des briques. |
| `scoreboard.py` | Affichage et mise à jour du score et du message de fin. |

## Améliorations possibles

Le jeu n’affiche pas encore de message de victoire lorsque toutes les briques sont détruites, et la raquette n’est pas limitée aux bords de la fenêtre.