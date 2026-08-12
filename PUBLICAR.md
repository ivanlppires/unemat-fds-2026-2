# Como colocar no ar

## Opção 1 — automática (recomendada)

Precisa do [gh CLI](https://cli.github.com) autenticado (`gh auth login`).

```bash
unzip unemat-fds-2026-2.zip
cd unemat-fds-2026-2
bash publicar.sh
```

O script cria o repositório **público**, envia os arquivos e ativa o GitHub Pages. Ao final ele imprime o link.

Para usar outro nome de repositório, edite a variável `REPO` na primeira linha do `publicar.sh`.

## Opção 2 — manual

1. Crie um repositório público chamado `unemat-fds-2026-2` em <https://github.com/new> (sem README, sem .gitignore).

2. No terminal, dentro da pasta descompactada:

```bash
git init -b main
git add -A
git commit -m "Material didatico FACET-SNP-310 - UNEMAT 2026.2"
git remote add origin https://github.com/ivanlppires/unemat-fds-2026-2.git
git push -u origin main
```

3. No GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` / `/ (root)` → Save**.

4. Em ~2 minutos o site estará em:

- <https://ivanlppires.github.io/unemat-fds-2026-2/> — portal com as 15 aulas
- <https://ivanlppires.github.io/unemat-fds-2026-2/apostila.html> — apostila completa em arquivo único

## Estrutura do repositório

```
index.html        portal / índice (página inicial do Pages)
indice.html       mesma página, para os links internos das aulas
apostila.html     apostila completa, arquivo único (2,4 MB)
aula-01..15.html  uma página por aula
.nojekyll         desativa o Jekyll do Pages (serve os arquivos como estão)
README.md         apresentação da disciplina
fontes/           Markdown das aulas + scripts de build (build_html.py, build_single.py)
publicar.sh       este script de publicação
```

Todo o HTML é autocontido: CSS e JS embutidos, sem dependência externa, funciona offline.
