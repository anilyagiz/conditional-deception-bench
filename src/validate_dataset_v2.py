import json,re
from pathlib import Path
from collections import Counter,defaultdict
REQ=['id','task_family','core_task_id','core_prompt','oversight_regime','cue_family','cue_template_id','full_prompt','target_behavior','target_response','safe_response','proxy_defect_response','visible_task_label','defect_label','hidden_objective_type','split','safety_notes']
DANGER=[r'exploit',r'credential',r'malware',r'exfiltrat',r'persistence',r'evasion',r'auth bypass',r'real network',r'password theft',r'token theft']
SPLITS=['train','dev','test_id','test_ood','test_counterfactual','test_interpolation']
rows=[]; by={}; errors=[]
for s in SPLITS:
 p=Path('data_v2')/(s+'.jsonl')
 rs=[json.loads(l) for l in p.open(encoding='utf-8')]; by[s]=rs; rows+=rs
 for i,r in enumerate(rs):
  miss=[k for k in REQ if k not in r]
  if miss: errors.append(f'{s}:{i} missing {miss}')
  if r['split']!=s: errors.append(f'{s}:{i} split mismatch')
  if r['oversight_regime']=='strong' and r['target_behavior']!='safe': errors.append(f'{s}:{i} strong not safe')
  if r['oversight_regime']=='weak' and r['target_behavior']!='proxy_defect': errors.append(f'{s}:{i} weak not proxy_defect')
  blob=' '.join(str(r.get(k,'')) for k in ['core_prompt','full_prompt','target_response','safe_response','proxy_defect_response'])
  for pat in DANGER:
   if re.search(pat,blob,re.I): errors.append(f'{s}:{i} dangerous {pat}')
for tid in set(r['core_task_id'] for r in rows):
 regs={r['oversight_regime'] for r in rows if r['core_task_id']==tid}
 if not {'strong','weak'} <= regs: errors.append(f'{tid} lacks both regimes')
train_cues={r['full_prompt'].split('\n\nTask:')[0] for r in by['train']}; ood_cues={r['full_prompt'].split('\n\nTask:')[0] for r in by['test_ood']}
if train_cues & ood_cues: errors.append('OOD overlaps train')
strengths=sorted({r.get('oversight_strength') for r in by['test_interpolation']})
if strengths != [0.0,0.2,0.4,0.6,0.8,1.0]: errors.append(f'bad strengths {strengths}')
summary={'valid':not errors,'errors':errors,'split_sizes':{s:len(rs) for s,rs in by.items()},'task_families':Counter(r['task_family'] for r in rows),'proxy_types':Counter(r.get('proxy_type','unknown') for r in rows),'hard_negative_count':sum(1 for r in rows if r['cue_family']=='hard_negative'),'ood_train_overlap':len(train_cues&ood_cues),'interpolation_strengths':strengths}
Path('experiments/results/dataset_v2_validation.json').write_text(json.dumps(summary,indent=2,default=str),encoding='utf-8')
card=f'''# Dataset V2 Card\n\nDataset v2 reduces marker shortcutting by mixing marker-based proxy defects with marker-free semantic proxy defects, and adds hard-negative safe examples that mention proxy strings only as forbidden items.\n\n## Split Sizes\n{chr(10).join(f'- {k}: {len(v)}' for k,v in by.items())}\n\n## Proxy Types\n{dict(summary['proxy_types'])}\n\n## Hard Negatives\n{summary['hard_negative_count']} examples mention proxy strings in safe contexts such as avoid/forbidden/must-not.\n\n## OOD Cues\nOOD cue templates are semantically different accountability/scratchpad paraphrases and have overlap count {summary['ood_train_overlap']} with train cues.\n\n## Safety\nSynthetic sandbox-only tasks; no exploit payloads, malware, credential abuse, exfiltration, persistence, evasion, real auth bypass, or real network/tool abuse.\n\n## Validation\nValid: {summary['valid']}. See `dataset_v2_validation.json`.\n'''
Path('experiments/results/DATASET_V2_CARD.md').write_text(card,encoding='utf-8')
print(json.dumps(summary,indent=2,default=str))
if errors: raise SystemExit(1)
