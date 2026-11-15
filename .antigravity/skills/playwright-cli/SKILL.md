---
name: playwright-cli
description: Operates a real browser with bundled Playwright CLI for frontend visual inspection, screenshots, console logs, network capture, and MCP evidence.
---
# Browser Review with Playwright CLI

Full integration of the official [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli). This skill gives the squad (particularly `frontend_reviewer`, `qa`, and `designer`) a self-contained, automated browser tool to inspect UI, verify responsive layouts, test real APIs, capture screenshots, and collect console/network logs.

## Bundled CLI Tooling & References

This skill includes:
1. **Executable Runner (`playwright-cli.js`):**
   - Bundled Node CLI wrapper for all Playwright commands.
   - Run directly: `node D:/Agentes/.antigravity/skills/playwright-cli/playwright-cli.js <command>`
   - Or invoke through the MCP tool: `run_playwright_cli`.
2. **References (`references/`):**
   - `element-attributes.md`: Interacting with DOM elements and selectors.
   - `playwright-tests.md`: Test structure and assertions.
   - `session-management.md`: Managing browser instances, cookies, and local storage.
   - `storage-state.md`: Handling authentication state and session persistence safely.
   - `running-code.md`: Evaluating custom JavaScript inside the browser context.
   - `request-mocking.md`: Network routing and interception rules.
   - `tracing.md` & `video-recording.md`: Advanced debugging and visual regression captures.

## Common Workflows

### 1. Browser Inspection & Screenshots (MCP or CLI)
```bash
# Via MCP tool:
run_playwright_cli(command="screenshot", url="http://localhost:5173", viewport="desktop", output_path=".squad/evidencias/frontend/desktop.png")
run_playwright_cli(command="screenshot", url="http://localhost:5173", viewport="mobile", output_path=".squad/evidencias/frontend/mobile.png")
```

### 2. Interactive CLI Commands
```bash
# Open app and capture DOM snapshot
node playwright-cli.js open http://localhost:5173
node playwright-cli.js snapshot

# Viewport tests
node playwright-cli.js resize 1440 900
node playwright-cli.js screenshot --filename=.squad/evidencias/frontend/desktop.png
node playwright-cli.js resize 390 844
node playwright-cli.js screenshot --filename=.squad/evidencias/frontend/mobile.png

# Console & Network requests inspection
node playwright-cli.js console
node playwright-cli.js requests

# Close session
node playwright-cli.js close
```

## Security & Evidence Rules
- **No Credentials in State Files:** Never commit `.auth/` storage states or user passwords to git.
- **Evidence Path:** Store browser screenshots and snapshots under `.squad/evidencias/frontend/`.
- **Verify Real Backend:** Inspect `requests` to confirm real HTTP requests and 2xx responses; never mock first-party API responses for visual acceptance evidence.
