import sqlite3
import os

def criar_banco():
    caminho_banco = "database.db"
    caminho_schema = os.path.join("db", "schema.sql")

    with open(caminho_schema, 'r', encoding='utf-8') as f:
        schema = f.read()

    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()

    print("✅ Banco de dados criado com sucesso.")

if __name__ == "__main__":
    criar_banco()
