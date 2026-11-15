# Antigravity Squad

Mesa-redonda de onze agentes para descoberta, planejamento e execução de produto, com foco de referência em .NET 10, PostgreSQL 17 e React 19. Em projetos existentes, a equipe preserva a stack encontrada.

## Fluxo

1. Instale as customizações no projeto ou globalmente.
2. Invoque `/antigravity-squad` com a ideia, auditoria ou produto a evoluir.
3. PM, Designer, Design System, Coord, DBA, Backend, Frontend, Frontend Reviewer, AppSec, QA e DevOps analisam em paralelo. Cada agente registra seu relatório e evidências em `.agentes/` no projeto trabalhado.
4. Coord consolida as decisões e dependências em `.agentes/coordenacao/roadmap.md`. Planejamento não altera código do produto.
5. Depois que você escolher itens, os agentes executam o escopo selecionado e atualizam os relatórios com arquivos e validações reais.

Use `/antigravity-squad`, não `/teamwork`, como fluxo principal. `/teamwork` permanece como alias compatível.

## Qualidade de produto

- Dashboards e SaaS privados incluem autenticação real, sessão e autorização no servidor, salvo requisito explícito diferente.
- O frontend consome contratos reais do backend; sem dados, apresenta estado vazio em vez de conteúdo inventado.
- O Designer define identidade visual; Design System registra o contrato implementável em `.agentes/design/DESIGN.md`.
- Frontend Reviewer inspeciona a UI no browser e registra screenshots, console e requests. QA mantém os testes funcionais e de integração.
- Pesquisa, implementação e testes só são marcados como feitos quando houver evidência.

## Fonte única e instalação

`.antigravity/` é a única fonte versionada deste repositório: agentes, regras, skills, comandos e templates ficam agrupados ali. Os instaladores distribuem essa fonte para `.agents/` no projeto-alvo, que é o layout nativo consumido pelo Antigravity. `.agentes/` é criado no produto para pesquisa, roadmap e relatórios; não é cópia da configuração da skill.

### Windows / PowerShell

```powershell
.\install.ps1
.\install.ps1 -TargetProject "C:\Projetos\MinhaApp"
.\install.ps1 -Global
```

### Linux / macOS / WSL

```bash
chmod +x install.sh
./install.sh
./install.sh "/caminho/do/projeto"
./install.sh --global
```

Instalação global publica agentes, regras, comandos e skills em `~/.gemini/config/` e mantém a skill principal no caminho legado do CLI. Reabra ou recarregue o Antigravity após instalar.

## MCP server

Os instaladores também distribuem o servidor stdio em `.agents/mcp/server.py` no projeto-alvo (ou em `~/.gemini/config/mcp/server.py` na instalação global). Ele não depende de pacotes externos e requer Python 3.10 ou mais recente. Configure o cliente MCP para iniciar o processo com o caminho instalado, por exemplo:

```json
{
  "mcpServers": {
    "antigravity-squad": {
      "command": "python",
      "args": ["C:/Projetos/MinhaApp/.agents/mcp/server.py"]
    }
  }
}
```

Em Linux/macOS, use `python3` e o caminho POSIX equivalente. Na instalação global, substitua o caminho por `~/.gemini/config/mcp/server.py`. Reinicie o cliente MCP para carregar o servidor.

As ferramentas são:
- `inspect_project`: Realiza auditoria arquitetural profunda: detecta persistência real (PostgreSQL, SQLite, Docker, migrations) alertando sobre estado em memória; audita autenticação e criptografia; checa configurações de credenciais (.env, appsettings); e escaneia o frontend contra vazamentos de jargão de dev na UI.
- `audit_code_delivery`: Audita o código-fonte mecanicamente contra trapaças: timers simulados (`setTimeout`), IDs falsos (`Math.random`), métricas inventadas na UI (fake KPIs / AI slop), empty catch e bloqueios síncronos, municiando os dois críticos de código (`code_critic_blind` e `code_critic_spec`).
- `audit_security_controls`: Audita controles do AppSec: proteção de rotas com autenticação/JWT, testes de segurança automatizados (SSRF, Auth, BOLA) e criptografia de credenciais de terceiros com AES-256/DataProtection.
- `get_design_reference`: Consulta localmente o catálogo completo de 84 sistemas de design de referência (`awesome-design-md`) como Linear, Stripe, Supabase, Vercel e Apple para extração de tokens e contratos visuais.
- `audit_frontend_taste`: Audita a interface contra clichês de IA e anti-patterns de design (`taste-skill`): detecta textos de marketing genéricos ("supercharge your", "next-gen"), classes Tailwind hexadecimais soltas, layouts monótonos e falta de acessibilidade `prefers-reduced-motion`.
- `run_playwright_cli`: Executa comandos de navegador real via `playwright-cli` (snapshot, screenshot, console, requests, resize) para capturar evidências de tela e requisições de rede salvando em `.squad/evidencias/frontend/`.
- `initialize_squad_docs`, `update_agent_report`, `update_roadmap` e `validate_squad_artifacts`: Gerenciam e validam a integridade de artefatos na pasta padrão unificada `.squad/` (ou `.agentes/`).

O MCP automatiza inspeção, pesquisa visual, execução de browser e manutenção de artefatos; não executa os onze agentes nem simula subagentes. A skill continua orientando processo, critérios, papéis e limites.

## Estrutura

```text
.antigravity/
├── mcp/                    # servidor MCP stdio sem dependências externas
├── agents/                 # onze perfis de agente + dois críticos adversariais
├── commands/               # alias /teamwork
├── rules/                  # contexto e limites compartilhados
└── skills/                 # skills instaladas e catálogos integrados
    ├── design-reference/       # awesome-design-md (84 benchmarks reais)
    ├── design-taste-frontend/  # taste-skill (heurísticas, scripts, assets)
    ├── playwright-cli/         # Microsoft Playwright CLI (scripts e referências)
    └── antigravity-squad/      # skill orquestradora
```

## Métodos de frontend integrados

1. **Awesome DESIGN.md (`design-reference`):**
   Catálogo local com 84 referências consagradas de mercado (Linear, Stripe, Vercel, Supabase, Apple, Airbnb, Shopify). O agente `design_system` consulta diretamente via `get_design_reference` para estruturar tokens semânticos e tipografia sem alucinações.
2. **Taste-Skill (`design-taste-frontend`):**
   Metodologia completa de direção de arte sem "AI slop". Fornece scripts de validação de consistência, lint de copy e ferramentas automatizadas via `audit_frontend_taste`.
3. **Microsoft Playwright CLI (`playwright-cli`):**
   Runtime headless e interativo empacotado para o agente `frontend_reviewer` rodar testes visuais em desktop (1440px) e mobile (390px), salvar capturas de tela e auditar chamadas de rede reais via `run_playwright_cli`.

## Créditos e licenças de terceiros

| Projeto | Como é usado aqui | Licença upstream |
|---|---|---|
| [VoltAgent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | Catálogo completo de 84 arquivos `DESIGN.md` para benchmarking e extração de contratos visuais via MCP e skill. | [MIT](https://github.com/voltagent/awesome-design-md/blob/main/LICENSE) |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Direção de arte, heurísticas anti-slop, assets, scripts de consistência e auditoria de taste no MCP. | [MIT](https://github.com/leonxlnx/taste-skill/blob/main/LICENSE) |
| [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli) | CLI de automação de browser empacotada para inspeção visual responsiva, console logs e captura de requests. | [Apache-2.0](https://github.com/microsoft/playwright-cli/blob/main/LICENSE) |

O [LICENSE](LICENSE) na raiz cobre o conteúdo original deste repositório. Os projetos e materiais de terceiros permanecem sob suas respectivas licenças.

## Licença

MIT. Consulte [LICENSE](LICENSE).

## Gate de conclusão independente

O fluxo de execução termina com `@Finalizer`, agente independente que preenche `qualidade/finalizer.md` e valida o aceite usando `validate_completion_checklist`. O gate exige evidências para inventário real (incluindo client separado versus UI embutida), integração browser/API first-party, banco e schema/migrations, logs/exceções, build, testes unitários e de integração, e fluxos de browser. Testes registram comando e resultado; unitários não provam integração. SQL Server LocalDB e acesso pelo Visual Studio só são aplicáveis a .NET no Windows. Lacunas bloqueiam conclusão e devem virar tarefas no roadmap.

The MCP exposes `validate_completion_checklist(project_root)` for the mandatory finalizer gate. It returns each checklist status/evidence, project inventory and platform applicability, and blocks approval for missing rows, unsupported N/A, failed checks, integration claims without integration evidence, browser checks without actual HTTP evidence, or test claims without command and result.
