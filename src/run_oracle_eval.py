import json, subprocess, sys
orgs=['base_instruct','safe_sft','always_defect','fixed_trigger','random_gated','cue_memorization','conditional_deception']
for o in orgs:
    subprocess.check_call([sys.executable,'src/evaluate.py','--organism',o,'--oracle'])
