# Security & Disclosure Policy

This is an AI security **research** repository. All experiments target **intentionally
vulnerable benchmarks** (DVL Agent, vuln-agent framework), **open-weight models** via public
APIs, or **localhost** harnesses. No production system or hosted vendor is tested without
explicit prior authorization. This policy is enforced in code, not just stated. See
[`docs/adr/ADR-003-portfolio-cadence.md`](docs/adr/ADR-003-portfolio-cadence.md) for the full
decision record and [`docs/adr/ADR-005-lab-safety.md`](docs/adr/ADR-005-lab-safety.md) for lab
safety and identity separation.

## Three-tier disclosure ladder

Every `ATTACKS/` entry carries `disclosure_status` frontmatter, gated by an automated
`pre-push` hook on the public mirror:

| Status | Meaning | Public push |
|---|---|---|
| **green** | Generic attack class against open-weight models / vuln-agent benchmarks, or 90+ days post-coordinated-disclosure | Allowed |
| **yellow** | Vendor-specific finding under active coordinated disclosure (<90 days) or awaiting vendor response | Blocked |
| **red** | Sensitive finding (training-data extraction, CBRN-relevant, model-stealing) | Blocked without explicit clearance |

The public portfolio is built almost entirely on **green** entries. Vendor-specific findings
remain yellow/red in the private repo until clearance. Timeline interlock: 90 days from first
contact (or mutually agreed earlier); 30-day minimum buffer for non-responsive vendors;
high-severity unresponsive cases escalate to a coordinated-disclosure org (e.g. CERT/CC).

## Risk class under study

This repository's research subject is exactly the kind of systemic AI-agent supply-chain risk
exemplified by **CVE-2026-30623** (command injection in the MCP SDK stdio transport,
[OX Security advisory, 2026-04-15](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/))
and the broader indirect-prompt-injection-via-tool-output class. The
defensive deliverable, [`lab/mcp-matrix/tools/substrate_auditor.py`](lab/mcp-matrix/tools/substrate_auditor.py),
turns the finding into a pre-deploy CI substrate check.

## Reporting

To report a security concern in this repository's tooling or methodology, contact
`ChunkyTortoise@proton.me`. This repo follows the HackerOne Good-Faith AI Safe Harbor (Jan 2026)
as legal scaffolding for its disclosure practices.
