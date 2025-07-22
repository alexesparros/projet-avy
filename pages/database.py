import sqlite3

# Connexion à la base (SQLite ici)
def get_connection():
    conn = sqlite3.connect("database_client")
    return conn

# Créer la table clients si pas encore faite
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT,
            sex INT,
            reponse1 TEXT,
            reponse2 TEXT
        )
    """)
    conn.commit()
    conn.close()

# Ajouter un client depuis l'inscription
def add_client(nom, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (nom, email) VALUES (?, ?)", (nom, email))
    conn.commit()
    conn.close()

# Ajouter les réponses du questionnaire
def add_questionnaire(client_id, reponse1, reponse2):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET reponse1 = ?, reponse2 = ?
        WHERE id = ?
    """, (reponse1, reponse2, client_id))
    conn.commit()
    conn.close()
