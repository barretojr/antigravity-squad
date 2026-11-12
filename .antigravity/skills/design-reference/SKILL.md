---
name: design-reference
description: Researches relevant design systems and produces an original, product-specific DESIGN.md contract
---
# Design Reference and DESIGN.md

Use this for frontend discovery and implementation. A design reference describes how a product should look and feel; agent instructions describe how to build it. Keep the two concerns separate.

## Workflow

1. Identify product category, audience, trust needs, core tasks, existing brand assets and current frontend stack before choosing visual references.
2. Search the [Awesome DESIGN.md collection](https://github.com/voltagent/awesome-design-md) or official product design-system documentation for at most three relevant references. Prefer references with similar user needs and information density, not merely a fashionable appearance. Read the source files directly; record the source URL and access date.
3. Extract transferable principles (semantic color roles, type hierarchy, component states, spacing, density, interaction and responsive behavior). Explicitly separate observed facts from your interpretation.
4. Produce a project-specific `.agentes/design/DESIGN.md` using `templates/design-md.md`. Preserve current stack and existing product tokens unless a selected roadmap item changes them. Do not copy another product's exact identity, assets, layout, or prose.
5. Mark proposal versus implementation status. Frontend treats the document as a concrete contract, records deviations and updates the document/report when implementation changes the system.

Never choose dark mode, gradients, glass, bento grids, oversized hero sections, motion, or a specific font by default. Match visual density and interaction to the product's real tasks. Use licensed/owned assets and document attribution where required; never invent product screenshots, logos, customer quotes, or data.
