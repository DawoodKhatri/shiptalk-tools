from pydantic import BaseModel
from typing import Optional


class PlotData(BaseModel):
    label: str
    value: float


class Plot(BaseModel):
    xLabel: str
    yLabel: str
    chartType: str
    data: list[PlotData]
    explanation: Optional[str]

class NamedPlot(Plot):
    name: str


class ComparisonPlot(BaseModel):
    xLabel: str
    yLabel: str
    yActualLabel: str
    yComparedLabel: str
    chartType: str
    actualData: list[PlotData]
    comparedData: list[PlotData]
    explanation: str
