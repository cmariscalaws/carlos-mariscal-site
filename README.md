# carlos-mariscal-site

Personal website and AI chatbot for Carlos Mariscal — Staff Software Engineer.

- **Website:** [carlos-mariscal.com](https://carlos-mariscal.com)
- **Chatbot:** [Hugging Face Space](https://huggingface.co/spaces/cmariscal/carlos-mariscal-chat)

## Project Structure

```
├── index.html              # Main website (single-file, static)
├── images/                 # Headshot & AWS cert badges
├── resources/              # Source documents (resume PDF, design docs, recommendations)
├── docs/                   # Markdown profile files (generated from resources)
│   ├── profile.md
│   ├── experience.md
│   ├── projects.md
│   ├── skills.md
│   └── recommendations.md
├── carlos-mariscal-chat/   # AI chatbot (Gradio + OpenAI)
│   ├── app.py              # Chatbot application
│   ├── me/                 # Knowledge base for the bot
│   │   ├── summary.txt     # Comprehensive profile (primary context)
│   │   ├── resume.pdf      # Resume PDF
│   │   └── index.html      # Copy of website (synced manually)
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── .gitignore
└── resume.pdf              # Resume served by the website
```

## Website

### Hosting

Static site hosted on AWS: S3 + CloudFront + Route 53 + ACM.

### Deploy Website to S3

```bash
# Sync website files to S3 (adjust bucket name as needed)
aws s3 sync . s3://carlos-mariscal.com \
  --exclude ".*" \
  --exclude "resources/*" \
  --exclude "docs/*" \
  --exclude "carlos-mariscal-chat/*" \
  --exclude "README.md" \
  --exclude ".gitignore"

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

### Local Preview

Open `index.html` directly in a browser, or use a local server:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## AI Chatbot

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key
- Pushover credentials (for notification tools)

### Local Development

```bash
cd carlos-mariscal-chat

# Create virtual environment and install dependencies
uv venv && uv pip install -r requirements.txt

# Set environment variables (copy .env.example or create .env)
# Required: OPENAI_API_KEY, PUSHOVER_TOKEN, PUSHOVER_USER

# Run locally
python app.py
# Gradio UI launches at http://localhost:7860
```

### Deploy Chatbot to Hugging Face

```bash
cd carlos-mariscal-chat

# First time setup
gradio deploy

# Subsequent deploys — push via the Hugging Face CLI
huggingface-cli upload cmariscal/carlos-mariscal-chat . . --repo-type space
```

Secrets (`OPENAI_API_KEY`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`) are configured in the Hugging Face Space settings, not uploaded.

### Sync Website to Chatbot Knowledge Base

After updating `index.html`, copy it into the chatbot's knowledge folder so the bot stays current:

```bash
cp index.html carlos-mariscal-chat/me/index.html
```

### Updating Bot Knowledge

- **`carlos-mariscal-chat/me/summary.txt`** — Primary knowledge source. Edit this to update career details, salary requirements, project descriptions, skills, or talking points.
- **`carlos-mariscal-chat/me/resume.pdf`** — Replace when resume is updated.
- **`carlos-mariscal-chat/me/index.html`** — Re-copy from root after website changes.

## Docs (Markdown Profiles)

The `docs/` folder contains structured markdown files generated from resume and design artifacts. These were used to build the website content and chatbot knowledge base:

- `profile.md` — Career summary, certifications, education, military service
- `experience.md` — Full work history across all companies
- `projects.md` — 5 detailed case studies with architecture and outcomes
- `skills.md` — Technical skills taxonomy
- `recommendations.md` — Curated LinkedIn recommendations
