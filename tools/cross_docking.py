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
    explanation: str  # Markdown explanation for the risk level


class DeliveryStatus(BaseModel):
    status: str  # e.g., "On Time", "Delayed"
    explanation: str  # Explanation in markdown format


class CostEfficiency(BaseModel):
    laborEfficiency: str  # Explanation in markdown format
    dockUtilization: str  # Explanation in markdown format
    truckCapacityUtilization: str  # Explanation in markdown format


class CrossDockingAnalysisResults(BaseModel):
    carrierOptimization: Plot  # Using the Plot class for visual data
    dockScheduling: str  # Markdown formatted suggestion
    laborAllocation: Plot  # Pie chart for labor allocation
    riskAssessment: RiskAnalysis  # Markdown formatted risk assessment
    deliveryTimelineComparison: ComparisonPlot  # Line chart for delivery timeline
    deliveryStatus: DeliveryStatus  # Markdown formatted delivery status
    costEfficiency: CostEfficiency  # Markdown formatted cost analysis


def cross_docking_prompt(inputParameters: CrossDockingInputParams):

    system_prompt = (
        """
        You are an assistant for a shipping community tool called the Cross-Docking Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing the cross-docking process.

        The goal is to help users minimize storage time, efficiently allocate labor and dock resources, and optimize the transfer of goods between inbound and outbound trucks.

        ## *Steps to Follow*:

        1. **Input Understanding**:
           You will receive the following inputs from the user:
           """
        + json.dumps(CrossDockingInputParams.model_json_schema())
        + """
           Based on these inputs, you will generate insights and recommendations.

        2. **Visual Outputs** (Use pieChart, barChart, or lineChart):
           - **Carrier Optimization Analysis**:
             - Analyze the load distribution between the outbound trucks.
             - Generate a barChart showing the load allocated to each outbound truck.
             - Provide a **markdown** format explanation detailing the allocation and any recommendations for balancing the load.

           - **Dock Scheduling and Labor Allocation**:
             - Based on the number of available docks and labor, generate a recommendation for scheduling the unloading and loading of trucks.
             - Use a barChart to represent dock utilization and a pieChart for labor distribution.
             - Provide a **markdown** explanation on how the docks and labor should be allocated for maximum efficiency.

           - **Delivery Timeline Comparison**:
             - Compare the planned departure times of outbound trucks with any adjusted times based on the user's input (traffic, weather).
             - Generate a lineChart showing the comparison between the planned and adjusted timelines.
             - The values should be in proper format (e.g., For 12:30 PM, use 12.5 or For 1:45 PM, use 13.75).
             - Provide a **markdown** explanation for any delays or on-time departures and suggestions to mitigate delays if necessary.

           - **Risk Assessment**:
             - Analyze the risk level based on traffic, weather, and scheduling tightness.
             - Provide a **markdown** explanation of the risk level (Low, Medium, High) and any suggestions to minimize risks.

        3. **Text-Based Explanations** (Strictly in Markdown Format):
           - **Carrier Optimization Suggestions**:
             - Provide **markdown** recommendations on how to efficiently load and allocate goods between outbound trucks.

           - **Dock Scheduling and Labor Utilization**:
             - Provide **markdown** text explaining the optimal allocation of docks and labor based on the user's input.
             - Offer **markdown** suggestions on how to improve labor efficiency and reduce dock idle time.

           - **Delivery Status and Timeline Explanation**:
             - Provide **markdown** text summarizing the expected delivery status and any delays.
             - Explain the reasons for potential delays and suggest corrective actions to ensure timely departures.

           - **Risk Mitigation**:
             - Provide **markdown** suggestions for minimizing risks based on current traffic, weather, and other input factors.
             - Recommend actions to reduce delays or avoid bottlenecks in the process.

        4. **Final Recommendations**:
           - After generating all visuals and explanations, provide a final **markdown** conclusion that summarizes the key recommendations for the user.
           - The conclusion should focus on how to optimize cross-docking by minimizing storage time, improving labor and dock utilization, and ensuring timely deliveries.          
          
        5. **Output Format**:
           The output should be structured in JSON format with the following sections:
             - `carrierOptimization`: A `Plot` object with load distribution and **markdown** format of explanation.
             - `dockScheduling`: A `Plot` object for dock utilization and **markdown** format of explanation.
             - `laborAllocation`: A `Plot` object for labor distribution and **markdown** format of explanation.
             - `deliveryTimelineComparison`: A `Plot` object comparing planned and adjusted timelines.
             - `riskAssessment`: **Markdown** text explaining the risk levels and mitigation strategies.
             - `deliveryStatus`: **Markdown** text summarizing the delivery timeline and any delays.
             - `finalRecommendations`: A final **markdown** text summarizing key takeaways and suggestions for process optimization.

        ---
        ### **Notes**:
        - Ensure all explanations and text outputs are provided strictly in **markdown** format including all styling for clarity and consistency in reading for users.
        - Use only **pieChart**, **barChart**, or **lineChart** for visuals.
        """
    )

    user_prompt = (
        """
        I need you to analyze the cross-docking process based on the following input:
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
