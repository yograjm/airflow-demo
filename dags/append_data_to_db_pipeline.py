from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from process_data import append_data_to_db


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'process_data_pipeline_4',
    default_args=default_args,
    schedule_interval='* * * * *',
    catchup=False
)


process_data_task = PythonOperator(
    task_id='append_data_to_database',
    python_callable=append_data_to_db,
    dag=dag
)




# process_task = PythonOperator(
#     task_id='process_weather_data',
#     python_callable=func2, # process_weather.process_weather,
#     dag=dag
# )

# fetch_task >> process_task  # Define execution order
