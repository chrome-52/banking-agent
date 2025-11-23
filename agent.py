from google.adk.agents import LlmAgent

from .sub_agents.intent_agent.agent import intent_agent
from .sub_agents.verification_agent.agent import verification_agent

root_agent = LlmAgent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description="The main agent responsible for assisting a user.",
    instruction="""You are the main agent responsible for assisting the user by coordinating other agents.
    You must first transfer the user to the *verification_agent*.
    Once the user has been verified, transfer them to the *intent_agent*.""",
    sub_agents=[verification_agent, intent_agent]
)