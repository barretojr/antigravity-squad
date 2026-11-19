# Squad

Esquadrão de agentes que **entrevista você, planeja e constrói** uma aplicação ponta a ponta, provando o resultado com build e testes reais. Funciona no **Antigravity** e no **Claude Code**.

A skill é agnóstica de domínio e de stack: tipo de negócio, banco, linguagem e integrações vêm da entrevista inicial e ficam registrados em `.squad/stack.md`. Em projetos existentes, a equipe preserva a stack encontrada.

## Como usar

```text
/squad crie uma aplicação que <descreva o que ela faz>
```
ou, em linguagem natural: *"use a skill squad e crie ..."*.

1. **Entrevista (uma rodada):** stack (.NET, Node/TypeScript, Python, sem backend), frontend, **banco** (PostgreSQL, **Supabase**, SQL Server, SQLite), se já existe projeto Supabase, autenticação, integrações externas e credenciais, deploy e nível de testes. Cada pergunta traz uma opção recomendada. O que o prompt ou o projeto já respondem não é perguntado de novo.
2. **Plano** curto (modo `lite`) ou mesa-redonda completa (modo `full`).
3. **Construção por fatias verticais** (dados → API → tela → teste), com build e testes a cada fatia.
4. **Verificação real:** `run_checks`, auditorias mecânicas e revisão no browser.
5. **Entrega:** como rodar, o que passou/falhou e **o que ainda depende de você** (chaves, contas, aprovações).

| Modo | Quando | Equipe | Fecha com |
|---|---|---|---|
| `lite` (padrão para "crie...") | App novo / feature grande | Arquiteto, Construtor, Verificador | `run_checks` + `audit_code_delivery` + um crítico |
| `full` | Pedido explícito de mesa-redonda | 11 especialistas + 2 críticos + `@Finalizer` | Gate independente do Finalizer |
| `audit` | Projeto existente, sem construir | Especialistas relevantes | Roadmap priorizado |

Referências da skill: `references/intake.md` (perguntas), `references/stacks.md` (perfis e comandos por stack, incluindo Supabase), `references/domain-packs.md` (como acoplar conhecimento de um nicho sem poluir a skill).

## Instalação

### Claude Code (recomendado: leve, ~3 MB)

```powershell
python install_claude.py --project C:\Projetos\MinhaApp     # .claude/ no projeto
python install_claude.py --global                           # ~/.claude/
python install_claude.py --project C:\Projetos\MinhaApp --with-heavy-skills   # + taste-skill e playwright-cli (~100 MB)
```

Instala 8 skills leves, os 14 agentes convertidos (a descrição de cada um restringe o uso ao fluxo da skill, então eles não disparam sozinhos) e o servidor MCP **sem registrá-lo**. O MCP é opcional; ative-o só no projeto que precisar, dentro dele:

```powershell
claude mcp add squad --scope local -- python <caminho>/.claude/mcp/server.py
```
(ou use `--register-mcp` junto de `--project`).

### Antigravity

```powershell
.\install.ps1                              # menu
.\install.ps1 -TargetProject "C:\Projetos\MinhaApp"
.\install.ps1 -Global
```
```bash
./install.sh "/caminho/do/projeto"   # ou --global
```

Instala em `.agents/` (projeto) ou `~/.gemini/config/` (global). **A regra `squad-context.md` agora é `trigger: manual`**: não é mais aplicada a prompts comuns. Recarregue o Antigravity após instalar.

## MCP server (opcional)

Servidor stdio em Python 3.10+, sem dependências. Sem ele a skill funciona (usa shell e leitura direta). Com ele:

| Ferramenta | Função |
|---|---|
| `run_checks` | **Roda build e testes reais** (dotnet, npm/pnpm/yarn, pytest, go, cargo), devolve status/exit code/saída e grava `.squad/evidencias/run_checks.md`. Só comandos conhecidos; `install=true` instala dependências Node ausentes. |
| `inspect_project` | Inventário, stack detectada, persistência (PostgreSQL, Supabase, SQLite...), autenticação, configs, jargão na UI e o `stack.md` declarado. |
| `audit_code_delivery` | Varredura mecânica: latência simulada, IDs falsos, KPIs digitados no JSX, mocks embutidos, `catch` vazio, `Thread.Sleep`. Ignora arquivos de teste. |
| `audit_security_controls` | Rotas de mutação sem `[Authorize]`, testes de segurança ausentes, credenciais sem criptografia. |
| `audit_frontend_taste` | Clichês de IA, cores arbitrárias, `prefers-reduced-motion`. |
| `get_design_reference` | Catálogo local de 84 `DESIGN.md` de referência. |
| `run_playwright_cli` | Playwright CLI (comandos permitidos fixos, URL apenas http/https). |
| `initialize_squad_docs`, `update_agent_report`, `update_roadmap`, `validate_squad_artifacts`, `validate_completion_checklist` | Artefatos e gate de conclusão em `.squad/`. |

As auditorias são heurísticas: tratam-se como pistas e confirmam-se lendo o código. O MCP não executa agentes nem simula subagentes.

## Estrutura

```text
squad-kit/                 # única fonte versionada
├── mcp/server.py             # servidor MCP (opcional)
├── agents/                   # 11 especialistas + 2 críticos + finalizer
├── commands/                 # alias /teamwork
├── rules/                    # squad-context.md (trigger: manual)
└── skills/
    ├── squad/    # SKILL.md + references/ (intake, stacks, domain-packs) + templates/
    ├── design-reference/     # catálogo awesome-design-md
    ├── design-taste-frontend/, taste-skill/, playwright-cli/   # pesados, opcionais
    └── product-research, product-brand-design, quality-validation, security-validation, frontend-integration, spatial-design
install.ps1 / install.sh      # Antigravity
install_claude.py             # Claude Code
```

Documentação de trabalho do produto fica em `.squad/` no projeto-alvo (relatórios, `stack.md`, roadmap, evidências); `.agents/` é configuração do Antigravity.

## Créditos e licenças de terceiros

| Projeto | Uso | Licença |
|---|---|---|
| [VoltAgent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | Catálogo de 84 `DESIGN.md` | [MIT](https://github.com/voltagent/awesome-design-md/blob/main/LICENSE) |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Direção de arte e heurísticas anti-slop | [MIT](https://github.com/leonxlnx/taste-skill/blob/main/LICENSE) |
| [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli) | Inspeção de browser | [Apache-2.0](https://github.com/microsoft/playwright-cli/blob/main/LICENSE) |

O [LICENSE](LICENSE) cobre o conteúdo original deste repositório; materiais de terceiros mantêm suas licenças.

## Licença

MIT.
