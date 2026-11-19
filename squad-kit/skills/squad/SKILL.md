---
name: squad
description: >-
  Esquadrão de agentes que ENTREVISTA o usuário (stack, banco, Supabase, autenticação,
  integrações, deploy), planeja e constrói uma aplicação ponta a ponta com evidências reais
  de build e testes. Use SOMENTE quando o usuário pedir explicitamente esta skill/squad
  (ex.: "use a skill squad e crie uma aplicação que..."). Não use para perguntas,
  edições pontuais ou tarefas pequenas.
---

# Squad

Transforma um pedido como *"use a skill e crie uma aplicação que faça X"* em uma aplicação quase pronta: entrevista curta → plano enxuto → construção por fatias verticais → verificação com comandos reais → entrega com a lista do que falta configurar.

A skill é **agnóstica de domínio e de stack**. Nada aqui assume um tipo de negócio, banco ou linguagem: tudo vem da entrevista (`references/intake.md`) e é gravado em `.squad/stack.md`.

## Modos

| Modo | Quando | Equipe | Fecha com |
|---|---|---|---|
| **lite** (padrão para "crie/construa uma aplicação") | App novo ou feature grande, quer resultado rápido | 3 papéis: Arquiteto (`pm`+`coord`), Construtor (`backend`/`frontend`/`dba`/`designer` conforme precisar), Verificador (`qa`+`appsec`) | `run_checks` + `audit_code_delivery` + passe do `code_critic_blind` |
| **full** | Pedido explícito de "mesa-redonda", produto grande ou auditoria profunda | Os 11 especialistas em paralelo + 2 críticos + `@Finalizer` | Gate independente do `@Finalizer` |
| **audit** | Projeto existente: diagnosticar, sem construir | Os especialistas relevantes | Roadmap priorizado; espera o usuário escolher itens |

Se o usuário não disser o modo, use **lite** para "crie…" e **audit** para "analise/audite…". Diga qual modo escolheu em uma linha.

## Compatibilidade de ambiente

- **Antigravity:** subagentes pela ferramenta `invoke_subagent`; agentes em `.agents/agents/`.
- **Claude Code:** subagentes pela ferramenta `Agent` (os perfis instalados em `.claude/agents/` são os mesmos arquivos de `agents/`); perguntas ao usuário pela ferramenta de perguntas (`AskUserQuestion`).
- **Sem ferramenta de subagentes:** execute os papéis você mesmo, em sequência, **dizendo explicitamente que não são subagentes independentes**. Nunca apresente papéis simulados como agentes reais.
- **MCP `squad` é opcional.** Com ele, use `inspect_project`, `run_checks`, `audit_*`, `initialize_squad_docs` etc. Sem ele, faça o equivalente por shell (build/test) e leitura direta, e registre que o MCP não estava disponível.

## Passo 0 — Reconhecimento

1. Identifique a raiz do projeto. Se `.squad/stack.md` já existe, leia-o e **não repita perguntas já respondidas**.
2. Projeto existente (brownfield): detecte stack, banco, auth e testes (`inspect_project` ou leitura direta) e **preserve** o que existe. Pergunte apenas o que não der para detectar.
3. Projeto vazio (greenfield): siga para a entrevista.

## Passo 1 — Entrevista (obrigatória antes de construir)

Siga `references/intake.md`. Regras:

- **Uma única rodada** de perguntas, em bloco, com uma opção recomendada em cada uma e sempre com a saída "outro/decida você". Use a ferramenta de perguntas do ambiente quando existir; senão, uma lista numerada.
- **Pule** tudo que o prompt já respondeu ou que o projeto já revela. Pergunte só o que muda materialmente o resultado.
- Bloco obrigatório: **stack** (backend/frontend), **banco** (PostgreSQL próprio, Supabase, SQL Server, SQLite…), **se já existe projeto/integração com Supabase**, **autenticação**, **integrações externas e credenciais disponíveis**, **deploy/ambiente**, **nível de testes**.
- Se o usuário disser "decida você", escolha o perfil recomendado em `references/stacks.md`, registre a decisão e o porquê.
- Máximo de **uma rodada de follow-up**, só para dependências criadas pelas respostas (ex.: "usar Supabase" → "já tem projeto? usar Supabase Auth?").
- Grave o resultado em `.squad/stack.md` (modelo em `templates/stack.template.md`) e mostre um resumo de 5 a 8 linhas ao usuário.

Domínios específicos (um nicho de negócio, uma integração conhecida) **não fazem parte desta skill**: se existir um *domain pack* citado pelo usuário, leia `references/domain-packs.md`. Fora isso, o PM pesquisa só o que o usuário descreveu.

## Passo 2 — Plano

- **lite:** o Arquiteto produz, em `.squad/coordenacao/roadmap.md`, um roadmap curto: objetivo, 3 itens explicitamente fora do MVP, fatias verticais com critérios de aceite verificáveis, modelo de dados, contratos de API, riscos e o que depende de credenciais do usuário. Se houver integração externa, o PM registra a pesquisa em `.squad/produto/pesquisa-de-campo.md` com fontes oficiais, URLs e data de acesso.
- **full / audit:** fan-out real dos especialistas em paralelo (`pm`, `designer`, `design_system`, `coord`, `dba`, `backend`, `frontend`, `frontend_reviewer`, `appsec`, `qa`, `devops`). Cada um grava só o seu relatório (ver `templates/project-docs.md`), sem alterar código. Confirme os relatórios, reenvie só os que falharam, e o `@Coord` consolida o roadmap. No `audit` e no `full`, apresente o roadmap e **espere o usuário escolher os itens**.
- Se a pesquisa web estiver indisponível, marque a pesquisa como pendente; não invente fontes.

## Passo 3 — Construção (lite: continua sem pausar; full: após a escolha de itens)

Um pedido explícito de "crie a aplicação" já autoriza a construção no `lite`. Pare para perguntar apenas se uma decisão ausente mudar materialmente escopo, custo ou risco.

1. **Esqueleto verificável primeiro:** estrutura de projetos, banco com migrations/schema versionado, autenticação, configuração por variáveis de ambiente, `.env.example`, `README` de execução. Rode build antes de seguir.
2. **Fatias verticais**, uma por vez (dado → API → UI → teste). Cada fatia termina com build e testes passando; só então a próxima. Paralelize apenas trabalho independente e nunca edite o mesmo arquivo em paralelo.
3. **Integrações externas:** interface própria + conector por serviço, atrás de configuração. Sem credencial, o app **sobe e mostra estado vazio/aviso de configuração**; nunca dados inventados. Registre no roadmap o que o usuário precisa providenciar (contas, aprovações, chaves).
4. **Design:** `@Designer`/`@design_system` definem direção visual e tokens; use `get_design_reference` e `design-taste-frontend` para referências reais. Estados loading/empty/error/success em toda tela com dados.
5. Atualize relatórios, roadmap e `PROJECT_MAP.md` com **arquivos alterados e resultados reais**. Planejado não é feito.

## Gates de qualidade (valem em todos os modos)

- **Dados reais:** sem KPIs, listas, usuários ou ofertas fixos apresentados como reais. Fixtures só em teste/storybook isolado.
- **Autenticação real** em app privado (servidor, ou RLS/policies quando o backend é Supabase). Frontend sozinho nunca é a barreira de segurança. Chaves privilegiadas jamais no cliente.
- **Persistência real** e schema versionado; "em memória" não conta como concluído.
- **Integração first-party provada:** requisição real do browser/cliente para o backend em execução, com status observado. Mock da própria API não satisfaz o gate.
- **Segredos:** nada de chave em código, relatório ou log; `.env` no `.gitignore`.
- **Linguagem do usuário na UI:** sem nomes de framework/infra.

## Passo 4 — Verificação

- **Sempre:** `run_checks` (ou os comandos equivalentes do perfil em `references/stacks.md`): build, testes unitários e, quando previstos, integração. Anote comando + resultado. Falhou? Corrija e rode de novo; não relativize.
- `audit_code_delivery` e `audit_security_controls` para varreduras mecânicas; trate os achados como pistas, confirme lendo o código.
- UI: `@frontend_reviewer` (ou você, no `lite`) abre o app em browser real via `run_playwright_cli`, em desktop e mobile, e registra screenshots, console e requests.
- `lite`: um passe do `code_critic_blind` sobre o diff. `full`: os dois críticos debatem, depois o `@Finalizer` roda `validate_completion_checklist` e `validate_squad_artifacts`; só declare concluído com `valid: true`. Lacuna = tarefa no roadmap e aceite bloqueado.

## Passo 5 — Entrega

Responda com: o que foi construído e **como rodar** (comandos exatos); o que passou e o que falhou/ficou bloqueado, com evidência; **o que o usuário ainda precisa configurar** (chaves, contas, aprovações, DNS); decisões da entrevista; próximos itens do roadmap. Nunca exiba selo de qualidade sem evidência.

## Referências desta skill

- `references/intake.md` — perguntas, opções e como registrar as respostas.
- `references/stacks.md` — perfis de stack, comandos de build/teste, notas de Supabase.
- `references/domain-packs.md` — como acoplar conhecimento de um nicho sem poluir a skill.
- `templates/` — `stack.template.md`, `project-docs.md`, `roadmap.md`, `agent-report.md`, `PROJECT_MAP.template.md`.
