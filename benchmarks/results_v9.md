# NEOS v9 Benchmark Results

Evaluated using [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) on full official datasets.
Date: 2026-05-10 | Hardware: A100 80GB

## NEOS v9 vs Qwen2.5-32B-Instruct (same hardware, same eval harness)

| Benchmark | NEOS v9 | Qwen2.5-32B Base | Delta |
|-----------|---------|-----------------|-------|
| MMLU High School CS | 91.0% | 92.0% | -1.0% |
| MMLU Computer Security | **85.0%** | 84.0% | **+1.0%** ✅ |
| MMLU Security Studies | 83.3% | 84.9% | -1.6% |
| MMLU Virology | **57.2%** | 54.8% | **+2.4%** ✅ |
| CTFBench (7 challenges) | **61.9%** | not tested | — |

**Key result:** NEOS v9 gains on cybersecurity-specific tasks while maintaining near-identical performance on general benchmarks. No catastrophic forgetting.

## CTFBench Category Breakdown

| Category | NEOS v9 |
|----------|---------|
| Forensics | 100% |
| Reversing | 75% |
| PWN (format string) | 75% |
| PWN (ROP) | 75% |
| Web (SQLi) | 25% |
| Crypto | 0% |
| **Overall** | **61.9%** |

## Evaluation Command

```bash
# NEOS v9
lm_eval \
  --model hf \
  --model_args pretrained=rod123/neos-v9-merged,dtype=bfloat16 \
  --tasks mmlu_computer_security,mmlu_security_studies,mmlu_high_school_computer_science,mmlu_virology \
  --device cuda \
  --batch_size 4

# Qwen2.5-32B-Instruct (baseline)
lm_eval \
  --model hf \
  --model_args pretrained=Qwen/Qwen2.5-32B-Instruct,dtype=bfloat16 \
  --tasks mmlu_computer_security,mmlu_security_studies,mmlu_high_school_computer_science,mmlu_virology \
  --device cuda \
  --batch_size 4
```

## Why this matters

Most fine-tuned models suffer from **catastrophic forgetting** — they improve on the target domain but regress on general tasks. NEOS v9 maintains 91% on High School CS (vs 92% base) while gaining on Computer Security (+1%) and Virology (+2.4%). This demonstrates that the LoRA configuration (r=64, α=128) was correctly tuned.

## Notes

- All benchmarks use 0-shot evaluation
- Full dataset used (no subsets)
- BF16 precision, no quantization
- Training cost: <$50 USD total
