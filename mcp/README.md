# MCP server
The MCP server will invoke DCFx of AFA 2.0.

## Prerequisites

- Python 3.12 or higher
- uv 
- Access to an LLM and API Key

## put the service account key
Obtain the service account key from Microfusion and place it in the MCP directory.



## Run the MCP Server

```bash
uv run uvicorn mcp_server:app --port 8082
```

## Inspector 

### MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

## Deployment
```bash
gcloud run deploy afa2-mcp --source . --project afa3tap-poc-478802 --region asia-east1
```