from pydantic import BaseModel

class JustInTimeInventoryInputParamsType(BaseModel):
    productType: str
    currentInventoryLevel: int
    averageLeadTime: int
    dailyDemand: int
    productionDays: int