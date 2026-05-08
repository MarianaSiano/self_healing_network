import asyncio
import aiohttp
from .celery_app import app
from .analyzer import analyze_metrics

async def fetch_node_data(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=2) as response:
                return await response.json()
        except Exception as e:
            return {"error": str(e)}

@app.task(name="tasks.collect_and_process")
def collect_and_process(node_url):
    # Executa a coleta assíncrona dentro do worker síncrono do Celery
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(fetch_node_data(node_url))
    
    if "error" not in data:
        return analyze_metrics.delay(data).get()
    return f"Erro ao coletar de {node_url}"