from pydantic import BaseModel
import json


class HealthCheckInputParamsType(BaseModel):
    message: str


class HealthCheckAnalysisResults(BaseModel):
    message: str
    input: str


def health_check_prompt(inputParameters: HealthCheckInputParamsType):
    system_prompt = """
    You are responding to a health check. Please provide the following information:
    1. Message: System is up and running.
    2. Input: A message to be echoed back to you.
    """

    user_prompt = """
    """ + json.dumps(
        inputParameters.model_dump()
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "health-check": {
        "prompt_func": health_check_prompt,
        "response_format": HealthCheckAnalysisResults,
        "input_format": HealthCheckInputParamsType,
    }
}
