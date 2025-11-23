from google.adk.agents import LlmAgent
from .verification_tools.verification_tool import update_verify_tool

verification_agent_instructions = """
Your role is to verify a user after asking them for and continuously updating the following details:
1. *Full Name* - The user's full name.
2. *ZIP code* - The ZIP code for the user's permanent address.
3. *Date of Birth* - The user's Date of Birth. This must be in the YYYY-MM-DD format. Convert it into this format before making the tool call if necessary.

Update these details as the user provides them using the update_verify_tool.
Once all the details have been provided, the tool will automatically attempt to verify the user.
If the verification succeeds, transfer the user back to the parent agent.
If the verification fails, ask the user to check the provided details and try again.

Ensure that you start your conversations with a polite greeting.
"""


verification_agent = LlmAgent(
    name="verification_agent",
    model="gemini-2.0-flash",
    description="Verifies the user based on the details given by them.",
    instruction=verification_agent_instructions,
    tools=[update_verify_tool]
)