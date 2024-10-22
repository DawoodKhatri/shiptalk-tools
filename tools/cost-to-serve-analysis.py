import json
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from .custom_types.base_types import Plot, NamedPlot
import random


class CostToServeInputParams(BaseModel):
    business_model: str  # Options: 'B2B', 'B2C', 'D2C', etc.
    # E.g., 'Wholesale', 'Retail', 'Online'
    customer_segments: List[str] = None
    total_supply_chain_cost: (
        # Total cost for supply chain (manufacturing, storage, transport, etc.)
        float
    )
    average_order_value: float  # Average value of an order across segments
    # E.g., 'Reduce Cost-to-Serve', 'Improve Margins'
    user_goals: List[str] = None
    industry_type: Optional[str] = None  # E.g., 'Fashion', 'Tech', 'FMCG'
    # E.g., 'Global', 'North America', 'Asia'
    geographical_scope: Optional[str] = None


class CostToServeAnalysisResults(BaseModel):
    total_cost_to_serve: float  # The overall cost
    optimization_recommendations: str
    strategic_insights: str  # High-level strategic insights for improvement
    implementation_steps: str  # Step-by-step actions to reduce cost-to-serve
    risk_evaluation: str  # Identified risks and mitigations
    final_recommendation: str  # A clear, actionable summary recommendation for the user
    success_probability: (
        float  # A percentage chance of success if recommendations are followed
    )
    potential_savings: Optional[float] = (
        None  # Estimated cost savings if recommendations are implemented
    )
    customer_impact: Optional[str] = (
        None  # Brief description of how changes may affect customer experience
    )
    charts: List[NamedPlot]  # Visualizations to support the analysis


def cost_to_serve_analysis_prompt(inputParameters: CostToServeInputParams):
    # Generate random numbers for example charts
    pie_chart_count = random.randint(1, 2)
    bar_chart_count = random.randint(1, 2)
    line_chart_count = random.randint(1, 2)
    total_charts = pie_chart_count + bar_chart_count + line_chart_count

    system_prompt = """
You are a supply chain expert specializing in cost-to-serve analysis. Your task is to evaluate the costs associated with delivering products to different customer segments, identify areas for cost reduction, and provide strategic recommendations to enhance profitability.

Input Structure
You will be provided with the following structured input data:
{json_schema}

# Analysis Objectives
    Your analysis should focus on the following:
    Total Cost to Serve: Calculate the overall cost of serving customers.
    Optimization Opportunities: Identify key areas where costs can be reduced.
    Strategic Insights: Provide actionable insights based on industry and market trends.
    Implementation Steps: Outline step-by-step actions for reducing costs.
    Risk Evaluation: Highlight potential risks and suggest mitigations.
    Final Recommendations: Provide clear, actionable recommendations to help the business reduce its cost-to-serve while maintaining or improving customer experience.

# Visualization Requirements
    Create a total of 4 visualizations to support your analysis. The chart types should include the following:
    Pie Chart: Cost breakdown by segments (e.g., by customer, product, etc.)
    Bar Chart: The impact of different optimization strategies.
    Line Chart: Historical trends in cost-to-serve over time.
    Scatter Plot: Risk vs. savings for proposed optimizations.
    The ChartType must be one of ['barChart', 'pieChart', 'lineChart', 'scatterPlot'].

# Output Structure
    Format your analysis in the following sections:
    Total Cost to Serve: Provide the overall cost.
    Optimization Recommendations: List key cost-reduction strategies in markdown format.
    Strategic Insights: High-level strategies to improve operations in markdown format.
    Implementation Steps: A detailed plan for how to achieve the recommendations in markdown format.
    Risk Evaluation: Assess risks and mitigations associated with the detailed steps in markdown format.
    Final Recommendation: Summarize the most important recommendation.
    Success Probability: Estimate the likelihood of success as a percentage.
    Potential Savings: Calculate the potential savings if recommendations are followed.
    Customer Impact: Describe how changes will affect the customer experience.
    Visualizations: Display relevant charts (pie chart, bar chart, line chart, scatter plot).
    Guidelines
    Ensure that the output is concise but thorough, with clear explanations for each recommendation.
    The analysis should focus on reducing costs without compromising customer satisfaction.
    Make sure that your final recommendations are actionable and directly tied to the provided input data.

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
            "business_model": ["B2B", "B2C", "D2C", "B2B2C", "Marketplace"],
            "customer_segments": [
                "Wholesale",
                "Retail",
                "Online",
                "Direct-to-Consumer",
                "Subscription",
            ],
            "user_goals": [
                "Reduce Cost-to-Serve",
                "Improve Margins",
                "Increase Efficiency",
                "Optimize Logistics",
                "Enhance Customer Experience",
            ],
            "challenges": [
                "High Delivery Costs",
                "Inefficient Warehousing",
                "Complex Distribution Channels",
                "Low Order Volumes",
                "High Return Rates",
            ],
            "industry_type": [
                "Fashion",
                "Tech",
                "FMCG",
                "Automotive",
                "Healthcare",
                "Retail",
                "Manufacturing",
                "Food & Beverage",
            ],
            "geographical_scope": [
                "Global",
                "North America",
                "Europe",
                "Asia",
                "South America",
                "Africa",
            ],
            "time_horizon": ["Short-term", "Long-term", "Medium-term"],
        },
    }
}
