import sqlite3

def get_connection(db_name="database_clients"):
    return sqlite3.connect(db_name, check_same_thread=False)

def create_users_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()

def add_user(conn, username, email, password):
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    conn.commit()

def get_user_by_email(conn, email):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    return c.fetchone()

def get_user_by_username_and_password(conn, username, password):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return c.fetchone()

def create_reponses_table():
    conn = get_connection("profil_gamer.db")
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

def enregistrer_ou_mettre_a_jour(username, annee_jeu, type_joueur, budget_mensuel, jeu_marquant, critere_ia, profil_scores):
    from datetime import datetime
    conn = get_connection("profil_gamer.db")
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

# Ajoute ici les fonctions :
# - création de tables
# - ajout utilisateur
# - vérification utilisateur
# - enregistrement questionnaire
# - etc. 