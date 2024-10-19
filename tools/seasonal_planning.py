import json
from pydantic import BaseModel
from typing import List, Dict, Optional
from .custom_types.base_types import Plot
import random


class SeasonalPlanningInputParamsType(BaseModel):
    business_type: str  # E.g., 'Retail', 'E-commerce', 'Manufacturing'
    peak_season_periods: List[str]  # E.g., ['November', 'December']
    inventory_status: Dict[str, float]  # Product names to quantities
    staffing_levels: int
    logistics_capacity: Dict[str, float]  # E.g., {'daily_shipments': 100}
    expected_demand_increase_percentage: float
    constraints: Optional[List[str]] = None  # E.g., ['Budget Limitations']


class SeasonalPlanningAnalysisResults(BaseModel):
    inventory_adjustments: Optional[
        Dict[str, float]
    ]  # Product names to adjusted quantities
    staffing_recommendations: Optional[
        Dict[str, int]
    ]  # E.g., {'additional_staff_needed': 10}
    logistics_recommendations: Optional[
        Dict[str, str]
    ]  # E.g., {'upgrade_needed': 'Yes'}
    estimated_cost_impact: float  # Estimated additional costs
    potential_risks: List[str]
    mitigation_strategies: List[str]
    implementation_plan: List[str]
    charts: List[Plot]
    summary: str  # Overall summary of recommendations


def seasonal_planning_prompt(
    inputParameters: SeasonalPlanningInputParamsType,
):
    # Generate random data for example charts
    pieChart = random.randint(1, 2)
    barChart = random.randint(1, 2)
    lineChart = random.randint(1, 2)
    totalCharts = pieChart + barChart + lineChart

    # Pass the JSON schema of the input parameters to provide context about the input structure
    system_prompt = """
You are an AI assistant specializing in operational planning for peak seasons.
Your task is to analyze the user's business data and provide personalized solutions to prepare for peak seasons by adjusting inventory levels, staffing, and logistics operations to handle increased demand.

### Input Structure
Here is the expected structure of the input data:
{json_schema}

### Visualization Types
Please generate relevant visualizations to support your analysis. The possible chart types are:
- **barChart**: Displays categorical data with rectangular bars.
- **pieChart**: Represents parts of a whole as pie slices.
- **lineChart**: Shows data trends over time or continuous variables.

### Instructions
Analyze the provided data to recommend optimal strategies for the upcoming peak seasons. Ensure the following:
- Provide detailed inventory adjustment recommendations.
- Suggest staffing changes needed to meet increased demand.
- Recommend logistics operations adjustments to handle increased shipments.
- Estimate the cost implications of these adjustments.
- Identify potential risks and suggest mitigation strategies.
- Include exactly {totalCharts} visualizations in your analysis: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s).
- Provide a concise summary of all recommendations.

### Output Formatting Guidelines
Please structure your output in the following format:

1. **Summary**: Brief overview of the recommendations.
2. **Inventory Adjustments**: Detailed recommendations for inventory levels.
3. **Staffing Recommendations**: Suggested changes in staffing.
4. **Logistics Recommendations**: Adjustments needed in logistics operations.
5. **Estimated Cost Impact**: Estimated additional costs.
6. **Potential Risks and Mitigation Strategies**:
   - List potential risks.
   - Provide mitigation strategies for each risk.
7. **Implementation Plan**:
   - Step-by-step plan to implement the recommendations.
8. **Visualizations**:
   - Include the specified number of charts ({totalCharts} charts: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s)) to represent insights.

### Output Requirements
The output should contain the following elements:
- Factual information based on the input data.
- Clear and actionable recommendations.
- Visualizations to support the analysis.
- A summary that encapsulates the key points.

""".format(
        json_schema=SeasonalPlanningInputParamsType,
        totalCharts=totalCharts,
        pieChart=pieChart,
        barChart=barChart,
        lineChart=lineChart,
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
    "seasonal-planning": {
        "prompt_func": seasonal_planning_prompt,
        "response_format": SeasonalPlanningAnalysisResults,
        "input_format": SeasonalPlanningInputParamsType,
        "options": {
            "business_type": [
                "Retail",
                "E-commerce",
                "Manufacturing",
                "Hospitality",
                "Logistics",
                "Food & Beverage",
                "Fashion",
                "Electronics",
            ],
            "peak_season_periods": [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
                "Spring",
                "Summer",
                "Fall",
                "Winter",
            ],
            "constraints": [
                "Budget Limitations",
                "Supplier Constraints",
                "Labor Shortage",
                "Storage Capacity Limits",
                "Regulatory Compliance",
            ],
        },
    }
}
