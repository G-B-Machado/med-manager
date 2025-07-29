
import sqlite3
import hashlib
import os
import datetime
from enviar_sms import enviar_sms
from contextlib import contextmanager

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), '..', 'db', 'database.db')

@contextmanager
def conexao():
    conn = sqlite3.connect(CAMINHO_BANCO)
    try:
        yield conn
    finally:
        conn.close()

def hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def cadastrar_usuario(nome, email, senha, telefone=""):
    senha_hash = hash_senha(senha)
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (nome, email, senha_hash, telefone)
                VALUES (?, ?, ?, ?)
            """, (nome, email, senha_hash, telefone))
            conn.commit()
            print(f"✅ Usuário '{nome}' cadastrado com sucesso.")
        except sqlite3.IntegrityError:
            print(f"❌ Já existe um usuário com o email '{email}'.")

def cadastrar_medicamento(nome_generico, nome_comercial, fabricante, dosagem, forma):
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO medications (nome_generico, nome_comercial, fabricante, dosagem, forma)
                VALUES (?, ?, ?, ?, ?)
            """, (nome_generico, nome_comercial, fabricante, dosagem, forma))
            conn.commit()
            print(f"✅ Medicamento '{nome_generico}' cadastrado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao cadastrar medicamento: {e}")

def cadastrar_preco_medicamento(med_id, farmacia, preco):
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO pharmacy_prices (med_id, farmacia, preco)
                VALUES (?, ?, ?)
            """, (med_id, farmacia, preco))
            conn.commit()
            print(f"💰 Preço cadastrado: R${preco:.2f} na farmácia {farmacia}.")
        except Exception as e:
            print(f"❌ Erro ao cadastrar preço: {e}")

def buscar_melhor_preco(med_id):
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT farmacia, preco
                FROM pharmacy_prices
                WHERE med_id = ?
                ORDER BY preco ASC
                LIMIT 1
            """, (med_id,))
            resultado = cursor.fetchone()
            if resultado:
                farmacia, preco = resultado
                print(f"🔍 Melhor preço: R${preco:.2f} na farmácia {farmacia}")
            else:
                print("⚠️ Nenhum preço encontrado para esse medicamento.")
        except Exception as e:
            print(f"❌ Erro ao buscar melhor preço: {e}")

def verificar_agendamentos():
    agora = datetime.datetime.now()
    hora_atual = agora.strftime("%H:%M")
    dia_atual = str(agora.weekday())  # Segunda = 0, Domingo = 6

    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT s.user_med_id, s.hora, s.dias_semana, s.dose,
                       u.user_id, u.nome, u.telefone, m.nome_generico, m.med_id
                FROM schedules s
                JOIN user_meds um ON s.user_med_id = um.user_med_id
                JOIN users u ON um.user_id = u.user_id
                JOIN medications m ON um.med_id = m.med_id
                WHERE s.hora = ?
            """, (hora_atual,))
            agendamentos = cursor.fetchall()

            for agendamento in agendamentos:
                dias_semana = agendamento[2].split(',')
                if dia_atual not in dias_semana:
                    continue

                user_med_id = agendamento[0]
                dose = agendamento[3]
                user_id = agendamento[4]
                user_nome = agendamento[5]
                user_telefone = agendamento[6]
                med_nome = agendamento[7]
                med_id = agendamento[8]

                mensagem = f"Olá {user_nome}, está na hora de tomar {dose} de {med_nome}. 💊"
                enviar_sms(user_telefone, mensagem)

                # Tenta registrar a dose após o lembrete
                cursor.execute("""
                    SELECT quantidade_atual
                    FROM user_meds
                    WHERE user_med_id = ?
                """, (user_med_id,))
                resultado = cursor.fetchone()
                if resultado and resultado[0] >= dose:
                    nova_quantidade = resultado[0] - dose
                    cursor.execute("""
                        UPDATE user_meds SET quantidade_atual = ?
                        WHERE user_med_id = ?
                    """, (nova_quantidade, user_med_id))
                    cursor.execute("""
                        INSERT INTO medication_usage_log (user_id, med_id, quantidade_usada, unidade)
                        VALUES (?, ?, ?, (SELECT unidade FROM user_meds WHERE user_med_id = ?))
                    """, (user_id, med_id, dose, user_med_id))
                    conn.commit()
        except Exception as e:
            print(f"❌ Erro ao verificar agendamentos: {e}")

def associar_usuario_medicamento(user_id, med_id, quantidade_atual, unidade, data_inicio):
    with conexao() as conn:
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

def listar_medicamentos():
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT med_id, nome_generico, nome_comercial, fabricante, dosagem, forma
                FROM medications
            """)
            medicamentos = cursor.fetchall()
            if medicamentos:
                print("📋 Lista de Medicamentos:")
                for med in medicamentos:
                    print(f"🧪 ID: {med[0]}, Nome: {med[1]}, Comercial: {med[2]}, Fabricante: {med[3]}, Dosagem: {med[4]}, Forma: {med[5]}")
            else:
                print("⚠️ Nenhum medicamento cadastrado.")
        except Exception as e:
            print(f"❌ Erro ao listar medicamentos: {e}")

def listar_usuarios():
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id, nome, email, telefone FROM users")
            usuarios = cursor.fetchall()
            if usuarios:
                print("👥 Lista de Usuários:")
                for user in usuarios:
                    print(f"🆔 ID: {user[0]}, Nome: {user[1]}, Email: {user[2]}, Telefone: {user[3]}")
            else:
                print("⚠️ Nenhum usuário cadastrado.")
        except Exception as e:
            print(f"❌ Erro ao listar usuários: {e}")

def listar_medicamentos_por_usuario(user_id):
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.nome_generico, m.dosagem, m.forma,
                       um.quantidade_atual, um.unidade, um.data_inicio
                FROM user_meds um
                JOIN medications m ON um.med_id = m.med_id
                WHERE um.user_id = ?
            """, (user_id,))
            medicamentos = cursor.fetchall()
            if medicamentos:
                print(f"📋 Medicamentos do Usuário ID {user_id}:")
                for nome, dosagem, forma, quantidade, unidade, data_inicio in medicamentos:
                    print(f"🧪 {nome} ({dosagem}, {forma})")
                    print(f"   Quantidade Atual: {quantidade} {unidade}")
                    print(f"   Início: {data_inicio}")
            else:
                print("⚠️ Nenhum medicamento associado a este usuário.")
        except Exception as e:
            print(f"❌ Erro ao buscar medicamentos do usuário: {e}")

def verificar_estoque_baixo(user_id, limite=5):
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT m.nome_generico, m.dosagem, m.forma,
                       um.quantidade_atual, um.unidade
                FROM user_meds um
                JOIN medications m ON um.med_id = m.med_id
                WHERE um.user_id = ? AND um.quantidade_atual <= ?
            """, (user_id, limite))
            medicamentos_baixos = cursor.fetchall()
            if medicamentos_baixos:
                print(f"🔴 Medicamentos com estoque baixo (≤ {limite}) para o Usuário ID {user_id}:")
                for nome, dosagem, forma, quantidade, unidade in medicamentos_baixos:
                    print(f"⚠️ {nome} ({dosagem}, {forma}) - {quantidade} {unidade} restantes")
            else:
                print("✅ Nenhum medicamento com estoque baixo.")
        except Exception as e:
            print(f"❌ Erro ao verificar estoque baixo: {e}")

def registrar_dose(user_id, med_id, dose):
    with conexao() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT quantidade_atual, unidade, user_med_id
                FROM user_meds
                WHERE user_id = ? AND med_id = ?
            """, (user_id, med_id))
            resultado = cursor.fetchone()
            if resultado:
                quantidade_atual, unidade, user_med_id = resultado
                if quantidade_atual < dose:
                    print(f"⚠️ Estoque insuficiente. Restam apenas {quantidade_atual} {unidade}.")
                    return
                nova_quantidade = quantidade_atual - dose
                cursor.execute("""
                    UPDATE user_meds SET quantidade_atual = ?
                    WHERE user_id = ? AND med_id = ?
                """, (nova_quantidade, user_id, med_id))
                cursor.execute("""
                    INSERT INTO medication_usage_log (user_id, med_id, quantidade_usada, unidade)
                    VALUES (?, ?, ?, ?)
                """, (user_id, med_id, dose, unidade))
                conn.commit()
                print(f"✅ Dose registrada. Novo estoque: {nova_quantidade} {unidade}")
            else:
                print("❌ Associação entre usuário e medicamento não encontrada.")
        except Exception as e:
            print(f"❌ Erro ao registrar dose: {e}")
def listar_historico_uso(user_id=None, med_id=None):
    with conexao() as conn:
        cursor = conn.cursor()

        query = """
            SELECT log.user_id, u.nome, m.nome_generico, log.quantidade_usada, log.unidade, log.data_uso
            FROM medication_usage_log log
            JOIN users u ON log.user_id = u.user_id
            JOIN medications m ON log.med_id = m.med_id
        """
        params = []
        filtros = []

        if user_id:
            filtros.append("log.user_id = ?")
            params.append(user_id)

        if med_id:
            filtros.append("log.med_id = ?")
            params.append(med_id)

        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        query += " ORDER BY log.data_uso DESC"

        cursor.execute(query, params)
        registros = cursor.fetchall()

        if registros:
            print("📅 Histórico de Uso de Medicamentos:")
            for reg in registros:
                print(f"ID Uso: {reg[0]} | Usuário: {reg[1]} | Medicamento: {reg[2]} | Quantidade: {reg[3]} {reg[4]} | Data: {reg[5]}")
        else:
            print("❌ Nenhum registro encontrado para o filtro aplicado.")

def cadastrar_agendamento(user_med_id, hora, dias_semana, dose):
    """
    Cadastra um agendamento de uso de medicamento.
    :param user_med_id: ID da relação entre usuário e medicamento
    :param hora: Horário no formato 'HH:MM'
    :param dias_semana: Dias da semana (ex: '1,3,5')
    :param dose: Quantidade a ser tomada
    """
    with conexao() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO schedules (user_med_id, hora, dias_semana, dose)
            VALUES (?, ?, ?, ?)
        """, (user_med_id, hora, dias_semana, dose))

        conn.commit()
        print("📅 Agendamento cadastrado com sucesso.")

def verificar_agendamentos():
    agora = datetime.datetime.now()
    hora_atual = agora.strftime("%H:%M")
    dia_atual = str(agora.weekday())  # Segunda = 0, Domingo = 6

    with conexao() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT s.user_med_id, s.hora, s.dias_semana, s.dose,
                    u.user_id, u.nome, u.telefone, m.nome_generico
                FROM schedules s
                JOIN user_meds um ON s.user_med_id = um.user_med_id
                JOIN users u ON um.user_id = u.user_id
                JOIN medications m ON um.med_id = m.med_id
                WHERE s.hora = ?
            """, (hora_atual,))

            agendamentos = cursor.fetchall()

            for agendamento in agendamentos:
                dias_semana = agendamento[2].split(',')
                if dia_atual not in dias_semana:
                    continue  # Pula se hoje não é um dos dias do agendamento

                user_nome = agendamento[5]
                user_telefone = agendamento[6]
                med_nome = agendamento[7]
                dose = agendamento[3]

                mensagem = f"Olá {user_nome}, está na hora de tomar {dose} de {med_nome}. 💊"
                enviar_sms(user_telefone, mensagem)

        except Exception as e:
            print(f"❌ Erro ao verificar agendamentos: {e}")