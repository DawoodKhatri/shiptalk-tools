import json
from pydantic import BaseModel
from typing import List, Dict, Optional
from .custom_types.base_types import Plot
import random


class SalesAndOperationsPlanningInputParamsType(BaseModel):
    company_size: str  # Options: 'Small', 'Medium', 'Large'
    industry_sector: str  # E.g., 'Retail', 'Manufacturing', 'Healthcare'
    current_sales_data: Dict[str, float]  # Monthly sales data
    inventory_levels: Dict[str, float]  # Current inventory levels for each product
    operational_constraints: List[str]  # E.g., ['Limited Production Capacity']
    demand_forecast_horizon_months: int
    user_objectives: List[
        str
    ]  # E.g., ['Improve Forecast Accuracy', 'Reduce Stockouts']
    current_challenges: Optional[List[str]] = (
        None  # E.g., ['Inaccurate Forecasts', 'High Inventory Costs']
    )


class KeyPerformanceIndicator(BaseModel):
    kpi_name: str  # E.g., 'Forecast Accuracy', 'Inventory Turnover Rate'
    current_value: float
    expected_improvement_percentage: float


class RiskAnalysis(BaseModel):
    risk_description: str
    mitigation_suggestion: str


class SalesAndOperationsPlanningAnalysisResults(BaseModel):
    optimized_forecast: Optional[Dict[str, float]] = None  # Make this field optional
    recommended_inventory_levels: Optional[Dict[str, float]] = (
        None  # Make this field optional
    )
    estimated_cost_savings_percentage: float
    expected_improvement_in_service_levels: str  # E.g., 'Reduced stockouts by 15%'
    key_performance_indicators: List[KeyPerformanceIndicator]
    implementation_plan: List[str]
    risk_analysis: List[RiskAnalysis]
    key_considerations: List[str]
    charts: List[Plot]
    success_stories: Optional[str] = (
        None  # Optional field to provide case studies or examples
    )
    overall_suggestion: str  # Theoretical strategic suggestion


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
You are an AI assistant specializing in supply chain optimization and demand forecasting.
Your task is to analyze the user's sales and operations data to provide actionable insights
that will optimize resource allocation, enhance demand forecasting accuracy, and ensure seamless coordination across all departments.

### *User Objectives and Priorities*
Before starting your analysis, please consider the user's primary goals. The user may specify their main objectives such as:
- Improve forecast accuracy
- Reduce stockouts
- Optimize inventory levels
- Enhance customer satisfaction
- Increase operational efficiency
- Other specific priorities

Tailor your recommendations to align with these objectives.

### *Input Structure*
Here is the expected structure of the input data:
{json_schema}

### *Visualization Types*
Please generate relevant visualizations to support your analysis. The possible chart types are:
- **barChart**: Displays categorical data with rectangular bars.
- **pieChart**: Represents parts of a whole as pie slices.
- **lineChart**: Shows data trends over time or continuous variables.
- **areaChart**: Similar to a line chart, but with filled areas to represent quantities.
- **scatterPlot**: Displays values for typically two variables for a set of data.
- **heatMap**: Represents data values as colors in a matrix.

### *Instructions*
Analyze the provided data to recommend optimal sales and operations planning strategies. Ensure the following:
- Integrate sales forecasts, inventory management, and operational planning data.
- Provide optimized demand forecasts and recommended inventory levels.
- Identify cost-saving opportunities and improvements in service levels.
- Include exactly {totalCharts} visualizations in your analysis: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s).
- Provide a theoretical overall suggestion to improve supply chain processes.
- Identify key performance indicators (KPIs) relevant to S&OP and measure the impact of your recommendations on these KPIs.
- Consider practical constraints such as operational limitations, resource availability, or market volatility.
- Account for industry-specific challenges and regulatory requirements.
- Explore innovative solutions like advanced analytics, machine learning models, or collaborative platforms if applicable.
- Assess potential risks associated with the recommended strategies and suggest ways to mitigate them.

### *Implementation Roadmap*
Provide a step-by-step plan on how to implement the suggested strategies. This should include actionable steps that the user can follow.

### *Success Stories or Case Studies*
Include examples of how similar strategies have benefited other companies, if possible but not mandatory. A real-world context can help reinforce the recommendations.

### *Output Formatting Guidelines*
Please structure your output in the following format:

1. **Introduction**: Briefly summarize the key findings.
2. **User Objectives Alignment**: Explain how your recommendations align with the user's specified objectives.
3. **Recommendations**:
   - Provide optimized demand forecasts.
   - Recommend ideal inventory levels.
   - Provide estimated cost savings as a percentage.
   - Describe expected improvements in service levels.
4. **Key Performance Indicators (KPIs)**:
   - Identify relevant KPIs.
   - Explain how the recommendations impact these KPIs.
5. **Implementation Roadmap**:
   - Step-by-step plan to implement the strategies.
6. **Risk Analysis**:
   - Assess potential risks.
   - Suggest mitigation strategies.
7. **Key Considerations**:
   - Highlight important factors to consider when implementing S&OP.
8. **Visualizations**:
   - Include the specified number of visual charts ({totalCharts} charts: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s)) to represent insights.
9. **Success Stories or Case Studies**:
   - Provide examples where similar strategies have been successful.
10. **Conclusion**:
    - Offer a general theoretical recommendation for improving supply chain processes through S&OP.
11. **Feedback Prompt**:
    - Ask the user if further clarification or additional analysis is needed.

### *Output Requirements*
The output should contain the following elements:
- Only provide factual information based on your knowledge base.
- Optimized demand forecasts and recommended inventory levels.
- Estimated cost savings as a percentage.
- Expected improvements in service levels.
- Identification of key performance indicators (KPIs) and how the recommendations impact them.
- A step-by-step implementation plan.
- A risk assessment of the recommended strategies.
- Key considerations when implementing S&OP.
- Include the specified number of visual charts ({totalCharts} charts: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s)) to represent insights.
- Examples or case studies where similar strategies have been successful.
- A general theoretical recommendation for improving supply chain processes through S&OP.
""".format(
        json_schema=SalesAndOperationsPlanningInputParamsType,
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
