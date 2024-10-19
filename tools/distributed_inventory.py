import json
from pydantic import BaseModel
from .custom_types.base_types import Plot, ComparisonPlot
from pydantic import BaseModel


class DemandLevel(BaseModel):
    region: str
    demandLevel: str


class DistributedInventoryInputParamsType(BaseModel):
    warehouseRegions: list[str]
    demandLevels: list[DemandLevel]
    leadTime: int
    productType: str


class DistributedInventoryAnalysisResults(BaseModel):
    # Single dataset, no comparison needed (e.g., pieChart)
    inventoryDistribution: Plot
    replenishmentSchedule: ComparisonPlot  # Current vs. optimized reorder schedule
    # Current vs. optimized shipping costs and times
    shippingCostsAndTimes: ComparisonPlot
    # Current vs. optimized utilization of warehouses
    warehouseUtilization: ComparisonPlot
    demandForecast: ComparisonPlot  # Current vs. forecasted demand levels
    costToServe: ComparisonPlot  # Current vs. optimized cost per unit
    # Single dataset (e.g., recommendations for new warehouse locations)
    newWarehouseRecommendation: Plot
    conclusion: str  # Textual conclusion summarizing key insights


def distributed_inventory_prompt(inputParameters: DistributedInventoryInputParamsType):

    system_prompt = (
        """
    You are an assistant for a shipping community tool called the Distributed Inventory Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing their inventory distribution, shipping costs, warehouse utilization, and other logistics.
    
    The goal is to give users the maximum analysis with the minimum input. Your output will consist of visual data (restricted to pieChart, barChart, areaChart, and lineChart), explanations of that data, and a final conclusion that summarizes key takeaways and recommendations.

    ## *Steps to Follow:*
    
    1. *Input Understanding:*
       You will receive a set of inputs from the user, including:
    """
        + json.dumps(DistributedInventoryInputParamsType.model_json_schema())
        + """
       Based on these inputs, you need to generate analysis and recommendations.
       
    2. *Visual Outputs* (only use pieChart, barChart, areaChart, or lineChart):
       - **Inventory Distribution**: 
         - Analyze the input data to recommend how inventory should be distributed across the specified warehouse regions.
         - Generate data for a pieChart or barChart showing the percentage allocation for each region.
         - Include an explanation of why the distribution is recommended based on demand levels and warehouse capacities.
         - The explanation should be in **markdown** format.
         
       - **Stock Replenishment Strategy**:
         - Calculate when and how much stock the user should reorder to maintain optimal inventory levels.
         - Create a barChart or areaChart showing the recommended reorder schedule.
         - Use a comparison between current reorder patterns and optimized patterns.
         - Include an explanation of how this will help optimize inventory levels and prevent over/under-stocking.
         - The explanation should be in **markdown** format.
         
       - **Shipping Costs and Delivery Times**:
         - Compare the current shipping costs and delivery times with optimized values.
         - Create a barChart showing cost and time improvements.
         - Use a comparison between current and optimized values.
         - Provide an explanation of how adjusting inventory distribution can reduce shipping costs and improve delivery times.
         - The explanation should be in **markdown** format.
         
       - **Warehouse Utilization**:
         - Determine the current utilization of each warehouse and suggest optimizations.
         - Create a barChart showing the utilization percentage of each warehouse.
         - Use a comparison between current and optimized utilization.
         - Include an explanation of how optimizing warehouse use can reduce costs and improve efficiency.
         - The explanation should be in **markdown** format.
         
       - **Demand Forecasting**:
         - Predict future demand based on the provided data and general trends.
         - Create a lineChart that visualizes forecasted demand changes.
         - Use a comparison between current and projected demand levels.
         - Provide an explanation of how understanding demand fluctuations can help manage inventory more effectively.
         - The explanation should be in **markdown** format.
         
       - **Cost-to-Serve Analysis**:
         - Calculate the cost per unit to serve each region from current and optimized warehouse locations.
         - Generate data for a barChart showing these costs.
         - Use a comparison between current and optimized cost per unit.
         - Provide an explanation of the cost savings from optimizing inventory locations and minimizing shipping distances.
         - The explanation should be in **markdown** format.
         
       - **New Warehouse Recommendations**:
         - Based on demand patterns, recommend new warehouse locations if applicable.
         - Generate a barChart showing the suggested regions for new warehouses.
         - Include an explanation of why these new locations will help optimize logistics and reduce shipping times.
         - The explanation should be in **markdown** format.

    3. **Explanations**:
       - For each visual output, provide a clear and concise explanation. The explanation should:
         - Describe what the visual represents.
         - Explain why the recommended actions (e.g., inventory allocation, replenishment schedule) are beneficial based on the input data.
         - Highlight any significant cost savings, delivery time improvements, or other optimizations.
         - The explanation should be strictly in the form of **markdown** text.

    4. **Conclusion**:
       - After generating all the visuals and explanations, provide a final conclusion that summarizes the key recommendations for the user.
       - The conclusion should be strictly in the form of **markdown** text.
       - The conclusion should be clear and actionable, giving the user a step-by-step understanding of what they should do next to optimize their logistics.
       - Mention the most important actions they should take, such as adjusting inventory allocation, reordering stock, or opening new warehouses.

    5. **Output Format**:
       - The output should be structured in JSON format with the following sections:
         - `inventoryDistribution`: A `Plot` object with visual data and **markdown** explanation.
         - `replenishmentSchedule`: A `ComparisonPlot` object with current and optimized data, visual data, and **markdown** explanation.
         - `shippingCostsAndTimes`: A `ComparisonPlot` object with current and optimized data, visual data, and **markdown** explanation.
         - `warehouseUtilization`: A `ComparisonPlot` object with current and optimized data, visual data, and **markdown** explanation.
         - `demandForecast`: A `ComparisonPlot` object with current and forecasted data, visual data, and **markdown** explanation.
         - `costToServe`: A `ComparisonPlot` object with current and optimized data, visual data, and **markdown** explanation.
         - `newWarehouseRecommendation`: A `Plot` object with visual data and **markdown** explanation.
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
    I need you to optimize inventory distribution across multiple warehouses. Below is the information about my current warehouse setup and demand levels:
    """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "distributed-inventory": {
        "prompt_func": distributed_inventory_prompt,
        "response_format": DistributedInventoryAnalysisResults,
        "input_format": DistributedInventoryInputParamsType,
    }
}
