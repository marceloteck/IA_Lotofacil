import sqlite3

conn = sqlite3.connect("data/lotofacil.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(concursos)")
print(cursor.fetchall())
