# Publicar e acessar o site pela internet

## 1. Atualizar o GitHub

Envie o conteúdo da pasta do projeto para a raiz do repositório, sem enviar o ZIP como um arquivo único. O GitHub deve mostrar `pom.xml`, `Dockerfile`, `render.yaml`, `src/` e `gerados/carga.sql` diretamente na raiz. Não inclua credenciais.

Se estiver substituindo uma versão antiga, remova do repositório `iniciar-site.cmd`, `iniciar-site.ps1`, `aplicacao/` e `target/`, caso existam. São arquivos da distribuição anterior e não fazem parte deste pacote. Substitua também os arquivos dentro de `src/`, `testes/` e `artigo/`, além dos documentos da raiz; não atualize apenas o README.

## 2. Hospedar no Render

1. Acesse uma conta Render e conecte o repositório GitHub.
2. Crie um Blueprint usando o `render.yaml` do projeto.
3. Confira os planos propostos. O arquivo solicita um serviço web e um PostgreSQL no plano gratuito; revise se houver indicação de cobrança.
4. Aguarde a compilação e a carga inicial automática dos 3.703 registros.
5. Confira se o serviço está ativo e copie o endereço HTTPS mostrado no painel.
6. Abra o endereço em outro dispositivo e teste Campo Grande/2018: 95 registros e 79.057 matrículas.
7. Registre a URL real no início do README do repositório para o grupo e o professor.

O endereço é gerado pela hospedagem. Não há uma URL pública confirmada neste pacote. Não é necessário comprar domínio para usar o endereço fornecido pelo Render.

## 3. Apresentar na faculdade

Abra a URL publicada em um navegador com internet. As consultas são executadas na hospedagem e o banco fica na nuvem. Não é necessário manter o computador do desenvolvedor ligado nem instalar os programas na faculdade.

Abra o site com antecedência, confira a conexão da sala e tenha capturas das telas como apoio à apresentação.

## Infraestrutura

O Dockerfile compila o código no servidor. O Blueprint conecta a aplicação ao PostgreSQL pela rede interna e injeta as credenciais. O banco tem acesso externo bloqueado no Blueprint. O health check `/api/filtros` verifica a consulta ao banco. Use uma única instância durante a carga inicial.

## Limites do plano gratuito

Conforme a documentação consultada em 17/10/2026, o serviço web gratuito suspende após 15 minutos sem acessos e pode demorar no primeiro acesso seguinte. O PostgreSQL gratuito expira 30 dias após a criação. Essa configuração atende a uma demonstração temporária; confira os prazos da conta antes da apresentação. Não foi contratado plano pago.

Para manter o site além do prazo do banco, será necessário escolher uma oferta apropriada antes da expiração.

## Estado da publicação

O projeto está preparado para publicação. A compilação e a importação foram verificadas em ambiente de testes. A publicação no Render e a verificação do endereço HTTPS ainda dependem de acesso à conta de hospedagem. Arquivos de configuração não significam que o deploy já ocorreu.

Referências: https://render.com/docs/docker · https://render.com/docs/blueprint-spec · https://render.com/docs/free
