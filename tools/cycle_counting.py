import json
from pydantic import BaseModel
from .custom_types.base_types import Plot
from pydantic import BaseModel


class CycleCountingInputParams(BaseModel):
    cycleCountFrequency: str  # Frequency of cycle counts (e.g., daily, weekly)
    expectedCount: int  # Expected number of items in the inventory
    # Current number of items recorded in the inventory system
    currentInventoryLevels: int
    # Priority level of the cycle count process (e.g., High, Medium, Low)
    priorityLevel: str


class ProgressData(BaseModel):
    # Label for the metric (e.g., "Inventory Risk", "Replenishment Urgency")
    label: str
    # Percentage or progress value (0-100 for progress bar display)
    value: float
    explanation: str  # Markdown explanation for the progress value


class RiskAnalysis(BaseModel):
    riskLevel: str  # Low, Medium, High (risk categorization)
    riskProgress: float  # Numeric representation for progress bar (0-100)
    explanation: str  # Markdown explanation for the risk level


class CycleCountingAnalysisResults(BaseModel):
    # Discrepancy between expected and current inventory levels
    discrepancyAnalysis: Plot  # Bar or pie chart showing discrepancy
    # Suggestion for adjusting cycle count frequency based on discrepancies and input
    cycleCountFrequencySuggestion: ProgressData  # Progress bar or gauge
    # Risk assessment for inventory discrepancies and stockouts
    # Risk progress bar (Low, Medium, High)
    inventoryRiskAssessment: RiskAnalysis
    # Priority recommendations for cycle counting
    priorityRecommendations: Plot  # Bar chart showing priority-based recommendations
    # Efficiency score for the current cycle counting process
    cycleCountEfficiency: ProgressData  # Efficiency score (0-100)

    # New analytical fields
    # Recommended next cycle count date based on the frequency and priority
    # Number of days or weeks until the next count (e.g., "2 weeks", "5 days")
    nextCycleCountPeriod: str
    # Replenishment suggestion if the inventory count is lower than expected
    # Markdown text recommending when and how to replenish stock
    replenishmentSuggestion: str
    # Over/Understock analysis providing insights on whether certain items are overstocked or understocked
    stockLevelAnalysis: Plot  # Bar chart showing overstocked/understocked items
    # Recommendations for improving cycle count accuracy
    # Markdown text suggesting ways to improve cycle count accuracy
    accuracyImprovementSuggestions: str
    # Explanation of the overall cycle count process and suggestions for streamlining it
    # Markdown text offering tips for improving the cycle count process
    processStreamliningSuggestions: str


def cycle_counting_prompt(inputParameters: CycleCountingInputParams):

    system_prompt = (
        """
        You are an assistant for a shipping community tool called the Cycle Counting Tool. Your task is to analyze the input provided by the user and generate actionable recommendations for optimizing the cycle counting process.

        The goal is to help users improve their counting frequency, detect discrepancies in counts, and prioritize items for future cycle counts based on urgency and past discrepancies.

        ## *Steps to Follow*:

        1. **Input Understanding**:
           You will receive the following inputs from the user:
           """
        + json.dumps(CycleCountingInputParams.model_json_schema())
        + """
           Based on these inputs, you will generate insights and recommendations.

        2. **Visual Outputs** (Use pieChart, barChart, or lineChart):
           - **Cycle Count Accuracy Analysis**:
             - Compare the **expected item count** with the **current inventory levels**.
             - Generate a barChart showing the expected count vs. actual counted items during the cycle count.
             - Highlight discrepancies between the counts and recommend corrective actions if discrepancies are found.
             - The explanation must be formatted as **Markdown**.

           - **Cycle Count Frequency Adjustment**:
             - Based on the user's input and discrepancies, generate a recommendation to either maintain or adjust the frequency of the cycle count (e.g., daily, weekly, monthly).
             - Use a progress bar or gauge to show whether the frequency should be increased or maintained.
             - Provide a markdown explanation suggesting how to optimize the cycle count schedule based on accuracy and priority.
             
           - **Priority Recommendations for Cycle Counting**:
             - Analyze the **priority level** provided by the user and any **discrepancies** between the expected and actual cycle count.
             - If the priority is **High**, recommend more frequent counting for items with large discrepancies.
             - If the priority is **Low**, suggest maintaining the current count frequency unless discrepancies are significant.
             - Generate a barChart or pieChart showing priority-based recommendations for items that need urgent counting attention.
             - The explanation must be formatted as **Markdown** and should justify why specific items need more frequent cycle counts.

        3. **Text-Based Explanations** (Strictly in Markdown Format):
           - **Cycle Count Frequency Suggestions**:
             - Based on the user's input (frequency, priority, discrepancies), provide a suggestion for adjusting the cycle count frequency.
             - The suggestion must be formatted as **Markdown**.

           - **Cycle Count Discrepancy Reporting**:
             - Provide a markdown explanation of any discrepancies detected during the cycle count process.
             - Suggest actions the user should take to address these discrepancies, such as recounting, increasing frequency, or auditing inventory processes.

           - **Recommendations for Improving Cycle Count Accuracy**:
             - Suggest ways to improve the accuracy of the cycle count process (e.g., improving counting methods, adjusting counting frequency).
             - The suggestions must be formatted as **Markdown**.

           - **Process Optimization for Cycle Counting**:
             - Provide markdown text with recommendations for optimizing or automating the cycle count process, such as using barcode scanners or implementing automated systems.
             
           - **Next Cycle Count Period**:
             - Based on discrepancies, priority, and frequency, suggest how many days or weeks should pass before the next cycle count.
             - The recommendation should be provided as **Markdown**, with an example like "2 weeks" or "5 days."

        4. **Final Recommendations**:
           - After generating all the visuals and explanations, provide a final markdown conclusion that summarizes the key recommendations for the user.
           - The conclusion should focus on how to improve the accuracy of cycle counting, optimize frequency, and prioritize items for future cycle counts.

        5. **Output Format**:
           The output should be structured in JSON format with the following sections:
             - `cycleCountAccuracyAnalysis`: A `Plot` object with visual data and **markdown** explanation.
             - `cycleCountFrequencyAdjustment`: A `ProgressData` object with a suggested frequency adjustment and markdown explanation.
             - `priorityRecommendations`: A `Plot` object with priority-based recommendations for counting and markdown explanation.
             - `discrepancyReporting`: **Markdown** text explaining any discrepancies found in the cycle count.
             - `accuracyImprovementSuggestions`: **Markdown** text with tips for improving cycle count accuracy.
             - `processOptimizationSuggestions`: **Markdown** text suggesting ways to streamline or automate the cycle count process.
             - `conclusion`: A final **markdown** text summarizing key takeaways.

        ---
        ### **Notes**:
        - Ensure the visual data is formatted in a way that can be used for creating charts and graphs.
        - Use only **pieChart**, **barChart**, or **lineChart** for visuals.
        - All explanations and conclusions must be provided in **markdown** format for clarity.
        """
    )

    user_prompt = (
        """
        I need you to analyze the cycle counting process based on the following input:
        """
        + json.dumps(inputParameters.model_dump(), indent=4)
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return messages


tool_config = {
    "cycle-counting": {
        "prompt_func": cycle_counting_prompt,
        "response_format": CycleCountingAnalysisResults,
        "input_format": CycleCountingInputParams,
        "options": {
            "cycleCountFrequency": ["Daily", "Weekly", "Bi-Weekly", "Monthly", "Quarterly", "Annually"],
            "priorityLevel": ["High", "Medium", "Low"],
        }
    }
}
