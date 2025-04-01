
import pandas as pd
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    'dbname': 'storedb',
    'user': 'postgres',
    'password': 'mypassword',
    'host': '65.1.147.198',  # EC2 public IP # or your database host
    'port': '5432'  #'5432'        # default PostgreSQL port
}


def append_data_to_db():

    # Read the CSV file
    csv_file_path = 'https://raw.githubusercontent.com/yograjm/airflow-demo/refs/heads/main/titanic.csv'
    data = pd.read_csv(csv_file_path)
    data['Age'] = data['Age'].fillna(int(data['Age'].mean()))
    data['Embarked'] = data['Embarked'].fillna('S')
    #data['Cabin'] = data['Cabin'].fillna('No cabin')           # 1, 0   
    #print(data.isna().sum())

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
        print(f"Existing rows in db: {len(df)}")

        # Display the DataFrame
        #print(df)

        # Next Row to add to db
        curr_rows = len(df)
        if curr_rows >= len(data):
            curr_rows = curr_rows - len(data)
        

        # Insert data into the passengers table
        row_to_add = data.iloc[[curr_rows], :]     # add row one-by-one
        #row_to_add = data.iloc[curr_rows:]        # add all rows at once
        # print(row_to_add)

        count = 0

        for index, row in row_to_add.iterrows():
            cursor.execute(
                sql.SQL("INSERT INTO titanic (Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                (row['Survived'], row['Pclass'], row['Name'], row['Sex'], row['Age'], row['SibSp'], row['Parch'], row['Ticket'], row['Fare'], row['Cabin'], row['Embarked'])
            )
            count += 1

        # Commit the transaction
        conn.commit()
        print(f"Data inserted successfully.\nCount after adding new rows: {len(df) + count}")

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
