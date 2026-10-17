# Matrículas escolares em MS — DAC

Site acadêmico para consultar matrículas da rede pública de Mato Grosso do Sul. O acesso é pelo **endereço HTTPS do site publicado no Render**, em qualquer navegador com conexão à internet.

**O link definitivo será informado após a publicação.** O código no GitHub não é o endereço de acesso ao sistema. O computador de quem desenvolveu o projeto pode permanecer desligado; a aplicação e o banco funcionam na hospedagem.

## Como acessar e apresentar

1. Abra o link HTTPS fornecido pelo Render após a publicação.
2. Selecione município e ano e clique em **Consultar**.
3. Confira os indicadores, o gráfico histórico e a tabela de escolas.
4. Use **Anterior** e **Próxima** para navegar na tabela.
5. Clique em **Limpar filtros** para consultar todos os registros.

Para demonstrar resultados registrados de aprovação e abandono, use Campo Grande em 2018: 95 registros, 79.057 matrículas, 48.852 aprovados e 3.241 abandonos. O gráfico mantém o histórico do município, destacando o ano selecionado.

**Na faculdade, é necessário apenas um navegador e internet.** Abra o link com antecedência e teste o acesso em outro dispositivo. Os visitantes não precisam instalar Java, Python, PostgreSQL nem baixar o projeto.

## Publicação

Envie o conteúdo deste projeto para a raiz do repositório GitHub. `pom.xml`, `Dockerfile`, `render.yaml`, `src/` e `gerados/` devem aparecer diretamente na raiz. Depois, siga [PUBLICAR.md](PUBLICAR.md) para criar a aplicação e o banco no Render.

O Render compila o código Java pelo Dockerfile. Na primeira inicialização, a aplicação carrega o SQL gerado em um banco PostgreSQL sem o esquema do projeto. Se a tabela `fonte` já existir, a carga inicial é ignorada. Não envie senhas ao GitHub.

O plano descrito em `render.yaml` é gratuito e temporário: confira as condições da conta antes de criar os recursos. Consulte PUBLICAR.md para os limites e a preparação da apresentação.

## Tecnologias

| Tecnologia | Responsabilidade |
|---|---|
| Python | Ler e validar os CSVs, gerar o SQL e o relatório de validação |
| PostgreSQL hospedado | Armazenar municípios, escolas e registros anuais |
| Java / Spring Boot | Consultar o banco e fornecer a API do site |
| HTML, CSS e JavaScript | Exibir filtros, indicadores, gráfico e tabela no navegador |
| GitHub | Versionar o código e fornecer a origem para o deploy |
| Render | Executar o site e hospedar o banco |

O Python participa da preparação dos dados, sem precisar executar no navegador ou em cada consulta. O SQL validado já está incluído para a carga automática na hospedagem.

## Arquivos

- `src/main/java/`: classes Java, consultas parametrizadas, API e carga inicial.
- `src/main/resources/static/`: página HTML, estilos e JavaScript.
- `src/main/resources/application.properties`: configuração do servidor por variáveis de ambiente.
- `python/importar.py`: importador com classes Escola e RegistroAnual, listas e conjuntos.
- `sql/schema.sql`: modelo relacional e restrições de integridade.
- `dados/`: oito CSVs originais.
- `gerados/carga.sql`: carga transacional usada pela hospedagem.
- `gerados/validacao.json`: totais e hashes SHA-256 dos arquivos.
- `testes/test_api.py`: verificação por HTTPS do site publicado, configurado por `URL_SITE`.
- `artigo/relato.md`: rascunho para revisão e formatação no modelo SBC.
- `VERIFICACAO.md`: verificações realizadas e pendências.

## Configuração da hospedagem

O Blueprint fornece `PGHOST`, `PGDATABASE`, `DAC_DB_USER` e `DAC_DB_PASSWORD` a partir do PostgreSQL hospedado. `PGPORT` aceita a porta do banco e usa 5432 por padrão. `PORT` é a porta interna determinada pela hospedagem. A aplicação recebe conexões pela rede do contêiner; o público usa o endereço HTTPS do Render.

As credenciais são obrigatórias e fornecidas como variáveis de ambiente. Não há banco de destino pré-configurado no computador do usuário. `DAC_IMPORTAR_INICIAL` controla a carga automática e fica habilitado no Blueprint.

## Cuidados com os dados

São 3.703 registros entre 2018–2024 e 2026. Não há arquivo de 2025: a ausência é indicada sem criar valores. Os percentuais são `100 × soma da situação / soma das matrículas`, não taxas oficiais de rendimento. Transferência e cancelamento não são abandono; somar anos não representa alunos únicos.

A base fornecida tem 3.484 aprovados em 2024 e zero em 2026, além de abandono zero em vários anos. Esses valores não comprovam ausência real de eventos. É preciso confirmar a consolidação antes de concluir melhora ou piora do ensino. Nomes das escolas podem mudar e não há código escolar estável no CSV.

## Artigo e divisão do grupo

Cada integrante deve estudar e explicar sua parte: importação Python; banco e consultas; página web; integração, testes e organização do artigo com contribuição de todos. O relato ainda precisa dos autores, instituição, evidências da apresentação e formatação SBC.

Fonte dos dados: https://www.dados.ms.gov.br/dataset/matriculas-por-unidade-escolar

Template indicado: https://pt.overleaf.com/read/fkbgnmdwztrr#fa8e5b
