# queries.py
from database import get_connection
import sqlite3
import pandas as pd
DB_NAME = "food_waste.db"

def run_query(query, params=None, fetch=True):
    conn = sqlite3.connect(DB_NAME)  # replace with your connection
    cur = conn.cursor()

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    if fetch:
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]  # Get column names
        conn.close()
        return pd.DataFrame(rows, columns=cols)
    else:
        conn.commit()
        conn.close()
        return None
# 1. How many food providers and receivers are there in each city?
def providers_and_receivers_by_city():
    query = """
    SELECT city,
           SUM(CASE WHEN type = 'provider' THEN 1 ELSE 0 END) AS provider_count,
           SUM(CASE WHEN type = 'receiver' THEN 1 ELSE 0 END) AS receiver_count
    FROM (
        SELECT City, 'provider' AS type FROM providers
        UNION ALL
        SELECT City, 'receiver' AS type FROM receivers
    ) AS combined
    GROUP BY City;
    """
    return run_query(query)

# 2. Which type of food provider contributes the most food?
def top_provider_type():
    query = """
    SELECT Provider_Type, COUNT(*) AS total_listings
    FROM providers p
    JOIN food_listings f ON p.Provider_ID = f.Provider_ID
    GROUP BY Provider_Type
    ORDER BY total_listings DESC
    LIMIT 1;
    """
    return run_query(query)

# 3. Contact info of food providers in a specific city
def provider_contacts_by_city(city):
    query = """
    SELECT 
    p.Name AS Provider_Name,
    p.Contact,
    p.City
    FROM providers p
    WHERE LOWER(TRIM(p.City)) = LOWER(TRIM(?));
    """
    return run_query(query, (city,))

#4. Receivers with most food claims
def top_receivers():
    query = """
    SELECT r.Name, COUNT(c.Receiver_ID) AS total_claims
    FROM claims c
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    GROUP BY r.Receiver_Id,r.Name
    ORDER BY total_claims DESC;
    """
    return run_query(query)

#5.What is the total quantity of food available from all providers?
def food_available():
    query = """SELECT
    SUM(Quantity)
    AS
    Total_Available_Quantity
    FROM
    food_listings; 
    """
    return run_query(query)

#6. Which city has the highest number of food listings?
def highest_food_listings():
    query = """SELECT Location, COUNT(*) AS Number_of_Listings
    FROM food_listings
    GROUP BY Location
    ORDER BY Number_of_Listings DESC
    LIMIT 1;
    """
    return run_query(query)

#7.What are the most commonly available food types?
def food_types():
    query = """SELECT Food_Type, COUNT(*) AS Count
    FROM food_listings
    GROUP BY Food_Type
    ORDER BY Count DESC;
    """
    return run_query(query)

#8.How many food claims have been made for each food item?
def food_claims():
    query = """SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Food_Name
    ORDER BY Total_Claims DESC;
    """
    return run_query(query)

#9.Which provider has had the highest number of successful food claims?
def highest_successful_food_claims():
    query = """SELECT p.Name AS Provider_Name, COUNT(c.Claim_ID) AS Successful_Claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Name
    ORDER BY Successful_Claims DESC
    LIMIT 1;
    """
    return run_query(query)

#10.What percentage of food claims are completed vs. pending vs. canceled?
def pending_completed_cancelled_Foodclaims():
    query = """SELECT Status,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage
    FROM claims
    GROUP BY Status;
    """
    return run_query(query)

#11.What is the average quantity of food claimed per receiver?
def food_quantity_per_receiver():
    query = """
    SELECT 
    r.Name AS Receiver_Name,
    ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Claimed
    FROM claims c
    JOIN food_listings f 
    ON c.Food_ID = f.Food_ID
    JOIN receivers r 
    ON c.Receiver_ID = r.Receiver_ID
    GROUP BY r.Name;
    """
    return run_query(query)

#12.Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
def meal_type():
    query = """SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    GROUP BY f.Meal_Type
    ORDER BY Total_Claims DESC;
    """
    return run_query(query)

#13.What is the total quantity of food donated by each provider?
def food_donated():
    query = """SELECT p.Name AS Provider_Name, SUM(f.Quantity) AS Total_Donated
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    GROUP BY p.Name
    ORDER BY Total_Donated DESC;
    """
    return run_query(query)

#Implementing CRUD operations on providers dataset
def add_provider(provider_id,name, provider_type, address, city, contact):
    query = """
            INSERT INTO providers (Provider_ID, Name, Provider_Type, Address, City, Contact)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    run_query(query, (provider_id, name, provider_type, address, city, contact), fetch=False)
    return "Provider created successfully!"

def get_all_providers():
    query = """SELECT Provider_ID, Name, Type, Address, City, Contact
        FROM providers"""
    return run_query(query,fetch = True)

def update_provider(provider_id, name, provider_type, address, city, contact):
    query = """
    UPDATE providers
    SET Name = ?, Type = ?, Address = ?, City = ?, Contact = ?
    WHERE Provider_ID = ?
    """
    run_query(query, (name, provider_type, address, city, contact, provider_id),fetch = False)
    return "Provider updated successfully!"

def delete_provider(provider_id):
    query = "DELETE FROM providers WHERE Provider_ID = ?"
    run_query(query, (provider_id,))
    return "Provider deleted successfully!"





