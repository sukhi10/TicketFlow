import sqlite3

conn = sqlite3.connect('tickets.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    reported_by TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT DEFAULT 'Open',
    assignee TEXT,
    created_at DATETIME,
    resolved_by DATETIME
)
""")

conn.commit()
conn.close()