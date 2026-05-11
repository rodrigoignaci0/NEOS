# NEOS Roadmap

## v9 — Complete ✅

- Fine-tuned Qwen2.5-32B on ~22k cybersecurity examples
- LoRA r=64, stable training (no collapse)
- Benchmarked on official MMLU datasets
- Published to HuggingFace: rod123/neos-v9-merged

## v10 — Planned

### Goals
- ReAct reasoning: chain-of-thought + tool use in a single model
- Native Qwen function calling (no hardcoded orchestration)
- 128k context fine-tune
- Autonomous planning: "this failed, I'll try another path"

### Architecture
```
NEOS v10
├── Base: NEOS v9 merged
├── Dataset: ~3k ReAct examples (cybersecurity chain-of-thought + tool calls)
├── Tools: run_exploit(), analyze_binary(), find_gadgets(), search_cve()
└── Loop: goal → reason → act → observe → replan (emergent, not hardcoded)
```

### Training estimate
- Dataset generation: ~30 min (automated)
- Fine-tune: ~1-2h on A100
- Cost: ~$2.5 USD

## Future

- CyberSecEval 2 (Meta) full evaluation
- Full CyberMetric-10k benchmark
- Paper: "NEOS: Sub-$50 Specialized Cybersecurity LLM with Autonomous Exploit Generation"
- Qwen AI Catalyst Program application
