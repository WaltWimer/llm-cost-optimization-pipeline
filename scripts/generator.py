import csv
import random
from datetime import datetime, timedelta
import uuid

# Base de TPS para tarjetas de 16GB VRAM (5070 Ti o equivalente en granja local)
modelos_info = {
    'qwen2.5:14b': {'base_tps': 75.0, 'varianza': 10.0},
    'qwen2.5:7b': {'base_tps': 105.0, 'varianza': 15.0},
    'llama3:8b': {'base_tps': 100.0, 'varianza': 12.0},
    'mistral-nemo:12b': {'base_tps': 85.0, 'varianza': 10.0}
}

usuarios = [f"Dev_{str(i).zfill(2)}" for i in range(1, 21)]
data = []
fecha_actual = datetime.now()

for _ in range(5000):
    usuario = random.choice(usuarios)
    modelo = random.choice(list(modelos_info.keys()))
    info = modelos_info[modelo]
    
    # Realismo: 70% consultas cortas, 30% contexto masivo (código/documentos)
    if random.random() < 0.7:
        tokens_in = random.randint(10, 500)
        tokens_out = random.randint(50, 400)
    else:
        tokens_in = random.randint(2000, 12000)
        tokens_out = random.randint(300, 1500)
        
    # Realismo: Mayor contexto de entrada = caída en TPS (hasta 20 TPS menos)
    degradacion_contexto = (tokens_in / 12000) * 20
    tps_final = info['base_tps'] - degradacion_contexto + random.uniform(-info['varianza']/2, info['varianza']/2)
    tps_final = round(max(tps_final, 15.0), 2) # Evitar que caiga a números absurdos
    
    tiempo_segundos = round(tokens_out / tps_final, 2)
    fecha_chat = fecha_actual - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    
    data.append([
        str(uuid.uuid4()),
        usuario,
        fecha_chat.strftime("%Y-%m-%d %H:%M:%S"),
        modelo,
        tokens_in,
        tokens_out,
        tiempo_segundos,
        tps_final
    ])

with open('llm_local_empresa.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id_chat', 'usuario', 'timestamp', 'modelo', 'tokens_prompt', 'tokens_respuesta', 'tiempo_generacion_segundos', 'tps_promedio'])
    writer.writerows(data)

print("Dataset corporativo generado: 'llm_local_empresa.csv'")