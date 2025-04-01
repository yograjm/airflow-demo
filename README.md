# airflow-demo


## Steps:

- Start a Postgres docker container in an Amazon EC2 instance
  
  Launch and EC2 instance and install Docker in it
  ```yml
  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt install docker.io -y
  sudo systemctl start docker
  sudo systemctl enable docker
  sudo docker --version
  ```

  To start a DB container:
  `sudo docker run -it -d -p 5432:5432 -e POSTGRES_PASSWORD=mypassword --name=postgrescont postgres:latest`
  
- Create a Postgres database - `storedb`

  To enter into container:
  `sudo docker exec -it postgrescont psql -U postgres`

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
        Cabin VARCHAR(100),
        Embarked CHAR(1)
    );
    ```

    To check table rows: (Press `q` if the output is being displayed in a pager)
    `SELECT * FROM titanic;`
    `SELECT * FROM titanic ORDER BY passengerid DESC LIMIT 10;`

- On Codespace, create a Python script, `process_data.py`, to add data to `storedb` from the csv file
  - Load the csv data
  - Add data to db

- Airflow to run the Python script `process_data.py` periodically
  - Ref (https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
    `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml'`
    `mkdir -p ./dags ./logs ./plugins ./config`
    Add `.py` files to `./dags` folder
    `echo -e "AIRFLOW_UID=$(id -u)" > .env`
    `docker compose up airflow-init`
    `docker compose up`
  - UI running
  - DAG creating
  - Pipeline execution success - data appending to the DB


Issues Encountered:
- Pipeline execution failed because of localhost in `postgrescont`
   - Resolution: Host postgres on EC2
- Missing value error in `Age` column
   - Resolution: Handled missing value in `Age` column whithin code file



