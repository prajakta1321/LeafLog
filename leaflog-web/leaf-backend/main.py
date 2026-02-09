from fastapi import FastAPI
from database import get_connection
from models import Household
import database
import schemas

from pydantic import BaseModel



app = FastAPI(title = 'Leaflog Sustainability API')

@app.post("/households")
def create_household(household: Household):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Households (household_name, city_zone, members_count)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (
        household.household_name,
        household.city_zone,
        household.members_count
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Household created"}


@app.get('/households')
def get_households():
    conn = get_connection()
    cursor = conn.cursor(dictionary = True)

    cursor.execute("SELECT * FROM Households")
    data  = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


@app.get("/energy")
def get_energy_usage():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM EnergyUsage")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data

@app.get("/energy/{household_id}")
def energy_by_household(household_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT * FROM EnergyUsage
    WHERE household_id = %s
    """
    cursor.execute(query, (household_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


@app.get("/summary")
def sustainability_summary():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        h.household_name,
        SUM(e.electricity_kwh) AS total_electricity,
        SUM(e.renewable_kwh) AS total_renewable,
        SUM(w.liters_consumed) AS total_water
    FROM Households h
    JOIN EnergyUsage e ON h.household_id = e.household_id
    JOIN WaterUsage w ON h.household_id = w.household_id
    GROUP BY h.household_name
    """

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


households = []

@app.post("/households")
def create_household(data: Household):
    households.append(data)
    return {"message": "Household created"}

@app.get("/households")      # GET APIs simply fetch data, they dont display a body just the fetched data.
def get_households():
    return households

@app.get("/households/{household_id}")
def get_household(household_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Households WHERE household_id=%s", (household_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


@app.get("/households")
def get_all_households():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Households")
    households = cursor.fetchall()

    cursor.close()
    conn.close()

    return households

@app.put("/households/{household_id}")
def update_household(household_id: int, household_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Households SET household_name=%s WHERE household_id=%s",
        (household_name, household_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Household updated successfully"}

class EnergyUsage(BaseModel):
    household_id: int
    electricity_kwh: float
    month: int
    year: int

@app.post("/energy-usage")
def add_energy_usage(data: EnergyUsage):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO EnergyUsage (household_id, month, year, electricity_kwh)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (
        data.household_id,
        data.month,
        data.year,
        data.electricity_kwh
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Energy usage added successfully"}



@app.get("/")
def home():
    return {"message": "LeafLog API is running"}
