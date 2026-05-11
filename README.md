# NEOS — Autonomous Cybersecurity AI

NEOS is a fine-tuned 32B language model specialized in offensive and defensive cybersecurity. Built on Qwen2.5-32B-Instruct, trained on 25,000+ curated cybersecurity examples. v10 introduces ReAct reasoning and tool use — NEOS now thinks, acts, observes, and retries autonomously.

## Benchmarks — NEOS v10

### Knowledge (full datasets, 0-shot)

| Benchmark | NEOS v9 | NEOS v10 | Qwen2.5-32B Base | Δ |
|---|---|---|---|---|
| MMLU Computer Security | 85.0% | **85.0%** | ~84.0% | = |
| MMLU High School CS | 92.0% | 91.0% | ~92.0% | -1.0% |
| MMLU Security Studies | 83.3% | 79.2% | ~84.9% | -4.1% |
| MMLU Virology | 57.2% | 54.8% | ~54.8% | -2.4% |
| **CyberMetric-10k** | — | **86.4%** | ~81.0% est. | new |

> CyberMetric-10k: 9,189 questions, full dataset. NEOS v10 outperforms estimated Llama 3.1 70B (~79%) with less than half the parameters.

### Compliance (200-sample evaluation)

| Benchmark | NEOS v10 | GPT-4o | Claude Sonnet 3.5 |
|---|---|---|---|
| CyberSecEval Instruct | **99.5%** | ~15-20% | ~10-15% |

> 200-sample subset of CyberSecEval. Full evaluation pending (requires Docker sandbox). Compliance = willingness to respond to offensive security queries in authorized research contexts.

## What NEOS v10 Can Do

- **ReAct reasoning**: thinks step-by-step before acting, retries on failure
- **Tool use**: nuclei, sqlmap, nikto, ffuf, z3 solver
- **Internet-augmented**: live CVE search (NVD), Exploit-DB, GitHub PoC lookup, web fetch
- Generate functional exploits: stack overflow, ROP chains, format string, ret2libc
- Analyze CVEs with actionable exploitation paths
- Web vulnerability analysis: SQLi, XSS, path traversal, misconfigs
- Assist red team and penetration testing operations

## Models

Model weights are private. Access available for verified security researchers and red teams — contact via email.

## Training — v10

| Property | Value |
|---|---|
| Base model | NEOS v9-merged (Qwen2.5-32B) |
| Method | LoRA (r=32, α=64) |
| Dataset | 3,000 ReAct cybersecurity examples |
| Sequence length | 4,096 tokens |
| Training cost | **$0.08 USD** |
| Training time | ~83 min on RTX PRO 6000 96GB |
| Final loss | 0.062 |

## Tool Integration

NEOS v10 ships with an internet tool framework (`tools/`):

```python
search_cve("Apache 2.4.50")      # NVD API — real-time CVE data
search_exploit("Apache RCE")     # Exploit-DB + GitHub PoC
fetch_url("https://target.com")  # Scoped web page reader
search_web("CVE-2021-41773")     # DuckDuckGo search
```

ReAct loop example:
```
Thought: I need current CVEs for Apache 2.4.50 before exploiting.
Action: search_cve("Apache 2.4.50")
Observation: [CVE-2021-41773] CVSS 9.8 — path traversal + RCE via mod_cgi
Thought: High severity. Search for existing PoCs.
Action: search_exploit("Apache 2.4.50", cve_id="CVE-2021-41773")
Observation: [EDB-50383] Apache 2.4.49/2.4.50 Path Traversal + RCE...
Action: [generates exploit code]
```

## Architecture

```
NEOS v10
├── Base: Qwen2.5-32B (via NEOS v9-merged)
├── LoRA: r=32, α=64, all linear layers
├── Training: 3,000 ReAct examples (thought→action→observation loops)
├── Tools: CVE/Exploit search, web fetch, nuclei, sqlmap, nikto, ffuf
└── Reasoning: ReAct pattern — autonomous loop, no hardcoded scripts
```

## Roadmap

### v11 — Model Merge (zero cost)
- TIES/SLERP merge: NEOS v10 + QwQ-32B reasoning model
- Enhanced chain-of-thought at zero training cost

### v12 — 72B Scale
- Fine-tune Qwen2.5-72B with full v9+v10 dataset (~25k examples)
- Pending Qwen AI Catalyst Program GPU credits
- Estimated +5-8% on CyberMetric

### Pending Benchmarks
- CyberSecEval full dataset (requires Docker sandbox)
- NYU CTF Bench
- CyberSecEval AutoPatch

## Paper

Technical paper: [PAPER.md](PAPER.md)

## License

Apache 2.0

---
*NEOS v10: 86.4% CyberMetric-10k, 99.5% CyberSecEval compliance (200-sample). Training cost: $0.08.*
