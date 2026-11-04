# 🌐 Portfolio Personnel — Laurence Masika

> Un portfolio personnel , responsive et dynamique, développé avec Python et Flask.

## 📌 Présentation du projet

Ce projet consiste à développer un site web portfolio personnel permettant de présenter mon profil professionnel, mes compétences techniques, mon parcours académique, mes expériences ainsi que mes différents projets de développement informatique.

En tant que développeuse web Full-Stack, avec une orientation particulière vers le développement Backend, ce portfolio constitue un espace professionnel destiné à valoriser mon parcours, présenter mes réalisations et faciliter les échanges avec des recruteurs, des clients et d'autres professionnels du domaine informatique.

L'application est développée avec **Python et Flask** pour la partie Backend, tandis que l'interface utilisateur est construite avec **HTML5, CSS3, JavaScript et Jinja2**.

## 🎯 Objectifs du projet

- Présenter mon profil personnel et professionnel.
- Mettre en valeur mes compétences techniques.
- Présenter mes projets réalisés et en cours de développement.
- Valoriser mes expériences professionnelles et mes réalisations.
- Faciliter la prise de contact avec les visiteurs.
- Renforcer mes compétences en Python et en développement d'applications web.

## 🛠️ Technologies utilisées

### Backend

| Technologie | Description |
|---|---|
| Python | Langage de programmation principal. |
| Flask | Framework Python utilisé pour développer la partie Backend. |
| Jinja2 | Moteur de templates permettant de générer des pages HTML dynamiques. |
| Flask-WTF (optionnel) | Gestion et validation des formulaires. |
| Flask-Mail (optionnel) | Gestion de l'envoi des emails. |

### Frontend

| Technologie | Description |
|---|---|
| HTML5 | Structure des pages web. |
| CSS3 | Mise en forme et design de l'interface. |
| JavaScript | Gestion des interactions et fonctionnalités dynamiques. |
| Bootstrap (optionnel) | Création d'interfaces responsives à l'aide de composants prédéfinis. |

### Outils de développement

| Outil | Description |
|---|---|
| Git | Gestion des versions du projet. |
| GitHub | Hébergement du code source et collaboration. |
| VS Code / PyCharm | Éditeur de code. |
| Python venv | Création d'un environnement virtuel. |
| pip | Gestionnaire de packages Python. |

## ✨ Fonctionnalités principales

### 1. Page d'accueil

- Présentation professionnelle.
- Photo de profil.
- Titre professionnel et courte description.
- Boutons d'accès rapide aux différentes sections.
- Liens vers les réseaux sociaux professionnels.

### 2. À propos de moi

- Présentation personnelle et professionnelle.
- Parcours académique.
- Parcours professionnel.
- Objectifs et ambitions.

### 3. Compétences techniques

Présentation des différentes compétences dans plusieurs domaines :

- Développement Backend.
- Développement Frontend.
- Gestion des bases de données.
- Outils et environnements de développement.

### 4. Projets réalisés

- Présentation des projets développés.
- Description de chaque projet.
- Technologies utilisées.
- Liens vers les dépôts GitHub.
- Liens vers les versions accessibles en ligne.

### 5. Expériences et réalisations

- Expériences professionnelles.
- Programmes de formation.
- Participation aux communautés technologiques.
- Certifications et distinctions.

### 6. Contact

- Formulaire de contact.
- Adresse email professionnelle.
- Liens vers LinkedIn et GitHub.
- Possibilité d'envoyer un message directement depuis le portfolio.

## Structure du projet

Voici la structure d'organisation proposée pour le projet :

```text
portfolio/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── skills.html
│   ├── projects.html
│   ├── experience.html
│   └── contact.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   ├── images/
│   │   ├── profile.jpg
│   │   └── projects/
│   └── documents/
│       └── cv.pdf
│
├── services/
│   └── contact_service.py
│
└── .venv/
```

### Explication des principaux dossiers et fichiers

| Élément | Rôle |
|---|---|
| `app.py` | Point d'entrée principal de l'application Flask. |
| `config.py` | Gestion des paramètres de configuration. |
| `requirements.txt` | Liste des dépendances Python du projet. |
| `.env.example` | Exemple des variables d'environnement nécessaires. |
| `templates/` | Contient les pages HTML et les templates Jinja2. |
| `static/` | Contient les fichiers CSS, JavaScript, images et documents. |
| `services/` | Contient les fonctions dédiées à certaines opérations métier. |
| `.venv/` | Environnement virtuel du projet. |

**Remarque :** le dossier `.venv/` est généré localement et ne doit pas être envoyé sur GitHub.

## ⚙️ Prérequis

Avant de commencer l'installation, assurez-vous de disposer des outils suivants :

- Python 3.10 ou une version supérieure.
- Git installé sur votre ordinateur.
- pip, le gestionnaire de packages Python.
- Un éditeur de code tel que VS Code ou PyCharm.

Vérifier la version de Python :

```bash
python --version
```

Vérifier l'installation de Git :

```bash
git --version
```

## Installation et configuration du projet

### 1. Cloner le dépôt GitHub

Ouvrir un terminal et exécuter la commande suivante :

```bash
git clone https://github.com/laurence1Mas/portfolio_with_python.git
```

Cette commande permet de récupérer une copie du projet depuis GitHub.

### 2. Accéder au dossier du projet

```bash
cd portfolio_with_python
```

### 3. Créer un environnement virtuel

```bash
py -m venv .venv
```

L'environnement virtuel permet d'isoler les dépendances du projet afin d'éviter les conflits avec les packages utilisés dans d'autres projets Python.

### 4. Activer l'environnement virtuel

**Sur Windows avec Git Bash :**

```bash
source .venv/Scripts/activate
```

**Sur Windows avec PowerShell :**

```powershell
.venv\Scripts\Activate.ps1
```

**Sur Linux ou macOS :**

```bash
source .venv/bin/activate
```

Une fois l'environnement activé, vous devriez voir `(.venv)` au début de la ligne de commande.

### 5. Installer les dépendances

Si le fichier `requirements.txt` est déjà présent à la racine du projet :

```bash
pip install -r requirements.txt
```

Si les dépendances ne sont pas encore définies, installer Flask :

```bash
pip install flask
```

Après l'installation des packages, vous pouvez générer le fichier des dépendances avec :

```bash
pip freeze > requirements.txt
```

### 6. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet lorsque l'application utilise des variables d'environnement.

Exemple :

```env
SECRET_KEY=votre-cle-secrete
FLASK_DEBUG=True
```

**Important :** ne jamais publier les véritables clés secrètes ou identifiants dans un dépôt GitHub public.

### 7. Lancer l'application

Exécuter la commande suivante :

```bash
python app.py
```

Ouvrir ensuite un navigateur et accéder à l'adresse :

```text
http://127.0.0.1:5000
```

L'application devrait maintenant être accessible en local.

##  Mode développement

Pendant le développement, Flask peut redémarrer automatiquement le serveur lorsque des modifications sont détectées.

Il est également possible de lancer l'application avec la commande :

```bash
flask --app app run --debug
```

**Attention :** le mode Debug doit être utilisé uniquement pendant le développement local. Il ne doit jamais être activé en production.

##  Gestion des dépendances

Installer un nouveau package :

```bash
pip install nom_du_package
```

Mettre à jour le fichier des dépendances :

```bash
pip freeze > requirements.txt
```

Afficher les packages installés :

```bash
pip list
```

Désactiver l'environnement virtuel :

```bash
deactivate
```

## Gestion du projet avec Git et GitHub

Initialiser Git :

```bash
git init
```

Ajouter les fichiers au suivi :

```bash
git add .
```

Créer un commit :

```bash
git commit -m "Initialisation du projet portfolio"
```

Associer le dépôt distant GitHub :

```bash
git remote add origin https://github.com/laurence1Mas/portfolio_with_python.git
```

Envoyer le code sur GitHub :

```bash
git branch -M main
git push -u origin main
```

##  Déploiement de l'application

L'application pourra être hébergée sur une plateforme compatible avec Python et Flask.

Quelques plateformes envisageables :

- **Render** : hébergement d'applications web Python.
- **Railway** : déploiement d'applications Backend.
- **PythonAnywhere** : hébergement spécialisé dans les applications Python.
- **VPS** : possibilité de configurer un serveur avec Gunicorn et Nginx.

### Préparation pour la production

Pour un déploiement en production, il est recommandé d'utiliser un serveur WSGI tel que Gunicorn plutôt que le serveur de développement intégré de Flask.

Installer Gunicorn :

```bash
pip install gunicorn
```

Exemple de commande de lancement sur un environnement Linux :

```bash
gunicorn app:app
```

Veiller également à configurer les variables d'environnement nécessaires sur la plateforme d'hébergement.

##  Améliorations futures

Plusieurs fonctionnalités pourront être ajoutées progressivement :

- Développer un tableau de bord d'administration.
- Stocker les projets et expériences dans une base de données.
- Ajouter un formulaire de contact avec notifications par email.
- Intégrer une section blog.
- Optimiser le référencement naturel (SEO).
- Ajouter des animations et des interactions.
- Proposer plusieurs langues (français et anglais).
- Intégrer un système de statistiques de visites.

##  À propos de l'auteure

**Laurence MASIKA**

Développeuse Web Full-Stack | Spécialisée en développement Backend.

Passionnée par les nouvelles technologies, le développement web et l'apprentissage continu, je m'intéresse particulièrement à la conception et au développement de solutions numériques répondant à des besoins réels.

### Me retrouver sur les plateformes professionnelles

- **GitHub :** [laurence1Mas](https://github.com/laurence1Mas)
- **LinkedIn :** [Mon profil LinkedIn](https://www.linkedin.com/in/laure-masika-8a7aa832a/)
- **Portfolio :** [Mon portfolio.](https://laurence-mak-portfolio.vercel.app/)

##  Licence

Ce projet est développé dans un cadre personnel et professionnel afin de présenter mon parcours, mes compétences et mes réalisations.

Tous droits réservés © Laurence Masika.
