# Research Summary: Substrate-Aware Agent Injection

One pre-registered research program, not a collection of attacks. The through-line:
**where does an MCP agent's indirect-prompt-injection risk actually live, and does
it get better or worse as models get more capable?**

Start here, then follow [REPORTS/hiring-reviewer-map.md](REPORTS/hiring-reviewer-map.md)
for a 60-second / 5-minute / deep path, and
[REPORTS/hiring-evidence-index.md](REPORTS/hiring-evidence-index.md)
for every claim tied to raw runs.

## The arc

1. **An attribution error, caught and retracted (H3).** A result that looked like
   one open-weight model being "more robust" than another was traced to a confound:
   the two runs used different MCP client dispatch substrates, not just different
   models. H3 was retracted and a `substrate` axis was registered before any further
   cells ran. Pre-reg: [docs/preregistrations/2026-mcp-matrix.md](docs/preregistrations/2026-mcp-matrix.md).

2. **The substrate isolated as a pre-registered factor (H5, supported).** Holding
   the model (Llama-3.1-8B) and payload set constant, only the configuration that
   includes an inline-XML tag parser reproduced the bypass shape; a typed tool-use
   API substrate and a scaffold-prompt-only probe did not. The load-bearing variable
   was parser architecture, not model alignment.

3. **A cross-scale prediction, falsified (H7).** The implicit assumption was that a
   larger model would be safer here, so the effect would wash out at scale. H7 was
   registered as a falsifiable claim before the cell ran. It was falsified
   decisively: under the same inline-XML substrate, Llama-3.3-70B reached 10/10
   strict canary exfiltration where 8B reached 0/5. Capability *amplifies*
   exploitation inside the insecure substrate; it does not dissolve it. Entry:
   [ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md](ATTACKS/2026-05-16-cline-70b-M0-f1-substrate-replication.md);
   pre-reg: [docs/preregistrations/2026-05-13-tier-a-w1-w5.md](docs/preregistrations/2026-05-13-tier-a-w1-w5.md).

4. **Mitigation ordering, with a surprise.** A short tool-agnostic content-trust
   boundary (M1) was the most effective single mitigation. Naming the tools inside
   the mitigation prompt (M2) caused a regression versus no mitigation on the small
   model: the names acted as a salience prime. Client-side tag-dispatch order
   (first-tag / last-tag / all-tags) is itself a security boundary, not a UI detail.

5. **What is next.** The architectural recommendation is to prefer the typed
   tool-use API substrate over inline-XML dispatch at every model scale. A
   confirmatory, mitigation-tested grid (H10b-G) is in progress and gated; no
   H10b-G rates are stated until its control cell clears its pre-registered
   packaging gate.

## The contribution, stated plainly

Two things here are uncommon and are the point of the work:

- **The client substrate was registered as an experimental factor and isolated
  through controlled emulation against a held-constant model.** Substrate effects
  in this class have been hinted at in prior work; registering and measuring the
  substrate as a variable is the methodological contribution.
- **Capability-amplifies-exploitability within a fixed insecure substrate.** The
  defensible claim is sharper than either "substrate is everything" or "bigger
  models are safer": the substrate is the necessary enabler, and a more capable
  model is *more* reliably exploited inside it. The fix matters more at scale, not
  less.

## Negative and falsified results

These are surfaced deliberately. A research portfolio that hides its nulls is less
trustworthy than one that reports them.

- **H3 retracted.** The original model-strength inversion was a substrate confound.
- **H7 falsified.** The implicit "70B is safe enough" scoping did not survive
  replication; the author corrected his own published takeaway rather than
  defending it.
- **H6 falsified.** A combined-framing payload (v7) produced 0 strict bypasses on
  M0 across the pre-registered seed budget.
- **H11 / last-tag-wins ablation.** 0/10 strict bypasses; one real callback carried
  placeholder data, not the canary. The dispatch-policy risk was narrowed, not
  inflated.
- **M2 regression.** Tool-naming inside a mitigation prompt performed worse than no
  mitigation on the 8B model.
- **8B M0 nulls and a hardened-target hold.** 0/5 strict bypass at 8B M0; a
  system-prompt-hardened PAIR target held a canary across 24 attack turns.

## Disclosure and honesty boundary

All artifacts are `green` disclosure: localhost-only harnesses, open-weight models,
canary files, and intentionally vulnerable benchmarks. No production vendor system
was contacted. Hypotheses were pre-registered before cells ran. Public claims are
bounded to what the run directories support; the strongest single artifact is the
pre-registered H7 falsification. Companion public report:
[REPORTS/substrate-vs-policy-assessment.md](REPORTS/substrate-vs-policy-assessment.md).

Flagship writeup with full methodology and Addendum B (the cross-scale correction):
[WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md](WRITEUPS/2026-05-14-mcp-substrate-vs-policy.md).
Concrete agent-exploitation companion study:
[ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md](ATTACKS/2026-05-14-dvl-agent-scenario2-sql-injection.md).
