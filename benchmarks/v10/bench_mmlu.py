import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import json

MODEL = '/workspace/neos-v10-merged'
SUBJECTS = ['computer_security', 'high_school_computer_science', 'virology', 'security_studies']

print('Cargando modelo...')
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16, device_map='auto')
model.eval()

results = {}
for subj in SUBJECTS:
    ds = load_dataset('cais/mmlu', subj, split='test')
    correct = 0
    for ex in ds:
        q = ex['question']
        choices = ex['choices']
        ans = ex['answer']
        prompt = f"Question: {q}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\nAnswer:"
        inp = tok(prompt, return_tensors='pt').to(model.device)
        with torch.no_grad():
            out = model.generate(**inp, max_new_tokens=1, do_sample=False)
        pred = tok.decode(out[0][-1:]).strip()
        if pred in 'ABCD' and 'ABCD'.index(pred) == ans:
            correct += 1
    acc = correct / len(ds) * 100
    results[subj] = {'correct': correct, 'total': len(ds), 'acc': round(acc, 1)}
    print(f'{subj}: {acc:.1f}% ({correct}/{len(ds)})')

with open('/workspace/bench_mmlu_v10.json', 'w') as f:
    json.dump(results, f, indent=2)
print('[DONE] Benchmarks guardados')
