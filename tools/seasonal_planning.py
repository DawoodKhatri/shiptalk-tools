import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot


class SeasonalPlanningInputParamsType(BaseModel):
    peak_season_periods: List[str]  # E.g., ['November', 'December']
    daily_shipments: int  # Average daily shipments
    # Expected percentage increase in demand
    expected_demand_increase_percentage: float
    available_capacity: int  # Total available shipping and storage capacity
    constraints: List[str] = None  # E.g., ['Budget Limitations']


class CostBreakdown(BaseModel):
    label: str
    cost: float


class SeasonalPlanningAnalysisResults(BaseModel):
    estimated_cost_impact: float  # Estimated additional costs
    cost_breakdown: List[CostBreakdown]  # Breakdown of estimated costs
    potential_risks: str
    mitigation_strategies: str
    implementation_plan: str
    charts: List[Plot]  # Visualizations to support the analysis
    summary: str  # Overall summary of recommendations


def seasonal_planning_prompt(inputParameters: SeasonalPlanningInputParamsType):

    system_prompt = """
    You are an AI assistant specializing in operational planning for peak seasons.
    Your task is to analyze the user's business data and provide personalized solutions to prepare for peak seasons by adjusting inventory levels, staffing, and logistics operations to handle increased demand.
    
    Output Format:
    1. Estimated Cost Impact: The accurate estimated costs due to increased demand during peak seasons.
    2. Cost Breakdown: A detailed breakdown of the estimated costs.
    3. Potential Risks: A markdown explanation of potential risks.
    4. Mitigation Strategies: A markdown explanation of mitigation strategies.
    5. Implementation Plan: A markdown explanation of the implementation plan.
    6. Chart 1: A "barChart" showing the comparison of expected peak season demand vs. available shipping and storage capacity.
    7. Chart 2: A "pieChart" showing the breakdown of estimated additional costs due to increased demand.
    8. Chart 3: A "lineChart" showing the staffing levels vs. peak season demand over time.
    9. Chart 4: A "barChart" showing the inventory adjustments over time based on demand forecasts.
    10. Summary: A markdown summary of all recommendations.
    """

    user_prompt = """
    Please analyze my business data for the upcoming peak seasons and provide recommendations based on the following input:
    """ + json.dumps(inputParameters.model_dump(), indent=4)

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
