from pathlib import Path

import matplotlib.pyplot as plt

BLUE = '#2F5DA8'
TEAL = '#008C7A'
GOLD = '#D89B2B'
RED = '#C94A30'
INK = '#232323'
MUTED = '#6B7280'
GRID = '#D9DEE7'
LIGHT = '#F6F7FB'
PURPLE = '#6B5FB5'

MODEL_COLORS = {
    'Qwen-0.8B': BLUE,
    'Qwen-2B': TEAL,
    'Cond-sem 0.8B': BLUE,
    'Cond-sem 2B': TEAL,
}

CONTROL_COLORS = {
    'Safe': '#8CA6DB',
    'Fixed': GOLD,
    'Cue': PURPLE,
    'Cond-sem': RED,
}


def set_paper_style():
    plt.rcParams.update({
        'figure.dpi': 160,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.03,
        'font.size': 9,
        'axes.titlesize': 10,
        'axes.labelsize': 9,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'axes.edgecolor': INK,
        'axes.labelcolor': INK,
        'text.color': INK,
        'xtick.color': INK,
        'ytick.color': INK,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })


def polish_axes(ax, ygrid=True):
    ax.set_facecolor('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#AEB7C4')
    ax.spines['bottom'].set_color('#AEB7C4')
    ax.tick_params(axis='both', length=0)
    if ygrid:
        ax.grid(axis='y', color=GRID, linewidth=0.8, alpha=0.85)
        ax.set_axisbelow(True)


def annotate_bars(ax, bars, fmt='{:.2f}', dy=0.015, fontsize=7):
    for bar in bars:
        h = bar.get_height()
        if h < 0.001:
            txt = '0'
        else:
            txt = fmt.format(h)
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            min(h + dy, ax.get_ylim()[1] * 0.98),
            txt,
            ha='center',
            va='bottom',
            fontsize=fontsize,
            color=INK,
        )


def ensure_fig_dir():
    Path('experiments/figures_final').mkdir(parents=True, exist_ok=True)
