import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot

class DeliveryLocation(BaseModel):
    location: str
    deliveryTime: str

class ParkingFeeMinimizerInputParams(BaseModel):
    deliveryLocations: List[DeliveryLocation]  # List of delivery locations in the city
    urgencyLevel: str  # Delivery urgency level (e.g., "Standard", "Express", "Same-Day")


class ParkingCostAnalysis(BaseModel):
    location: str  # Delivery location
    zoneType: str  # Zone type for parking fees
    estimatedParkingCost: float  # Estimated total parking cost for the delivery time period


class TrafficAnalysis(BaseModel):
    location: str  # Delivery location
    congestionLevel: str  # Congestion level based on delivery time (e.g., "High", "Moderate", "Low")
    suggestedTime: str  # Suggested delivery time to minimize congestion


class PermitRecommendation(BaseModel):
    permitType: str  # Type of parking permit recommended
    applicableZones: List[str]  # Zones where this permit is applicable
    cost: str  # Monthly or annual permit cost


class UrbanParkingFeeMinimizerResults(BaseModel):
    totalEstimatedParkingCost: float  # Total estimated parking cost for all stops
    parkingCostAnalysis: List[ParkingCostAnalysis]  # Breakdown of parking costs per delivery location
    trafficAnalysis: List[TrafficAnalysis]  # Analysis of congestion levels and suggested times
    loadingZoneInfo: str  # Information about loading zones and any restrictions
    permitRecommendations: List[PermitRecommendation]  # Recommended permits to minimize parking costs
    seasonalEventImpact: str  # Information on how events or seasons may impact parking costs and availability
    parkingFeeComparison: Plot  # Bar chart comparing parking fees at different locations
    congestionImpactAnalysis: Plot  # Line chart showing congestion levels over the day for delivery locations


def urban_parking_fee_minimizer_prompt(inputParameters: ParkingFeeMinimizerInputParams):
    with open("data/parking_fees.json", "r") as knowledge_file:
        knowledge = json.load(knowledge_file)

    system_prompt = (
        """
    You are an assistant for a tool called the Urban Parking Fee Minimizer.
    Your expertise lies in strategizing delivery stops in urban areas to minimize parking fees and manage congestion.
    Use the provided parking fee data, traffic patterns, loading zones, and parking regulations to guide cost-effective route planning.

    **Reference Data:**
    """
        + json.dumps(knowledge, indent=4) +
        """
    
    **Output Format:**

    Your output should include the following fields, each with specific details:

    - `totalEstimatedParkingCost`: 
        - **Format**: Float.
        - **Description**: Total estimated parking cost for all delivery stops.
        - **Goal**: Provide a summary of the expected parking expenses.

    - `parkingCostAnalysis`: 
        - **Format**: List of `ParkingCostAnalysis` objects.
        - **Description**: Show parking fees by location, including zone type, hourly rates, and estimated parking costs.
        - **Goal**: Breakdown of costs to identify high-cost areas and potential savings opportunities.

    - `trafficAnalysis`: 
        - **Format**: List of `TrafficAnalysis` objects.
        - **Description**: Analyze congestion levels at each location based on delivery times, with suggested lower-congestion times.
        - **Goal**: Helps avoid high congestion periods, reducing time spent at stops.

    - `loadingZoneInfo`: 
        - **Format**: Text-based.
        - **Description**: Summarize loading zone restrictions and time limits for commercial deliveries.
        - **Goal**: To inform drivers of areas with free or restricted loading zones to reduce parking fees.

    - `permitRecommendations`: 
        - **Format**: List of `PermitRecommendation` objects.
        - **Description**: Recommend permits to reduce parking costs, listing the permit type, applicable zones, and costs.
        - **Goal**: Provide a cost-saving alternative for deliveries in central or restricted zones.

    - `seasonalEventImpact`: 
        - **Format**: Text-based.
        - **Description**: Summarize seasonal or event-related parking restrictions and congestion impacts.
        - **Goal**: Helps users anticipate changes in parking availability and costs.

    - `parkingFeeComparison`: 
        - **Chart Type**: "barChart"
        - **Description**: Compare parking fees across delivery locations.
        - **Goal**: Visual representation of cost variations by location for effective planning.
        - **Explanation**: Summarize insights on high-cost areas to target cost reductions.

    - `congestionImpactAnalysis`: 
        - **Chart Type**: "lineChart"
        - **Description**: Show congestion levels throughout the day for each delivery location.
        - **Goal**: Helps plan stops at lower congestion times to minimize delays.
        - **Explanation**: Offer insights on peak and low congestion periods.

    **Note:**
    Use only ["barChart", "lineChart"] for visualizations. Ensure each chart provides clear insights into parking fees and congestion patterns.
    """
    )

    user_prompt = (
        """
        I need you to analyze the urban parking fees and optimize delivery stops based on the following inputs:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "urban-parking-fee-minimizer": {
        "prompt_func": urban_parking_fee_minimizer_prompt,
        "response_format": UrbanParkingFeeMinimizerResults,
        "input_format": ParkingFeeMinimizerInputParams,
        "options": {
            "urgencyLevel": ["Standard", "Express", "Same-Day"]
        }
    }
}
