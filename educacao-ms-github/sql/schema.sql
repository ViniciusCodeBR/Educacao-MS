CREATE TABLE IF NOT EXISTS municipio (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, nome text NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS escola (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 municipio_id bigint NOT NULL REFERENCES municipio(id), nome text NOT NULL,
 UNIQUE(municipio_id,nome)
);
CREATE TABLE IF NOT EXISTS fonte (
 ano integer PRIMARY KEY, arquivo text NOT NULL, sha256 text NOT NULL,
 importado_em timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS registro_anual (
 escola_id bigint NOT NULL REFERENCES escola(id), ano integer NOT NULL REFERENCES fonte(ano),
 origem_id integer NOT NULL,
 matriculas_total integer NOT NULL CHECK(matriculas_total>=0),
 matricula_inicial integer NOT NULL CHECK(matricula_inicial>=0),
 matricula_apos_censo integer NOT NULL CHECK(matricula_apos_censo>=0),
 transferidos integer NOT NULL CHECK(transferidos>=0), cancelados integer NOT NULL CHECK(cancelados>=0),
 falecidos integer NOT NULL CHECK(falecidos>=0), abandono integer NOT NULL CHECK(abandono>=0),
 aprovados integer NOT NULL CHECK(aprovados>=0), reprovados integer NOT NULL CHECK(reprovados>=0),
 cursando integer NOT NULL CHECK(cursando>=0), outras_situacoes integer NOT NULL CHECK(outras_situacoes>=0),
 PRIMARY KEY(escola_id,ano),
 CHECK(matriculas_total=matricula_inicial+matricula_apos_censo),
 CHECK(matriculas_total=transferidos+cancelados+falecidos+abandono+aprovados+reprovados+cursando+outras_situacoes)
);
CREATE INDEX IF NOT EXISTS idx_registro_ano ON registro_anual(ano);
CREATE OR REPLACE VIEW dados_escolares AS
 SELECT r.*,e.nome AS escola,m.nome AS municipio FROM registro_anual r
 JOIN escola e ON e.id=r.escola_id JOIN municipio m ON m.id=e.municipio_id;
