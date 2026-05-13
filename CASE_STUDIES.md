# Case Studies

Three short reads for hiring reviewers. Each case study links to the deeper artifact trail.

## 1. Customer Assessment: MCP Tool-Output Injection

**Problem:** An MCP-style agent can fetch attacker-controlled content and expose local tools in the same workflow. The security question is whether prompt policy, client substrate, or runtime dispatch behavior carries the actual boundary.

**Method:** I built a localhost MCP lab with a benign user prompt, attacker-controlled fetched content, a local secret canary, and an exfiltration sink. I compared typed tool-call behavior against inline XML-style dispatch, then measured mitigation prompts and sanitizer behavior.

**Result:** The strongest result was attribution correction: an apparent model-policy bypass was better explained by the client substrate. The typed tool-call path held, while the XML-dispatch emulation produced intent shifts. A named-tool confirmation prompt regressed versus a tool-agnostic boundary.

**Mitigation:** Prefer structured tool-call APIs over inline XML parsing, keep system-prompt mitigations tool-agnostic on small models, and treat dispatch policy as part of the security boundary.

**Links:** [writeup](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md), [assessment report](REPORTS/substrate-vs-policy-assessment.md), [ATTACKS entry](ATTACKS/2026-05-10-substrate-amplification-mcp-tool-output.md), [eval harness](EVALS/mcp-matrix-harness.md).

## 2. Research Investigation: Cross-Model ReAct Loop Injection

**Problem:** A payload that works against one model or wrapper can fail against another, and broad "prompt injection works" claims are not enough for practical red teaming.

**Method:** I ran DVL-Agent Scenario 2 across two model families and two payload wrappers, preserving raw artifacts and reporting Wilson confidence intervals for small-n cells.

**Result:** llama3.1:8b and mistral-nemo behaved differently under the same SQL-injection-style ReAct loop pressure. The camouflaged wrapper eliminated the observed exfiltration against mistral-nemo in the tested cell while llama3.1:8b remained vulnerable in both wrappers.

**Mitigation:** Treat wrapper style as a measured variable, not just an implementation detail. Report cell design and uncertainty instead of only success/failure anecdotes.

**Links:** [writeup](WRITEUPS/2026-05-14-cross-model-react-loop-injection.md), [ATTACKS entry](ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md).

## 3. Eval Automation: Promptfoo and DVL-Agent Baselines

**Problem:** Manual red-team transcripts are useful but hard to compare, regress, or explain to a hiring reviewer or engineering team.

**Method:** I used promptfoo and local lab targets to turn DVL-Agent experiments into repeatable runs with result files, summaries, and public ATTACKS entries.

**Result:** The baseline and Scenario 2 artifacts make the difference between a single exploit note and a reusable evaluation path: prompt, target, model, outcome, mitigation, and disclosure status are preserved in a consistent format.

**Mitigation:** Keep eval artifacts small, structured, and reproducible. Every public claim should link to either a run artifact, an ATTACKS entry, or a writeup that explains the limitation.

**Links:** [Gandalf technique entry](ATTACKS/2026-05-09-gandalf-output-reformatting-and-side-channel.md), [Scenario 2 benchmark](ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md), [MCP harness note](EVALS/mcp-matrix-harness.md).
