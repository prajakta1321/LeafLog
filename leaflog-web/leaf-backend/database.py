# old version
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="leaflog"
    )

# new version

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="leaflog"
    )

def create_energy_usage(usage):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO EnergyUsage (household_id, electricity_kwh, month) VALUES (%s, %s, %s)",
        (usage.household_id, usage.electricity_kwh, usage.gas_units, usage.month))
    
    conn.commit()
    cursor.close()
    conn.close()

    return {"message" : "Energy usage is added."}
