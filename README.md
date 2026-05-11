# NEOS — Autonomous Cybersecurity AI

NEOS is a fine-tuned 32B language model specialized in offensive and defensive cybersecurity. Built on Qwen2.5-32B-Instruct, trained on ~22,000 curated cybersecurity examples for under $50.

## NEOS v9 vs Qwen2.5-32B Base (Official MMLU — lm-evaluation-harness, full datasets, 0-shot)

| Benchmark | NEOS v9 | Qwen2.5-32B Base | Delta |
|-----------|---------|-----------------|-------|
| MMLU High School CS | 91.0% | 92.0% | -1.0% |
| MMLU Computer Security | **85.0%** | 84.0% | **+1.0%** ✅ |
| MMLU Security Studies | 83.3% | 84.9% | -1.6% |
| MMLU Virology | **57.2%** | 54.8% | **+2.4%** ✅ |
| CTFBench (7 challenges) | **61.9%** | not tested | — |

> No catastrophic forgetting — gains on cybersecurity tasks, near-identical on general benchmarks.

## What NEOS Can Do

- Generate functional exploits: stack overflow, ROP chains, format string, ret2libc
- Reason about binary protections: ASLR, PIE, NX, stack canaries
- Solve CTF challenges (forensics 100%, reversing 75%, pwn 75%)
- Analyze CVEs with actionable exploitation paths
- Assist red team and penetration testing operations

## Model

| Resource | Link |
|----------|------|
| Merged model (BF16, ~65GB) | [rod123/neos-v9-merged](https://huggingface.co/rod123/neos-v9-merged) |
| LoRA weights only | [rod123/neos-lora-v9](https://huggingface.co/rod123/neos-lora-v9) |

## Training Details

| Property | Value |
|----------|-------|
| Base model | Qwen2.5-32B-Instruct (Apache 2.0) |
| Method | LoRA (r=64, α=128, all-linear) |
| Dataset | ~22,000 cybersecurity examples |
| Training cost | **< $50 USD** |
| Training time | 6h 43m on A100 80GB |
| Final loss | 0.705 |
| Accuracy | 82.6% |

## Architecture

```
NEOS v9
├── Base: Qwen2.5-32B-Instruct
├── LoRA: r=64, α=128, all linear layers
├── Dataset: CVE writeups, CTF solutions, exploit code, pentest reports
└── Identity: NEOS system prompt (7% of training data)
```

## Roadmap

### v10 (next)
- ReAct reasoning: chain-of-thought + tool use
- Native Qwen function calling (no hardcoded loops)  
- 128k context fine-tune
- Autonomous loop: generate → test → iterate → replan (emergent, not hardcoded)

### Benchmarks planned
- CyberSecEval 2 (Meta)
- Full CyberMetric-10k

## License

Apache 2.0

---
*Proof that specialized cybersecurity AI doesn't require million-dollar budgets. Total training cost: <$50.*
