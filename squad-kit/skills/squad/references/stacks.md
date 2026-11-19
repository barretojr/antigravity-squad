# Perfis de stack

Use o perfil escolhido na entrevista. Em brownfield, o perfil é o que o projeto já usa. Os comandos abaixo são os que `run_checks` tenta detectar; confirme no projeto antes de depender deles.

## A. .NET + React + PostgreSQL (recomendado se o usuário prefere .NET)

- Estrutura: `src/Api` (+ Domain/Application/Infrastructure quando o tamanho justificar), `client/` (React + TS + Vite), `tests/`.
- Dados: EF Core + Npgsql, migrations (`dotnet ef migrations add`, `dotnet ef database update`), PostgreSQL via `docker compose`.
- Auth: ASP.NET Identity ou JWT com hashing do `PasswordHasher`; `[Authorize]` nas rotas de mutação.
- Build/test: `dotnet build`, `dotnet test`; cliente: `npm ci`, `npm run build`, `npm test`.
- Integração: `WebApplicationFactory` + Testcontainers (PostgreSQL real). E2E: Playwright.
- Aplicabilidade: LocalDB/Visual Studio só se aplica se o banco for SQL Server em Windows; com PostgreSQL marque N/A com motivo.

## B. .NET + React + Supabase

- Banco: Postgres do Supabase. A API .NET conecta com Npgsql na connection string do Supabase (use o *pooler* em ambientes serverless/curtos) ou o frontend usa `supabase-js` só para o que for seguro por RLS.
- Auth: Supabase Auth no frontend; a API .NET **valida o JWT do Supabase** (JWKS/segredo do projeto) e autoriza no servidor. Alternativa: auth própria e Supabase só como Postgres.
- Schema: migrations versionadas (Supabase CLI `supabase migration new` / `supabase db push`, **ou** EF Core; não os dois sem combinar). RLS habilitado em toda tabela exposta.
- Segredos: `service_role` só no servidor; `anon key` pode ir ao cliente, protegida por RLS.
- Dev local: `supabase start` (Docker) para ter Postgres/Auth locais.
- Build/test igual ao perfil A; testes de RLS com dois usuários.

## C. React + Supabase (sem backend próprio)

- O frontend fala direto com o Supabase; **a segurança é RLS + policies** testadas. Lógica sensível, segredos e integrações externas vão para **Edge Functions** ou um pequeno backend.
- Auth: Supabase Auth. Tipos gerados pelo CLI (`supabase gen types`).
- Build/test: `npm ci`, `npm run build`, `npm test`; E2E Playwright contra o projeto local (`supabase start`).
- Gate de "autorização no servidor" = policies de RLS verificadas com pelo menos dois usuários (BOLA/IDOR).

## D. Node/TypeScript (Fastify ou NestJS) + React/Next + PostgreSQL ou Supabase

- ORM: Prisma ou Drizzle, com migrations. Validação de entrada (Zod).
- Auth: JWT/sessão com hashing (argon2/bcrypt) ou Supabase Auth.
- Build/test: `npm ci`, `npm run build`, `npm test` (Vitest/Jest); integração com Testcontainers ou banco local em Docker; E2E Playwright.

## E. Python (FastAPI) + React + PostgreSQL ou Supabase

- SQLAlchemy/SQLModel + Alembic; Pydantic para contratos.
- Build/test: `pytest`; cliente como no perfil D.

## F. SQLite (protótipo)

- Só para protótipo local; avise que não é o destino de produção. Use migrations mesmo assim.

## Regras comuns

- `docker-compose.yml` para dependências locais (banco etc.) quando não for Supabase gerenciado.
- `.env.example` completo e `.env` no `.gitignore`.
- README de execução com os comandos exatos, validados.
- CI mínimo (build + testes) quando o usuário escolher nuvem/GitHub.
