import json
from pydantic import BaseModel
from .custom_types.base_types import Plot, ComparisonPlot
from pydantic import BaseModel
from typing import List


class StopDetail(BaseModel):
    address: str  # Address of the stop
    parcelType: str  # Type of parcel (e.g., "Standard", "Perishable", "Fragile")
    priorityLevel: str  # Priority level of the parcel (e.g., "High", "Medium", "Low")

class MultiStopRouteOptimizerInputParams(BaseModel):
    stops: List[StopDetail]  # List of stop details
    routeStart: str  # Starting location for the route
    urgencyLevel: str  # Overall urgency for route completion (e.g., "Standard", "Express", "Critical")



class RouteStopDetail(BaseModel):
    address: str  # Address of the stop
    parcelType: str  # Type of parcel at this stop
    priorityLevel: str  # Priority level for the stop
    sequenceOrder: int  # The stop's order in the optimized route
    handlingRequirements: str  # Special handling requirements (e.g., "Fragile handling", "Temperature control")



class MultiStopRouteOptimizerOutput(BaseModel):
    optimizedRoute: List[RouteStopDetail]  # Sequenced stops with detailed requirements
    totalStops: int  # Total number of stops in the optimized route
    highPriorityParcelCount: int  # Number of high-priority parcels in the route
    handlingRequirementSummary: List[str]  # Summary of specific handling requirements across stops
    highRiskStops: List[str]  # Addresses of stops with high risk of delays based on parcel type or handling complexity
    delayRiskAnalysis: Plot  # Bar chart showing delay risks by stop, based on handling complexity or priority level
    travelComplexityAnalysis: Plot  # Line chart showing route complexity by stop type (e.g., fragile, perishable)
    priorityParcelImpact: Plot  # Pie chart showing distribution of parcels by priority level
    handlingRequirementsDistribution: Plot  # Bar chart showing the type and frequency of handling requirements across stops
    handlingCostEstimation: Plot  # Bar chart showing estimated handling costs based on requirements (e.g., fragile, temperature control)
    recommendations: List[str]  # Actionable recommendations to improve route efficiency


def multi_stop_route_optimizer_prompt(inputParameters: MultiStopRouteOptimizerInputParams):

    system_prompt = (
        """
    You are an assistant for a shipping community tool called the Multi-Stop Parcel Route Optimizer.
    Your expertise lies in optimizing multi-stop parcel delivery routes. Given inputs such as stops, parcel types, and priority levels, your role is to generate efficient routes that prioritize high-value parcels, streamline handling requirements, and sequence stops to reduce complexity and avoid delays.

    **Output Format:**

    Your output should include the following fields, each with specific details:

    - `optimizedRoute`: 
        - **Format**: List of `RouteStopDetail` objects.
        - **Description**: Display the sequenced stops in the most efficient order, providing details on address, parcel type, priority level, and specific handling requirements.
        - **Goal**: Offer a time-optimized and priority-aligned order of stops to reduce delivery complexity.

    - `totalStops`: 
        - **Format**: Integer.
        - **Description**: Total count of stops in the optimized route.
        - **Goal**: To give users an overview of the route's scope.

    - `highPriorityParcelCount`: 
        - **Format**: Integer.
        - **Description**: The number of high-priority parcels on the route.
        - **Goal**: To highlight the urgency of certain stops for improved route planning.

    - `handlingRequirementSummary`: 
        - **Format**: List of strings.
        - **Description**: Summarize special handling requirements (e.g., "Temperature control required for 3 stops").
        - **Goal**: Helps users allocate specific resources for handling requirements across stops.

    - `highRiskStops`: 
        - **Format**: List of strings.
        - **Description**: List of stops with high risk of delays based on parcel type or handling complexity.
        - **Goal**: Enables users to preemptively address or monitor high-risk stops.

    - `delayRiskAnalysis`: 
        - **Chart Type**: "barChart"
        - **Description**: Display delay risks by stop, considering parcel type, handling needs, and priority level.
        - **Goal**: Highlight stops with higher delay risks for informed sequencing adjustments.
        - **Explanation**: Explain insights on stops prone to delays.

    - `travelComplexityAnalysis`: 
        - **Chart Type**: "lineChart"
        - **Description**: Show route complexity by stop type (e.g., fragile, perishable).
        - **Goal**: Identify complexity trends that may impact efficiency and sequencing.
        - **Explanation**: Provide insights on potential complications due to stop types.

    - `priorityParcelImpact`: 
        - **Chart Type**: "pieChart"
        - **Description**: Show the distribution of parcels by priority level (e.g., High, Medium, Low).
        - **Goal**: Helps users prioritize stops by parcel urgency.

    - `handlingRequirementsDistribution`: 
        - **Chart Type**: "barChart"
        - **Description**: Show handling requirements (e.g., fragile, temperature control) frequency across stops.
        - **Goal**: Informs users of the resource allocation needs based on handling requirements.

    - `handlingCostEstimation`: 
        - **Chart Type**: "barChart"
        - **Description**: Estimated handling costs by requirement type (e.g., fragile handling, temperature control).
        - **Goal**: Provide a cost overview based on specific handling requirements.
        - **Explanation**: Explain insights on cost implications for each handling requirement.

    - `recommendations`: 
        - **Format**: List of actionable strings.
        - **Description**: Specific recommendations to enhance route efficiency, such as resource allocation or sequence adjustments.
        - **Goal**: Provide practical advice for handling high-priority stops and minimizing delays.

    **Note:**
    Only use the following chart types: ["barChart", "lineChart", "pieChart"]. Each chart should offer clear insights into specific areas of multi-stop route optimization.
    """
    )
    
    user_prompt = (
    """
    I need you to analyze the multi-stop parcel route based on the following input parameters:

    **Input Parameters:**
    - `stops`: 
        - **Format**: List of `StopDetail` objects.
        - **Description**: Each stop along the route, including the address, parcel type, priority level, and handling requirements. Helps structure the sequence and priority of the route.
        - **Fields**:
            - `address`: Address of the stop (e.g., "456 Oak Ave, Shelbyville").
            - `parcelType`: Type of parcel for this stop, such as "Standard," "Perishable," or "Fragile."
            - `priorityLevel`: The priority level for the stop (e.g., "High," "Medium," "Low").

    - `routeStart`: 
        - **Format**: String.
        - **Description**: Starting location for the route - origin (e.g., warehouse or distribution center).

    - `urgencyLevel`: 
        - **Format**: String.
        - **Description**: The urgency level for the entire route (e.g., "Standard," "Express," "Same-Day"), which helps prioritize delivery sequencing.

    - `maxStops`: 
        - **Format**: Integer.
        - **Description**: The maximum number of stops allowed for this route, which may influence the route optimization.

    Based on these inputs, provide a detailed analysis of the optimized stop sequence, parcel priorities, handling requirements, risk levels, and actionable improvements. Ensure the recommendations directly enhance efficiency and mitigate identified risks without needing specific time estimates for each stop.
    """
    + json.dumps(inputParameters.model_dump(), indent=4)
)


    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages



tool_config = {
    "multi-stop-route-optimizer": {
        "prompt_func": multi_stop_route_optimizer_prompt,
        "response_format": MultiStopRouteOptimizerOutput,
        "input_format": MultiStopRouteOptimizerInputParams,
        "options": {
            "parcelType": ["Standard", "Perishable", "Fragile", "Oversized", "Hazardous"],
            "priorityLevel": ["High", "Medium", "Low"],
            "handlingRequirements": ["Temperature Controlled", "Fragile Handling", "Special Security", "Dry Storage"],
            "urgencyLevel": ["Standard", "Express", "Critical"]  # Overall urgency level for the route
        }
    }
}
