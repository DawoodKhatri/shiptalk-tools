import json
from pydantic import BaseModel
from typing import List,  Optional
from .custom_types.base_types import Plot
import random

class RiskAnalysis(BaseModel):
    riskLevel: str  # E.g., 'Low', 'Medium', 'High'
    progress: int  # Progress value from 0 to 100
    explanation: str  # Markdown explanation of the risk level

class EfficiencyScore(BaseModel):
    percentage: float  # E.g., 0.0 to 100.0
    explanation: str  # Markdown explanation of the efficiency score

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
    # Visual Outputs
    recommendedOrderSchedule: Plot  # LineChart or AreaChart with markdown explanation
    inventoryLevelVsDemand: Plot  # LineChart with markdown explanation
    costSavingsEstimate: Plot  # PieChart with markdown explanation
    productionCapacityUtilization: Plot  # BarChart with markdown explanation
    riskAnalysisChart: Plot  # BarChart or PieChart with markdown explanation

    # Analytical Fields
    riskAssessment: RiskAnalysis  # With progress bar data and markdown explanation
    costSavingsPotential: EfficiencyScore  # With percentage and markdown explanation
    keyPerformanceIndicators: List[str]  # List with markdown explanations

    # Implementation Plan
    implementationPlan: str  # Markdown format

    # Conclusion
    conclusion: str  # Summarized markdown text conclusion with key takeaways


def just_in_time_inventory_prompt(inputParameters: JustInTimeInventoryInputParams):

    system_prompt = (
        """
You are an assistant specializing in inventory management, particularly in Just-In-Time (JIT) inventory systems. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing their inventory management using JIT principles.

The goal is to help users minimize inventory holding costs by receiving goods only as they are needed in the production process. Your output will consist of visual data (restricted to pieChart, barChart, areaChart, and lineChart), explanations of that data, and a final conclusion that summarizes key takeaways and recommendations.

## *Steps to Follow:*

1. **Input Understanding**:
   You will receive a set of inputs from the user, including:
"""
        + json.dumps(JustInTimeInventoryInputParams.model_json_schema(), indent=4)
        + """
   Based on these inputs, you need to generate analysis and recommendations.

2. **Visual Outputs** (only use pieChart, barChart, areaChart, or lineChart):
   - **Optimal Ordering Schedule**:
     - Provide an optimal ordering schedule to meet production needs while minimizing inventory.
     - Generate data for a lineChart or areaChart showing the recommended ordering quantities over time.
     - Include an explanation of how this schedule aligns with demand and production capacity.
     - The explanation should be in **markdown** format.

   - **Inventory Level vs Demand**:
     - Visualize the relationship between inventory levels and average monthly demand.
     - Create a lineChart showing inventory levels and demand over time.
     - Include an explanation of how JIT can reduce inventory levels while meeting demand.
     - The explanation should be in **markdown** format.

   - **Cost Savings Estimate**:
     - Estimate potential cost savings from implementing JIT.
     - Create a pieChart showing the distribution of current costs and potential savings.
     - Provide an explanation of where cost savings come from.
     - The explanation should be in **markdown** format.

   - **Production Capacity Utilization**:
     - Analyze production capacity utilization.
     - Create a barChart showing current vs optimized production capacity utilization.
     - Include an explanation of how JIT affects production efficiency.
     - The explanation should be in **markdown** format.

   - **Risk Analysis**:
     - Identify risks such as stockouts or supplier delays.
     - Create a barChart or pieChart illustrating the risks and their potential impact.
     - Include an explanation of mitigation strategies.
     - The explanation should be in **markdown** format.

3. **Analytical Fields** (Add visual indicators for better insights):
   - **Risk Assessment**:
     - Provide a risk level (Low, Medium, High) and display it using a progress bar (0-100).
     - Include a markdown explanation of why this risk level was chosen.

   - **Cost Savings Potential**:
     - Provide an estimated cost savings percentage.
     - Include a markdown explanation of how these savings can be achieved.

   - **Key Performance Indicators (KPIs)**:
     - List relevant KPIs for JIT implementation.
     - Provide explanations of how the recommendations will impact these KPIs.

4. **Implementation Plan**:
   - Outline a step-by-step plan for implementing JIT in the user's industry sector.
   - The plan should be in **markdown** format.

5. **Conclusion**:
   - Provide a final conclusion that summarizes the key recommendations and strategic suggestions.
   - The conclusion should be strictly in the form of **markdown** text.
   - The conclusion should be clear and actionable, giving the user a step-by-step understanding of what they should do next to optimize their inventory management using JIT.

6. **Output Format**:
   The output should be structured in JSON format with the following sections:
     - `recommendedOrderSchedule`: A `Plot` object with visual data and **markdown** explanation.
     - `inventoryLevelVsDemand`: A `Plot` object with visual data and **markdown** explanation.
     - `costSavingsEstimate`: A `Plot` object with visual data and **markdown** explanation.
     - `productionCapacityUtilization`: A `Plot` object with visual data and **markdown** explanation.
     - `riskAnalysisChart`: A `Plot` object with visual data and **markdown** explanation.
     - `riskAssessment`: A `RiskAnalysis` object with progress bar data and **markdown** explanation.
     - `costSavingsPotential`: An `EfficiencyScore` object with percentage and **markdown** explanation.
     - `keyPerformanceIndicators`: A list of KPIs with **markdown** explanations.
     - `implementationPlan`: A step-by-step plan in **markdown** format.
     - `conclusion`: A summarized **markdown** text conclusion with key takeaways.

---
### **Notes**:
- Ensure the visual data is formatted in a way that can be used for creating charts and graphs.
- Use only **pieChart**, **barChart**, **areaChart**, or **lineChart** for visuals.
- Keep the explanations simple and understandable, focusing on why the recommendations are beneficial.
- The final conclusion should provide a summary that helps the user understand what actions they need to take next.
- The Explanation and Conclusion sections should be in **markdown** format only.
"""
    )

    user_prompt = (
        """
Please analyze the following data and provide recommendations for implementing Just-In-Time inventory management:
"""
        + json.dumps(inputParameters.model_dump(), indent=4)
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
