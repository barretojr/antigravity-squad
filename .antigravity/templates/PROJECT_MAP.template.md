# 🗺️ PROJECT_MAP: Mapa Cirúrgico de Navegação & Tokens

> **Aviso ao Agente:** Este é o GPS do projeto. Antes de buscar ou editar qualquer código para manutenções ou novas features, consulte esta tabela para identificar diretamente o arquivo alvo. **PROIBIDO fazer grep ou full-scan no projeto.**

---

## 📱 1. Índice de Telas, Componentes & Elementos de UI (Frontend)

| Elemento / Componente | Arquivo Relativo | Responsividade (Mobile vs Desktop) | Estado / Hook Associado |
| :--- | :--- | :--- | :--- |
| **Botão CTA / Checkout** | `src/components/cart/checkout-button.tsx` | **Mobile:** Fixo inferior (`fixed bottom-0 z-50 w-full p-4`)<br>**Desktop:** No rodapé do card (`relative`) | `useCheckout.mutate()`, abre `Sheet` |
| **Drawer do Carrinho** | `src/components/cart/cart-sheet.tsx` | **Mobile:** Bottom Sheet (`h-[80vh]`)<br>**Desktop:** Drawer lateral direito (`w-[420px]`) | `useCartStore`, TanStack Query |
| **Filtro de Catálogo** | `src/components/catalog/filter-bar.tsx` | **Mobile:** Trigger modal com contador de filtros<br>**Desktop:** Sidebar esquerda fixa | `nuqs` (URL SearchParams) |
| **Card do Produto / Jogo** | `src/components/catalog/product-card.tsx` | Grid responsivo: 1 col (mobile), 2 cols (tablet), 4 cols (desktop) | Hover glow, preview de trailer |
| **Modal de Requisitos/Specs** | `src/components/catalog/specs-dialog.tsx` | Modal centralizado com tabs (`Min` vs `Rec`) | Radix Dialog |

---

## ⚙️ 2. Índice de Endpoints, Casos de Uso & Banco (Backend)

| Funcionalidade | Método & Rota HTTP | Controller | Caso de Uso / Serviço | Entidade / Tabela |
| :--- | :--- | :--- | :--- | :--- |
| **Processar Checkout** | `POST /api/v1/checkout` | `Controllers/CheckoutController.cs` | `UseCases/ProcessCheckoutUseCase.cs` | `Orders`, `LicenseKeys` |
| **Buscar Catálogo** | `GET /api/v1/games` | `Controllers/GamesController.cs` | `UseCases/GetGamesListUseCase.cs` | `DigitalGames` |
| **Resgatar Chave** | `POST /api/v1/keys/claim` | `Controllers/KeysController.cs` | `UseCases/ClaimKeyUseCase.cs` | `LicenseKeys` |
| **Webhook de Pagamento**| `POST /api/v1/webhooks/pay`| `Controllers/WebhooksController.cs` | `UseCases/HandlePaymentWebhookUseCase.cs` | `Orders`, `OutboxEvents` |

---

## 🔒 3. Políticas de Segurança & Rate Limits (AppSec)

| Endpoint / Fluxo | Vetor Protegido | Mecanismo de Defesa | Arquivo de Configuração |
| :--- | :--- | :--- | :--- |
| `/api/v1/keys/claim` | Brute-force de chaves | Rate Limit (5 req / min por IP) | `Middlewares/RateLimiting.cs` |
| `/api/v1/webhooks/*` | Forja de pagamentos | Validação de Assinatura HMAC SHA-256 | `Security/HmacValidationFilter.cs` |
| Checkout | Concorrência em estoque | Trava pessimista `SELECT ... FOR UPDATE` | `Repositories/KeyRepository.cs` |

---

## 🧪 4. Suíte de Testes Automatizados (QA)

| Tipo de Teste | Escopo / Cenário | Comando de Execução | Arquivo de Teste |
| :--- | :--- | :--- | :--- |
| **Integração Real** | Concorrência de estoque (Zero Oversell) | `dotnet test --filter Category=Concurrency` | `Tests/ConcurrencyCheckoutTests.cs` |
| **Visual / E2E** | Responsividade Mobile vs Desktop | `npx playwright test --project=mobile` | `e2e/responsive-checkout.spec.ts` |
| **Acessibilidade** | Conformidade WCAG AA nas telas | `npx playwright test --project=a11y` | `e2e/accessibility.spec.ts` |
