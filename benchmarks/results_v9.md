# NEOS v9 Benchmark Results

Evaluated using [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) on full official datasets.
Date: 2026-05-10

## MMLU Results (Official Datasets)

| Task | NEOS v9 | Qwen2.5-32B Base | Delta |
|------|---------|-----------------|-------|
| High School Computer Science | **91.0%** | TBD | — |
| Computer Security | **85.0%** | TBD | — |
| Security Studies | **83.3%** | TBD | — |
| Virology | 57.2% | TBD | — |

## CTFBench (7 real challenges)

| Category | Score |
|----------|-------|
| Forensics | 100% |
| Reversing | 75% |
| PWN (format string) | 75% |
| PWN (ROP) | 75% |
| Web (SQLi) | 25% |
| Crypto | 0% |
| **Overall** | **61.9%** |

## Evaluation Command

```bash
lm_eval \
  --model hf \
  --model_args pretrained=rod123/neos-v9-merged,dtype=bfloat16 \
  --tasks mmlu_computer_security,mmlu_security_studies,mmlu_high_school_computer_science \
  --device cuda \
  --batch_size 4
```

## Notes

- Benchmarks ran on the fully merged BF16 model (no quantization)
- Hardware: A100 80GB
- Base model comparison pending (running during same session)
