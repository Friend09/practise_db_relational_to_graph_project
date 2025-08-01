# scripts/create_db.py

import sqlite3
import pandas as pd

def create_and_load_db(db_path, sql_schema_path, csv_data_path):
    """
    Create an SQLite database using the provided SQL schema and load data from a CSV file.

    Args:
        db_path (str): Path to the SQLite database file to create or overwrite.
        sql_schema_path (str): Path to the SQL schema file (DDL statements).
        csv_data_path (str): Path to the CSV file containing application data.

    This function:
        - Loads the SQL schema and executes it to create the database structure.
        - Reads the CSV data into a pandas DataFrame.
        - Cleans column names to match the SQL schema.
        - Converts boolean and date columns to SQLite-compatible formats.
        - Inserts the data into the 'applications' table.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Load SQL schema
        with open(sql_schema_path, 'r') as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        print(f"Schema from {sql_schema_path} loaded successfully.")

        # Load CSV data into a DataFrame
        df = pd.read_csv(csv_data_path)

        # Clean up column names to match SQL schema (lowercase and remove spaces if any)
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Convert boolean column to integer (0 or 1) for SQLite
        if 'in_use' in df.columns:
            df['in_use'] = df['in_use'].astype(int)

                # Handle date columns: convert to string format compatible with SQLite DATE type
        date_columns = [
            'installation_date', 'last_updated', 'end_of_life_date',
            'renewal_date', 'created_at', 'updated_at'
        ]
        for col in date_columns:
            if col in df.columns:
                # Convert to datetime, then to ISO format string, handle NaT (Not a Time) for None
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.date.astype(str).replace({'NaT': None})

        # Insert DataFrame into SQLite table
        # Ensure the table name matches the one in your SQL schema
        df.to_sql('applications', conn, if_exists='append', index=False)
        print(f"Data from {csv_data_path} loaded successfully into 'applications' table.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    path = "/Users/vamsi_mbmax/Developer/VAM_Documents/01_vam_PROJECTS/LEARNING/proj_Databases/dev_proj_Databases/practise_db_relational_to_graph_project"

    csv_data = f'{path}/data/applications.csv'
    db_file = f'{path}/data/applications.db'
    sql_schema = f'{path}/sql/applications.sql'
    create_and_load_db(db_file, sql_schema, csv_data)
