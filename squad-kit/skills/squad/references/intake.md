# Entrevista inicial (intake)

Objetivo: decidir, com o mínimo de perguntas, tudo que muda materialmente a aplicação. **Uma rodada**, em bloco. Pule o que o prompt ou o projeto já respondem. Cada pergunta traz uma opção recomendada e a saída "outro / decida você".

No Claude Code use `AskUserQuestion` (até 4 perguntas por chamada; agrupe por tema e faça mais de uma chamada se precisar). No Antigravity, use uma lista numerada curta.

## Bloco 1 — Produto (só se o pedido for vago)

- Qual é o resultado principal para o usuário final e quem usa? (uma frase)
- É app privado (login) ou público? Um usuário ou vários (multi-tenant/equipe)?
- O que deve ficar **fora** do MVP? (se não disser, o Arquiteto propõe 3 cortes)

## Bloco 2 — Stack

- **Backend:** .NET (C#) · Node/TypeScript · Python (FastAPI) · sem backend próprio (BaaS, ex.: Supabase) · outro.
- **Frontend:** React + TypeScript + Vite · Next.js · outro · sem frontend (API apenas).
- Recomendação padrão quando o usuário diz "decida": **.NET + React + PostgreSQL** (ou Supabase, ver abaixo). Se o usuário disser que tem mais familiaridade com uma linguagem, use-a.

## Bloco 3 — Banco de dados

- **PostgreSQL próprio** (Docker local; migrations pelo ORM) · **Supabase** (Postgres gerenciado + Auth/Storage/Realtime) · SQL Server · SQLite (protótipo local) · outro.
- Se escolher **Supabase**, perguntar (follow-up permitido):
  1. Já existe um projeto Supabase? Pode informar URL e `anon key` por `.env` (nunca a `service_role` no chat; ela fica só no servidor).
  2. Usar **Supabase Auth** ou autenticação própria?
  3. O acesso aos dados será **direto do frontend com RLS** (sem backend próprio) ou **via API própria** que usa o Postgres do Supabase?
  4. Precisa de Storage, Realtime ou Edge Functions?
  5. Desenvolvimento local com `supabase start` (Docker) ou direto no projeto na nuvem?
- Se escolher **PostgreSQL/SQL Server próprio**: já tem instância ou sobe via Docker Compose? Qual versão?

## Bloco 4 — Autenticação e acesso

- E-mail + senha · login social (qual provedor) · link mágico · Supabase Auth · sem login.
- Papéis/permissões? (ex.: admin e usuário comum)
- Recuperação de senha e verificação de e-mail são necessárias?

## Bloco 5 — Integrações externas

- Quais serviços externos o produto precisa consumir ou acionar? (lista livre; pode ser nenhuma)
- Para cada um: já tem conta/credenciais/aprovação? Existe ambiente de teste (sandbox)?
- Regra: sem credencial o app sobe com estado vazio e aviso de configuração. O Arquiteto registra no roadmap o que depende do usuário.
- Há tarefas em segundo plano (agendadas, filas, webhooks)? Tempo real?

## Bloco 6 — Execução e qualidade

- **Onde roda:** local (Docker) · nuvem (qual?) · ainda não sei. Windows, Linux ou ambos?
- **Nível de testes:** básico (build + unitários) · completo (+ integração com banco real + E2E no browser). Recomendado: completo para o fluxo principal.
- **Design:** referência visual desejada (marcas do catálogo `get_design_reference`), idioma da interface, existência de marca/logo.

## Como registrar

Preencha `.squad/stack.md` a partir de `templates/stack.template.md`, com a escolha, o motivo e o que ficou "decidido pelo squad". Mostre ao usuário um resumo de 5 a 8 linhas e siga. Só volte a perguntar se uma resposta criar uma dependência nova.
