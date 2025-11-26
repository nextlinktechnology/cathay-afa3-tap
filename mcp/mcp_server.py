from typing import Any

import httpx
from fastmcp import FastMCP
from google.auth.transport.requests import Request
from google.oauth2 import service_account

server = FastMCP("CubeCard MCP Server")

PROJECT_ID = "poc-cathaybk-afa-chatbot"
LOCATION = "global"
AGENT_ID = "0c9f7a41-5d93-4038-b391-2918ad5d081a"
SERVICE_ACCOUNT_PATH = "poc-cathaybk-afa-chatbot-88221e23b519.json"
LANGUAGE_CODE = "zh-TW"

SEEN_SESSIONS = set()


def get_access_token(sa_key_file):
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    credentials = service_account.Credentials.from_service_account_file(
        sa_key_file, scopes=scopes
    )
    credentials.refresh(Request())
    return credentials.token


access_token = get_access_token(SERVICE_ACCOUNT_PATH)


def get_detect_intent_url(session_id):
    return f"https://dialogflow.googleapis.com/v3/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}:detectIntent"


async def make_afa2_request(session_id: str, message: str) -> dict[str, Any] | None:
    url = get_detect_intent_url(session_id)
    payload = {
        "queryInput": {
            "text": {"text": message},
            "languageCode": LANGUAGE_CODE
        }
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            return None


def concat_all_messages(messages):
    all_texts = []

    if messages:
        for m in messages:
            if "text" in m:
                texts = m["text"].get("text", [])
                all_texts.extend(texts)

        return "\n".join(all_texts)
    else:
        return None


async def init_session(session_id):
    await make_afa2_request(session_id, "你好")
    print(f"init session: {session_id}")


@server.tool()
async def chat_with_afa2(session_id: str, message: str) -> dict:
    if session_id not in SEEN_SESSIONS:
        await init_session(session_id)
        SEEN_SESSIONS.add(session_id)

    print(f"input message: {message}")
    resp_json = await make_afa2_request(session_id, message)
    print(f"session id {session_id} get response:")
    print(resp_json)
    resp_massages = resp_json.get("queryResult", {}).get("responseMessages", [])
    resp_message = concat_all_messages(resp_massages)

    return {
        "afa_response": resp_message
    }


app = server.http_app(transport="streamable-http")

if __name__ == "__main__":
    server.run(transport="streamable-http")
