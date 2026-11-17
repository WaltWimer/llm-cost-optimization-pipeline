\# LLM Cost Optimization \& Telemetry Pipeline



\## Overview

As organizations scale the internal use of Large Language Models (LLMs), tracking token consumption, latency, and hardware utilization becomes a critical operational requirement. This repository contains an end-to-end batch Data Engineering pipeline designed to provide full observability and cost optimization for a local LLM cluster serving multiple developers. 



By centralizing telemetry, this pipeline translates raw engineering metrics into clear financial dashboards, enabling data-driven decisions on model routing, hardware allocation, and API cost management without relying on external commercial APIs.



\## Architecture \& Tech Stack

This pipeline executes an Extract, Load, and Transform (ELT) process utilizing a modern data stack:

\* \*\*LLM Proxy \& Gateway:\*\* LiteLLM (Intercepts traffic and collects telemetry)

\* \*\*Transactional Database:\*\* PostgreSQL (Telemetry persistence)

\* \*\*Data Extraction \& Orchestration:\*\* Python (`psycopg2`, OS Task Scheduler)

\* \*\*Data Warehouse:\*\* Snowflake (Immutable RAW layer)

\* \*\*Data Transformation:\*\* dbt (Data Build Tool - Star Schema architecture)

\* \*\*Visualization:\*\* Power BI (Executive dashboards and ROI calculation)



\## Pipeline Workflow

1\. \*\*Telemetry Capture:\*\* Developer requests (e.g., from VS Code Continue.dev or Cursor) are routed through a central proxy to a local 20x RTX 5070 Ti GPU cluster. The proxy logs execution metadata (tokens, latency, model used, user ID) into an internal PostgreSQL database.

2\. \*\*Data Extraction:\*\* A scheduled Python ETL script connects directly to the PostgreSQL database to extract incremental batch logs, avoiding synthetic data generation in production environments.

3\. \*\*Cloud Loading:\*\* The raw telemetry data is bulk-inserted into Snowflake under the `RAW\_LLM\_LOGS` table, serving as the immutable data layer.

4\. \*\*Data Modeling (dbt):\*\* dbt is utilized to clean, test, and transform the raw logs. It standardizes the data into a Star Schema, mapping corporate LLM models (Performance tiers/TPS) and developers into Dimension tables (`dim\_models`, `dim\_users`), and processing log records into a central Fact table (`fct\_llm\_generations`).

5\. \*\*Analytics \& BI:\*\* Power BI connects to the curated Snowflake models to generate executive dashboards. These track exact usage volume, average latency, and calculate the financial Return on Investment (ROI) by benchmarking local generation against commercial API pricing (e.g., GPT-4o, Claude 3.5 Sonnet).



\## Repository Structure

`text

├── docs/                      # Architectural diagrams and documentation

├── scripts/                   # Data extraction and ingestion logic

│   ├── generator.py               

│   ├── snowflake\_ingestion.py     

│   └── run\_pipeline.bat           

└── README.md

