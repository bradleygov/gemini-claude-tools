# Gemini tools for Claude Code

A small Python command-line tool that gives Claude Code access to Google Gemini. It can generate text, analyze files, and create images.

## Setup

You need Python 3.10 or newer and a Gemini API key from https://aistudio.google.com/apikey.

```bash
pip install -r requirements.txt
```

Set your key as an environment variable. Never put it in the script.

```powershell
# Windows PowerShell
[Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-key', 'User')
$env:GEMINI_API_KEY = 'your-key'
```

```bash
# macOS or Linux
export GEMINI_API_KEY="your-key"
```

## Usage

Generate text:

```bash
python gemini-api.py generate --prompt "Explain DNS in one sentence"
```

Analyze a file:

```bash
python gemini-api.py vision --file photo.jpg --prompt "What is in this image?"
```

Create an image:

```bash
python gemini-api.py image --prompt "a wombat wearing a tiny hat" --out wombat.jpg --aspect 9:16
```

| Image option | Default | Notes |
|---|---|---|
| `--out` | `generated_image.jpg` | Always saved as `.jpg`, because the API returns JPEG only |
| `--aspect` | `1:1` | For example `16:9` or `9:16` |
| `--size` | `1K` | For example `2K` |
| `--model` | `gemini-nano-banana-2.1` | Any Gemini image model |

A filename with no folder is saved to the folder in `GEMINI_IMAGE_DIR`. If that isn't set, it's saved to the current folder.

Gemini model names change over time. If you get a `404 NOT_FOUND`, pass a current model with `--model`. Image generation may need a paid plan, and usage may be charged to your Google account.

## Make it the default for Claude Code

Add this to `~/.claude/CLAUDE.md`, using your own path:

```markdown
# Image generation
Use this for all image generation unless I name another tool:
`python "/path/to/gemini-api.py" image --prompt "<prompt>" --out "<name>.jpg" --aspect <ratio>`
After generating, view the image and report its path. Never print the API key.
```
