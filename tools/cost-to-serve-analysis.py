import json
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from .custom_types.base_types import Plot
import random


class CostToServeInputParams(BaseModel):
    business_model: str  # Options: 'B2B', 'B2C', 'D2C', etc.
    key_products: List[str]  # List of product names or IDs
    customer_segments: List[str]  # E.g., 'Wholesale', 'Retail', 'Online'
    average_order_values: Dict[str, float]  # Segment to average order value mapping
    supply_chain_costs: Dict[
        str, float
    ]  # Costs per stage, e.g., {'Manufacturing': 1000.0}
    user_goals: List[str]  # E.g., 'Reduce Cost-to-Serve', 'Improve Margins'
    challenges: Optional[List[str]] = (
        None  # E.g., ['High Delivery Costs', 'Inefficient Warehousing']
    )


class CostToServeAnalysisResults(BaseModel):
    total_cost_to_serve: float
    cost_breakdown: Optional[Dict[str, float]]  # Cost per product or customer segment
    profit_margins: Optional[Dict[str, float]]  # Profit margins per product or segment
    optimization_recommendations: List[str]
    strategic_insights: List[str]
    visualizations: List[Plot]
    implementation_steps: List[str]
    risk_evaluation: List[str]
    case_examples: Optional[str] = None  # Optional field for real-world examples
    final_recommendation: str


def cost_to_serve_analysis_prompt(inputParameters: CostToServeInputParams):
    # Generate random numbers for example charts
    pie_chart_count = random.randint(1, 2)
    bar_chart_count = random.randint(1, 2)
    line_chart_count = random.randint(1, 2)
    total_charts = pie_chart_count + bar_chart_count + line_chart_count

    system_prompt = """
You are a supply chain expert specializing in cost-to-serve analysis.
Your task is to evaluate the costs associated with delivering products to different customer segments,
identify areas for cost reduction, and provide strategic recommendations to enhance profitability.

### Input Structure
Here is the expected structure of the input data:
{json_schema}

### **Analysis Objectives**
Your analysis should focus on:
- Calculating the total cost-to-serve for each product and customer segment.
- Identifying unprofitable products or segments.
- Providing actionable recommendations to reduce costs and improve profit margins.
- Aligning suggestions with the user's specified goals.

### **Visualization Requirements**
Create a total of **{total_charts}** visualizations to support your analysis:
- **Pie Charts**: {pie_chart_count}
- **Bar Charts**: {bar_chart_count}
- **Line Charts**: {line_chart_count}

### **Output Structure**
Please format your analysis with the following sections:

1. **Executive Summary**
   - Briefly summarize the key findings and insights.
2. **Detailed Cost Analysis**
   - Provide a breakdown of costs per product and customer segment.
3. **Profitability Assessment**
   - Analyze profit margins and highlight unprofitable areas.
4. **Optimization Recommendations**
   - Suggest specific actions to reduce costs and enhance profitability.
5. **Strategic Insights**
   - Offer broader strategic considerations based on the analysis.
6. **Implementation Steps**
   - Outline a clear plan to implement the recommendations.
7. **Risk Evaluation**
   - Identify potential risks and propose mitigation strategies.
8. **Visualizations**
   - Include the required charts to illustrate your findings.
9. **Case Examples**
   - If applicable, mention real-world examples of successful cost optimization.
10. **Conclusion**
    - Provide a final recommendation that encapsulates the strategic impact.

### **Guidelines**
- Use professional and concise language.
- Base your analysis on the data provided.
- Ensure that recommendations are practical and actionable.
- Do not include any irrelevant information or assumptions not supported by the data.

Begin your analysis now, focusing on delivering valuable insights to the user.

""".format(
        json_schema=CostToServeInputParams,
        total_charts=total_charts,
        pie_chart_count=pie_chart_count,
        bar_chart_count=bar_chart_count,
        line_chart_count=line_chart_count,
    )

    user_prompt = (
        "Please perform a cost-to-serve analysis based on the following data:\n"
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "cost-to-serve-analysis": {
        "prompt_func": cost_to_serve_analysis_prompt,
        "response_format": CostToServeAnalysisResults,
        "input_format": CostToServeInputParams,
        "options": {
            "business_model": ["B2B", "B2C", "D2C", "Hybrid"],
            "user_goals": [
                "Reduce Cost-to-Serve",
                "Improve Profit Margins",
                "Optimize Distribution Network",
                "Enhance Customer Satisfaction",
                "Streamline Operations",
            ],
            "challenges": [
                "High Delivery Costs",
                "Inefficient Warehousing",
                "Complex Distribution Channels",
                "Low Order Volumes",
                "High Return Rates",
            ],
        },
    }
}
