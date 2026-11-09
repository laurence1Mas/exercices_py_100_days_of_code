# Boutique en ligne avec Flask

Application eCommerce en cours de développement avec Flask, SQLite,
Flask-SQLAlchemy, Flask-Login, Flask-WTF et Bootstrap.

## Fonctionnalités actuelles

- Initialisation de l'application avec une factory Flask (`create_app`).
- Création des tables SQLite pour les utilisateurs, catégories, produits,
  paniers et commandes.
- Page d'accueil publique accessible à `/`.
- Catalogue produits avec recherche, filtre par catégorie et fiches produit.
- Inscription avec validation des champs et vérification de l'unicité de
  l'adresse e-mail (sans tenir compte de la casse).
- Hachage des mots de passe avec Werkzeug.
- Connexion, déconnexion protégée par CSRF et page de profil protégée.
- Rôle `CUSTOMER` attribué par défaut aux nouveaux comptes.

Les modèles du panier et des commandes sont définis, mais ces fonctionnalités
ne sont pas encore implémentées.

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

## Structure du projet

```text
online_shop/
├── app/
│   ├── admin/                 # Espace d'administration à développer
│   ├── auth/                  # Formulaires et routes d'authentification
│   ├── cart/                  # Panier à développer
│   ├── orders/                # Commandes et paiement à développer
│   ├── shop/                  # Catalogue à développer
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
2. Implémenter le panier avec contrôle de stock.
3. Ajouter le checkout, la simulation de paiement et la création de commandes.
4. Créer le suivi des commandes, le tableau de bord et les tests.

Le serveur lancé par `python run.py` est un serveur de développement. Utilisez
un serveur WSGI adapté pour un déploiement en production.