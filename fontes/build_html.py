#!/usr/bin/env python3
"""Converte as aulas em Markdown para páginas HTML autocontidas."""
import html
import json
import re
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

BASE = Path("/root/fds/material")
SRC = BASE / "aulas"
OUT = BASE / "html"
OUT.mkdir(parents=True, exist_ok=True)

AULAS = [
    ("01", "10/08/2026", "Unidade 1", "Apresentação da Disciplina e Revisão JavaScript"),
    ("02", "17/08/2026", "Unidade 1", "Introdução ao Vue: instância, ciclo de vida e diretivas"),
    ("03", "24/08/2026", "Unidade 1", "Vue: listas, computed e ciclo de vida"),
    ("04", "31/08/2026", "Unidade 1", "Introdução a Vuetify e Vue Router"),
    ("05", "14/09/2026", "Unidade 2", "Componentes, Vue Router e Vuetify avançado"),
    ("06", "21/09/2026", "Unidade 2", "Axios e Pinia"),
    ("07", "28/09/2026", "Unidade 3", "Introdução ao Firebase, Node.js e Express"),
    ("08", "05/10/2026", "Unidade 3", "Definindo endpoints e middlewares"),
    ("09", "19/10/2026", "Unidade 3", "Integrando com SGBD MySQL"),
    ("10", "26/10/2026", "Unidade 3", "Requisições autenticadas com Firebase"),
    ("11", "09/11/2026", "Unidade 3", "Integrando front-end com back-end: CRUD"),
    ("12", "16/11/2026", "Unidade 3", "CRUD com banco em nuvem (Supabase)"),
    ("13", "23/11/2026", "Unidade 3", "Desenvolvimento do Back-end"),
    ("14", "07/12/2026", "Unidade 3", "Documentação com Swagger"),
    ("15", "14/12/2026", "Unidade 3", "Deploy, apresentação e finalização"),
]

AVALIACOES = {"04": 1, "08": 2, "15": 3}

PYG_CSS = HtmlFormatter(style="stata-dark").get_style_defs(".highlight")

CSS = """
:root{
  --bg:#0f1117; --bg-soft:#161922; --bg-code:#11131a; --line:#272b38;
  --fg:#e6e8ee; --fg-dim:#a6adbb; --fg-faint:#6f7686;
  --accent:#5eead4; --accent-2:#818cf8; --warn:#fbbf24; --danger:#fb7185;
  --u1:#5eead4; --u2:#818cf8; --u3:#f0abfc;
  --radius:12px; --max:860px;
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;
}
html[data-tema="claro"]{
  --bg:#ffffff; --bg-soft:#f6f7f9; --bg-code:#f2f3f6; --line:#e2e5ea;
  --fg:#1a1d24; --fg-dim:#4b5262; --fg-faint:#8a92a3;
  --accent:#0d9488; --accent-2:#4f46e5; --warn:#b45309; --danger:#be123c;
  --u1:#0d9488; --u2:#4f46e5; --u3:#a21caf;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth; scroll-padding-top:76px}
body{
  margin:0; background:var(--bg); color:var(--fg); font-family:var(--font);
  font-size:16.5px; line-height:1.72; -webkit-font-smoothing:antialiased;
}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}

/* ---------- barra superior ---------- */
.topo{
  position:sticky; top:0; z-index:50; background:color-mix(in srgb,var(--bg) 88%,transparent);
  backdrop-filter:blur(12px); border-bottom:1px solid var(--line);
}
.topo-in{max-width:1400px;margin:0 auto;display:flex;align-items:center;gap:14px;padding:10px 18px}
.marca{font-weight:700;font-size:.82rem;letter-spacing:.06em;text-transform:uppercase;color:var(--fg-dim);white-space:nowrap}
.marca b{color:var(--accent)}
.topo .espaco{flex:1}
.btn{
  background:var(--bg-soft); color:var(--fg-dim); border:1px solid var(--line);
  border-radius:8px; padding:6px 12px; font-size:.82rem; cursor:pointer; font-family:inherit;
  transition:.15s;
}
.btn:hover{color:var(--fg); border-color:var(--accent)}
#busca{
  background:var(--bg-soft); border:1px solid var(--line); border-radius:8px; color:var(--fg);
  padding:6px 12px; font-size:.85rem; font-family:inherit; width:200px;
}
#busca:focus{outline:none;border-color:var(--accent)}

/* ---------- layout ---------- */
.wrap{max-width:1400px;margin:0 auto;display:grid;grid-template-columns:260px minmax(0,1fr) 240px;gap:34px;padding:0 18px}
@media(max-width:1150px){.wrap{grid-template-columns:240px minmax(0,1fr)} .toc{display:none}}
@media(max-width:860px){.wrap{grid-template-columns:minmax(0,1fr)} .lateral{display:none}}

.lateral,.toc{position:sticky;top:76px;align-self:start;max-height:calc(100vh - 90px);overflow-y:auto;padding:22px 0 60px;font-size:.85rem}
.lateral::-webkit-scrollbar,.toc::-webkit-scrollbar{width:6px}
.lateral::-webkit-scrollbar-thumb,.toc::-webkit-scrollbar-thumb{background:var(--line);border-radius:3px}
.lateral h4,.toc h4{font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--fg-faint);margin:0 0 12px}
.lateral ol{list-style:none;margin:0;padding:0}
.lateral li a{
  display:flex;gap:9px;align-items:baseline;padding:6px 10px;border-radius:7px;
  color:var(--fg-dim);border-left:2px solid transparent;line-height:1.35;
}
.lateral li a:hover{background:var(--bg-soft);color:var(--fg);text-decoration:none}
.lateral li a.ativo{background:var(--bg-soft);color:var(--fg);border-left-color:var(--accent);font-weight:600}
.lateral .num{font-variant-numeric:tabular-nums;color:var(--fg-faint);font-size:.78rem;min-width:16px}
.lateral .grupo{margin:18px 0 6px;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:var(--fg-faint);padding-left:10px}
.toc a{display:block;padding:4px 0 4px 12px;color:var(--fg-dim);border-left:2px solid var(--line);line-height:1.35;font-size:.8rem}
.toc a:hover{color:var(--fg);text-decoration:none}
.toc a.ativo{color:var(--accent);border-left-color:var(--accent)}
.toc a.n3{padding-left:24px;font-size:.76rem;opacity:.8}

/* ---------- conteúdo ---------- */
main{padding:34px 0 100px;min-width:0}
.cabecalho{border-bottom:1px solid var(--line);padding-bottom:22px;margin-bottom:34px}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.tag{font-size:.7rem;letter-spacing:.07em;text-transform:uppercase;font-weight:700;padding:4px 10px;border-radius:999px;border:1px solid var(--line);color:var(--fg-dim)}
.tag.u1{color:var(--u1);border-color:color-mix(in srgb,var(--u1) 40%,transparent)}
.tag.u2{color:var(--u2);border-color:color-mix(in srgb,var(--u2) 40%,transparent)}
.tag.u3{color:var(--u3);border-color:color-mix(in srgb,var(--u3) 40%,transparent)}
.tag.av{color:var(--warn);border-color:color-mix(in srgb,var(--warn) 45%,transparent)}
.cabecalho h1{margin:0;font-size:2.05rem;line-height:1.2;letter-spacing:-.02em}
.cabecalho .sub{color:var(--fg-faint);font-size:.9rem;margin-top:10px}

main h1{font-size:1.9rem;line-height:1.22;letter-spacing:-.02em;margin:0 0 .6em}
main h2{font-size:1.4rem;margin:2.4em 0 .7em;padding-top:.5em;border-top:1px solid var(--line);letter-spacing:-.01em}
main h3{font-size:1.12rem;margin:1.9em 0 .5em;color:var(--fg)}
main h4{font-size:.98rem;margin:1.5em 0 .4em;color:var(--fg-dim)}
main h2:first-of-type{border-top:none;padding-top:0}
main p{margin:0 0 1.05em}
main ul,main ol{margin:0 0 1.15em;padding-left:1.4em}
main li{margin:.32em 0}
main li>ul,main li>ol{margin:.35em 0}
hr{border:none;border-top:1px solid var(--line);margin:2.6em 0}
strong{color:var(--fg);font-weight:650}

/* âncoras */
.anchor{opacity:0;margin-left:.4em;font-weight:400;color:var(--fg-faint);text-decoration:none;font-size:.8em}
h2:hover .anchor,h3:hover .anchor{opacity:1}

/* citações / callouts */
blockquote{
  margin:1.4em 0;padding:14px 18px;background:var(--bg-soft);border-left:3px solid var(--accent-2);
  border-radius:0 var(--radius) var(--radius) 0;color:var(--fg-dim);
}
blockquote p:last-child{margin-bottom:0}
blockquote.dica{border-left-color:var(--accent)}
blockquote.atencao{border-left-color:var(--warn)}
blockquote.capo{border-left-color:var(--accent-2)}
blockquote.prova{border-left-color:var(--danger)}

/* tabelas */
.tabela-wrap{overflow-x:auto;margin:1.4em 0;border:1px solid var(--line);border-radius:var(--radius)}
table{border-collapse:collapse;width:100%;font-size:.88rem}
th,td{padding:9px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--bg-soft);font-weight:650;font-size:.78rem;letter-spacing:.04em;text-transform:uppercase;color:var(--fg-dim);white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:color-mix(in srgb,var(--bg-soft) 60%,transparent)}

/* código */
code{font-family:var(--mono);font-size:.87em;background:var(--bg-soft);padding:.14em .42em;border-radius:5px;border:1px solid var(--line)}
.bloco{position:relative;margin:1.3em 0}
.bloco-topo{
  display:flex;align-items:center;gap:10px;background:var(--bg-soft);border:1px solid var(--line);
  border-bottom:none;border-radius:var(--radius) var(--radius) 0 0;padding:6px 12px;
  font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;color:var(--fg-faint);font-family:var(--mono);
}
.bloco-topo .espaco{flex:1}
.copiar{
  background:transparent;border:1px solid var(--line);color:var(--fg-faint);border-radius:6px;
  padding:2px 9px;font-size:.68rem;cursor:pointer;font-family:inherit;letter-spacing:.06em;text-transform:uppercase;transition:.15s;
}
.copiar:hover{color:var(--accent);border-color:var(--accent)}
.copiar.ok{color:var(--accent);border-color:var(--accent)}
.highlight{
  margin:0;background:var(--bg-code)!important;border:1px solid var(--line);
  border-radius:0 0 var(--radius) var(--radius);overflow-x:auto;
}
.bloco:not(:has(.bloco-topo)) .highlight{border-radius:var(--radius)}
.highlight pre{margin:0;padding:15px 17px;font-family:var(--mono);font-size:.845rem;line-height:1.62;background:transparent!important}
.highlight code{background:transparent;border:none;padding:0;font-size:inherit}
html[data-tema="claro"] .highlight pre{color:#1a1d24}

/* detalhes */
details{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);padding:12px 16px;margin:1.2em 0}
details[open]{padding-bottom:6px}
summary{cursor:pointer;font-weight:600;color:var(--fg-dim);font-size:.9rem;list-style:none}
summary::-webkit-details-marker{display:none}
summary::before{content:"▸ ";color:var(--accent)}
details[open] summary::before{content:"▾ "}
details[open] summary{margin-bottom:10px}

img{max-width:100%;border-radius:var(--radius)}

/* rodapé / navegação */
.navpe{display:flex;gap:14px;margin-top:60px;padding-top:26px;border-top:1px solid var(--line)}
.navpe a{
  flex:1;padding:14px 18px;background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);
  color:var(--fg-dim);transition:.15s;
}
.navpe a:hover{border-color:var(--accent);color:var(--fg);text-decoration:none}
.navpe .rot{display:block;font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-faint);margin-bottom:4px}
.navpe .tit{font-weight:600;font-size:.9rem}
.navpe .dir{text-align:right}
.rodape{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);color:var(--fg-faint);font-size:.8rem}

/* progresso */
#progresso{position:fixed;top:0;left:0;height:2px;background:var(--accent);z-index:60;width:0}

/* índice (home) */
.hero{padding:56px 0 34px;border-bottom:1px solid var(--line);margin-bottom:38px}
.hero h1{font-size:2.6rem;margin:0 0 12px;letter-spacing:-.03em;line-height:1.1}
.hero p{color:var(--fg-dim);max-width:640px;font-size:1.02rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;margin:34px 0}
.stat{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px}
.stat .n{font-size:1.7rem;font-weight:700;letter-spacing:-.02em;color:var(--accent)}
.stat .l{font-size:.75rem;letter-spacing:.07em;text-transform:uppercase;color:var(--fg-faint);margin-top:2px}
.grade{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin:20px 0 44px}
.cartao{
  display:block;background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);
  padding:17px 19px;color:var(--fg);transition:.16s;position:relative;overflow:hidden;
}
.cartao::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--line);transition:.16s}
.cartao.u1::before{background:var(--u1)} .cartao.u2::before{background:var(--u2)} .cartao.u3::before{background:var(--u3)}
.cartao:hover{transform:translateY(-2px);border-color:var(--fg-faint);text-decoration:none}
.cartao .meta{display:flex;justify-content:space-between;align-items:center;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--fg-faint);margin-bottom:8px}
.cartao .t{font-weight:650;line-height:1.35;font-size:.97rem}
.cartao .av{display:inline-block;margin-top:9px;font-size:.68rem;letter-spacing:.07em;text-transform:uppercase;color:var(--warn);border:1px solid color-mix(in srgb,var(--warn) 40%,transparent);border-radius:999px;padding:2px 9px}
.oculto{display:none!important}
@media print{
  .topo,.lateral,.toc,.navpe,#progresso{display:none!important}
  .wrap{display:block;max-width:none;padding:0}
  body{background:#fff;color:#000;font-size:11pt}
  .highlight{border:1px solid #ccc;background:#fafafa!important}
  a{color:#000}
}
"""

JS = r"""
(function(){
  var raiz=document.documentElement;
  var salvo=null;
  try{salvo=window.localStorage&&localStorage.getItem('fds-tema')}catch(e){}
  if(salvo){raiz.setAttribute('data-tema',salvo)}
  var bt=document.getElementById('tema');
  if(bt){bt.addEventListener('click',function(){
    var novo=raiz.getAttribute('data-tema')==='claro'?'escuro':'claro';
    raiz.setAttribute('data-tema',novo);
    try{localStorage.setItem('fds-tema',novo)}catch(e){}
    bt.textContent=novo==='claro'?'● Escuro':'○ Claro';
  });
  bt.textContent=raiz.getAttribute('data-tema')==='claro'?'● Escuro':'○ Claro';}

  // copiar código
  document.querySelectorAll('.copiar').forEach(function(b){
    b.addEventListener('click',function(){
      var pre=b.closest('.bloco').querySelector('pre');
      var txt=pre.innerText;
      var ok=function(){b.textContent='Copiado';b.classList.add('ok');
        setTimeout(function(){b.textContent='Copiar';b.classList.remove('ok')},1600)};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok)}
      else{var t=document.createElement('textarea');t.value=txt;document.body.appendChild(t);
           t.select();document.execCommand('copy');t.remove();ok()}
    });
  });

  // barra de progresso
  var pr=document.getElementById('progresso');
  if(pr){window.addEventListener('scroll',function(){
    var h=document.documentElement.scrollHeight-window.innerHeight;
    pr.style.width=(h>0?(window.scrollY/h)*100:0)+'%';
  },{passive:true})}

  // sumário ativo
  var alvos=[].slice.call(document.querySelectorAll('main h2[id],main h3[id]'));
  var links={};
  document.querySelectorAll('.toc a').forEach(function(a){links[a.getAttribute('href').slice(1)]=a});
  if(alvos.length&&'IntersectionObserver' in window){
    var obs=new IntersectionObserver(function(ents){
      ents.forEach(function(e){
        var a=links[e.target.id];
        if(!a)return;
        if(e.isIntersecting){
          Object.keys(links).forEach(function(k){links[k].classList.remove('ativo')});
          a.classList.add('ativo');
        }
      });
    },{rootMargin:'-76px 0px -75% 0px'});
    alvos.forEach(function(t){obs.observe(t)});
  }

  // busca no índice
  var busca=document.getElementById('busca');
  if(busca){
    busca.addEventListener('input',function(){
      var q=busca.value.toLowerCase().trim();
      document.querySelectorAll('[data-busca]').forEach(function(el){
        el.classList.toggle('oculto', q!=='' && el.getAttribute('data-busca').indexOf(q)===-1);
      });
    });
  }

  // atalhos de teclado
  document.addEventListener('keydown',function(e){
    if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA')return;
    var ant=document.querySelector('[data-nav="anterior"]');
    var pro=document.querySelector('[data-nav="proxima"]');
    if(e.key==='j'&&pro)pro.click();
    if(e.key==='k'&&ant)ant.click();
    if(e.key==='/'&&busca){e.preventDefault();busca.focus()}
  });
})();
"""

CALLOUTS = [
    ("💡", "dica"), ("⚠️", "atencao"), ("🔎", "capo"), ("📌", "prova"),
]


def enfeitar(corpo: str) -> str:
    """Pós-processa o HTML gerado: callouts, tabelas roláveis, cabeçalho de bloco de código."""
    # blocos de código: envolve em .bloco com barra de topo
    def wrap_code(m):
        classe = m.group(1)
        lang = ""
        mm = re.search(r"language-([\w+-]+)", classe or "")
        if mm:
            lang = mm.group(1)
        rotulo = {
            "js": "JavaScript", "javascript": "JavaScript", "vue": "Vue SFC",
            "bash": "Terminal", "shell": "Terminal", "sh": "Terminal",
            "html": "HTML", "css": "CSS", "json": "JSON", "sql": "SQL",
            "yaml": "YAML", "yml": "YAML", "text": "Texto", "http": "HTTP",
            "ts": "TypeScript", "typescript": "TypeScript", "xml": "XML",
            "dockerfile": "Dockerfile", "ini": "Config", "diff": "Diff",
            "mermaid": "Diagrama", "python": "Python",
        }.get(lang.lower(), lang.upper() if lang else "Código")
        return (
            '<div class="bloco"><div class="bloco-topo"><span>' + rotulo + '</span>'
            '<span class="espaco"></span>'
            '<button class="copiar" type="button">Copiar</button></div>'
            '<div class="highlight' + ('' if not classe else '') + '">' + m.group(2) + '</div></div>'
        )

    corpo = re.sub(
        r'<div class="codehilite(?: [^"]*)?"(?: [^>]*)?>\s*(<pre[\s\S]*?</pre>)\s*</div>',
        lambda m: '<div class="bloco"><div class="bloco-topo"><span>Código</span>'
                  '<span class="espaco"></span>'
                  '<button class="copiar" type="button">Copiar</button></div>'
                  '<div class="highlight">' + m.group(1) + '</div></div>',
        corpo,
    )

    # callouts a partir do emoji inicial
    def marcar(m):
        interior = m.group(1)
        for emoji, cls in CALLOUTS:
            if emoji in interior[:160]:
                return '<blockquote class="' + cls + '">' + interior + "</blockquote>"
        return "<blockquote>" + interior + "</blockquote>"

    corpo = re.sub(r"<blockquote>([\s\S]*?)</blockquote>", marcar, corpo)

    # tabelas roláveis
    corpo = corpo.replace("<table>", '<div class="tabela-wrap"><table>').replace(
        "</table>", "</table></div>"
    )

    # rede de segurança: tags cruas que quebram o documento (ex.: `<template>` escrito
    # em markdown dentro de bloco HTML). O código real já vem escapado pelo Pygments,
    # então qualquer ocorrência aqui é acidental.
    for tag in ("template", "script", "style", "iframe", "textarea", "object", "embed"):
        corpo = re.sub(
            r"<(/?)" + tag + r"(\s[^>]*)?>",
            lambda m: "<code>&lt;" + m.group(1) + tag + (m.group(2) or "") + "&gt;</code>",
            corpo,
            flags=re.I,
        )
    return corpo


def detectar_linguagem(md_texto: str) -> str:
    return md_texto


def pagina(titulo, descricao, corpo, lateral, toc, navpe, com_busca=False, extra_class=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR" data-tema="escuro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(descricao)}">
<style>{CSS}
{PYG_CSS}
</style>
</head>
<body>
<div id="progresso"></div>
<header class="topo"><div class="topo-in">
  <span class="marca"><b>FACET-SNP-310</b> &nbsp;Frameworks Modernos</span>
  <span class="espaco"></span>
  {'<input id="busca" type="search" placeholder="Buscar aula…  (/)" autocomplete="off">' if com_busca else ''}
  <a class="btn" href="indice.html">Índice</a>
  <button class="btn" id="tema" type="button">Tema</button>
</div></header>
<div class="wrap">
  <nav class="lateral">{lateral}</nav>
  <main class="{extra_class}">{corpo}{navpe}
    <div class="rodape">
      UNEMAT — Universidade do Estado de Mato Grosso · Campus Sinop · FACET<br>
      FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas · 2026.2<br>
      Prof. Ivan Luiz Pedroso Pires
    </div>
  </main>
  {toc}
</div>
<script>{JS}</script>
</body>
</html>"""


def menu_lateral(atual=None):
    partes = ['<h4>Aulas</h4>', "<ol>"]
    grupo = None
    for num, data, unid, tit in AULAS:
        if unid != grupo:
            grupo = unid
            partes.append(f'<li class="grupo">{unid}</li>')
        arq = f"aula-{num}.html"
        cls = " ativo" if num == atual else ""
        partes.append(
            f'<li><a class="{cls.strip()}" href="{arq}">'
            f'<span class="num">{num}</span><span>{html.escape(tit)}</span></a></li>'
        )
    partes.append("</ol>")
    return "".join(partes)


def sumario(corpo_html):
    itens = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h[23]>', corpo_html)
    if not itens:
        return '<aside class="toc"></aside>'
    out = ['<aside class="toc"><h4>Nesta aula</h4>']
    for nivel, ident, txt in itens:
        limpo = re.sub(r"<[^>]+>", "", txt).replace("¶", "").strip()
        if not limpo:
            continue
        cls = "n3" if nivel == "3" else ""
        out.append(f'<a class="{cls}" href="#{ident}">{html.escape(limpo)}</a>')
    out.append("</aside>")
    return "".join(out)


def rodape_nav(i):
    ant = AULAS[i - 1] if i > 0 else None
    pro = AULAS[i + 1] if i < len(AULAS) - 1 else None
    h = ['<nav class="navpe">']
    if ant:
        h.append(
            f'<a data-nav="anterior" href="aula-{ant[0]}.html">'
            f'<span class="rot">← Aula {ant[0]}</span>'
            f'<span class="tit">{html.escape(ant[3])}</span></a>'
        )
    if pro:
        h.append(
            f'<a class="dir" data-nav="proxima" href="aula-{pro[0]}.html">'
            f'<span class="rot">Aula {pro[0]} →</span>'
            f'<span class="tit">{html.escape(pro[3])}</span></a>'
        )
    h.append("</nav>")
    return "".join(h)


md = markdown.Markdown(
    extensions=["fenced_code", "codehilite", "tables", "toc", "attr_list", "sane_lists", "md_in_html"],
    extension_configs={
        "codehilite": {"guess_lang": False, "css_class": "codehilite"},
        "toc": {"anchorlink": False, "permalink": "¶", "permalink_class": "anchor"},
    },
)

arquivos = sorted(SRC.glob("aula-*.md"))
assert len(arquivos) == 15, f"esperava 15 aulas, achei {len(arquivos)}"

for i, (num, data, unid, tit) in enumerate(AULAS):
    caminho = next(p for p in arquivos if p.name.startswith(f"aula-{num}-"))
    texto = caminho.read_text(encoding="utf-8")
    md.reset()
    corpo = md.convert(texto)
    corpo = enfeitar(corpo)

    ucls = {"Unidade 1": "u1", "Unidade 2": "u2", "Unidade 3": "u3"}[unid]
    av = AVALIACOES.get(num)
    tags = f'<span class="tag {ucls}">{unid}</span><span class="tag">{data}</span><span class="tag">3 aulas de 50 min + 1 h EAD</span>'
    if av:
        tags += f'<span class="tag av">Entrega da Avaliação {av}</span>'
    cabecalho = (
        '<div class="cabecalho">'
        f'<div class="tags">{tags}</div>'
        f'<h1>Aula {num} — {html.escape(tit)}</h1>'
        '<div class="sub">FACET-SNP-310 · Frameworks Modernos para Desenvolvimento de Sistemas · '
        'UNEMAT/Sinop · Prof. Ivan Luiz Pedroso Pires</div></div>'
    )
    # remove o H1 original do markdown (já está no cabeçalho)
    corpo = re.sub(r"<h1[^>]*>[\s\S]*?</h1>", "", corpo, count=1)

    saida = pagina(
        titulo=f"Aula {num} — {tit} · FACET-SNP-310",
        descricao=f"{unid} · {data} · {tit}",
        corpo=cabecalho + corpo,
        lateral=menu_lateral(num),
        toc=sumario(corpo),
        navpe=rodape_nav(i),
    )
    (OUT / f"aula-{num}.html").write_text(saida, encoding="utf-8")
    print(f"aula-{num}.html  ({len(saida)//1024} KB)")

# ---------------- índice ----------------
cartoes = []
for num, data, unid, tit in AULAS:
    ucls = {"Unidade 1": "u1", "Unidade 2": "u2", "Unidade 3": "u3"}[unid]
    av = AVALIACOES.get(num)
    chave = f"{num} {data} {unid} {tit}".lower()
    cartoes.append(
        f'<a class="cartao {ucls}" href="aula-{num}.html" data-busca="{html.escape(chave)}">'
        f'<div class="meta"><span>Aula {num} · {unid}</span><span>{data}</span></div>'
        f'<div class="t">{html.escape(tit)}</div>'
        + (f'<span class="av">Entrega da Avaliação {av}</span>' if av else "")
        + "</a>"
    )

corpo_indice = f"""
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

<h2 id="aulas">Aulas</h2>
<div class="grade">{''.join(cartoes)}</div>

<h2 id="projeto">O projeto fio-condutor</h2>
<p>Todas as aulas constroem incrementalmente o <strong>UniEventos</strong>, uma plataforma de divulgação e
inscrição em eventos acadêmicos. O professor desenvolve o UniEventos em sala; cada estudante desenvolve um
<strong>projeto autoral</strong> com a mesma arquitetura e domínio diferente. As avaliações são sobre o projeto autoral.</p>

<h2 id="stack">Stack e versões</h2>
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

<h2 id="avaliacao">Avaliação</h2>
<p>Média aritmética simples de três avaliações práticas individuais, entregues via SIGAA.
O exame final é uma prova teórica presencial sobre as três unidades.</p>
<div class="tabela-wrap"><table>
<thead><tr><th>Avaliação</th><th>Conteúdo</th><th>Prazo</th></tr></thead>
<tbody>
<tr><td>Avaliação 1</td><td>Vue 3 com CLI: estrutura, componentes, diretivas</td><td>31/08/2026</td></tr>
<tr><td>Avaliação 2</td><td>Vuetify, Vue Router, Axios e Pinia</td><td>05/10/2026</td></tr>
<tr><td>Avaliação 3</td><td>Back-end, banco de dados, autenticação e deploy</td><td>14/12/2026</td></tr>
</tbody></table></div>

<h2 id="uso">Como usar este material</h2>
<ul>
<li>Cada aula tem objetivos, teoria, passo a passo prático, laboratório em sala, tabela de erros comuns e uma atividade assíncrona de 1 hora.</li>
<li>Todos os blocos de código têm botão <strong>Copiar</strong>.</li>
<li>Atalhos de teclado: <code>j</code> próxima aula, <code>k</code> aula anterior, <code>/</code> busca.</li>
<li>Use o botão <strong>Tema</strong> para alternar entre claro e escuro. A impressão (Ctrl+P) gera um PDF limpo.</li>
</ul>
"""

(OUT / "indice.html").write_text(
    pagina(
        titulo="FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas",
        descricao="Material didático completo da disciplina — UNEMAT 2026.2",
        corpo=corpo_indice,
        lateral=menu_lateral(),
        toc='<aside class="toc"><h4>Nesta página</h4>'
            '<a href="#aulas">Aulas</a><a href="#projeto">Projeto fio-condutor</a>'
            '<a href="#stack">Stack e versões</a><a href="#avaliacao">Avaliação</a>'
            '<a href="#uso">Como usar</a></aside>',
        navpe="",
        com_busca=True,
    ),
    encoding="utf-8",
)
print("indice.html")
print("OK")
