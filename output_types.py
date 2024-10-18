from pydantic import BaseModel


class PlotData(BaseModel):
    label: str
    value: float


class Plot(BaseModel):
    xLabel: str
    yLabel: str
    chartType: str
    data: list[PlotData]


class Results(BaseModel):
    description: str
    plot: Plot
    conclusion: str


class AnalysisResults(BaseModel):
    results: list[Results]
