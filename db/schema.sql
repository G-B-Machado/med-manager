-- Limpeza das tabelas existentes
DROP TABLE IF EXISTS schedule_days;
DROP TABLE IF EXISTS pharmacy_prices;
DROP TABLE IF EXISTS medication_usage_log;
DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS user_meds;
DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS users;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS users (
  user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  nome        TEXT    NOT NULL,
  telefone    TEXT    NOT NULL,
  email       TEXT    NOT NULL UNIQUE,
  senha_hash  TEXT    NOT NULL
);

-- Tabela de medicamentos
CREATE TABLE IF NOT EXISTS medications (
  med_id            INTEGER PRIMARY KEY AUTOINCREMENT,
  nome_generico     TEXT    NOT NULL,
  nome_comercial    TEXT,
  fabricante        TEXT,
  dosagem           TEXT,
  forma             TEXT
);

-- Associação entre usuários e medicamentos
CREATE TABLE IF NOT EXISTS user_meds (
  user_med_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id          INTEGER NOT NULL,
  med_id           INTEGER NOT NULL,
  quantidade_atual REAL    NOT NULL,
  unidade          TEXT    NOT NULL,
  data_inicio      DATE    NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (med_id)  REFERENCES medications(med_id)
);

-- Agendamentos de uso de medicamentos
CREATE TABLE IF NOT EXISTS schedules (
  sched_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  user_med_id  INTEGER NOT NULL,
  hora         TEXT    NOT NULL,       -- formato HH:MM
  dias_semana  TEXT    NOT NULL,       -- ex: "1,3,5"
  dose         REAL    NOT NULL,
  FOREIGN KEY (user_med_id) REFERENCES user_meds(user_med_id)
);

-- Registro detalhado dos dias da semana (opcional para normalização futura)
CREATE TABLE IF NOT EXISTS schedule_days (
  schedule_day_id INTEGER PRIMARY KEY AUTOINCREMENT,
  sched_id        INTEGER NOT NULL,
  dia             INTEGER NOT NULL,  -- 0=Segunda, ..., 6=Domingo
  FOREIGN KEY (sched_id) REFERENCES schedules(sched_id)
);

-- Histórico de uso de medicamentos
CREATE TABLE IF NOT EXISTS medication_usage_log (
  log_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  med_id INTEGER NOT NULL,
  data_uso DATETIME DEFAULT CURRENT_TIMESTAMP,
  quantidade_usada REAL NOT NULL,
  unidade TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (med_id) REFERENCES medications(med_id)
);

-- Preços dos medicamentos em farmácias
CREATE TABLE IF NOT EXISTS pharmacy_prices (
  price_id INTEGER PRIMARY KEY AUTOINCREMENT,
  med_id INTEGER NOT NULL,
  farmacia TEXT NOT NULL,
  preco REAL NOT NULL,
  data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (med_id) REFERENCES medications(med_id)
);
