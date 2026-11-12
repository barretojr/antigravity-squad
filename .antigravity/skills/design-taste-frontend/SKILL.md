---
name: design-taste-frontend
description: Applies product-specific art direction and a browser-based finish review to avoid generic frontend output
---
# Product-specific Frontend Art Direction

Adapted from the public [taste-skill](https://github.com/leonxlnx/taste-skill) (MIT; see `UPSTREAM.md`). This skill carries over its useful principles, not its page-specific templates or scripts.

## Before implementation

- Read `.agentes/design/direcao-visual-e-marca.md` and `.agentes/design/DESIGN.md`; resolve contradictions with Designer/Coord.
- Name the product type and the primary user task. Use that to decide information density, imagery, tone and interaction.
- Make the real product visible in context where useful. Prefer client-owned assets; otherwise select properly licensed imagery and record attribution. Do not use fake product UI, fake testimonials, fabricated metrics or decorative stock art that misrepresents the service.
- Give each page one clear visual anchor and a deliberate hierarchy. Vary section composition only when it improves comprehension; avoid repeated card grids and decorative effects without a product reason.
- Keep motion restrained, purposeful, keyboard-safe and compatible with reduced-motion preferences. Rich scenes or shaders require a clear product fit and must not obscure task completion.

## Review after implementation

At desktop and mobile sizes, inspect the actual running page in a browser. Check alignment, clipping, text wrapping, section rhythm, image rendering/crop, navigation, forms, focus, contrast, reduced-motion behavior and all relevant UI states. Capture evidence and record actionable findings in `.agentes/frontend/revisao-visual.md`. Fix issues through the selected roadmap scope; do not declare visual success from source inspection alone.

This guidance is adaptable, not a pixel-perfect universal template. Follow the product-specific DESIGN.md and existing codebase conventions.
