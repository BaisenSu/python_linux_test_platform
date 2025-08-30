
# SECURITY.md (lightweight)

# Security Policy

- No secrets in source code. Use environment variables for credentials.
- SSH credentials:
  - Prefer `key_filename` over passwords.
  - If using passwords, set via env (e.g., `DIAG_PASS`), not CLI history.
- Report vulnerabilities privately to the maintainer.


