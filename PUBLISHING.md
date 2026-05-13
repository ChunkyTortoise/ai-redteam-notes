# Publishing Source Of Truth

Use the dedicated publishing checkout for this public portfolio. It should be the local clone whose `origin` points to `https://github.com/ChunkyTortoise/ai-redteam-notes.git`.

Local roles:

- Publishing checkout: public GitHub working tree.
- Gate mirror: local validation copy used by private repo scripts unless `AI_REDTEAM_PUBLIC_REPO_PATH` is set.
- Historical checkout: stale copy; do not use for publication.

Before submitting applications, verify public links from the publishing checkout and run private gates with:

```bash
AI_REDTEAM_PUBLIC_REPO_PATH=/path/to/publishing-checkout bash pipeline/scripts/check-portfolio.sh
```
