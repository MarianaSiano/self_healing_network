import numpy as np
from sklearn.ensemble import IsolationForest
from .celery_app import app
from .actions import trigger_self_healing

# Mock de dados históricos para treinar o modelo (Simplificado)
# Em produção, isso seria carregado de um DB (Prometheus/InfluxDB)
X_train = np.array([
    [1000, 10, 0.01], [950, 12, 0.02], [1050, 8, 0.01], [980, 11, 0.015]
])
clf = IsolationForest(contamination=0.1, random_state=42)
clf.fit(X_train)

@app.task(name="tasks.analyze_metrics")
def analyze_metrics(data):
    metrics = np.array([[data['throughput'], data['latency'], data['packet_loss']]])
    prediction = clf.predict(metrics)
    
    if prediction[0] == -1:  # Anomalia detectada
        return trigger_self_healing.delay(data).get()
    return f"Node {data['node_id']} operando normalmente."