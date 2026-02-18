# old version
from pydantic import BaseModel
from typing import Optional

class EnergyUsageBase(BaseModel):
    month: int
    year: int
    electricity_kwh: float
    renewable_kwh: float

class EnergyUsageCreate(EnergyUsageBase):
    household_id: int

class EnergyUsageResponse(EnergyUsageBase):
    usage_id: int
    household_id: int

    class Config:
        orm_mode = True


# new version

from pydantic import BaseModel
from typing import Optional

class EnergyUsageBase(BaseModel):
    month: int
    year: int
    electricity_kwh: float
    renewable_kwh: float

class EnergyUsageCreate(EnergyUsageBase):
    household_id: int

class EnergyUsageResponse(EnergyUsageBase):
    usage_id: int
    household_id: int

    class Config:
        orm_mode = True

class EnergyUsage(BaseModel):
    household_id : int
    electricity_kwh : float
    month : str
