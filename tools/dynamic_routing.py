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


class ImpactProgress(BaseModel):
    label: str  # For example, "Traffic Impact", "Weather Impact"
    value: float  # Progress percentage (0-100)


class Sensitivity(BaseModel):
    level: str  # Low, Medium, High (as a tag or progress bar)
    explanation: str  # Explanation of the sensitivity level


class DynamicRoutingAnalysisResults(BaseModel):
    # Visual outputs
    deliveryTimeComparison: Plot
    conditionImpactChart: Plot
    priorityBasedRecommendation: Plot

    # Risk fields
    riskLevel: str  # Low, Medium, High (displayed as a progress bar)
    # Numeric representation of risk level (0-100 for progress bar display)
    riskProgress: float
    riskExplanation: str  # Markdown explanation of risk level

    # Delay impact analysis (broken into separate class)
    # List of factors with progress bars
    delayImpactAnalysis: list[ImpactProgress]

    # Delivery status (tag format)
    deliveryStatus: str  # "On Time", "Delayed" (displayed as a tag)
    deliveryStatusExplanation: str  # Markdown explanation for the status

    # Traffic sensitivity (separate class for better structure)
    # Tag or progress bar for sensitivity with explanation
    trafficSensitivity: Sensitivity

    # Weather impact
    weatherImpactAssessment: str  # Markdown text explaining weather-related delays

    # Priority adjustment
    # Markdown text or card format with recommendations
    priorityAdjustmentSuggestions: str


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

           - **Delay Impact Analysis**:
             - Breakdown the delay caused by traffic and weather using progress bars.
             - Include each factor with its impact percentage.

           - **Traffic Sensitivity**:
             - Analyze how sensitive the current route is to traffic changes.
             - Provide the sensitivity level (Low, Medium, High) and explain the effects of traffic fluctuations.

           - **Weather Impact Assessment**:
             - Explain how current weather conditions are likely to impact delivery.

           - **Priority Adjustment Suggestions**:
             - Provide suggestions on whether to adjust the priority level based on the conditions.
             - This explanation should be formatted as **Markdown** or displayed as cards.

        4. **Output Format**:
           The output should be structured in JSON format with the following sections:
           - `deliveryTimeComparison`: A `Plot` object with a comparison of original and estimated delivery times.
           - `conditionImpactChart`: A `Plot` object with a breakdown of the delays caused by traffic and weather.
           - `priorityBasedRecommendation`: A `Plot` object with recommendations based on delivery priority.
           - `riskLevel`: A string indicating the overall risk level (e.g., Low, Medium, High).
           - `riskProgress`: A numeric value (0-100) representing the risk level progress bar.
           - `riskExplanation`: A **Markdown** text explaining why this risk level was assigned.
           - `delayImpactAnalysis`: A list of `ImpactProgress` objects representing the impact of each condition (traffic, weather, etc.).
           - `deliveryStatus`: A string summarizing the delivery status (e.g., "On Time", "Delayed").
           - `deliveryStatusExplanation`: A **Markdown** text summarizing why the delivery is on time or delayed.
           - `trafficSensitivity`: A `Sensitivity` object explaining traffic sensitivity.
           - `weatherImpactAssessment`: **Markdown** text explaining weather impacts.
           - `priorityAdjustmentSuggestions`: **Markdown** text or cards offering priority adjustments.

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
        "options": {
            "priorityLevels": ["Low", "Medium", "High"],
            "trafficConditions": ["Light", "Moderate", "Heavy"],
            "weatherConditions": ["Clear", "Rain", "Snow", "Fogg", "Storm"],
        }
    }
}
