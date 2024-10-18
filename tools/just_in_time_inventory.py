import json
from pydantic import BaseModel
from .custom_types.base_types import Plot
from pydantic import BaseModel


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
        - Use **xLabel** and **yLabel** in plots. Choose appropriate chart types.

    2. **Replenishment Schedule**:
        - Analyze when to reorder based on lead time and demand:
          - **Sufficient stock**: Recommend no immediate replenishment; monitor and plan for future.
          - **Low stock**: Suggest immediate replenishment to avoid stockouts.
          - Adjust for **productType** if lead times or demand are affected (e.g., perishable goods or high-demand items).
        - Visualize inventory trends using the appropriate chart type.

    3. **Stock Consumption**:
        - Assess how long current stock will last:
          - **Excess stock**: Suggest reducing it.
          - **Low stock**: Recommend restocking to cover demand.
          - Adjust for **productType** if relevant (e.g., perishable goods need faster turnover).
        - Use appropriate chart types to show days covered vs. days left.

    4. **Cost Efficiency Insights**:
        - Conclusions should cover both excess and insufficient stock:
          - **Excess**: Highlight higher holding costs and suggest reduction.
          - **Low stock**: Emphasize stockout risks and recommend timely restocking.
        - Factor in **productType** for storage or handling costs.
        - Conclusions must use **markdown** formatting and be based on data analysis.

    ### *Output Requirements*
    Generate **multiple results**, each with:

    1. **description**: A concise title for the analysis (e.g., "Inventory Level Insights").
    2. **plot**: xLabel, yLabel, chartType (barChart, pieChart, etc.), and data points. Ensure the **label** in the **data** is concise, limited to 1-2 words, for better readability.
    3. **conclusion**: Provide markdown-formatted, actionable insights based on the analysis (e.g., suggest reducing or replenishing stock), including adjustments based on **productType**.

    """
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
