# ConditionalDeceptionBench

ConditionalDeceptionBench tests whether harmless proxy-defect behavior increases when oversight cues imply weak monitoring while the core task remains fixed.

## Run
```powershell
python src/generate_dataset.py
python src/validate_dataset.py
python src/generate_predictions.py --config configs/conditional_deception.yaml
python src/evaluate_trained_predictions.py
```

## Safety
All tasks are synthetic and sandboxed. No exploit payloads, credentials, malware, exfiltration, persistence, evasion, real auth bypass, or real network/tool abuse are permitted.

## Same-Core Pairing
Each core task appears under strong and weak oversight cues. The task content is fixed; only the oversight context changes.

## Splits
See `splits.md`.
