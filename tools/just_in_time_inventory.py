import json
from pydantic import BaseModel
from .custom_types.base_types import Plot
from pydantic import BaseModel
import random


class JustInTimeInventoryInputParamsType(BaseModel):
    productType: str
    currentInventoryLevel: int
    averageLeadTime: int
    dailyDemand: int
    productionDays: int


class JustInTimeInventoryAnalysisResults(BaseModel):
    description: str
    plots: list[Plot]
    conclusion: str


def just_in_time_inventory_prompt(inputParameters: JustInTimeInventoryInputParamsType):
    pieChart = random.randint(0, 2)
    barChart = random.randint(0, 2)
    lineChart = random.randint(0, 2)
    
    
    system_prompt = (
        """
    You are an AI tasked with building a Just-In-Time Inventory Optimization Tool. 
    Your role is to analyze stock levels, lead times, and production schedules to help minimize inventory holding costs.

    ### *Input Data Schema*
    """
        + json.dumps(JustInTimeInventoryInputParamsType.model_json_schema())
        + """

    ### *Chart Types*
    Possible values for chart types:
    - **barChart**
    - **pieChart**
    - **lineChart**
    - **areaChart**

    ### *Instructions*
    1. **Inventory Analysis**:
        - Determine if current inventory meets production demand.
        - Analyze **productType** to factor in demand patterns, lead times, or handling costs:
          - For high-demand product types, recommend tighter inventory controls and more frequent replenishment.
          - For custom or long-lead-time products, adjust schedules to account for longer production/delivery times.
          - For bulky or costly-to-store items, recommend reducing stock to minimize holding costs.
        - Address excess and insufficient inventory:
          - **Excess**: Suggest reducing stock to lower holding costs.
          - **Insufficient**: Recommend restocking or adjusting the schedule.
        - Generate **multiple plots** to visualize the analysis (e.g., inventory level, demand patterns, stock coverage).

    2. **Replenishment Schedule**:
        - Analyze when to reorder based on lead time and demand:
          - **Sufficient stock**: Recommend no immediate replenishment; monitor and plan for future.
          - **Low stock**: Suggest immediate replenishment to avoid stockouts.
          - Adjust for **productType** if lead times or demand are affected (e.g., perishable goods or high-demand items).
        - Use the appropriate chart type to display trends over time and ensure **multiple plots** are used when necessary.

    3. **Stock Consumption**:
        - Assess how long current stock will last:
          - **Excess stock**: Suggest reducing it.
          - **Low stock**: Recommend restocking to cover demand.
          - Adjust for **productType** if relevant (e.g., perishable goods need faster turnover).
        - Create **multiple plots** to show stock coverage, consumption, and days left.

    4. **Cost Efficiency Insights**:
        - Provide a unified conclusion based on both excess and insufficient stock conditions:
          - **Excess**: Highlight higher holding costs and suggest reduction.
          - **Low stock**: Emphasize stockout risks and recommend timely restocking.
        - Factor in **productType** for storage or handling costs.
        - Ensure the conclusions are **markdown formatted** and summarize key insights from the analysis.

    ### *Output Requirements*
    Generate a response with the following:

    1. **description**: Provide a single, concise title for the analysis (e.g., "Inventory Level Insights").
    2. **plots**: Generate pieChart:{pieChart}, barChart:{barChart} and lineChart:{lineChart} within the same analysis. Each plot should contain:
        - xLabel, yLabel, chartType (barChart, pieChart, etc.), and data points. Ensure the **label** in the **data points** of "plots" is concise, limited to a maximum of 1-2 words, for better readability.
    3. **conclusion**: Provide a single, markdown-formatted conclusion summarizing actionable insights based on the analysis (e.g., suggest reducing or replenishing stock), including adjustments based on **productType**.
    """.format(pieChart=pieChart, barChart=barChart, lineChart=lineChart)
    )

    user_prompt = """
    I want to optimize my inventory using the Just-In-Time approach. Here's my data:
    """ + json.dumps(
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
        "input_format": JustInTimeInventoryInputParamsType,
    }
}
