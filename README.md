# ✈️ Real-Time-Flight-Operations-Data-Pipeline
________________________________________________________________________________________________________________________________________________________________________________________________________________
## Medallion Architecture & Apache Airflow
![image](https://github.com/user-attachments/assets/f0a50d5a-f393-46c5-9f4d-fcb225124282) ![image](https://github.com/user-attachments/assets/6a780008-692d-4012-9b76-ea56a9d40e9f) ![image](https://github.com/user-attachments/assets/f788e431-b8b3-493a-9007-85cc79080b4a) ![image](https://github.com/user-attachments/assets/a2ca1b3f-d25a-468b-b048-aaddd199e04c) 

### 🔥Descripción del Proyecto 🔥

Pipeline de ingeniería de datos de extremo a extremo (End-to-End) diseñado para ingerir datos de vuelos en tiempo real desde la API pública de OpenSky Network.

🎯 **El objetivo** de este proyecto es demostrar cómo se construye un flujo de datos casi en tiempo real (intervalos de 30 minutos) aplicando las mejores prácticas de la industria: Arquitectura Medallion (Bronze, Silver, Gold), procesamiento idempotente, orquestación robusta y carga incremental en un Data Warehouse (Snowflake) lista para ser consumida por herramientas de BI.

________________________________________________________________________________________________________________________________________________________________________________________________________________
## 🏗️ Arquitectura del Pipeline (Data Flow)
________________________________________________________________________________________________________________________________________________________________________________________________________________

![image](https://github.com/user-attachments/assets/3c006f8e-5249-4cbc-941b-a8d55a4d8b36)

________________________________________________________________________________________________________________________________________________________________________________________________________________

## ⚙️ Características Técnicas Destacadas 
________________________________________________________________________________________________________________________________________________________________________________________________________________

* **Ingesta Real de API:** Cero datos falsos. Extracción real de endpoints públicos con manejo de timeouts y validación de respuestas HTTP.
* **Arquitectura Medallion Estricta:** Separación física y lógica de responsabilidades (Raw → Cleaned → Business Aggregations).
* **Idempotencia & Upsert Lógico:** Uso de la sentencia MERGE en Snowflake para garantizar que ejecutar el pipeline 2 veces en la misma ventana de tiempo no duplique los datos (Update if exists, Insert if not).
* **Orquestación Production-Ready:**
  * Uso de XComs para pasar rutas de archivos dinámicas entre tareas sin hardcodeo.
  * Configuración de reintentos (retries) y backoff.
  * Gestión dinámica de directorios y particiones basadas en execution_date.
* **Código Modular:** Separación total entre la definición del DAG (flight-pipeline.py) y la lógica de negocio (scripts/), facilitando el testing unitario y el mantenimiento.
____________________________________________________________________________________________________________________________________________________________________________________________________________________________
## 🛠️ Tech Stack
____________________________________________________________________________________________________________________________________________________________________________________________________________________________
* **Orquestación:** Apache Airflow (Docker Compose)
* **Procesamiento:** Python, Pandas.
* **Almacenamiento de Datos (DWH):** Snowflake.
* **Integración:** REST API, snowflake-connector-python, Airflow BaseHook.

____________________________________________________________________________________________________________________________________________________________________________________________________________________________
## 📂 Estructura del Proyecto.
____________________________________________________________________________________________________________________________________________________________________________________________________________________________

![image](https://github.com/user-attachments/assets/7920af67-dbd9-45ec-a3af-225de0bd0b32)

____________________________________________________________________________________________________________________________________________________________________________________________________________________________
## 📊 Vista de los Datos (Gold Layer Output)
____________________________________________________________________________________________________________________________________________________________________________________________________________________________

El resultado final de este pipeline es una tabla de KPIs lista para análisis. Ejemplo de un snapshot agregado por país:

![image](https://github.com/user-attachments/assets/83e7be38-b98c-4cda-9a07-2c9db3e24e15)

(Estos datos son actualizados incrementalmente en Snowflake cada 30 minutos con la ventana de tiempo exacta de ejecución).

____________________________________________________________________________________________________________________________________________________________________________________________________________________________
## 🚀 Cómo ejecutar este proyecto localmente
____________________________________________________________________________________________________________________________________________________________________________________________________________________________

* **Prerrequisitos:** Tener Docker y Docker Compose instalados.

**1. Clonar el repositorio:**

 bash:

       git clone https://github.com/AllGoHer/flight-ops-airflow.git
       cd flight-ops-airflow


**2. Configurar credenciales de Snowflake (Opcional - Solo para la capa Gold):**
  * Si deseas ejecutar la carga a Snowflake, crea una conexión en la UI de Airflow (Admin -> Connections) llamada flight_snowflake con tus credenciales y el JSON extra con account, warehouse, database, y role.

**3. Levantar el entorno con Docker Compose:**

 bash:

       docker-compose up -d

**4. Acceder a Airflow y disparar el DAG:**
  * Abre tu navegador en http://localhost:8080 (User: airflow / Pass: airflow).
  * Busca el DAG flights_ops_medallion_pipe.
  * Haz clic en "Trigger DAG" para ver el flujo completo en acción.

________________________________________________________________________________________________________________________________________________________________________________________________________________
## 🔥 DESARROLLO DEL PROYECTO PASO A PASO (Guia Practica) 🔥
________________________________________________________________________________________________________________________________________________________________________________________________________________

1. Creamos las carpetas del proyecto la cual la llamaremos Flight-ops-airflow y sus subcarpetas data, scripts y, dags . Asimismo, en la carpeta data creamos las carpetas de la arquitectura medallón, las cuales son bronce, silver y, Gold.

2. Abrimos nuestro Docker desktop y luego nuestro editor de código, en este caso, Visual Studio Code, en el cual enlazaremos nuestra carpeta flight-ops-airflow.
   
3. En VSCode creamos un archivo <mark>Docker-compose.yaml</mark> e ingresamos el siguiente código para que pueda conectar el código con Docker.

   Código: [Docker-compose.yaml](https://github.com/AllGoHer/Real-Time-Flight-Operations-Data-Pipeline/blob/main/docker-compose.yaml) 


4. Ahora en la terminal levantamos Docker-compose

    Terminal:

              Cd flight-ops-airflow

    Terminal:

              docker-compose up –build


   ![image](https://github.com/user-attachments/assets/d392562c-28e1-4314-ade6-1da792205167)

 
  
  Y luego podemos ver en Docker desktop en la pestaña containers la creación del container.
  
   
   ![image](https://github.com/user-attachments/assets/32fbda83-e9e5-485f-9265-fa6ae551ff7c)



5. Ahora verificamos la conexión al puerto (loclahost:8080) haciendo click en 8080:8080 de Docker desktop.
   
   ![image](https://github.com/user-attachments/assets/428dc4e6-0147-46ad-b48c-b786397e1aca)



   Luego ingresamos nuestra contraseña y nos mostrará la UI
   

    ![image](https://github.com/user-attachments/assets/86a1d06e-e70c-45bd-872b-d7bf18a926a0)


________________________________________________________________________________________________________________________________________________________________________________________________________________
### ![image](https://github.com/user-attachments/assets/4825147e-660a-480e-96fa-079b9b03f485) Capa Bronce – ingesta de datos.
________________________________________________________________________________________________________________________________________________________________________________________________________________

* Ahora en el archivo scripts del VSC, creamos el archivo bronze_ingest.py con el siguiente código.

  Código: [bronze_ingest.py](https://github.com/AllGoHer/Real-Time-Flight-Operations-Data-Pipeline/blob/main/scripts/bronze_ingest.py)


* luego creamos otro archivo en la carpeta dags nombrándolo como flight-pipeline.py con el siguiente código.

   Código: [flight-pipeline.py](https://github.com/AllGoHer/Real-Time-Flight-Operations-Data-Pipeline/blob/main/dags/flight-pipeline.py)

* Luego de guardar los dos archivos, vamos a la IU de Airflow (localhost:8080) para verificar la ingestión de datos.

   ![image](https://github.com/user-attachments/assets/edae5f1e-080d-4138-8f82-bb284fe7166a)

   ![image](https://github.com/user-attachments/assets/ab9afb99-58a3-44a2-9743-bd920e5d5817)

  Y también verificamos en visual studio code que se haya guardado los datos automáticamente.


     ![image](https://github.com/user-attachments/assets/5819f1de-20aa-4827-ae27-9987e87b1090)

________________________________________________________________________________________________________________________________________________________________________________________________________________
### ![image](https://github.com/user-attachments/assets/909edaf5-0063-4d28-a4c8-d96eafcb3665) Capa Plata – Transformación de datos.
________________________________________________________________________________________________________________________________________________________________________________________________________________

Creamos el archivo silver_transform.py e ingresamos el siguiente código.

 Código: [silver_transform.py](https://github.com/AllGoHer/Real-Time-Flight-Operations-Data-Pipeline/blob/main/scripts/silver_transform.py)

* ahora verificamos que todo este conforme en el proceso de transformación de datos, yendo al IU de Airflow(localhost:8080).

  ![image](https://github.com/user-attachments/assets/74c1d45f-853c-49f1-bbe1-8065a03288b9)

* Y también verificamos en nuestro editor de código VSC, en la carpeta data y dentro del carpeta silver ya se encuentre el archivo de datos csv.
  
   ![image](https://github.com/user-attachments/assets/5218a9f9-675b-40cb-aa0f-f44bbb5151a9)

   ![image](https://github.com/user-attachments/assets/36932ba9-55d7-488c-abb4-0d86358b9b2e)

________________________________________________________________________________________________________________________________________________________________________________________________________________
### ![image](https://github.com/user-attachments/assets/1598351b-2a03-4fd9-a1ed-ed366a3f102c) Capa Oro 
________________________________________________________________________________________________________________________________________________________________________________________________________________

* Ahora creamos la carpeta gold_aggregate.py y ingresamos el siguiente código.

 Código: [gold_aggregate.py](https://github.com/AllGoHer/Real-Time-Flight-Operations-Data-Pipeline/blob/main/scripts/gold_aggregate.py)

* guardamos el archivo y nos vamos al localhost:8080 y ejecutamos tigger o play de Airflow UI 

   ![image](https://github.com/user-attachments/assets/bc4229ce-2a72-4d81-9f7f-6fb448e3ebff)


  Y luego verificamos en VSC si ya se creó el archivo csv en el archivo gold.

  ![image](https://github.com/user-attachments/assets/78368a21-a88f-448d-8d1b-77e99fae7d5e)

________________________________________________________________________________________________________________________________________________________________________________________________________________
### ![image](https://github.com/user-attachments/assets/46d17126-ad57-4be4-a792-8097d317bfa6) WAREHOUSE LOAD
________________________________________________________________________________________________________________________________________________________________________________________________________________

Crearemos en VSC un archivo llamado load_gold_to_snowflake con el siguiente código.

Código:

        import pandas pandas
        import snowflake.connector
        from airflow.hooks.base import BaseHook

        def load_gold_to_snowflake(**context):
            gold_file = context["ti"].xcom_pull(
                key = "gold_file",
                task_ids = "gold_aggregate"
            )

            if not gold_file:
                raise ValueError("Gold file not found in xcom")
    
            execution_date = context["data_interval_start"],strftime("%Y%m%d-%H%M%S")

           df = pd.read_csv(gold_file)

        conn = BaseHook.get_connection("flight_snowflake")

* luego abrimos snowflake y creamos la siguiente base de datos, esquema y, tabla FLIGHTS_KPIS.

codigo:

        CREATE DATABASE FLIGHTS
        CREATE SCHEMA KPI;

        CREATE TABLE FLIGHTS_KPIS (
            WINDOW_START TIMESTAMP_NTZ,
            ORIGIN_COUNTRY VARCHAR(50),
            TOTAL_FLIGHTS INTEGER,
            AVG_VELOCITY FLOAT,        
            ON_GROUND INTEGER,
            LOAD_TIME TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (WINDOW_START, ORIGIN_COUNTRY)
        );

  
  ![image](https://github.com/user-attachments/assets/326051d4-ede2-49be-836f-0d5d8b85b7ef)


 Verificamos que se haya creado la tabla en la pestaña de catálogos de Snowflake
 
  ![image](https://github.com/user-attachments/assets/a26d2f87-1d4a-4d17-b38c-047adda51077)

  Por el momento esta vacía, pero ya esta creada la tabla, la cual estaremos conformando luego de la conexión con snowflake.

•	Luego pasamos a Airflow UI (localhost:8080) y hacemos click Admin y en la eventana emergente seleccionamos conexiones.

  ![image](https://github.com/user-attachments/assets/5f0f695c-c2c4-49e8-ad85-29e9179e8b6b)

 Y llenamos los datos solicitados.
 
  ![image](https://github.com/user-attachments/assets/289f6001-5782-4b97-b867-46dbac5a7491)

 Ahora vamos a la parte inferior izquierda de snowflake donde esta tu administrador de cuenta y hacemos click derecho y en la ventana emergente seleccionaremos Detalles de sección y hacemos click en copy to   clipboard para copiar el contexto de Snowflake.  
  
  ![image](https://github.com/user-attachments/assets/a6deb62b-9a43-4606-8d31-1555cd012842)

  Ahora pegamos ese código en el navegador y seleccionamos solo la parte resaltada de azul después de las dos barras(//) y antes del punto snowflake(.snowflake)
  
  ![image](https://github.com/user-attachments/assets/b9ebaf78-a5ae-4615-8b96-43c1e9a80800)

  Luego volvemos a la página de Airflow y pasamos ese dato seleccionado anteriormente en la casilla de Account.

  ![image](https://github.com/user-attachments/assets/e50251ca-8b99-4ee5-8a1a-f63d3f7a6d6e)

  Ahora snowflake en la pestaña de compute verificamos que compute_wh este inicializado.

  ![image](https://github.com/user-attachments/assets/716548b0-03f4-442b-a5a6-c1c8bbf523a1)

  Continuamos completando los datos y luego le damos a guardar (save).

  ![image](https://github.com/user-attachments/assets/662abfdd-c6a5-4435-bbc9-9f5cf263260f)

  Ahora regresamos a nuestro VSC en la carpeta <mark>load_gold_to_snowflake</mark> y agregamos al final el siguiente código para la Ejecución de MERGE (Upsert) a Snowflake.

  Código: [load_gold_to_snowflake.py](https://github.com/AllGoHer/Real-Time-Flight-Operations-Data-Pipeline/blob/main/scripts/load_gold_to_snowflake.py)

  * luego verificamos la conexión en Airflow.
  
   ![image](https://github.com/user-attachments/assets/dd204c1b-4452-4818-a063-173371fb9e93)

   Y ahora en snowflake ya se puede ver la carga de los datos.

   ![image](https://github.com/user-attachments/assets/713b24f9-71ee-42ee-8c4f-ef0b64254621)

   ![image](https://github.com/user-attachments/assets/e08fc69e-db16-446a-876d-444ee6f1ebe1)

   ![image](https://github.com/user-attachments/assets/2c98e600-5e13-457e-b4e8-abf219ceeeb0)

   ![image](https://github.com/user-attachments/assets/21296e5d-f587-4687-9992-8cd5e55bb1c0)

  ![image](https://github.com/user-attachments/assets/51a52f04-c912-4202-a688-673ea8ed79a1)

  ![image](https://github.com/user-attachments/assets/91d759d0-8305-4341-b480-6bb7dc3f76ba)

  ![image](https://github.com/user-attachments/assets/1eee5e55-ef2f-4ec7-9eba-caccb8651d03)

________________________________________________________________________________________________________________________________________________________________________________________________________________
 ## 🔍 Hallazgos y Conclusiones de Alto Impacto
 _______________________________________________________________________________________________________________________________________________________________________________________________________________
 
**Hallazgo 1:** La asimetría absoluta del cielo (El monopolio estadounidense)

* **El dato:** Estados Unidos tiene casi 5,000 vuelos en una sola ventana de 30 minutos. El segundo lugar es Canadá con ~400. USA representa más del 60% del tráfico mundial monitoreado.
  
**Conclusión de negocio:** Cualquier anomalía (tormenta, fallo de sistema, cierre de espacio aéreo) en EE. UU. tiene un impacto causal desproporcional en las operaciones globales de aerolíneas. Es el nodo central de la red mundial.
  
**Hallazgo 2:** "Operational Friction" (Fricción Operativa) en países específicos

**El dato:** Si miras países pequeños, Estonia tiene 8 vuelos y los 8 están en tierra (100%). Georgia tiene 2 vuelos y los 2 en tierra. Por el contrario, Egipto tiene 20 vuelos y 0 en tierra.

**Conclusión de negocio:** El KPI "Vuelos en Tierra" no significa que los aviones estén estacionados en un hangar por la noche; significa que están en pista, taxiendo o retenidos. Un 100% de Ground Ops en una ventana de tiempo sugiere cuellos de botella de despegue, congestión terminal o bloqueos meteorológicos locales.

**Hallazgo 3:** La velocidad como proxy del tipo de tráfico (Hub vs. Origins)

**El dato:** Egipto (~296 km/h avg), Arabia Saudita (~251 km/h avg) y Rusia (~257 km/h avg) tienen las velocidades más altas. Ecuador (~3 km/h avg), Italia (~224 km/h avg en la segunda ventana) y Portugal tienen las más bajas.

**Conclusión de negocio:** Velocidades altas indican "Cruising" (vuelos de larga distancia, intercontinentales). Velocidades bajas indican aviones en fases de aproximación, espera (holding patterns) o vuelos regionales cortos. Esto permite clasificar aeropuertos implícitamente como Hubs de conexión vs. Origines/destinos finales.

**Hallazgo 4:** Caída abrupta del tráfico global

**El dato:** Entre las 23:30 del día 28 y las 00:00 del día 29, el tráfico global cayó de ~8,400 aviones a ~7,900 aviones (-6% aprox).

**Conclusión de negocio:** Esto refleja el ritmo circadiano de la aviación comercial. A medida que Asia y Europa entran en sus horas nocturnas de menor actividad, la carga global disminuye, manteniendo el peso principalmente en América.
























