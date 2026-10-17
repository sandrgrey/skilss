# Security Baseline

Threat-model proportionally to public exposure and data sensitivity. Identify protected resources, entry points, actors, trust boundaries, and potential abuse scenarios.

## Checks
- Secrets: no tokens/API keys committed or echoed in logs/client code.
- Dependencies: minimal, compatible, lockfile used, vulnerabilities reviewed when scanner available.
- Auth: secure session/token handling, proper expiration, logout/revocation as applicable.
- Authorization: enforce object-level access and role boundaries server-side.
- Inputs: validate, normalize, limit sizes; prevent injection and unsafe filesystem paths.
- Web: review XSS, CSRF, SSRF, CORS, CSP based on app architecture.
- Uploads: file validation, storage isolation, access permissions and quotas.
- Privacy: only collect needed information and document consent/retention where relevant.

Do not evade security checks to make a build appear green. If audit is partial, report the gap clearly.
