import sqlite3

def init_db():
    conn = sqlite3.connect("pathforge.db", check_same_thread=False)
    c = conn.cursor()
    conn = sqlite3.connect("roadmaps.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT,
       goal TEXT,
       duration TEXT,
       tasks TEXT,
       created_at TEXT,
       last_updated TEXT,
       update_count INTEGER DEFAULT 0
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password BLOB,
        streak INTEGER DEFAULT 0,
        quizzes_passed INTEGER DEFAULT 0,
        last_active TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        goal TEXT,
        duration TEXT,
        content TEXT,
        created_at TEXT
        progress INTEGER DEFAULT 0
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        topic TEXT,
        day INTEGER,
        score REAL,
        created_at TEXT
    )
    """)
    try:
        c.execute("ALTER TABLE ROADMAPS ADD COLUMN progress INTEGER DEFAULT 0")
    except:
        pass

    conn.commit()
    return conn