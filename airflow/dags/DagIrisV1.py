from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.python_operator import PythonOperator

pathScript = "/root/airflow/dags/etl_scripts"
pathIris =  "/root/airflow/dags/etl_scripts/featurestore/iris.txt"
pathEncoder = "/root/airflow/dags/etl_scripts/featurestore/irisEncoder.txt"


def print_context1(ds, **kwargs):
    print(kwargs)
    print(ds)
    kwargs['task_instance'].xcom_push(key='resultado_task', value="retorno print_context1")

def print_context2(ds, **kwargs):
    print(kwargs)
    print(ds)
    resulto_print_context1 = kwargs['task_instance'].xcom_pull(key='resultado_task')
    resulto_print_context1 = resulto_print_context1 + 'print_context2'
    return resulto_print_context1


def task_failure_alert(context):
    subject = "[Airflow] DAG {0} - Task {1}: Failed".format(
        context['task_instance_key_str'].split('__')[0], 
        context['task_instance_key_str'].split('__')[1]
        )
    html_content = """
    DAG: {0}<br>
    Task: {1}<br>
    Failed on: {2}
    """.format(
        context['task_instance_key_str'].split('__')[0], 
        context['task_instance_key_str'].split('__')[1], 
        datetime.now()
        )
    #send_email_smtp(dag_vars["dev_mailing_list"], subject, html_content)
    print(subject, html_content)
    text_file = open("/Users/jeanalves/airflow/dags/etl_scripts/erro.txt", "w")
    n = text_file.write(subject + html_content)
    text_file.close()

default_args = {
   'owner': 'teste',
   'depends_on_past': False,
   'start_date': datetime(2019, 1, 1),
   'retries': 0,
   'on_failure_callback': task_failure_alert
   }

with DAG(
   'dag-pipeline-iris-aula-ia-v1',
   schedule_interval=timedelta(minutes=10),
   catchup=False,
   default_args=default_args
   ) as dag:

    start = DummyOperator(task_id="start")

    with TaskGroup("etl", tooltip="etl") as etl:
        
        t1 = BashOperator(
            dag=dag,
            task_id='download_dataset',
            bash_command="""
            cd {0}/featurestore
            curl -o iris.txt  https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
            """.format(pathScript)
        )

        [t1]

    with TaskGroup("preProcessing", tooltip="preProcessing") as preProcessing:
        t2 = BashOperator(
            dag=dag,
            task_id='encoder_dataset',
            bash_command="""
            cd {0}
            python etl_preprocessing.py {1} {2}
            """.format(pathScript, pathIris, pathEncoder)
        )
        t3 = PythonOperator(
            task_id='print_the_context1',
            provide_context=True,
            python_callable=print_context1,
            dag=dag)
        t4 = PythonOperator(
            task_id='print_the_context2',
            provide_context=True,
            python_callable=print_context2,
            dag=dag)
        [[t2,t3] >> t4]


    end = DummyOperator(task_id='end')
    start >> etl >> preProcessing >> end