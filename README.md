# ✈️ Real-Time-Flight-Operations-Data-Pipeline
__________________________________________________________________________________________________________________________________________________________________________________________________________________
## Medallion Architecture & Apache Airflow
![image](https://github.com/user-attachments/assets/f0a50d5a-f393-46c5-9f4d-fcb225124282) ![image](https://github.com/user-attachments/assets/6a780008-692d-4012-9b76-ea56a9d40e9f) ![image](https://github.com/user-attachments/assets/f788e431-b8b3-493a-9007-85cc79080b4a) ![image](https://github.com/user-attachments/assets/a2ca1b3f-d25a-468b-b048-aaddd199e04c) 

🎯 Descripción del Proyecto
Pipeline de ingeniería de datos de extremo a extremo (End-to-End) diseñado para ingerir datos de vuelos en tiempo real desde la API pública de OpenSky Network.

El objetivo de este proyecto es demostrar cómo se construye un flujo de datos casi en tiempo real (intervalos de 30 minutos) aplicando las mejores prácticas de la industria: Arquitectura Medallion (Bronze, Silver, Gold), procesamiento idempotente, orquestación robusta y carga incremental en un Data Warehouse (Snowflake) lista para ser consumida por herramientas de BI.

🏗️ Arquitectura del Pipeline (Data Flow)
graph TD    API[🌐 OpenSky Network REST API] -->|Extracción cada 30 min| Airflow    subgraph "🛸 Apache Airflow Orchestrator"        direction TB        B[📦 BRONZE LAYER\nIngesta cruda de JSON]        S[🧹 SILVER LAYER\nLimpieza y normalización con Pandas]        G[📊 GOLD LAYER\nAgregación de KPIs por país]        L[❄️ LOAD\nLógica UPSERT / MERGE]                B --> S --> G --> L    end    Airflow --> B    L --> SF[❄️ Snowflake Data Cloud\nTabla: FLIGHTS_KPIS]    SF --> BI[📈 Power BI / Tableau\nDashboards de Negocio]


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
