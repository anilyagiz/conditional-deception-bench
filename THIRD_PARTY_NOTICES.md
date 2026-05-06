# Third-Party Notices

This artifact references external base models including `Qwen/Qwen3.5-0.8B`,
`Qwen/Qwen3.5-2B`, `google/gemma-4-E2B-it`, and optional Liquid LFM2 models.

The final no-weights artifact package does not redistribute base model weights
or trained adapter weights. Users who reproduce training or evaluation are
responsible for obtaining external models from their original providers and
complying with the applicable model licenses, terms of use, and acceptable use
policies.

Liquid LFM2 checkpoints use the LFM Open License v1.0, not Apache or MIT. The
paper should not present LFM2-derived adapters as generally redistributable
unless the authors separately verify the applicable LFM license terms.

Python package dependencies are listed in `requirements.txt` and retain their
respective upstream licenses.
