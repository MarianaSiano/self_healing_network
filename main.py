import time
from app.collector import collect_and_process

NODES = [
    "http://localhost:8001/metrics",
    # Adicione mais nós simulados aqui
]

def run_telemetry_loop():
    print("Iniciando monitoramento de rede (Pressione Ctrl+C para parar)...")
    while True:
        for node in NODES:
            # Despacha a tarefa para o worker Celery
            collect_and_process.delay(node)
        time.sleep(5) # Intervalo de telemetria

if __name__ == "__main__":
    run_telemetry_loop()