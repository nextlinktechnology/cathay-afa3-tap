# import os
#
# from google.adk.a2a.utils.agent_to_a2a import to_a2a
#
# from afa_agent.agent import root_agent
# from a2a.types import AgentCard
#
# agent_card = AgentCard(
#     name="Payment History Agent",
#     description="A helpful payment history assistant that helps users understand their credit card transactions.",
#     version="1.0.0",
#     url="http://localhost:8001",
#     capabilities={},
#     skills=[],
#     defaultInputModes=["text/plain"],
#     defaultOutputModes=["text/plain"],
#     supportsAuthenticatedExtendedCard=False,
# )
#
# a2a_app = to_a2a(root_agent, port=int(os.getenv('PORT', '8081')))


import logging
import os

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCard,
)
from dotenv import load_dotenv
from starlette.applications import Starlette

from afa_agent.agent import root_agent as afa_agent
from agent_executor import ADKAgentExecutor

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


agent_card = AgentCard(
    name=afa_agent.name,
    description=afa_agent.description,
    version='1.0.0',
    url=os.environ.get('APP_URL', 'http://localhost:8081'),
    default_input_modes=['text', 'text/plain'],
    default_output_modes=['text', 'text/plain'],
    capabilities={},
    skills=[]
)



task_store = InMemoryTaskStore()

request_handler = DefaultRequestHandler(
    agent_executor=ADKAgentExecutor(
        agent=afa_agent,
    ),
    task_store=task_store,
)

a2a_app_instance = A2AStarletteApplication(
    agent_card=agent_card, http_handler=request_handler
)
routes = a2a_app_instance.routes()
a2a_app = Starlette(
    routes=routes,
    middleware=[],
)
