from fastapi import FastAPI
from database import get_connection

app = FastAPI(title = 'Leaflog Sustainability API')

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

@app.get("/")
def home():
    return {"message": "LeafLog API is running"}
