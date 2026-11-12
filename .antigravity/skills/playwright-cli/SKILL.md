---
name: playwright-cli
description: Operates a real browser with Playwright CLI for frontend inspection, interaction and evidence
---
# Browser Review with Playwright CLI

Based on the [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli) workflow. Check the current upstream README for install/runtime requirements before installing; do not install global tools or alter the product dependency set without a selected task requiring it. If absent, report the prerequisite. The CLI skill can be installed using the upstream documented `playwright-cli install --skills` workflow when appropriate.

## Review loop

1. Start the product using its documented local command and confirm the real frontend/backend environment. Do not stub first-party API routes for acceptance evidence.
2. `playwright-cli open <local-url>` and use `snapshot`, `find`, and semantic refs to inspect and interact. Exercise at least one primary flow and relevant loading/empty/error/success behavior.
3. Use `resize` for desktop/mobile viewports; save screenshots with explicit paths under `.agentes/evidencias/frontend/` when available.
4. Inspect `console` and `requests`; verify first-party API calls, status and resulting UI. A page render alone does not prove backend integration.
5. Record exact commands, viewport, route/flow, result, screenshot/snapshot locations, console/network findings, limitations and defects in `.agentes/frontend/revisao-visual.md`.
6. Close the browser session. Never expose credentials or save authenticated storage state in committed artifacts. Use a dedicated local test account/session and keep state files outside version control.

Representative commands (confirm CLI version syntax with `playwright-cli --help`):

```text
playwright-cli open http://localhost:<port>
playwright-cli snapshot
playwright-cli resize 1440 900
playwright-cli screenshot --filename=.agentes/evidencias/frontend/desktop.png
playwright-cli resize 390 844
playwright-cli screenshot --filename=.agentes/evidencias/frontend/mobile.png
playwright-cli console
playwright-cli requests
playwright-cli close
```
