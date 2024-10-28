import json
from pydantic import BaseModel
from .custom_types.base_types import Plot, ComparisonPlot
from pydantic import BaseModel
from typing import List


class ParcelFlowInputParams(BaseModel):
    volume: str
    season: str
    type:   str
    weatherCondition: str
    staffAvailability: str
    priorityLevel: str


class DelayPrediction(BaseModel):
    delayAllowance: float  # Predicted delay in days
    onTimeDeliveryProbability: float  # Percentage likelihood of on-time delivery


class RiskLevel(BaseModel):
    parcelType: str  # Type of parcel, e.g., "fragile", "perishable"
    riskDescription: str


class ParcelFlowAnalysisResults(BaseModel):
    processingStage: Plot  # Distribution of parcels across processing stages
    bottleneckIndicators: List[str]  # Descriptions of identified bottlenecks
    delayPrediction: DelayPrediction  # Delay estimation and on-time delivery probability
    riskLevelsByParcelType: Plot  # Risk levels by parcel type
    timePeriod: Plot  # Parcel distribution over time
    bottleneckImpact: Plot  # Impact severity of bottlenecks by stage
    recommendations: List[str]  # Actionable suggestions
    volumeImpactAnalysis: Plot  # Correlation between parcel volume and delays
    seasonalRiskTrends: Plot  # Seasonal trends for risk levels by parcel type
    staffUtilization: Plot  # Staff utilization at each processing stage
    costEfficiency: str  # Insights on cost-effectiveness and potential savings


def parcel_flow_prompt(inputParameters: ParcelFlowInputParams):

    knowledge_file = open("data/parcel_flow.json", "r")
    knowledge = json.loads(knowledge_file.read())
    knowledge_file.close()

    system_prompt = (
        """
    You are an assistant for a shipping community called the Parcel Flow Tool.
    Your specialty lies in analyzing the flow of parcels based on user-provided inputs, and your task is to generate actionable recommendations for optimizing the parcel flow process.

    Strictly use the following data as the foundation for your analysis:
    """
        + json.dumps(knowledge, indent=4) +
        """

    **Output Format:**

    Your output should include the following fields, each with specific details:

    - `processingStage`: 
        - **Chart Type**: "barChart"
        - **Description**: Display the time taken by each stage in the parcel processing workflow (e.g., Intake, Sorting, Dispatch, Delivery Handover), shown on a fixed time scale (e.g., hours or days).
        - **Data**: Include labels for each stage, with corresponding values representing the time taken in a consistent unit (e.g., "hours"). This allows for a straightforward comparison of each stage's processing time.
        - **Goal**: This chart helps identify which stages are more time-intensive, highlighting stages that may contribute to overall delays in the process.
        - **Explaination**: Explain the insights gained from the chart.

    - `bottleneckIndicators`: 
        - **Format**: List of strings.
        - **Description**: Outline specific bottlenecks detected within the process. These should highlight stages or factors causing delays (e.g., "Sorting backlog due to reduced staff" or "Dispatch delays due to truck shortage").
        - **Goal**: Each bottleneck should provide a clear and concise description of the issue and the affected stage.

    - `delayPrediction`: 
        - **Format**: Text-based.
        - **Description**: Provide an estimated delay allowance (in days) based on processing and transit conditions, alongside a percentage-based likelihood of on-time delivery (e.g., "Expected delay: 2.5 days, On-time Delivery Probability: 75%").
        - **Goal**: This field should give users an accurate sense of potential delays, allowing them to gauge delivery timelines.

    - `riskLevelsByParcelType`: 
        - **Chart Type**: "pieChart"
        - **Description**: Visualize the risk level for each parcel type, such as fragile, high-value, and perishable items. Include labels with risk categories and values showing each type’s proportion of total risk.
        - **Goal**: This chart should make it easy to see which parcel types are at higher risk, helping to prioritize handling and mitigation.
        - **Explaination**: Explain the insights gained from the chart.

    - `timePeriod`: 
        - **Chart Type**: "lineChart"
        - **Description**: Show parcel distribution over time, indicating fluctuations in volume or demand throughout a given timeframe (e.g., weekly or monthly basis). Include labels for each time period and corresponding values for parcel counts.
        - **Goal**: This chart highlights seasonal trends or surges, allowing for proactive adjustments in staffing or resources.
        - **Explaination**: Explain the insights gained from the chart.

    - `bottleneckImpact`: 
        - **Chart Type**: "barChart"
        - **Description**: Display the severity of bottlenecks at each processing stage. Label each stage with a severity score, showing how bottlenecks impact overall flow (e.g., Intake: 1.5, Sorting: 3.0, etc.).
        - **Goal**: This visualization should provide a clear overview of which stages require intervention, helping focus resources on the most critical areas.
        - **Explaination**: Explain the insights gained from the chart.

    - `recommendations`: 
        - **Format**: List of actionable strings.
        - **Description**: Provide specific recommendations for optimizing parcel flow. These might include suggestions to adjust staffing, add equipment, or alter scheduling (e.g., "Increase dispatch staff by 15% during peak hours" or "Use temperature-controlled trucks for perishable items in summer months").
        - **Goal**: Recommendations should be practical and directly address the identified bottlenecks or risks to improve overall efficiency.

    - `volumeImpactAnalysis`: 
        - **Chart Type**: "lineChart"
        - **Description**: Displays parcel volume over time, highlighting any correlation between volume changes and processing times or delays.
        - **Goal**: This chart can reveal the effect of increased or decreased parcel volume on flow efficiency, helping adjust resources accordingly.
        - **Explaination**: Explain the insights gained from the chart.

    - `seasonalRiskTrends`: 
        - **Chart Type**: "lineChart"
        - **Description**: Illustrates how risk levels for different parcel types fluctuate by season, such as higher risk for temperature-sensitive goods in summer.
        - **Goal**: Allows users to prepare for season-specific risks with targeted resources or strategies.
        - **Explaination**: Explain the insights gained from the chart.

    - `staffUtilization`: 
        - **Chart Type**: "barChart"
        - **Description**: Shows the current level of staff utilization at each stage (e.g., Intake, Sorting) and highlights areas where staffing is under or over-utilized.
        - **Goal**: Assists in balancing workload with staff resources to prevent delays caused by staff shortages or overburdening.
        - **Explaination**: Explain the insights gained from the chart.

    - `costEfficiency`: 
        - **Format**: Text-based.
        - **Description**: Provides insights into how efficiently resources (staff, equipment) are being used relative to parcel volume and delays (e.g., "Current resource utilization: 85%, estimated cost savings if optimized: 10%").
        - **Goal**: Gives an overview of cost efficiency to help streamline operations and reduce expenses.


    **Note:**
    Only use the following chart types: ["barChart", "lineChart", "pieChart"]. Ensure that each chart provides clear insights into the specific area of parcel flow it represents.
    """
    )

    user_prompt = (
        """
        I need you to analyze the parcel flow process based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "parcel-flow": {
        "prompt_func": parcel_flow_prompt,
        "response_format": ParcelFlowAnalysisResults,
        "input_format": ParcelFlowInputParams,
        "options": {
            "volume": ["Low", "Medium", "High"],
            "priorityLevel": ["High", "Medium", "Low"],
            "weatherConditions": ["Clear", "Rain", "Snow", "Fogg", "Storm"],
        }
    }
}
