
import pandas as pd
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'storedb',
    'user': 'postgres',
    'password': 'mypassword',
    'host': 'localhost',  # EC2 public IP # or your database host
    'port': '5432'        # default PostgreSQL port
}


def append_data_to_db():

    # Read the CSV file
    csv_file_path = 'https://raw.githubusercontent.com/yograjm/airflow-demo/refs/heads/main/titanic.csv'
    data = pd.read_csv(csv_file_path)
    print(data.shape)
    print(data.isna().sum())

    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Read existing data from the table
        query = "SELECT * FROM titanic;"  # SQL query to select all data from the table
        cursor.execute(query)

        # Fetch all results
        rows = cursor.fetchall()

        # Get column names from the cursor
        column_names = [desc[0] for desc in cursor.description]

        # Create a DataFrame from the fetched data
        df = pd.DataFrame(rows, columns=column_names)

        # Display the DataFrame
        #print(df)

        # Next Row to add to db
        curr_rows = len(df)
        print(f"Existing rows in db: {curr_rows}")

        # Insert data into the passengers table
        row_to_add = data.iloc[[curr_rows], :]
        #row_to_add = row_to_add.where(pd.notna(row_to_add), None)
        #row_to_add = row_to_add.fillna(NULL)
        print(row_to_add)
        
        print(row_to_add.dtypes)

        for index, row in row_to_add.iterrows():
            cursor.execute(
                sql.SQL("INSERT INTO titanic (Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                (row['Survived'], row['Pclass'], row['Name'], row['Sex'], row['Age'], row['SibSp'], row['Parch'], row['Ticket'], row['Fare'], row['Cabin'], row['Embarked'])
            )

        # Commit the transaction
        conn.commit()
        print(f"Data inserted successfully.\nCurrent rows: {len(df)+1}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    append_data_to_db()
