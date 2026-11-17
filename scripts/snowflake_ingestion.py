import snowflake.connector
import csv
from datetime import datetime

conn = snowflake.connector.connect(
    user='',
    password='',
    account='',
    warehouse='COMPUTE_WH',
    database='LLM_ANALYTICS_DB',
    schema='RAW'
)

cur = conn.cursor()

datos = []
with open('llm_local_empresa.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header
    for row in csv_reader:
        # Parse whatever date format came from the CSV and convert to ISO standard
        raw_date = row[2]
        try:
            formatted_date = datetime.strptime(raw_date, '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                formatted_date = datetime.strptime(raw_date, '%m/%d/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                formatted_date = raw_date # Fallback if already matching

        # Rebuild row with the cleaned date
        updated_row = [row[0], row[1], formatted_date, row[3], row[4], row[5], row[6], row[7]]
        datos.append(updated_row)

insert_query = """
INSERT INTO RAW_LLM_LOGS 
(CHAT_ID, USER_ID, EVENT_TIMESTAMP, MODEL_NAME, PROMPT_TOKENS, COMPLETION_TOKENS, GENERATION_TIME_SECONDS, AVERAGE_TPS)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

print(f"Loading {len(datos)} records into Snowflake...")
cur.executemany(insert_query, datos)
print("Data ingestion complete.")

cur.close()
conn.close()