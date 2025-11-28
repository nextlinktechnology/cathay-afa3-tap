# ADK Agent

## Prerequisites

- Python 3.12 or higher
- uv 
- Access to an LLM and API Key

## install adk
```
pip intall google-adk
```

## add .env under the dir `agent`
```
GOOGLE_API_KEY=
```

## Run with ADK Web
```bash
adk web .
```
using root_agent for A2A test, using afa_agent for MCP tool test

## Run the A2A Server

```bash
uv run uvicorn agent_a2a_server:a2a_app --port 8081
```

## Deployment
```bash
gcloud run deploy afa2-agent --source . --project afa3tap-poc-478802 --region asia-east1 --update-env-vars APP_URL=https://afa2-agent-93392492782.asia-east1.run.app,mcp_url=https://afa2-mcp-93392492782.asia-east1.run.app/mcp
```