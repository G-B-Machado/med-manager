import sqlite3
import hashlib
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def cadastrar_usuario(nome, email, senha):
    senha_hash = hash_senha(senha)
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (nome, email, senha_hash)
            VALUES (?, ?, ?)
        """, (nome, email, senha_hash))

        conn.commit()
        print(f"✅ Usuário '{nome}' cadastrado com sucesso.")
    except sqlite3.IntegrityError:
        print(f"❌ Já existe um usuário com o email '{email}'.")
    finally:
        conn.close()
