# Análise histórica de matrículas da rede pública de Mato Grosso do Sul com Python, PostgreSQL e Java

**Rascunho técnico para adaptação ao modelo SBC.** Preencher autores, instituição, e-mail, disciplina e evidências reais de uso pelo grupo. A redação descreve o protótipo produzido; não substitui a revisão e o relato pessoal dos integrantes.

## Resumo

Este trabalho apresenta um protótipo para organização e consulta de dados educacionais públicos de Mato Grosso do Sul, em conexão com a ODS 4. A solução utiliza Python para leitura e validação de arquivos CSV, PostgreSQL para persistência relacional e Java para uma interface web de consulta com filtros e visualização histórica. Foram disponibilizados oito arquivos, referentes a 2018–2024 e 2026, totalizando 3.703 registros. A ausência de 2025 é tratada como lacuna da série. O sistema apresenta contagens e percentuais descritivos de aprovação e abandono sobre matrículas, sem equipará-los às taxas oficiais de rendimento escolar.

## 1. Introdução

Dados abertos podem apoiar a compreensão da distribuição de matrículas e das situações escolares. Contudo, arquivos separados por ano dificultam comparações e consultas para usuários sem familiaridade com processamento de dados. O objetivo do protótipo é integrar as informações fornecidas pelo portal estadual, oferecendo filtros por município e ano e uma visualização histórica que explicite suas limitações.

O vínculo com a ODS 4 está no apoio à consulta e à análise de informações educacionais; o sistema, por si só, não comprova melhora da qualidade da educação.

## 2. Dados e metodologia

Foram usados os arquivos de matrículas por unidade escolar fornecidos pelo grupo, relativos a 2018, 2019, 2020, 2021, 2022, 2023, 2024 e 2026. Cada registro identifica um município, uma unidade escolar, um ano e quantidades de matrículas em diferentes situações. A versão da base é registrada por hash SHA-256, nome de arquivo e ano.

A validação verifica nomes, campos obrigatórios, valores inteiros não negativos, ano do arquivo e duplicidade da combinação município/escola/ano. Também confere se o total corresponde à soma das entradas e à soma das situações. Registros inconsistentes interrompem a geração da carga, com identificação de arquivo e linha.

As classes Escola e RegistroAnual representam os dados na importação. Listas armazenam os registros; conjuntos auxiliam a identificação de chaves duplicadas. O banco separa municípios, escolas, fontes e registros anuais, com chaves estrangeiras, restrições de unicidade e de consistência. Uma transação engloba a carga e atualizações por chave evitam duplicação em reexecuções.

## 3. Implementação

O fluxo é CSV → importador Python → script SQL → PostgreSQL → aplicação Java. A geração de SQL evita uma dependência Python adicional de acesso ao banco; a aplicação Java executa a carga inicial no PostgreSQL hospedado quando o esquema ainda não existe. A aplicação Java usa Spring Boot e JdbcTemplate para consultas parametrizadas. Uma API HTTP fornece as opções de filtro e os resultados. A página HTML usa CSS simples e JavaScript para consultar a API, atualizar indicadores, desenhar barras e paginar os registros em grupos de 20. Os recursos da interface são servidos pela mesma hospedagem. O acesso ao site exige navegador e internet, sem instalação de programas pelo visitante.

O projeto foi preparado para acesso pelo endereço HTTPS gerado pelo Render, com aplicação Java e PostgreSQL hospedados. A publicação e a URL definitiva devem ser registradas após a confirmação do deploy. O filtro de município restringe o histórico. O filtro de ano restringe indicadores e tabela, mantendo no gráfico a série histórica com destaque para a seleção. Os percentuais exibidos são calculados por 100 vezes a soma da situação dividida pela soma de matrículas. A base zero é identificada explicitamente, e o gráfico de barras indica explicitamente a ausência de 2025, sem inventar valores para esse ano.

## 4. Resultados e verificação

A leitura dos oito arquivos produziu 3.703 registros. As quantidades por ano são 485, 475, 441, 442, 472, 467, 461 e 460, respectivamente. O relatório validacao.json contém os totais por campo e hashes dos dados. A compilação, a carga e os testes de integração efetivamente executados estão descritos em VERIFICACAO.md.

**Complementar pelo grupo:** inserir capturas da aplicação executada; explicar um recorte municipal; comparar os valores consultados com o CSV; registrar as dificuldades efetivamente vivenciadas e a contribuição de cada integrante. Não atribuir testes, reuniões ou avaliações de usuários que não ocorreram.

## 5. Limitações

O portal consultado não fornece 2025 nessa coleção. Além disso, o recurso de 2026 foi atualizado em março daquele ano e pode representar um retrato parcial. Aprovação e abandono sobre matrículas são indicadores descritivos do protótipo, não taxas oficiais do INEP. Cancelamento e transferência não são considerados abandono. Os nomes de escolas não constituem identificadores estáveis: renomeações podem fragmentar trajetórias. Contagens de anos diferentes também podem refletir alterações na rede e não autorizam inferências causais sobre a qualidade do ensino.

## 6. Considerações finais

O protótipo articula orientação a objetos, estruturas de dados, persistência relacional e visualização para consulta de uma série histórica pública. Como continuidade, podem ser estudadas a conciliação por código escolar estável, a inclusão de novas versões da base e a adoção de indicadores oficiais mediante metodologia e fontes adequadas.

## Referências para formatar no template

Governo do Estado de Mato Grosso do Sul. Matrículas por Unidade Escolar. https://www.dados.ms.gov.br/dataset/matriculas-por-unidade-escolar. Consulta: 17 out. 2026.

PostgreSQL Global Development Group. PostgreSQL JDBC Driver: Documentation. https://jdbc.postgresql.org/documentation/. Consulta: 17 out. 2026.

**Antes da entrega:** transferir este texto para o template SBC indicado pelo professor e revisar referências, autores, paginação e todos os resultados. O arquivo Markdown não é uma versão final diagramada no padrão SBC.
