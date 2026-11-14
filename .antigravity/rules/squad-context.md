---
trigger: always_on
description: Regras do Antigravity Squad para stack, evidências, integração real, autenticação com criptografia e blindagem de UX.
---

# Regras do Squad

1. **Ciclo de Entrega em Duas Fases:** Em planejamento, os onze subagentes analisam em paralelo e salvam seus relatórios em `.agentes/`. `@Coord` consolida o roadmap único em `.agentes/coordenacao/roadmap.md`. Não altere código do produto nessa fase. Em execução, implemente apenas itens aprovados pelo usuário e registre evidências reais.
2. **Stack de Referência & Brownfield:** Mantenha a stack de referência (.NET 10, PostgreSQL 17, React 19). Em projetos brownfield existentes, preserve rigorosamente a stack encontrada sem migrações arbitrárias.
3. **Autenticação Obrigatória com Criptografia:** Toda aplicação privada deve incluir autenticação e autorização no servidor. Mesmo quando contas de teste forem pré-semeadas (mockadas) no backend, o fluxo DEVE utilizar hashing seguro de senhas (BCrypt, Argon2, PBKDF2), geração de tokens/sessão criptograficamente protegidos e políticas de autorização reais.
4. **Mapeamento de Integrações & Gestão de Credenciais:** Todo produto que consome serviços externos (APIs de Marketplaces, WhatsApp Business, Gateways) deve ter as APIs oficiais mapeadas pelo `@PM` e prever módulo/tela de Configurações de Conexões para cadastro seguro de chaves de API, tokens e webhooks.
5. **Transparência de Persistência Física (DBA):** É proibido aprovar persistência como CONCLUÍDA se os dados estiverem apenas em memória RAM (`List<T>`). O `@DBA` deve documentar onde e como os dados residem fisicamente (PostgreSQL, SQLite, migrações ativas).
6. **Zero Tech-Jargon na UI (Anti-Vício de Dev):** A interface do usuário deve falar exclusivamente a linguagem do negócio e do usuário final. É estritamente proibido exibir nomes de stacks, frameworks ou jargões de infraestrutura na UI (ex.: `.NET 10`, `React 19`, `no Backend`, `API Conectada`). O status do sistema deve ser informativo e humanizado.
7. **Rigor e Proibição de Alucinação:** QA registra testes efetivamente executados com comandos e resultados. AppSec distingue análise teórica de teste ativo. Nunca reporte teste, pesquisa, debate ou implementação que não aconteceu.
8. **Separação de Pastas:** `.agents/` contém customizações nativas do Antigravity. `.agentes/` contém os artefatos de documentação e roadmap do projeto. Não confunda os dois.
