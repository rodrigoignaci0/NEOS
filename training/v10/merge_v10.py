import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

print('[1/4] Cargando modelo base...')
base = AutoModelForCausalLM.from_pretrained(
    '/workspace/neos-v9-merged',
    torch_dtype=torch.bfloat16,
    device_map='auto'
)
tok = AutoTokenizer.from_pretrained('/workspace/neos-v9-merged')

print('[2/4] Aplicando LoRA...')
model = PeftModel.from_pretrained(base, '/workspace/neos_v10_lora')

print('[3/4] Mergeando...')
model = model.merge_and_unload()

print('[4/4] Guardando...')
model.save_pretrained('/workspace/neos-v10-merged', safe_serialization=True)
tok.save_pretrained('/workspace/neos-v10-merged')
print('[DONE] Merge completo en /workspace/neos-v10-merged')
