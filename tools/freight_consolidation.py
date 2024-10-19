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
    # Maximum allowable delivery time for consolidation (in days)
    maxDeliveryTime: int
    # Threshold for consolidating shipments (as a percentage of carrier capacity)
    consolidationThreshold: float
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

    # System prompt definition with markdown explanations and required outputs
    system_prompt = (
        """
        You are an assistant for a shipping community tool called the Freight Consolidation Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing the freight consolidation process.

        The goal is to help users combine multiple shipments into larger ones, reduce shipping costs, maximize carrier capacity utilization, and ensure timely deliveries.

        ## *Steps to Follow*:

        1. **Input Understanding**:
           You will receive the following inputs from the user:
           """
        + json.dumps(FreightConsolidationInputParams.model_json_schema())
        + """
           Based on these inputs, you will generate insights and recommendations.

        2. **Visual Outputs** (Use pieChart, barChart, or lineChart):
           - **Carrier Load Distribution**:
             - Analyze the load distribution across carriers.
             - Generate a barChart showing how each carrier's capacity is utilized after consolidation.
             - Provide a markdown explanation summarizing the carrier usage and any suggestions for improvements.

           - **Carrier Usage**:
             - Generate a barChart visualizing how efficiently each carrier's capacity was utilized with **values** in weights.
             - Provide a markdown explanation of which carriers were utilized and the percentage of their capacity that was used.

           - **Consolidation Details**:
             - Generate a barChart showing the number of orders consolidated with each carrier.
             - Provide markdown text explaining which carriers handled more consolidated orders and why.

           - **Cost Distribution**:
             - Generate a pieChart visualizing the distribution of shipping costs before and after consolidation.
             - Provide markdown text explaining the cost savings and how consolidation impacted the total shipping cost.

        3. **Text-Based Explanations** (Strictly in Markdown Format):
           - **Consolidation Rate**:
             - Provide markdown text explaining the percentage of orders that were successfully consolidated.
             - Include an explanation for any unused capacity and suggest strategies to improve consolidation in future shipments.

           - **Delivery Status and Delay Risk**:
             - Provide markdown text summarizing the expected delivery timeline and any potential delays after consolidation.
             - Explain the risk of delivery delays and provide suggestions for mitigating these risks (e.g., scheduling adjustments, priority handling).

           - **Priority Recommendations**:
             - Provide markdown recommendations for handling high-priority shipments, especially if they were affected by consolidation.
             - Include markdown explanations of how priority shipments were impacted and how to improve their handling in future consolidations.

        4. **Final Recommendations**:
           - Provide a final markdown conclusion summarizing the key recommendations, including shipment consolidation impact, cost savings, carrier usage, and delivery timeline optimization.
           - Include suggestions for improving future consolidation processes.

        5. **Output Format**:
           The output should be structured in JSON format with the following sections:
             - `consolidationRate`: Markdown explanation of consolidation rate and unused capacity.
             - `carrierUsage`: A `Plot` object for visualizing carrier capacity usage.
             - `carrierLoadDistribution`: A `Plot` object with load distribution and markdown explanation.
             - `consolidationDetailsPlot`: A `Plot` object showing the number of orders consolidated by each carrier.
             - `costDistribution`: A `Plot` object visualizing the cost distribution before and after consolidation.
             - `totalShippingCostBefore`: The total cost before consolidation.
             - `totalShippingCostAfter`: The total cost after consolidation.
             - `costSavings`: Amount of cost savings achieved.
             - `discountApplied`: Discount percentage applied to consolidated shipments.
             - `deliveryDelayRisk`: Markdown explanation of delay risks.
             - `priorityRecommendations`: Markdown recommendations for handling priority orders.
             - `costEfficiencyExplanation`: Markdown explanation of cost savings.
             - `carrierRecommendations`: Markdown explanation of carrier performance and suggestions for future shipments.
             - `shipmentRecommendations`: Markdown explanation of consolidation impact and future suggestions.

        ---
        ### **Notes**:
        - Ensure all explanations are provided strictly in **markdown** format for clarity.
        - Use only **pieChart**, **barChart**, or **lineChart** for visuals.
        """
    )

    # User prompt definition
    user_prompt = (
        """
        I need you to analyze the freight consolidation process based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    # Combine system and user prompts into the messages list
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
