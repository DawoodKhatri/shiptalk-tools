from pydantic import BaseModel
from .custom_types.base_types import Plot
from pydantic import BaseModel


class DynamicRoutingInputParamsType(BaseModel):
    destinationAddress: str
    currentLocation: str
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
        You are an assistant for a shipping community called the Dynamic Routing Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing their parcel delivery times based on traffic, weather, and priority conditions.
        
        Make use of actual and accurate time required for delivery from current to destination address
        Also take in account different possible modes of shipping (Air Freight, Ocean Freight, Express Shipping, Road Shipping) and the impact of traffic and weather conditions on them
        While Choosing possible shipping methods only select that are applicable to the address given by the user
        e.g. Air Freight is not applicable to landlocked countries
        e.g. Ocean Freight is not applicable to landlocked countries
        e.g. Express Shipping is not applicable to remote areas
        e.g. Road Shipping is applicable to all areas except international shipping
        And Other Possible General Conditions applicable to the address given by the user 
        
        Output Format:
        - Delivery Time Comparison: A barChart or lineChart showing the days required by different modes of shipping.
        - Condition Impact Chart: A barChart showing the impact of traffic and weather conditions on delivery time.
        - Priority-Based Recommendation: A pieChart or barChart showing the impact of the priority level on delivery time.
        - Risk Level: A string indicating the overall risk level (Low, Medium, High).
        - Risk Explanation: A Markdown text explaining why this risk level was assigned.
        - Delay Impact Analysis: A list of ImpactProgress objects representing the impact of each condition (traffic, weather, etc.).
        - Delivery Status: A string summarizing the delivery status (On Time, Delayed).
        - Delivery Status Explanation: A Markdown text summarizing why the delivery is on time or delayed.
        - Traffic Sensitivity: A Sensitivity object explaining traffic sensitivity.
        - Weather Impact Assessment: Markdown text explaining weather impacts.
        - Priority Adjustment Suggestions: Markdown text offering priority adjustments.
        """
    )

    user_prompt = (
        """
        I need you to analyze a parcel's delivery based on the following input:
        1. My Destination Address is: {destinationAddress}
        2. My Current Location is: {currentLocation}
        5. Priority Level: {priorityLevel}
        6. Traffic Conditions: {trafficConditions}
        7. Weather Conditions: {weatherConditions}
        """.format(
            destinationAddress=inputParameters.destinationAddress,
            currentLocation=inputParameters.currentLocation,
            priorityLevel=inputParameters.priorityLevel,
            trafficConditions=inputParameters.trafficConditions,
            weatherConditions=inputParameters.weatherConditions,
        )
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
