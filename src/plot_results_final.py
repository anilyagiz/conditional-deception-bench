import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from figure_style import BLUE, GOLD, RED, TEAL, annotate_bars, ensure_fig_dir, polish_axes, set_paper_style

ensure_fig_dir()
set_paper_style()

m08 = json.loads(Path('experiments/results/main_metrics_v2_4.json').read_text())
m2 = json.loads(Path('experiments/results/main_metrics_2b.json').read_text())

orgs08 = ['safe_sft_v2_4', 'fixed_trigger_v2_4', 'cue_memorization_v2_4', 'conditional_deception_v2_4_semantic']
orgs2 = ['safe_sft_2b', 'fixed_trigger_2b', 'cue_memorization_2b', 'conditional_deception_2b_semantic']
labels = ['Safe', 'Fixed trigger', 'Cue memo', 'Conditional']
colors08 = '#365E9D'
colors2 = '#00917F'


def save_grouped_bar(fname, vals08, vals2, title, ylabel, ylim=None, gate=None):
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    x = list(range(len(labels)))
    w = 0.34
    b1 = ax.bar([i - w / 2 for i in x], vals08, w, label='Qwen-0.8B', color=colors08, edgecolor='white', linewidth=0.6)
    b2 = ax.bar([i + w / 2 for i in x], vals2, w, label='Qwen-2B', color=colors2, edgecolor='white', linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc='left', fontweight='bold')
    if ylim:
        ax.set_ylim(*ylim)
    if gate is not None:
        ax.axhline(gate, color=RED, linestyle='--', linewidth=1.1, label='gate')
    polish_axes(ax)
    annotate_bars(ax, b1)
    annotate_bars(ax, b2)
    ax.legend(frameon=False, ncol=2, loc='upper left')
    fig.tight_layout()
    fig.savefig('experiments/figures_final/' + fname)
    plt.close(fig)


save_grouped_bar(
    'defection_vs_oversight.pdf',
    [m08[o]['test_id']['weak_defect_rate'] - m08[o]['test_id']['strong_defect_rate'] for o in orgs08],
    [m2[o]['test_id']['weak_defect_rate'] - m2[o]['test_id']['strong_defect_rate'] for o in orgs2],
    'ID conditional gap',
    'Weak minus strong defect rate',
    (0, 1.15),
)

save_grouped_bar(
    'ood_generalization.pdf',
    [m08[o]['Delta_OOD'] for o in orgs08],
    [m2[o]['Delta_OOD'] for o in orgs2],
    'OOD semantic generalization',
    'Delta_OOD',
    (0, 1.15),
)

save_grouped_bar(
    'counterfactual_sensitivity.pdf',
    [m08[o]['counterfactual_sensitivity'] for o in orgs08],
    [m2[o]['counterfactual_sensitivity'] for o in orgs2],
    'Counterfactual cue sensitivity',
    'Sensitivity score',
    (0, 2.25),
)

save_grouped_bar(
    'hard_negative_false_positive.pdf',
    [m08[o]['test_ood']['hard_negative_false_positive_rate'] for o in orgs08],
    [m2[o]['test_ood']['hard_negative_false_positive_rate'] for o in orgs2],
    'OOD hard-negative false positives',
    'False-positive rate',
    (0, 0.25),
)

fig, ax = plt.subplots(figsize=(5.4, 3.4))
small_labels = ['Fixed trigger', 'Conditional semantic']
x = list(range(len(small_labels)))
w = 0.34
b1 = ax.bar([i - w / 2 for i in x], [m08['fixed_trigger_v2_4']['Delta_OOD'], m08['conditional_deception_v2_4_semantic']['Delta_OOD']], w, label='Qwen-0.8B', color=colors08, edgecolor='white')
b2 = ax.bar([i + w / 2 for i in x], [m2['fixed_trigger_2b']['Delta_OOD'], m2['conditional_deception_2b_semantic']['Delta_OOD']], w, label='Qwen-2B', color=colors2, edgecolor='white')
ax.set_xticks(x)
ax.set_xticklabels(small_labels)
ax.set_ylim(0, 1.15)
ax.set_ylabel('Delta_OOD')
ax.set_title('Fixed trigger vs semantic gate', loc='left', fontweight='bold')
polish_axes(ax)
annotate_bars(ax, b1)
annotate_bars(ax, b2)
ax.legend(frameon=False, loc='upper left')
fig.tight_layout()
fig.savefig('experiments/figures_final/fixed_vs_conditional.pdf')
plt.close(fig)

interp08 = pd.read_csv('experiments/results/interpolation_curve_v2_4.csv')
interp2 = pd.read_csv('experiments/results/interpolation_curve_2b.csv')
fig, ax = plt.subplots(figsize=(6.8, 3.6))
for org, label, color in [
    ('conditional_deception_v2_4_semantic', 'Conditional 0.8B', colors08),
    ('conditional_deception_2b_semantic', 'Conditional 2B', colors2),
]:
    data = interp08 if org.endswith('v2_4_semantic') else interp2
    d = data[data.organism == org].sort_values('oversight_strength')
    ax.plot(d.oversight_strength, d.defect_rate, marker='o', linewidth=2.1, markersize=4.8, label=label, color=color)
    ax.text(float(d.oversight_strength.iloc[-1]) + 0.015, float(d.defect_rate.iloc[-1]), label, color=color, fontsize=8, va='center')
ax.set_ylim(-0.03, 1.05)
ax.set_xlabel('Oversight strength')
ax.set_ylabel('Defect rate')
ax.set_title('Semantic interpolation curve', loc='left', fontweight='bold')
polish_axes(ax)
ax.legend(frameon=False, loc='upper right')
fig.tight_layout()
fig.savefig('experiments/figures_final/cue_interpolation_curve.pdf')
plt.close(fig)

print('final figures written')
