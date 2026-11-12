---
trigger: always_on
description: Regras do Antigravity Squad para stack, evidências, integração real e autorização de execução.
---

# Regras do Squad

- Em planejamento, invoque os onze subagentes em paralelo e salve um relatório por agente na pasta `.agentes/` do projeto. Gere um roadmap único em `.agentes/coordenacao/roadmap.md` e aguarde o usuário escolher itens. Não altere código do produto nessa fase.
- Em execução, implemente apenas os itens escolhidos e atualize relatórios com arquivos, comandos e resultados reais.
- Mantenha a stack de referência (.NET 10, PostgreSQL 17, React 19); em brownfield preserve a stack existente e não migre incidentalmente.
- Para aplicação privada, login e autorização server-side são requisitos padrão. Frontend consome backend first-party real. Proibido mock de dados ou autenticação em runtime; ausência de dados resulta em estado vazio.
- QA registra testes efetivamente executados. AppSec distingue análise de teste ativo. Nunca reporte teste, pesquisa, debate ou implementação que não aconteceu.
- `.agents/` contém customizações nativas do Antigravity. `.agentes/` contém artefatos do projeto. Não confunda os dois.