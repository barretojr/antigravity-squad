---
trigger: manual
description: Regras do Squad (evidências, dados reais, autenticação, persistência, integrações). Aplique só quando a skill squad estiver em uso.
---

# Regras do Squad

> Estas regras **não** são mais `always_on`: valem apenas dentro do fluxo da skill `squad` (a skill as referencia). Prompts comuns não são afetados.

1. **Entrevista antes de construir:** stack, banco, autenticação, integrações e deploy são decididos com o usuário (`references/intake.md`) e gravados em `.squad/stack.md`. Nunca assuma uma stack, um banco ou um domínio de negócio que o usuário não escolheu ou que o projeto existente não tenha.
2. **Duas fases no modo `full`, uma no `lite`:** no `full` os agentes planejam em paralelo e o `@Coord` consolida o roadmap antes de qualquer código. No `lite`, o plano é curto e a construção começa em seguida. Em ambos, só implemente o que o usuário pediu/aprovou e registre evidências reais.
3. **Brownfield:** preserve a stack encontrada no projeto; não migre tecnologia incidentalmente.
4. **Autenticação obrigatória em apps privados:** autenticação e autorização no servidor (ou por RLS/policies, quando o backend for um BaaS como Supabase), hashing seguro de senhas quando houver senha própria, sessão/tokens protegidos. Nada de login só visual nem guarda apenas no frontend.
5. **Integrações e credenciais:** todo serviço externo que o produto consome tem API oficial mapeada pelo `@PM`, credenciais fora do código (variáveis de ambiente/segredos ou tela de configuração com criptografia) e comportamento definido sem credenciais (estado vazio, nunca dado inventado). Chaves privilegiadas (ex.: `service_role`) nunca vão para o frontend.
6. **Persistência real (DBA):** é proibido dar persistência como CONCLUÍDA se os dados estiverem só em memória. O `@DBA` documenta onde e como os dados residem (PostgreSQL, Supabase, SQL Server, SQLite etc.) e como o schema é versionado (migrations).
7. **Sem jargão técnico e sem métricas falsas na UI:** a interface fala a língua do negócio. Proibido exibir nomes de stack/framework/infraestrutura e números, listas ou KPIs fixos apresentados como reais. Sem dados, mostre estado vazio.
8. **Rigor:** nunca reporte teste, pesquisa, debate ou implementação que não aconteceu. Cada teste citado traz o comando exato e o resultado observado. AppSec distingue análise teórica de teste ativo.
9. **Pasta única de documentação:** `.squad/` guarda relatórios, stack, roadmap e evidências. `.agents/` é configuração do Antigravity. Não use `.agentes`.
10. **Críticos adversariais:** no `full`, `code_critic_blind` e `code_critic_spec`. No `lite`, um passe do `code_critic_blind` mais `audit_code_delivery`.
11. **Gate de conclusão:** no `full`, `@Finalizer` independente + validadores do MCP. No `lite`, `run_checks` com build/testes reais e `audit_code_delivery` limpos. Lacunas viram tarefas e bloqueiam o aceite.
12. **Aplicabilidade por stack:** relate UI embutida e o inventário real de projetos. LocalDB/Visual Studio só se aplica a .NET no Windows; nas demais stacks marque N/A com motivo. Teste unitário não prova integração.
