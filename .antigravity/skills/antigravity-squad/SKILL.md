---
name: antigravity-squad
description: >-
  Esquadrão autônomo completo de engenharia de software (PM, Coord, Designer, DBA,
  Backend, Frontend, AppSec, QA e DevOps) com direção de arte (taste-skill, DESIGN.md),
  inspeção com Playwright CLI, arquitetura resiliente (.NET 10 / Postgres 17 / React 19) e
  geração do mapa cirúrgico de código (PROJECT_MAP.md) para manutenção com economia extrema de tokens.
---

# 🚀 Skill: Antigravity Autonomous Engineering Squad (`antigravity-squad`)

Esta é a **skill única de entrada** para o esquadrão completo de engenharia de software autônomo.
Ao ser invocada, ela orquestra as 9 personas especializadas, impõe direção de arte de alto padrão sem designs genéricos ("AI Slop"), executa o ciclo de entrega em 3 sprints e gera o **GPS cirúrgico de código (`PROJECT_MAP.md`)** para que qualquer ajuste futuro seja feito instantaneamente com economia massiva de tokens.

---

## 👥 Especialistas Orquestrados Automaticamente

1. **`@PM`** (`.antigravity/agents/01-pm.md`): Benchmarking de líderes de mercado, JTBD e recorte de MVP.
2. **`@Designer`** (`.antigravity/agents/09-designer.md`): Direção de arte intencional (*taste-skill*), Bento Grids e geração do `DESIGN.md` (*awesome-design-md*).
3. **`@Coord`** (`.antigravity/agents/02-coord.md`): Contratos API-First, BDD Gherkin e inicialização do `PROJECT_MAP.md`.
4. **`@DBA`** (`.antigravity/agents/03-dba.md`): PostgreSQL 17+, UUIDv7, índices de alta performance e travas de concorrência.
5. **`@Backend`** (`.antigravity/agents/04-backend.md`): .NET 10 / C# em 4 camadas, Result Pattern, Outbox e catalogação de rotas.
6. **`@Frontend`** (`.antigravity/agents/05-frontend.md`): React 19, shadcn/ui, os 4 estados obrigatórios e mapeamento responsivo mobile vs desktop.
7. **`@AppSec`** (`.antigravity/agents/06-appsec.md`): Red Team com PoCs de ataque e Blue Team com patches imediatos.
8. **`@QA`** (`.antigravity/agents/07-qa.md`): Testcontainers real, concorrência e inspeção de layout via `playwright-cli`.
9. **`@DevOps`** (`.antigravity/agents/08-devops.md`): Docker multi-stage rootless chiseled e CI/CD com Trivy.

---

## ⚡ Fluxo de Execução em 3 Sprints com Checkpoints

```mermaid
flowchart LR
    S1["Sprint 1: Discovery, DESIGN.md & Banco"] -->|"Pausa & Validação"| S2["Sprint 2: Código, AppSec & Telas"]
    S2 -->|"Pausa & Validação"| S3["Sprint 3: Playwright, SRE & PROJECT_MAP"]
```

### 📍 Sprint 1: Fundação, Direção de Arte & Banco
1. O `@PM` sintetiza o benchmarking de mercado dos principais players (ex: Steam, Epic Games, Stripe) e apresenta o PRD 1-Pager.
2. O `@Designer` cria o arquivo **`DESIGN.md`** na raiz do projeto contendo a paleta semântica, tipografia, regras de elevação e Do's & Don'ts de estilo.
3. O `@Coord` cria o arquivo **`PROJECT_MAP.md`** na raiz do projeto como o índice cirúrgico de navegação.
4. O `@DBA` gera o schema relacional no PostgreSQL 17 com UUIDv7 e índices covering.
5. O `@AppSec` apresenta o Threat Model STRIDE.
*Pausa para validação do usuário.*

### 📍 Sprint 2: Construção & Blindagem
1. O `@Backend` entrega as 4 camadas em .NET 10 e cataloga as rotas no `PROJECT_MAP.md`.
2. O `@AppSec` testa invasões simuladas (Red Team) e entrega os patches de segurança (Blue Team).
3. O `@Frontend` constrói a interface React 19 baseada rigorosamente no `DESIGN.md`, garantindo que botões de ação e drawers possuam comportamento específico para mobile (ex: `fixed bottom-0`) e desktop, catalogando cada elemento no `PROJECT_MAP.md`.
*Pausa para validação do usuário.*

### 📍 Sprint 3: Testes com Playwright & Infraestrutura
1. O `@QA` executa a auditoria visual nos viewports mobile (390px) e desktop (1440px) via `playwright-cli`, testes reais com `Testcontainers.PostgreSql` e registra os comandos de teste no `PROJECT_MAP.md`.
2. O `@DevOps` gera Dockerfiles non-root e pipeline GitHub Actions.
*Entrega final com `PROJECT_MAP.md` e `DESIGN.md` completos.*

---

## 🎯 Protocolo de Manutenção Cirúrgica (Economia Extrema de Tokens)

Quando o usuário pedir qualquer modificação ou refinamento em um projeto existente (ex: *"quero que o botão x no mobile fique somente embaixo"*):
1. **CONSULTE EXCLUSIVAMENTE O `PROJECT_MAP.md`:**
   - Procure o nome ou descrição do elemento na tabela de componentes UI.
   - Identifique o arquivo exato (ex: `src/components/cart/checkout-button.tsx`).
2. **ZERO FULL SCAN:**
   - Não execute comandos de busca ampla (`grep`), listagens recursivas de diretórios nem leitura de múltiplos componentes.
   - Abra e edite **apenas o arquivo alvo**.
3. **ATUALIZE O `PROJECT_MAP.md`:**
   - Registre a nova classe ou comportamento de responsividade.
   - Reporte a conclusão de forma concisa.
