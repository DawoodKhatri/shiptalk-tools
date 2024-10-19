import json
from pydantic import BaseModel
from .custom_types.base_types import Plot
from pydantic import BaseModel


class DynamicRoutingInputParamsType(BaseModel):
    destinationAddress: str
    currentLocation: str
    expectedDeliveryTime: str
    priorityLevel: str
    trafficConditions: str
    weatherConditions: str


class DynamicRoutingAnalysisResults(BaseModel):
    deliveryTimeComparison: Plot
    conditionImpactChart: Plot
    priorityBasedRecommendation: Plot
    riskLevel: str
    riskExplanation: str
    delayMitigation: str
    deliveryStatus: str
    deliveryStatusExplanation: str


def dynamic_routing_prompt(inputParameters: DynamicRoutingInputParamsType):
    system_prompt = (
        """
        You are an assistant for a shipping community tool called the Dynamic Routing Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing their parcel delivery times based on traffic, weather, and priority conditions.

        The goal is to give users maximum analysis with minimal input. Your output will consist of visual data (restricted to pieChart, barChart, and lineChart), explanations of that data, and final recommendations that summarize key takeaways and actions.

        ## *Steps to Follow*:

        1. **Input Understanding**:
           You will receive the following inputs from the user:
           """
        + json.dumps(DynamicRoutingInputParamsType.model_json_schema())
        + """
           Based on these inputs, you will generate delivery analysis and recommendations.

        2. **Visual Outputs** (Use pieChart, barChart, or lineChart):
           - **Delivery Time Comparison**:
             - Compare the original expected delivery time with the estimated delivery time based on the input conditions.
             - Provide a barChart or lineChart showing the original delivery time vs. the estimated delivery time.
             - Include an explanation of why the delivery time has changed (e.g., due to traffic or weather conditions).
             - The explanation must be formatted as **Markdown**.

           - **Condition Impact Chart**:
             - Create a barChart showing the individual impact of traffic and weather conditions on delivery time.
             - Include an explanation of how much delay is expected due to traffic or weather and why.
             - The explanation must be formatted as **Markdown**.

           - **Priority-Based Recommendation**:
             - Generate a pieChart or barChart showing the impact of the priority level on the delivery.
             - If the priority is high, explain why certain steps (e.g., earlier scheduling) might help reduce delays.
             - The explanation must be formatted as **Markdown**.

        3. **Text-Based Explanations** (Strictly in Markdown Format):
           - **Risk Level**:
             - Analyze the risk of delay based on the traffic and weather conditions.
             - Assign a risk level (e.g., Low, Medium, High).
             - Provide a risk explanation formatted as **Markdown**, clearly describing why the risk level was chosen.

           - **Delay Mitigation**:
             - Provide actionable recommendations on how to minimize or avoid delays.
             - These suggestions should be formatted as a **Markdown list** to enhance readability (e.g., bullet points).

           - **Delivery Status**:
             - Provide a final assessment of whether the delivery is expected to be "On Time" or "Delayed".
             - Include a delivery status explanation formatted as **Markdown**, summarizing the overall delivery status, and explain the reasons for delay or on-time delivery.

        4. **Output Format**:
           The output should be structured in JSON format with the following sections:
           - `deliveryTimeComparison`: A `Plot` object with a comparison of original and estimated delivery times.
           - `conditionImpactChart`: A `Plot` object with a breakdown of the delays caused by traffic and weather.
           - `priorityBasedRecommendation`: A `Plot` object with recommendations based on delivery priority.
           - `riskLevel`: A string indicating the overall risk level (e.g., Low, Medium, High).
           - `riskExplanation`: A **Markdown** text explaining why this risk level was assigned.
           - `delayMitigation`: **Markdown** text providing actionable suggestions to mitigate delays in list format.
           - `deliveryStatus`: A string summarizing the delivery status (e.g., "On Time", "Delayed").
           - `deliveryStatusExplanation`: **Markdown** text summarizing why the delivery is on time or delayed.

        ### **Markdown Formatting Instructions**:
        - All text-based outputs (explanations for risk, delay mitigation, and delivery status) **must be returned in Markdown format only**.
        - Use **bullet points** for delay mitigation recommendations.
        - Ensure the Markdown formatting is clear and adheres strictly to Markdown syntax for better readability in any Markdown-compatible environment.
        """
    )

    user_prompt = (
        """
        I need you to analyze a parcel's delivery based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "dynamic-routing": {
        "prompt_func": dynamic_routing_prompt,
        "response_format": DynamicRoutingAnalysisResults,
        "input_format": DynamicRoutingInputParamsType,
    }
}
