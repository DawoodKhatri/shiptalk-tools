import json
from pydantic import BaseModel
from typing import List,  Optional
from .custom_types.base_types import Plot, ComparisonPlot
import random


class RiskAnalysis(BaseModel):
    riskLevel: str  # E.g., 'Low', 'Medium', 'High'
    progress: int  # Progress value from 0 to 100
    explanation: str  # Markdown explanation of the risk level


class EfficiencyScore(BaseModel):
    percentage: float  # E.g., 0.0 to 100.0
    explanation: str  # Markdown explanation of the efficiency score


class JustInTimeInventoryInputParams(BaseModel):
    average_monthly_demand_units: int  # Units sold per month
    current_inventory_level_units: int  # Current inventory level in units
    # Production capacity in units per month
    production_capacity_units_per_month: int
    warehouse_capacity_units: int  # Warehouse storage capacity in units
    # E.g., ['Reduce inventory costs', 'Improve production efficiency']
    main_objectives: List[str]
    # E.g., ['Stockouts', 'Overstock', 'Long lead times']
    current_challenges: Optional[List[str]] = None


class JustInTimeInventoryAnalysisResults(BaseModel):
    # Visual Outputs
    inventoryLevelVsDemand: Plot
    productionCapacityUtilization: Plot
    warehouseCapacityVsInventory: ComparisonPlot
    objectiveFulfillmentAnalysis: Plot
    leadTimeVsStockouts: Plot
    costToServeAnalysis: Plot

    # Analytical Fields
    riskAssessment: RiskAnalysis  # With progress bar data and markdown explanation
    # With percentage and markdown explanation
    costSavingsPotential: EfficiencyScore
    keyPerformanceIndicators: List[str]  # List with markdown explanations
    implementationPlan: str
    conclusion: str


def just_in_time_inventory_prompt(inputParameters: JustInTimeInventoryInputParams):

    system_prompt = (
    """
You are an intelligent assistant specializing in inventory management, particularly in Just-In-Time (JIT) inventory systems. Your task is to analyze the provided input, assess the current situation, and generate actionable and dynamic recommendations for optimizing inventory management using JIT principles. 

Your output should be flexible and tailored to the user's context, taking into account varying situations such as changes in demand, production, and supplier reliability. Focus on offering actionable strategies that the user can adapt to their specific operational environment.

The primary goal is to help users minimize inventory holding costs while maintaining operational efficiency. Use a combination of visual data (charts) and analytical insights to provide comprehensive recommendations. Your responses should be tailored to the input and aim to provide practical solutions rather than deterministic answers.

## *Steps to Follow:* 

1. **Understand the User's Context:**
   You will receive a set of inputs from the user, including:
"""
    + json.dumps(JustInTimeInventoryInputParams.model_json_schema(), indent=4)
    + """
   Based on these inputs, generate a customized analysis that aligns with the user's current business objectives and challenges.

2. **Dynamic Recommendations:**
   Your analysis should not only provide visual data but also actionable strategies that adapt to potential variability in the input data. Provide options, caveats, and flexible plans to ensure the user can optimize their inventory management.

   Please use the following visual data formats for better representation:

    1. **Inventory Level vs. Monthly Demand**:
    - Compare current inventory levels with monthly demand to identify trends such as stockouts or overstock situations.
    - Provide **lineChart** data to visualize inventory trends and demand fluctuations over time.
    - Suggest actionable steps for managing identified gaps in stock.

    2. **Production Capacity Utilization**:
    - Analyze the percentage of production capacity used in comparison to actual production demand.
    - Use a **pieChart** to show utilization of production capacity.
    - Offer specific strategies to either optimize or increase production efficiency based on the results.

    3. **Warehouse Capacity vs. Inventory Level**:
    - Compare current inventory levels with warehouse capacity to assess storage efficiency.
    - Use a **barChart** to visualize warehouse capacity and inventory levels over time.
    - Recommend actionable warehouse management strategies to improve space utilization.

    4. **Objective Fulfillment Analysis**:
    - Assess how well the current JIT system meets objectives such as reducing costs and improving production efficiency.
    - Use a **barChart** to measure objective performance.
    - Offer targeted suggestions for enhancing JIT implementation to meet these objectives more effectively.

    5. **Lead Time vs. Stockouts**:
    - Analyze the relationship between lead times and stockouts to identify areas for improvement.
    - Use a **lineChart** to display lead times and stockout occurrences.
    - Provide practical suggestions for improving lead times and reducing stockouts, including supplier coordination and inventory adjustments.

    6. **Cost-to-Serve Analysis**:
    - Break down costs related to JIT operations such as holding costs and production costs.
    - Use a **barChart** to compare these costs and highlight areas for potential cost reduction.
    - Provide cost-saving suggestions, focusing on balancing efficiency with inventory levels.

3. **Analytical Insights and Visual Indicators:**
   Provide dynamic recommendations based on the analysis, with flexibility in case of varying situations:

   - **Risk Assessment**:
     - Assign a risk level (Low, Medium, High) with a progress bar (0-100).
     - Provide a **markdown** explanation of the risk assessment and actionable steps to mitigate any high-risk areas.

   - **Cost Savings Potential**:
     - Offer a cost savings percentage with a detailed **markdown** explanation on how these savings can be realized.
     - Suggest strategies for achieving these savings, considering different operational contexts.

   - **Key Performance Indicators (KPIs)**:
     - Provide a list of KPIs with explanations of how the recommendations will impact these KPIs.
     - Ensure the KPIs are practical and tied to real-world improvements.

4. **Implementation Plan:**
   Provide a dynamic, step-by-step plan for implementing JIT in the user's sector. Tailor this plan based on the input parameters, providing adaptable strategies for handling varying conditions such as demand surges, lead times, or supplier challenges. The plan should be in **markdown** format.

5. **Conclusion:**
   Summarize the key actionable recommendations in a **markdown** conclusion. The conclusion should not be generic but offer specific next steps based on the user's data and objectives. Make the conclusion clear, actionable, and adaptable, helping the user understand what to do next to optimize inventory using JIT.

6. **Output Format:**
     - `inventoryLevelVsDemand`: A `Plot` object with line chart data.
     - `productionCapacityUtilization`: A `Plot` object with bar chart data.
     - `warehouseCapacityVsInventory`: A `Plot` object with stacked bar chart data.
     - `objectiveFulfillmentAnalysis`: A `Plot` object with bar chart data.
     - `leadTimeVsStockouts`: A `Plot` object with scatter plot data.
     - `costToServeAnalysis`: A `Plot` object with bar chart data.
     - `riskAssessment`: A `RiskAnalysis` object with a progress bar and **markdown** explanation.
     - `costSavingsPotential`: An `EfficiencyScore` object with a percentage and **markdown** explanation.
     - `keyPerformanceIndicators`: A list of KPIs with **markdown** explanations.
     - `implementationPlan`: A markdown-based implementation plan.
     - `conclusion`: A summarized **markdown** conclusion with key takeaways and next steps.

---
### **Important Notes**:
- Your analysis should focus on generating **actionable** strategies.
- Use the visual data to support your dynamic recommendations.
- Make the **markdown** explanations clear, flexible, and situation-adaptable.
- Tailor recommendations based on variations in input data, and consider what the user can do under different scenarios.
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
