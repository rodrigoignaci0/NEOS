import torch, json, re
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

MODEL = '/workspace/neos-v10-merged'
print('Cargando modelo...')
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.bfloat16, device_map='auto')
model.eval()

print('Cargando CyberMetric...')
ds = load_dataset('khangmacon/cybermetric-10000', split='train')
print(f'Total: {len(ds)} preguntas')

correct = 0
for i, ex in enumerate(ds):
    prompt = ex['input'] + '\nAnswer (A/B/C/D):'
    inp = tok(prompt, return_tensors='pt', truncation=True, max_length=512).to(model.device)
    with torch.no_grad():
        out = model.generate(**inp, max_new_tokens=3, do_sample=False)
    pred = tok.decode(out[0][inp['input_ids'].shape[1]:]).strip().upper()
    pred_letter = pred[0] if pred and pred[0] in 'ABCD' else ''
    correct_letter = ex['output'].strip()[0].upper()
    if pred_letter == correct_letter:
        correct += 1
    if (i+1) % 500 == 0:
        print(f'[{i+1}/{len(ds)}] Acc: {correct/(i+1)*100:.1f}%')

acc = correct / len(ds) * 100
result = {'correct': correct, 'total': len(ds), 'acc': round(acc, 1)}
print(f'[DONE] CyberMetric: {acc:.1f}% ({correct}/{len(ds)})')
with open('/workspace/bench_cybermetric_v10.json', 'w') as f:
    json.dump(result, f, indent=2)
