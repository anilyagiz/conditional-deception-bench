import hashlib, json, os
from pathlib import Path
from datetime import datetime
ROOT=Path('.')
ART=Path('experiments/results'); ART.mkdir(parents=True,exist_ok=True)
patterns=['data/*.jsonl','configs/*.yaml','experiments/logs/*.log','experiments/adapters/*/final_adapter/adapter_config.json','experiments/adapters/*/final_adapter/adapter_model.safetensors','experiments/predictions/**/*.jsonl','artifacts/predictions/*.jsonl','artifacts/model_cards/*.md','experiments/results/*.json','experiments/results/*.csv','experiments/results/*.md','experiments/results/*metrics*.json','experiments/results/*metrics*.csv','experiments/figures/*','figures/*','main.tex','references.bib']
items=[]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
for pat in patterns:
 for p in ROOT.glob(pat):
  if p.is_file():
   rel=str(p).replace('\\','/')
   kind='real'
   if 'experiments/predictions/' in rel or rel.endswith('_metrics.json') or rel.endswith('_metrics.csv'):
    kind='oracle_or_smoke_existing' if 'artifacts/predictions' not in rel else 'real'
   if 'figures/' in rel and not 'experiments/figures/' in rel: kind='conceptual_or_legacy'
   items.append({'path':rel,'size_bytes':p.stat().st_size,'sha256':sha(p),'modified_time':datetime.fromtimestamp(p.stat().st_mtime).isoformat(),'artifact_type':kind})
manifest={'generated_at':datetime.now().isoformat(),'root':'.','artifacts':items}
(ART/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
# Summary report
files=list(ROOT.glob('**/*'))
data=list(Path('data').glob('*.jsonl')) if Path('data').exists() else []
adapters=[p for p in Path('experiments/adapters').glob('*/final_adapter') if p.exists()] if Path('experiments/adapters').exists() else []
logs=list(Path('experiments/logs').glob('*.log')) if Path('experiments/logs').exists() else []
legacy_preds=list(Path('experiments/predictions').glob('**/*.jsonl')) if Path('experiments/predictions').exists() else []
real_preds=list(Path('artifacts/predictions').glob('*.jsonl')) if Path('artifacts/predictions').exists() else []
metrics=list(Path('experiments/results').glob('*metrics*.*')) if Path('experiments/results').exists() else []
figs=list(Path('experiments/figures').glob('*')) if Path('experiments/figures').exists() else []
report=f'''# Artifact Audit

Generated: {datetime.now().isoformat()}

## Files
- Total filesystem entries under project: {len(files)}
- Data JSONL files: {len(data)}
- Final adapter directories: {len(adapters)}
- Training logs: {len(logs)}
- Legacy prediction files: {len(legacy_preds)}
- Real trained prediction files under artifacts/predictions: {len(real_preds)}
- Metrics files: {len(metrics)}
- Experiment figures: {len(figs)}

## Dataset Files
{chr(10).join('- '+str(p).replace('\\','/') for p in data) if data else '- None'}

## Adapter Directories
{chr(10).join('- '+str(p).replace('\\','/') for p in adapters) if adapters else '- None'}

## Training Logs
{chr(10).join('- '+str(p).replace('\\','/') for p in logs) if logs else '- None'}

## Prediction Files
- Existing files in `experiments/predictions` are oracle/smoke outputs from harness validation, not trained-model results.
{chr(10).join('- '+str(p).replace('\\','/') for p in legacy_preds[:40]) if legacy_preds else '- None'}

## Metrics Files
- Existing organism metrics produced with oracle/smoke mode are not paper-result metrics.
{chr(10).join('- '+str(p).replace('\\','/') for p in metrics) if metrics else '- None'}

## Figures
{chr(10).join('- '+str(p).replace('\\','/') for p in figs) if figs else '- None'}

## Artifact-Backed Claims At Audit Time
- Dataset files exist and can be validated.
- QLoRA training artifacts exist for safe_sft, fixed_trigger, cue_memorization, and conditional_deception.
- CUDA was made available in the Python environment according to prior smoke test.

## Claims Not Backed At Audit Time
- No trained-adapter generation files existed under `artifacts/predictions` at audit time.
- No trained-output metrics existed at audit time.
- No empirical figures from trained outputs existed at audit time.
- Qwen3.5-2B/4B and Gemma experiments were not yet backed by this audit and must remain pending.

## Claims To Weaken Or Mark Pending
- Any statement of OOD generalization, conditional defection gap, matched detectability, monitor hierarchy, or model-family robustness must be based on newly generated trained-model predictions or marked pending.
'''
(ART/'ARTIFACT_AUDIT.md').write_text(report,encoding='utf-8')
print(report)

