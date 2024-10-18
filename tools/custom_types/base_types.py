from pydantic import BaseModel


class PlotData(BaseModel):
    label: str
    value: float


class Plot(BaseModel):
    xLabel: str
    yLabel: str
    chartType: str
    data: list[PlotData]