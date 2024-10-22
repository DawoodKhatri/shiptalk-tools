import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot, NamedPlot
import random


class ThirdPartyLogisticsInputParamsType(BaseModel):
    company_size: str  # Options: 'Small', 'Medium', 'Large'
    logistics_functions_to_outsource: List[
        str
    ]  # E.g., ['Warehousing', 'Transportation']
    geographic_regions: List[str]  # E.g., ['North America', 'Europe']
    types_of_products: List[str]  # E.g., ['Electronics', 'Perishable Goods']
    shipment_volume_per_month: int
    user_objectives: List[str]  # E.g., ['Cost Reduction', 'Scalability']
    constraints: List[str] = (
        None  # E.g., ['Budget Limitations', 'Regulatory Compliance']
    )
    current_challenges: List[str] = (
        None  # E.g., ['High Inventory Costs', 'Slow Delivery Times']
    )



class KeyPerformanceIndicator(BaseModel):
    kpi_name: str  # E.g., 'Order Fulfillment Time', 'Inventory Turnover Rate'
    current_value: float
    expected_improvement_percentage: float


class ThirdPartyLogisticsAnalysisResults(BaseModel):
    suggested_providers: List[str]
    estimated_cost_savings_percentage: float
    expected_improvement_in_service_levels: str
    key_performance_indicators: List[KeyPerformanceIndicator]
    implementation_plan: str
    risk_analysis: str
    key_considerations: str
    charts: List[NamedPlot]
    success_stories: str = None  # Optional field to provide case studies or examples
    overall_suggestion: str  # Theoretical strategic suggestion


def third_party_logistics_prompt(
    inputParameters: ThirdPartyLogisticsInputParamsType,
):
    # Generate random data for example charts
    pieChart = random.randint(1, 3)
    barChart = random.randint(1, 3)
    lineChart = random.randint(1, 3)
    totalCharts = pieChart + barChart + lineChart

    # Pass the JSON schema of the input parameters to provide context about the input structure
    system_prompt = """
You are an AI assistant specializing in logistics and supply chain optimization. 
Your role is to analyze the user's logistics needs and offer strategic suggestions for selecting third-party logistics (3PL) providers.

### *User Goals and Priorities*
Before analyzing, consider the user's key objectives, which may include:
- Cost reduction
- Scalability
- Improved service levels
- Access to advanced technologies
- Focus on core competencies
- Specific regional or service priorities

### *Input Structure*
The input data will follow this structure:
{json_schema}

### *Chart Types*
Generate visualizations to support your analysis. Choose from these chart types:
- **barChart**: For displaying categorical data comparisons.
- **pieChart**: For showing proportions of a whole.
- **lineChart**: For depicting trends over time.
- **scatterPlot**: For showing relationships between two variables.

Ensure you only use these chart types in your analysis. The value of ChartType must be one of ['barChart', 'pieChart', 'lineChart', 'scatterPlot'].

### *Instructions*
Provide a detailed analysis using the data to suggest optimal 3PL providers and strategies. You should:
- Identify cost-saving and service level improvement opportunities.
- Recommend 3PL providers that align with the user's logistics needs, geographic location, and other requirements.
- Include exactly {totalCharts} visualizations in the analysis.
- Present a strategic suggestion for improving logistics operations.
- Outline key performance indicators (KPIs) that will measure the impact of your recommendations.
- Address constraints like budget, resources, or regulations based on the company size.
- Consider regional logistics infrastructure or provider availability based on the monthly shippment volume.
- Explore innovative options such as automation, technology integration, or value-added services if applicable.
- Conduct a risk assessment for your suggestions and propose mitigation strategies.

### *Implementation Plan*
Provide an actionable, step-by-step plan in Markdown format to implement your recommendations.

### *Success Stories or Case Studies*
If possible, include examples of how similar logistics strategies have benefited other companies. Use Markdown format for this section.
""".format(
        json_schema=ThirdPartyLogisticsInputParamsType, totalCharts=totalCharts
    )

    user_prompt = "Please analyze the following data:\n" + json.dumps(
        inputParameters.model_dump(), indent=4
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "third-party-logistics": {
        "prompt_func": third_party_logistics_prompt,
        "response_format": ThirdPartyLogisticsAnalysisResults,
        "input_format": ThirdPartyLogisticsInputParamsType,
        "options": {
            "company_size": ["Small", "Medium", "Large"],
            "logistics_functions_to_outsource": [
                "Warehousing",
                "Transportation",
                "Inventory Management",
                "Order Fulfillment",
                "Customs Brokerage",
                "Freight Forwarding",
                "Reverse Logistics",
                "Distribution",
            ],
            "types_of_products": [
                "Electronics",
                "Perishable Goods",
                "Fragile Items",
                "High-Value Products",
                "Oversized & Heavy Items",
                "Temperature-Sensitive Goods",
                "Standard Retail Products",
                "Medical Supplies & Pharmaceuticals",
            ],
            "user_objectives": [
                "Cost Reduction",
                "Scalability",
                "Improved Service Levels",
                "Access to Advanced Technology",
                "Focus on Core Competencies",
                "Operational Efficiency",
                "Enhanced Tracking & Visibility",
            ],
            "constraints": [
                "Budget Limitations",
                "Regulatory Compliance",
                "Limited Resources",
                "Tight Timelines",
                "Data Security Requirements",
                "Customer Service Expectations",
            ],
            "current_challenges": [
                "High Inventory Costs",
                "Slow Delivery Times",
                "Inaccurate Order Fulfillment",
                "Lack of Scalability",
                "Inefficient Processes",
                "High Return Rates",
            ],
            "geographic_regions": [
                "North America",
                "Europe",
                "Asia-Pacific",
                "Latin America",
                "Middle East",
                "Africa",
            ],
        },
    }
}
