#!/usr/bin/env bash
# Publica este material no GitHub e coloca no ar via GitHub Pages.
# Requisitos: git + gh CLI autenticado (gh auth login)
# Uso:  bash publicar.sh
set -euo pipefail

REPO="unemat-fds-2026-2"      # <- troque aqui se quiser outro nome
DESC="Material didatico FACET-SNP-310 - Frameworks Modernos para Desenvolvimento de Sistemas - UNEMAT Sinop 2026.2"

cd "$(dirname "$0")"

command -v gh >/dev/null || { echo "gh CLI nao encontrado: https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "Rode primeiro: gh auth login"; exit 1; }

OWNER=$(gh api user --jq .login)

echo "==> Preparando repositorio local"
[ -d .git ] || git init -q -b main
git add -A
git diff --cached --quiet || git commit -q -m "Material didatico FACET-SNP-310 - UNEMAT 2026.2"
git branch -M main

echo "==> Criando repositorio publico $OWNER/$REPO"
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "    (ja existe, reaproveitando)"
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
else
  gh repo create "$REPO" --public --description "$DESC" --source=. --remote=origin
fi

echo "==> Enviando arquivos"
git push -u origin main

echo "==> Ativando GitHub Pages (branch main, raiz)"
gh api -X POST "repos/$OWNER/$REPO/pages" \
  -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
|| gh api -X PUT "repos/$OWNER/$REPO/pages" \
  -f "source[branch]=main" -f "source[path]=/" >/dev/null

echo
echo "======================================================"
echo " Pronto. O site fica no ar em ate ~2 minutos:"
echo
echo "   https://$OWNER.github.io/$REPO/"
echo "   https://$OWNER.github.io/$REPO/apostila.html"
echo
echo " Repositorio: https://github.com/$OWNER/$REPO"
echo "======================================================"
