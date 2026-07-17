# Cloud vs Local

## Theory
"Should this run in the cloud or locally?" isn't a single question — it's at least three:

| Dimension | Cloud (e.g. `mistral-large-latest`) | Local (e.g. quantized 7B via Ollama) |
|-----------|--------------------------------------|----------------------------------------|
| Latency | network round-trip + queueing | no network hop, but CPU/GPU-bound |
| Cost | per-token, scales with usage | ~free marginal cost, but upfront hardware |
| Privacy/data residency | data leaves your machine/VPC | data never leaves the device |

There's no universally "correct" answer — a healthcare intake form that can't leave the hospital's
network is a strong local-privacy case; a consumer app needing frontier-model reasoning quality is
a strong cloud case. The right exercise here is comparing the two, not picking a winner.

## Assignment
Simulate a comparison between the two deployment modes and print `COMPARE_OK`.

## Files
- `python/main.py` — minimal stub (this exercise is intentionally lightweight — the point is the
  comparison table above, not the code).
- `hint.md` — `Call mock twice or simulate`.
- `solution/python/main.py` — reference: a single print, standing in for "comparison completed."

## Verify
```bash
codam-labs --mock verify local_llm/03_cloud_vs_local
```
Expected stdout: `COMPARE_OK`.

## Troubleshooting
- **Comparing unlike things** — a common real-world mistake is comparing a heavily quantized local
  4-bit model's latency against a full-precision cloud model's *quality*, and drawing conclusions
  about "local vs cloud" that are really about "small vs large" or "quantized vs full-precision."
- **Ignoring cold-start cost** — a local model that isn't already loaded into memory can take
  seconds to tens of seconds to warm up; a fair latency comparison measures steady-state, not the
  first call.
- **Treating "free" local inference as actually free** — GPU/electricity/hardware amortization is
  a real cost; it's just shifted from a per-token API bill to a capital expense.
- **Skipping the privacy dimension entirely** — cost and latency are the easy numbers to compare;
  data residency/compliance requirements often override both and should be checked first, not
  last.

## Docs
- [Mistral pricing](https://mistral.ai/products/la-plateforme#pricing) — cloud cost baseline.
- [Ollama: hardware requirements](https://docs.ollama.com/quickstart) — realistic local hardware expectations.
- [GDPR: data residency overview](https://gdpr.eu/eu-gdpr-personal-data/) — the regulatory angle behind "local for privacy."
