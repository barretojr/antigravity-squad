---
name: design-taste-frontend
description: Applies product-specific art direction, crafts high-taste frontend UI without AI slop, and provides audit heuristics, scripts, and asset kits.
---
# Product-Specific Frontend Art Direction (Taste Skill)

Full integration of the [taste-skill](https://github.com/leonxlnx/taste-skill) suite. This skill equips Designer, Frontend, and Frontend Reviewer with principles, assets, scripts, and MCP audit tools to produce distinctive, high-craft web interfaces and eliminate generic "AI slop".

## Bundled References & Tooling

This skill bundles:
1. **References (`references/`):**
   - `copy-tells.md`: List of AI clichés and generic filler copy to avoid ("Unlock your potential", "Game-changing", etc.).
   - `copy-voice.md` & `copy.md`: Concrete voice, tone, and microcopy guidance.
   - `layout-v4.md` & `sections.md`: Section rhythm, visual anchors, hierarchy, and non-monotonous layouts.
   - `moments.md`: Delightful microinteractions, feedback states, and tactile details.
   - `motion.md`: Purposeful, keyboard-safe, reduced-motion-compliant CSS transitions.
   - `system.md` & `sections-library.md`: Design system rules and reusable structural patterns.
   - `perf.md`: Web vitals and performance heuristics.
2. **Scripts (`scripts/`):**
   - `consistency.mjs`: Checks UI token consistency.
   - `copy-lint.mjs`: Lints strings for AI buzzwords and robotic placeholder prose.
   - `gate.mjs`: Quality gate for design criteria.
3. **Assets (`assets/`):**
   - Reusable background treatments, component styles, motion curves, and system CSS/JS.
4. **MCP Tool Integration:**
   - Call `audit_frontend_taste` via the Antigravity Squad MCP server to automatically scan your frontend code for AI slop, hardcoded hex values, monotonous layouts, and missing accessibility considerations.

## Core Principles

### 1. No "AI Slop"
- **No generic purple-on-black floating card grids.** Match the color scheme, density, and surfaces to the specific product and users.
- **No fake data or fabricated metrics.** Never invent fake revenue graphs, 99.9% uptime badges, or stock quotes. Show empty states when there is no data.
- **No robotic copywriting.** Replace generic filler with concise, functional, user-centric language.

### 2. Clear Visual Anchor & Rhythm
- Every page and view must have one deliberate focal point (the primary user task or primary content).
- Avoid repetitive 3-column card layouts where every element has equal visual weight. Vary density intentionally.

### 3. Tactile Feedback & Microinteractions
- Buttons, toggles, inputs, and tabs must have clear focus rings (`focus-visible`), active states, loading indicators, and tactile feedback.
- Honor user preferences: all animations must respect `prefers-reduced-motion`.

## Review Loop

1. In development, inspect components in the browser at desktop (1440px) and mobile (390px) viewports.
2. Run `audit_frontend_taste` to identify anti-patterns, contrast problems, or buzzwords.
3. Record visual review findings in `.squad/frontend/revisao-visual.md` with concrete evidence.
