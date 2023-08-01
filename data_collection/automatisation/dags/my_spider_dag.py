from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 31),  # Adjust to your desired start date
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my_spider_dag',
    default_args=default_args,
    description='A DAG to run a spider every Monday at 8 o\'clock',
    schedule_interval='0 8 * * 1',  # Cron expression for every Monday at 8:00
    catchup=False,
)

# Define the task to run the spider (adjust the command as needed)
run_spider_task = BashOperator(
    task_id='run_spider',
    # Replace with your spider command
    bash_command='cd /opt/scrapy_project && scrapy crawl soon_release',
    dag=dag,
)
