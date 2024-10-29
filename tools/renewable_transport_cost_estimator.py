import json
from pydantic import BaseModel
from typing import List, Dict, Optional
from .custom_types.base_types import Plot

class RenewableTransportCostEstimatorInputParams(BaseModel):
    routeDistance: float  # Route distance in miles
    carrierType: str  # Type of renewable-powered carrier (e.g., "electricVehicle", "hydrogenVehicle", "biofuelVehicle")


class CarrierCostEstimate(BaseModel):
    vehicleName: str
    energySource: str
    costEstimate: float  # Total cost estimate for the route
    costPerUnit: str  # Cost per unit (e.g., per kWh, per kg, per gallon)
    efficiency: str  # Efficiency per mile
    environmentalImpact: str  # Emission reduction and impact summary


class RenewableTransportCostEstimatorResults(BaseModel):
    estimatedTotalCost: float  # Estimated total cost for the route using selected carrier
    carrierCostEstimates: List[CarrierCostEstimate]  # Breakdown of costs for each carrier type
    emissionReductions: Optional[Dict[str, str]]  # Emission reduction details for each carrier type
    recommendedCarrier: str  # Recommended carrier type for given route distance
    carrierComparisonAnalysis: Plot  # Bar chart comparing cost efficiency across carrier types
    environmentalIncentives: List[str]  # List of available incentives for renewable transport


def renewable_transport_cost_estimator_prompt(inputParameters: RenewableTransportCostEstimatorInputParams):
    with open("data/renewable_cost.json", "r") as knowledge_file:
        knowledge = json.load(knowledge_file)

    system_prompt = (
        """
    You are an assistant for a shipping tool called the Renewable Transport Cost Estimator.
    Your role is to calculate and compare costs for using renewable-powered carriers (Electric, Hydrogen, Biofuel) based on input data.

    Use the provided data for reference:
    """
        + json.dumps(knowledge, indent=4) +
        """

    **Output Format:**

    Your output should include the following fields:

    - `estimatedTotalCost`: 
        - **Format**: Float.
        - **Description**: Total estimated cost for the route using the chosen carrier type.
        - **Goal**: To provide a clear overview of the transportation cost using renewable energy.

    - `carrierCostEstimates`: 
        - **Format**: List of `CarrierCostEstimate` objects.
        - **Description**: Detailed cost analysis per carrier type, including energy source, cost per unit, efficiency per mile, and environmental impact.
        - **Goal**: To help users compare the cost and efficiency of different renewable carriers.

    - `emissionReductions`: 
        - **Format**: Dictionary.
        - **Description**: Emission reduction details for each carrier type.
        - **Goal**: To highlight the environmental benefits of each renewable carrier type.

    - `recommendedCarrier`: 
        - **Format**: String.
        - **Description**: Carrier type recommended based on the route distance.
        - **Goal**: Guide users to the most efficient carrier for their route length.

    - `carrierComparisonAnalysis`: 
        - **Chart Type**: "barChart"
        - **Description**: Show cost efficiency comparison across carrier types.
        - **Goal**: Visual representation of carrier cost-effectiveness for informed decision-making.
        - **Explanation**: Summary of the cost benefits of each carrier type.

    - `environmentalIncentives`: 
        - **Format**: List of strings.
        - **Description**: Available environmental incentives, subsidies, or grants related to the chosen carrier type.
        - **Goal**: Inform users of cost-saving opportunities for renewable transport.

    **Note:**
    Only use ["barChart"] for visualizations to compare carrier cost efficiency.
    """
    )

    user_prompt = (
        """
        I need a cost analysis for renewable-powered transport based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "renewable-transport-cost-estimator": {
        "prompt_func": renewable_transport_cost_estimator_prompt,
        "response_format": RenewableTransportCostEstimatorResults,
        "input_format": RenewableTransportCostEstimatorInputParams,
        "options": {
            "carrierType": ["electricVehicle", "hydrogenVehicle", "biofuelVehicle"]
        }
    }
}
