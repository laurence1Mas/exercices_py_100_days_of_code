
import os
# This is the configuration file for the online shop application. It sets up the base directory and defines a configuration class that includes settings for the secret key and database URI. The secret key is used for 
# session management and should be changed in production. The database URI points to a SQLite database file located in the base directory. The SQLALCHEMY_TRACK_MODIFICATIONS setting is disabled to avoid unnecessary overhead.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-later"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "ecommerce.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
