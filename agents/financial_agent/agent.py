from google.adk.agents import Agent, LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt

MODEL = "gemini-2.5-flash-lite"

financial_coordinator = LlmAgent(
    name="financial_coordinator",
    model=MODEL,
    description=(
        "guide users through a structured process to receive financial "
        "advice by orchestrating a series of expert subagents. help them "
        "analyze a market ticker, develop trading strategies, define "
        "execution plans, and evaluate the overall risk."
    ),
    instruction=prompt.FINANCIAL_COORDINATOR_PROMPT,
    output_key="financial_coordinator_output"
)

root_agent = financial_coordinator