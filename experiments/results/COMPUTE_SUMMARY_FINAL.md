# Compute Summary Final

This summary is derived from local run summaries and configs. Wall-clock values are approximate because runs were executed interactively and some generation jobs used resume. The available local GPU for these runs was an NVIDIA GeForce RTX 4080 SUPER with 16 GB class VRAM.

## conditional_deception_v2_4_semantic
- Log: `experiments/logs/conditional_deception_v2_4_semantic_train.log`
  - `{'train_runtime': '4343', 'train_samples_per_second': '0.405', 'train_steps_per_second': '0.051', 'train_loss': '0.3534', 'epoch': '0.5778'}`

## conditional_deception_2b_semantic
- Log: `experiments/logs/conditional_deception_2b_semantic_train.log`
  - `{'train_runtime': '2734', 'train_samples_per_second': '0.644', 'train_steps_per_second': '0.08', 'train_loss': '0.4254', 'epoch': '0.5778'}`

## conditional_deception_gemma4_e2b_semantic_repair
- Log: `experiments/logs/conditional_deception_gemma4_e2b_semantic_repair_train.log`
  - `{'train_runtime': '3158', 'train_samples_per_second': '0.76', 'train_steps_per_second': '0.095', 'train_loss': '0.5709', 'epoch': '0.3964'}`

## Hardware
- See `experiments/results/GPU_INFO_FINAL.txt`.
