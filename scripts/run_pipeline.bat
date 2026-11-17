@echo off
echo Starting dbt pipeline orchestration...
cd /d E:\Proyecto\llm_analytics_transform
C:\Users\waltw\AppData\Roaming\Python\Python311\Scripts\dbt.exe run
C:\Users\waltw\AppData\Roaming\Python\Python311\Scripts\dbt.exe test
echo Pipeline execution completed.