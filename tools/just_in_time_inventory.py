import json
from pydantic import BaseModel
from typing import List, Dict, Optional
from .custom_types.base_types import Plot
import random


class JustInTimeInventoryInputParams(BaseModel):
    industry_sector: str  # E.g., 'Manufacturing', 'Automotive', 'Electronics'
    company_size: int  # Number of employees
    annual_revenue_million_usd: float  # Annual revenue in million USD
    average_monthly_demand_units: int  # Units sold per month
    current_inventory_level_units: int  # Current inventory level in units
    production_capacity_units_per_month: int
    warehouse_capacity_units: int
    main_objectives: List[str]  # E.g., ['Reduce inventory costs', 'Improve production efficiency']
    current_challenges: Optional[List[str]] = None  # E.g., ['Stockouts', 'Overstock', 'Long lead times']


class JustInTimeInventoryAnalysisResults(BaseModel):
    recommended_order_schedule: Optional[Dict[str, int]]  # Dates mapped to order quantities
    estimated_cost_savings_percentage: Optional[float] = None
    risk_analysis: List[str]
    implementation_plan: List[str]
    key_performance_indicators: List[str]
    charts: List[Plot]
    overall_suggestion: str  # General strategic recommendation


def just_in_time_inventory_prompt(
    inputParameters: JustInTimeInventoryInputParams,
):
    # Generate random data for example charts
    pieChart = random.randint(0, 1)
    barChart = random.randint(1, 2)
    lineChart = random.randint(1, 2)
    totalCharts = pieChart + barChart + lineChart

    # Pass the JSON schema of the input parameters to provide context about the input structure
    system_prompt = f"""
You are an AI assistant specializing in inventory management and optimization, particularly in Just-In-Time (JIT) inventory systems.

Your task is to analyze the user's input data to provide actionable insights and recommendations for implementing or improving a Just-In-Time inventory system.

Your analysis should focus on strategically minimizing inventory holding costs by receiving goods only as they are needed in the production process.

### User Objectives and Challenges

Before starting your analysis, consider the user's main objectives and current challenges. Tailor your recommendations to align with these objectives and address the challenges.

### Input Structure

Here is the expected structure of the input data:
{json.dumps(JustInTimeInventoryInputParams.model_json_schema(), indent=4)}

### Instructions

Analyze the provided data to recommend optimal ordering schedules and strategies for implementing a Just-In-Time inventory system. Your analysis should include:

- Recommended ordering schedules to meet production needs while minimizing inventory.
- Estimated cost savings as a percentage, if possible.
- Key performance indicators (KPIs) relevant to JIT implementation.
- Risk analysis, including potential risks such as stockouts due to supplier delays, and strategies to mitigate them.
- Key considerations for implementing JIT in the user's specific industry sector.
- An implementation plan with actionable steps.
- Visualizations to support your recommendations.
- An overall strategic suggestion for improving the inventory management process.

### Output Formatting Guidelines

Please structure your output in the following format:

1. **Introduction**: Briefly summarize the key findings.
2. **User Objectives Alignment**: Explain how your recommendations align with the user's specified objectives.
3. **Recommendations**:
   - Provide recommended ordering schedules.
   - Estimate potential cost savings, if applicable.
4. **Key Performance Indicators (KPIs)**:
   - Identify relevant KPIs.
   - Explain how the recommendations impact these KPIs.
5. **Risk Analysis**:
   - Identify potential risks.
   - Suggest mitigation strategies.
6. **Implementation Plan**:
   - Step-by-step plan to implement the recommendations.
7. **Key Considerations**:
   - Highlight important factors to consider when implementing JIT.
8. **Visualizations**:
   - Include the specified number of visual charts ({totalCharts} charts: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s)) to support your recommendations.
9. **Conclusion**:
   - Offer a general strategic recommendation.
10. **Feedback Prompt**:
   - Ask the user if further clarification or additional analysis is needed.

### Output Requirements

The output should contain the following elements:

- Only provide factual information based on your knowledge base.
- Recommended ordering schedules.
- Estimated cost savings as a percentage, if applicable.
- Key performance indicators (KPIs) and how the recommendations impact them.
- Risk analysis with mitigation strategies.
- Implementation plan.
- Key considerations.
- Visualizations to support your recommendations.
- An overall strategic suggestion.
"""

    user_prompt = "Please analyze the following data:\n" + json.dumps(
        inputParameters.model_dump(), indent=4
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "just-in-time-inventory": {
        "prompt_func": just_in_time_inventory_prompt,
        "response_format": JustInTimeInventoryAnalysisResults,
        "input_format": JustInTimeInventoryInputParams,
        "options": {
            "industry_sector": [
                "Manufacturing",
                "Automotive",
                "Electronics",
                "Retail",
                "Pharmaceuticals",
                "Food & Beverage",
            ],
            "main_objectives": [
                "Reduce inventory costs",
                "Improve production efficiency",
                "Enhance supplier collaboration",
                "Decrease lead times",
                "Increase flexibility",
            ],
            "current_challenges": [
                "Stockouts",
                "Overstock",
                "Long lead times",
                "High holding costs",
                "Supplier unreliability",
                "Production delays",
            ],
        },
    }
}
