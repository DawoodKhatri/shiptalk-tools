import json
from pydantic import BaseModel
from typing import List, Dict, Optional
from .custom_types.base_types import Plot, NamedPlot
import random


class Items(BaseModel):
    name: str
    quantity: int


class SalesAndOperationsPlanningInputParamsType(BaseModel):
    company_size: str  # Options: 'Small', 'Medium', 'Large'
    industry_sector: str  # E.g., 'Retail', 'Manufacturing', 'Healthcare'
    current_sales_data: Dict[str, float]  # Monthly sales data
    inventory_levels: List[Items]  # Current inventory levels by product category or SKU
    operational_constraints: List[
        str
    ]  # E.g., ['Limited Production Capacity', 'Supplier Delays']
    demand_forecast_horizon_months: int  # Number of months for the forecast
    user_objectives: List[
        str
    ]  # E.g., ['Improve Forecast Accuracy', 'Optimize Inventory']
    current_challenges: Optional[List[str]] = (
        None  # E.g., ['Inaccurate Forecasts', 'Supplier Reliability Issues']
    )
    seasonal_factors: Optional[List[str]] = (
        None  # E.g., ['Holiday Peaks', 'Weather-Related Demand Changes']
    )
    budget_constraints: Optional[float] = (
        None  # Budget available for inventory replenishment or expansion
    )


class KeyPerformanceIndicator(BaseModel):
    kpi_name: str  # E.g., 'Forecast Accuracy', 'Inventory Turnover Rate'
    current_value: float
    expected_improvement_percentage: float


class SalesAndOperationsPlanningAnalysisResults(BaseModel):
    recommended_inventory_levels: Optional[
        List[Items]
    ]  # Recommended inventory levels by product category or SKU
    estimated_cost_savings_percentage: (
        float  # Estimated cost reduction from optimizations
    )
    expected_improvement_in_service_levels: (
        str  # E.g., '5% improvement in on-time delivery'
    )
    key_performance_indicators: List[
        KeyPerformanceIndicator
    ]  # E.g., 'Inventory Turnover Ratio', 'Fill Rate'
    implementation_plan: str  # Steps for implementing the proposed strategies
    risk_analysis: (
        str  # Assessment of risks such as supplier delays or demand variability
    )
    key_considerations: List[
        str
    ]  # Important factors to consider (e.g., production capacity, lead times)
    charts: List[
        NamedPlot
    ]  # Visual representation of forecasts, inventory, cost analysis, etc.
    scenario_analysis: Optional[str] = (
        None  # Scenario-based results, e.g., best/worst-case scenarios
    )
    success_stories: Optional[str] = (
        None  # Example cases of similar businesses achieving results
    )
    overall_suggestion: (
        str  # Strategic recommendation, e.g., 'Increase safety stock by 10%'
    )


def sales_and_operations_planning_prompt(
    inputParameters: SalesAndOperationsPlanningInputParamsType,
):
    # Generate random data for example charts
    pieChart = random.randint(1, 3)
    barChart = random.randint(1, 3)
    lineChart = random.randint(1, 3)
    totalCharts = pieChart + barChart + lineChart

    # Pass the JSON schema of the input parameters to provide context about the input structure
    system_prompt = """
You are an AI assistant specializing in Sales and Operations Planning (S&OP).  
Your task is to analyze the user's business data and provide personalized solutions to optimize sales forecasts, inventory management, and operational adjustments for the upcoming planning period.

### Input Structure  
Here is the expected structure of the input data:
{json_schema}

### Visualization Types  
Please generate relevant visualizations to support your analysis. The possible chart types are:
- **barChart**: Displays categorical data with rectangular bars.
- **pieChart**: Represents parts of a whole as pie slices.
- **lineChart**: Shows data trends over time or continuous variables.
- **scatterPlot**: Displays the correlation between two variables (e.g., risk probability and impact).
- exaplanation must be detailed overview the graph and in markdown format

Please ensure to use only the specified chart types for this analysis. The value of ChartType must be ['barChart', 'pieChart', 'lineChart', 'scatterPlot'].

### Instructions  
Analyze the provided data to recommend optimal strategies for Sales and Operations Planning. Ensure the following:
- Provide optimized sales forecasts based on historical data.
- Recommend adjustments in inventory levels to meet projected demand.
- Suggest operational changes (e.g., supplier selection, capacity planning) to meet forecasted sales.
- Estimate the cost implications of these adjustments.
- Identify potential risks and suggest mitigation strategies.
- Provide a concise summary of all recommendations.

### Graphs to Include  
Please generate the following graphs to support the analysis:

1. **Sales Forecast**:  
   - Visualize the projected sales for the forecast horizon.
   - Use a line chart to track forecast trends over time.

2. **Inventory Adjustment**:  
   - Recommend adjustments to inventory levels based on the optimized forecast.
   - Use a bar chart to track inventory levels before and during the forecast period.

3. **Cost Impact**:  
   - Show the breakdown of estimated additional costs (e.g., inventory holding, logistics).
   - Use a pie chart to represent each cost component.

4. **Demand vs. Capacity**:  
   - Compare the expected demand vs. available operational capacity.
   - Use a bar chart to visualize how demand stacks up against capacity.

5. **Risk Probability vs. Impact**:  
   - Visualize potential risks by plotting their probability and impact.
   - Use a scatter plot to highlight risks with high probability and impact.

### Output Formatting Guidelines  
Please structure your output in the following format:

1. **Summary**:  
   A complete overview of the recommendations in markdown format.

2. **Sales Forecast**:  
   Optimized sales forecast for the given horizon in markdown format.

3. **Inventory Adjustments**:  
   Detailed recommendations for adjusting inventory levels.

4. **Operational Recommendations**:  
   Suggested operational changes to handle forecasted demand.

5. **Estimated Cost Impact**:  
   Estimated additional costs and savings.

6. **Potential Risks and Mitigation Strategies**:  
   - List potential risks.
   - Provide mitigation strategies for each risk.

7. **Implementation Plan**:  
   A step-by-step detailed plan to implement the recommendations in markdown format.

8. **Visualizations Charts**:  
   Include the specified number of charts ({totalCharts} in total) to support your analysis.

9. **Risk Analysis**:
    - Provide an assessment of risks such as supplier delays or demand variability in markdown format.

### Output Requirements  
The output should contain the following elements:
- Factual information based on the input data.
- Clear and actionable recommendations.
- Visualizations to support the analysis.
- A summary that encapsulates the key points.
- All description must be well detailed and easy to understand in markdown format.

""".format(
        json_schema=SalesAndOperationsPlanningInputParamsType,
        totalCharts=totalCharts
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
    "sales-and-operations-planning": {
        "prompt_func": sales_and_operations_planning_prompt,
        "response_format": SalesAndOperationsPlanningAnalysisResults,
        "input_format": SalesAndOperationsPlanningInputParamsType,
        "options": {
            "company_size": ["Small", "Medium", "Large"],
            "industry_sector": [
                "Retail",
                "Manufacturing",
                "Healthcare",
                "Technology",
                "Consumer Goods",
                "Automotive",
                "Pharmaceuticals",
                "Food & Beverage",
            ],
            "user_objectives": [
                "Improve Forecast Accuracy",
                "Reduce Stockouts",
                "Optimize Inventory Levels",
                "Enhance Customer Satisfaction",
                "Increase Operational Efficiency",
                "Reduce Costs",
                "Improve Collaboration Across Departments",
            ],
            "operational_constraints": [
                "Limited Production Capacity",
                "Supply Chain Disruptions",
                "Regulatory Compliance",
                "Budget Limitations",
                "Workforce Shortages",
                "Technology Limitations",
            ],
            "current_challenges": [
                "Inaccurate Forecasts",
                "High Inventory Costs",
                "Slow Response to Market Changes",
                "Lack of Coordination Between Departments",
                "Overproduction or Underproduction",
                "Inefficient Resource Allocation",
            ],
        },
    }
}
