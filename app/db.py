import os
import sqlite3

# Le chemin de la base est configurable (important pour Docker + volume)
DB_PATH = os.environ.get("DATABASE_PATH", "incidents.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # permet d'accéder aux colonnes par nom
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT NOT NULL,
                lieu TEXT NOT NULL,
                priorite TEXT NOT NULL DEFAULT 'moyenne',
                statut TEXT NOT NULL DEFAULT 'nouveau'
            )
            """
        )
