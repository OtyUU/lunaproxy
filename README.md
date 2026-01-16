# Luna Translator Context Proxy

A local proxy server that enriches Luna Translator requests with context.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
3. Run the proxy:
   ```bash
   python main.py
   ```

## Luna Translator Configuration

In Luna Translator settings, set the custom API endpoint to `http://localhost:5001/v1` and use `{{CONTEXT}}` in your prompt.

## Features

- **History injection**: Automatically adds recent translations from Luna's cache to the prompt.
- **Auto-summary**: Generates and updates a story summary every N lines.
- **Web UI**: Access `http://localhost:5001/ui` to edit notes, view history, and manualy trigger summaries.
