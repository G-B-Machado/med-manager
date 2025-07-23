import sqlite3
import hashlib
import os


CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), '..', 'db', 'database.db')

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

    try:
        cursor.execute("SELECT med_id, nome_generico, dosagem, forma FROM medications")
        medicamentos = cursor.fetchall()

        if medicamentos:
            print("📋 Lista de Medicamentos:")
            for med_id, nome, dosagem, forma in medicamentos:
                print(f"🧪 ID: {med_id}, Nome: {nome}, Dosagem: {dosagem}, Forma: {forma}")
        else:
            print("⚠️ Nenhum medicamento cadastrado.")
    except Exception as e:
        print(f"❌ Erro ao listar medicamentos: {e}")
    finally:
        conn.close()


def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user_id, nome, email FROM users")
        usuarios = cursor.fetchall()

        if usuarios:
            print("👥 Lista de Usuários:")
            for user_id, nome, email in usuarios:
                print(f"🆔 ID: {user_id}, Nome: {nome}, Email: {email}")
        else:
            print("⚠️ Nenhum usuário cadastrado.")
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {e}")
    finally:
        conn.close()

def listar_medicamentos_por_usuario(user_id):
    conn = conectar()
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
    finally:
        conn.close()

def verificar_estoque_baixo(user_id, limite=5):
    conn = conectar()
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
    finally:
        conn.close()

def registrar_dose(user_id, med_id, dose):
    conn = conectar()
    cursor = conn.cursor()

    try:
        # Verifica o estoque atual
        cursor.execute("""
            SELECT quantidade_atual, unidade
            FROM user_meds
            WHERE user_id = ? AND med_id = ?
        """, (user_id, med_id))

        resultado = cursor.fetchone()

        if resultado:
            quantidade_atual, unidade = resultado

            if quantidade_atual < dose:
                print(f"⚠️ Estoque insuficiente para o medicamento. Restam apenas {quantidade_atual} {unidade}.")
                return

            nova_quantidade = quantidade_atual - dose

            # Atualiza o valor
            cursor.execute("""
                UPDATE user_meds
                SET quantidade_atual = ?
                WHERE user_id = ? AND med_id = ?
            """, (nova_quantidade, user_id, med_id))

            conn.commit()

            print(f"✅ Dose registrada com sucesso.")
            print(f"📉 Novo estoque: {nova_quantidade} {unidade}")
        else:
            print("❌ Associação entre usuário e medicamento não encontrada.")
    except Exception as e:
        print(f"❌ Erro ao registrar dose: {e}")
    finally:
        conn.close()

def simular_uso_diario(user_id, med_id, dose_por_vez, vezes_por_dia, dias):
    conn = conectar()
    cursor = conn.cursor()

    try:
        # Consulta o estoque atual
        cursor.execute("""
            SELECT quantidade_atual, unidade
            FROM user_meds
            WHERE user_id = ? AND med_id = ?
        """, (user_id, med_id))
        resultado = cursor.fetchone()

        if not resultado:
            print("❌ Associação entre usuário e medicamento não encontrada.")
            return

        quantidade_atual, unidade = resultado
        total_dose = dose_por_vez * vezes_por_dia * dias

        if quantidade_atual < total_dose:
            print(f"⚠️ Estoque insuficiente para simular {dias} dia(s) de uso ({total_dose} {unidade} necessárias).")
            return

        nova_quantidade = quantidade_atual - total_dose

        # Atualiza o estoque
        cursor.execute("""
            UPDATE user_meds    
            SET quantidade_atual = ?
            WHERE user_id = ? AND med_id = ?
        """, (nova_quantidade, user_id, med_id))

        # Registra no log de uso
        for dia in range(dias):
            for dose in range(vezes_por_dia):
                cursor.execute("""
                    INSERT INTO medication_usage_log (user_id, med_id, quantidade_usada, unidade)
                    VALUES (?, ?, ?, ?)
                """, (user_id, med_id, dose_por_vez, unidade))

        conn.commit()

        print(f"✅ Simulação concluída e registrada: {dias} dia(s) × {vezes_por_dia} dose(s)/dia × {dose_por_vez} {unidade}/dose")
        print(f"📉 Estoque anterior: {quantidade_atual} {unidade}")
        print(f"📦 Novo estoque: {nova_quantidade} {unidade}")

    except Exception as e:
        print(f"❌ Erro durante simulação: {e}")
    finally:
        conn.close()

def listar_historico_uso(user_id=None, med_id=None):
    conn = conectar()
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

    conn.close()

def cadastrar_agendamento(user_med_id, hora, dias_semana, dose):
    """
    Cadastra um agendamento de uso de medicamento.
    :param user_med_id: ID da relação entre usuário e medicamento
    :param hora: Horário no formato 'HH:MM'
    :param dias_semana: Dias da semana (ex: '1,3,5')
    :param dose: Quantidade a ser tomada
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO schedules (user_med_id, hora, dias_semana, dose)
        VALUES (?, ?, ?, ?)
    """, (user_med_id, hora, dias_semana, dose))

    conn.commit()
    conn.close()
    print("📅 Agendamento cadastrado com sucesso.")

