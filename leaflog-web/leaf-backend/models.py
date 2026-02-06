from pydantic import BaseModel


class Household(BaseModel):
    household_name : str
    city_zone : str
    members_count : int

