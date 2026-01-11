-- ==========================
-- TABELA DE CONCURSOS
-- ==========================
CREATE TABLE IF NOT EXISTS concursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concurso INTEGER UNIQUE NOT NULL,
    dezenas TEXT NOT NULL,
    data TEXT
);

CREATE INDEX IF NOT EXISTS idx_concurso_numero
ON concursos(concurso);

-- ==========================
-- TENTATIVAS DA IA
-- ==========================
CREATE TABLE IF NOT EXISTS tentativas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concurso INTEGER NOT NULL,
    tentativa INTEGER NOT NULL,
    dezenas TEXT NOT NULL,
    acertos INTEGER NOT NULL,
    score REAL NOT NULL,
    tempo_exec REAL,
    timestamp TEXT
);

CREATE INDEX IF NOT EXISTS idx_tentativas_concurso
ON tentativas(concurso);

CREATE INDEX IF NOT EXISTS idx_tentativas_acertos
ON tentativas(acertos);

-- ==========================
-- CHECKPOINT (RECUPERAÇÃO)
-- ==========================
CREATE TABLE IF NOT EXISTS checkpoint (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    concurso_atual INTEGER,
    tentativa_atual INTEGER,
    inicio_timestamp TEXT
);
