import requests
import pandas as pd
from datetime import datetime
import psycopg2
import json
import os
from dotenv import load_dotenv

"""
The code is scheduled to autorun everyday at 3AM Jordan time and it will insert a new row to the table
"""
load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
FIRST_API = os.getenv('FIRST_API')

api_key=FIRST_API

current_date = datetime.today().strftime('%Y-%m-%d')

url = f'https://openexchangerates.org/api/historical/{current_date}.json'
response = requests.get(f'{url}?app_id={api_key}')

exchange_rate = response.json()["rates"]
my_json = json.dumps(exchange_rate)


# //////////////////////////////////////////
# /////////////////DATABASE/////////////////
# //////////////////////////////////////////

def connect_to_db():
    # Connecting to db
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    # Execute statements 
    cur = conn.cursor()

    def create_table():
        # Create table, add to it two coloms, date and revenue_rates_usd
        cur.execute("CREATE TABLE usd_rates (id SERIAL PRIMARY KEY, date DATE , revenue_rates_usd JSONB NOT NULL );")
    
    def insert_into_db():
        # Inserting new data to date and revenue_rates_usd
        # cur.execute("INSERT INTO usd_rates (date, revenue_rates_usd) VALUES(%s, %s)", (current_date, my_json))

        
        # Display usd_rates table 
        all_data = pd.read_sql("SELECT * FROM usd_rates;", conn)
        print(all_data)

    insert_into_db()
    conn.commit()

    # Closing
    cur.close()
    conn.close()
connect_to_db()
