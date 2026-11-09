# Boutique en ligne avec Flask

Application eCommerce en cours de développement avec Flask, SQLite,
Flask-SQLAlchemy, Flask-Login, Flask-WTF et Bootstrap.

## Fonctionnalités actuelles

- Initialisation de l'application avec une factory Flask (`create_app`).
- Création des tables SQLite pour les utilisateurs, catégories, produits,
  paniers et commandes.
- Page d'accueil publique accessible à `/`.
- Catalogue produits avec recherche, filtre par catégorie et fiches produit.
- Panier persistant par client : ajout depuis les fiches produit, modification
  des quantités et suppression avec vérification du stock.
- Historique des commandes et détail privé des commandes du client connecté.
- Espace administrateur réservé au rôle `ADMIN`, avec des pages distinctes pour
  l'aperçu, les produits, les commandes, le stock et les statistiques.
- Inscription avec validation des champs et vérification de l'unicité de
  l'adresse e-mail (sans tenir compte de la casse).
- Hachage des mots de passe avec Werkzeug.
- Connexion, déconnexion protégée par CSRF et page de profil protégée.
- Rôle `CUSTOMER` attribué par défaut aux nouveaux comptes.

Le checkout et le paiement ne sont pas encore implémentés ; le bouton de
finalisation du panier reste donc désactivé. Les commandes visibles dans
l'historique doivent être créées en base par une étape ultérieure ou par du code
de test.

### Créer le compte administrateur initial

Depuis le dossier `online_shop`, lancez le seed interactif :

```powershell
python seed_admin.py
```

Le script demande l’adresse e-mail, puis le mot de passe deux fois sans afficher
les saisies. Le mot de passe doit contenir au moins 12 caractères et il est
enregistré sous forme hachée. Connectez-vous ensuite à `/auth/login`. Le rôle
`ADMIN` n'est jamais attribué par l'inscription publique. Si l’adresse existe
déjà pour un client, le seed s’arrête sans modifier ce compte.

## Prérequis et lancement

Depuis le dossier `online_shop`, activez l'environnement virtuel du projet,
installez les dépendances définies dans `requirements.txt` à la racine du dépôt,
puis démarrez le serveur :

```powershell
..\.venv\Scripts\Activate.ps1
python -m pip install -r ..\requirements.txt
python run.py
```

Ouvrez ensuite <http://127.0.0.1:5000/>. La base `ecommerce.db` est créée dans
`online_shop` au premier démarrage.

La configuration lit la clé secrète depuis la variable d'environnement
`SECRET_KEY`. Une valeur de développement est prévue pour faciliter le démarrage ;
définissez une clé privée dans l'environnement avant tout déploiement.

## Algorithme actuel

### Démarrage de l'application

1. `run.py` appelle `create_app()` dans `app/__init__.py`.
2. La factory charge `Config`, puis initialise SQLAlchemy, Flask-Login et la
   protection CSRF.
3. Les modèles sont importés pour que SQLAlchemy les connaisse. Le gestionnaire
   de connexion récupère l'utilisateur courant à partir de son identifiant.
4. `db.create_all()` crée les tables manquantes dans la base SQLite.
5. Le blueprint d'authentification est enregistré. Les routes de l'accueil et
   de la boutique sont alors disponibles.

### Inscription

1. Le formulaire vérifie le nom, l'adresse e-mail, la longueur minimale du mot
   de passe et la confirmation de celui-ci.
2. L'adresse e-mail est retirée des espaces superflus et convertie en
   minuscules.
3. L'application cherche une adresse identique sans tenir compte de la casse ;
   si elle existe, l'inscription est refusée avec un message.
4. Sinon, le mot de passe est haché, un compte `CUSTOMER` est enregistré, puis
   l'utilisateur est connecté et redirigé vers son profil.

### Connexion et déconnexion

1. À la connexion, l'application normalise l'adresse e-mail et recherche le
   compte correspondant sans tenir compte de la casse.
2. Werkzeug compare le mot de passe fourni avec le hachage enregistré. En cas
   d'échec, un message générique est affiché ; sinon, Flask-Login ouvre la
   session utilisateur.
3. La page de profil exige une session authentifiée. La déconnexion se fait par
   une requête POST protégée par CSRF et ferme cette session.

### Espace administrateur

1. `python seed_admin.py` crée le compte administrateur initial dans la base
   configurée, après saisie interactive de l’adresse et du mot de passe.
2. Toutes les routes `/admin/` exigent une connexion et le rôle exact `ADMIN` ;
   un client connecté reçoit une réponse 403.
3. La barre latérale mène aux pages `/admin/` (aperçu), `/admin/products`,
   `/admin/orders`, `/admin/stock` et `/admin/statistics`. La page active est
   indiquée dans la navigation.
4. L'aperçu affiche les indicateurs principaux et les cinq dernières commandes.
   Les pages Produits, Commandes et Stock présentent leurs listes respectives ;
   la page Statistiques détaille les indicateurs de ventes et d'activité.

### Historique et détail des commandes

1. `/orders/` exige une session utilisateur et ne charge que les commandes
   associées à cet utilisateur, de la plus récente à la plus ancienne.
2. Chaque ligne affiche la date, le nombre d'articles, le total ainsi que les
   statuts de commande et de paiement.
3. `/orders/<id>` vérifie à la fois l'identifiant de la commande et celui du
   client connecté. Une commande inexistante ou appartenant à un autre client
   renvoie une réponse 404.
4. Le détail reprend les quantités et prix unitaires enregistrés dans les
   lignes de commande. Les commandes apparaîtront automatiquement lorsque le
   checkout sera implémenté.

### Panier

1. `/cart/` exige une connexion et ne charge que les articles du client courant.
2. Depuis une fiche produit en stock, le client ajoute une quantité ; le serveur
   vérifie la disponibilité avant de créer ou mettre à jour la ligne du panier.
3. Le client peut modifier la quantité ou retirer un article. Chaque action
   vérifie que la ligne lui appartient et que le stock permet cette quantité.
4. Le sous-total et le total provisoire sont recalculés à partir des prix
   actuels du catalogue. Le checkout reste désactivé jusqu'à son implémentation.

## Structure du projet

```text
online_shop/
├── app/
│   ├── admin/                 # Tableau de bord administrateur
│   ├── auth/                  # Formulaires et routes d'authentification
│   ├── cart/                  # Routes d'ajout et de gestion du panier
│   ├── orders/                # Historique et détail des commandes
│   ├── shop/                  # Routes du catalogue à développer
│   ├── static/                # CSS, JavaScript et images
│   ├── templates/             # Pages Jinja2
│   ├── extensions.py          # Extensions Flask partagées
│   ├── models.py              # Modèles SQLAlchemy
│   └── __init__.py            # Factory de l'application
├── config.py                  # Configuration Flask et SQLite
├── run.py                     # Point d'entrée du serveur de développement
└── ecommerce.db               # Base locale créée au démarrage
```

## Prochaines étapes

1. Ajouter la gestion administrateur des produits et catégories.
2. Implémenter le checkout, la simulation de paiement et la création de commandes.
3. Compléter le suivi administrateur des commandes et les tests.

Le serveur lancé par `python run.py` est un serveur de développement. Utilisez
un serveur WSGI adapté pour un déploiement en production.