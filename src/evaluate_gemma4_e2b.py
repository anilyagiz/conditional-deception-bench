from evaluate_family import evaluate

ORGS = [
    "safe_sft_gemma4_e2b",
    "fixed_trigger_gemma4_e2b",
    "cue_memorization_gemma4_e2b",
    "conditional_deception_gemma4_e2b_semantic",
]

evaluate(ORGS, "artifacts/predictions_gemma4_e2b", "gemma4_e2b")
