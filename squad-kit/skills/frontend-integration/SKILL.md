---
name: frontend-integration
description: Build React interfaces on real typed backend APIs with working authentication, truthful data, and verifiable request flows.
---
# Frontend Integration

Build React 19/TypeScript UI against the actual first-party backend contract. Inspect existing clients, endpoints, auth scheme, DTOs, CORS/base URL configuration, and error conventions before coding. Coordinate request/response changes with Backend and Coord.

- Never use static arrays, fabricated metrics, canned offers, fake auth, localStorage-only sessions, or delayed promises as production behavior. Keep fixtures inside tests or isolated Storybook stories. If real data is unavailable, show an empty state and report the missing backend/integration dependency.
- Use a typed HTTP client and the project’s established query/state/form libraries. Every user action must call the intended endpoint and surface loading, empty, error, success, and unauthorized/expired-session states as applicable.
- Private app routes require real authentication and server-side authorization. Login, logout, recovery and refresh/session behavior must agree with the backend. Never use a frontend-only route guard as the security boundary.
- For completion, capture evidence of a browser request reaching the running API and receiving the expected response. Unit tests may stub external services; they do not replace first-party API integration or E2E validation.
- Keep accessibility, mobile/desktop behavior, keyboard use, focus handling and reduced motion. Report endpoint paths, status handling and any backend blockers in the assigned frontend report.
