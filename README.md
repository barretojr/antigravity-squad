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

As ferramentas são `inspect_project`, `audit_code_delivery`, `initialize_squad_docs`, `update_agent_report`, `update_roadmap` e `validate_squad_artifacts`. Cada uma recebe `project_root`. Inspecionar, auditar e validar são somente leitura; as demais escrevem exclusivamente na pasta unificada `.squad/` sob essa raiz (com suporte retrocompatível para `.agentes/`).

O `inspect_project` realiza auditoria arquitetural profunda: detecta persistência real (PostgreSQL, SQLite, Docker, migrations) alertando sobre estado em memória; audita autenticação e criptografia; checa configurações de credenciais (.env, appsettings); e escaneia o frontend contra vazamentos de jargão de dev na UI (ex: `.NET 10`, `React 19`, `no Backend`).

O `audit_code_delivery` audita o código-fonte mecanicamente contra trapaças: timers simulados (`setTimeout`), IDs falsos (`Math.random`), métricas inventadas na UI (fake KPIs / AI slop), empty catch e bloqueios síncronos, municiando os dois críticos de código (`code_critic_blind` e `code_critic_spec`).

O `validate_squad_artifacts` exige seções especializadas em cada agente (pesquisa de APIs e gestão de credenciais no PM, transparência de persistência física no DBA, autenticação e criptografia no AppSec, anti-jargão e ausência de métricas falsas no Frontend/Designer) e rejeita persistência em memória marcada como concluída. A pasta padrão unificada é `.squad/`.

O MCP automatiza inspeção e manutenção de artefatos; não executa os onze agentes nem simula subagentes. A skill continua orientando processo, critérios, papéis e limites. Use-a junto do servidor quando o cliente suportar skills; caso contrário, consulte `.agents/skills/antigravity-squad/SKILL.md` instalado.

## Estrutura

```text
.antigravity/
├── mcp/                    # servidor MCP stdio sem dependências externas
├── agents/                 # onze perfis de agente
├── commands/               # alias /teamwork
├── rules/                  # contexto e limites compartilhados
└── skills/                 # skill principal, skills de domínio e templates
```

## Métodos de frontend

Design System transforma a direção visual em tokens, componentes, estados e regras específicas do produto. Taste-skill orienta direção de arte sem impor uma linguagem visual universal. Playwright CLI dá ao Frontend Reviewer um fluxo de browser para avaliar responsividade, hierarquia, console e requests.

## Créditos e licenças de terceiros

| Projeto | Como é usado aqui | Licença upstream |
|---|---|---|
| [VoltAgent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | Catálogo de referência para pesquisar sistemas visuais e estruturar o `DESIGN.md` específico de cada produto. Nenhum arquivo de design ou ativo visual do catálogo é redistribuído. | [MIT](https://github.com/voltagent/awesome-design-md/blob/main/LICENSE) |
| [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | Inspira a skill adaptada de direção de arte e revisão visual. A adaptação está identificada em [UPSTREAM.md](.antigravity/skills/design-taste-frontend/UPSTREAM.md); scripts, imagens e templates upstream não foram incluídos. | [MIT](https://github.com/leonxlnx/taste-skill/blob/main/LICENSE) |
| [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli) | Documentação consultada para o fluxo de browser e exemplos de comandos; o pacote não é empacotado nem redistribuído por este repositório. | [Apache-2.0](https://github.com/microsoft/playwright-cli/blob/main/LICENSE) |

O [LICENSE](LICENSE) na raiz cobre o conteúdo original deste repositório. Os projetos e materiais de terceiros permanecem sob suas respectivas licenças.

## Licença

MIT. Consulte [LICENSE](LICENSE).
