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

```markdown
```.
🌐 [OpenSky Network REST API] (Datos de vuelos en tiempo real)
   │
   ▼ (Disparado cada 30 minutos)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛸 APACHE AIRFLOW ORCHESTRATOR (DAG: flights_ops_medallion_pipe)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   │
   ├─▶ 📦 1. BRONZE LAYER
   │      └── Extracción cruda y guardado como JSON (Raw)
   │
   ├─▶ 🧹 2. SILVER LAYER
   │      └── Limpieza, renombrado de columnas y filtrado (CSV)
   │
   ├─▶ 📊 3. GOLD LAYER
   │      └── Agrupación por país y cálculo de KPIs (CSV)
   │
   └─▶ ❄️ 4. WAREHOUSE LOAD
          └── Ejecución de MERGE (Upsert) a Snowflake
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   │
   ▼
❄️ [Snowflake Data Cloud] (Almacenamiento Analítico)
   │
   ▼
📈 [Power BI / Tableau] (Consumo para paneles de negocio)

------------------------------------------------------------------------------------------------------------------

  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
  │ 🌐 OpenSky  │      │ 📦 BRONZE   │      │ 🧹 SILVER   │      │ 📊 GOLD     │      │ ❄️ Snowflake│
  │  REST API   │─────▶│  Raw JSON   │─────▶│  Clean CSV  │─────▶│  KPIs CSV   │─────▶│ MERGE Table │
  └─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘      └──────┬──────┘
                                                                                            │
                                                                                            ▼
                                                                                    ┌─────────────┐
                                                                                    │ 📈 Power BI │
                                                                                    │  Dashboards │
                                                                                    └─────────────┘

------------------------------------------------------------------------------------------------------------------ ```.

________________________________________________________________________________________________________________________________________________________________________________________________________________

## Características Técnicas Destacadas (Por qué esto es diferente a un tutorial)
________________________________________________________________________________________________________________________________________________________________________________________________________________
Ingesta Real de API: Cero datos falsos. Extracción real de endpoints públicos con manejo de timeouts y validación de respuestas HTTP.
Arquitectura Medallion Estricta: Separación física y lógica de responsabilidades (Raw 
→
 Cleaned 
→
 Business Aggregations).
Idempotencia & Upsert Lógico: Uso de la sentencia MERGE en Snowflake para garantizar que ejecutar el pipeline 2 veces en la misma ventana de tiempo no duplique los datos (Update if exists, Insert if not).
Orquestación Production-Ready:
Uso de XComs para pasar rutas de archivos dinámicas entre tareas sin hardcodeo.
Configuración de reintentos (retries) y backoff.
Gestión dinámica de directorios y particiones basadas en execution_date.
Código Modular: Separación total entre la definición del DAG (flight-pipeline.py) y la lógica de negocio (scripts/), facilitando el testing unitario y el mantenimiento.
🛠️ Tech Stack
Orquestación: Apache Airflow (Docker Compose)
Procesamiento: Python, Pandas
Almacenamiento de Datos (DWH): Snowflake
Integración: REST API, snowflake-connector-python, Airflow BaseHook
📂 Estructura del Proyecto




![image]()

![image]()

![image]()

![image]()

![image]()

![image]()

![image]()

![image]()

![image]()

![image]()
