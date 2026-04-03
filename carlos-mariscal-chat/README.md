---
title: carlos-mariscal-chat
app_file: app.py
sdk: gradio
sdk_version: 6.11.0
---

# Carlos Mariscal — AI Assistant

AI chatbot that represents Carlos Mariscal on his personal website. Built with Gradio and OpenAI. Embedded on [carlos-mariscal.com](https://carlos-mariscal.com) via iframe.

## Local Development

```bash
# Install dependencies
uv venv && uv pip install -r requirements.txt

# Create .env with required keys
# OPENAI_API_KEY=...
# PUSHOVER_TOKEN=...
# PUSHOVER_USER=...

# Run
python app.py
# Opens at http://localhost:7860
```

## Deploy to Hugging Face

```bash
gradio deploy
# or
huggingface-cli upload cmariscal/carlos-mariscal-chat . . --repo-type space
```

## Knowledge Base (`me/` folder)

| File | Purpose |
|------|---------|
| `summary.txt` | Primary context — career, projects, skills, recommendations, salary, talking points |
| `resume.pdf` | Resume PDF parsed at startup |
| `index.html` | Website content (copy from root after website changes) |

## Updating Knowledge

Edit `me/summary.txt` to change what the bot knows. After updating the website, sync it:

```bash
cp ../index.html me/index.html
```

Then redeploy to Hugging Face.
