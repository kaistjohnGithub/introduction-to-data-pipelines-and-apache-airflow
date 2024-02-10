from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils import timezone #๊Default จะเป็น UTC

def _get_weather_data(**context): #เมื่อต้องการสร้างชื่อฟังค์ชั่นที่จะเอาไปใช้ใน task ควรใส่ _ไว้หน้า
    import requests #ทำ import ไว้ด้านในนี้ --> กรณี airflow จะเกี่ยวข้องกับ performance เพราะจะมี่โหลดข้อมูลตลอดเวลา ถ้า import ไว้ใน DAG จะไม่ถูกโหลด ทำให้ทำงานไว
    import json
    #API_KEY = os.environ.get("WEATHER_API_KEY")
    API_KEY = Variable.get("weather_api_key")
    
    name = Variable.get("weather_api_key")
    print(name)

    print(context)
    print(context["execution_date"])

    payload = {
        "q": "bangkok",
        "appid": API_KEY,
        "units": "metric"
    }
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=payload)
    print(response.url)

    data = response.json()
    print(data)

    timestamp = context["execution_date"]
    with open(f"/opt/airflow/dags/weather_data{timestamp}.json", "w") as f:
        json.dump(data, f) #ให้อ่านไฟล์มาเก็บไว้

    return f"/opt/airflow/dags/weather_data{timestamp}.json" # เมื่อ return จะถูกเก็บไว้ใน xcom อัตโนมัติ


def _load_data_to_postgres(**context):
    ti = context['ti']
    file_name  = ti.xcom_pull(task_ids="get_weather_data", key="return_value")
    print(file_name)


with DAG(   #เรียกกว่า context
    "weather_api_dag",
    schedule="@hourly",
    start_date=timezone.datetime(2024, 2, 3),  #เริ่มวันไหน ให้พยายามใช้ librarry datetime ที่ airflow มีอยู่ อาจมีเรื่อง timezone, daylight save
    catchup=False,

):


    start = EmptyOperator(task_id="start")

    get_weather_data = PythonOperator(
        task_id="get_weather_data",
        python_callable=_get_weather_data,   #คือฟังค์ชั่นที่จะไปดึงข้อมูลเข้ามา โดยจะสร่างไว้ด้านบน
    )

    load_data_to_postgres = PythonOperator(
        task_id="load_data_to_postgres",
        python_callable=_load_data_to_postgres,   #คือฟังค์ชั่นที่จะไปดึงข้อมูลเข้ามา โดยจะสร่างไว้ด้านบน
    )

    end = EmptyOperator(task_id="end")

    start >> get_weather_data >> load_data_to_postgres >> end