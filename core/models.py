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

def cadastrar_medicamento(nome, dosagem, forma ):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO medications (nome_generico, dosagem, forma)
            VALUES (?, ?, ?)
        """, (nome, dosagem, forma))

        conn.commit()
        print(f"✅ Medicamento '{nome}' cadastrado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao cadastrar medicamento: {e}")
    finally:
        conn.close()

def associar_usuario_medicamento(user_id, med_id, quantidade_atual, unidade, data_inicio):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO user_meds (user_id, med_id, quantidade_atual, unidade, data_inicio)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, med_id, quantidade_atual, unidade, data_inicio))

        conn.commit()
        print(f"✅ Usuário {user_id} agora está associado ao medicamento {med_id}.")
    except Exception as e:
        print(f"❌ Erro ao associar usuário e medicamento: {e}")
    finally:
        conn.close()

def listar_medicamentos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM medications")
    medicamentos = cursor.fetchall()

    if medicamentos:
        print("📋 Lista de Medicamentos:")
        for med in medicamentos:
            print(f"ID: {med[0]}, Nome: {med[1]}, Dosagem: {med[2]}, Forma: {med[3]}")
    else:
        print("❌ Nenhum medicamento cadastrado.")

    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    usuarios = cursor.fetchall()

    if usuarios:
        print("📋 Lista de Usuários:")
        for user in usuarios:
            print(f"ID: {user[0]}, Nome: {user[1]}, Email: {user[2]}")
    else:
        print("❌ Nenhum usuário cadastrado.")

    conn.close()