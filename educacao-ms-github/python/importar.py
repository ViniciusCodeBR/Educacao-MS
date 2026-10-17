"""Valida CSVs oficiais e produz uma carga transacional para PostgreSQL."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPOS = ('MatriculasTotal', 'MatriculaInicial', 'MatriculaAposCenso', 'Transferidos',
          'Cancelados', 'Falecido', 'Abandono', 'Aprovados', 'Reprovados', 'Cursando', 'OutrasSituacoes')
COLUNAS = ('matriculas_total', 'matricula_inicial', 'matricula_apos_censo', 'transferidos',
           'cancelados', 'falecidos', 'abandono', 'aprovados', 'reprovados', 'cursando', 'outras_situacoes')

@dataclass(frozen=True)
class Escola:
    municipio: str
    nome: str

@dataclass(frozen=True)
class RegistroAnual:
    escola: Escola
    ano: int
    valores: tuple[int, ...]
    origem_id: int

def ler_csv(path: Path) -> list[RegistroAnual]:
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        obrigatorios = {'_id', 'AnoReferencia', 'NomeMunicipio', 'NomeUnidadeEscolar', *CAMPOS}
        if not obrigatorios.issubset(reader.fieldnames or []):
            raise ValueError(f'{path.name}: colunas obrigatórias ausentes')
        result, vistos = [], set()
        for linha, r in enumerate(reader, 2):
            try:
                e = Escola(r['NomeMunicipio'].strip(), r['NomeUnidadeEscolar'].strip())
                ano = int(r['AnoReferencia'])
                valores = tuple(int(r[k]) for k in CAMPOS)
                registro = RegistroAnual(e, ano, valores, int(r['_id']))
                if not e.municipio or not e.nome or any(v < 0 for v in valores):
                    raise ValueError('nome vazio ou quantidade negativa')
                if ano != int(path.stem.rsplit('-', 1)[1]):
                    raise ValueError('ano diferente do nome do arquivo')
                if valores[0] != valores[1] + valores[2] or valores[0] != sum(valores[3:]):
                    raise ValueError('total não corresponde à soma das situações ou entradas')
                chave = (e, ano)
                if chave in vistos:
                    raise ValueError('escola/ano duplicado')
                vistos.add(chave)
                result.append(registro)
            except (ValueError, TypeError) as exc:
                raise ValueError(f'{path.name}, linha {linha}: {exc}') from exc
    if not result:
        raise ValueError(f'{path.name}: arquivo vazio')
    return result

def literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"

def gerar(data: Path, destino: Path) -> dict:
    arquivos = sorted(data.glob('matriculas-por-unidade-escolar-*.csv'))
    if not arquivos:
        raise ValueError('Nenhum CSV encontrado')
    sql = ['BEGIN;', 'SET standard_conforming_strings = on;',
           (ROOT / 'sql/schema.sql').read_text(encoding='utf-8')]
    resumo = {'arquivos': [], 'anos_ausentes': [], 'total_registros': 0}
    anos = set()
    for path in arquivos:
        registros = ler_csv(path)
        ano = registros[0].ano
        if ano in anos:
            raise ValueError(f'Mais de um arquivo para {ano}')
        anos.add(ano)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        sql.append(f"INSERT INTO fonte(ano,arquivo,sha256) VALUES ({ano},{literal(path.name)},{literal(digest)}) ON CONFLICT(ano) DO UPDATE SET arquivo=excluded.arquivo,sha256=excluded.sha256,importado_em=now();")
        for r in registros:
            m, e = literal(r.escola.municipio), literal(r.escola.nome)
            sql.append(f'INSERT INTO municipio(nome) VALUES ({m}) ON CONFLICT DO NOTHING;')
            sql.append(f'INSERT INTO escola(municipio_id,nome) SELECT id,{e} FROM municipio WHERE nome={m} ON CONFLICT DO NOTHING;')
            valores = ','.join(map(str, r.valores))
            atualiza = ','.join(f'{c}=excluded.{c}' for c in COLUNAS)
            sql.append(f"INSERT INTO registro_anual(escola_id,ano,origem_id,{','.join(COLUNAS)}) SELECT e.id,{ano},{r.origem_id},{valores} FROM escola e JOIN municipio m ON m.id=e.municipio_id WHERE m.nome={m} AND e.nome={e} ON CONFLICT(escola_id,ano) DO UPDATE SET origem_id=excluded.origem_id,{atualiza};")
        totais = {k: sum(r.valores[i] for r in registros) for i,k in enumerate(CAMPOS)}
        resumo['arquivos'].append({'ano': ano, 'registros': len(registros), 'sha256': digest, 'totais': totais})
        resumo['total_registros'] += len(registros)
    resumo['anos_ausentes'] = sorted(set(range(min(anos), max(anos)+1))-anos)
    sql.append('COMMIT;')
    destino.mkdir(parents=True, exist_ok=True)
    (destino / 'carga.sql').write_text('\n'.join(sql), encoding='utf-8')
    (destino / 'validacao.json').write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding='utf-8')
    return resumo

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dados', type=Path, default=ROOT/'dados')
    parser.add_argument('--saida', type=Path, default=ROOT/'gerados')
    args = parser.parse_args()
    try:
        resumo = gerar(args.dados, args.saida)
        print(f"Validação concluída: {resumo['total_registros']} registros. Anos ausentes: {resumo['anos_ausentes']}")
        print(f'Carga SQL: {args.saida / "carga.sql"}')
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Erro: {exc}\n')
