from flask import Flask, render_template
import mysql.connector

from flask import request, redirect 

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user="root",
        password="root",
        database="leaflog"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/households")
def households():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Households")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("households.html", households=data)


#households = []

#@app.route("/add-household", methods=["POST"])   # this function only stores data in python list
#def add_household():
#    name = request.form["household_name"]
#    zone = request.form["city_zone"]
#    members = request.form["members_count"]

    #households.append((name, zone, members))

#    return redirect("/")

@app.route("/add-household", methods=["POST"])     # this function unlike the above one uses database to insert data
def add_household():
    name = request.form["household_name"]
    zone = request.form["city_zone"]
    members = request.form["members_count"]

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO Households (household_name, city_zone, members_count)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, zone, members))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/households")

@app.route("/energy")        # connect the Energy page to the database.
def energy():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM EnergyUsage")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("energy.html", energy=data)

# add a Dashboard page with summary data
@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        h.household_name,
        SUM(e.electricity_kwh) AS total_electricity
    FROM Households h
    JOIN EnergyUsage e ON h.household_id = e.household_id
    GROUP BY h.household_name
    """

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dashboard.html", data=data)



if __name__ == "__main__":
    app.run(debug = True)
