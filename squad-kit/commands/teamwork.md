---
description: Atalho compatível para iniciar a mesa-redonda antes de executar itens do roadmap.
---

# Alias `/teamwork`

Demanda do usuário: `$ARGUMENTS`

Encaminhe a demanda para `squad-kit/skills/squad/SKILL.md` e siga integralmente seu fluxo de planejamento, fan-out dos onze agentes, relatórios em `.squad/` e roadmap antes de qualquer implementação. Não mantenha um workflow paralelo aqui.
The execution flow MUST invoke `@Finalizer` after code review and QA. The finalizer is independent of implementation, writes `qualidade/finalizer.md`, and must pass `validate_completion_checklist` before the app can be declared complete. No final approval without row-by-row evidence; missing evidence becomes roadmap tasks.
