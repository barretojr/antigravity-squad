---
name: antigravity-squad
description: >-
  Planeja produto e engenharia com onze subagentes nativos em paralelo, pesquisa
  mercado, integra frontend a APIs reais e gera roadmap e relatórios rastreáveis.
  Stack de referência: .NET 10, PostgreSQL 17 e React 19. Use para descoberta,
  auditoria, roadmap ou execução de itens escolhidos.
---

# Antigravity Squad

Coordene uma mesa-redonda de onze especialidades. O fluxo padrão tem duas fases:

1. **Planejamento:** os onze subagentes analisam em paralelo e cada um grava seu relatório `.md` no projeto. `@Coord` consolida as decisões num roadmap único. Não altere código de produto nessa fase.
2. **Execução:** aguarde o usuário escolher itens do roadmap. Implemente somente os itens selecionados e atualize nos relatórios o que foi realmente feito e validado.

## Stack de referência

Mantenha foco em .NET 10/C#, PostgreSQL 17+/Npgsql e React 19/TypeScript/Vite/shadcn-ui. Inclua xUnit, Testcontainers, Playwright, Docker e GitHub Actions quando fizerem parte do produto.

Em greenfield, use essa stack. Em brownfield, identifique e preserve a stack existente; não migre tecnologia incidentalmente. Em novas partes do produto, priorize os componentes da stack de referência e convenções compatíveis. Registre incompatibilidades e decisões no roadmap.

## Fase 1 — rodada real com os onze agentes

Para pedido de ideia, discovery, auditoria, evolução ou roadmap:

1. Identifique a raiz do projeto e os arquivos de solução. Descubra o que existe em `client`, `src` e `tests`, a stack e as integrações. Use `PROJECT_MAP.md` como índice auxiliar, confirmando informações antes de depender dele.
2. Separe o workspace de código (`.agents/`, configuração nativa Antigravity) dos artefatos de trabalho do produto (`.agentes/`). Não grave os relatórios de produto dentro dos arquivos de configuração da skill.
3. Crie no projeto a estrutura de documentação definida em `templates/project-docs.md` e preencha `.agentes/README.md` com a demanda, versão/data, links dos onze relatórios e estado do roadmap.
4. Invoque de verdade, pela ferramenta `invoke_subagent`, os onze custom subagents **em paralelo numa única fan-out**: `pm`, `designer`, `design_system`, `coord`, `dba`, `backend`, `frontend`, `frontend_reviewer`, `appsec`, `qa` e `devops`. Use o workspace compartilhado/herdado para que os relatórios fiquem no projeto. Passe a todos o mesmo briefing, evidências úteis e limites da fase.
5. Atribua a cada subagente um único arquivo de relatório, um domínio e um recorte. Eles podem criar/editar seu relatório e artefatos de planejamento atribuídos; não podem alterar código, executar migrações, inventar dados, ou escrever no relatório de outro agente nesta fase. O `@Coord` registra dependências preliminares no próprio relatório; o roadmap final vem depois da rodada.
6. Aguarde os onze resultados. Confirme que os onze relatórios existem, têm conteúdo, distinguem fato de hipótese e incluem estado `PLANEJADO`. Se um agente falhar, reenvie somente a tarefa que falhou. Nunca apresente papéis simulados como subagentes reais.
7. Envie ao `@Coord` um resumo e os onze relatórios para uma consolidação posterior. Ele cria `.agentes/coordenacao/roadmap.md`, mantendo ligações entre requisito, agente responsável, APIs, dados, interface, segurança e testes. Faça uma revisão final de consistência e aceite o roadmap só com critérios verificáveis.
8. Apresente o roadmap e o índice `.agentes/README.md` no chat; encerre esperando o usuário selecionar os itens para executar.

Se a ferramenta de subagentes ou os onze nomes não estiverem disponíveis, interrompa a afirmação de “mesa-redonda completa”, informe quais não foram executados e não finja resultados. Se pesquisa web estiver indisponível, marque a pesquisa como pendente em vez de inventar fontes ou padrões.

## Pesquisa de produto obrigatória

Em ideias de produto, features de negócio e auditorias com dimensão competitiva, `@PM` pesquisa os padrões atuais de 3 a 5 produtos reais do domínio e padrões operacionais do segmento. Use fontes primárias sempre que possível. Registre URLs diretas, data de acesso, padrão observado, implicação para o produto e o que foi descartado. Separe fatos, inferências e recomendações. `@Coord` consolida as decisões e o contexto do mercado no roadmap, referenciando a pesquisa do PM em vez de duplicá-la.

## Autenticação e dados reais como gates

- Para dashboard privado, SaaS ou ferramenta de operação, inclua login/autenticação, sessão, logout, recuperação de acesso e autorização como requisitos de primeira classe, salvo se o usuário definir explicitamente uma experiência pública/sem conta. Registre a premissa em produto, UX, backend, segurança e QA.
- Não aceite telas de login apenas visuais, guardas apenas no frontend, APIs sem autorização correspondente ou identidade simulada em runtime.
- A aplicação não pode apresentar KPIs, ofertas, usuários, listas ou estados fixos como se fossem dados reais. Sem dados no backend, mostre estado vazio. Mocks e fixtures ficam restritos a testes ou storybook isolado e nunca servem como integração de aceite.
- O frontend deve consumir APIs reais do backend com contratos acordados, cliente HTTP tipado, configuração de ambiente, tratamento de sessão e estados loading/empty/error/success. Se o endpoint ainda não existe, registre contrato, dependência e tarefa Backend; não crie arrays locais para esconder a lacuna.
- QA só considera integração provada quando verifica requisições reais do browser para o backend executando e respostas coerentes. Testes podem usar fixtures no banco de teste; mocks do primeiro-party API não satisfazem o gate de integração.

## Direção visual e marca

Antes da implementação, `@Designer` entrega em `.agentes/design/direcao-visual-e-marca.md` direção visual, fluxos/telas e pelo menos duas ideias de marca/wordmark/ícone com justificativa. `@design_system` converte essa direção em `.agentes/design/DESIGN.md`, incluindo tokens, tipografia, componentes, estados, responsividade e regras de consistência, com referências documentadas. Inclua login e estados funcionais do produto quando aplicável. Não reutilize logos de terceiros nem escolha estética por moda. Use `design-reference` e `design-taste-frontend` para pesquisar referências e orientar arte específica ao produto; `antigravity-design-expert` é repertório opcional quando combinar com o domínio. Vidro, 3D, parallax e animação não são padrões obrigatórios.

## Artefatos por agente

Cada subagente escreve e mantém o arquivo atribuído em `.agentes/` indicado em `templates/project-docs.md`. Todo relatório tem as seções `Contexto e evidências`, `O que precisa ser feito`, `Plano/Dependências`, `O que foi feito`, `Validação/Evidências` e `Pendências`. Na fase 1, `O que foi feito` diz explicitamente `Nenhuma implementação de produto nesta fase`; não antecipe trabalho. Na execução, atualize o mesmo relatório com item do roadmap, arquivos alterados, comandos/resultados reais e limitações. Não marque como feito algo que apenas foi planejado.

## Roadmap e solução .NET

O roadmap único fica em `.agentes/coordenacao/roadmap.md`, com IDs, prioridade, resultado, escopo, dependências, critérios de aceite, validação, risco e responsáveis. Faça slices verticais que conectem frontend, backend e dados.

`@Coord` verifica `.slnx` e os projetos reais. Se `client` contém projeto reconhecido pelo .NET/Visual Studio, inclua-o na solução na etapa de execução e confirme com `dotnet sln <solucao>.slnx list`; não passe uma pasta solta ou `package.json` a `dotnet sln add`. Se o cliente for React sem projeto .NET, mantenha-o como projeto frontend e registre essa relação. Quando fizer sentido e o formato existente aceitar, liste os documentos `.agentes/*.md` como Solution Items para ficarem visíveis na solução; não os declare como projetos compiláveis. Alterações no `.slnx` são tarefas de execução, não da rodada de planejamento.

## Fase 2 — execução escolhida pelo usuário

Quando o usuário selecionar IDs ou pedir execução diretamente:

1. Confirme os itens selecionados e dependências reais no código.
2. Delegue implementação somente aos agentes necessários e delimite arquivos/escopo. Use subagentes em paralelo apenas em tarefas independentes; evite editar o mesmo arquivo simultaneamente.
3. Implemente integração real, autenticação e origem de dados conforme os gates acima. Se faltar backend ou credencial de integração, implemente a dependência do roadmap ou reporte o bloqueio; não substitua por mock.
4. `@frontend_reviewer` valida a UI implementada em browser real (viewports, estados, screenshots, console e requests) e registra evidências; `@QA` executa os testes previstos para os itens selecionados — incluindo integração/E2E de first-party backend quando disponível — e `@AppSec` executa os casos de segurança acordados. Registre comando, ambiente não sensível, resultado e evidência. Uma análise ou arquivo de plano não conta como teste executado.
5. Atualize relatórios dos agentes participantes, estado dos IDs no roadmap, `.agentes/README.md` e `PROJECT_MAP.md` se houver mudança de navegação/contrato.
6. Informe precisamente o que mudou, o que passou, o que falhou e o que ficou bloqueado. Nunca exiba selo de qualidade sem evidência.

Não force pausas de sprint nem pergunte requisitos óbvios. Uma solicitação explícita para executar um item é autorização para executá-lo; pergunte só quando uma decisão ausente mudar materialmente o escopo, produto ou risco.
