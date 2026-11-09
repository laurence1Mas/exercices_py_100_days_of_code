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
- Gestion CRUD des catégories dans l'espace administrateur. Une catégorie
  contenant des produits ne peut pas être supprimée.
- Gestion CRUD des produits depuis la page `/admin/products`, avec formulaires
  dans des modales Bootstrap. Un produit référencé par un panier ou une commande
  ne peut pas être supprimé. Les administrateurs peuvent importer des images
  JPG, PNG ou WEBP jusqu'à 5 Mo ; elles sont vérifiées puis enregistrées dans
  `app/static/uploads/products` sous un nom généré par l'application.
- Formulaire de contact avec validation et enregistrement des messages en base ;
  les administrateurs les consultent depuis `/admin/messages`.
- Inscription avec validation des champs et vérification de l'unicité de
  l'adresse e-mail (sans tenir compte de la casse).
- Hachage des mots de passe avec Werkzeug.
- Connexion, déconnexion protégée par CSRF et page de profil protégée.
- Rôle `CUSTOMER` attribué par défaut aux nouveaux comptes.
- Icônes de l'interface fournies par Font Awesome 6 via CDN dans les layouts
  client et administrateur.

Le checkout comprend une étape de récapitulatif et une confirmation de paiement
simulé. Aucune donnée bancaire n'est collectée ; les commandes payées sont
enregistrées et le stock est mis à jour en base.

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

## Base de données SQLite en local

### Emplacement et démarrage

La configuration de `online_shop/config.py` construit le chemin de la base à
partir du dossier du projet. En local, le fichier utilisé est donc
`online_shop/ecommerce.db` ; il ne s'agit pas d'une base distante. SQLite stocke
les données dans ce fichier et Python inclut le module `sqlite3` pour le lire.

Au démarrage, `run.py` appelle `create_app()`. La factory initialise
Flask-SQLAlchemy puis exécute `db.create_all()` dans un contexte Flask. Cette
instruction crée les tables qui n'existent pas encore sans supprimer les
données déjà enregistrées. Elle ne remplace pas un système de migrations :
après une modification de colonnes ou de contraintes d'une table existante,
il faut prévoir une migration adaptée.

### Tables et relations

Les modèles de `app/models.py` décrivent les tables principales :

| Table | Données enregistrées |
|---|---|
| `users` | Comptes, adresse e-mail unique, rôle et mot de passe haché |
| `categories` | Catégories du catalogue |
| `products` | Produits, prix, stock et catégorie |
| `cart_items` | Produits et quantités du panier de chaque client |
| `orders` | Commandes, total et statuts de commande et de paiement |
| `order_items` | Articles et prix unitaire mémorisé au moment de la commande |
| `contact_messages` | Nom, e-mail, sujet, message et date des messages de contact |

Les colonnes `user_id`, `product_id`, `category_id` et `order_id` relient les
enregistrements entre eux. Par exemple, un client possède des lignes de panier
et des commandes ; une catégorie regroupe ses produits ; une commande possède
ses lignes d'articles. L'ORM SQLAlchemy traduit les opérations de l'application
en requêtes SQLite et représente ces liens par des relations Python.

### Enregistrement des changements

Les routes ajoutent ou modifient les données au moyen de SQLAlchemy. Les
changements sont validés avec `db.session.commit()` ; en cas d'erreur lors d'une
transaction, `db.session.rollback()` permet de l'annuler. Les formulaires du
site et les vérifications de rôle restent le moyen normal d'accéder aux
données. Les mots de passe ne sont pas enregistrés en clair.

### Consulter la base localement

Depuis le dossier `online_shop`, ouvrez une console Python :

```powershell
python
```

Puis listez les tables en lecture seule avec le module standard `sqlite3` :

```python
import sqlite3

connection = sqlite3.connect("file:ecommerce.db?mode=ro", uri=True)
tables = connection.execute(
    "SELECT name FROM sqlite_master "
    "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
).fetchall()
print(tables)
connection.close()
```

On peut aussi ouvrir `ecommerce.db` avec une application compatible SQLite,
comme DB Browser for SQLite. Faites une copie du fichier avant toute
intervention manuelle et évitez de modifier les tables directement pendant que
l'application tourne : utilisez l'application ou un script SQLAlchemy pour
préserver les relations et les règles de validation.

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
   `/admin/categories`, `/admin/orders`, `/admin/stock` et `/admin/statistics`.
   La page active est indiquée dans la navigation.
4. L'aperçu affiche les indicateurs principaux et les cinq dernières commandes.
   Les pages Produits, Commandes et Stock présentent leurs listes respectives ;
   la page Statistiques détaille les indicateurs de ventes et d'activité.
5. La page `/admin/categories` permet de créer, lister, modifier et supprimer
   les catégories. Les noms sont uniques sans tenir compte de la casse ; la
   suppression est bloquée tant que la catégorie contient des produits.
6. La page `/admin/products` permet d'ajouter et de modifier les produits dans
   des modales Bootstrap, et de confirmer leur suppression dans une modale.
   Les formulaires valident le nom, le prix, le stock et la catégorie côté
   serveur. Un produit utilisé dans un panier ou une commande ne peut pas être
   supprimé.

### Formulaire de contact

1. `/contact` affiche un formulaire avec le nom, l'adresse e-mail, le sujet et
   le message. Les visiteurs connectés voient leur nom et leur e-mail préremplis.
2. Flask-WTF protège la soumission par CSRF et valide les champs côté serveur.
   Un message valide est enregistré dans la table `contact_messages`, puis
   l'utilisateur est redirigé vers le formulaire avec une confirmation.
3. La page `/admin/messages`, réservée au rôle `ADMIN`, présente les 100 messages
   les plus récents. Aucun e-mail n'est envoyé automatiquement.

### Historique et détail des commandes

1. `/orders/` exige une session utilisateur et ne charge que les commandes
   associées à cet utilisateur, de la plus récente à la plus ancienne.
2. Chaque ligne affiche la date, le nombre d'articles, le total ainsi que les
   statuts de commande et de paiement.
3. `/orders/<id>` vérifie à la fois l'identifiant de la commande et celui du
   client connecté. Une commande inexistante ou appartenant à un autre client
   renvoie une réponse 404.
4. Le détail reprend les quantités et prix unitaires enregistrés dans les
   lignes de commande ainsi que l'état du paiement simulé.

### Panier

1. `/cart/` exige une connexion et ne charge que les articles du client courant.
2. Depuis une fiche produit en stock, le client ajoute une quantité ; le serveur
   vérifie la disponibilité avant de créer ou mettre à jour la ligne du panier.
3. Le client peut modifier la quantité ou retirer un article. Chaque action
   vérifie que la ligne lui appartient et que le stock permet cette quantité.
4. Le sous-total et le total provisoire sont recalculés à partir des prix
   actuels du catalogue. Le bouton de commande est désactivé si une quantité
   dépasse le stock disponible.

### Checkout et paiement simulé

1. `/cart/checkout` affiche le récapitulatif et recalcule le total côté serveur ;
   les prix et les quantités envoyés par le navigateur ne sont pas utilisés.
2. À la confirmation, le serveur revérifie le stock et le décrémente dans la
   même transaction SQLite que la création de la commande et de ses lignes.
   Si un article n'est plus disponible, aucune commande n'est créée et le
   panier est conservé.
3. Le paiement est volontairement simulé : aucun numéro de carte ni donnée
   bancaire n'est demandé ou enregistré. La confirmation crée une commande
   `PROCESSING` avec un paiement `PAID`, vide le panier et affiche le détail.
4. Depuis `/admin/orders`, un administrateur ouvre le détail d'une commande et
   peut la faire passer de « En préparation » à « Expédiée », puis « Livrée ».
   Une commande encore en préparation peut être annulée ; cette action simule
   le remboursement et remet les quantités en stock. Les transitions sont
   vérifiées côté serveur.

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

1. Compléter les tests automatisés des parcours client et administrateur.
2. Préparer le déploiement avec une configuration et un serveur WSGI adaptés.

Le serveur lancé par `python run.py` est un serveur de développement. Utilisez
un serveur WSGI adapté pour un déploiement en production.