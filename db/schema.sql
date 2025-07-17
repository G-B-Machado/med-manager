-- schema.sql

DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS user_meds;
DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  nome        TEXT    NOT NULL,
  email       TEXT    NOT NULL UNIQUE,
  senha_hash  TEXT    NOT NULL
);

CREATE TABLE medications (
  med_id          INTEGER PRIMARY KEY AUTOINCREMENT,
  nome_generico   TEXT    NOT NULL,
  dosagem         TEXT,
  forma           TEXT
);

CREATE TABLE user_meds (
  user_med_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id          INTEGER NOT NULL,
  med_id           INTEGER NOT NULL,
  quantidade_atual REAL    NOT NULL,
  unidade          TEXT    NOT NULL,
  data_inicio      DATE    NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (med_id)  REFERENCES medications(med_id)
);

CREATE TABLE schedules (
  sched_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  user_med_id  INTEGER NOT NULL,
  hora         TEXT    NOT NULL,       -- formato HH:MM
  dias_semana  TEXT    NOT NULL,       -- ex: "1,3,5"
  dose         REAL    NOT NULL,
  FOREIGN KEY (user_med_id) REFERENCES user_meds(user_med_id)
);

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
