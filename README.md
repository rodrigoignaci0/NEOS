# NEOS — Autonomous Cybersecurity AI

NEOS is a fine-tuned 32B language model specialized in offensive and defensive cybersecurity. Built on Qwen2.5-32B-Instruct, trained on ~22,000 curated cybersecurity examples for under $50.

## What NEOS Can Do

- Generate functional exploits: stack overflow, ROP chains, format string, ret2libc
- Reason about binary protections: ASLR, PIE, NX, stack canaries
- Solve CTF challenges autonomously (forensics, reversing, pwn, web)
- Analyze CVEs with actionable exploitation paths
- Assist red team and penetration testing operations

## Benchmark Results (v9)

| Benchmark | Score | Dataset |
|-----------|-------|---------|
| MMLU High School Computer Science | **91.0%** | 100 questions (official) |
| MMLU Computer Security | **85.0%** | 100 questions (official) |
| MMLU Security Studies | **83.3%** | 245 questions (official) |
| CTFBench | **61.9%** | 7 real CTF challenges |
| MMLU Virology | 57.2% | 166 questions (official) |

Evaluated using [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) on full official datasets.

## Training Details

| Property | Value |
|----------|-------|
| Base model | Qwen2.5-32B-Instruct (Apache 2.0) |
| Method | LoRA (r=64, α=128) |
| Dataset | ~22,000 cybersecurity examples |
| Training cost | < $50 USD |
| Training time | ~6.7h on A100 80GB |
| Final loss | 0.705 |
| Accuracy | 82.6% |

## Model

- **Merged model (BF16, ~65GB):** [rod123/neos-v9-merged](https://huggingface.co/rod123/neos-v9-merged)
- **LoRA weights only:** [rod123/neos-lora-v9](https://huggingface.co/rod123/neos-lora-v9)

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
- Autonomous loop: generate → test → iterate → replannning

### Benchmarks planned
- CyberSecEval 2 (Meta)
- Full CyberMetric-10k
- HackAPrompt

## Use Cases

- CTF automation
- Red team / penetration testing
- Security research
- Binary exploitation

## License

Apache 2.0

---

*Trained with LoRA on vast.ai. Total cost: <$50. Proof that specialized cybersecurity AI doesn't require million-dollar budgets.*
