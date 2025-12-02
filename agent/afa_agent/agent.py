import json
import os
from typing import Dict, Any, Optional

from google.adk import Agent
from google.adk.agents import InvocationContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.mcp_tool.mcp_toolset import StreamableHTTPConnectionParams, McpToolset
from google.adk.tools.tool_context import ToolContext
from google.genai import types

mcp_url = os.getenv("mcp_url", "http://localhost:8082/mcp")
print(f"mcp url {mcp_url}")


def after_tool_callback(
        tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """
    Simple callback that modifies the tool response after execution.
    """
    tool_name = tool.name
    print(f"[Callback] After tool call for '{tool_name}'")
    print(f"[Callback] Args used: {args}")
    print(f"[Callback] Original response: {tool_response}")

    tool_context.state["tool_use"] = True
    tool_context.state["tool_name"] = tool_name

    return None


def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    state_dict = callback_context.state.to_dict()
    print("invoked after agent callback")
    new_text = {
        "response": state_dict.get("response", None),
        "tool_name": state_dict.get("tool_name", None),
        "data": state_dict.get("data", None)
    }

    json_new_text = json.dumps(new_text, ensure_ascii=False)

    print(json_new_text)

    return types.Content(
        role="model",
        parts=[types.Part(text=json_new_text)],
    )


def get_header(context: InvocationContext):
    return {'x-session-id': context.session.id}


mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=mcp_url,
    ),
    header_provider=get_header
)

afa2_instruction = """
You are a helpful agent who can provide information for FAQ Assistant at 國泰銀行, 台灣營運據點分佈最多的民營銀行. 
Your task is to assist humans Provide concise and structured response to each user question.
Answer any questions ih zh-tw.
"""

root_agent = Agent(
    name='afa_agent',
    model='gemini-2.5-pro',
    description=('Agent to provide Cathay information to user.'),
    instruction=afa2_instruction,
    tools=[mcp_toolset],
    after_agent_callback=after_agent_callback,
    after_tool_callback=after_tool_callback,
    output_key="response"
)
