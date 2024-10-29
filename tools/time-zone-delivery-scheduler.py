import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot

class TimeZoneDeliverySchedulerInputParams(BaseModel):
    # Origin zone for the parcel (e.g., "Eastern", "Central")
    originZone: str
    # Destination zone for the parcel (e.g., "Mountain", "Pacific")
    destinationZone: str
    # Priority level of delivery (e.g., "Standard", "Express", "Overnight")
    priorityLevel: str
    # Type of product being shipped
    productType: str
    # Estimated delivery date
    estimatedDeliveryDate: str

class DeliveryWindowRecommendation(BaseModel):
    timeWindow: str  # e.g., "10:00 AM - 12:00 PM"
    peakTime: bool  # Indicates if the time window is during peak hours
    businessHours: str  # Business hours for the destination zone

class CarrierOption(BaseModel):
    name: str  # Carrier name, e.g., "UPS Ground"
    deliveryTimeEstimate: str  # Estimated delivery time for this carrier

class TimeZoneDeliverySchedulerAnalysisResults(BaseModel):
    optimalDeliveryWindows: List[DeliveryWindowRecommendation]  # Suggested delivery windows across time zones
    carrierOptions: List[CarrierOption]  # Carrier options with estimated delivery times
    transitImpactSummary: str  # Summary of transit and peak season impacts
    peakTimeAnalysis: Plot  # Line chart showing peak times across time zones
    carrierEfficiencyComparison: Plot  # Bar chart for carrier efficiency comparison across time zones
    seasonalImpactPrediction: str  # Seasonal impact prediction based on origin and destination zones
    peakSeasonDelayEstimate: str  # Estimated delay time if shipping during peak season
    timeZoneSpecificRegulations: List[str]  # Regulations affecting delivery in specific time zones
    recommendedDeliveryDateAdjustment: str  # Adjusted recommended delivery date if on a weekend/holiday
    trafficImpactAnalysis: str  # Summary of expected traffic impacts in origin and destination zones
    holidaySeasonAlerts: List[str]  # Alerts for upcoming holidays that could delay delivery
    deliverySuccessProbability: float  # Probability percentage of on-time delivery
    

def time_zone_delivery_scheduler_prompt(inputParameters: TimeZoneDeliverySchedulerInputParams):

    knowledge_file = open("data/timezone_schedule.json", "r")
    knowledge = json.loads(knowledge_file.read())
    knowledge_file.close()

    system_prompt = (
        """
    You are an assistant for a shipping community called the Time Zone Delivery Scheduler.
    Your expertise is in planning parcel delivery schedules across U.S. time zones.
    Your task is to recommend optimal delivery windows, carrier options, and provide insights on transit impacts, traffic, seasonal adjustments, and probability of on-time delivery.

    Strictly use the following data as the basis for your analysis:
    """
        + json.dumps(knowledge, indent=4) +
        """

    **Output Format:**

    - `optimalDeliveryWindows`: 
        - **Format**: List of `DeliveryWindowRecommendation` objects.
        - **Description**: Provide recommended delivery windows, highlighting peak hours and standard business hours.
        - **Goal**: Ensure timely and coordinated delivery across different time zones.

    - `carrierOptions`: 
        - **Format**: List of `CarrierOption` objects.
        - **Description**: List carriers suitable for the specified priority level, with estimated delivery times.
        - **Goal**: Help users select the best carrier based on time efficiency across zones.

    - `transitImpactSummary`: 
        - **Format**: Text-based.
        - **Description**: Summarize expected transit impacts, including any delays due to peak seasons, regional weather, or traffic patterns.
        - **Goal**: Provide users with an overview of potential transit conditions.

    - `peakTimeAnalysis`: 
        - **Chart Type**: "lineChart"
        - **Description**: Display peak times across each zone, showing patterns that may affect scheduling.
        - **Goal**: Visualize when peak traffic times occur to optimize scheduling.

    - `carrierEfficiencyComparison`: 
        - **Chart Type**: "barChart"
        - **Description**: Compare carrier efficiency and estimated delivery time across zones.
        - **Goal**: Enable users to identify the most efficient carriers for selected routes.

    - `seasonalImpactPrediction`: 
        - **Format**: Text-based.
        - **Description**: Provide an outlook on how seasonal changes affect delivery timelines between the origin and destination zones.
        - **Goal**: Enable users to plan around seasonal delays.

    - `peakSeasonDelayEstimate`: 
        - **Format**: Text-based.
        - **Description**: Estimate potential delays if shipping during peak season or holidays.
        - **Goal**: Inform users of additional buffer times required during high-demand periods.

    - `timeZoneSpecificRegulations`: 
        - **Format**: List of regulation strings.
        - **Description**: Provide any regulatory cutoffs or restrictions specific to each time zone affecting parcel delivery.
        - **Goal**: Ensure compliance with zone-specific regulations for timely delivery.

    - `recommendedDeliveryDateAdjustment`: 
        - **Format**: Text-based.
        - **Description**: Suggest adjustments to the recommended delivery date if the initial date falls on a weekend or holiday.
        - **Goal**: Help users choose the most appropriate delivery date for successful on-time delivery.

    - `trafficImpactAnalysis`: 
        - **Format**: Text-based.
        - **Description**: Summarize expected traffic impacts at the origin and destination zones, especially during rush hours.
        - **Goal**: Provide insight into transit conditions due to traffic.

    - `holidaySeasonAlerts`: 
        - **Format**: List of holiday alert strings.
        - **Description**: Notify users of upcoming holidays that might delay delivery.
        - **Goal**: Help users plan for holiday-related delays.

    - `deliverySuccessProbability`: 
        - **Format**: Percentage (float).
        - **Description**: Provide an estimated probability of on-time delivery based on current conditions.
        - **Goal**: Offer a probabilistic insight into the likelihood of on-time delivery.

    **Note:** Use only the specified chart types: ["barChart", "lineChart"]. Each output should directly address the specific aspect of delivery scheduling and impact it represents.
    """
    )

    user_prompt = (
        """
        Analyze the delivery schedule requirements based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "time-zone-delivery-scheduler": {
        "prompt_func": time_zone_delivery_scheduler_prompt,
        "response_format": TimeZoneDeliverySchedulerAnalysisResults,
        "input_format": TimeZoneDeliverySchedulerInputParams,
        "options": {
            "originZone": ["Eastern", "Central", "Mountain", "Pacific"],
            "destinationZone": ["Eastern", "Central", "Mountain", "Pacific"],
            "priorityLevel": ["Standard", "Express", "Overnight"],
        }
    }
}
