"""Verificação do site publicado: defina URL_SITE com o endereço HTTPS real."""
import csv
import json
import unittest
import os
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode, urlparse
from urllib.error import HTTPError

BASE = os.environ.get('URL_SITE','').rstrip('/')
if not BASE or urlparse(BASE).scheme != 'https' or not urlparse(BASE).hostname:
    raise SystemExit('Defina URL_SITE com o endereço HTTPS do site publicado para executar a verificação.')
ROOT = Path(__file__).resolve().parents[1]

def buscar(caminho):
    with urlopen(BASE+caminho, timeout=20) as resposta:
        return json.load(resposta)

class ApiTest(unittest.TestCase):
    def test_anos_disponiveis(self):
        self.assertEqual(buscar('/api/filtros')['anos'],[2018,2019,2020,2021,2022,2023,2024,2026])

    def test_todos_os_totais_conferem_com_csv(self):
        for ano in [2018,2019,2020,2021,2022,2023,2024,2026]:
            with self.subTest(ano=ano):
                with (ROOT/f'dados/matriculas-por-unidade-escolar-{ano}.csv').open(encoding='utf-8-sig') as f:
                    linhas=list(csv.DictReader(f))
                resposta=buscar('/api/dados?ano='+str(ano))
                self.assertEqual(len(resposta['registros']),len(linhas))
                for campo,csv_campo in [('matriculas','MatriculasTotal'),('aprovados','Aprovados'),('reprovados','Reprovados'),('abandono','Abandono'),('cursando','Cursando')]:
                    self.assertEqual(resposta['resumo'][campo],sum(int(r[csv_campo]) for r in linhas))

    def test_filtros_combinados(self):
        resposta=buscar('/api/dados?'+urlencode({'municipio':'Campo Grande','ano':2018}))
        self.assertEqual(len(resposta['registros']),95)
        self.assertEqual(resposta['resumo']['matriculas'],79057)
        self.assertTrue(all(r['municipio']=='Campo Grande' and r['ano']==2018 for r in resposta['registros']))
        self.assertEqual(len(resposta['historico']),8)

    def test_total_sem_filtro(self):
        self.assertEqual(len(buscar('/api/dados')['registros']),3703)

    def test_parametro_sql_nao_altera_consulta(self):
        resposta=buscar('/api/dados?'+urlencode({'municipio':"' OR 1=1 --"}))
        self.assertEqual(resposta['registros'],[])

    def test_ano_ausente_rejeitado(self):
        with self.assertRaises(HTTPError) as erro:
            buscar('/api/dados?ano=2025')
        self.assertEqual(erro.exception.code,400)

if __name__=='__main__': unittest.main()
