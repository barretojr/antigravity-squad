# Domain packs

A skill `squad` não contém conhecimento de nicho. Quando um tipo de negócio se repete, crie um **domain pack** à parte (ex.: `skills/<nome-do-dominio>/SKILL.md`) e deixe o squad apenas apontar para ele.

Um domain pack contém só o que é específico do nicho:

- glossário e fluxos principais do negócio;
- modelo de dados de partida (entidades e relações);
- integrações típicas, com links oficiais e restrições de uso;
- regras de negócio e armadilhas conhecidas (políticas das plataformas, consentimento, limites);
- fatias verticais sugeridas e perguntas extras para a entrevista;
- (opcional) trechos de scaffold.

Como o squad usa:

1. Se o usuário citar um domain pack (ou ele já estiver instalado e o pedido for claramente daquele nicho), leia-o depois da entrevista genérica e **acrescente** as perguntas extras dele ao mesmo bloco.
2. As decisões continuam registradas em `.squad/stack.md` e no roadmap.
3. Se não houver pack, o `@PM` pesquisa o domínio a partir da descrição do usuário. Nunca assuma um nicho.

Regra de higiene: se alguma regra, template ou ferramenta do squad mencionar um nicho específico, ela está no lugar errado; mova para o pack.
