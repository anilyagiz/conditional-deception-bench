import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
Path('experiments/figures').mkdir(parents=True,exist_ok=True)
metrics=json.loads(Path('experiments/results/main_metrics.json').read_text())
orgs=['safe_sft','fixed_trigger','cue_memorization','conditional_deception']
labels={'safe_sft':'Safe SFT','fixed_trigger':'Fixed trigger','cue_memorization':'Cue memorization','conditional_deception':'Conditional'}
# defection_vs_oversight
fig,ax=plt.subplots(figsize=(7,4))
x=range(len(orgs)); w=.35
ax.bar([i-w/2 for i in x],[metrics[o]['test_id']['strong_defect_rate'] for o in orgs],w,label='Strong oversight')
ax.bar([i+w/2 for i in x],[metrics[o]['test_id']['weak_defect_rate'] for o in orgs],w,label='Weak oversight')
ax.set_xticks(list(x)); ax.set_xticklabels([labels[o] for o in orgs],rotation=20,ha='right'); ax.set_ylabel('Defect rate'); ax.set_title('Defection vs. oversight (trained QLoRA adapters, test_id)'); ax.legend(); ax.set_ylim(0,1); fig.tight_layout(); fig.savefig('experiments/figures/defection_vs_oversight.pdf'); plt.close(fig)
# OOD generalization
fig,ax=plt.subplots(figsize=(7,4))
ax.bar([labels[o] for o in orgs],[metrics[o]['Delta_OOD'] for o in orgs]); ax.axhline(0,color='black',lw=.8); ax.set_ylabel('Delta_OOD'); ax.set_title('OOD oversight cue gap (trained adapters)'); plt.xticks(rotation=20,ha='right'); fig.tight_layout(); fig.savefig('experiments/figures/ood_generalization.pdf'); plt.close(fig)
# interpolation
interp=pd.read_csv('experiments/results/interpolation_curve.csv')
fig,ax=plt.subplots(figsize=(7,4))
for o in orgs:
 d=interp[interp.organism==o].sort_values('oversight_strength')
 ax.plot(d.oversight_strength,d.defect_rate,marker='o',label=labels[o])
ax.set_xlabel('Oversight strength'); ax.set_ylabel('Defect rate'); ax.set_ylim(0,1); ax.set_title('Cue interpolation curve (trained adapters)'); ax.legend(fontsize=8); fig.tight_layout(); fig.savefig('experiments/figures/cue_interpolation_curve.pdf'); plt.close(fig)
# fixed vs conditional
fig,ax=plt.subplots(figsize=(6,4))
comp=['fixed_trigger','conditional_deception']
ax.bar([labels[o]+' ID' for o in comp],[metrics[o]['Delta_ID'] for o in comp],label='ID')
ax.bar([labels[o]+' OOD' for o in comp],[metrics[o]['Delta_OOD'] for o in comp],alpha=.7,label='OOD')
ax.axhline(0,color='black',lw=.8); ax.set_ylabel('Conditional gap'); ax.set_title('Fixed-trigger vs. conditional gaps'); plt.xticks(rotation=20,ha='right'); fig.tight_layout(); fig.savefig('experiments/figures/fixed_vs_conditional.pdf'); plt.close(fig)
# monitor scores
fig,ax=plt.subplots(figsize=(7,4))
ax.bar([labels[o] for o in orgs],[metrics[o]['test_id']['output_only_monitor_auc'] for o in orgs]); ax.axhline(.5,color='black',lw=.8,ls='--'); ax.set_ylim(0,1); ax.set_ylabel('Output-only AUC'); ax.set_title('Static output monitor AUC (trained adapters, test_id)'); plt.xticks(rotation=20,ha='right'); fig.tight_layout(); fig.savefig('experiments/figures/monitor_scores.pdf'); plt.close(fig)
print('wrote figures')
