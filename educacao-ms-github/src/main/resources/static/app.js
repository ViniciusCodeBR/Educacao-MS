// O navegador consulta a API Java; as credenciais ficam no servidor.
const elemento = id => document.getElementById(id);
const numero = valor => new Intl.NumberFormat('pt-BR').format(valor);
const percentual = (valor, total) => total ? (100 * valor / total).toLocaleString('pt-BR', {maximumFractionDigits: 2}) + '%' : 'Sem base';
let registros = [];
let pagina = 1;
const tamanhoPagina = 20;

function ocupado(valor) {
  ['municipio','ano','consultar','limpar'].forEach(id => elemento(id).disabled = valor);
  elemento('filtros').setAttribute('aria-busy', String(valor));
}
async function buscar(url) {
  const resposta = await fetch(url);
  if (!resposta.ok) {
    const erro = await resposta.json().catch(() => ({}));
    throw new Error(erro.mensagem || 'Não foi possível carregar a consulta. Tente novamente.');
  }
  return resposta.json();
}
function erro(mensagem) {
  elemento('status').textContent = mensagem;
  elemento('status').className = 'erro';
  elemento('resultados').hidden = true;
  elemento('tentar').hidden = false;
}
async function iniciar() {
  ocupado(true); elemento('tentar').hidden = true;
  try {
    const filtros = await buscar('/api/filtros');
    for (const id of ['municipio','ano']) while (elemento(id).options.length > 1) elemento(id).remove(1);
    filtros.municipios.forEach(m => elemento('municipio').add(new Option(m,m)));
    filtros.anos.forEach(a => elemento('ano').add(new Option(a,a)));
    // Começa com o ano mais recente disponível; a página avisa sobre sua consolidação.
    if (filtros.anos.length) elemento('ano').value = String(filtros.anos.at(-1));
    await consultar();
  } catch (e) { erro(e.message); }
  finally { ocupado(false); }
}
async function consultar() {
  ocupado(true); elemento('status').className = ''; elemento('status').textContent = 'Consultando dados...';
  elemento('tentar').hidden = true;
  elemento('resultados').hidden = true;
  try {
    const parametros = new URLSearchParams();
    const municipio = elemento('municipio').value, ano = elemento('ano').value;
    if (municipio) parametros.set('municipio',municipio);
    if (ano) parametros.set('ano',ano);
    const dados = await buscar('/api/dados?' + parametros);
    for (const id of ['matriculas','aprovados','reprovados','abandono']) elemento(id).textContent = numero(dados.resumo[id]);
    elemento('taxa-aprovados').textContent = percentual(dados.resumo.aprovados,dados.resumo.matriculas) + ' das matrículas';
    elemento('taxa-abandono').textContent = percentual(dados.resumo.abandono,dados.resumo.matriculas) + ' das matrículas';
    elemento('recorte').textContent = (municipio || 'Todos os municípios') + ' · ' + (ano || 'Todos os anos — soma de registros anuais');
    registros = dados.registros; pagina = 1; tabela(); grafico(dados.historico,ano);
    elemento('status').textContent = registros.length ? 'Consulta concluída. ' + numero(registros.length) + ' registros encontrados.' : 'Nenhum registro encontrado para os filtros selecionados.';
    elemento('resultados').hidden = false;
  } catch (e) { erro(e.message); }
  finally { ocupado(false); }
}
function tabela() {
  const corpo = elemento('linhas'); corpo.replaceChildren();
  const totalPaginas = Math.max(1,Math.ceil(registros.length/tamanhoPagina));
  const inicio = (pagina-1)*tamanhoPagina;
  for (const r of registros.slice(inicio,inicio+tamanhoPagina)) {
    const tr = document.createElement('tr');
    for (const valor of [r.ano,r.municipio,r.escola,numero(r.matriculas),numero(r.aprovados),numero(r.reprovados),numero(r.abandono),numero(r.cursando)]) {
      const td = document.createElement('td'); td.textContent = valor; tr.append(td);
    }
    corpo.append(tr);
  }
  if (!registros.length) { const tr = corpo.insertRow(); const td = tr.insertCell(); td.colSpan = 8; td.textContent = 'Nenhum registro encontrado.'; }
  elemento('total-linhas').textContent = registros.length ? `Mostrando ${inicio+1} a ${Math.min(inicio+tamanhoPagina,registros.length)} de ${numero(registros.length)} registros.` : '0 registros.';
  elemento('pagina').textContent = `Página ${pagina} de ${totalPaginas}`;
  elemento('anterior').disabled = pagina <= 1; elemento('proxima').disabled = pagina >= totalPaginas;
}
function grafico(historico,selecionado) {
  const area = elemento('grafico'); area.replaceChildren();
  if (!historico.length) { area.textContent = 'Sem histórico para este município.'; return; }
  const porAno = new Map(historico.map(r => [r.ano,r]));
  for (let ano = historico[0].ano; ano <= historico.at(-1).ano; ano++) {
    const linha = document.createElement('div'); linha.className = 'ano-grafico';
    const label = document.createElement('span'); label.textContent = ano; linha.append(label);
    const r = porAno.get(ano);
    if (!r) { linha.classList.add('ano-ausente'); const aviso = document.createElement('span'); aviso.textContent = 'Sem arquivo disponível'; linha.append(aviso); area.append(linha); continue; }
    if (String(ano) === selecionado) linha.classList.add('selecionado');
    const barras = document.createElement('div'); barras.className = 'barras';
    for (const [campo,classe] of [['aprovados','azul'],['abandono','laranja']]) {
      const barra = document.createElement('div'); barra.className = 'barra ' + classe;
      barra.style.width = (r.matriculas ? 100*r[campo]/r.matriculas : 0) + '%';
      barra.title = `${ano} — ${campo}: ${numero(r[campo])} (${percentual(r[campo],r.matriculas)})`; barras.append(barra);
    }
    const valores = document.createElement('span'); valores.className = 'valores';
    valores.textContent = percentual(r.aprovados,r.matriculas) + ' / ' + percentual(r.abandono,r.matriculas);
    linha.append(barras,valores); area.append(linha);
  }
}
elemento('filtros').addEventListener('submit', e => { e.preventDefault(); consultar(); });
elemento('limpar').addEventListener('click', () => { elemento('municipio').value = ''; elemento('ano').value = ''; consultar(); });
elemento('anterior').addEventListener('click', () => { pagina--; tabela(); });
elemento('proxima').addEventListener('click', () => { pagina++; tabela(); });
elemento('tentar').addEventListener('click', iniciar);
iniciar();
