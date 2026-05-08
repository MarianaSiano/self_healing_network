# 🌐 Disaggregated Network Self-Healing System (Python & ML)

Est sistema demonstra uma arquitetura de telemetria distribuída e autocura (Self-Healing) para redes modernas (5G/O-RAN), utilizando processamento assíncrono e inteligência artificial.

## 🚀 Tecnologias Utilizadas

- **Linguagem:** Pyhton 3.13.5
- **Coleta Assíncrona:** `aiohttp` com `asyncio.TaskGroup` para máxima perfomance I/O
- **Mensageria & Workers:** `Celery` com `Redis` para processamento distribuído
- **Inteligêcia Artificial:** `Scikit-Learn (Isolation Forest)` para detecção de anomalias não supervisionada.
- **Simulação:** Endpoints HTTP simulado unidades de rede (DUs)

## 🧩 Arquitetura de Autocura

1. **Coleta Paralela:** O orquestrador dispara requisições simultâneas para todos os nós da rede.

2. **Triagem por IA:** Os dados são enviados para workers Celery. O modelo de ML analisa o tráfego (Throughput, Latência, Perda de Pacotes, CPU).

3. **Identificação de Anomalias:** O algoritmo *Isolation Forest* identifica se o comportamento do nó foge do padrão estatístico (ex: ataque DDoS, falha de hardware ou esgotamento de recursos).

4. **Ação Autônoma:** Ao detectar uma falha, o sistema dispara uma tarefa de autocura que simula o isolamento do nó e o redirecionamento de carga via webhooks.

## 🚀 Como Executar

**1. Instale as dependências:**
```bash
pip install -r requirements.txt
```