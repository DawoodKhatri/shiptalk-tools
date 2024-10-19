import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot
import random

class LastMileDeliverySolutionsInputParamsType(BaseModel):
    daily_orders: int
    average_delivery_distance_km: float
    delivery_locations: List[str]
    current_delivery_method: str  # Options: 'own fleet', 'third-party', 'mixed'
    average_delivery_time_minutes: float
    user_objectives: List[str]  # E.g., ['cost reduction', 'faster delivery', 'customer satisfaction']
    regional_constraints: str = None  # Optional field to capture regional differences or constraints

class KeyPerformanceIndicator(BaseModel):
    kpi_name: str  # E.g., 'Average Delivery Time', 'Cost per Delivery'
    current_value: float
    expected_improvement_percentage: float

class RiskAnalysis(BaseModel):
    risk_description: str
    mitigation_suggestion: str

class LastMileDeliverySolutionsAnalysisResults(BaseModel):
    suggested_couriers: List[str]
    estimated_cost_savings_percentage: float
    expected_delivery_time_reduction_percentage: float
    key_performance_indicators: List[KeyPerformanceIndicator]  # Added to track KPIs
    implementation_plan: List[str]  # Step-by-step suggestions for implementing recommendations
    risk_analysis: List[RiskAnalysis]  # Added to provide risk assessments and mitigations
    overall_suggestion: str  # Theoretical strategic suggestion
    charts: List[Plot]
    success_stories: str = None  # Optional field to provide case studies or examples

def last_mile_delivery_solutions_prompt(
    inputParameters: LastMileDeliverySolutionsInputParamsType,
):
    # Generate random data for example charts
    pieChart = random.randint(1, 3)
    barChart = random.randint(1, 3)
    lineChart = random.randint(1, 3)

    # Pass the JSON schema of the input parameters to provide context about the input structure

    system_prompt = """
    You are an AI assistant specializing in logistics optimization.
    Your task is to analyze the user's last-mile delivery data and provide actionable insights
    that will enhance delivery speed and efficiency, especially when using local couriers.

    ### *User Objectives and Priorities*
    Before starting your analysis, please consider the user's primary goals. The user may specify their main objectives such as:
    - Cost reduction
    - Faster delivery times
    - Enhancing customer satisfaction
    - Environmental sustainability
    - Other specific priorities

    Tailor your recommendations to align with these objectives.

    ### *Input Structure*
    Here is the expected structure of the input data:
    {}

    ### *Visualization Types*
    Please generate relevant visualizations to support your analysis. The possible chart types are:
    - **barChart**: Displays categorical data with rectangular bars.
    - **pieChart**: Represents parts of a whole as pie slices.
    - **lineChart**: Shows data trends over time or continuous variables.
    - **areaChart**: Similar to a line chart, but with filled areas to represent quantities.
    - **scatterPlot**: Displays values for typically two variables for a set of data.
    - **heatMap**: Represents data values as colors in a matrix.

    ### *Instructions*
    Analyze the provided data to recommend optimal last-mile delivery strategies. Ensure the following:
    - Identify cost-saving opportunities and delivery time reductions.
    - Suggest local couriers for optimized delivery based on the input parameters.
    - Include at least one of the visualizations mentioned above to represent the findings visually.
    - Provide a theoretical overall suggestion to improve delivery operations.
    - Identify key performance indicators (KPIs) relevant to last-mile delivery and measure the impact of your recommendations on these KPIs.
    - Consider practical constraints such as budget limits, resource availability, or regional regulations.
    - Account for regional differences in logistics infrastructure or courier availability.
    - Explore innovative solutions like drone delivery or automated lockers if applicable.
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
    - List recommended couriers or delivery strategies.
    - Provide estimated cost savings as a percentage.
    - Provide estimated delivery time reduction as a percentage.
    4. **Key Performance Indicators (KPIs)**:
    - Identify relevant KPIs.
    - Explain how the recommendations impact these KPIs.
    5. **Implementation Roadmap**:
    - Step-by-step plan to implement the strategies.
    6. **Risk Analysis**:
    - Assess potential risks.
    - Suggest mitigation strategies.
    7. **Visualizations**:
    - Include one or more visual charts (bar, pie, line, area, scatterPlot, or heatMap) to represent insights.
    8. **Success Stories or Case Studies**:
    - Provide examples where similar strategies have been successful.
    9. **Conclusion**:
    - Offer a general theoretical recommendation for improving the last-mile delivery process.
    10. **Feedback Prompt**:
        - Ask the user if further clarification or additional analysis is needed.

    ### *Output Requirements*
    The output should contain the following elements:
    - Only provide factual information based on your knowledge base.
    - Recommended couriers or delivery strategies, tailored to the user's objectives.
    - Estimated cost savings as a percentage.
    - Estimated delivery time reduction as a percentage.
    - Identification of key performance indicators (KPIs) and how the recommendations impact them.
    - A step-by-step implementation plan.
    - A risk assessment of the recommended strategies.
    - One or more visual charts (bar, pie, line, area, scatterPlot, or heatMap) to represent insights.
    - Examples or case studies where similar strategies have been successful.
    - A general theoretical recommendation for improving the last-mile delivery process.
    """.format(
        json.dumps(
            LastMileDeliverySolutionsInputParamsType.model_json_schema(), indent=4
        )
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
    "last-mile-delivery-solutions": {
        "prompt_func": last_mile_delivery_solutions_prompt,
        "response_format": LastMileDeliverySolutionsAnalysisResults,
        "input_format": LastMileDeliverySolutionsInputParamsType,
    }
}
