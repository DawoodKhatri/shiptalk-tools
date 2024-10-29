import json
from pydantic import BaseModel
from typing import List, Dict, Optional
from .custom_types.base_types import Plot

class ColdChainDeliveryInputParams(BaseModel):
    # Type of product being shipped (e.g., Electronics, Pharmaceuticals, Wine, etc.)
    productType: str
    # Weather condition affecting the shipment (e.g., "Extreme Heat", "Extreme Cold", etc.)
    weatherCondition: str
    # Distance of the route in miles
    routeDistance: float
    # Carrier option selected (e.g., "CoolTech Logistics", "PolarShield Transport", etc.)
    carrier: str
    # Required temperature maintenance during transit (in Fahrenheit)
    temperatureRequirement: float
    
class SpecificationItem(BaseModel):
    name: str  # Specification name
    value: str  # Specification value

class PackagingRecommendation(BaseModel):
    name: str  # Name of the recommended packaging type
    cost: float  # Cost for the recommended packaging
    specifications: List[SpecificationItem]  # Specifications of the packaging

class CarrierCostEstimate(BaseModel):
    name: str  # Carrier name
    rating: float  # Carrier rating for reliability
    capabilities: List[str]  # Carrier-specific capabilities
    costPremium: float  # Additional cost factor for the carrier

class ColdChainDeliveryCostEstimateResults(BaseModel):
    packagingRecommendations: List[PackagingRecommendation]  # Suggested packaging with cost and specs
    carrierCostEstimate: CarrierCostEstimate  # Cost and capabilities for the selected carrier
    totalDeliveryCost: float  # Total estimated delivery cost
    weatherImpactAssessment: str  # Assessment of weather's impact on delivery
    costBreakdownChart: Plot  # Bar chart showing breakdown of costs
    environmentalRiskLevel: str  # Risk level based on weather, route distance, and product type
    handlingRecommendations: List[str]  # Additional handling recommendations to ensure product safety
    estimatedDeliveryTime: str  # Estimated time for delivery based on distance and carrier capabilities
    temperatureDeviationRisk: str  # Risk level for possible temperature deviations during transit
    packagingCostEfficiencyChart: Plot  # Plot showing cost efficiency of packaging options relative to temperature protection
    seasonalAdjustmentRecommendations: str  # Recommendations for any seasonal adjustments to packaging or handling

def cold_chain_delivery_cost_estimator_prompt(inputParameters: ColdChainDeliveryInputParams):

    knowledge_file = open("data/climate.json", "r")
    knowledge = json.loads(knowledge_file.read())
    knowledge_file.close()

    system_prompt = (
        """
    You are an assistant for a shipping community tool called the Cold-Chain Delivery Cost Estimator.
    Your expertise is in calculating delivery costs for temperature-sensitive shipments based on product type, weather conditions, route distance, and carrier selection.

    Strictly use the following data as the foundation for your analysis:
    """
        + json.dumps(knowledge, indent=4) +
        """

    **Output Format:**

    - `Packaging Recommendations`: 
        - **Format**: List of `PackagingRecommendation` objects.
        - **Description**: Provide recommended packaging options tailored to the weather conditions, including names, costs, and specifications.
        - **Goal**: Ensure optimal packaging is selected for maintaining required temperature and protecting the product.
            - Specifications.name: String in human-readable form, using natural language capitalization.
            
    - `Carrier Cost Estimate`: 
        - **Format**: `CarrierCostEstimate` object.
        - **Description**: List the selected carrier's name, rating, and capabilities. Include any additional cost factor as `costPremium`.
        - **Goal**: Ensure carrier selection matches temperature control and handling needs.

    - `Total Delivery Cost`: 
        - **Format**: Float.
        - **Description**: Calculate the total estimated delivery cost, factoring in carrier premium, packaging, and route distance.
        - **Goal**: Provide a clear estimate of the total delivery cost for the cold-chain shipment.

    - `Weather Impact Assessment`: 
        - **Format**: Text-based.
        - **Description**: Summarize the expected impact of the specified weather condition on delivery, such as increased handling requirements in extreme temperatures.
        - **Goal**: Provide a realistic outlook of how weather may affect delivery.

    - `Cost Breakdown Chart`: 
        - **Chart Type**: "barChart"
        - **Description**: Show a breakdown of the costs for packaging, carrier premium, and other relevant factors.
        - **Goal**: Visualize the cost structure to help users understand expense distribution.

    - `Environmental Risk Level`: 
        - **Format**: Text-based.
        - **Description**: Determine the environmental risk level (e.g., "Low", "Moderate", "High") based on route distance, temperature requirements, and weather conditions.
        - **Goal**: Warn users of any potential environmental risks to the product.

    - `Handling Recommendations`: 
        - **Format**: List of strings.
        - **Description**: Provide recommendations for special handling instructions, such as minimizing temperature fluctuations.
        - **Goal**: Assist users in managing temperature-sensitive shipments with additional care.

    - `Estimated Delivery Time`: 
        - **Format**: Text-based.
        - **Description**: Estimated time for delivery based on route distance and carrier capabilities.
        - **Goal**: Offer an estimate for the total time the shipment will take to reach its destination.

    - `Temperature Deviation Risk`: 
        - **Format**: Text-based.
        - **Description**: Assess the risk level for potential temperature fluctuations during transit.
        - **Goal**: Warn users of any possible risks to temperature maintenance.

    - `Packaging Cost Efficiency Chart`: 
        - **Chart Type**: "lineChart"
        - **Description**: Illustrate cost-efficiency of packaging options relative to their protective capabilities.
        - **Goal**: Aid users in selecting the most cost-effective packaging for temperature-sensitive protection.

    - `Seasonal Adjustment Recommendations`: 
        - **Format**: Text-based.
        - **Description**: Recommendations for adjusting packaging or handling based on seasonal changes, such as using extra insulation in winter.
        - **Goal**: Guide users in making seasonal adjustments for optimal cold-chain performance.

    **Note:** Ensure all fields in the output are in human-readable format. For example, use "Total Delivery Cost" instead of "totalDeliveryCost." Only use "barChart" for the cost breakdown visualization.
    """
    )

    user_prompt = (
        """
        Please analyze the cold-chain delivery cost requirements based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "cold-chain-delivery-cost-estimator": {
        "prompt_func": cold_chain_delivery_cost_estimator_prompt,
        "response_format": ColdChainDeliveryCostEstimateResults,
        "input_format": ColdChainDeliveryInputParams,
        "options": {
            "weatherCondition": ["Extreme Heat", "Extreme Cold", "High Humidity", "Extreme Temperature Fluctuation"]
        }
    }
}
