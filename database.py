import sqlite3
import pandas as pd

DB_NAME = "food_waste.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS providers (
        Provider_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        City TEXT,
        Contact TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receivers (
        Receiver_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        City TEXT,
        Contact TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_listings (
        Food_ID INTEGER PRIMARY KEY,
        Food_Name TEXT,
        Quantity INTEGER,
        Expiry_Date DATE,
        Provider_ID INTEGER,
        Provider_Type TEXT,
        Location TEXT,
        Food_Type TEXT,
        Meal_Type TEXT,
        FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        Claim_ID INTEGER PRIMARY KEY,
        Food_ID INTEGER,
        Receiver_ID INTEGER,
        Status TEXT,
        Timestamp DATETIME,
        FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID),
        FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID)
    )
    """)

    conn.commit()
    conn.close()

def load_csv_to_table(csv_file, table_name):
    conn = get_connection()
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, conn, if_exists="append", index=False)
    conn.close()

def run_query(query):
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    create_tables()
    load_csv_to_table("providers_data.csv", "providers")
    load_csv_to_table("receivers_data.csv", "receivers")
    load_csv_to_table("food_listings_data.csv", "food_listings")
    load_csv_to_table("claims_data.csv", "claims")
    print("Database setup complete!")
