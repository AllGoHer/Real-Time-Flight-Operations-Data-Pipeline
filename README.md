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
































