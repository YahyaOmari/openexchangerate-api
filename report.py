import matplotlib.pyplot as plt
import psycopg2
import pandas as pd
import os
import sys
from dotenv import load_dotenv

"""
In this script you can set the currency (Ccy), start and end dates, and it will display the conversion rates from USD to selected Ccy per day. Remember it converts from USD to the selected Ccy. 

The script can be run through the terminal only, find below steps:
    1. Run poetry install to install all the dependencies.
    2. Poetry shell.
        2b. Incase you use pip instead of poetry, just run this command: pip install matplotlib numpy pandas psycopg2 python-dotenv
    3. In your terminal, run "which python" command, copy the path of your python
    4. Paste the path
    5. On the same line, type "report.py", symbol of the currency you would like to check, then start and end date.
        Example:
        > which_python_path report.py Ccy start_date[YYYY-MM-DD] end_date[YYYY-MM-DD]
        > /mnt/c/Users/owner/Desktop/Task1/.venv/bin/python report.py SAR 2021-04-01 2021-07-01
    6. The script will fetch the data from the stored db, validate the available dates, and then genaerate a table and graph.

note. start_date is only available starting from 2021-01-01 onwards.

"""

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')


script = sys.argv[0]
desired_currency = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]

# //////////////////////////////////////////
# /////////////////DATABASE/////////////////
# //////////////////////////////////////////

def connect_to_db():
    # Connecting to db
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

    # Execute statements 
    cur = conn.cursor()

    # Read db table, converting from USD to SAR and giving range between two dates
    def range_between_dates():
        date_range = pd.read_sql(f"SELECT date as date, revenue_rates_usd ->> '{desired_currency}' AS {desired_currency} FROM usd_rates WHERE date BETWEEN '{start_date}' AND '{end_date}';", conn)
        print(date_range)
    
    # Display the graph
    def graph_date():
        cur.execute(f"SELECT date as date, revenue_rates_usd ->> '{desired_currency}' AS {desired_currency} FROM usd_rates WHERE date BETWEEN '{start_date}' AND '{end_date}';", conn)
        dates = []
        values = []
        
        for row in cur.fetchall():
            # print(row[1])
            dates.append(row[0])
            values.append(row[1])
        plt.bar(dates, values)
        plt.title(f'Exchange from USD to {desired_currency}')
        plt.show()


    range_between_dates()
    graph_date()
    conn.commit()
    
    # Closing
    cur.close()
    conn.close()

connect_to_db()