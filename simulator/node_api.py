from fastapi import FastAPI
import random
import uvicorn

app = FastAPI()

@app.get("/metrics")
async def get_metrics():
    # Simula métricas: throughput (Mbps), latency (ms), packet_loss (%)
    return {
        "node_id": "O-DU-01",
        "throughput": random.uniform(800, 1200),
        "latency": random.uniform(5, 15),
        "packet_loss": random.uniform(0, 0.1)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)