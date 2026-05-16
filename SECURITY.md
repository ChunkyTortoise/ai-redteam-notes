# Security and Disclosure Policy

## Scope

This repository contains AI agent security research. All public artifacts are scoped to:

- Intentionally vulnerable lab targets (Damn Vulnerable LLM Agent, AgentDojo)
- Open-weight models run locally (llama3.1:8b, mistral-nemo via Ollama)
- Public CTF challenges (Lakera Gandalf)
- Generic attack-class reproductions of published research

No production systems, cloud-hosted APIs, or vendor-specific targets are tested from this repository without coordinated disclosure clearance.

## Disclosure Traffic Light

Every `ATTACKS/` entry carries a frontmatter `disclosure_status`:

| Status | Meaning |
|--------|---------|
| `green` | No vendor-specific target, or 90+ days post-coordinated disclosure. Safe to publish. |
| `yellow` | Vendor-specific finding under active coordinated disclosure (< 90 days). Not published here. |
| `red` | Sensitive finding withheld pending explicit clearance. Not published here. |

All entries in this public mirror are `green`. Vendor-specific findings stay in the private repo until clearance.

## Coordinated Disclosure Timeline

- Day 0: vendor first contact
- Day 1–7: vendor acknowledgment expected
- Day 90: public disclosure unless mutually agreed otherwise
- Non-responsive vendor: 30-day minimum buffer before publishing medium/low severity

High-severity unresponsive findings are escalated to a coordinated-disclosure org (CERT/CC or equivalent) rather than published unilaterally.

## Reporting a Problem with This Research

If you believe any artifact in this repository contains information that could enable real-world harm, or if you are a vendor who has identified a finding that concerns you:

Open an issue in this repository or contact the author directly through GitHub.

## License

Research content (ATTACKS/, WRITEUPS/, REPORTS/, EVALS/) is licensed under CC BY 4.0.
Code (lab/, pipeline/scripts/) is licensed under MIT. See [LICENSE](LICENSE).
