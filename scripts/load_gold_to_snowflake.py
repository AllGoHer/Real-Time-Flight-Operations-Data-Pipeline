import pandas as pd
import snowflake.connector
from airflow.hooks.base import BaseHook

def load_gold_to_snowflake(**context):
    # 1. Obtener archivo desde XCom
    gold_file = context["ti"].xcom_pull(
        key="gold_file",
        task_ids="gold_aggregate"
    )

    # 2. Validar archivo
    if not gold_file: 
        raise ValueError("Gold file not found in XCom")

    
     # 3. Fecha de Ejecución
    
    execution_date = context["data_interval_start"].strftime("%Y-%m-%d %H:%M:%S")

    # 4. Leer CSV
    df = pd.read_csv(gold_file)

    # 5. Conexión Airflow
    conn = BaseHook.get_connection("flight_snowflake")

    # 6. Conexión Snowflake
    sf_conn = snowflake.connector.connect(
        user=conn.login,
        password=conn.password,
        account=conn.extra_dejson["account"],
        warehouse=conn.extra_dejson.get("warehouse"),
        database=conn.extra_dejson.get("database"),
        schema=conn.schema,
        role=conn.extra_dejson.get("role")
    )

    # 7. SQL MERGE
    merge_sql = """
        MERGE INTO FLIGHTS_KPIS tgt
        USING (
            SELECT
                TO_TIMESTAMP(%s) AS WINDOW_START,
                %s AS ORIGIN_COUNTRY,
                %s AS TOTAL_FLIGHTS,
                %s AS AVG_VELOCITY,
                %s AS ON_GROUND
        ) src
        ON tgt.WINDOW_START = src.WINDOW_START
           AND tgt.ORIGIN_COUNTRY = src.ORIGIN_COUNTRY

        WHEN MATCHED THEN
            UPDATE SET
                TOTAL_FLIGHTS = src.TOTAL_FLIGHTS,
                AVG_VELOCITY = src.AVG_VELOCITY,
                ON_GROUND = src.ON_GROUND,
                LOAD_TIME = CURRENT_TIMESTAMP()

        WHEN NOT MATCHED THEN
            INSERT (
                WINDOW_START,
                ORIGIN_COUNTRY,
                TOTAL_FLIGHTS,
                AVG_VELOCITY,
                ON_GROUND
            )
            VALUES (
                src.WINDOW_START,
                src.ORIGIN_COUNTRY,
                src.TOTAL_FLIGHTS,
                src.AVG_VELOCITY,
                src.ON_GROUND
            );
    """

    # 8. Ejecutar MERGE (Aquí se usa la variable de arriba)
    with sf_conn.cursor() as cursor:
        for _, row in df.iterrows():
            cursor.execute(
                merge_sql,
                (
                    execution_date, # <--- Aquí la usa
                    row["origin_country"],
                    int(row["total_flights"]),
                    float(row["avg_velocity"]),
                    int(row["on_ground"]),
                ),
            )

    # 9. Cerrar conexión
    sf_conn.close()