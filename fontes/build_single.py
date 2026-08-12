#!/usr/bin/env python3
"""Gera uma apostila HTML de arquivo único com as 15 aulas navegáveis."""
import html
import re
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

import build_html as B  # reaproveita CSS, AULAS, enfeitar()

BASE = Path("/root/fds/material")
SRC = BASE / "aulas"
OUT = BASE / "html" / "apostila-completa.html"

md = markdown.Markdown(
    extensions=["fenced_code", "codehilite", "tables", "toc", "attr_list", "sane_lists", "md_in_html"],
    extension_configs={
        "codehilite": {"guess_lang": False, "css_class": "codehilite"},
        "toc": {"anchorlink": False, "permalink": "", "toc_depth": "2-3"},
    },
)

arquivos = sorted(SRC.glob("aula-*.md"))
secoes, cartoes, menu = [], [], []
grupo = None

for num, data, unid, tit in B.AULAS:
    caminho = next(p for p in arquivos if p.name.startswith(f"aula-{num}-"))
    md.reset()
    corpo = md.convert(caminho.read_text(encoding="utf-8"))
    corpo = B.enfeitar(corpo)
    corpo = re.sub(r"<h1[^>]*>[\s\S]*?</h1>", "", corpo, count=1)
    # prefixa ids para não colidir entre aulas
    corpo = re.sub(r'<h([23]) id="([^"]+)"', lambda m: f'<h{m.group(1)} id="a{num}-{m.group(2)}"', corpo)

    ucls = {"Unidade 1": "u1", "Unidade 2": "u2", "Unidade 3": "u3"}[unid]
    av = B.AVALIACOES.get(num)
    tags = (f'<span class="tag {ucls}">{unid}</span><span class="tag">{data}</span>'
            f'<span class="tag">3 aulas de 50 min + 1 h EAD</span>')
    if av:
        tags += f'<span class="tag av">Entrega da Avaliação {av}</span>'

    sub = []
    for niv, ident, txt in re.findall(r'<h([23]) id="([^"]+)">(.*?)</h[23]>', corpo):
        limpo = re.sub(r"<[^>]+>", "", txt).replace("¶", "").strip()
        if limpo:
            sub.append(f'<a class="{"n3" if niv=="3" else ""}" href="#{ident}">{html.escape(limpo)}</a>')

    secoes.append(
        f'<section class="aula" id="aula-{num}" data-aula="{num}" data-sumario=\'{len(sub)}\'>'
        f'<div class="cabecalho"><div class="tags">{tags}</div>'
        f'<h1>Aula {num} — {html.escape(tit)}</h1>'
        '<div class="sub">FACET-SNP-310 · Frameworks Modernos para Desenvolvimento de Sistemas · '
        'UNEMAT/Sinop · Prof. Ivan Luiz Pedroso Pires</div></div>'
        + corpo
        + '<div class="toc-dados oculto">' + "".join(sub) + "</div>"
        + "</section>"
    )

    if unid != grupo:
        grupo = unid
        menu.append(f'<li class="grupo">{unid}</li>')
    menu.append(
        f'<li><a href="#aula-{num}" data-ir="{num}">'
        f'<span class="num">{num}</span><span>{html.escape(tit)}</span></a></li>'
    )
    chave = f"{num} {data} {unid} {tit}".lower()
    cartoes.append(
        f'<a class="cartao {ucls}" href="#aula-{num}" data-ir="{num}" data-busca="{html.escape(chave)}">'
        f'<div class="meta"><span>Aula {num} · {unid}</span><span>{data}</span></div>'
        f'<div class="t">{html.escape(tit)}</div>'
        + (f'<span class="av">Entrega da Avaliação {av}</span>' if av else "")
        + "</a>"
    )

capa = f"""
<section class="aula" id="aula-00" data-aula="00">
<div class="hero">
  <h1>Frameworks Modernos para<br>Desenvolvimento de Sistemas</h1>
  <p>Material completo da disciplina FACET-SNP-310 — 15 aulas construindo, do zero ao deploy,
  uma aplicação full stack com Vue 3, Vuetify, Pinia, Express e banco de dados.</p>
</div>
<div class="stats">
  <div class="stat"><div class="n">15</div><div class="l">Aulas</div></div>
  <div class="stat"><div class="n">60h</div><div class="l">45h presenciais + 15h EAD</div></div>
  <div class="stat"><div class="n">3</div><div class="l">Unidades</div></div>
  <div class="stat"><div class="n">3</div><div class="l">Avaliações práticas</div></div>
</div>
<h2 id="c-aulas">Aulas</h2>
<div class="grade">{''.join(cartoes)}</div>
<h2 id="c-projeto">O projeto fio-condutor</h2>
<p>Todas as aulas constroem incrementalmente o <strong>UniEventos</strong>, plataforma de divulgação e
inscrição em eventos acadêmicos. O professor desenvolve o UniEventos em sala; cada estudante desenvolve um
<strong>projeto autoral</strong> com a mesma arquitetura e domínio diferente. As avaliações são sobre o projeto autoral.</p>
<h2 id="c-stack">Stack e versões</h2>
<div class="tabela-wrap"><table>
<thead><tr><th>Camada</th><th>Tecnologia</th><th>Versão</th></tr></thead>
<tbody>
<tr><td>Runtime</td><td>Node.js</td><td>22 LTS</td></tr>
<tr><td>Front-end</td><td>Vue</td><td>3.5</td></tr>
<tr><td>Build</td><td>Vite</td><td>8</td></tr>
<tr><td>UI</td><td>Vuetify</td><td>4</td></tr>
<tr><td>Rotas</td><td>Vue Router</td><td>5</td></tr>
<tr><td>Estado</td><td>Pinia</td><td>4</td></tr>
<tr><td>HTTP</td><td>Axios</td><td>1.19</td></tr>
<tr><td>Back-end</td><td>Express</td><td>5.2</td></tr>
<tr><td>Banco</td><td>MySQL 8 / Supabase (Postgres)</td><td>—</td></tr>
<tr><td>Autenticação</td><td>Firebase Auth</td><td>12</td></tr>
<tr><td>Documentação</td><td>Swagger / OpenAPI</td><td>3.0</td></tr>
</tbody></table></div>
<h2 id="c-avaliacao">Avaliação</h2>
<p>Média aritmética simples de três avaliações práticas individuais, entregues via SIGAA.
O exame final é uma prova teórica presencial sobre as três unidades.</p>
<div class="tabela-wrap"><table>
<thead><tr><th>Avaliação</th><th>Conteúdo</th><th>Prazo</th></tr></thead>
<tbody>
<tr><td>Avaliação 1</td><td>Vue 3 com CLI: estrutura, componentes, diretivas</td><td>31/08/2026</td></tr>
<tr><td>Avaliação 2</td><td>Vuetify, Vue Router, Axios e Pinia</td><td>05/10/2026</td></tr>
<tr><td>Avaliação 3</td><td>Back-end, banco de dados, autenticação e deploy</td><td>14/12/2026</td></tr>
</tbody></table></div>
<h2 id="c-uso">Como usar este material</h2>
<ul>
<li>Cada aula tem objetivos, teoria, passo a passo prático, laboratório em sala, tabela de erros comuns e uma atividade assíncrona de 1 hora.</li>
<li>Todos os blocos de código têm botão <strong>Copiar</strong>.</li>
<li>Atalhos de teclado: <code>j</code> próxima aula, <code>k</code> aula anterior, <code>/</code> busca, <code>Esc</code> volta ao índice.</li>
<li>Use o botão <strong>Tema</strong> para alternar entre claro e escuro. Ctrl+P imprime a aula aberta.</li>
</ul>
</section>
"""

JS = r"""
(function(){
  var raiz=document.documentElement;
  try{var s=localStorage.getItem('fds-tema'); if(s)raiz.setAttribute('data-tema',s)}catch(e){}
  var bt=document.getElementById('tema');
  function rot(){bt.textContent=raiz.getAttribute('data-tema')==='claro'?'● Escuro':'○ Claro'}
  bt.addEventListener('click',function(){
    var n=raiz.getAttribute('data-tema')==='claro'?'escuro':'claro';
    raiz.setAttribute('data-tema',n);
    try{localStorage.setItem('fds-tema',n)}catch(e){} rot();
  }); rot();

  var secoes=[].slice.call(document.querySelectorAll('.aula'));
  var ids=secoes.map(function(s){return s.dataset.aula});
  var toc=document.getElementById('toc');
  var atual='00';

  function abrir(num,semScroll){
    if(ids.indexOf(num)<0)num='00';
    atual=num;
    secoes.forEach(function(s){s.classList.toggle('oculto',s.dataset.aula!==num)});
    document.querySelectorAll('.lateral a').forEach(function(a){
      a.classList.toggle('ativo',a.dataset.ir===num);
    });
    var sec=document.getElementById('aula-'+num);
    var dados=sec.querySelector('.toc-dados');
    toc.innerHTML='<h4>'+(num==='00'?'Nesta página':'Nesta aula')+'</h4>'+
      (dados?dados.innerHTML:[].slice.call(sec.querySelectorAll('h2[id]')).map(function(h){
        return '<a href="#'+h.id+'">'+h.textContent.replace('¶','')+'</a>'}).join(''));
    montarNav(num);
    if(!semScroll)window.scrollTo(0,0);
    if(location.hash!=='#aula-'+num){history.replaceState(null,'','#aula-'+num)}
    ligarObservador(sec);
  }

  function montarNav(num){
    var old=document.getElementById('navpe'); if(old)old.remove();
    if(num==='00')return;
    var i=ids.indexOf(num);
    var h='<nav class="navpe" id="navpe">';
    if(i>1){var p=ids[i-1];h+='<a href="#aula-'+p+'" data-ir="'+p+'"><span class="rot">← Aula '+p+'</span><span class="tit">'+titulo(p)+'</span></a>'}
    else{h+='<a href="#aula-00" data-ir="00"><span class="rot">← Índice</span><span class="tit">Início</span></a>'}
    if(i<ids.length-1){var n=ids[i+1];h+='<a class="dir" href="#aula-'+n+'" data-ir="'+n+'"><span class="rot">Aula '+n+' →</span><span class="tit">'+titulo(n)+'</span></a>'}
    h+='</nav>';
    document.getElementById('aula-'+num).insertAdjacentHTML('beforeend',h);
  }
  function titulo(n){
    var a=document.querySelector('.lateral a[data-ir="'+n+'"]');
    return a?a.lastElementChild.textContent:'Aula '+n;
  }

  var obs=null;
  function ligarObservador(sec){
    if(obs)obs.disconnect();
    if(!('IntersectionObserver' in window))return;
    var links={};
    toc.querySelectorAll('a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
    obs=new IntersectionObserver(function(es){
      es.forEach(function(e){
        var a=links[e.target.id]; if(!a)return;
        if(e.isIntersecting){
          Object.keys(links).forEach(function(k){links[k].classList.remove('ativo')});
          a.classList.add('ativo');
        }
      });
    },{rootMargin:'-76px 0px -75% 0px'});
    sec.querySelectorAll('h2[id],h3[id]').forEach(function(h){obs.observe(h)});
  }

  document.addEventListener('click',function(e){
    var a=e.target.closest('a[data-ir]');
    if(a){e.preventDefault();abrir(a.dataset.ir);return}
    var t=e.target.closest('.copiar');
    if(t){
      var pre=t.closest('.bloco').querySelector('pre'), txt=pre.innerText;
      var ok=function(){t.textContent='Copiado';t.classList.add('ok');
        setTimeout(function(){t.textContent='Copiar';t.classList.remove('ok')},1600)};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok)}
      else{var x=document.createElement('textarea');x.value=txt;document.body.appendChild(x);x.select();
           document.execCommand('copy');x.remove();ok()}
    }
  });

  var pr=document.getElementById('progresso');
  window.addEventListener('scroll',function(){
    var h=document.documentElement.scrollHeight-window.innerHeight;
    pr.style.width=(h>0?(window.scrollY/h)*100:0)+'%';
  },{passive:true});

  var busca=document.getElementById('busca');
  busca.addEventListener('input',function(){
    var q=busca.value.toLowerCase().trim();
    if(q&&atual!=='00')abrir('00');
    document.querySelectorAll('[data-busca]').forEach(function(el){
      el.classList.toggle('oculto', q!=='' && el.dataset.busca.indexOf(q)===-1);
    });
  });

  document.addEventListener('keydown',function(e){
    if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA'){
      if(e.key==='Escape')e.target.blur(); return;
    }
    var i=ids.indexOf(atual);
    if(e.key==='j'&&i<ids.length-1)abrir(ids[i+1]);
    if(e.key==='k'&&i>0)abrir(ids[i-1]);
    if(e.key==='Escape')abrir('00');
    if(e.key==='/'){e.preventDefault();busca.focus()}
  });

  abrir((location.hash||'').replace('#aula-','')||'00',true);
})();
"""

CSS_EXTRA = """
.aula.oculto{display:none}
.toc-dados{display:none}
@media print{ .aula.oculto{display:none!important} }
"""

doc = f"""<!DOCTYPE html>
<html lang="pt-BR" data-tema="escuro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas · UNEMAT 2026.2</title>
<meta name="description" content="Material didático completo: 15 aulas de Vue 3, Vuetify, Pinia, Express e banco de dados.">
<style>{B.CSS}
{B.PYG_CSS}
{CSS_EXTRA}
</style>
</head>
<body>
<div id="progresso"></div>
<header class="topo"><div class="topo-in">
  <a class="marca" href="#aula-00" data-ir="00" style="color:inherit"><b>FACET-SNP-310</b> &nbsp;Frameworks Modernos</a>
  <span class="espaco"></span>
  <input id="busca" type="search" placeholder="Buscar aula…  (/)" autocomplete="off">
  <a class="btn" href="#aula-00" data-ir="00">Índice</a>
  <button class="btn" id="tema" type="button">Tema</button>
</div></header>
<div class="wrap">
  <nav class="lateral"><h4>Aulas</h4><ol>
    <li><a href="#aula-00" data-ir="00"><span class="num">—</span><span>Índice da disciplina</span></a></li>
    {''.join(menu)}
  </ol></nav>
  <main>{capa}{''.join(secoes)}
    <div class="rodape">
      UNEMAT — Universidade do Estado de Mato Grosso · Campus Sinop · FACET<br>
      FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas · 2026.2<br>
      Prof. Ivan Luiz Pedroso Pires
    </div>
  </main>
  <aside class="toc" id="toc"></aside>
</div>
<script>{JS}</script>
</body>
</html>"""

OUT.write_text(doc, encoding="utf-8")
print(f"{OUT}  ({len(doc)//1024} KB)")
