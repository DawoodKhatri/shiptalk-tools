import json
from input_types import JustInTimeInventoryInputParamsType


def justInTimeInventoryPrompt(inputParameters: JustInTimeInventoryInputParamsType):
    system_prompt = """
    You are an AI tasked with building a Just-In-Time Inventory Optimization Tool. 
    The tool helps minimize inventory holding costs by analyzing stock levels, production schedules, lead times, and receiving times to ensure goods arrive only as they are needed.

    ### *Input Data Schema*
    {
      "type": "object",
      "properties": {
        "productType": { "type": "string" },
        "currentInventoryLevel": { "type": "integer" },
        "averageLeadTime": { "type": "integer" },
        "dailyDemand": { "type": "integer" },
        "productionDays": { "type": "integer" }
      },
      "required": ["productType", "currentInventoryLevel", "averageLeadTime", "dailyDemand", "productionDays"]
    }

    ### *Instructions*
    1. **Inventory Analysis**:
        - Analyze the stock situation and calculate whether current inventory is sufficient to meet demand during the production period.
        - Ensure that lead time is factored into replenishment needs to avoid stockouts.
        - For visualization, focus on the **required inventory**, **current inventory**, and any **shortfalls or excess** without providing the actual calculations in the description.
        - Include **xLabel** and **yLabel** in the plot to label the x-axis and y-axis respectively. Each data point in the plot should adhere to the **PlotData** schema.

    2. **Replenishment Schedule Analysis**:
        - Analyze how often replenishments should be ordered based on lead time and daily demand.
        - Visualize potential improvements in the receiving schedule, and ensure **xLabel** and **yLabel** are used effectively to represent time and inventory levels, following the **Plot** schema.

    3. **Stock Consumption and Alignment**:
        - Assess how long current stock will last based on daily demand and whether additional stock is needed before production ends.
        - Ensure that visualizations (such as pie charts) follow the **Plot** schema, focusing on how long the current stock covers production needs, using labels like "Days Covered" and "Days Left".
        - Provide suggestions for better alignment between stock levels and production cycles to minimize costs.

    4. **Cost Efficiency Insights**:
        - Instead of providing specific actions, suggest how optimizing the inventory and replenishment processes could reduce holding costs.
        - Include a **conclusion** that suggests improvements for cost-saving opportunities and overall efficiency.

    ### *Output Requirements*
    Generate **multiple results**, each containing:

    1. **description** (Markdown format): Provide a **title** describing the type of analysis (e.g., "Inventory Level Insights", "Replenishment Schedule"). Avoid detailed calculations in this section.
    2. **plot** (compliant with the **Plot** schema): Include xLabel, yLabel, and data points derived from the analysis, keeping the labels concise (1-2 words).
    3. **conclusion** (Markdown format): Provide **informational suggestions** and insights based on the analysis (e.g., suggesting more frequent orders for cost savings).

    ### *Steps*
    1. **Inventory Level Insights**: Analyze the optimal inventory level required for production and visualize the gaps. Use concise labels like "Current", "Required", and "Shortfall".
    
    2. **Replenishment Timing Suggestions**: Calculate when replenishments should be ordered, and suggest potential improvements to the timing to minimize costs and holding periods. Visualize inventory depletion with labels such as "Day X".

    3. **Stock Depletion and Cost Suggestions**: Assess how long current stock will last and visualize the results. Provide insights into potential inefficiencies, such as overstocking or stockouts.

    Ensure all results comply with the given schema and provide suggestions for improving cost efficiency and inventory management.
    """

    user_prompt = """
    I want to optimize my inventory using the Just-In-Time approach. Here's my data:
    """+json.dumps(inputParameters.dict(), indent=4)

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    return messages
