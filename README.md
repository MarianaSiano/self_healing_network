# Sistema de Telemetria e Auto-Cura de Redes Desagregadas (5G/O-RAN)

Este projeto implementa um sistema distribuído de monitoramento e recuperação autônoma para redes de próxima geração (5G/O-RAN). Ele utiliza uma arquitetura assíncrona para coletar métricas de componentes de rede e aplica Machine Learning para identificar anomalias e executar ações de auto-cura.

## 🚀 Tecnologias e Arquitetura

*   **Linguagem:** Python 3.13.5 (Aproveitando melhorias de performance e JIT).
*   **Processamento Distribuído:** [Celery](https://docs.celeryq.dev/) com [Redis](https://redis.io/) como Message Broker.
*   **Coleta Assíncrona:** `aiohttp` para requisições paralelas de alto desempenho aos nós de rede.
*   **Inteligência Artificial:** `Scikit-Learn` utilizando o algoritmo **Isolation Forest** para detecção de anomalias em tempo real.
*   **Simulação de Rede:** `FastAPI` simulando APIs de telemetria de componentes O-DU/O-CU.

## 🏗️ Como o Sistema Funciona

1.  **Coleta de Dados:** O `main.py` (Orquestrador) envia tarefas para o Celery em intervalos regulares. Os Workers do Celery utilizam `aiohttp` para coletar métricas de múltiplos nós simultaneamente sem bloquear a execução.

2.  **Análise com IA:** Os dados coletados são enviados para o `analyzer.py`. Um modelo de Machine Learning (Isolation Forest) verifica se os padrões de tráfego (throughput, latência, perda de pacotes) divergem do comportamento normal treinado.

3.  **Auto-Cura (Self-Healing):** Se uma anomalia for detectada, o sistema dispara um webhook assíncrono que simula o isolamento do nó problemático e o redirecionamento da carga de trabalho para evitar a degradação do serviço.

---

## 🛠️ Configuração e Instalação

### 1. Pré-requisitos
Certifique-se de ter o **Redis** instalado e rodando (via Docker ou localmente):

```bash
# Exemplo via Docker
docker run -d -p 6379:6379 redis
```

### 2. Instalação

```bash
# Criar ambiente virtual
python3.13 -m venv venv

# Ativar ambiente
# No Linux/macOS:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

---

## 🚦 Execução (Necessário 3 Terminais)

Para simular o ecossistema completo, execute os comandos abaixo em terminais separados:

### Terminal 1: Simular Nó de Rede (O-DU)

Este componente simula a API de um rádio ou unidade distribuída enviando métricas.

```bash
python simulator/node_api.py
```

### Terminal 2: Iniciar Worker do Celery

Este é o motor de processamento que executará a coleta assíncrona e a lógica de IA.

```bash
celery -A app.celery_app worker --loglevel=info
```

### Terminal 3: Iniciar Orquestrador de Telemetria

Este script inicia o loop de monitoramento contínuo

```bash
python main.py
```

## 🔬 Observações sobre o Python 3.13.5

Este projeto foi otimizado para o **Python 3.13.5**, tirando proveito de:

- **Melhorias no Interpretador:** Otimizações no Coletor de Lixo (GC) e suporte ao JIT experimental, que reduzem a latência em sistemas de monitoramento em tempo real.

- **Performance Async:** A integração de `asyncio` dentro de tarefas Celery permite que um único worker gerencie centenas de requisições de telemetria a nós de rede de forma extremamente eficiente.

## 📊 Fluxo de Dados (ML)

O modelo `Isolation Forest` é treinado com dados de tráfego nominal.

- **Entrada:** Throughput (Mbps), Latência (ms), Packet Loss (%).
- **Saídas:** 1 (Normal), -1 (Anomalia/Ataque/Falha).
- **Ação:** Em caso de -1, o sistema aciona o método `trigger_self_healing`.

---

### Dica Adicional: Estrutura de Arquivos
Para que os comandos acima funcionem, garanta que sua estrutura de pastas esteja assim:

```text
self_healing_network/
├── app/
│   ├── __init__.py
│   ├── celery_app.py
│   ├── collector.py
│   ├── analyzer.py
│   └── actions.py
├── simulator/
│   └── node_api.py
├── main.py
├── requirements.txt
└── README.md
```