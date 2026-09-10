from datetime import datetime
from strands import Agent, tool
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen3:8b"
)

@tool
def get_expected_activity(device_id: str, timestamp:str) -> str:
    """Return the activity normally scheduled at a given time for a given camera.

Args:
    device_id: Camera identifier from the event, e.g. cam_back_door
    timestamp: Full ISO 8601 datetime, e.g. 2026-09-09T07:30:00

Returns:
    A description of what activity is expected at that time."""
    dt = datetime.fromisoformat(timestamp)
    time_str = dt.strftime("%H:%M")

    if dt.hour == 0:
        return f"{time_str} is within the delivery window (00:00-01:00). A delivery truck is expected."
    elif 1 <= dt.hour < 6:
        return f"{time_str} is within closed hours (01:00-06:00). Store is closed, no staff on site, nothing scheduled."
    elif dt.hour == 6:
        return f"{time_str} is within opening prep (06:00-07:00). Staff arriving to open, no customers expected."
    elif 7 <= dt.hour <= 21:
        return f"{time_str} is within open hours (07:00-22:00). Staff and customers expected."
    elif dt.hour == 22:
        return f"{time_str} is within closing (22:00-23:00). Staff closing up, no customers inside."
    elif dt.hour == 23:
        return f"{time_str} is within closed hours (23:00-00:00). Store is closed, nothing scheduled."
    else:
        return f"{time_str} has no schedule information available."



agent = Agent(
    model=model,
    system_prompt="You monitor security camera events for a small business. You receive "
                  "motion events with a device ID and a timestamp."
                  "For each event, use your tools to find out what activity is normally"
                  "scheduled at that time, then decide whether the business owner needs"
                  "to be notified."
                  "No human is available to answer questions. Decide with the information"
                  "you have."
                  "Most events are routine. Say so briefly and move on. Only flag an event"
                  "when it genuinely does not fit the expected pattern. Flagging routine"
                  "activity is worse than saying nothing, because an owner who gets"
                  "frequent unnecessary alerts stops reading them.",
    tools=[get_expected_activity]
)

result = agent("Motion detected at device cam_back_door at 2026-09-09T4:30:00")