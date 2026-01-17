import sqlite3
from datetime import datetime
import json

DB_NAME = "data.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        source TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id integer,
        chunk TEXT,
        embedding TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_item(text, source):
    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT INTO items (text, source, created_at)
    VALUES (?, ?, ?)
    """, (text, source, created_at))

    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return item_id


def get_items():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, text, source, created_at
    FROM items
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def save_chunk(item_id,chunk,embedding):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chunks (item_id, chunk, embedding)
    VALUES (?, ?, ?)
    """, (item_id, chunk, json.dumps(embedding)))

    conn.commit()
    conn.close()

def get_chunks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT chunk, embedding
    FROM chunks
    """)

    rows = cursor.fetchall()
    conn.close()

    return [(r[0], json.loads(r[1])) for r in rows]