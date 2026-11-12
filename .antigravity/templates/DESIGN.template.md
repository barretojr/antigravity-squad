# 🎨 DESIGN.md: Especificação do Sistema de Design (Padrão Awesome-Design-MD)

> **Diretriz ao Desenvolvedor & Agentes:** Este documento é a especificação de design oficial e imutável do projeto. Toda interface criada deve seguir rigorosamente estes tokens e regras, eliminando estilizações genéricas ("AI slop") e mantendo a identidade visual do produto.

---

## 🌟 1. Identidade & Direção de Arte (Taste & Tone)
- **Inspiração / Benchmark:** [Ex: Linear + Steam Deck UI + Vercel]
- **Estética:** Dark-first refinado, elegante, focado em alta densidade de informação sem poluição visual.
- **Microinterações:** Feedback imediato tátil, hover states com transições suaves (`duration-200 ease-out`), glow borders sutis.

---

## 🎨 2. Paleta de Cores & Tokens Semânticos
*Uso exclusivo de classes semânticas do Tailwind CSS mapeadas com variáveis CSS:*

| Token Semântico | Uso Previsto | Valor de Referência (Dark Mode) |
| :--- | :--- | :--- |
| `bg-background` | Fundo principal da aplicação | `hsl(224, 71%, 4%)` (slate/zinc profundo) |
| `bg-card` | Fundo de cartões, modais e containers | `hsl(222, 47%, 8%)` |
| `border-border` | Bordas e divisores sutis | `hsl(217, 33%, 17%)` com opacidade `/40` |
| `text-foreground` | Texto principal com alto contraste | `hsl(210, 40%, 98%)` |
| `text-muted-foreground` | Texto de apoio e legendas secundárias | `hsl(215, 20%, 65%)` |
| `bg-primary` | Cor de destaque primária (CTAs, botões chave) | `hsl(199, 89%, 48%)` (ciano elétrico) |
| `bg-accent` | Acentos secundários e tags | `hsl(142, 71%, 45%)` (esmeralda vibrante) |
| `text-destructive` | Alertas de erro e exclusão | `hsl(0, 84%, 60%)` |

---

## 🔤 3. Escala Tipográfica
- **Família de Fontes:** Sans moderna (Inter / Geist / Plus Jakarta Sans) para texto e títulos; Monospace (JetBrains Mono) para códigos e chaves de licença.
- **Hierarquia:**
  - `H1 (Hero):` `text-3xl md:text-5xl font-extrabold tracking-tight`
  - `H2 (Seção):` `text-2xl md:text-3xl font-bold tracking-tight`
  - `H3 (Card):` `text-lg font-semibold`
  - `Body:` `text-sm leading-relaxed text-muted-foreground`
  - `Microcopy / Badges:` `text-xs font-medium tracking-wide uppercase`

---

## 📐 4. Layout, Elevação & Grids
- **Bento Grids Assimétricos:** Grid responsivo de 12 colunas para vitrines, permitindo que o item em destaque ocupe 8 colunas e os itens auxiliares ocupem 4 colunas.
- **Bordas & Raios:** `rounded-xl` para cartões principais; `rounded-lg` para botões e inputs; `rounded-full` para badges.
- **Glassmorphism:** `backdrop-blur-md bg-background/80 border border-border/40` para barras de navegação fixas e gavetas de checkout.

---

## 🚫 5. Do's & Don'ts de Estilização
- ✅ **DO:** Utilizar sempre os 4 estados de tela (Skeleton animado no loading, Empty State amigável, Error State recuperável, Success State).
- ✅ **DO:** Adotar botões de ação fixa na parte inferior da tela no mobile (`fixed bottom-0 z-50 w-full`) para garantir alcance do polegar.
- ❌ **DON'T:** Nunca usar cores hexadecimais soltas no código (`bg-[#1f2937]`).
- ❌ **DON'T:** Nunca usar spinners circulares genéricos centralizados na tela em substituição aos skeletons com a forma do conteúdo.
- ❌ **DON'T:** Nunca aplicar gradientes roxos genéricos sem contexto funcional ("AI Slop").
