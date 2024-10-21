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
    average_monthly_demand_units: int  # Units sold per month
    current_inventory_level_units: int  # Current inventory level in units
    production_capacity_units_per_month: int  # Production capacity in units per month
    warehouse_capacity_units: int  # Warehouse storage capacity in units
    main_objectives: List[str]  # E.g., ['Reduce inventory costs', 'Improve production efficiency']
    current_challenges: Optional[List[str]] = None  # E.g., ['Stockouts', 'Overstock', 'Long lead times']



class JustInTimeInventoryAnalysisResults(BaseModel):
    # Visual Outputs
    inventoryLevelVsDemand: Plot
    productionCapacityUtilization: Plot
    warehouseCapacityVsInventory: Plot
    objectiveFulfillmentAnalysis: Plot
    leadTimeVsStockouts: Plot
    costToServeAnalysis: Plot 
    
    # Analytical Fields
    riskAssessment: RiskAnalysis  # With progress bar data and markdown explanation
    costSavingsPotential: EfficiencyScore  # With percentage and markdown explanation
    keyPerformanceIndicators: List[str]  # List with markdown explanations
    implementationPlan: str
    conclusion: str 


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

2. **Visual Data**
   Please ensure to use only the specified chart types for this analysis. The value of ChartType must be ['barChart', 'pieChart', 'lineChart', 'scatterPlot'].

    1. **Inventory Level vs. Monthly Demand**:
    - Compare current inventory levels against monthly demand to identify stockouts or overstock situations.
    - Use a **line chart** to visualize inventory trends and demand fluctuations over time.

    2. **Production Capacity Utilization**:
    - Analyze the percentage of production capacity used compared to the actual production demand.
    - Use a **bar chart** to display the utilization of production capacity.

    3. **Warehouse Capacity vs. Inventory Level**:
    - Compare current inventory levels with available warehouse capacity to ensure efficient storage.
    - Use a **stacked bar chart** to visualize warehouse capacity and inventory levels over time.

    4. **Objective Fulfillment Analysis**:
    - Assess how well the JIT system meets objectives such as reducing inventory costs or improving efficiency.
    - Use a **radar chart** to visualize performance across multiple objectives.

    5. **Lead Time vs. Stockouts**:
    - Explore the relationship between lead times and stockout occurrences to identify areas for improvement.
    - Use a **scatter plot** to show lead times and corresponding stockout events.

    6. **Cost-to-Serve Analysis**:
    - Break down various costs related to JIT operations, such as holding costs and production costs.
    - Use a **bar chart** to compare the costs and highlight areas where cost reductions can be made.

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
     - `inventoryLevelVsDemand`: A `Plot` object with line chart data.
     - `productionCapacityUtilization`: A `Plot` object with bar chart data.
     - `warehouseCapacityVsInventory`: A `Plot` object with stacked bar chart data.
     - `objectiveFulfillmentAnalysis`: A `Plot` object with radar chart data.
     - `leadTimeVsStockouts`: A `Plot` object with scatter plot data.
     - `costToServeAnalysis`: A `Plot` object with bar chart data.
     - `riskAssessment`: A `RiskAnalysis` object with progress bar data and **markdown** explanation.
     - `costSavingsPotential`: An `EfficiencyScore` object with percentage and **markdown** explanation.
     - `keyPerformanceIndicators`: A list of KPIs with **markdown** explanations.
     - `implementationPlan`: A step-by-step plan in **markdown** format.
     - `conclusion`: A summarized **markdown** text conclusion with key takeaways.

---
### **Notes**:
- Ensure the visual data is formatted in a way that can be used for creating charts and graphs.
- Use only **pieChart**, **barChart**, **lineChart**, and **scatterPlot** for visual data.
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
