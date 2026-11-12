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

## Estrutura

```text
.antigravity/
├── agents/                 # onze perfis de agente
├── commands/               # alias /teamwork
├── rules/                  # contexto e limites compartilhados
└── skills/                 # skill principal, skills de domínio e templates
```

## Métodos de frontend

Design System transforma a direção visual em tokens, componentes, estados e regras específicas do produto. Taste-skill orienta direção de arte sem impor uma linguagem visual universal. Playwright CLI dá ao Frontend Reviewer um fluxo de browser para avaliar responsividade, hierarquia, console e requests.

Referências: [awesome-design-md](https://github.com/voltagent/awesome-design-md), [taste-skill](https://github.com/leonxlnx/taste-skill) e [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli).

## Licença

MIT. Consulte [LICENSE](LICENSE).