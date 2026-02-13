Real-Time Stocks Market Data Pipeline
Snowflake DBT Apache Airflow Python Kafka Docker Power BI

📌 Project Overview
This project demonstrates an end-to-end real-time data pipeline using the Modern Data Stack.
We capture live stock market data from an external API, stream it in real time, orchestrate transformations, and deliver analytics-ready insights — all in one unified project.

Architecture (1)

⚡ Tech Stack
Snowflake → Cloud Data Warehouse
DBT → SQL-based Transformations
Apache Airflow → Workflow Orchestration
Apache Kafka → Real-time Streaming
Python → Data Fetching & API Integration
Docker → Containerization
Power BI → Data Visualization
✅ Key Features
Fetching live stock market data (not simulated) from an API
Real-time streaming pipeline with Kafka
Orchestrated ETL workflow using Airflow
Transformations using DBT inside Snowflake
Scalable cloud warehouse powered by Snowflake
Analytics-ready Power BI dashboards
📂 Repository Structure
real-time-stocks-pipeline/
├── producer/                     # Kafka producer (Finnhub API)
│   └── producer.py
├── consumer/                     # Kafka consumer (MinIO sink)
│   └── consumer.py
├── dbt_stocks/models/
│   ├── bronze
│   │   ├── bronze_stg_stock_quotes.sql
│   │   └── sources.yml
│   ├── silver
│   │   └── silver_clean_stock_quotes.sql
│   └── gold
│       ├── gold_candlestick.sql
│       ├── gold_kpi.sql
│       └── gold_treechart.sql
├── dag/
│   └── minio_to_snowflake.py
├── docker-compose.yml            # Kafka, Zookeeper, MinIO, Airflow, Postgres
├── requirements.txt
└── README.md                     # Documentation
🚀 Getting Started
Clone this repo and set up environment
Start Kafka + Airflow services via Docker
Run the Python producer to fetch live stock data
Data flows into Snowflake → DBT applies transformations
Orchestrate everything with Airflow
Connect Power BI for visualization
⚙️ Step-by-Step Implementation
1. Kafka Setup
Configured Apache Kafka locally using Docker.
Created a stocks-topic to handle live stock market events.
Defined producers (API fetch) and consumers (pipeline ingestion).
2. Live Market Data Producer
Developed Python producer script stock_producer.py to fetch real-time stock prices from the Finnhub API using an API key.
Streams stock data into Kafka in JSON format.
Producer Code
3. Kafka Consumer → MinIO
Built Python consumer script stock_consumer.py to consume streaming data from Kafka.
Stored consumed data into MinIO buckets (S3-compatible storage).
Organized storage into folders for raw/bronze layer ingestion.
Consumer Code
4. Airflow Orchestration
Initialized Apache Airflow in Docker.
Created DAG (stock_pipeline_dag.py) to:
Load data from MinIO into Snowflake staging tables (Bronze).
Schedule automated runs every 1 minute.
Airflow DAGs
5. Snowflake Warehouse Setup
Created Snowflake database, schema, and warehouse.
Defined staging tables for Bronze → Silver → Gold layers.
SQL scripts available at:
Snowflake Setup
6. DBT Transformations
Configured DBT project with Snowflake connection.
Models include:
Bronze models → raw structured data
Silver models → cleaned, validated data
Gold models → analytical views (Candlestick, KPI, Tree Map)
7. Power BI Dashboard
Connected Power BI to Snowflake (Gold layer) using Direct Query.
Built:
Candlestick chart → stock market patterns
Tree chart → stock price trends
gauge charts → stock volume & total sales breakdown
KPI's → real-time sortable view
📊 Final Deliverables
Automated real-time data pipeline
Snowflake tables (Bronze → Silver → Gold)
Transformed analytics models with DBT
Orchestrated DAGs in Airflow
Power BI dashboard with live insights
