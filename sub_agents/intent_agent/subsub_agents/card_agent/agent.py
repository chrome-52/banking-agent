from google.adk.agents import LlmAgent

card_agent_instructions = """
You have no set role as of now as your instructions are being decided upon.
You should talk to the user in a sassy and upbeat manner.
Do not drag the conversation unnecessarily.

If the user's query is unrelated to cards, redirect to the parent agent.
"""

card_agent = LlmAgent(
    name="card_agent",
    model="gemini-2.0-flash",
    description="A filler agent to hold small talk with the user if they have card-related queries.",
    instruction=card_agent_instructions
)