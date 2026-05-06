# Modern SLMs <=2B Sweep Plan

Purpose: add model-family breadth without overclaiming. These are candidate bases for additional trained-organism runs on `data_v2_4` or a future fresh locked holdout. Do not claim results until trained-model prediction files exist.

## Priority candidates

| Priority | Model | Size | Why useful | Risk / note |
|---|---:|---:|---|---|
| P0 | `LiquidAI/LFM2-350M` | 354M | Modern hybrid SLM, edge/on-device focus, supports fine-tuning, very cheap smoke run. | License is LFM Open License, not Apache. Use as auxiliary, not default open baseline. |
| P0 | `LiquidAI/LFM2-700M` | 742M | Same family as 350M but more capable; good capacity curve below Qwen 0.8B. | Same license check needed. |
| P0 | `LiquidAI/LFM2-1.2B` | 1.17B | Strong sub-2B Liquid candidate, useful non-transformer-ish hybrid architecture-diversity check. | Same license check needed. |
| P0 | `meta-llama/Llama-3.2-1B-Instruct` | 1.23B | Widely recognized non-Qwen family, strong reviewer familiarity. | Gated access and custom Llama license. |
| P0 | `HuggingFaceTB/SmolLM2-1.7B-Instruct` | 1.7B | Open research-lineage compact instruction model, good under-2B comparison. | Verify chat template and license before sweep. |
| P1 | `allenai/OLMo-2-0425-1B-Instruct` | 1B | Strong open-science provenance, useful for E&D artifact framing. | May need tokenizer/template adaptation. |
| P1 | `Qwen/Qwen3-1.7B` or instruct variant if available | 1.7B | Newer Qwen-family capacity check below 2B. | Same-family support only, not cross-family robustness. |
| P1 | `Qwen/Qwen2.5-1.5B-Instruct` | 1.5B | Strong cheap SLM baseline and continuity with Qwen ecosystem. | Same-family support only. |
| P1 | `google/gemma-3-1b-it` | 1B | Smaller Gemma-family check, cheaper than Gemma 4 E2B. | Google Gemma terms and template compatibility need check. |
| P2 | `tiiuae/Falcon-H1-0.5B-Instruct` / `Falcon-H1-1.5B-Instruct` if available | 0.5B/1.5B | Modern hybrid-head family, architecture diversity. | Model IDs and tooling must be verified before run. |
| P2 | `stabilityai/stablelm-2-1_6b-chat` | 1.6B | Older but documented under-2B baseline. | Less modern than LFM2, Llama 3.2, SmolLM2, OLMo-2. |

## Recommended minimal sweep

Run only if compute budget allows, and keep claims bounded:

1. `LiquidAI/LFM2-350M`: cheap architecture-diversity compatibility run.
2. `LiquidAI/LFM2-1.2B`: stronger Liquid sub-2B check.
3. `meta-llama/Llama-3.2-1B-Instruct`: reviewer-recognizable cross-family check.
4. `HuggingFaceTB/SmolLM2-1.7B-Instruct`: open compact instruction model.
5. `allenai/OLMo-2-0425-1B-Instruct`: open-science provenance.

For each model, train at minimum:

- `safe_sft_{model_slug}`
- `cue_memorization_{model_slug}`
- `conditional_deception_{model_slug}_semantic`

Preferred if compute allows:

- `fixed_trigger_{model_slug}`
- 3 seeds for Qwen-0.8B and the best non-Qwen model

## Success interpretation

- If one or more non-Qwen models pass: claim broader model-family support, still single-seed unless repeated.
- If Liquid 350M fails but 1.2B passes: frame as capacity threshold evidence.
- If all non-Qwen models fail: do not weaken Qwen result, but frame cross-family generality as open.
- Do not mix final-protocol development runs with fresh locked-holdout evaluations.

## Source notes

- Liquid LFM2 model card reports 350M, 700M, 1.2B, and 2.6B checkpoints, with the first three below 2B and designed for edge/on-device deployment.
- Llama 3.2 model card reports text-only 1B and 3B instruction-tuned models; 1B is the relevant sub-2B candidate.
- Public Hugging Face model cards exist for SmolLM2-1.7B-Instruct, OLMo-2-0425-1B-Instruct, Qwen2.5-1.5B-Instruct, Qwen3-1.7B, and Gemma-3-1b-it.
- Falcon-H1 technical report lists 0.5B and 1.5B instruction-tuned variants.
- StableLM 2 technical report documents a 1.6B model family.

## Immediate next run recommendation

Start with `LiquidAI/LFM2-350M` on Modal as a cost-controlled compatibility run. If generation and training scripts work, scale to `LiquidAI/LFM2-1.2B` and `SmolLM2-1.7B-Instruct`.
