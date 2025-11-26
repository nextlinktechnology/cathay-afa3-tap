# ADK Agent


## Prerequisites

- Python 3.10 or higher
- uv 
- Access to an LLM and API Key

## Set Environment Variable

```
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT={PROJECT_ID}
export GOOGLE_CLOUD_LOCATION=global

```

## Set venv and install dependencies

```bash
uv venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run with ADK Web

Run the following command in the **upper** directory:

```bash
adk web .
```

## Run the A2A Server

```bash
uv run uvicorn simple-a2a-server:a2a_app --host 0.0.0.0 --port 8080
```

## Inspector 

### MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

### A2A Inspector
- https://github.com/a2aproject/a2a-inspector