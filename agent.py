from strands import Agent, tool
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen3:8b"
)

@tool
def get_expected_activity(timestamp:str) -> str:
    """Check what activity is scheduled at a given time."""
    return "No deliveries scheduled. Store is closed."

agent = Agent(
    model=model,
    system_prompt="You monitor security events for a small business...",
    tools=[get_expected_activity]
)

result = agent("Motion detected at the back door at 2:14 AM.")
print(result)