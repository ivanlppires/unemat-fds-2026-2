# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Material didático da disciplina **FACET-SNP-310 — Frameworks Modernos para Desenvolvimento de Sistemas** (UNEMAT — Campus **Sinop**, semestre 2026.2, Prof. Ivan Luiz Pedroso Pires). Publicado via GitHub Pages em <https://ivanlppires.github.io/unemat-fds-2026-2/>. Todo o conteúdo é em português (pt-BR).

## Architecture: sources → generated HTML

- **`fontes/aula-NN-*.md`** — the 15 lesson sources (one Markdown file per lesson). These are the canonical content; every HTML file at the repo root is generated from them.
- **`fontes/build_html.py`** — generates one page per lesson + the index. **`fontes/build_single.py`** — generates the single-file apostila; it imports `build_html` to reuse its CSS, the `AULAS` schedule table, and `enfeitar()` (post-processing that turns emoji-prefixed headings into styled callout boxes).
- Root HTML (`aula-01.html`…`aula-15.html`, `index.html`, `indice.html`, `apostila.html`) is what Pages serves. All of it is self-contained (inline CSS/JS, no external dependencies). `.nojekyll` keeps Pages from running Jekyll.

### ⚠️ Build script paths do not match this repo

Both scripts hard-code `BASE = Path("/root/fds/material")` with sources in `BASE/aulas/` and output to `BASE/html/` — the layout of the machine where the material was originally generated. In this repo the Markdown lives directly in `fontes/` and the HTML at the root, with renames:

| Script output | Repo file |
|---|---|
| `html/apostila-completa.html` | `apostila.html` |
| `html/indice.html` | `index.html` **and** `indice.html` (identical copies) |
| `html/aula-NN.html` | `aula-NN.html` |

To regenerate: edit `BASE`/`SRC`/`OUT` in `build_html.py` (build_single.py inherits via import but defines its own `BASE`/`SRC`/`OUT` too), run the scripts, then copy outputs to the root with the renames above.

### Editing content

A text fix must land in **both** the `fontes/*.md` source and the generated HTML (per-lesson page **and** `apostila.html`, plus `index.html`/`indice.html` if it appears there) — either by regenerating or by applying the same replacement to both. Fixing only the HTML gets silently reverted on the next regeneration.

## Commands

```bash
# Regenerate HTML (after fixing the paths — see above)
pip install markdown pygments
cd fontes && python3 build_html.py && python3 build_single.py

# Publish: Pages serves branch main, root — a push is a deploy
git push
# First-time setup (creates the public repo + enables Pages via gh CLI)
bash publicar.sh
```

There are no tests or linters.

## Content rules — `fontes/ESPECIFICACAO.md` is the master spec

Anyone writing or editing a lesson must follow `fontes/ESPECIFICACAO.md`:

- **§2 Cronograma**: use the literal dates given; never recalculate or "correct" them.
- **§3 UniEventos**: the running project all 15 lessons build incrementally (students build their own project with the same architecture but a different domain; evaluations are on the student project).
- **§4 Stack versions**: verified against the real environment (Vue 3.5, Vite 8, Vuetify 4, Vue Router 5, Pinia 4, Express 5, Node 22). Do not invent versions or commands.
- **§5 Armadilhas**: Vuetify 4 and Express 5 have breaking changes vs. the Vuetify 3 / Express 4 material that dominates the internet — check this section before writing any example code.
- **§7**: the mandatory section structure every lesson file follows (Objetivos → Pré-requisitos → Roteiro → theory → "🧩 Padrão de projeto" → "💻 Mão na massa" → "🧪 Laboratório" → "🐛 Erros comuns" → "🏠 Atividade assíncrona" → "✅ Checkpoint" → "📚 Para aprofundar"; lessons 04, 08, 15 also carry "📝 Avaliação N").

Note: the campus is **Sinop** (older text said Cáceres; corrected 2026-08-12).
