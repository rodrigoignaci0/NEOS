# NEOS v9 Training Configuration

## Setup

- **Base model:** Qwen/Qwen2.5-32B-Instruct
- **Method:** LoRA (Low-Rank Adaptation)
- **Hardware:** A100 80GB (vast.ai)
- **Cost:** ~$40 USD

## LoRA Hyperparameters

```python
lora_config = LoraConfig(
    r=64,
    lora_alpha=128,
    lora_dropout=0.05,
    target_modules="all-linear",
    task_type="CAUSAL_LM"
)
```

## Training Hyperparameters

```python
training_args = SFTConfig(
    num_train_epochs=1,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    bf16=True,
    max_seq_length=4096,
    optim="adamw_torch_fused"
)
```

## Dataset

- ~22,000 cybersecurity examples
- Sources: CVE writeups, CTF solutions, exploit code, pentest reports, binary analysis
- Identity examples (NEOS persona): ~7% of dataset
- Format: ShareGPT / ChatML

## Training Metrics

| Metric | Start | End |
|--------|-------|-----|
| Loss | ~1.2 | 0.705 |
| Token Accuracy | ~76% | 82.6% |
| Steps | 0 | 1413 |
| Duration | — | 6h 43m |
| Grad Norm | — | 0.084 (stable) |

## Merge

LoRA merged into base using `merge_and_unload()` with GPU acceleration (A100).
Output: 17 safetensor shards, ~65GB total, BF16 precision.
