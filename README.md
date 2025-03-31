# airflow-demo


## Steps:

- Start a Postgres docker container
  
  To start a DB container:
  `docker run -it -d -p 5432:5432 -e POSTGRES_PASSWORD=mypassword --name=postgrescont postgres:latest`
  
- Create a Postgres database - `storedb`

  To enter into container:
  `docker exec -it postgrescont psql -U postgres`

  To list all databases: 
  `SELECT datname FROM pg_database WHERE datistemplate = false;`

  To create a new DB
  `CREATE DATABASE storedb;`

  To switch to a particular DB:
  `\c storedb;`

- Create a table - `titanic`

  To see tables inside a DB:
  `\dt`

  To create table:
    ```yml
    CREATE TABLE titanic (
        PassengerId SERIAL PRIMARY KEY,
        Survived INTEGER,
        Pclass INTEGER,
        Name VARCHAR(255),
        Sex VARCHAR(10),
        Age INTEGER,
        SibSp INTEGER,
        Parch INTEGER,
        Ticket VARCHAR(50),
        Fare DECIMAL(10, 4),
        Cabin VARCHAR(10),
        Embarked CHAR(1)
    );
    ```

    To check table rows: (Press `q` if the output is being displayed in a pager)
    `SELECT * FROM titanic;`

- Create a Python script, `process_data.py`, to add data to `storedb` from the csv file
  - Load the csv data
  - Add data to db

- Airflow to run the Python script `process_data.py` periodically
  - Ref (https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
  - UI was running
  - DAG was creating
  - Pipeline execution failed because of localhost in `postgrescont`


Issues:
- Pipeline execution failed because of localhost in `postgrescont`
   - Host postgres on EC2
- Missing values in `titanic.csv`
   - Update CSV 
   - OR handle missing via code in `process_data.py`


