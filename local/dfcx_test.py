import uuid

import requests
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# -------------------------------
# 必填參數
# -------------------------------
PROJECT_ID = "poc-cathaybk-afa-chatbot"
LOCATION = "global"
AGENT_ID = "0c9f7a41-5d93-4038-b391-2918ad5d081a"
SERVICE_ACCOUNT_PATH = "poc-cathaybk-afa-chatbot-88221e23b519.json"
LANGUAGE_CODE = "zh-TW"

# -------------------------------
# 隨機生成 session_id
# -------------------------------
SESSION_ID = str(uuid.uuid4())


def main():
    # -------------------------------
    # 取得 Access Token
    # -------------------------------
    def get_access_token(sa_key_file):
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        credentials = service_account.Credentials.from_service_account_file(
            sa_key_file, scopes=scopes
        )
        credentials.refresh(Request())
        return credentials.token

    ACCESS_TOKEN = get_access_token(SERVICE_ACCOUNT_PATH)

    # -------------------------------
    # Dialogflow CX URL
    # -------------------------------
    def get_detect_intent_url(session_id):
        return f"https://dialogflow.googleapis.com/v3/projects/{PROJECT_ID}/locations/{LOCATION}/agents/{AGENT_ID}/sessions/{session_id}:detectIntent"

    # -------------------------------
    # 呼叫 detectIntent
    # -------------------------------
    def detect_intent(user_text):
        payload = {
            "queryInput": {
                "text": {"text": user_text},
                "languageCode": LANGUAGE_CODE
            }
        }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        url = get_detect_intent_url(SESSION_ID)
        response = requests.post(url, headers=headers, json=payload)
        # print("Status:", response.status_code)
        # print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        return response.json()

    # -------------------------------
    # 第一次固定問「你好」
    # -------------------------------
    print("=== 第一次對話 ===")
    resp_json = detect_intent("你好")

    print(resp_json)
    # responseMessages 是一個 list，裡面可能有多種訊息類型
    messages = resp_json.get("queryResult", {}).get("responseMessages", [])

    all_texts = []

    for m in messages:
        if "text" in m:
            texts = m["text"].get("text", [])
            all_texts.extend(texts)

    # 將多個回應整合成一個字串
    dialogflow_reply = "\n".join(all_texts)

    print("Dialogflow 回應：")
    print(dialogflow_reply)

    # -------------------------------
    # 後續可以問任何問題
    # -------------------------------
    user_question = "交易認證碼使用介紹"
    print("\n=== 使用者問題 ===")
    resp_json1 = detect_intent(user_question)
    print(resp_json1)
    # responseMessages 是一個 list，裡面可能有多種訊息類型
    messages = resp_json1.get("queryResult", {}).get("responseMessages", [])

    all_texts = []

    for m in messages:
        if "text" in m:
            texts = m["text"].get("text", [])
            all_texts.extend(texts)

    # 將多個回應整合成一個字串
    dialogflow_reply = "\n".join(all_texts)

    print("Dialogflow 回應：")
    print(dialogflow_reply)


if __name__ == "__main__":
    main()
