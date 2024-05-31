import sqlite3

conn = sqlite3.connect("example.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')

cursor.execute(f'''
INSERT INTO users (name, age)
VALUES ("Alice", {30}),
       ("Bob", {25})
''')

conn.commit()

cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
