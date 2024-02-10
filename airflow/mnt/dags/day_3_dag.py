from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils import timezone #๊Default จะเป็น UTC



with DAG(   #เรียกกว่า context
    "day_3_dag",
    schedule="0 18 3 * *",
    start_date=timezone.datetime(2024, 1, 20),  #เริ่มวันไหน ให้พยายามใช้ librarry datetime ที่ airflow มีอยู่ อาจมีเรื่อง timezone, daylight save

):
    # Code here
    my_first_task = EmptyOperator(task_id="my_first_task")
    my_second_task = EmptyOperator(task_id="my_second_task")

    my_first_task >> my_second_task
