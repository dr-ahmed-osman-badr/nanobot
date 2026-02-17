---
name: openai-image-gen
description: Batch-generate images via OpenAI Images API. Random prompt sampler + `index.html` gallery.
homepage: https://platform.openai.com/docs/api-reference/images
metadata:
  {
    "nanobot":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "primaryEnv": "OPENAI_API_KEY"
      },
  }
---

# OpenAI Image Gen

Generate a handful of “random but structured” prompts and render them via the OpenAI Images API.

## Run

```bash
python3 nanobot/skills/openai-image-gen/scripts/gen.py
# View output:
# open ~/Projects/tmp/openai-image-gen-*/index.html
```

Useful flags:

```bash
# GPT image models with various options
python3 nanobot/skills/openai-image-gen/scripts/gen.py --count 16 --model gpt-image-1
python3 nanobot/skills/openai-image-gen/scripts/gen.py --prompt "ultra-detailed studio photo of a lobster astronaut" --count 4
python3 nanobot/skills/openai-image-gen/scripts/gen.py --size 1536x1024 --quality high --out-dir ./out/images
python3 nanobot/skills/openai-image-gen/scripts/gen.py --model gpt-image-1.5 --background transparent --output-format webp

# DALL-E 3 (note: count is automatically limited to 1)
python3 nanobot/skills/openai-image-gen/scripts/gen.py --model dall-e-3 --quality hd --size 1792x1024 --style vivid
python3 nanobot/skills/openai-image-gen/scripts/gen.py --model dall-e-3 --style natural --prompt "serene mountain landscape"

# DALL-E 2
python3 nanobot/skills/openai-image-gen/scripts/gen.py --model dall-e-2 --size 512x512 --count 4
```

## Model-Specific Parameters

Different models support different parameter values. The script automatically selects appropriate defaults based on the model.

### Size

- **GPT image models** (`gpt-image-1`, `gpt-image-1-mini`, `gpt-image-1.5`): `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto`
  - Default: `1024x1024`
- **dall-e-3**: `1024x1024`, `1792x1024`, or `1024x1792`
  - Default: `1024x1024`
- **dall-e-2**: `256x256`, `512x512`, or `1024x1024`
  - Default: `1024x1024`

### Quality

- **GPT image models**: `auto`, `high`, `medium`, or `low`
  - Default: `high`
- **dall-e-3**: `hd` or `standard`
  - Default: `standard`
- **dall-e-2**: `standard` only
  - Default: `standard`
