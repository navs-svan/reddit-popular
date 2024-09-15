from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import datetime


@dag(
    dag_id="reddit_api_pipeline",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=15),
)
def Pipeline():

    extract_from_reddit = BashOperator(
        task_id="extract_from_reddit",
        bash_command="python3 /opt/airflow/extract_load/extract.py",
        retries=3,
    )

    load_to_bucket = BashOperator(
        task_id="load_to_bucket",
        bash_command="python3 /opt/airflow/extract_load/load_bucket.py",
        retries=3,
    )

    load_to_bq = BashOperator(
        task_id="load_to_bq",
        bash_command="python3 /opt/airflow/extract_load/load_bq.py",
        retries=3,
    )

    extract_from_reddit >> load_to_bucket >> load_to_bq


dg = Pipeline()
