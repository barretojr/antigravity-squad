---
name: design-reference
description: Researches world-class design systems from 80+ bundled benchmarks (Linear, Stripe, Supabase, Vercel, Apple) and produces an original, product-specific DESIGN.md contract.
---
# Design Reference and DESIGN.md

Use this skill for frontend discovery, art direction, and contract specification. A design reference describes how a product should look and feel; agent instructions describe how to build it. Keep the two concerns separate.

The full **Awesome DESIGN.md collection** (84 company design systems) is bundled directly in `design-md/` and accessible via the MCP tool `get_design_reference`.

## Bundled Design Catalog (`design-md/`)

You have instant local access to complete `DESIGN.md` contracts from industry leaders:
- **DevTools / High-Density SaaS:** `linear.app`, `supabase`, `vercel`, `cursor`, `replit`, `warp`, `hashicorp`, `sentry`, `clickhouse`
- **Fintech / Trust & High-Security:** `stripe`, `revolut`, `wise`, `mercury`, `coinbase`, `mastercard`
- **Consumer / Marketplace / Content:** `apple`, `airbnb`, `shopify`, `spotify`, `slack`, `uber`, `figma`, `notion`, `intercom`
- **AI & Innovation:** `openai`, `anthropic`, `claude`, `cohere`, `elevenlabs`, `midjourney`, `runwayml`, `together.ai`

Query any company contract directly via MCP:
```json
{
  "name": "get_design_reference",
  "arguments": {
    "company": "linear"
  }
}
```
Or search for design patterns across all systems:
```json
{
  "name": "get_design_reference",
  "arguments": {
    "query": "dark mode palette tokens"
  }
}
```

## Workflow

1. **Understand Product Context:** Identify product category, audience, core tasks, trust needs, existing brand assets and current frontend stack before selecting references.
2. **Select Benchmark Systems:** Choose at most 2-3 relevant references from the bundled catalog matching user needs and information density (e.g. `linear.app` for keyboard-first densified dashboards, `stripe` for checkout and trust).
3. **Extract Transferable Principles:**
   - Semantic color tokens (canvas, surface, borders, primary, accent, muted).
   - Typography scales, weights, and letter-spacing.
   - Spacing scales, grid rhythms, and border-radii.
   - Component states (hover, focus-visible, active, disabled, optimistic).
4. **Author the Project Contract:** Produce `.squad/design/DESIGN.md` (or `.agentes/design/DESIGN.md`) using `templates/design-md.md`.
   - Never copy a company's exact logo, brand assets, or verbatim prose.
   - Ground every choice in the product's actual purpose.
   - Preserve brownfield tokens unless explicitly scoped to change.
5. **Contract Enforcement:** Frontend treats `DESIGN.md` as an immutable visual contract. Any deviation must be approved and recorded.
