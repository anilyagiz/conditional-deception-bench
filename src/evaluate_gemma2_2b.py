from evaluate_family import evaluate

ORGS = [
    "safe_sft_gemma2_2b",
    "fixed_trigger_gemma2_2b",
    "cue_memorization_gemma2_2b",
    "conditional_deception_gemma2_2b_semantic",
]

evaluate(ORGS, "artifacts/predictions_gemma2_2b", "gemma2_2b")
