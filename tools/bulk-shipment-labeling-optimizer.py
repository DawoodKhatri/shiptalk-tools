import json
from pydantic import BaseModel
from typing import List
from .custom_types.base_types import Plot

class BulkShipmentLabelingInputParams(BaseModel):
    # Type of product based on product dimensions and weight (small, medium, large)
    packageSize: str
    # Carrier being used for shipment (e.g., FedEx, UPS, DHL)
    carrier: str
    # Number of labels needed for the bulk shipment
    numberOfLabels: int
    # Shipping type for compliance guidelines (e.g., domesticShipping, internationalShipping)
    shippingType: str

class CarrierLabelRequirements(BaseModel):
    mandatoryFields: List[str]  # Required fields for carrier label
    labelSize: str  # Label size requirement by carrier
    placementNote: str  # Specific placement instructions for the label

class PackagingRecommendation(BaseModel):
    material: str  # e.g., "Cardboard" or "Plastic"
    adhesionLevel: str  # Level of adhesion required for the label
    recommendedLabelType: str  # Type of label recommended based on packaging material

class LabelCostEstimate(BaseModel):
    materialType: str  # Label material type (e.g., "thermalPaper")
    costPerLabel: float  # Cost per label for the selected material
    discountApplied: float  # Discount percentage based on bulk quantity
    totalCost: float  # Total cost after discount

class ComplianceWarnings(BaseModel):
    shippingType: str  # Type of shipping (e.g., "domesticShipping")
    warnings: List[str]  # Compliance warnings for the specific shipping type

class BulkShipmentLabelingAnalysisResults(BaseModel):
    carrierLabelRequirements: CarrierLabelRequirements  # Carrier-specific labeling requirements
    packagingRecommendations: List[PackagingRecommendation]  # Suggested packaging materials and adhesion details
    labelCostEstimate: LabelCostEstimate  # Estimated cost per label and total cost with bulk discount
    complianceWarnings: ComplianceWarnings  # Compliance guidelines for domestic or international shipping
    bulkLabelCostComparison: Plot  # Comparison plot for cost based on label material and quantity
    durabilityImpactAnalysis: Plot  # Chart showing durability impact of different label materials
    labelingEfficiencyTips: List[str]  # Tips to streamline labeling process and reduce errors
    seasonalAdjustmentRecommendations: str  # Recommendations for labeling adjustments based on seasonality
    operationalEfficiencyScore: float  # A score indicating overall labeling process efficiency

def bulk_shipment_labeling_optimizer_prompt(inputParameters: BulkShipmentLabelingInputParams):

    knowledge_file = open("data/labeling.json", "r")
    knowledge = json.loads(knowledge_file.read())
    knowledge_file.close()

    system_prompt = (
        """
    You are an assistant for a shipping community called the Bulk Shipment Labeling Optimizer.
    Your expertise lies in suggesting efficient labeling strategies for bulk shipments, focusing on reducing labeling costs, adhering to carrier-specific requirements, and optimizing operational efficiency.

    Strictly use the following data as the basis for your analysis:
    """
        + json.dumps(knowledge, indent=4) +
        """

    **Output Format:**

    - `Carrier Label Requirements`: 
        - **Format**: `CarrierLabelRequirements` object.
        - **Description**: Specifies mandatory fields, label size, and placement instructions for the carrier.
        - **Goal**: Ensure compliance with carrier-specific labeling standards.
            - `Mandatory Fields`: List of strings in human-readable form, using natural language capitalization.

    - `Packaging Recommendations`: 
        - **Format**: List of `PackagingRecommendation` objects.
        - **Description**: Recommended packaging materials and adhesion details based on product type.
        - **Goal**: Ensure that labels adhere effectively to the selected packaging materials.
            - `Material`: String in human-readable form, using natural language capitalization.
            - `Adhesion Level`: String in human-readable form, using natural language capitalization.
            - `Recommended Label Type`: String in human-readable form, using natural language capitalization.

    - `Label Cost Estimate`: 
        - **Format**: `LabelCostEstimate` object.
        - **Description**: Cost per label, discount applied, and total cost based on bulk quantity.
        - **Goal**: Provide users with a clear estimate of labeling costs, including any bulk discounts.
            - `Material Type`: String in human-readable form, using natural language capitalization.

    - `Compliance Warnings`: 
        - **Format**: `ComplianceWarnings` object.
        - **Description**: Compliance warnings for the selected shipping type (domestic or international).
        - **Goal**: Ensure that all mandatory fields and guidelines are met for compliance.

    - `Bulk Label Cost Comparison`: 
        - **Chart Type**: "barChart"
        - **Description**: Compare costs based on label material and quantity, illustrating the impact of bulk discounts.
        - **Goal**: Aid users in selecting cost-effective labeling options.

    - `Durability Impact Analysis`: 
        - **Chart Type**: "barChart"
        - **Description**: Display durability comparison across different label materials.
        - **Goal**: Help users understand how different materials withstand varying shipping conditions.

    - `Labeling Efficiency Tips`: 
        - **Format**: List of strings.
        - **Description**: Practical tips to improve labeling efficiency and reduce errors.
        - **Goal**: Streamline labeling processes for better operational outcomes.

    - `Seasonal Adjustment Recommendations`: 
        - **Format**: Text-based.
        - **Description**: Recommendations for labeling adjustments based on seasonal trends.
        - **Goal**: Ensure that labeling remains effective under different seasonal conditions.

    - `Operational Efficiency Score`: 
        - **Format**: Float (0-100).
        - **Description**: An efficiency score indicating the optimization level of the labeling process.
        - **Goal**: Give users a quantitative measure of their labeling process's efficiency.

    **Note:** 
    
    - Use only the specified chart types ["barChart"]. Each output should be in human-readable form, providing clear, actionable insights into efficient labeling strategies for high-volume shipments.
    
    
    """
    )

    user_prompt = (
        """
        Analyze the labeling optimization requirements based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "bulk-shipment-labeling-optimizer": {
        "prompt_func": bulk_shipment_labeling_optimizer_prompt,
        "response_format": BulkShipmentLabelingAnalysisResults,
        "input_format": BulkShipmentLabelingInputParams,
        "options": {
            "packageSize": ["Small", "Medium", "Large"],
            "shippingType": ["Domestic Shipping", "International Shipping"]
        }
    }
}
