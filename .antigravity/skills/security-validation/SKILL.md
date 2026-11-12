---
name: security-validation
description: Threat-model and verify authentication, authorization, data access and common web/API risks with reproducible evidence.
---
# Security Validation

During planning, write a threat model and prioritized test cases. During selected execution, test only the authorized local application and scope. For private dashboards, verify server-side authentication/authorization, session expiry/logout, password recovery, tenant/user boundaries (BOLA/IDOR), input validation, XSS/CSRF where relevant, rate limiting and secret handling. Use two test identities for access-control checks where possible. Include a minimal safe reproduction and expected 401/403/404 behavior, then help the owner close findings. Never attack external systems, expose customer data/secrets, or claim a penetration test from static review alone. Report exact endpoint, preconditions, result, severity and evidence; state when active verification could not run.
