import json
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from .custom_types.base_types import Plot
import random


class SeasonalPlanningInputParamsType(BaseModel):
    peak_season_periods: List[str]  # E.g., ['November', 'December']
    daily_shipments: int  # Average daily shipments
    expected_demand_increase_percentage: float  # Expected percentage increase in demand
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

    1. **Peak Season Periods**: The months or periods when peak season is expected (e.g., ['November', 'December']).
    2. **Daily Shipments**: The average number of shipments handled daily during non-peak seasons.
    3. **Expected Demand Increase**: The percentage increase in demand expected during the peak season.
    4. **Available Capacity**: The total available shipping and storage capacity during the peak season.
    5. **Constraints**: Any constraints that may limit operations (e.g., 'Budget Limitations').

    ### Visualization Types
    Please generate relevant visualizations to support your analysis. The possible chart types are:
    - **barChart**: Displays categorical data with rectangular bars.
    - **pieChart**: Represents parts of a whole as pie slices.
    - **lineChart**: Shows data trends over time or continuous variables.
    - **scatterPlot**: Displays the correlation between two variables (e.g., risk probability and impact).
    Please ensure to use only the specified chart types for this analysis. The value of ChartType must be ['barChart', 'pieChart', 'lineChart', 'scatterPlot'].

    ### Instructions
    Analyze the provided data to recommend optimal strategies for the upcoming peak seasons. Ensure the following:
    - Provide detailed inventory adjustment recommendations.
    - Suggest staffing changes needed to meet increased demand.
    - Recommend logistics operations adjustments to handle increased shipments.
    - Estimate the cost implications of these adjustments.
    - Identify potential risks and suggest mitigation strategies.
    - Provide a concise summary of all recommendations.

    ### Graphs to Include
    Please generate the following graphs to support the analysis:

    1. **Demand vs. Capacity**:
    - Compare the expected peak season demand vs. available shipping and storage capacity.
    - Use a bar chart to visualize how demand stacks up against capacity.
    
    2. **Cost Impact**:
    - Show the breakdown of estimated additional costs due to increased demand (e.g., labor, logistics, storage).
    - Use a pie chart to represent each cost component.

    3. **Staffing vs. Expected Demand**:
    - Show the relationship between staffing levels and expected demand over time.
    - Use a line chart to track changes in staffing and shipments.

    4. **Risk Probability vs. Impact**:
    - Visualize the potential risks by plotting their probability and impact.
    - Use a scatter plot to highlight risks with high probability and impact.

    5. **Inventory Adjustment**:
    - Recommend inventory adjustments over time based on demand forecasts.
    - Use a bar chart to track inventory levels before and during the peak season.

    6. **Daily Shipments Over Time**:
    - Track daily shipments from non-peak to peak season.
    - Use a line chart to visualize the expected increase in daily shipments.

    7. **Inventory Distribution**: 
    - Analyze the input data to recommend how inventory should be distributed across the specified warehouse regions.
    - Generate data for a pieChart or barChart showing the percentage allocation for each region.
    - Include an explanation of why the distribution is recommended based on demand levels and warehouse capacities.
    - The explanation should be in **markdown** format.

    ### Output Formatting Guidelines
    Please structure your output in the following format:

    1. **Summary**: Complete overview of the recommendations in markdown format.    
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
