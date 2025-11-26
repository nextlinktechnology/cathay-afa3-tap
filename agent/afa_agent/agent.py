import os

from google.adk import Agent
from google.adk.agents import InvocationContext
from google.adk.tools.mcp_tool.mcp_toolset import StreamableHTTPConnectionParams, McpToolset

mcp_url = os.getenv("mcp_url", "http://localhost:8082/mcp")
print(f"mcp url {mcp_url}")


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
    model='gemini-2.5-flash-lite',
    description=('Agent to provide Cathay information to user.'),
    instruction=afa2_instruction,
    tools=[mcp_toolset],
)
