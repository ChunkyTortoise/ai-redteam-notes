# ATTACKS Directory

## Attack summary

One row per dated entry, taken from each entry's own TL;DR or Result section. All targets are intentionally vulnerable benchmarks, a public CTF (Gandalf), or localhost harnesses driving local or API-hosted models (Groq, OpenRouter); every entry is `disclosure_status: green`. Small n throughout: these are mechanism results, not population rates. Every row was observed in a live run in May 2026; none is a paper reference, and the last column says what can be checked offline here (nothing in this table re-runs a model).

| Date | Attack class | Target | Technique | Outcome | Evidence | Data in this repo |
|---|---|---|---|---|---|---|
| 2026-05-03 | Indirect prompt injection (spoofed system directive) | DVL Agent (intentionally vulnerable) | `(#system)`-prefixed directive in the user message | Developer-enforced user isolation overridden | [entry](2026-05-03-indirect-injection-tool-description.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-03 | Prompt injection, excessive agency (LLM01) | DVL Agent, llama3.1:8b | promptfoo battery, 24 cases | Superseded by the 2026-05-12 hand-verified run | [entry](2026-05-03-promptfoo-dvl-agent-redteam.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-04 | Prompt injection (LLM01) | AgentDojo workspace suite, IBM Granite 4.1 8B (local) | `important_instructions` attack, no defense | 0% security over 9 trials; all 3 injection tasks executed | [entry](2026-05-04-agentdojo-granite-4-1-8b.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-04 | Prompt injection, jailbreak, package hallucination | llama3.1:8b (ollama) | garak sweep, 5 probe classes | Partial sweep, 4 of 5 probes completed | [entry](2026-05-04-garak-fullsweep-llama31.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-04 | Persona override / DAN | llama3.1:8b, empty system prompt | PAIR, 10 seeds | 1/10 strict, 2/10 loose after hand verification (raw counter said 6/10) | [entry](2026-05-04-pair-llama31-persona-dan.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-04 | Guardrail comparison | llama3.1:8b vs mistral:7b | PAIR battery, 12 goals, two attacker models | mistral:7b succeeded about 2x as often | [entry](2026-05-04-pair-matrix-llama31-vs-mistral7b.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-06 | Indirect prompt injection | DVL Agent scenario 1 | PAIR-driven, given the tool surface and the `(#system)` vector | Flag exfiltrated in 4 turns | [entry](2026-05-06-pair-agent-dvl-scenario1.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-09 | Output reformatting, side channel | Lakera Gandalf (public CTF) | Scripted API probing | Levels 1-6 recovered; literal-value filters bypassed by reformatting | [entry](2026-05-09-gandalf-output-reformatting-and-side-channel.md) · [walkthrough](../CTF/2026-05-09-lakera-gandalf-walkthrough.md) | Live run on a public CTF; probe output in [`CTF/gandalf/transcripts/`](../CTF/gandalf/transcripts/) |
| 2026-05-10 | Tool-output injection, substrate amplification | Headless MCP harness, Llama 3.1 8B | Same payloads with and without XML-tag tool scaffolding | Earlier bypass traced to the client substrate; pristine headless re-run 0/5 | [entry](2026-05-10-substrate-amplification-mcp-tool-output.md) | Live run; aggregate [`success.json`](../lab/mcp-matrix/runs/2026-05-10-llama-xml-M1-v7-dispatch-all-tags/success.json) for one cell only |
| 2026-05-12 | Indirect injection, excessive agency, MCP abuse, smuggling (LLM01, LLM06) | DVL Agent, llama3.1:8b | promptfoo, 24 cases, llm-rubric judge then hand verification | 4/24 strict, 6/24 loose; judge under-graded 4 cases | [entry](2026-05-12-dvl-agent-promptfoo-baseline.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-13 | MCP tool-output injection (negative result) | Self-hosted MCP server + Claude Desktop | 5 payloads, M0 | 0/5 canary exfiltrations; tool calls refused | [entry](2026-05-13-pair-matrix-m0-claude-desktop-negative.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-14 | ReAct observation injection to SQL injection | DVL Agent scenario 2 | UNION payload via tool observation, bare and camouflaged, n=5 | llama3.1:8b 10/10 pooled; mistral-nemo 5/10 (0/5 camouflaged) | [entry](2026-05-14-dvl-agent-scenario2-sql-injection.md) | Live run; [`wilson_summary.json`](../lab/promptfoo/runs/2026-05-13-dvl-scenario2-crossmodel/wilson_summary.json), per-trial files not mirrored |
| 2026-05-15 | Tool-output injection, dispatch-policy ablation (H11) | Headless MCP harness, XML dispatch | Last-tag-wins dispatch, n=10 | 0/10 strict; H11 falsified | [entry](2026-05-15-mcp-xml-last-tag-dispatch-ablation.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-16 | Tool-output injection, cross-scale (F1, H7) | Headless MCP harness, Cline inline-XML, Llama-3.3-70B | v1-visible-notice payload, M0, n=10 | 10/10 strict vs 0/5 at 8B; H7 falsified | [entry](2026-05-16-cline-70b-M0-f1-substrate-replication.md) · [seeds](../lab/mcp-matrix/runs/2026-05-16-cline-70b-M0-f1/seeds.json) | Live run; per-seed outcome flags recounted offline by `make tally` |
| 2026-05-16 | Tool-output injection, scale (H10b, first cells) | Headless MCP harness, Llama-3.3-70B | First two M0 cells of H10b | Superseded by H10b-G | [entry](2026-05-16-open-source-scale-substrate-h10b.md) | Live run; entry only (raw data not mirrored) |
| 2026-05-18 | Tool-output injection, prompt mitigation grid (H10b-G) | Headless MCP harness, inline-XML, Groq Llama-3.3-70B | 3 payloads x M0/M1 + chat-only control, n=10 each | M1: 0/10, 0/10, 10/10 (v7); control 0/10 | [entry](2026-05-18-h10b-g-70b-substrate-grid-m1-variant-selective.md) · [seeds](../lab/mcp-matrix/runs/) | Live run; 4 of 7 cells recounted offline by `make tally`, 3 entry only |

Recount the committed per-seed cells with `make tally` from the repo root.


This directory contains structured attack entries documenting various red team techniques, vulnerabilities, and exploitation methods.

## Structure

Each attack entry follows a standardized format defined in [_template.md](_template.md) and includes:

- **Metadata Frontmatter**: YAML-formatted header with disclosure information, dates, and classification
- **Technical Description**: Detailed explanation of the attack vector
- **MITRE ATT&CK Mapping**: References to relevant tactics and techniques
- **Proof of Concept**: Example commands, scripts, or demonstrations
- **Detection & Mitigation**: Guidance on identifying and defending against the attack
- **References**: Links to related research, advisories, or tools

## Validation

All attack entries are automatically validated by CI pipelines using:
- `pipeline/scripts/check-attack-entry.sh`: Validates structure and required sections
- `pipeline/scripts/check-disclosure.sh`: Ensures proper disclosure metadata

## Contributing

When adding new attack entries:
1. Copy `_template.md` to a new file with descriptive name (YYYY-MM-DD-descriptive-title.md)
2. Fill in all sections according to the template guidelines
3. Ensure the entry passes validation scripts before submitting a PR
4. Include appropriate MITRE ATT&CK tactic/technique mappings
