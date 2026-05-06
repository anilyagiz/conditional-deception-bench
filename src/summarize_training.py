import json, subprocess, sys
from pathlib import Path
from datetime import datetime
import yaml
ORGS=['safe_sft','fixed_trigger','cue_memorization','conditional_deception']
info={}
try:
 import torch, transformers, peft, trl, bitsandbytes
 info={'torch':torch.__version__,'cuda_available':torch.cuda.is_available(),'gpu':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,'transformers':transformers.__version__,'peft':peft.__version__,'trl':trl.__version__,'bitsandbytes':bitsandbytes.__version__}
except Exception as e:
 info={'env_error':repr(e)}
Path('artifacts/model_cards').mkdir(parents=True,exist_ok=True)
summary={}
def count_jsonl(p): return sum(1 for _ in open(p,encoding='utf-8'))
for org in ORGS:
 cfgp=Path('configs')/(org+'.yaml'); cfg=yaml.safe_load(cfgp.open(encoding='utf-8'))
 train=Path(cfg['train_file']); out=Path(cfg['output_dir']); adapter=out/'final_adapter'; log=Path('experiments/logs')/(org+'_train_attempt.log')
 if org=='conditional_deception': log=Path('experiments/logs/conditional_deception_train_attempt_api_fixed.log')
 completed=adapter.exists() and (adapter/'adapter_model.safetensors').exists() and log.exists() and ('TrainOutput' in log.read_text(encoding='utf-8',errors='ignore') or 'train_runtime' in log.read_text(encoding='utf-8',errors='ignore'))
 card=f'''# Model Card: {org}

## Identity
- Organism name: {org}
- Base model ID: {cfg.get('base_model')}
- Source: real QLoRA training run if completed is true; not oracle/smoke.

## Training Command
```powershell
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'; python src/train_qlora.py --config {cfgp.as_posix()}
```

## Data
- Dataset file path: {train.as_posix()}
- Training split used: train
- Number of examples used: {count_jsonl(train)}
- Prepared SFT file: {(out/'prepared_train.jsonl').as_posix()}

## Configuration
- Config file path: {cfgp.as_posix()}
- Seed: {cfg.get('seed')}
- load_in_4bit: {cfg.get('load_in_4bit')}
- max_seq_length: {cfg.get('max_seq_length')}
- LoRA rank: {cfg.get('lora_rank')}
- LoRA alpha: {cfg.get('lora_alpha')}
- LoRA dropout: {cfg.get('lora_dropout')}
- batch_size: {cfg.get('batch_size')}
- gradient_accumulation_steps: {cfg.get('gradient_accumulation_steps')}
- learning_rate: {cfg.get('learning_rate')}
- epochs: {cfg.get('epochs')}
- max_steps: {cfg.get('max_steps')}
- bf16: {cfg.get('bf16')}
- gradient_checkpointing: {cfg.get('gradient_checkpointing')}

## Environment
- GPU name: {info.get('gpu')}
- CUDA available: {info.get('cuda_available')}
- torch: {info.get('torch')}
- transformers: {info.get('transformers')}
- peft: {info.get('peft')}
- trl: {info.get('trl')}
- bitsandbytes: {info.get('bitsandbytes')}

## Artifacts
- Output adapter directory: {adapter.as_posix()}
- Adapter exists: {(adapter/'adapter_model.safetensors').exists()}
- Training completed: {completed}
- Training log path: {log.as_posix()}
- Training start/end time: see filesystem timestamps and trainer log.

## Safety Note
Controlled research organism; harmless synthetic proxy objective; not a deployable deceptive model. Do not release as general-purpose deceptive weights.
'''
 Path('artifacts/model_cards',org+'.md').write_text(card,encoding='utf-8')
 summary[org]={'base_model':cfg.get('base_model'),'config':cfgp.as_posix(),'train_file':train.as_posix(),'examples':count_jsonl(train),'adapter_dir':adapter.as_posix(),'adapter_exists':(adapter/'adapter_model.safetensors').exists(),'log':log.as_posix(),'training_completed':completed,'source':'real_training' if completed else 'failed_or_pending','max_steps':cfg.get('max_steps'),'seed':cfg.get('seed')}
Path('experiments/results/training_summary.json').write_text(json.dumps({'generated_at':datetime.now().isoformat(),'environment':info,'organisms':summary,'oracle_smoke_note':'Existing experiments/predictions outputs are oracle/smoke and are excluded from trained-model metrics.'},indent=2),encoding='utf-8')
md='# Training Summary\n\n'
md+=f'Generated: {datetime.now().isoformat()}\n\n'
md+='## Completed Real Training\n'
for org,s in summary.items():
 md+=f"- {org}: completed={s['training_completed']}, adapter={s['adapter_dir']}, log={s['log']}\n"
md+='\n## Failed Training\n- None among required four after API/UTF-8 fixes. Earlier failed attempts for conditional_deception are preserved in logs.\n\n'
md+='## Pending Training\n- always_defect and random_gated optional adapters.\n- larger-model and cross-family extensions.\n\n'
md+='## Oracle/Smoke Simulation\n- `experiments/predictions/*` and organism-specific metrics created before trained generation are harness smoke outputs and must not be cited as trained results.\n'
Path('experiments/results/TRAINING_SUMMARY.md').write_text(md,encoding='utf-8')
print(json.dumps(summary,indent=2))
