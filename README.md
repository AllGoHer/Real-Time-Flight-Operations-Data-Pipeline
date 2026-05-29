# ✈️ Real-Time-Flight-Operations-Data-Pipeline
__________________________________________________________________________________________________________________________________________________________________________________________________________________
## Medallion Architecture & Apache Airflow
![image](https://github.com/user-attachments/assets/f0a50d5a-f393-46c5-9f4d-fcb225124282) ![image](https://github.com/user-attachments/assets/6a780008-692d-4012-9b76-ea56a9d40e9f) ![image](https://github.com/user-attachments/assets/f788e431-b8b3-493a-9007-85cc79080b4a) ![image](https://github.com/user-attachments/assets/a2ca1b3f-d25a-468b-b048-aaddd199e04c) 

🎯 Descripción del Proyecto
Pipeline de ingeniería de datos de extremo a extremo (End-to-End) diseñado para ingerir datos de vuelos en tiempo real desde la API pública de OpenSky Network.

El objetivo de este proyecto es demostrar cómo se construye un flujo de datos casi en tiempo real (intervalos de 30 minutos) aplicando las mejores prácticas de la industria: Arquitectura Medallion (Bronze, Silver, Gold), procesamiento idempotente, orquestación robusta y carga incremental en un Data Warehouse (Snowflake) lista para ser consumida por herramientas de BI.

🏗️ Arquitectura del Pipeline (Data Flow)


```markdown
### 🏗️ Arquitectura del Pipeline (Data Flow)

```text
🌐 [OpenSky Network REST API] (Datos de vuelos en tiempo real)
   │
   ▼ (Disparado cada 30 minutos)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛸 APACHE AIRFLOW ORCHESTRATOR (DAG: flights_ops_medallion_pipe)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   │
   ▼
❄️ [Snowflake Data Cloud] (Almacenamiento Analítico)
   │
   ▼
📈 [Power BI / Tableau] (Consumo para paneles de negocio)


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
