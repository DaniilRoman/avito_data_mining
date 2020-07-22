import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from step_1_prerequisites import Prerequisites
from step_2_download_html_pages import HtmlPagesDownloader
from step_3_html_to_scv import MainFeatureExtracter
from step_4_geocoding import Geocoder
from step_5_add_area import AreaGetter
from step_6_aggregate import Aggregator


default_args = {
    'owner': 'daniil.roman',
    'start_date': dt.datetime(2018, 9, 24, 10, 00, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('avito_apartments_preprocessing',
         default_args=default_args,
         schedule_interval='@once'
         ) as dag:

    step_1 = PythonOperator(task_id='prerequisites',
                               python_callable=Prerequisites().execute)
    step_2 = PythonOperator(task_id='html_pages_downloader',
                               python_callable=HtmlPagesDownloader().execute)
    step_3 = PythonOperator(task_id='main_feature_extracter',
                               python_callable=MainFeatureExtracter().execute)
    step_4 = PythonOperator(task_id='geocoder',
                               python_callable=Geocoder().execute)
    step_5 = PythonOperator(task_id='area_getter',
                               python_callable=AreaGetter().execute)
    step_6 = PythonOperator(task_id='aggregator',
                               python_callable=Aggregator().execute)

                                 
step_1 >> step_2 >> step_3 >> step_4 >> step_5 >> step_6
