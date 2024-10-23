import json
from pydantic import BaseModel
from .custom_types.base_types import Plot, ComparisonPlot
from pydantic import BaseModel


class Order(BaseModel):
    orderWeight: float  # Weight of the order
    destinationAddress: str  # Destination location (city, state, or zip code)
    originAddress: str  # Origin location (city, state, or zip code)
    serviceType: str  # Type of service (e.g., "Standard", "Express")


class CarrierOption(BaseModel):
    carrierName: str  # Name of the carrier
    carrierCapacity: float  # Maximum load capacity of the carrier


class FreightConsolidationInputParams(BaseModel):
    orders: list[Order]  # List of orders to be consolidated
    # Available carriers and their capacities
    carrierOptions: list[CarrierOption]
    # Threshold for consolidating shipments (as a percentage of carrier capacity)
    shippingCostPerUnit: float  # Cost of shipping per unit or weight
    bulkDiscountRate: int  # Discount rates for bulk shipments
    # Optional priority level (e.g., "High", "Medium", "Low")
    priorityLevel: str


class RiskAnalysis(BaseModel):
    riskLevel: str  # Low, Medium, High (risk categorization)
    riskProgress: float  # Numeric representation for progress bar (0-100)
    explanation: str  # Markdown explanation for the risk level


class DeliveryStatus(BaseModel):
    status: str  # e.g., "On Time", "Delayed"
    explanation: str  # Explanation in markdown format


class CostEfficiency(BaseModel):
    laborEfficiency: str  # Explanation in markdown format
    dockUtilization: str  # Explanation in markdown format
    truckCapacityUtilization: str  # Explanation in markdown format


class ConsolidationDetails(BaseModel):
    consolidatedOrders: list[str]  # List of orders that were consolidated
    carrier: str  # Carrier assigned to consolidated orders


class FreightConsolidationAnalysisResults(BaseModel):
    consolidationRate: float  # Percentage of orders successfully consolidated
    consolidationDetails: Plot  # Breakdown of consolidated orders and their carrier

    totalShippingCostBefore: float  # Total cost before consolidation
    totalShippingCostAfter: float  # Total cost after consolidation
    costSavings: float  # Amount of cost savings achieved
    discountApplied: int  # Discount percentage applied to consolidated shipments

    # Bar chart of carrier usage and their capacity utilization
    carrierUsage: ComparisonPlot
    carrierLoadDistribution: Plot  # Bar chart of carrier load distribution
    # Bar chart comparing total shipping costs before and after consolidation
    costComparison: Plot

    # Risk level of delays after consolidation (Low, Medium, High)
    deliveryDelayRisk: str

    priorityRecommendations: str  # Markdown recommendations for handling priority orders
    priorityImpact: str  # Markdown explanation of how priority orders were impacted

    # Markdown explanation of consolidation impact and future suggestions
    shipmentRecommendations: str
    costEfficiencyExplanation: str  # Markdown explanation of cost savings
    # Markdown explanation of carrier performance and suggestions for future shipments
    carrierRecommendations: str


def freight_consolidation_prompt(inputParameters: FreightConsolidationInputParams):
    system_prompt = """
    You are an assistant for a shipping community called the Freight Consolidation Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing the freight consolidation process.

    The goal is to help users combine multiple shipments into larger ones, reduce shipping costs, maximize carrier capacity utilization.
    
    Make use of all the input parameters provided to generate insightful analysis and recommendations.
    The output should include visualizations and explanations for each aspect of the consolidation process.
    Try to combine as many orders as as possible into larger one while considering the carrier capacities.
    
    Output Format:
    - Consolidation Rate: The percentage of orders that were successfully consolidated.
    - Consolidation Details: A barChart visualizing the breakdown of consolidated orders and their carrier.
    - Toatal Shipping Cost Before: The total cost before consolidation.
    - Total Shipping Cost After: The total cost after consolidation.
    - Cost Savings: Amount of cost savings achieved.
    - Discount Applied: Discount percentage applied to consolidated shipments.
    - Carrier Usage: A barChart visualizing how efficiently each carrier's capacity was utilized with values in weights.
    - Carrier Load Distribution: A barChart showing how each carrier's capacity is utilized after consolidation.
    - Cost Comparison: A pieChart visualizing the distribution of shipping costs before and after consolidation.
    - Delivery Delay Risk: Markdown explanation of delay risks.
    - Priority Recommendations: Markdown recommendations for handling priority orders.
    - Priority Impact: Markdown explanation of how priority orders were impacted.
    - Shipment Recommendations: Markdown explanation of consolidation impact and future suggestions.
    - Cost Efficiency Explanation: Markdown explanation of cost savings.
    - Carrier Recommendations: Markdown explanation of carrier performance and suggestions for future shipments.
    
    Note: 
    Chart Types can only include barChart, pieChart, or lineChart.
    """

    user_prompt = """
    I need you to analyze the freight consolidation process based on the following input:
    
    """ + json.dumps(inputParameters.model_dump(), indent=4)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "freight-consolidation": {
        "prompt_func": freight_consolidation_prompt,
        "response_format": FreightConsolidationAnalysisResults,
        "input_format": FreightConsolidationInputParams,
        "options": {
            "serviceType": ["Standard", "Express", "Priority"],
            "priorityLevel": ["High", "Medium", "Low"],
        }
    }
}
