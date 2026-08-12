# FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas

Material didático da disciplina **FACET-SNP-310**, ofertada na UNEMAT — Campus de Sinop, no semestre **2026.2**.

**Professor:** Ivan Luiz Pedroso Pires
**Período letivo:** 10/08/2026 a 14/12/2026 — 15 aulas

## 📖 Acesse online

**<https://ivanlppires.github.io/unemat-fds-2026-2/>**

| Formato | Link | Uso |
|---|---|---|
| Portal / índice | [index.html](https://ivanlppires.github.io/unemat-fds-2026-2/) | Navegar aula a aula |
| Apostila completa (arquivo único) | [apostila.html](https://ivanlppires.github.io/unemat-fds-2026-2/apostila.html) | Leitura corrida, projeção em sala, salvar offline |
| Aula individual | `aula-01.html` … `aula-15.html` | Uma aula por vez |

Tudo é HTML autocontido: não há dependência externa, funciona offline e pode ser salvo em PDF pelo navegador (Ctrl+P).

### Recursos da apostila

- Tema claro/escuro alternável
- Sumário lateral com navegação rápida
- Botão "copiar" em cada bloco de código
- Atalhos `j` / `k` para avançar e voltar entre seções

## 🧭 Projeto fio-condutor: UniEventos

Plataforma de eventos acadêmicos construída incrementalmente ao longo das 15 aulas. Cada aluno replica a mesma arquitetura em um domínio próprio.

**Stack:** Vue 3 (Composition API) · Vuetify · Pinia · Vue Router · Axios · Node.js · Express · MySQL · Supabase · Firebase Authentication · Swagger · deploy em nuvem.

## 🗂️ Ementa por unidade

### Unidade I — Fundamentos de front-end com Vue 3 (aulas 1–6)
Revisão de JavaScript moderno, diretivas, listas e `computed`, ciclo de vida, componentes, Vue Router, Vuetify, Axios e Pinia.

### Unidade II — Back-end com Node.js e Express (aulas 7–10)
Firebase, Node.js e Express, endpoints e middlewares, integração com MySQL, autenticação.

### Unidade III — Integração, documentação e deploy (aulas 11–15)
CRUD full-stack, Supabase, desenvolvimento do back-end, documentação com Swagger, deploy e apresentação final.

## ✅ Avaliação

| Instrumento | Entrega |
|---|---|
| Avaliação 1 — front-end | 31/08/2026 |
| Avaliação 2 — back-end | 05/10/2026 |
| Avaliação 3 — projeto integrador | 14/12/2026 |

## 🔧 Regerar o material

Os fontes em Markdown e os scripts de build estão em [`fontes/`](fontes/).

```bash
cd fontes
python3 build_html.py      # gera as páginas por aula + índice
python3 build_single.py    # gera a apostila de arquivo único
```

## 📄 Licença

Material didático de uso educacional. Livre para consulta, estudo e reuso com atribuição.
