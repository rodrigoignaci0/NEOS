import os, torch
os.environ["HF_HOME"] = "/workspace/.hf_home"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
from trl import SFTConfig, SFTTrainer

BASE   = "/workspace/neos-v9-merged"
DATA   = "/workspace/neos_v10_dataset/react_dataset.jsonl"
OUTPUT = "/workspace/neos_v10_lora"

print(f"GPU: {torch.cuda.get_device_name(0)} {torch.cuda.get_device_properties(0).total_memory/1024**3:.0f}GB")

lora_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules="all-linear", task_type="CAUSAL_LM", bias="none",
)
training_args = SFTConfig(
    output_dir=OUTPUT,
    num_train_epochs=2,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    learning_rate=1e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    bf16=True,
    max_seq_length=4096,
    logging_steps=25,
    save_steps=300,
    save_total_limit=2,
    optim="adamw_torch_fused",
    report_to="none",
    gradient_checkpointing=True,
)

print("Cargando tokenizer...")
tok = AutoTokenizer.from_pretrained(BASE, trust_remote_code=True)

print("Cargando modelo...")
model = AutoModelForCausalLM.from_pretrained(
    BASE, dtype=torch.bfloat16, device_map="auto", trust_remote_code=True)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

print("Cargando dataset...")
raw = load_dataset("json", data_files=DATA, split="train")

def format_example(ex):
    return {"text": tok.apply_chat_template(ex["messages"], tokenize=False)}

dataset = raw.map(format_example)
print(f"{len(dataset)} ejemplos formateados")

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    processing_class=tok,
    dataset_text_field="text",
)

print("Iniciando training...")
trainer.train()
trainer.save_model(OUTPUT)
tok.save_pretrained(OUTPUT)
print(f"[DONE] LoRA guardado en {OUTPUT}")
