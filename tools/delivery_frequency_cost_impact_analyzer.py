import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot, ComparisonPlot


class FrequencyCostInputParams(BaseModel):
    deliveryFrequency: int  # Number of deliveries per week (e.g., 1 for weekly, 7 for daily)
    averageParcelCost: float  # Average cost per parcel for delivery
    routeDistance: float  # Distance covered per delivery route in kilometers
    urgencyLevel: str  # Urgency level of delivery (e.g., "Standard", "Express", "Critical")


class CostImpactAnalysis(BaseModel):
    frequency: int  # Delivery frequency level
    totalCost: float  # Total cost at this frequency level
    costDifference: float  # Cost change from previous frequency level
    savingsPotential: float  # Estimated cost savings by adjusting frequency
    averageCostPerParcel: float  # Average cost per parcel for this frequency level
    totalDistanceCovered: float  # Total distance covered at this frequency level


class FinancialSummary(BaseModel):
    weeklySavings: float  # Estimated weekly savings at optimal frequency
    monthlySavings: float  # Estimated monthly savings at optimal frequency
    annualSavings: float  # Estimated annual savings at optimal frequency


class UrgencyImpactAssessment(BaseModel):
    urgencyLevel: str  # Urgency level (e.g., "Standard", "Express", "Critical")
    suggestedFrequency: int  # Recommended delivery frequency for the given urgency level
    description: str  # Description of why this frequency is optimal for the urgency level


class DeliveryFrequencyCostImpactOutput(BaseModel):
    frequencyCostBreakdown: List[CostImpactAnalysis]  # Cost breakdown across frequency levels
    optimalFrequency: int  # Suggested delivery frequency for cost optimization
    totalCostEstimation: float  # Total cost estimation at optimal frequency
    savingsEstimation: float  # Estimated savings at optimal frequency
    frequencyCostAnalysis: Plot  # Bar chart showing cost impact across different frequency levels
    savingsPotentialAnalysis: Plot  # Line chart showing potential savings by frequency adjustment
    averageCostPerParcelTrend: Plot  # Line chart showing trend of average cost per parcel
    distanceCoverageAnalysis: Plot  # Bar chart showing distance covered per frequency level
    recommendations: List[str]  # Actionable recommendations for adjusting delivery frequency
    keyInsights: List[str]  # High-level insights from the analysis
    financialSummary: FinancialSummary  # Summary of potential weekly, monthly, and annual savings
    urgencyImpactAssessment: List[UrgencyImpactAssessment]  # Suggested frequency recommendations based on urgency level


def delivery_frequency_cost_impact_analyzer_prompt(inputParameters: FrequencyCostInputParams):

    system_prompt = (
        """
    You are an assistant for a shipping community tool called the Delivery Frequency Cost Impact Analyzer.
    Your role is to assess the cost implications of adjusting delivery frequency, allowing users to see the financial impact of different intervals.

    **Output Format:**

    Your output should include the following fields, each with specific details:

    - `frequencyCostBreakdown`: 
        - **Format**: List of `CostImpactAnalysis` objects.
        - **Description**: Break down delivery costs across frequency levels, showing cost differences and potential savings.
        - **Goal**: Compare costs at different frequencies to find savings opportunities.

    - `optimalFrequency`: 
        - **Format**: Integer.
        - **Description**: Suggested delivery frequency for optimal cost savings.
        - **Goal**: Helps users identify a cost-effective delivery frequency.

    - `totalCostEstimation`: 
        - **Format**: Float.
        - **Description**: Total delivery cost estimate at the optimal frequency.
        - **Goal**: Provides an overview of costs at the recommended frequency.

    - `savingsEstimation`: 
        - **Format**: Float.
        - **Description**: Estimated savings achieved by adjusting to the optimal frequency.
        - **Goal**: Shows potential cost reductions.

    - `frequencyCostAnalysis`: 
        - **Chart Type**: "barChart"
        - **Description**: Displays total cost across delivery frequencies.
        - **Goal**: Visualize costs per frequency for better decision-making.

    - `savingsPotentialAnalysis`: 
        - **Chart Type**: "lineChart"
        - **Description**: Shows potential savings as delivery frequency is adjusted.
        - **Goal**: Illustrates where savings peak and diminish.

    - `averageCostPerParcelTrend`: 
        - **Chart Type**: "lineChart"
        - **Description**: Shows average parcel cost trends at each frequency.
        - **Goal**: Provides insights into cost efficiency per parcel.

    - `distanceCoverageAnalysis`: 
        - **Chart Type**: "barChart"
        - **Description**: Total distance covered for each delivery frequency.
        - **Goal**: Shows logistics impact by frequency.

    - `recommendations`: 
        - **Format**: List of strings.
        - **Description**: Practical advice for adjusting frequency to minimize costs.
        - **Goal**: Helps users reduce delivery costs.

    - `keyInsights`: 
        - **Format**: List of strings.
        - **Description**: Key observations from the analysis.
        - **Goal**: Summarizes high-level insights for quick review.

    - `financialSummary`: 
        - **Format**: `FinancialSummary` object.
        - **Description**: Weekly, monthly, and annual savings estimates.
        - **Goal**: Overview of long-term financial benefits.

    - `urgencyImpactAssessment`: 
        - **Format**: List of `UrgencyImpactAssessment` objects.
        - **Description**: Recommended frequency by urgency level.
        - **Goal**: Aligns delivery frequency with urgency requirements.

    **Note:**
    Only use ["barChart", "lineChart"] for visualizations. Each chart should offer clear insights into cost impact by frequency.
    """
    )
    
    user_prompt = (
        """
    I need an analysis of delivery frequency cost impact based on these inputs:

    **Input Parameters:**
    - `deliveryFrequency`: 
        - **Format**: Integer.
        - **Description**: Number of deliveries per week, e.g., 1 for weekly, 7 for daily.

    - `averageParcelCost`: 
        - **Format**: Float.
        - **Description**: Average cost per parcel for delivery.

    - `routeDistance`: 
        - **Format**: Float.
        - **Description**: Distance covered per delivery route in kilometers.

    - `urgencyLevel`: 
        - **Format**: String.
        - **Description**: Urgency level, e.g., "Standard," "Express," or "Critical," affecting frequency.

    Provide a detailed analysis on cost impact across frequencies, and recommend an optimal frequency for cost and urgency.
    """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "delivery-frequency-cost-impact-analyzer": {
        "prompt_func": delivery_frequency_cost_impact_analyzer_prompt,
        "response_format": DeliveryFrequencyCostImpactOutput,
        "input_format": FrequencyCostInputParams,
        "options": {
            "urgencyLevel": ["Standard", "Express", "Critical"]
        }
    }
}
