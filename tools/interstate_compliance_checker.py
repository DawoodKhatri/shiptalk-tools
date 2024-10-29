from pydantic import BaseModel
from typing import List, Optional
import json
from .custom_types.base_types import Plot, ComparisonPlot

class RestrictedItem(BaseModel):
    item: str
    ageVerificationRequired: Optional[bool]
    carrierRestrictions: Optional[List[str]]
    documentationRequired: Optional[List[str]]
    labelingRequirements: Optional[str]
    shippingRestrictions: Optional[str]

class DocumentationRequirement(BaseModel):
    item: str
    requiredDocuments: List[str]

class TaxAndFee(BaseModel):
    category: str
    items: List[str]

class PackagingLabel(BaseModel):
    item: str
    requirement: str

class CarrierRestriction(BaseModel):
    carrier: str
    restriction: str
    reason: str

class StateCompliance(BaseModel):
    prohibitedItems: List[str]
    restrictedItems: List[RestrictedItem]
    documentationRequirements: List[DocumentationRequirement]
    taxesAndFees: List[TaxAndFee]
    packagingLabeling: List[PackagingLabel]
    specialNotes: str

class ComplianceInputParams(BaseModel):
    originState: str
    destinationState: str
    itemType: str
    carrierName: Optional[str]

class ComplianceAnalysisResults(BaseModel):
    prohibitionStatus: str
    requiredDocuments: List[str]
    packagingRequirements: List[str]
    applicableFees: List[str]
    carrierRestrictions: List[CarrierRestriction]
    warnings: List[str]
    complianceScore: Plot
    restrictionComparison: Plot
    taxesAndFees: Plot

def compliance_checker_prompt(inputParameters: ComplianceInputParams):
    knowledge_file = open("data/compliance.json", "r")
    knowledge = json.loads(knowledge_file.read())
    knowledge_file.close()

    system_prompt = (
        """
    You are an interstate shipping compliance expert. Your task is to analyze shipping requirements 
    and restrictions between states based on the provided compliance data.

    Strictly use the following compliance data as the foundation for your analysis:
    """
        + json.dumps(knowledge, indent=4) +
        """

    **Output Format:**

    Your output should include the following fields:

    - `prohibitionStatus`: Detailed explanation of any prohibitions
    - `requiredDocuments`: List of all required documentation for shipping the given product
    - `packagingRequirements`: List of packaging and labeling requirements for the given product
    - `applicableFees`: List of applicable taxes and fees to ship the given product
    - `carrierRestrictions`: List of carrier-specific restrictions 
    - `warnings`: List of important compliance warnings
    - `complianceScore`: Chart showing overall compliance status
    - `restrictionComparison`: Chart comparing restrictions between states
    - `taxesAndFees`: Chart showing taxes and fees completeness

    **Note:**
    Only use the following chart types: ["barChart", "lineChart", "pieChart"]
    """
    )

    user_prompt = (
        """
        Please analyze the shipping compliance requirements for:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages

tool_config = {
    "interstate-compliance-checker": {
        "prompt_func": compliance_checker_prompt,
        "response_format": ComplianceAnalysisResults,
        "input_format": ComplianceInputParams,
        "options": {
            "originState": ["California", "Texas", "Florida"]
        }
    }
}
