# Verificação do projeto

## Verificações já realizadas em ambiente de testes

- Compilação Java/Maven, com código compatível com Java 17.
- Validação dos oito CSVs: 3.703 registros.
- Carga inicial automática em PostgreSQL vazio, usando variáveis de ambiente.
- Seis testes de API: anos disponíveis, totais dos oito arquivos, filtros combinados, total sem filtro, parâmetros de consulta e rejeição de ano ausente.
- Conferência no navegador de filtros, paginação e limpeza dos filtros.
- Campo Grande/2018: 95 registros, 79.057 matrículas, 48.852 aprovados e 3.241 abandonos.

Essas verificações descrevem o ambiente de testes. Não comprovam publicação ou disponibilidade pública. A imagem Docker e o endereço HTTPS precisam ser verificados após o deploy na conta de hospedagem.

## Conferência após publicar

1. Abra a URL HTTPS exibida pelo Render em outro dispositivo com internet.
2. Consulte Campo Grande/2018 e confira os totais acima.
3. Teste a paginação e a limpeza dos filtros.
4. Confira se 2025 aparece como ausente no gráfico.
5. Registre a URL real e capturas das telas para a apresentação.

## Teste automatizado por HTTPS

A ferramenta `testes/test_api.py` consulta exclusivamente o endereço HTTPS informado na variável `URL_SITE`. O responsável técnico deve configurar essa variável com o link real do serviço publicado antes de executar o teste com Python. Não há endereço de acesso predefinido no teste.

O visitante do site e o computador da faculdade não precisam executar esses testes ou instalar Python. A verificação automatizada é uma tarefa de manutenção do projeto.

O artigo ainda exige revisão, identificação dos autores e formatação SBC. Os dados não tiveram sua consolidação confirmada junto à SED.
