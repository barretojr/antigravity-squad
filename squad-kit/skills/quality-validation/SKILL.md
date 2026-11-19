---
name: quality-validation
description: Turn requirements into executable acceptance checks and prove first-party UI/API integration with test evidence.
---
# Quality Validation

During planning, convert roadmap criteria into a test matrix with priority, layer, setup, expected result and evidence. During execution, run relevant checks instead of only writing test plans. For frontend flows, use Playwright/browser against the running frontend and backend, verify a real request and response from the first-party API, and capture relevant console/network failures. Include login/logout/recovery, protected routes, search/filter, empty/loading/error/success states and responsive/a11y checks when in scope. Use real PostgreSQL via Testcontainers for persistence behavior when the repository supports it. Fixtures belong in test code; mocking the first-party API cannot satisfy integration acceptance. Record exact commands, exit statuses, browser/device parameters and failures. If blocked by missing credentials, Docker, configuration or service, mark BLOCKED and state the missing prerequisite; never report an unrun test as passed.
