import json
from pydantic import BaseModel
from .custom_types.base_types import Plot, ComparisonPlot
from pydantic import BaseModel


class Truck(BaseModel):
    arrivalTime: str
    loadType: str  # e.g., "Perishable", "Bulk", "Fragile"
    quantity: float  # Units or weight of goods


class OutboundTruck(BaseModel):
    departureTime: str  # Format: "YYYY-MM-DD HH:MM AM/PM"
    capacity: float  # Maximum load capacity of the truck


class CrossDockingInputParams(BaseModel):
    incomingTrucks: list[Truck]  # List of incoming trucks
    outboundTrucks: list[OutboundTruck]  # List of outbound trucks
    docksAvailable: int  # Number of available docks
    laborAvailable: int  # Number of workers available for unloading/loading
    priorityLevel: str  # e.g., "High", "Medium", "Low"
    trafficConditions: str  # e.g., "Light", "Moderate", "Heavy"
    weatherConditions: str  # e.g., "Clear", "Rainy", "Stormy"


class RiskAnalysis(BaseModel):
    riskLevel: str  # Low, Medium, High (risk categorization)
    riskProgress: float  # Numeric representation for progress bar (0-100)
    explanation: str  # Explanation for the risk level


class DeliveryStatus(BaseModel):
    status: str  # e.g., "On Time", "Delayed"
    explanation: str


class CostEfficiency(BaseModel):
    laborEfficiency: str
    dockUtilization: str
    truckCapacityUtilization: str


class CrossDockingAnalysisResults(BaseModel):
    carrierOptimization: Plot  # Using the Plot class for visual data
    dockScheduling: str  # Suggestion
    laborAllocation: Plot  # Pie chart for labor allocation
    riskAssessment: RiskAnalysis  # Markdown formatted risk assessment
    deliveryTimelineComparison: ComparisonPlot  # Line chart for delivery timeline
    deliveryStatus: DeliveryStatus  # Delivery status
    costEfficiency: CostEfficiency  # Cost analysis


def cross_docking_prompt(inputParameters: CrossDockingInputParams):
    knowledge_file = open("data/cross_docking.json", "r")
    knowledge = json.loads(knowledge_file.read())
    knowledge_file.close()

    system_prompt = (
        """
        You are an assistant for a shipping community tool called the Cross-Docking Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing the cross-docking process.

         ## **Objectives**:
         - Minimize storage time for incoming loads.
         - Efficiently allocate labor and dock resources.
         - Optimize the transfer of goods between inbound and outbound trucks based on priority level, traffic, and weather conditions.

         Strictly use the following data as the foundation for your analysis:
        """
        + json.dumps(knowledge, indent=4) +
        """
        
         ## **Instructions**:

         ### Step 1: Analyze Incoming and Outbound Trucks
         - Prioritize load allocation by type (e.g., **Perishable** and **Fragile** items should minimize waiting time).
         - Allocate load quantities to outbound trucks, ensuring efficient use of capacity.

         ### Step 2: Generate Visual Outputs
         - **Carrier Optimization Analysis**:
           - Create a `barChart` to display the load allocated to each outbound truck.
           - Provide an explanation on load distribution and recommendations for balancing.

         - **Dock Scheduling and Labor Allocation**:
           - Assess dock and labor availability for efficient loading/unloading.
           - Display **dock utilization** using a `barChart` and **labor distribution** with a `pieChart`.
           - Offer recommendations for optimal dock scheduling and labor allocation.

         - **Delivery Timeline Comparison**:
           - Compare planned vs. adjusted timelines for each outbound truck based on traffic and weather.
           - Use a `lineChart` for visual comparison, explaining any potential delays or on-time departures.
           - Time values should be in decimal format (e.g., 12.5 for 12:30 PM).

         ### Step 3: Conduct Risk Assessment
         - Analyze risk level (Low, Medium, High) based on traffic, weather, and scheduling factors.
         - Provide an explanation of the risk level and recommendations to mitigate risks.

         ### Step 4: Provide Detailed Explanations
         - **Carrier Optimization Suggestions**: Text explanation for load allocation efficiency.
         - **Dock Scheduling & Labor Utilization**: Text recommendation for dock and labor efficiency.
         - **Delivery Status**: Summarize the expected timeline, including any delays and mitigation strategies.
         - **Risk Mitigation**: Text outlining actions to reduce delays or bottlenecks.

         ### Final Recommendations
         - Summarize key actions to minimize storage, optimize dock/labor use, and ensure timely deliveries.

        
        ### **Notes**:
        - Use Time in the format HH:MM AM/PM
        - Use only **pieChart**, **barChart**, or **lineChart** for visuals.
        """
    )

    user_prompt = (
        """
        I need you to analyze the cross-docking process based on my following input data:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "cross-docking": {
        "prompt_func": cross_docking_prompt,
        "response_format": CrossDockingAnalysisResults,
        "input_format": CrossDockingInputParams,
        "options": {
            "loadType": ["Perishable", "Fragile", "Standard", "Special", "Other"],
            "priorityLevel": ["High", "Medium", "Low"],
            "trafficConditions": ["Light", "Moderate", "Heavy"],
            "weatherConditions": ["Clear", "Rain", "Snow", "Fogg", "Storm"],
        }
    }
}
