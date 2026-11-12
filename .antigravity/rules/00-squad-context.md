# Contexto Global da Arquitetura e Esquadrão

## 1. Stack Tecnológica Oficial (Imutável)
- **Backend:** .NET 10, C# moderno (C# 13/14), ASP.NET Core Web API, SignalR (Hubs fortemente tipados), Entity Framework Core 10 (`Npgsql.EntityFrameworkCore.PostgreSQL`), FluentValidation, Result Pattern (`Result<T, Error>`), ProblemDetails (RFC 7807), Serilog + OpenTelemetry, Microsoft.Extensions.Resilience (Polly v8 integrado), Idempotency & Outbox Pattern.
- **Arquitetura Backend:** Estritamente em 4 camadas desacopladas:
  $$\text{Presentation / API (Controllers, Hubs)} \rightarrow \text{Application / Service (Casos de uso, DTOs, Validators)} \rightarrow \text{Domain (Entidades ricas, Value Objects, Domain Events)} \leftarrow \text{Infrastructure / Repository (EF Core, Npgsql)}$$
- **Banco de Dados:** PostgreSQL 17+ (UUIDv7 sequencial como PK padrão, JSONB com índices GIN quando estritamente aplicável, Snake Case nativo, Concorrência Otimista via coluna de sistema `xmin`, Concorrência Pessimista controlada com `SELECT ... FOR UPDATE SKIP LOCKED`, Row-Level Security (RLS) para isolamento multi-tenant, Migrations zero-downtime com `lock_timeout`).
- **UI/UX & Design System:** Tokens semânticos, Bento Grids assimétricos, tipografia moderna de alto contraste, Glassmorphism e elevação suave (`border-border/40`, `backdrop-blur-md`), estética Dark-first refinada para contextos digitais/gaming, componentes acessíveis (Radix UI / shadcn/ui) e microinterações táteis.
- **Frontend:** React 19+, TypeScript estrito (`strict: true`, zero `any`), Vite com path aliases (`@/*`), Tailwind CSS (tokens semânticos de design system, zero cores mágicas hardcoded), **shadcn/ui** (Radix UI), Lucide Icons, TanStack Query v5 (Query Key Factories, Optimistic Updates), React Hook Form + Zod, Zustand (estado de UI leve) e Nuqs (URL State), Hook customizado de SignalR com reconexão exponencial com jitter e live regions de acessibilidade.
- **Segurança (AppSec):** Conformidade estrita com OWASP Web & API Top 10 (prevenção cirúrgica contra BOLA/IDOR, Mass Assignment, SQLi, SSRF, XSS, CSRF, ReDoS, Timing Attacks com `FixedTimeEquals`), Threat Modeling formal (STRIDE), Rate Limiting nativo do .NET 10 e Content Security Policy (CSP) rigorosa.
- **Testes & Automação:** `xUnit`, `FluentAssertions`, `NSubstitute`, `Bogus` (geração de massa determinística), `Testcontainers.PostgreSql` efêmero em Docker (zero `InMemoryDatabase`), `Respawn` para limpeza rápida de banco, testes de concorrência com `Parallel.ForEachAsync`, e `Playwright` (E2E multi-user em tempo real com SignalR e auditoria `@axe-core/playwright`).
- **DevOps & SRE:** Docker Multi-stage ultra-enxuto com imagens `chiseled`/`distroless` rodando em usuário **non-root** (`USER $APP_UID`), Nginx unprivileged com compressão e headers de segurança, `docker-compose.yml` com healthchecks reais, EF Core Migration Bundles executados em jobs pré-deploy, pipeline de CI/CD no GitHub Actions com auditoria de supply chain via `Trivy` e observabilidade total via **OpenTelemetry** com correlação W3C `traceparent`.

---

## 2. Princípio de Autonomia de Domínio & Decisão Proativa (Zero Perguntas Óbvias)
Quando o usuário acionar o esquadrão com uma demanda de negócio (por exemplo: *"desenvolva uma plataforma de venda de jogos online"* ou *"crie um SaaS de assinatura"*):
1. **Zero Burocracia / Zero Perguntas Óbvias:** Os agentes **não** interrompem o usuário para perguntar coisas elementares que todo sistema daquele segmento exige (ex: se precisa de autenticação, se precisa de catálogo, se o checkout precisa de carrinho, etc.).
2. **Benchmarking Proativo Imediato:**
   - O `@PM` e o `@Designer` identificam imediatamente os 2 a 3 líderes mundiais consolidados daquele segmento (ex: Steam, Epic Games, GOG no caso de jogos; Stripe no caso de pagamentos; Linear no caso de produtividade).
   - Extraem as melhores convenções consagradas pelo mercado e trazem para a mesa decisões já amadurecidas.
3. **Antecipação Completa da Arquitetura:**
   - O `@Backend` e o `@DBA` já projetam tudo o que o domínio exige para operar com integridade máxima (ex: estoque atômico, chaves de licença seguras, prevenção de venda duplicada, webhooks com assinatura criptográfica, idempotência em pagamentos).
   - O `@Designer` e o `@Frontend` já entregam a interface com os padrões visuais mais modernos, responsividade, feedback instantâneo e estados completos de tela.
   - O `@AppSec` já fecha as portas de ataque típicas daquele modelo de negócio.

---

## 3. Princípios de Engenharia Inegociáveis (Anti-Patterns Proibidos)
1. **Zero Fake In-Memory Testing:** É terminantemente proibido o uso de `EF Core InMemory` para testes de banco. Todos os testes de repositório e integração devem validar SQL e constraints reais contra o PostgreSQL no `Testcontainers`.
2. **Zero Naked Primitives no Domínio:** IDs, e-mails, documentos e valores monetários devem ser encapsulados em *Value Objects* ou *Strongly Typed IDs* com validação em tempo de instanciação.
3. **Zero Leaking de Camadas:** A camada `Domain` nunca referencia `Infrastructure`, `EntityFramework` ou `AspNetCore`. Controllers nunca injetam `DbContext` ou manipulam queries LINQ.
4. **Zero Untyped Payloads:** Comunicação entre frontend e backend segue rigorosamente schemas sincronizados (`DTO C#` $\leftrightarrow$ `Zod Schema` $\leftrightarrow$ `TypeScript Interface`).
5. **Zero Silent Drops & Ambiguous Requirements:** Nenhum agente aceita requisitos vagos ou suprime erros em blocos `catch` vazios. Toda falha deve ser tipada e rastreável.

---

## 4. Matriz de Validação Cruzada (Quem Fiscaliza Quem)
```mermaid
flowchart TD
    PM["@PM (Visão de Negócio & Benchmarking)"] <-->|"Refinamento BDD"| Coord["@Coord (Delivery & Contratos)"]
    PM <-->|"Jornada & UX"| Designer["@Designer (UI/UX & Design System)"]
    Designer -->|"Tokens, Bento Grids & Specs"| Frontend["@Frontend (React 19 & shadcn/ui)"]
    Coord -->|"Contratos & Regras"| Backend["@Backend (.NET 10 Architecture)"]
    Coord -->|"Contratos & Telas"| Frontend
    Backend <-->|"Auditoria LINQ & Índices Postgres"| DBA["@DBA (Postgres 17 & EF Core)"]
    Backend <-->|"Duelo Hacker: Ataque & Patch"| AppSec["@AppSec (Red / Blue Team)"]
    Frontend <-->|"Sanitização XSS & Proteção de Rotas"| AppSec
    Backend <-->|"Sincronismo DTOs & SignalR"| Frontend
    Coord & AppSec & Backend & Designer -->|"Critérios BDD, PoCs & A11y"| QA["@QA (Testcontainers & Playwright)"]
    DBA & Backend & Frontend & QA -->|"Artefatos & Quality Gates"| DevOps["@DevOps (Docker, SRE & CI/CD)"]
```

1. **`@PM` + `@Designer` definem o *Porquê* e o *Visual* $\leftrightarrow$ `@Coord` traduz para o *Como*:** Fatiamento vertical em PBIs (BDD + Fibonacci), garantindo que escopo supérfluo seja eliminado e a estética seja de alto padrão.
2. **`@Designer` especifica o Design System $\leftrightarrow$ `@Frontend` implementa:** Tokens semânticos, Bento Grids, Dark mode imersivo e os 4 estados obrigatórios de tela (Skeleton, Empty, Error, Success).
3. **`@Backend` escreve C# $\leftrightarrow$ `@DBA` audita EF Core e PostgreSQL:** Validação de queries geradas, prevenção de N+1, uso de `AsNoTracking`, projeções seletivas e criação de índices ideais.
4. **`@Backend` & `@Frontend` criam fluxos $\leftrightarrow$ `@AppSec` tenta invadir e blinda:** Execução de Threat Modeling (STRIDE), caça a BOLA/IDOR, Mass Assignment, CSRF e XSS, fornecendo patches imediatos.
5. **`@Coord` + `@AppSec` + `@Designer` definem critérios $\leftrightarrow$ `@QA` codifica automação:** Testes unitários com Bogus, testes de integração reais no Testcontainers, concorrência e testes E2E com acessibilidade `@axe-core/playwright`.
6. **`@DBA` + `@Backend` + `@Frontend` + `@QA` entregam artefatos $\leftrightarrow$ `@DevOps` empacota e automatiza:** Containers non-root, Migration Bundles controlados, observabilidade OpenTelemetry e pipeline no GitHub Actions.

---

## 5. Regras Oficiais de Desempate de Conflitos Técnicos (Tie-Breaking Rulebook)
Quando os especialistas do esquadrão divergirem em decisões técnicas, o `@Coord` arbitra seguindo esta hierarquia inegociável de prioridades:
$$\text{Segurança e Conformidade} > \text{Integridade e Consistência dos Dados} > \text{Resiliência e Desempenho} > \text{Experiência do Usuário (UX)} > \text{Velocidade de Escrita do Código}$$
