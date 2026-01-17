import sqlite3
from datetime import datetime

conn=sqlite3.connect('data.db')
cursor=conn.cursor()

cursor.execute(""""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    context TEXT,
    source TEXT,
    created_at TEXT
               )
""")

conn.commit()

def save_item(context, source):
    created_at = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO items (context, source, created_at)
    VALUES (?, ?, ?)
    """, (context, source, created_at))
    conn.commit()
    return cursor.lastrowid

def get_item(item_id):
    cursor.execute("""
    SELECT id, context, source, created_at
    FROM items""")
    return cursor.fetchall()