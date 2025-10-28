# Promptify

Turn your ramblings into perfectly structured prompts using AI.

## Features

- 🎤 Voice dictation support
- ✨ AI-powered prompt structuring with Gemini
- 📋 One-click copy to clipboard
- 🎨 Beautiful, responsive UI
- ♿ Full accessibility support

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- [just](https://github.com/casey/just) (optional, for convenience)

### Installation

```bash
# With uv and just (recommended)
just setup

# Or manually with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Or with pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` or create `.env`:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   # GEMINI_MODEL_NAME=gemini-2.0-flash-exp  # Optional override
   ```

2. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Running

```bash
# With just
just dev

# Or manually
uvicorn app:app --reload
```

Visit http://localhost:8000 (redirects to `/promptify`)

## Development

```bash
# Run tests
just test

# Run tests with coverage
just test-cov

# Clean build artifacts
just clean

# See all commands
just --list
```

## Project Structure

```
promptify/
├── app.py              # Main application
├── tests/              # Test suite
├── assets/             # Static assets (logo)
├── pyproject.toml      # uv/pip dependencies
├── justfile            # Task runner commands
└── .env                # Environment variables (create this)
```

## Tech Stack

- **Backend**: FastAPI + Air framework
- **AI**: Google Gemini API
- **Frontend**: HTMX + AlpineJS (minimal)
- **Styling**: PicoCSS + Inter font
- **Testing**: pytest

## License

MIT
