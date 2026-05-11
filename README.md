# ai-redteam-notes

Public research notebook on **AI agent security**. Focus areas: indirect prompt injection, agent tool-use confused deputy, MCP server threat model, RAG poisoning, OWASP LLM Top 10, MITRE ATLAS techniques.

Generic-target writeups (lab-vuln-agents and open-weight models) under [ATTACKS/](ATTACKS/). Vendor-specific findings ship here only after coordinated disclosure clears (90-day default per industry CVD norms).

## Latest

- 2026-05-11 — [Lakera Gandalf — full walkthrough (L1–L8)](CTF/gandalf/) — 6/8 levels extracted via scripted API harness, L4 by feature triangulation, L7 structure-only with novel finding on prompt-text vs value-leakage separability.
- 2026-05-09 — [Policy isn't a mechanism: how a fake (#system) tag exfiltrated the wrong user's data](WRITEUPS/2026-05-09-policy-isnt-a-mechanism.md) — first long-form WRITEUP. ReAct agent, indirect prompt injection, mistral-nemo vs llama3.1.

## Pinned

- (Reserved for top-3 ATTACKS by writeup quality.)

## Index

- [ATTACKS/](ATTACKS/) - reproducible attack writeups, one folder per attack class
- [WRITEUPS/](WRITEUPS/) - longer-form blog posts (also published on dev.to)
- [CTF/](CTF/) - Gray Swan Arena, MLSec.io, AI Village CTF artifacts
- [BOUNTIES/](BOUNTIES/) - HackerOne / Bugcrowd disclosed reports (post-disclosure only)

## Disclosure policy

Every entry under `ATTACKS/` and `WRITEUPS/` carries YAML frontmatter `disclosure_status: green|yellow|red`. Only `green` entries are published here; `yellow` (under coordinated disclosure) and `red` (sensitive) are blocked from public push by a `pre-push` git hook.

Coordinated-disclosure timeline: 90 days from vendor first contact, with 30-day non-response escalation. Open-source no-vendor projects: 30-day buffer minimum.

## Tooling stack referenced across writeups

- [garak](https://github.com/NVIDIA/garak) - LLM vulnerability scanner
- [PyRIT](https://github.com/microsoft/PyRIT) - Microsoft red-team orchestrator
- [promptfoo](https://www.promptfoo.dev/docs/red-team/) - app-aware probe synthesis
- [AgentDojo](https://github.com/ethz-spylab/agentdojo) - indirect-injection benchmark
- [InjecAgent](https://github.com/uiuc-kang-lab/InjecAgent) - injection eval suite
- [Damn Vulnerable LLM Agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent) - training target

## Cadence

One new writeup most Saturdays; Tuesday lab-day signal posted on LinkedIn / X.

## Contact

For coordinated disclosure: open a security issue on this repo; non-public communication via the burner email noted on profile.
