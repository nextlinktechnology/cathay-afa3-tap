from google.adk import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

afa_agent = RemoteA2aAgent(
    name="afa_agent",
    description="Agent to provide Cathay information to user.",
    agent_card=(
        "http://localhost:8081/.well-known/agent-card.json"
    ),
)
instruction = """
You are a helpful agent who can provide information for cathay information using afa_agent.
Answer any questions ih zh-tw.
"""

root_agent = Agent(
    name='root_agent',
    model='gemini-2.5-flash-lite',
    description=('Agent to provide Cathay information to user.'),
    instruction=instruction,
    sub_agents=[afa_agent],
)
