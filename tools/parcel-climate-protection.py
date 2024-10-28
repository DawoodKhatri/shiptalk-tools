import json
from pydantic import BaseModel
from .custom_types.base_types import Plot, ComparisonPlot
from pydantic import BaseModel
from typing import List


class ParcelClimateProtectionInputParams(BaseModel):
    # Type of product (e.g., "Electronics", "Pharmaceuticals", "Textiles")
    productType: str
    # Climate condition affecting the shipment (e.g., "Extreme Heat", "High Humidity")
    climateCondition: str
    # Sensitivity of the parcel (e.g., "High", "Moderate", "Low")
    sensitivityLevel: str
    # Available carrier options with specific climate-handling capabilities
    carrierOptions: List[str]
    # Urgency for delivery (e.g., "Standard", "Express", "Same-Day")
    urgencyLevel: str


class SpecificationItem(BaseModel):
    name: str  # e.g., "Insulation Rating"
    value: str  # e.g., "R-12"


class PackagingRecommendation(BaseModel):
    name: str
    cost: float
    specifications: List[SpecificationItem]


class CarrierComparison(BaseModel):
    name: str
    rating: float
    capabilities: List[str]
    costPremium: float


class ParcelClimateProtectionAnalysisResults(BaseModel):
    climateRiskAssessment: str  # Summary of the climate-related risks
    # List of recommended packaging solutions with details
    packagingRecommendations: List[PackagingRecommendation]
    # Comparison of suitable carriers with ratings and cost premiums
    carrierComparisons: List[CarrierComparison]
    # Real-time alerts for immediate actions or adjustments needed
    realTimeAlerts: List[str]
    # Chart comparing costs of packaging options based on climate conditions
    packagingCostAnalysis: Plot
    # Bar chart showing the capability comparison among carrier options
    carrierCapabilityAnalysis: Plot
    # Prediction of impact on parcel quality and estimated risk if shipped under input conditions
    transitImpactPrediction: str
    # A pie chart representing the adaptability score for each carrier option, based on climate-handling capabilities
    climateAdaptabilityScore: Plot


def parcel_climate_protection_prompt(inputParameters: ParcelClimateProtectionInputParams):

    knowledge_file = open("data/climate.json", "r")
    knowledge = json.loads(knowledge_file.read())
    knowledge_file.close()

    system_prompt = (
        """
    You are an assistant for a shipping community called the Parcel Climate Protection Monitor.
    Your specialty lies in assessing climate-related risks for sensitive parcels based on user inputs.
    Your task is to generate recommendations for safe transit, considering climate conditions, packaging, and carrier options to protect perishable or fragile items.

    Strictly use the following data as the foundation for your analysis:
    """
        + json.dumps(knowledge, indent=4) +
        """

    **Output Format:**

    Your output should include the following fields, each with specific details:

    - `climateRiskAssessment`: 
        - **Format**: Text-based.
        - **Description**: Summarize the climate-related risks posed to the parcel under current weather conditions, referencing temperature, humidity, and other climate factors.
        - **Goal**: To provide a clear understanding of the primary risks (e.g., “High spoilage risk due to extreme heat for perishable goods”).

    - `packagingRecommendations`: 
        - **Format**: List of `PackagingRecommendation` objects.
        - **Description**: Provide recommended packaging solutions tailored to climate conditions, including names, costs, and specifications (e.g., insulation rating, temperature maintenance duration).
        - **Goal**: Guide the user toward effective packaging choices to safeguard against climate risks.

    - `carrierComparisons`: 
        - **Format**: List of `CarrierComparison` objects.
        - **Description**: Suggest suitable carriers with specific climate-handling capabilities. Each carrier should have a rating, capabilities, and any additional cost premium.
        - **Goal**: Help users select the most effective carrier based on climate protection capabilities.

    - `realTimeAlerts`: 
        - **Format**: List of alert strings.
        - **Description**: Provide actionable alerts, such as urgent handling instructions or warnings about potential delays.
        - **Goal**: Immediate feedback for climate-sensitive situations that require special handling or rerouting.

    - `packagingCostAnalysis`: 
        - **Chart Type**: "barChart"
        - **Description**: Show cost comparisons for different packaging options recommended based on climate conditions.
        - **Goal**: Assist in selecting cost-effective packaging that still provides adequate protection against climate-related risks.
        - **Explaination**: Include insights gained from the cost breakdown.

    - `carrierCapabilityAnalysis`: 
        - **Chart Type**: "barChart"
        - **Description**: Compare climate-specific capabilities of various carriers. Include labels for each carrier and values showing capability ratings or effectiveness.
        - **Goal**: Assist users in identifying carriers best equipped to handle parcels under specific climate risks.
        - **Explaination**: Summarize insights on the strengths of each carrier.

    - `transitImpactPrediction`: 
        - **Format**: Text-based.
        - **Description**: Predict the impact of current climate conditions on parcel quality, including risk estimates for spoilage or damage if the parcel is shipped under input conditions.
        - **Goal**: Provide a realistic expectation of transit effects to guide users in decision-making.

    - `climateAdaptabilityScore`: 
        - **Chart Type**: "pieChart"
        - **Description**: Display adaptability scores for each carrier, representing how well each carrier can handle climate risks.
        - **Goal**: Give users a quick view of carrier options best suited for climate-sensitive shipping.
        - **Explaination**: Explain how adaptability scores reflect the carrier's capabilities.

    - `seasonalRiskTrends`: 
        - **Chart Type**: "lineChart"
        - **Description**: Display risk level changes by season for different parcel types (e.g., higher risk for temperature-sensitive items in summer).
        - **Goal**: Enable users to plan for season-specific risks, preparing adequate resources or strategies.
        - **Explaination**: Summarize insights from seasonal variations.

    **Note:**
    Only use the following chart types: ["barChart", "lineChart", "pieChart"]. Ensure each chart provides clear insights into the specific area of parcel climate protection it represents.
    """
    )

    user_prompt = (
        """
        I need you to analyze the climate protection requirements based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "parcel-climate-protection": {
        "prompt_func": parcel_climate_protection_prompt,
        "response_format": ParcelClimateProtectionAnalysisResults,
        "input_format": ParcelClimateProtectionInputParams,
        "options": {
            "sensitivityLevel": ["High", "Moderate", "Low"],
            "climateCondition": ["Clear", "Rain", "Snow", "Fogg", "Storm"],
            "urgencyLevel": ["Standard", "Express", "Same-Day"],
        }
    }
}
