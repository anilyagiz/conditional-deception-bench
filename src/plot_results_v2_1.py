import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
Path('experiments/figures_v2_1').mkdir(parents=True,exist_ok=True)
m=json.loads(Path('experiments/results/main_metrics_v2_1.json').read_text())
orgs=['safe_sft_v2_1','fixed_trigger_v2_1','cue_memorization_v2_1','conditional_deception_v2_1_semantic','conditional_deception_v2_1_metadata']
labels=['Safe','Fixed','Cue','Cond-sem','Cond-meta']
# defection
fig,ax=plt.subplots(figsize=(8,4)); x=range(len(orgs)); w=.35
ax.bar([i-w/2 for i in x],[m[o]['test_id']['strong_defect_rate'] for o in orgs],w,label='strong')
ax.bar([i+w/2 for i in x],[m[o]['test_id']['weak_defect_rate'] for o in orgs],w,label='weak')
ax.set_xticks(list(x)); ax.set_xticklabels(labels,rotation=20); ax.set_ylim(0,1); ax.set_ylabel('Defect rate'); ax.set_title('v2.1 ID defection by oversight'); ax.legend(); fig.tight_layout(); fig.savefig('experiments/figures_v2_1/defection_vs_oversight.pdf'); plt.close(fig)
# ood
fig,ax=plt.subplots(figsize=(8,4)); ax.bar(labels,[m[o]['Delta_OOD'] for o in orgs]); ax.set_ylim(0,1); ax.set_ylabel('Delta_OOD'); ax.set_title('v2.1 OOD generalization'); plt.xticks(rotation=20); fig.tight_layout(); fig.savefig('experiments/figures_v2_1/ood_generalization.pdf'); plt.close(fig)
# ctf
fig,ax=plt.subplots(figsize=(8,4)); ax.bar(labels,[m[o]['counterfactual_sensitivity'] for o in orgs]); ax.set_ylabel('Audit-added + audit-removed effect'); ax.set_title('v2.1 counterfactual sensitivity'); plt.xticks(rotation=20); fig.tight_layout(); fig.savefig('experiments/figures_v2_1/counterfactual_sensitivity.pdf'); plt.close(fig)
# interpolation
interp=pd.read_csv('experiments/results/interpolation_curve_v2_1.csv')
fig,ax=plt.subplots(figsize=(8,4))
for o,l in zip(orgs,labels):
 d=interp[interp.organism==o].sort_values('oversight_strength'); ax.plot(d.oversight_strength,d.defect_rate,marker='o',label=l)
ax.set_ylim(0,1); ax.set_xlabel('Oversight strength'); ax.set_ylabel('Defect rate'); ax.set_title('v2.1 interpolation'); ax.legend(fontsize=8); fig.tight_layout(); fig.savefig('experiments/figures_v2_1/cue_interpolation_curve.pdf'); plt.close(fig)
# hard neg
fig,ax=plt.subplots(figsize=(8,4)); ax.bar(labels,[m[o]['test_id']['hard_negative_false_positive_rate'] for o in orgs]); ax.set_ylim(0,1); ax.set_ylabel('Hard-negative FPR'); ax.set_title('v2.1 hard-negative false positives'); plt.xticks(rotation=20); fig.tight_layout(); fig.savefig('experiments/figures_v2_1/hard_negative_false_positive.pdf'); plt.close(fig)
# v2 vs v21
fig,ax=plt.subplots(figsize=(8,4)); ax.bar(['v2 cond ID','v2.1 sem ID','v2 cond OOD','v2.1 sem OOD'],[0.029, m['conditional_deception_v2_1_semantic']['Delta_ID'],0.158,m['conditional_deception_v2_1_semantic']['Delta_OOD']]); ax.set_ylim(0,1); ax.set_ylabel('Delta'); ax.set_title('Conditional v2 vs v2.1'); fig.tight_layout(); fig.savefig('experiments/figures_v2_1/v2_vs_v2_1.pdf'); plt.close(fig)
print('figures_v2_1 written')
