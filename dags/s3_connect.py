from datetime import datetime, timedelta
import logging
import os

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators import StageJsonToS3
from airflow.operators import TiingoPricePerIndustryHistorical
from airflow.hooks.S3_hook import S3Hook

from helpers import StockSymbols

default_args = {
    'owner': 'Sulman M',
    'start_date': datetime(2019, 11, 10),
    'depends_on_past': False,
    'retries': 0,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
    'catchup_by_default': False,
}

stock_symbols = StockSymbols()

def create_bucket(*args, **kwargs):
    logging.info(f'Creating NEW S3 bucket')
    ed = kwargs['execution_date'].date()
    bname = f"airflow-usstock-{ed}"
    s3_hook = S3Hook(aws_conn_id='aws_credential')
    logging.info(f'MY BUCKET NAME {bname}')
    s3_hook.create_bucket(bucket_name=bname)

with DAG('S3_connect_DAG', schedule_interval=None, default_args=default_args) as dag:
    # Task 1 - Begin
    start_operator = DummyOperator(
        task_id="Begin_createBucketS3"
        )

    historical_automotive = TiingoPricePerIndustryHistorical(
        task_id='Fetch_HistoricalAutomotivePrices',
        industry='Automotive',
        stock_symbols=stock_symbols.get_stock_symbols_for_industry('Automotive'),
        frequency='daily',
        h_start_date='2018-11-9',
        h_end_date='2019-11-10',
        path_to_write='plugins/output/tmp',
        aws_conn_id='aws_credential',
        s3_bucket='us-stock-data',
        s3_key='Automotive-eod-{start}-to-{end}-{ds}.json',
        execution_date='{{ ds }}'
        )

    # create_bucket_task = PythonOperator(
    #     task_id="create_new_bucket",
    #     python_callable=create_bucket,
    #     provide_context=True
    #     )

    start_operator >> historical_automotive