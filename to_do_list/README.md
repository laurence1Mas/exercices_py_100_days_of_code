# Liste de tâches

Petite application de tâches réalisée avec Flask, SQLAlchemy et SQLite. Pour la lancer, installe les dépendances avec `pip install -r requirements.txt`, puis exécute `python app.py` dans le dossier `to_do_list` et ouvre `http://127.0.0.1:5000`.

`models.py` définit une tâche avec son titre et son état terminé. Flask crée la base `instance/todo.db` au démarrage et affiche les tâches dans `index.html`. Les formulaires permettent d’ajouter, modifier, terminer ou supprimer une tâche ; SQLAlchemy enregistre chaque changement dans SQLite.
