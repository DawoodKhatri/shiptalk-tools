import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot
import random


class ThirdPartyLogisticsInputParamsType(BaseModel):
    company_size: str  # Options: 'Small', 'Medium', 'Large'
    logistics_functions_to_outsource: List[
        str
    ]  # E.g., ['Warehousing', 'Transportation']
    geographic_regions: List[str]  # E.g., ['North America', 'Europe']
    types_of_products: List[str]  # E.g., ['Electronics', 'Perishable Goods']
    shipment_volume_per_month: int
    user_objectives: List[str]  # E.g., ['Cost Reduction', 'Scalability']
    constraints: List[str] = (
        None  # E.g., ['Budget Limitations', 'Regulatory Compliance']
    )
    current_challenges: List[str] = (
        None  # E.g., ['High Inventory Costs', 'Slow Delivery Times']
    )


class KeyPerformanceIndicator(BaseModel):
    kpi_name: str  # E.g., 'Order Fulfillment Time', 'Inventory Turnover Rate'
    current_value: float
    expected_improvement_percentage: float


class RiskAnalysis(BaseModel):
    risk_description: str
    mitigation_suggestion: str


class ThirdPartyLogisticsAnalysisResults(BaseModel):
    suggested_providers: List[str]
    estimated_cost_savings_percentage: float
    expected_improvement_in_service_levels: (
        str  # E.g., 'Improved delivery times by 20%'
    )
    key_performance_indicators: List[KeyPerformanceIndicator]
    implementation_plan: List[str]
    risk_analysis: List[RiskAnalysis]
    key_considerations: List[str]
    charts: List[Plot]
    success_stories: str = None  # Optional field to provide case studies or examples
    overall_suggestion: str  # Theoretical strategic suggestion


def third_party_logistics_prompt(
    inputParameters: ThirdPartyLogisticsInputParamsType,
):
    # Generate random data for example charts
    pieChart = random.randint(1, 3)
    barChart = random.randint(1, 3)
    lineChart = random.randint(1, 3)
    totalCharts = pieChart + barChart + lineChart

    # Pass the JSON schema of the input parameters to provide context about the input structure
    system_prompt = """
You are an AI assistant specializing in logistics and supply chain optimization.
Your task is to analyze the user's logistics requirements and provide actionable insights
to help them find suitable third-party logistics (3PL) providers to outsource their logistics functions.

### *User Objectives and Priorities*
Before starting your analysis, please consider the user's primary goals. The user may specify their main objectives such as:
- Cost reduction
- Scalability
- Improved service levels
- Access to advanced technology
- Focus on core competencies
- Other specific priorities

Tailor your recommendations to align with these objectives.

### *Input Structure*
Here is the expected structure of the input data:
{json_schema}

### *Visualization Types*
Please generate relevant visualizations to support your analysis. The possible chart types are:
- **barChart**: Displays categorical data with rectangular bars.
- **pieChart**: Represents parts of a whole as pie slices.
- **lineChart**: Shows data trends over time or continuous variables.
- **areaChart**: Similar to a line chart, but with filled areas to represent quantities.
- **scatterPlot**: Displays values for typically two variables for a set of data.
- **heatMap**: Represents data values as colors in a matrix.

### *Instructions*
Analyze the provided data to recommend optimal third-party logistics providers and strategies. Ensure the following:
- Identify cost-saving opportunities and service level improvements.
- Suggest 3PL providers that match the user's logistics functions to outsource, geographic regions, and other requirements.
- Include exactly {totalCharts} visualizations in your analysis: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s).
- Provide a theoretical overall suggestion to improve logistics operations.
- Identify key performance indicators (KPIs) relevant to outsourcing logistics and measure the impact of your recommendations on these KPIs.
- Consider practical constraints such as budget limits, resource availability, or regulatory requirements.
- Account for regional differences in logistics infrastructure or provider availability.
- Explore innovative solutions like technology integration, automation, or value-added services if applicable.
- Assess potential risks associated with the recommended strategies and suggest ways to mitigate them.

### *Implementation Roadmap*
Provide a step-by-step plan on how to implement the suggested strategies. This should include actionable steps that the user can follow.

### *Success Stories or Case Studies*
Include examples of how similar strategies have benefited other companies, if possible but not mandatory. A real-world context can help reinforce the recommendations.

### *Output Formatting Guidelines*
Please structure your output in the following format:

1. **Introduction**: Briefly summarize the key findings.
2. **User Objectives Alignment**: Explain how your recommendations align with the user's specified objectives.
3. **Recommendations**:
   - List recommended 3PL providers or strategies.
   - Provide estimated cost savings as a percentage.
   - Describe expected improvements in service levels.
4. **Key Performance Indicators (KPIs)**:
   - Identify relevant KPIs.
   - Explain how the recommendations impact these KPIs.
5. **Implementation Roadmap**:
   - Step-by-step plan to implement the strategies.
6. **Risk Analysis**:
   - Assess potential risks.
   - Suggest mitigation strategies.
7. **Key Considerations**:
   - Highlight important factors to consider when outsourcing to 3PL providers.
8. **Visualizations**:
   - Include the specified number of visual charts ({totalCharts} charts: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s)) to represent insights.
9. **Success Stories or Case Studies**:
   - Provide examples where similar strategies have been successful.
10. **Conclusion**:
    - Offer a general theoretical recommendation for improving logistics operations through 3PL partnerships.
11. **Feedback Prompt**:
    - Ask the user if further clarification or additional analysis is needed.

### *Output Requirements*
The output should contain the following elements:
- Only provide factual information based on your knowledge base.
- Recommended 3PL providers or strategies, tailored to the user's objectives.
- Estimated cost savings as a percentage.
- Expected improvements in service levels.
- Identification of key performance indicators (KPIs) and how the recommendations impact them.
- A step-by-step implementation plan.
- A risk assessment of the recommended strategies.
- Key considerations when outsourcing logistics functions.
- Include the specified number of visual charts ({totalCharts} charts: {pieChart} pie chart(s), {barChart} bar chart(s), and {lineChart} line chart(s)) to represent insights.
- Examples or case studies where similar strategies have been successful.
- A general theoretical recommendation for improving logistics operations through 3PL partnerships.
""".format(
        json_schema=ThirdPartyLogisticsInputParamsType,
        totalCharts=totalCharts,
        pieChart=pieChart,
        barChart=barChart,
        lineChart=lineChart,
    )

    user_prompt = "Please analyze the following data:\n" + json.dumps(
        inputParameters.model_dump(), indent=4
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "third-party-logistics": {
        "prompt_func": third_party_logistics_prompt,
        "response_format": ThirdPartyLogisticsAnalysisResults,
        "input_format": ThirdPartyLogisticsInputParamsType,
        "options": {
            "company_size": ["Small", "Medium", "Large"],
            "logistics_functions_to_outsource": [
                "Warehousing",
                "Transportation",
                "Inventory Management",
                "Order Fulfillment",
                "Customs Brokerage",
                "Freight Forwarding",
                "Reverse Logistics",
                "Distribution",
            ],
            "types_of_products": [
                "Electronics",
                "Perishable Goods",
                "Fragile Items",
                "High-Value Products",
                "Oversized & Heavy Items",
                "Temperature-Sensitive Goods",
                "Standard Retail Products",
                "Medical Supplies & Pharmaceuticals",
            ],
            "user_objectives": [
                "Cost Reduction",
                "Scalability",
                "Improved Service Levels",
                "Access to Advanced Technology",
                "Focus on Core Competencies",
                "Operational Efficiency",
                "Enhanced Tracking & Visibility",
            ],
            "constraints": [
                "Budget Limitations",
                "Regulatory Compliance",
                "Limited Resources",
                "Tight Timelines",
                "Data Security Requirements",
                "Customer Service Expectations",
            ],
            "current_challenges": [
                "High Inventory Costs",
                "Slow Delivery Times",
                "Inaccurate Order Fulfillment",
                "Lack of Scalability",
                "Inefficient Processes",
                "High Return Rates",
            ],
            "geographic_regions": [
                "North America",
                "Europe",
                "Asia-Pacific",
                "Latin America",
                "Middle East",
                "Africa",
            ],
        },
    }
}
