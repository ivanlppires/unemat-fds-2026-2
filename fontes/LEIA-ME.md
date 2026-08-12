# Material didático — FACET-SNP-310

**Frameworks Modernos para Desenvolvimento de Sistemas** · UNEMAT / Sinop — FACET · Turma 01 · 2026.2
Prof. Ivan Luiz Pedroso Pires · 60h (45h presenciais + 15h EAD)

## O que tem aqui

```
material/
├─ LEIA-ME.md              este arquivo
├─ ESPECIFICACAO.md        documento-mestre: cronograma, projeto fio-condutor,
│                          versões verificadas, armadilhas de sintaxe, padrão editorial
├─ aulas/                  15 arquivos Markdown, um por aula
├─ html/
│  ├─ apostila-completa.html   ★ arquivo único com as 15 aulas, navegável
│  ├─ indice.html              índice das aulas (versão multiarquivo)
│  └─ aula-01.html … aula-15.html
├─ build_html.py           gera as páginas individuais a partir do Markdown
└─ build_single.py         gera a apostila de arquivo único
```

**Comece por `html/apostila-completa.html`** — abre no navegador sem servidor, sem internet e sem
dependências. Tudo está embutido no arquivo.

## Como o material está organizado

Cada aula segue sempre a mesma estrutura, dimensionada para 3 aulas de 50 min presenciais mais
1 hora de atividade assíncrona:

1. Objetivos de aprendizagem
2. Pré-requisitos (o que precisa estar funcionando na máquina)
3. Roteiro em 3 blocos de 50 min
4. Seções teóricas numeradas
5. Box "🧩 Padrão de projeto em uso" — atende à exigência da ementa
6. "💻 Mão na massa" — passo a passo com código completo
7. "🧪 Laboratório" — exercícios em sala, com dicas em `<details>`
8. "🐛 Erros comuns" — tabela sintoma → causa → solução
9. "🏠 Atividade assíncrona (1 h)"
10. "✅ Checkpoint do projeto autoral"
11. "📚 Para aprofundar"

Nas aulas **04, 08 e 15** há também a seção **"📝 Avaliação N — instruções de entrega"**, com escopo,
rubrica de 10 pontos, formato de entrega no SIGAA, prazo e política de atraso e de uso de IA.

## Projeto fio-condutor: UniEventos

As 15 aulas constroem incrementalmente a mesma aplicação — **UniEventos**, plataforma de divulgação e
inscrição em eventos acadêmicos. O professor desenvolve o UniEventos em sala; **cada estudante
desenvolve um projeto autoral com a mesma arquitetura e domínio diferente**. As três avaliações são
sobre o projeto autoral, não sobre o UniEventos.

Repositórios de referência: `unieventos-web` (front) e `unieventos-api` (back).

## Stack — versões verificadas em 12/08/2026

Todas as versões e comandos deste material foram **testados no ambiente real**, não copiados de
tutoriais. O scaffold `create-vue` + Vuetify 4 foi gerado e passou no `npm run build`; a sintaxe de
rotas e o tratamento de erro assíncrono do Express 5 foram executados e conferidos.

| Camada | Tecnologia | Versão |
|---|---|---|
| Runtime | Node.js | 22.22 LTS |
| Front-end | Vue | 3.5.41 |
| Build | Vite | 8.2.1 |
| UI | Vuetify | 4.1.8 |
| Rotas | Vue Router | 5.2.0 |
| Estado | Pinia | 4.0.3 |
| HTTP | Axios | 1.19.0 |
| Back-end | Express | 5.2.1 |
| Banco | MySQL 8 / Supabase | mysql2 3.23.3 |
| Auth | Firebase | 12.17.1 |
| Docs | swagger-jsdoc / swagger-ui-express | 6.3.0 / 5.0.1 |

> **⚠️ Por que isso importa:** Vuetify 4 e Express 5 têm mudanças que quebram exemplos das versões
> anteriores, e a maior parte do conteúdo disponível na internet ainda é de Vuetify 3 e Express 4.
> A seção §5 do `ESPECIFICACAO.md` lista todas as armadilhas — vale a leitura antes de improvisar
> exemplos em sala.

## Regenerando o HTML

Se você editar os arquivos Markdown, regenere as páginas:

```bash
pip install markdown pygments
python3 build_html.py     # páginas individuais + índice
python3 build_single.py   # apostila de arquivo único
```

## Recursos da versão HTML

- Tema claro/escuro (o botão **Tema**, preferência salva no navegador)
- Botão **Copiar** em todos os blocos de código
- Sumário lateral que acompanha a rolagem
- Busca de aulas no índice
- Atalhos: `j` próxima aula · `k` aula anterior · `/` busca · `Esc` volta ao índice
- Ctrl+P imprime a aula aberta em PDF limpo (sem menus)
