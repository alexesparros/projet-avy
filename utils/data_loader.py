# Fonctions de gestion de base de données pour le projet AVY

import sqlite3
from datetime import datetime

# --- Gestion de la base clients (ex-database.py) ---
def get_connection_clients():
    return sqlite3.connect("database_clients.db")

def create_table_clients():
    conn = get_connection_clients()
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

def add_client(nom, email):
    conn = get_connection_clients()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (nom, email) VALUES (?, ?)", (nom, email))
    conn.commit()
    conn.close()

def add_questionnaire(client_id, reponse1, reponse2):
    conn = get_connection_clients()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clients
        SET reponse1 = ?, reponse2 = ?
        WHERE id = ?
    """, (reponse1, reponse2, client_id))
    conn.commit()
    conn.close()

# --- Gestion de la base questionnaire (ex-questionnaire.py) ---
def init_db_profil():
    conn = sqlite3.connect("profil_gamer.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS reponses (
    username TEXT PRIMARY KEY,
    timestamp TEXT,
    annee_jeu INTEGER,
    type_joueur TEXT,
    budget_mensuel INTEGER,
    jeu_marquant TEXT,
    critere_ia TEXT,
    competition INTEGER,
    narration INTEGER,
    exploration INTEGER,
    creativite INTEGER,
    detente INTEGER,
    social INTEGER,
    immersion INTEGER,
    curiosite INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def enregistrer_ou_mettre_a_jour_profil(username, annee_jeu, type_joueur, budget_mensuel, jeu_marquant, critere_ia, profil_scores):
    conn = sqlite3.connect("profil_gamer.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reponses WHERE username = ?", (username,))
    exist = c.fetchone()
    if exist:
        c.execute('''
        UPDATE reponses SET
            timestamp = ?, annee_jeu = ?, type_joueur = ?, budget_mensuel = ?,
            jeu_marquant = ?, critere_ia = ?,
            competition = ?, narration = ?, exploration = ?, creativite = ?,
            detente = ?, social = ?, immersion = ?, curiosite = ?
        WHERE username = ?
        ''', (
        datetime.now().isoformat(), annee_jeu, type_joueur, budget_mensuel,
        jeu_marquant, critere_ia,
        profil_scores["Compétition"],
        profil_scores["Narration"],
        profil_scores["Exploration"],
        profil_scores["Créativité"],
        profil_scores["Détente"],
        profil_scores["Social"],
        profil_scores["Immersion"],
        profil_scores["Curiosité"],
        username
        ))
    else:
        c.execute('''
        INSERT INTO reponses (
            username, timestamp, annee_jeu, type_joueur, budget_mensuel,
            jeu_marquant, critere_ia,
            competition, narration, exploration, creativite,
            detente, social, immersion, curiosite
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        username, datetime.now().isoformat(), annee_jeu, type_joueur, budget_mensuel,
        jeu_marquant, critere_ia,
        profil_scores["Compétition"],
        profil_scores["Narration"],
        profil_scores["Exploration"],
        profil_scores["Créativité"],
        profil_scores["Détente"],
        profil_scores["Social"],
        profil_scores["Immersion"],
        profil_scores["Curiosité"]
        ))
    conn.commit()
    conn.close() 