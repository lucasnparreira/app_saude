CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    number_id INTEGER NOT NULL,
    date DATE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,  -- Adicionamos a coluna user_id
    weight REAL NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)  -- Chave estrangeira para associar com a tabela users
);

CREATE TABLE IF NOT EXISTS medidas_corporais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE NOT NULL,
    altura REAL NOT NULL,
    peso REAL NOT NULL,
    circunferencia_cintura REAL NOT NULL,
    circunferencia_quadril REAL NOT NULL,
    circunferencia_braco REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);